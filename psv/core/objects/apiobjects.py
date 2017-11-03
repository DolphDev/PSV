from ..objects import BaseRow, Selection, cleanup_name
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

    def __init__(self, csvdict=None, columns=None, 
                 cls=BaseRow, parsing=parser, outputfile=None,
                 typetranfer=True, *args, **kwargs):
        # Since I close the file after this, the row must be placed into memory
        rebuild_column_map = False
        self.__apimother__ = self
        self.__outputname__ = outputfile
        self.__columns__ = columns
        self.__columnsmap__ = {}
        
        if columns:
            self.__columnsmap__.update(
                column_crunch_repeat(self.__columns__))
        else:
            rebuild_column_map = True

        if csvdict is None:
            csvdict = {}
        if csvdict:
            self.__rows__ = list(
                parser(csvdict, cls, self.__columnsmap__, typetranfer, *args, **kwargs))
            if rebuild_column_map:
                self.__columnsmap__.update(
                    column_crunch_repeat(self.__rows__[0].keys()))
        else:
            self.__rows__ = list()
        if not self.__columns__:
            self.__columns__ = tuple()

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


    def addcolumn(self, columnname, columndata="",
                  add_to_columns=True, clear=True):
        """Adds a column
        :param columnname: Name of the column to add.
        :param columndata: The default value of the new column.
        :param add_to_columns: Determines whether this column should
            be added to the internal tracker.
        :type columnname: :class:`str`
        :type add_to_columns: :class:`bool`
        Note: Rows that are being accessed by another thread will error out if clear is True
        Note:
        """
        if columnname in self.columns:
            raise ValueError(
                "'{}' column already exists"
                .format(columnname))
        for row in self.rows:
            row.addcolumn(columnname, columndata)
        if add_to_columns:
            self.columns += (columnname,)
            self.__columnsmap__.clear()
            self.__columnsmap__.update(column_crunch_repeat(self.__columns__))
        return self

    def __delitem__(self, v):
        del self.__rows__[v]

def _column_repeat_dict(columns, clean_ups):
    master = {}
    for x in clean_ups:
        master[x] = None
    for x in columns:
        cl_name = cleanup_name(x)
        if master[cl_name] is None:
            master[cl_name] = (x,)
        else:
            master[cl_name] = master[cl_name] + (x,)
    return master

def column_crunch_repeat(columns):
    rv = {}
    clean_ups = set(cleanup_name(x) for x in columns)
    ref = _column_repeat_dict(columns, clean_ups)
    if len(clean_ups) == len(columns):
        for x in clean_ups:
            for column in ref[x]:
                rv.update({x:column})
    for x in clean_ups:
        if len(ref[x]) > 1:
            counter = 0
            for column in ref[x]:
                cln = x+"_"+str(counter)
                while cln in clean_ups:
                    counter += 1
                    cln = x+"_"+str(counter)
                rv.update({cln:column})
                counter += 1
        else:
            for column in ref[x]:
                rv.update({x:column})
      
    return rv