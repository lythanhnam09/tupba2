from lib.util.sql_table import *
from lib.util.parser import PostProcessor
import lib.util.sql_command as sql_command
import lib.provider.anonpone as anonpone
import lib.util.util as util
import html2text
import re

class PostReplyTo(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'post_reply_to'
    _props = {
        'post_id': 0,
        'reply_id': 0
    }
    _primary = ['post_id', 'reply_id']
    _auto_primary = False
    _reference = {}

class PostReplyBy(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'post_reply_by'
    _props = {
        'post_id': 0,
        'reply_id': 0
    }
    _primary = ['post_id', 'reply_id']
    _auto_primary = False
    _reference = {}

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

    @classmethod
    def from_json(cls, json:dict): # TODO: AND here !!!
        rdict = {
            'id': int(json['_pid']),
            'thread_id': int(json['_tid']),
            'title': '',
            'username': json['_name'],
            'tripcode': json['_trip'],
            'comment_plain': json.get('_comment', ''), # and then it null sometime... (I know this won't solve it but just to make sure)
            'comment_html': '',
            'is_qm': int(json['_QM']),
            'post_date': int(json['_date'])
        } 
        o = cls(data=rdict)
        return o

    def process_html(self):
        processor = PostProcessor(self.cols['comment_plain'], self)
        self.cols['comment_html'] = processor.process()

    def extra_col(self):
        self.cols['post_date_str'] = util.date_str_from_timestamp(self.cols['post_date'], '%d-%m-%Y(%a) %H:%M:%S')
        if (self.cols['comment_plain'] == None): self.cols['comment_plain'] = ''
        h = html2text.HTML2Text()
        h.ignore_links = True
        self.cols['comment_plain'] = h.handle(self.cols['comment_plain'])

    def add_replies(self, ls_id:list):
        batch = db_util.DBBatch(self._dbfile)
        ls_rt = [(self.cols['id'], id) for id in ls_id]
        ls_rb = [(id, self.cols['id']) for id in ls_id]
        sql = sql_command.insert('post_reply_to', PostReplyTo.get_props_name(), or_ignore=True)
        batch.add_exec_multi(sql, ls_rt)
        sql = sql_command.insert('post_reply_by', PostReplyBy.get_props_name(), or_ignore=True)
        batch.add_exec_multi(sql, ls_rb)
        batch.run()

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

    @classmethod
    def from_json(cls, json:dict):
        rdict = {
            'post_id': int(json['_pid']),
            'alt_id': 0,
            'alt_name': 'Normal',
            'filename': None,
            'link': anonpone.image_link(json['_filename']) if json['_filename'] != None else None,
            'offline_link': None,
            'status_code': 0
        }
        o = cls(data=rdict)
        return o

    @classmethod
    def from_lewd_json(cls, json:dict):
        # if json['_lewd'] != '1':
        #     return None
        rdict = {
            'post_id': int(json['_pid']),
            'alt_id': 1,
            'alt_name': 'Lewd',
            'filename': None,
            'link': anonpone.image_link(json['_filenameLewd']) if json['_filenameLewd'] != None else None,
            'offline_link': None,
            'status_code': 0
        }
        o = cls(data=rdict)
        return o

    @classmethod
    def from_desu_json(cls, json:dict):
        rdict = {
            'post_id': int(json['num']),
            'alt_id': 0,
            'alt_name': 'Normal',
            'filename': json['media']['media_filename'],
            'link': json['media']['media_link'],
            'offline_link': None,
            'status_code': 0
        }
        o = cls(data=rdict)
        return o
