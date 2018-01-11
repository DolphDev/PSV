from types import FunctionType
from string import printable

def multiple_index(row, v):
    
    tracker = []
    for x in v:
        if not isinstance(x, str):
            raise TypeError("Multi-Index does not support type {}".format(type(x)))
        if x == "ROW_OBJ":
            tracker.append(row)
            continue
        if x == "|ROW_OBJ|":
            tracker.append(row.getcolumn("ROW_OBJ"))
            continue
        tracker.append(row.getcolumn(x))
    return tuple(tracker)

def _index_function_gen(api, func):
    for x in api.rows:
        if func(x):
            yield x

def translate_type(string):
    try:
        if string.isdigit():
            return int(string)
        return float(string)
    except ValueError:
        return string
    except AttributeError:
        return string


def generate_func(name, kwargs):
    if isinstance(name, FunctionType) and not kwargs:
        return name
    elif isinstance(name, str) or kwargs or name is None:
        def select_func(row):
            if kwargs:
                for k,v in kwargs.items():
                    if isinstance(v, FunctionType):
                        if not v(row.getcolumn(k)):
                            return False
                    else:
                        if not row.getcolumn(k) == v:
                            return False
            if name:
                if isinstance(name, FunctionType):
                    if not name(row):
                        return False
                else:
                    if not bool(row.getcolumn(name)):
                        return False
            return True
        return select_func
    else:
        raise TypeError(
            "'f' cannot not be {}, must be str, function, or NoneType".format(
                type(name)))  

def generate_func_any(name, kwargs):
    "Note: Currently a Hack based off generate_func, rewrite necessary"
    if isinstance(name, FunctionType) and not kwargs:
        return name
    elif isinstance(name, str) or kwargs or name is None:
        def select_func(row):
            if kwargs:
                for k,v in kwargs.items():
                    if isinstance(v, FunctionType):
                        if v(row.getcolumn(k)):
                            return True
                    else:
                        if row.getcolumn(k) == v:
                            return True
            if name:
                if isinstance(name, FunctionType):
                    if name(row):
                        return True
                else:
                    if bool(row.getcolumn(name)):
                        return True
            return False
        return select_func
    else:
        raise TypeError(
            "'f' cannot not be {}, must be str, function, or NoneType".format(
                type(name)))  



def asciireplace(string, rw='?'):
    def _gen(string):
        for x in string:
            if x not in printable:
                yield rw
            else:
                yield x
    return "".join(_gen(string))

def limit_text(string, limit):

    if limit and isinstance(string, str):
        return string[:limit]
    else:
        return string
