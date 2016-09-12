"""This file contains all csv/excel parsing code"""

from ..utils import cleanup_name, translate_type

def parser(csvfile, cls, typetranfer=True, *args, **kwargs):
    """This generates row objects for csv, and sets them up 
    for dynamic access"""
    for row in csvfile:
        yield cls({cleanup_name(x): {"org_name": x, "value": translate_type(row[x]) if typetranfer else row[x]}
        for x in row.keys()}, *args, **kwargs)

def parser_addrow(columns, cls, typetranfer=True, *args, **kwargs):
    r = cls({}, *args, **kwargs)
    r.update(({cleanup_name(x): {"org_name": x, "value": ""} for x in columns}))
    return r


