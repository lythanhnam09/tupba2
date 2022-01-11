import sqlite3
import logging


#logging = logging.Logger('db_util', logging.INFO)
# logging.basicConfig(level=logging.INFO)

def db_close(conn):
    conn.commit()
    conn.close()

def make_conn(dbconn):
    if (isinstance(dbconn, str)): return sqlite3.connect(dbconn)
    else: return dbconn

def close_temp_conn(dbconn, conn):
    if (isinstance(dbconn, str)): conn.close()

def db_exec_script(dbfile:str, sqlfile):
    logging.info(f'{sqlfile}: Reading SQL script')
    txt = ''
    with open(sqlfile, 'rt') as sqlf:
        txt = sqlf.read()
    logging.info(f'{dbfile}: Executing script \'{sqlfile}\'')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    cur.executescript(txt)
    conn.commit()
    close_temp_conn(dbfile, conn)

def db_exec(dbfile, sql, param:tuple = (), constraint = False):
    logging.info(f'{dbfile}: {sql}')
    logging.debug(f'-> {param}')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    if (constraint):
        logging.info(f'{dbfile}: pragma foreign_keys = on')
        cur.execute('pragma foreign_keys = on')
    cur.execute(sql, param)
    conn.commit()
    close_temp_conn(dbfile, conn)

def db_exec_multi(dbfile, sql, param:list = None, constraint = False):
    logging.info(f'{dbfile}: {sql}')
    logging.debug(f'-> {param}')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    if (constraint):
        logging.info(f'{dbfile}: pragma foreign_keys = on')
        cur.execute('pragma foreign_keys = on')
    cur.executemany(sql, param)
    conn.commit()
    close_temp_conn(dbfile, conn)

def db_get_all(dbfile, sql, param:tuple = ()) -> list:
    logging.info(f'{dbfile}: {sql}')
    logging.debug(f'-> {param}')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    ls = cur.fetchall()
    cur.close()
    conn.commit()
    close_temp_conn(dbfile, conn)
    return ls

def db_get_iter(dbfile, sql, param:tuple = ()):
    logging.info(f'{dbfile}: {sql}')
    logging.debug(f'-> {param}')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    return cur

def db_get_single_row(dbfile, sql, param:tuple = ()) -> tuple:
    logging.info(f'{dbfile}: {sql}')
    logging.debug(f'-> {param}')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    res = cur.fetchone()
    conn.commit()
    close_temp_conn(dbfile, conn)
    return res

def db_get_single_cell(dbfile, sql, param:tuple = ()):
    logging.info(f'{dbfile}: {sql}')
    logging.debug(f'-> {param}')
    conn = make_conn(dbfile)
    cur = conn.cursor()
    cur.execute(sql, param)
    res = cur.fetchone()
    if (res != None): res = res[0]
    conn.commit()
    close_temp_conn(dbfile, conn)
    return res

class DBBatch:
    def __init__(self, dbfile, constraint = False):
        self.dbfile = dbfile
        self.ls_query:list = []
        self.ls_result:list = []
        self.constraint = constraint
        self.cur = None
        self.conn = make_conn(dbfile)

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

    def run(self, close = True, commit = True, get_result = True) -> list:
        # self.conn = sqlite3.connect(self.dbfile)
        self.cur = self.conn.cursor()
        if (self.constraint):
            logging.info(f'DBBatch:{self.dbfile}: pragma foreign_keys = on')
            self.cur.execute('pragma foreign_keys = on')
        if (get_result):
            result = []
        for query in self.ls_query:
            logging.info(f'DBBatch:{self.dbfile}: {query["q"]}')
            logging.debug(f' -> {query["p"]}')
            res = query['f'](self.cur, query['q'], query['p'])
            if (get_result): result.append(res)
        
        if (commit): self.conn.commit()
        if (close): close_temp_conn(self.dbfile, self.conn)
        self.ls_query.clear()
        if (get_result): return result

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
    

