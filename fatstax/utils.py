from types import FunctionType

def multiple_index(row, v):
    
    tracker = []
    for x in v:
        tracker.append(row.getcolumn(x))
    return tuple(tracker)

def multiisinstance(*args, types=None):
    if types is None:
        raise Exception()
    try:
        for x in args:
            for typ in types:
                assert(type(x) in types)
        return True
    except AssertionError:
        return False

