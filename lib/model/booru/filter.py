from lib.util.sql_table import *
import lib.util.db_util as db_util

class BooruFilter(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'booru_filter'
    _props = {
        'id': 0,
        'name': '',
        'color': '',
        'show_count': 0,
        'spoiler_count': 0,
        'hide_count': 0,
        'spoiler_list': '',
        'filter_text': '',
        'sort_index': 0
    }
    _primary = ['id']
    _auto_primary = True
    _reference = {}
    
    def parse_query(self, text):
        text = text.strip(' \n')
        lsq = [s.strip(' \n') for s in text.split(',')]
        ls_spoiler = []
        self.cols['show_count'] = 0
        self.cols['hide_count'] = 0
        self.cols['spoiler_count'] = 0
        self.cols['filter_text'] = text
        for t in lsq:
            if t[0] in ['+', '-', '`']:
                if (t[0] == '+'):
                    self.cols['show_count'] += 1
                elif (t[0] == '-'):
                    self.cols['hide_count'] += 1
                elif (t[0] == '`'):
                    self.cols['spoiler_count'] += 1
                    ls_spoiler.append(t[1:])
            else:
                self.cols['show_count'] += 1
        self.cols['spoiler_list'] = ','.join(ls_spoiler)

    @classmethod
    def add_filter(cls, name, text):
        conn = db_util.make_conn(cls._dbfile)
        max_sort = db_util.db_get_single_cell(conn, 'select max(sort_index) from booru_filter')

        o = cls()

        o.cols['sort_index'] = (max_sort or 0) + 1
        o.cols['name'] = name
        o.parse_query(text)

        o.cols['id'] = cls.insert(o, conn=conn)

        conn.close()
        return o

    def update_filter(self, name, text):
        self.cols['name'] = name
        self.parse_query(text)
        BooruFilter.update(self)

    @classmethod
    def swap_filter_order(cls, id1, id2):
        conn = db_util.make_conn(cls._dbfile)
        f1 = cls.find_id(id1, conn=conn)
        f2 = cls.find_id(id2, conn=conn)
        if (f1 == None or f2 == None): return
        t = f1['sort_index']
        f1['sort_index'] = f2['sort_index']
        f2['sort_index'] = t
        cls.update(f1, ['sort_index'], conn=conn)
        cls.update(f2, ['sort_index'], conn=conn)
        conn.close()

