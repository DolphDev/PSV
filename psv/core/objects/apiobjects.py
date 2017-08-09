from ..objects import BaseRow, Selection
from ..parsing import parser, parser_addrow
from ..utils import multiple_index, _index_function_gen
from ..utils import generate_func
from ..exceptions.messages import ApiObjectMsg as msg
from types import FunctionType


class MainSelection(Selection):
    """This extended selection allows the acceptance of the parsing data and the ability
    to delete/add rows in a supported way"""

    __slots__ = ["__outputname__", "__canrefrencecolumn__",
                 "__columns__", "__columnsmap__",
                 "__rows__", "__apimother__"]

    def __init__(self, csvdict=None, columns=None, columnsmap=None, 
                 cls=BaseRow, parsing=parser, outputfile=None,
                 typetranfer=True, *args, **kwargs):
        # Since I close the file after this, the row must be placed into memory
        self.__apimother__ = self
        self.__outputname__ = outputfile
        self.__columns__ = columns
        self.__columnsmap__ = {"hello":"Hello!"}

        if csvdict is None:
            csvdict = {}
        if csvdict:
            self.__rows__ = list(
                parser(csvdict, cls, self.__columnsmap__, typetranfer, *args, **kwargs))
        else:
            self.__rows__ = list()

    @property
    def rows(self):
        return self.__rows__

    @rows.deleter
    def rows(self, v):
        del self.__rows__[v]

    @property
    def columns(self):
        return self.__columns__

    @columns.setter
    def columns(self, v):
        self.__columns__ = v


    def addrow(self, columns=None, cls=BaseRow, **kwargs):
        r = parser_addrow(columns if columns else self.__columns__, cls, self.__columnsmap__)
        self.__rows__.append(r)
        if kwargs:
            for k, v in kwargs.items():
                r.setcolumn(k, v)
        return r

    def __delitem__(self, v):
        del self.__rows__[v]

def _column_repeat_dict(columns, clean_ups):
    master = {}
    for x in clean_ups:
        master[x] = None
    for x in columns:
        cl_name = cleanup_name(x, {})
        if master[cl_name] is None:
            master[cl_name] = (x,)
        else:
            master[cl_name] = master[cl_name] + (x,)
    return master

def column_crunch_repeat(columns):
    rv = {}
    clean_ups = set(cleanup_name(x, {}) for x in columns)
    if len(clean_ups) == len(columns):
        return {}
    ref = _column_repeat_dict(columns, clean_ups)
    for x in clean_ups:
        if len(ref[x]) > 1:
            counter = 0
            for column in ref[x]:
                rv.update({column:x+"_"+str(counter)})
                counter += 1