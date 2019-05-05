from types import FunctionType
from string import printable
from .objects import ROW_OBJ


def multiple_index(row, v):
    tracker = []
    for x in v:
        if x is ROW_OBJ:
            tracker.append(row)
            continue
        if not isinstance(x, str):
            raise TypeError("Multi-Index does not support type {}".format(type(x)))
        tracker.append(row.getcolumn(x))
    return tuple(tracker)

def _index_function_gen(api, func):
    for x in api.rows:
        if func(x):
            yield x

def translate_type(string):
    """Depreciated, Now must be enabled in functions that use it
       Too slow to be default, and conversions can lose information

       Takes a string and converts it float or a int if possible
    """
    # This is way too greedy
    try:
        if string.isdigit():
            return int(string)
        return float(string)
    except ValueError:
        return string
    except AttributeError:
        return string

def generate_func(arg, kwargs):
    """Generates a function based on the arguments given"""
    if isinstance(arg, FunctionType) and not kwargs:
        return arg
    elif isinstance(arg, str) or kwargs or arg is None:
        def select_func(row, arg=arg, kwargs=kwargs):
            if kwargs:
                for k,v in kwargs.items():
                    if isinstance(v, FunctionType):
                        if not v(row.getcolumn(k)):
                            return False
                    elif isinstance(v, bool):
                        if not bool(row.getcolumn(k)) is v:
                            return False
                    else:
                        if not row.getcolumn(k) == v:
                            return False
            if arg:
                if isinstance(arg, FunctionType):
                    if not arg(row):
                        return False
                else:
                    if not bool(row.getcolumn(arg)):
                        return False

            return True
        return select_func
    else:
        raise TypeError(
            "'f' cannot not be {}, must be str, function, or NoneType".format(
                type(arg)))  

def generate_func_any(arg, kwargs):
    """

    """
    if isinstance(arg, FunctionType) and not kwargs:
        return arg
    elif isinstance(arg, str) or kwargs or arg is None:
        def select_func(row, arg=arg, kwargs=kwargs):
            if kwargs:
                for k,v in kwargs.items():
                    if isinstance(v, FunctionType):
                        if v(row.getcolumn(k)):
                            return True
                    elif isinstance(v, bool):
                        if bool(row.getcolumn(k)) is v:
                            return True
                    else:
                        if row.getcolumn(k) == v:
                            return True
            if arg:
                if isinstance(arg, FunctionType):
                    if arg(row):
                        return True
                else:
                    if bool(row.getcolumn(arg)):
                        return True
            return False
        return select_func
    else:
        raise TypeError(
            "'f' cannot not be {}, must be str, function, or NoneType".format(
                type(arg)))  

def asciireplace(string, rw='?'):
    def _gen(string):
        for x in string:
            if x in printable:
                yield x
    return "".join(_gen(string))

def limit_text(string, limit):

    if limit and isinstance(string, str):
        return string[:limit]
    else:
        return string
