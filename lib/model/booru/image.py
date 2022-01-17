from lib.util.sql_table import *

class BooruImage(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'image'
    _props = {
        'id': 0,
        'name': '',
        'description': '',
        'thumbnail_generated': 0,
        'mime_type': '',
        'animated': 0,
        'extension': '',
        'upvote': 0,
        'downvote': 0,
        'score': 0,
        'fave': 0,
        'comment_count': 0,
        'wilson_score': 0,
        'uploader': '',
        'image_size': 0,
        'width': 0,
        'height': 0,
        'link_view': '',
        'link_source': '',
        'duration': 0,
        'delete_reason': '',
        'created_at': '',
        'updated_at': ''
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

    def extra_col(self):
        pass

    @classmethod
    def from_json(cls, js):
        rdict = {
            'id': js['id'],
            'name': js['name'],
            'description': js['description'],
            'thumbnail_generated': js['thumbnails_generated'],
            'mime_type': js['mime_type'],
            'animated': 1 if js['animated'] else 0,
            'extension': js['format'],
            'upvote': js['upvotes'],
            'downvote': js['downvotes'],
            'score': js['score'],
            'fave': js['faves'],
            'comment_count': js['comment_count'],
            'wilson_score': js['wilson_score'],
            'uploader': js['uploader'],
            'image_size': js['size'],
            'width': js['width'],
            'height': js['height'],
            'link_view': js['view_url'],
            'link_source': js['source_url'],
            'duration': js['duration'],
            'delete_reason': js['deletion_reason'],
            'created_at': js['created_at'],
            'updated_at': js['updated_at']
        }

        o = cls(data=rdict)
        return o

    def get_image(self, size_name):
        ls = self['sizes']
        ls_name = {
            'full': 'Full',
            'tall': 'Tall',
            'large': 'Large',
            'medium': 'Medium',
            'small': 'Small',
            'thumb': 'Thumbnail',
            'thumb_small': 'Small Thumbnail',
            'thumb_tiny': 'Tiny Thumbnail',
        }
        if (size_name in ls_name):
            size_name = ls_name[size_name]
        for sz in ls:
            if (sz.cols['name'] == size_name):
                return sz
        return None

class BooruImageSize(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'image_size'
    _props = {
        'image_id': 0,
        'link': '',
        'name': '',
        'size_index': 0
    }
    _primary = ['image_id', 'link']
    _auto_primary = False
    _reference = {}

    @classmethod
    def from_key_pair(cls, name, link, id, ext = ''):
        ls_size_index = {
            'full': 8,
            'tall': 7,
            'large': 6,
            'medium': 5,
            'small': 4,
            'thumb': 3,
            'thumb_small': 2,
            'thumb_tiny': 1,
        }
        ls_name = {
            'full': 'Full',
            'tall': 'Tall',
            'large': 'Large',
            'medium': 'Medium',
            'small': 'Small',
            'thumb': 'Thumbnail',
            'thumb_small': 'Small Thumbnail',
            'thumb_tiny': 'Tiny Thumbnail',
        }
        rdict = {
            'image_id': id,
            'link': link,
            'name': ls_name[name] if (name in ls_name) else name,
            'size_index': ls_size_index[name] if (name in ls_size_index) else 0
        }
        if (ext == 'webm' and (name.find('thumb') != -1)):
            rdict['link'] = rdict['link'].replace('.webm', '.gif')
        
        o = cls(data=rdict)
        return o

class BooruImageHistory(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'history'
    _props = {
        'image_id': 0,
        'view_timestamp': 0,
        'view_count': 0
    }
    _primary = ['image_id']
    _auto_primary = False
    _reference = {}