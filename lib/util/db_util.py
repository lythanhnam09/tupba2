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
