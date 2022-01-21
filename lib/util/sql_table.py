import lib.util.sql_command as sql_command
import lib.util.db_util as db_util
import math
import logging


class SQLRef:
    def __init__(self, col, ref_table, ref_col):
        self.col = col
        self.ref_col = ref_col
        self.ref_table = ref_table

    def get(self, table, where = None, order_by = None, limit = None, offset = None, conn = None):
        return None

    def get_one(self, table, where = None, order_by = None, offset = None, conn = None):
        return None

    def get_page(self, table, page, per_page, where = None, order_by = None, conn = None):
        logging.warning(f'{self.__class__.__name__}.filter(): {self.__class__.__name__} does not have get_page()')
        return None

    def filter(self, table, where = None, order_by = None, limit = None, offset = None, conn = None):
        logging.warning(f'{self.__class__.__name__}.filter(): {self.__class__.__name__} does not have filter()')
        return None

class SQLRefOne(SQLRef):
    def __init__(self, col, ref_table, ref_col):
        super().__init__(col, ref_table, ref_col)

    def get(self, table, where = None, order_by = None, limit = None, offset = None, conn = None):
        return self.ref_table.find_id(table.cols[self.col], conn = conn)

    def get_one(self, table, where = None, order_by = None, offset = None, conn = None):
        return self.ref_table.find_id(table.cols[self.col], conn = conn)

class SQLRefMany(SQLRef):
    def __init__(self, col, ref_table, ref_col):
        super().__init__(col, ref_table, ref_col)

    def get(self, table, where = None, order_by = None, limit = None, offset = None, conn = None):
        if (where == None):
            where = []
        where.append([self.ref_col, table.cols[self.col]])
        return self.ref_table.select(where=where, order_by=order_by, limit=limit, offset=offset, conn = conn)

    def get_one(self, table, where = None, order_by = None, offset = None, conn = None):
        if (where == None):
            where = []
        where.append([self.ref_col, table.cols[self.col]])
        return self.ref_table.select_one(where=where, order_by=order_by, offset=offset, conn = conn)

    def get_page(self, table, page, per_page, where = None, order_by = None, conn = None):
        if (where == None):
            where = []
        where.append([self.ref_col, table.cols[self.col]])
        return self.ref_table.get_page(page, per_page, where=where, order_by=order_by, conn = conn)

    # def filter(self, table, where = None, order_by = None, limit = None, offset = None):
    #     if (where == None):
    #         where = []
    #     where.append([self.ref_col, table.cols[self.col]])
    #     return self.ref_table.select(where=where, order_by=order_by, limit=limit, offset=offset)

class SQLRefPivot(SQLRef):
    def __init__(self, col, ref_table, ref_col, pivot_ref):
        super().__init__(col, ref_table, ref_col)
        self.pivot_ref = pivot_ref

    def get(self, table, where = None, order_by = None, limit = None, offset = None, conn = None):
        name_t1 = 't1'
        name_t2 = 't2'

        ref_pivot:SQLRef = self.ref_table._reference[self.pivot_ref]
        t1 = f'{self.ref_table._table_name} {name_t1}'
        t2 = f'{ref_pivot.ref_table._table_name} {name_t2}'
        join_on = f'{name_t1}.{ref_pivot.col} = {name_t2}.{ref_pivot.ref_col}'
        if (where == None): where = []
        where.append([f't1.{self.ref_col}', table.cols[self.col]])
        sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by, limit=limit, offset=offset)

        qresult = db_util.db_get_all(conn or table._dbfile, sql)
        result = []

        for row in qresult:
            pos = len(ref_pivot.ref_table._props.keys())
            o2 = self.ref_table(row=row[pos:])
            o2.cols[self.pivot_ref] = ref_pivot.ref_table(row=row[:pos])

            result.append(o2)

        return result

    def get_one(self, table, where = None, order_by = None, offset = None, conn = None):
        name_t1 = 't1'
        name_t2 = 't2'

        ref_pivot:SQLRef = self.ref_table._reference[self.pivot_ref]
        t1 = f'{self.ref_table._table_name} {name_t1}'
        t2 = f'{ref_pivot.ref_table._table_name} {name_t2}'
        join_on = f'{name_t1}.{ref_pivot.col} = {name_t2}.{ref_pivot.ref_col}'
        if (where == None): where = []
        where.append([f't1.{self.ref_col}', table.cols[self.col]])
        sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by, limit=1, offset=offset)

        qresult = db_util.db_get_all(conn or table._dbfile, sql)

        if (len(qresult) > 0):
            pos = len(ref_pivot.ref_table._props.keys())
            o2 = self.ref_table(row=qresult[0][pos:])
            o2.cols[self.pivot_ref] = ref_pivot.ref_table(row=qresult[0][:pos])
            
            return o2
        return None

    def get_many(self, table, where = None, order_by = None, limit = None, offset = None, conn = None):
        name_t1 = 't1'
        name_t2 = 't2'

        ref_pivot:SQLRef = self.ref_table._reference[self.pivot_ref]
        t1 = f'{self.ref_table._table_name} {name_t1}'
        t2 = f'{ref_pivot.ref_table._table_name} {name_t2}'
        join_on = f'{name_t1}.{ref_pivot.col} = {name_t2}.{ref_pivot.ref_col}'
        if (where == None): where = []
        where.append([f't1.{self.ref_col}', table.cols[self.col]])
        sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by, limit=limit, offset=offset)

        qresult = db_util.db_get_all(conn or table._dbfile, sql)
        result = []

        for row in qresult:
            pos = len(ref_pivot.ref_table._props.keys())
            result.append(ref_pivot.ref_table(row=row[:pos]))

        return result

    def get_page(self, table, page_num, per_page, where = None, order_by = None, conn = None):
        limit = per_page
        if (page_num < 1): page_num = 1
        offset = (page_num-1) * per_page

        name_t1 = 't1'
        name_t2 = 't2'

        ref_pivot:SQLRef = self.ref_table._reference[self.pivot_ref]
        t1 = f'{self.ref_table._table_name} {name_t1}'
        t2 = f'{ref_pivot.ref_table._table_name} {name_t2}'
        join_on = f'{name_t1}.{ref_pivot.col} = {name_t2}.{ref_pivot.ref_col}'
        if (where == None): where = []
        where.append([f't1.{self.ref_col}', table.cols[self.col]])

        batch = db_util.DBBatch(conn or table._dbfile)
        if (per_page == 0):
            sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by)
            batch.add_get_all(sql)
        else:
            sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by, limit=limit, offset=offset)
            batch.add_get_all(sql)
        sql = sql_command.select_join([t1, t2], join_on, columns=['count(*)'], where=where)
        batch.add_get_one_cell(sql)
        qresult = batch.run()
        
        data = []

        for row in qresult[0]:
            pos = len(ref_pivot.ref_table._props.keys())
            o2 = self.ref_table(row=row[pos:])
            o2.cols[self.pivot_ref] = ref_pivot.ref_table(row=row[:pos])

            data.append(o2)

        total_count = qresult[1]
        page_count = math.ceil(total_count / per_page) if per_page > 0 and math.ceil(total_count / per_page) > 0 else 1

        page = ResultPage(page_num, page_count, per_page, total_count, data)

        return page

    def get_many_page(self, table, page_num, per_page, where = None, order_by = None, conn = None):
        limit = per_page
        if (page_num < 1): page_num = 1
        offset = (page_num-1) * per_page

        name_t1 = 't1'
        name_t2 = 't2'

        ref_pivot:SQLRef = self.ref_table._reference[self.pivot_ref]
        t1 = f'{self.ref_table._table_name} {name_t1}'
        t2 = f'{ref_pivot.ref_table._table_name} {name_t2}'
        join_on = f'{name_t1}.{ref_pivot.col} = {name_t2}.{ref_pivot.ref_col}'
        if (where == None): where = []
        where.append([f't1.{self.ref_col}', table.cols[self.col]])

        batch = db_util.DBBatch(conn or table._dbfile)
        if (per_page == 0):
            sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by)
            batch.add_get_all(sql)
        else:
            sql = sql_command.select_join([t1, t2], join_on, columns=[f'{name_t2}.*', f'{name_t1}.*'], where=where, order_by=order_by, limit=limit, offset=offset)
            batch.add_get_all(sql)
        sql = sql_command.select_join([t1, t2], join_on, columns=['count(*)'], where=where)
        batch.add_get_one_cell(sql)
        qresult = batch.run()
        
        data = []

        for row in qresult[0]:
            pos = len(ref_pivot.ref_table._props.keys())
            data.append(ref_pivot.ref_table(row=row[:pos]))

        total_count = qresult[1]
        page_count = math.ceil(total_count / per_page) if per_page > 0 and math.ceil(total_count / per_page) > 0 else 1

        page = ResultPage(page_num, page_count, per_page, total_count, data)

        return page

class ResultPage:
    def __init__(self, page_num:int, page_count:int, per_page:int, total_count:int, data:list):
        self.page_num = page_num
        self.page_count = page_count
        self.per_page = per_page
        self.total_count = total_count
        self.data = data
    
    def __repr__(self):
        return f'ResultPage({self.page_num=}, {self.page_count=}, {self.per_page=}, {self.total_count=}, data[{len(self.data)}])'

class SQLTable:
    _dbfile = ':memory:'
    _table_name = 'table'
    _props = {'id': 0}
    _primary = ['id']
    _auto_primary = False
    _reference = {} #dict of name and ref class {'image': SQLRefOne('image_id', Image, 'id'), ...}

    def __init__(self, row:tuple = None, data:dict = None):
        if (row != None):
            self.cols = self._props.copy()
            self.read_row(row)
            self.extra_col()
        else:
            if (data != None):
                self.cols = data.copy()
                self.extra_col()
            else:
                self.cols = self._props.copy()

    def __getitem__(self, key):
        if (not key in self.cols):
            return self.get_ref(key)
        return self.cols[key]

    def __setitem__(self, key, value):
        self.cols[key] = value

    def get(self, col, default_none = None):
        if (not col in self.cols):
            return self.get_ref(col)
        return self.cols[col] if self.cols[col] is not None else default_none

    def extra_col(self):
        pass

    def no_id_dict(self):
        d = self.cols.copy()
        for k in self._primary:
            d.pop(k)
        return d

    def read_row(self, row:tuple):
        cnt = 0
        rl = len(row)
        rp = len(self._props.keys())
        if (rl != rp):
            raise Exception(f'Table properties and row column count missmatch: {rl} - {rp}')
        for p in self._props.keys():
            self.cols[p] = row[cnt]
            cnt += 1

    @classmethod
    def get_props_name(cls, no_id = False, id_last = False, blacklist:list = None) -> list:
        lsprop = list(cls._props.keys())
        if (blacklist != None):
            for k in blacklist:
                lsprop.remove(k)
        if (no_id):
            return list(set(lsprop).difference(set(cls._primary)))
        else:
            if (id_last):
                return list(set(lsprop).difference(set(cls._primary))) + list(cls._primary)
            else:
                return lsprop

    def get_cols_name(self, no_id = False, id_last = False, blacklist:list = None) -> list:
        lsprop = self._props.keys()
        if (blacklist != None):
            for k in blacklist:
                lsprop.remove(k)
        if (no_id):
            return list(set(lsprop).difference(set(self._primary)))
        else:
            if (id_last):
                return list(set(lsprop).difference(set(self._primary))) + list(self._primary)
            else:
                return lsprop

    def to_tuple(self, no_id = False, id_last = False) -> tuple:
        lsname = self.get_cols_name(no_id, id_last)
        lsval = []
        for n in lsname:
            lsval.append(self.cols[n])
        return tuple(lsval)

    def id_value_tuple(self) -> tuple:
        return tuple([self.cols[n] for n in self._primary])

    def col_value_tuple(self, col:list) -> tuple:
        return tuple([self.cols[n] for n in col])

    @classmethod
    def get_raw(cls, sql:str, param:tuple = tuple(), conn = None):
        result = db_util.db_get_all(conn or cls._dbfile, sql, param)
        ls = [cls(row=o) for o in result]
        return ls

    @classmethod
    def find_id(cls, id, conn = None):
        id_val = id
        if (len(cls._primary) == 1 and type(id_val) != tuple):
            id_val = (id,)
        sql = sql_command.select(cls._table_name, where=cls._primary)
        r = db_util.db_get_single_row(conn or cls._dbfile, sql, id_val)
        if (r != None):
            return cls(row = r)
        return None

    @classmethod
    def find_or_insert(cls, o, where = None, order_by = None, offset = None, conn = None):
        conn = db_util.make_conn(conn)
        sql = sql_command.select(cls._table_name, where=where, order_by=order_by, limit=1, offset=offset)
        result = db_util.db_get_single_row(conn, sql)
        if (result == None):
            sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary))
            id = db_util.db_exec(conn, sql, o.to_tuple(no_id=cls._auto_primary))
            o.cols[cls._primary[0]] = id
            return o
        o = cls(row=result)
        return o

    @classmethod
    def select(cls, where = None, order_by = None, limit = None, offset = None, conn = None):
        sqlresult = db_util.db_get_all(conn or cls._dbfile, sql_command.select(cls._table_name, where=where, order_by=order_by, limit=limit, offset=offset))

        result = [cls(row=row) for row in sqlresult]

        return result

    @classmethod
    def select_one(cls, where = None, order_by = None, offset = None, conn = None):
        sqlresult = db_util.db_get_all(conn or cls._dbfile, sql_command.select(cls._table_name, where=where, order_by=order_by, limit=1, offset=offset))

        return None if len(sqlresult) == 0 else cls(row=sqlresult[0])

    @classmethod
    def get_count(cls, where = None, conn = None):
        count = db_util.db_get_single_cell(conn or cls._dbfile, sql_command.select(cls._table_name, ['count(*)'], where))
        return count

    @classmethod
    def get_page(cls, page_num:int, per_page:int, where = None, order_by = None, conn = None):
        """ Note: page_num starts at 1 or it will set to 1 if lower"""
        limit = per_page
        if (page_num < 1): page_num = 1
        offset = (page_num-1) * per_page
        
        batch = db_util.DBBatch(conn or cls._dbfile)

        if (per_page == 0):
            sql = sql_command.select(cls._table_name, where=where, order_by=order_by)
            batch.add_get_all(sql)
        else:
            sql = sql_command.select(cls._table_name, where=where, order_by=order_by, limit=limit, offset=offset)
            batch.add_get_all(sql)
        
        sql = sql_command.select(cls._table_name, ['count(*)'], where=where)
        batch.add_get_one_cell(sql)

        lsres = batch.run(close=conn == None)

        data = [cls(row=r) for r in lsres[0]]
        total_count = lsres[1]
        page_count = math.ceil(total_count / per_page) if per_page > 0 and math.ceil(total_count / per_page) > 0 else 1

        page = ResultPage(page_num, page_count, per_page, total_count, data)

        return page

    @classmethod
    def insert(cls, o, or_ignore = False, force_primary = False, update_conflict = False, set_col:list = None, where = None, conn = None):
        sql = ''
        if (isinstance(o, list)):
            if (len(o) == 0): return
            sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary and not force_primary), or_ignore=or_ignore)
            lsarg = []
            for k in o:
                arg = k.to_tuple(no_id=cls._auto_primary and not force_primary)
                if (update_conflict):
                    arg = k.to_tuple(no_id=cls._auto_primary and not force_primary)

                    if (set_col != None):
                        #lsset = list(set(cls.get_props_name()) & set(set_col))
                        arg += k.col_value_tuple(set_col)

                        if (where == None): arg += k.id_value_tuple()
                        sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary and not force_primary), or_ignore=or_ignore, update_conflict=update_conflict, set_value=set_col, where=where or cls._primary)
                    else:
                        arg += k.to_tuple(id_last=True)

                        sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary and not force_primary), or_ignore=or_ignore, update_conflict=update_conflict, set_value=cls.get_props_name(no_id=True), where=cls._primary)

                lsarg.append(arg)
            db_util.db_exec_multi(conn or cls._dbfile, sql, lsarg)
        else:
            if (update_conflict):
                lsarg = o.to_tuple(no_id=cls._auto_primary and not force_primary)

                if (set_col != None):
                    #lsset = list(set(cls.get_props_name()) & set(set_col))
                    lsarg += o.col_value_tuple(set_col)

                    if (where == None): lsarg += o.id_value_tuple()
                    sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary and not force_primary), or_ignore=or_ignore, update_conflict=update_conflict, set_value=set_col, where=where or cls._primary)
                else:
                    lsarg += o.to_tuple(id_last=True)

                    sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary and not force_primary), or_ignore=or_ignore, update_conflict=update_conflict, set_value=cls.get_props_name(no_id=True), where=cls._primary)

                return db_util.db_exec(cls._dbfile, sql, lsarg)
            sql = sql_command.insert(cls._table_name, cls.get_props_name(no_id=cls._auto_primary and not force_primary), or_ignore=or_ignore)
            #logging.debug(o)
            #logging.debug(o.cols)
            return db_util.db_exec(conn or cls._dbfile, sql, o.to_tuple(no_id=cls._auto_primary and not force_primary))

    @classmethod
    def update(cls, o, set_col:list = None, where = None, conn = None):
        if (isinstance(o, list)):
            lsarg = []
            if (set_col != None):
                #lsset = list(set(o.get_cols_name()) & set(set_col))
                for i in o:
                    lsval = i.col_value_tuple(set_col)
                    if (where == None): lsval += i.id_value_tuple()
                    lsarg.append(lsval)
                sql = sql_command.update(cls._table_name, set_col, where or cls._primary)
                db_util.db_exec_multi(conn or cls._dbfile, sql, lsarg)
            else:
                lsarg = [x.to_tuple(id_last=True) for x in o]
                sql = sql_command.update(cls._table_name, o.get_cols_name(no_id=True), cls._primary)
                db_util.db_exec_multi(conn or cls._dbfile, sql, lsarg)
        else:
            if (set_col != None):
                #lsset = list(set(o.get_cols_name()) & set(set_col))
                lsval = o.col_value_tuple(set_col)
                if (where == None): lsval += o.id_value_tuple()
                sql = sql_command.update(cls._table_name, set_col, where or cls._primary)
                db_util.db_exec(conn or cls._dbfile, sql, lsval)
            else:
                sql = sql_command.update(cls._table_name, o.get_cols_name(no_id=True), cls._primary)
                db_util.db_exec(conn or cls._dbfile, sql, o.to_tuple(id_last=True))

    @classmethod
    def delete(cls, o = None, where = None, constraint = True, conn = None):
        if (where != None):
            sql = sql_command.delete(cls._table_name, where)
            db_util.db_exec(conn or cls._dbfile, sql, constraint=constraint)
        else:
            sql = sql_command.delete(cls._table_name, cls._primary)
            db_util.db_exec(conn or cls._dbfile, sql, o.id_value_tuple(), constraint)

    def get_ref(self, ref_name:str, where = None, order_by = None, limit = None, offset = None, save_result = False, save_name = None, get_many = False, conn = None):
        if (not ref_name in self._reference):
            raise Exception(f'Reference {ref_name!r} not found')
        if (get_many):
            if (not isinstance(self._reference[ref_name], SQLRefPivot)):
                raise Exception(f'Reference {ref_name!r} is not a pivot reference but {type(self._reference[ref_name])}')
            result = self._reference[ref_name].get_many(self, where, order_by, limit, offset, conn)
        else:
            result = self._reference[ref_name].get(self, where, order_by, limit, offset, conn)
        if (save_result): self.cols[save_name or ref_name] = result
        return result

    def get_ref_page(self, ref_name:str, page_num:int, per_page:int, where = None, order_by = None, save_result = False, save_name = None, get_many = False, conn = None):
        if (not ref_name in self._reference):
            raise Exception(f'Reference {ref_name!r} not found')
        if (get_many):
            if (not isinstance(self._reference[ref_name], SQLRefPivot)):
                raise Exception(f'Reference {ref_name!r} is not a pivot reference but {type(self._reference[ref_name])}')
            result = self._reference[ref_name].get_many_page(self, page_num, per_page, where, order_by, conn)
        else:
            result = self._reference[ref_name].get_page(self, page_num, per_page, where, order_by, conn)
        
        if (save_result): self.cols[save_name or ref_name] = result
        return result

    def get_ref_one(self, ref_name:str, where = None, order_by = None, offset = None, save_result = False, save_name = None, conn = None):
        if (not ref_name in self._reference):
            raise Exception(f'Reference {ref_name!r} not found')

        result = self._reference[ref_name].get_one(self, where, order_by, offset, conn)

        if (save_result):
            if (save_name != None):
                self.cols[save_name] = result
            else:
                self.cols[ref_name] = result
        return result

    def __repr__(self):
        return f'{self._table_name}{self.cols}'

    def __eq__(self, other):
        if (type(other) != SQLTable):
            return False
        return (self.cols == other.cols)