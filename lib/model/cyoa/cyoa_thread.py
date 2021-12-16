from lib.util.sql_table import *


class Thread(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'thread'
    _props = {
        'id': 0,
        'total_reply': 0,
        'total_post': 0,
        'total_word': 0,
        'thread_time': 0,
        'title': '',
        'board': '',
        'chan': '',
        'is_canon': 0,
        'thread_date': 0,
        'current_page': 0
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

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
