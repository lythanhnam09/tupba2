from lib.util.sql_table import *


class Fanart(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'fanart'
    _props = {
        'id': 0,
        'cyoa_id': 0,
        'title': '',
        'artist': '',
        'is_lewd': 0,
        'link': '',
        'offline_link': '',
        'status_code': 0
    }
    _primary = ['id']
    _auto_primary = True
    _reference = {}

    @classmethod
    def from_json(cls, js):
        # print(js)
        rdict = {
            'id': 0,
            'cyoa_id': js['cyoa_id'],
            'title': js['title'],
            'artist': js['artist'],
            'is_lewd': 1 if js['lewd'] else 0,
            'link': js['url'],
            'offline_link': None,
            'status_code': 0
        }
        o = cls(data=rdict)
        return o
