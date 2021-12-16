import logging
from lib.util.sql_table import *
import lib.util.sql_command as sql_command
import sqlite3

class Tag(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'tag'
    _props = {
        'id': 0,
        'name': '',
        'color': '',
        'sort_index': 0
    }
    _primary = ['id']
    _auto_primary = False
    _reference = {}

    @classmethod
    def get_sort_index(cls, name:str):
        if (name.lower() in ['image', 'image only', 'text', 'text only']):
            return 10
        if (name.lower() in ['lewd', 'lewd quest']):
            return 20
        return 100

    @classmethod
    def get_color(cls, name:str):
        if (name.lower() in ['image', 'image only', 'text', 'text only']):
            return 'bg-primary'
        if (name.lower() in ['lewd', 'lewd quest']):
            return 'bg-pink'
        return 'bg-secondary'

    @classmethod
    def save_from_name_list(cls, js:list) -> list:
        result = []

        conn = conn = sqlite3.connect(cls._dbfile)
        cur = conn.cursor()
        sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=True), or_ignore=True)
        for t in js:
            if (t.strip(' ') == ''): continue
            tag = Tag(row=(0, t, cls.get_color(t), cls.get_sort_index(t)))
            val = tag.to_tuple(no_id=True)
            logging.debug(f'{cls._dbfile}: {sql} -> {val}')
            cur.execute(sql, val)
            tag['id'] = cur.lastrowid
            if (tag['id'] == 0):
                tsql = sql_command.select('tag', ['id'], ['name'])
                cur.execute(tsql, (tag['name'], ))
                res = cur.fetchone()
                if (res != None): tag['id'] = res[0]
            result.append(tag)
        conn.commit()
        conn.close()
        return result


class CyoaTag(SQLTable):
    _dbfile = 'data/cyoa.db'
    _table_name = 'cyoa_tag'
    _props = {
        'cyoa_id': 0,
        'tag_id': 0
    }
    _primary = ['cyoa_id', 'tag_id']
    _auto_primary = False
    _reference = {}

