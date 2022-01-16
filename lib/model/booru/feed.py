from lib.util.sql_table import *

class BooruFeed(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'feed'
    _props = {
        'id': 0,
        'name': '',
        'color': '',
        'show_count': 0,
        'spoiler_count': 0,
        'hide_count': 0,
        'filter_text': ''
    }
    _primary = ['id']
    _auto_primary = True
    _reference = {}

