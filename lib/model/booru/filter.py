from lib.util.sql_table import *

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