"""This file contains all csv parsing code"""

from ..utils import translate_type
from ..objects import cleanup_name

def parser(csvfile, cls, columns_map, typetransfer=True, custom_columns=False ,*args, **kwargs):
    """This generates row objects for csv, and sets them up 
    for dynamic access"""
    # To prevent reduntant and wasteful checks, we check for each condition only once
    if custom_columns:
        if typetransfer:
            for row in csvfile:
                yield cls({(x): translate_type(row[x])
                       for x in custom_columns}, columns_map, *args, **kwargs)
        else:
            for row in csvfile:
                yield cls({(x): (row[x])
                           for x in custom_columns}, columns_map, *args, **kwargs)       
    else:
        if typetransfer:
            for row in csvfile:
                yield cls({(x): translate_type(row[x])
                           for x in row.keys()}, columns_map, *args, **kwargs)
        else:
            for row in csvfile:
                yield cls(row, columns_map, *args, **kwargs) 


def parser_addrow(columns, cls, columns_map, typetransfer=True, *args, **kwargs):
    r = cls({}, columns_map, *args, **kwargs)
    r.update(({(x): "" for x in columns}))
    return r
