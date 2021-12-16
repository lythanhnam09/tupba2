from lib.util.sql_table import *


class Fanart(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'fanart'
    _props = {
        'id': 0,
        'cyoa_id': 0,
        'title': '',
        'artist': '',
        'link': '',
        'offline_link': '',
        'status_code': 0
    }
    _primary = ['id']
    _auto_primary = True
    _reference = {}
