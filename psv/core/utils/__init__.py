from types import FunctionType
from string import ascii_lowercase, digits, ascii_uppercase
from string import printable
ascii_lowercase = (ascii_lowercase+"_"+digits)


def cleanup_name(s):
    return "".join(filter(lambda x: x in ascii_lowercase, s.lower()))

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

def column_string(n):
    div=n
    string=""
    temp=0
    while div>0:
        module=(div-1)%26
        string=chr(65+module)+string
        div=int((div-module)/26)
    return string

def generate_func(name, kwargs):
    if isinstance(name, FunctionType) and not kwargs:
        return name
    elif isinstance(name, str) or kwargs or name is None:
        def select_func(row):
            try:
                if kwargs:
                    for k,v in kwargs.items():
                        if isinstance(v, FunctionType):
                            assert v(row.getcolumn(k))
                        else:
                            assert row.getcolumn(k) == v
                if name:
                    if isinstance(name, FunctionType):
                        assert name(row)
                    else:
                        assert bool(row.getcolumn(name))
            except AssertionError:
                return False
            return True
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
