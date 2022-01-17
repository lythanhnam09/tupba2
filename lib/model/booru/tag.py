from lib.util.sql_table import *
import lib.util.sql_command as sql_command 

class BooruTag(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'tag'
    _props = {
        'id': 0,
        'name': '',
        'color': '',
        'sort_index': 0,
        'description': '',
    }
    _primary = ['id']
    _auto_primary = True
    _reference = {}

    @classmethod
    def from_name(cls, name:str):
        rdict = {
            'id': 0,
            'name': name,
            'color': 'tag-def',
            'sort_index': 150,
            'description': '',
        }
        if (name in ['explicit', 'safe', 'questionable', 'suggestive']):
            rdict['color'] = 'tag-type'
            rdict['sort_index'] = 10
        if (name.find(':') != -1 and len([s.strip() for s in name.split(':') if s != '']) > 1):
            rdict['color'] = 'tag-category'
            rdict['sort_index'] = 50
        if (name.startswith('artist:')):
            rdict['color'] = 'tag-artist'
            rdict['sort_index'] = 30
        if (name.startswith('comic:')):
            rdict['color'] = 'tag-comic'
            rdict['sort_index'] = 45
        if (name.startswith('art pack:')):
            rdict['color'] = 'tag-artpack'
            rdict['sort_index'] = 40
        if (name.startswith('oc:')):
            rdict['color'] = 'tag-oc'
            rdict['sort_index'] = 47

        return cls(data=rdict)

class BooruImageTag(SQLTable):
    _dbfile = 'data/booru.db'
    _table_name = 'image_tag'
    _props = {
        'image_id': 0,
        'tag_id': 0
    }
    _primary = ['image_id', 'tag_id']
    _auto_primary = False
    _reference = {}
