from types import FunctionType
from string import ascii_lowercase, digits, ascii_uppercase

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
        tracker.append(row.getcolumn(x))
    return tuple(tracker)

def _index_function_gen(api, func):
    for x in filter(lambda x:not x.is_deleted, api.rows):
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
    def select_func(row):
        try:
            if kwargs:
                for k,v in kwargs.items():
                    assert row.getcolumn(k) == v
                return True
            elif name:
                return bool(row.getcolumn(name))
            else: 
                return True
        except AssertionError:
            return False
    return select_func