from lib.util.sql_table import *
import lib.util.util as util


class Thread(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'thread'
    # TODO: Rewrte prop list
    _props = {
        'id': 0,
        'title': '',
        'is_canon': 0,
        'thread_date': 0,
        'thread_image': '',
        'op_name': '',
        'chan': '',
        'board': '',
        'total_op_post': 0,
        'total_post': 0,
        'total_word': 0,
        'thread_time': 0,
        'current_page': 0
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

    @classmethod
    def from_json(cls, json:dict):
        rdict = {
            'id': json['_tid'],
            'title': json['_subject'],
            'is_canon': int(json['_canon']),
            'thread_date': int(json['_date']),
            'thread_image': None,
            'op_name': None,
            'chan': json['_channame'] if (json['_channame'].find('chan') != -1) else json['_channame'] + 'chan',
            'board': json['_boardcode'],
            'total_op_post': json['_stats'].get('threadPosts', None), # everything in ['_stats'] is already int
            'total_post': int(json['_stats'].get('postCount', '0')), # ... except this
            'total_word': json['_stats'].get('threadWords', None), # also ocationally missing every field 
            'thread_time': json['_stats'].get('threadTime', 0), # SEROIUSLY, WHAT KIND OF SHITTY DB HE BEEN USING ANYWAY
            'current_page': int(json['_page'])
        }
        o = cls(data=rdict)
        return o

    def extra_col(self):
        self.cols['thread_date_str'] = util.date_str_from_timestamp(self.cols['thread_date'], '%d-%m-%Y(%a) %H:%M:%S')

    def get_op_image(self, save = True):
        post = self.get_ref_one('posts', save_result=save, save_name='op_post')
        if (post != None):
            return post.get_ref_one('images', save_result=save, save_name='op_image')['link']
        return self.cols['thread_image']

    def get_title(self, alt_name, index = 0):
        return self.cols['title'] if self.cols['title'] not in ['', None] else (f'{alt_name}{"" if index == None else " #" + str(index)}')
    
    def get_post_ids(self) -> list:
        sql = f'select p.id from thread t join post p on t.id = p.thread_id where t.id in (select ct.thread_id from cyoa_thread ct where ct.cyoa_id = ?)'
        result = db_util.db_get_all(self._dbfile, sql, (self.cols['id'],))
        return [x[0] for x in result]

class CyoaThread(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'cyoa_thread'
    _props = {
        'cyoa_id': 0,
        'thread_id': 0
    }
    _primary = ['cyoa_id', 'thread_id']
    _auto_primary = False
    _reference = {}
