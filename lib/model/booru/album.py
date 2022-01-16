from lib.util.sql_table import *

class BooruAlbum(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'album'
    _props = {
        'id': 0,
        'thumbnail_id': 0,
        'name': '',
        'color': ''
    }
    _primary = ['id']
    _auto_primary = True
    _reference = {}

class BooruAlbumImage(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'album_image'
    _props = {
        'album_id': 0,
        'image_id': 0,
        'sort_index': 0
    }
    _primary = ['album_id', 'image_id']
    _auto_primary = False
    _reference = {}
