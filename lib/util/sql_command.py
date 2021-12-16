

def _parse_expr_list(arg:list) -> str:
    if (type(arg) == list):
        ls_expr = []
        index = 0
        last_type = 'none'
        for expr in arg:
            if (type(expr) == str):
                if (expr.lower() in ['and', 'or', 'not']):
                    if (index > 0):
                        ls_expr.append(expr.lower())
                    else:
                        raise Exception('where argument expect a column name or expression in first list index')
                    last_type = 'keyword'
                else:
                    if (last_type != 'keyword' and last_type != 'none'):
                        ls_expr.append('and')
                    if (expr.find('(') != -1):
                        ls_expr.append(expr)
                    else:
                        ls_expr.append(f'{expr} = ?')
                    last_type = 'str'
            if (type(expr) == list):
                if (last_type != 'keyword' and last_type != 'none'):
                    ls_expr.append('and')
                if (len(expr) ==  1):
                    ls_expr.append(f'{expr[0]} = ?')
                elif (len(expr) == 2):
                    if (expr[1] in ['=', '<>', '>', '<', 'in', 'like']):
                        ls_expr.append(f'{expr[0]} {expr[1]} ?')
                    else:
                        if (type(expr[1]) in [int, float]):
                            ls_expr.append(f'{expr[0]} = {expr[1]}')
                        elif (type(expr[1]) == str):
                            ls_expr.append(f'{expr[0]} = \'{expr[1]}\'')
                        elif (type(expr[1]) == list):
                            ls_expr.append(f'{expr[0]} = {expr[1][0]}')
                elif (len(expr) == 3):
                    value = expr[2]
                    if (type(expr[2]) in [int, float]):
                        expr[2] = f'{expr[2]}'
                    elif (type(expr[2]) == str):
                        expr[2] = f'\'{expr[2]}\''
                    elif (type(expr[2]) == list):
                        ls_expr.append(f'{expr[0]} = {expr[2][0]}')
                    ls_expr.append(' '.join(expr))
                last_type = 'list'
            index += 1

        return ' '.join(ls_expr)
    else:
        return f'{arg} = ?'

def select(table:list, columns:list = None, where:list = None, group_by:list = None, having:list = None, order_by:list = None, limit:int = None, offset:int = None, line_break = False) -> str:
    result = ''

    if (columns == None):
        result += 'select *'
    else:
        result += 'select ' + ', '.join(columns)

    result += ('\n' if line_break else ' ') + 'from ' + (','.join(table) if (type(table) == list) else table)

    if (where != None):
        result += ('\n' if line_break else ' ') + 'where '
        result += _parse_expr_list(where)

    if (group_by != None):
        result += ('\n' if line_break else ' ') + 'group by '
        result += ', '.join(group_by)

    if (having != None):
        result += ('\n' if line_break else ' ') + 'having '
        result += _parse_expr_list(having)

    if (order_by != None):
        result += ('\n' if line_break else ' ') + 'order by '
        if (type(order_by) == list):
            result += ' '.join(order_by)
        else:
            result += order_by

    if (limit != None):
        result += ('\n' if line_break else ' ') + f'limit {limit}'

    if (offset != None):
        result += ('\n' if line_break else ' ') + f'offset {offset}'

    return result

def select_join(table:list, join_on:str, columns:list = None, where:list = None, group_by:list = None, having:list = None, order_by:list = None, limit:int = None, offset:int = None, line_break = False) -> str:
    result = ''

    if (columns == None):
        result += 'select *'
    else:
        result += 'select ' + ', '.join(columns)

    if (len(table) == 2):
        result += ('\n' if line_break else ' ') + f'from {table[0]} join {table[1]} on '
        result += join_on
    else:
        raise Exception('The number of join table in list must be 2, otherwise better use select()')

    if (where != None):
        result += ('\n' if line_break else ' ') + 'where '
        result += _parse_expr_list(where)

    if (group_by != None):
        result += ('\n' if line_break else ' ') + 'group by '
        result += ', '.join(group_by)

    if (having != None):
        result += ('\n' if line_break else ' ') + 'having '
        result += _parse_expr_list(having)

    if (order_by != None):
        result += ('\n' if line_break else ' ') + 'order by '
        if (type(order_by) == list):
            result += ' '.join(order_by)
        else:
            result += order_by

    if (limit != None):
        result += ('\n' if line_break else ' ') + f'limit {limit}'

    if (offset != None):
        result += ('\n' if line_break else ' ') + f'offset {offset}'

    return result

def insert(table:str, columns:list = None, values:list = None, or_ignore = False, update_conflict = False, set_value:dict = None, where:list = None) -> str:
    result = 'insert' + (' or ignore ' if or_ignore else ' ') + f'into {table} '

    if (columns != None):
        result += '(' + ', '.join(columns) + ') '

    result += 'values '

    if (values == None):
        result += '(' + ', '.join(['?'] * len(columns)) + ')'
    else:
        for i in range(len(values)):
            if (type(values[i]) == str):
                values[i] = f'\'{values[i]}\''
            else:
                values[i] = f'{values[i]}'
        result += '(' + ', '.join(values) + ')'

    if (update_conflict):
        result += ' on conflict do update set '
        if (type(set_value) == list):
            result += ', '.join([f'{x} = ?' for x in set_value])
        elif (type(set_value) == dict):
            result += ', '.join([f'{k} = {set_value[k]!r}' for k in set_value])
        if (where != None):
            result += ' where ' + _parse_expr_list(where)

    return result

def update(table:str, set_value:dict, where:list = None):
    result = f'update {table} set '

    if (type(set_value) == dict):
        result += ', '.join([f'{k} = {set_value[k]!r}' for k in set_value])
    elif (type(set_value) == list):
        result += ', '.join([f'{x} = ?' for x in set_value])

    if (where != None):
        result += ' where ' + _parse_expr_list(where)

    return result

def delete(table:str, where:list = None):
    result = f'delete from {table}'

    if (where != None):
        result += ' where ' + _parse_expr_list(where)

    return result
