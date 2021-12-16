from lib.util.sql_table import *
import lib.provider.anonpone as anonpone
import lib.util.util as util
import html2text

class Cyoa(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'cyoa'
    _props = {
        'id': 0,
        'name': '',
        'short_name': '',
        'description': '',
        'image_link': '',
        'cyoa_type': 0,
        'board': '',
        'chan': '',
        'is_live': 0,
        'status': 0,
        'last_post_time': 0,
        'first_post_time': 0,
        'quest_time': 0,
        'total_image': 0,
        'total_post': 0,
        'total_thread': 0,
        'total_fanart': 0,
        'word_count': 0,
        'lewd_exist': 0,
        'image_path': ''
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

    def extra_col(self):
        self.cols['first_post_date_str'] = util.date_str_from_timestamp(self.cols['first_post_time'], '%d-%m-%Y')
        self.cols['last_post_date_str'] = util.date_str_from_timestamp(self.cols['last_post_time'], '%d-%m-%Y')
        self.cols['total_image_per'] = f'{self.cols["total_image"] / self.cols["total_post"] * 100:.2f}%'
        h = html2text.HTML2Text()
        h.ignore_links = True
        self.cols['description'] = h.handle(self.cols['description'])

    @classmethod
    def from_json(cls, json:dict):
        rdict = {
            'id': json['_cid'],
            'name': json['_title'],
            'short_name': json['_shortname'],
            'description': json['_description'],
            'image_link': anonpone.image_link(json['_filename']),
            'cyoa_type': json['_type'],
            'board': json['_boardcode'],
            'chan': json['_channame'],
            'is_live': int(json['_live']),
            'status': int(json['_status']),
            'last_post_time': json['_lastPost']['_date'],
            'first_post_time': json['_firstPost']['_date'],
            'quest_time': json['_stats']['questTime'],
            'total_image': json['_stats']['totalImages'],
            'total_post': json['_stats']['totalPosts'],
            'total_thread': json['_stats']['totalThreads'],
            'total_fanart': 0 if json['_stats']['totalFanart'] is None else json['_stats']['totalFanart'],
            'word_count':json['_stats']['totalWordCount'],
            'lewd_exist':json['_stats']['lewdExists'],
            'image_path':None
        }
        o = cls(data=rdict)
        return o
