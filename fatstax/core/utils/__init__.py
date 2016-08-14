from types import FunctionType
from string import ascii_lowercase, digits

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
