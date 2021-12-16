import sqlite3
import logging


#logging = logging.Logger('db_util', logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

def db_close(conn):
    conn.commit()
    conn.close()

def db_exec_script(dbfile, sqlfile):
    logging.debug(f'{sqlfile}: Reading SQL script')
    txt = ''
    with open(sqlfile, 'rt') as sqlf:
        txt = sqlf.read()
    logging.debug(f'{dbfile}: Executing script \'{sqlfile}\'')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.executescript(txt)
    conn.commit()
    conn.close()

def db_exec(dbfile, sql, param:tuple = (), constraint = False):
    logging.debug(f'{dbfile}: {sql} -> {param}')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    if (constraint):
        logging.debug(f'{dbfile}: pragma foreign_keys = on')
        cur.execute('pragma foreign_keys = on')
    cur.execute(sql, param)
    conn.commit()
    conn.close()

def db_exec_multi(dbfile, sql, param:list = None, constraint = False):
    logging.debug(f'{dbfile}: {sql} -> {param}')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    if (constraint):
        logging.debug(f'{dbfile}: pragma foreign_keys = on')
        cur.execute('pragma foreign_keys = on')
    cur.executemany(sql, param)
    conn.commit()
    conn.close()

def db_get_all(dbfile, sql, param:tuple = ()) -> list:
    logging.debug(f'{dbfile}: {sql} -> {param}')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    ls = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return ls

def db_get_iter(dbfile, sql, param:tuple = ()):
    logging.debug(f'{dbfile}: {sql} -> {param}')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    return cur

def db_get_single_row(dbfile, sql, param:tuple = ()) -> tuple:
    logging.debug(f'{dbfile}: {sql} -> {param}')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res

def db_get_single_cell(dbfile, sql, param:tuple = ()):
    logging.debug(f'{dbfile}: {sql} -> {param}')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    res = cur.fetchone()
    if (res != None): res = res[0]
    conn.commit()
    conn.close()
    return res

class DBBatch:
    def __init__(self, dbfile, constraint = False):
        self.dbfile = dbfile
        self.ls_query:list = []
        self.ls_result:list = []
        self.constraint = constraint
        self.cur = None
        self.conn = None

    def _get_all(self, cur, sql, param):
        cur.execute(sql, param)
        ls = cur.fetchall()
        return ls

    def _get_one(self, cur, sql, param):
        cur.execute(sql, param)
        res = cur.fetchone()
        return res

    def _get_one_cell(self, cur, sql, param):
        cur.execute(sql, param)
        res = cur.fetchone()
        return res[0] if res != None else None

    def _exec(self, cur, sql, param):
        cur.execute(sql, param)
        return cur.lastrowid

    def _exec_multi(self, cur, sql, param):
        cur.executemany(sql, param)
        return None

    def add_get_all(self, sql:str, param:tuple = ()):
        self.ls_query.append({'f': self._get_all, 'q': sql, 'p': param})

    def add_get_one(self, sql:str, param:tuple = ()):
        self.ls_query.append({'f': self._get_one, 'q': sql, 'p': param})

    def add_get_one_cell(self, sql:str, param:tuple = ()):
        self.ls_query.append({'f': self._get_one_cell, 'q': sql, 'p': param})

    def add_exec(self, sql:str, param:tuple = (), contraint=False):
        self.ls_query.append({'f': self._exec, 'q': sql, 'p': param})

    def add_exec_multi(self, sql:str, param:list = [], contraint=False):
        self.ls_query.append({'f': self._exec_multi, 'q': sql, 'p': param})

    def run(self, commit = True, close = True, get_result = True) -> list:
        self.conn = sqlite3.connect(self.dbfile)
        self.cur = self.conn.cursor()
        if (self.constraint):
            logging.debug(f'DBBatch:{self.dbfile}: pragma foreign_keys = on')
            self.cur.execute('pragma foreign_keys = on')
        if (get_result):
            result = []
        for query in self.ls_query:
            logging.debug(f'DBBatch:{self.dbfile}: {query["q"]} -> {query["p"]}')
            res = query['f'](self.cur, query['q'], query['p'])
            if (get_result): result.append(res)
        
        if (commit): self.conn.commit()
        if (close): self.conn.close()
        self.ls_query.clear()
        if (get_result): return result

    def commit(self):
        self.cur.commit()

    def close(self):
        self.conn.close()
    

