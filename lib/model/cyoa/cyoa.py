from lib.util.sql_table import *
from lib.model.cyoa.cyoa_thread import Thread
import lib.provider.anonpone as anonpone
import lib.util.util as util
import html2text
import re
import sqlite3

class Cyoa(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'cyoa'
    _props = {
        'id': 0,
        'name': '',
        'short_name': '',
        'description': '',
        'image_link': '',
        'cyoa_type': 0,
        'board': '',
        'chan': '',
        'is_live': 0,
        'status': 0,
        'last_post_time': 0,
        'first_post_time': 0,
        'quest_time': 0,
        'total_image': 0,
        'total_post': 0,
        'total_thread': 0,
        'total_fanart': 0,
        'word_count': 0,
        'lewd_exist': 0,
        'image_path': '',
        'save_status': 0
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

    def extra_col(self):
        self.cols['first_post_date_str'] = util.date_str_from_timestamp(self.cols['first_post_time'], '%d-%m-%Y')
        self.cols['last_post_date_str'] = util.date_str_from_timestamp(self.cols['last_post_time'], '%d-%m-%Y')
        self.cols['total_image_per'] = f'{self.cols["total_image"] / self.cols["total_post"] * 100:.2f}%'
        h = html2text.HTML2Text()
        h.ignore_links = True
        self.cols['description'] = h.handle(self.cols['description'])

    @classmethod
    def find_shortname(cls, shortname):
        sql = sql_command.select(cls._table_name, where=['short_name'])
        r = db_util.db_get_single_row(cls._dbfile, sql, (shortname, ))
        if (r != None):
            return cls(row = r)
        return None

    @classmethod
    def from_json(cls, json:dict):
        rdict = {
            'id': json['_cid'],
            'name': json['_title'],
            'short_name': json['_shortname'],
            'description': json['_description'],
            'image_link': anonpone.image_link(json['_filename']),
            'cyoa_type': json['_type'],
            'board': json['_boardcode'],
            'chan': json['_channame'],
            'is_live': int(json['_live']),
            'status': int(json['_status']),
            'last_post_time': int(json['_lastPost']['_date']),
            'first_post_time': int(json['_firstPost']['_date']),
            'quest_time': json['_stats']['questTime'],
            'total_image': json['_stats']['totalImages'],
            'total_post': json['_stats']['totalPosts'],
            'total_thread': json['_stats']['totalThreads'],
            'total_fanart': 0 if json['_stats']['totalFanart'] is None else json['_stats']['totalFanart'],
            'word_count':json['_stats']['totalWordCount'],
            'lewd_exist':json['_stats']['lewdExists'],
            'image_path':None,
            'save_status': 0
        }
        o = cls(data=rdict)
        return o

    @classmethod
    def filter_tags(cls, query:str = '', page:int = 1, per_page:int = 20, order_by = ['last_post_time', 'desc']):
        lswhere = []
        if (query.strip(' ') == ''):
            lswhere = None
        else:
            lstag = [s.strip(' ') for s in query.split(',')]
            for tag in lstag:
                ls = re.split('[=:<>][>=]?', tag, maxsplit=1)
                # re.findall(pattern, string)
                if (len(ls) < 2):
                    lswhere.append([f'{tag!r}', 'in', ['(select t.name from cyoa_tag ct join tag t on ct.tag_id = t.id where ct.cyoa_id = c.id)']])
                else:
                    ls = list(re.findall('(\w+)([:<>=][>=]?)([\w ]+)', tag)[0])
                    if (ls[1] == ':'):
                        ls[1] = 'like'
                        ls[2] = f'%{ls[2]}%'
                    lswhere.append(ls)

        limit = per_page
        if (page < 1): page = 1
        offset = (page-1) * per_page
        
        batch = db_util.DBBatch(cls._dbfile)

        if (per_page == 0):
            sql = sql_command.select(cls._table_name + ' c', where=lswhere, order_by=order_by)
            batch.add_get_all(sql)
        else:
            sql = sql_command.select(cls._table_name + ' c', where=lswhere, order_by=order_by, limit=limit, offset=offset)
            batch.add_get_all(sql)
        
        sql = sql_command.select(cls._table_name + ' c', ['count(*)'], where=lswhere)
        batch.add_get_one_cell(sql)

        lsres = batch.run()

        data = [cls(row=r) for r in lsres[0]]
        total_count = lsres[1]
        page_count = math.ceil(total_count / per_page) if per_page > 0 else 1

        page = ResultPage(page, page_count, per_page, total_count, data)

        return page

    def check_steath_lewd(self, save_tag_data = True):
        have_lewd_tag = False
        for t in self.get_ref('tags', order_by=['sort_index', 'asc'], save_result=save_tag_data):
            if (t.cols['tag'].cols['name'] in ['lewd', 'lewd quest']):
                have_lewd_tag = True
                break
        self.cols['steath_lewd'] = (not have_lewd_tag) and (self.cols['lewd_exist'] == 1)

    def get_list_emty(self):
        sql = 'select t.* from thread t join cyoa_thread ct on t.id = ct.thread_id where ct.cyoa_id = ? and (select count(*) from post p where p.thread_id = t.id) = 0'
        ls = db_util.db_get_all(self._dbfile, sql, (self.cols['id'], ))
        result = [Thread(row=x) for x in ls]
        return result

    def get_image_list(self, is_qm:bool = None, alt_id:int = None, alt_op = None, thread_num:list = None, offline:bool = False, page:int = 1, per_page:int = 40):
        from lib.model.cyoa.post import PostImage
        conn = sqlite3.connect(self._dbfile)
        
        sql = 'select {0} from ((post_image pi join post p on pi.post_id = p.id) psi join thread t on psi.thread_id = t.id) ti join cyoa_thread ct on t.id = ct.thread_id where '
        
        lsexpr = []

        lsexpr.append(f'ct.cyoa_id = {self.cols["id"]}')

        if (is_qm != None):
            lsexpr.append(f'p.is_qm = {is_qm}')
        
        if (alt_id != None):
            if (alt_op == None):
                lsexpr.append(f'pi.alt_id = {alt_id}')
            else:
                alt_op = alt_op.replace(':', '=')
                lsexpr.append(f'pi.alt_id {alt_op} {alt_id}')
        
        if (thread_num != None):
            if (isinstance(thread_num, list) and len(thread_num > 1)):
                lsexpr.append(f't.id in ({",".join(thread_num)})')
            else:
                if (isinstance(thread_num, list) and len(thread_num == 1)):
                    lsexpr.append(f't.id = {thread_num[0]}')
                elif (not isinstance(thread_num, list)):
                    lsexpr.append(f't.id = {thread_num}')
        
        if (offline):
            lsexpr.append(f'pi.offline_link is not null')

        sql += ' and '.join(lsexpr)
        print(sql)
        qsql = sql.format('pi.*')
        countsql = sql.format('count(*)')

        limit = per_page
        if (page < 1): page = 1
        offset = (page-1) * per_page

        qsql += ' order by p.post_date asc, pi.alt_id'

        qsql += f' limit {limit} offset {offset}'

        ls = PostImage.get_raw(qsql, conn=conn)
        count = db_util.db_get_single_cell(conn, countsql)
        conn.close()

        page_count = math.ceil(count / per_page) if per_page > 0 else 1

        page_res = ResultPage(page, page_count, per_page, count, ls)

        return page_res