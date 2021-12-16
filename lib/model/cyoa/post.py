from lib.util.sql_table import *


class Post(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'post'
    _props = {
        'id': 0,
        'thread_id': 0,
        'title': '',
        'username': '',
        'tripcode': '',
        'comment_plain': '',
        'comment_html': '',
        'is_qm': 0,
        'post_date': 0
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

class PostImage(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'post_image'
    _props = {
        'post_id': 0,
        'alt_id': 0,
        'alt_name': '',
        'filename': '',
        'link': '',
        'offline_link': '',
        'status_code': 0
    }
    _primary = ['post_id', 'alt_id']
    _auto_primary = False
    _reference = {}
