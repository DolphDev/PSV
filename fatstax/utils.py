def argstotuple(*args):
    return args

def multiple_index(row, v):
    
    tracker = []
    for x in v:
        tracker.append(row.getcolumn(x))
    return tuple(tracker)