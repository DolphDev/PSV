"""This file contains all csv/excel parsing code"""

from ..utils import translate_type
from ..objects import cleanup_name


def parser(csvfile, cls, columns_map, typetranfer=True, *args, **kwargs):
    """This generates row objects for csv, and sets them up 
    for dynamic access"""
    for row in csvfile:
        if typetranfer:
            yield cls({(x): translate_type(row[x])
                       for x in row.keys()}, columns_map, *args, **kwargs)
        else:
            yield cls(row, columns_map, *args, **kwargs) 


def parser_addrow(columns, cls, columns_map, typetranfer=True, *args, **kwargs):
    r = cls({}, columns_map, *args, **kwargs)
    r.update(({(x): "" for x in columns}))
    return r
