from ..objects import Row, Selection, cleanup_name
from ..parsing import parser, parser_addrow
from ..utils import multiple_index, _index_function_gen
from ..utils import generate_func
from ..exceptions.messages import ApiObjectMsg as msg
from types import FunctionType
import threading

# We have to manually lock threads for editing columns to prevent corruption
column_manipulation_lock = threading.RLock()

class MainSelection(Selection):
    """This extended selection allows the acceptance of the parsing data and the ability
    to delete/add rows in a supported way"""

    __slots__ = ["__canrefrencecolumn__",
                 "__columns__", "__columnsmap__",
                 "__rows__", "__rowcls__"]

    def __init__(self, csvdict=None, columns=None, 
                 cls=Row, parsing=parser,typetransfer=True, 
                 custom_columns=False, *args, **kwargs):

        # Local Flag to detirmine state of column mapping
        rebuild_column_map = False
        # This is used to be consistent with child selections 
        # and methods
        self.__columns__ = columns
        self.__columnsmap__ = {}
        try:
            # TypeError may be triggered by issubclass or
            # by else condition
            if cls is Row or issubclass(cls, Row):
                self.__rowcls__ = cls
            else:
                raise TypeError("cls argument was not supplied with a valid type")
        except TypeError:
            raise ValueError(
                msg.badcls.format(Row, cls if isinstance(cls, type) else type(cls)))

        if columns:
            self.__columnsmap__.update(
                column_crunch_repeat(self.__columns__))
        else:
            rebuild_column_map = True

        if csvdict is None:
            csvdict = {}
        if csvdict:
            if custom_columns:
                self.__rows__ = list(
                    parser(csvdict, cls, self.__columnsmap__, typetransfer, columns, *args, **kwargs))
            else:
                self.__rows__ = list(
                    parser(csvdict, cls, self.__columnsmap__, typetransfer, None, *args, **kwargs))
            if rebuild_column_map:
                # This catches mistakes if .load() is used instead of safe_load() / opencsv()
                try:
                    self.__columnsmap__.update(
                        column_crunch_repeat(self.__rows__[0].keys()))
                except AttributeError:
                    # Errornous Headers - Usually caused by single column
                    # Spreadsheets that don't have a header
                    raise ValueError("Bad CSV - File contains a single column with no header")
                except IndexError:
                    # Empty File, No Additional work needed.
                    pass

        else:
            self.__rows__ = list()
        if not self.__columns__:
            self.__columns__ = list()
        elif not isinstance(self.columns, list):
            self.__columns__ = list(self.__columns__) 

    @property
    def __apimother__(self):
        return self
    

    @property
    def rows(self):
        return self.__rows__

    @property
    def columns(self):
        return self.__columns__
        
    def addrow(self, cls=None, **kwargs):
        try:
            if cls is None:
                cls = self.__rowcls__
            r = parser_addrow(self.__columns__, cls, self.__columnsmap__)
            self.__rows__.append(r)
            if kwargs:
                for k, v in kwargs.items():
                    r.setcolumn(k, v)
            return r
        except TypeError as exc:
            from inspect import isclass
            # Generate Error Message
            if isinstance(cls, str):
                raise ValueError("'{}' is not a class and was not a subclass of {}. You may have meant to use {}.addcolumn()".format(
                    cls,
                    Row.__name__,
                    self.__class__.__name__))
            if isclass(cls):
                if not issubclass(cls, Row):
                    raise TypeError("{} was not a subclass of {}".format(cls.__name__, Row.__name__))
            raise exc

    def addcolumn(self, columnname, columndata="", clear=True):
        """Adds a column
        :param columnname: Name of the column to add.
        :param columndata: The default value of the new column.
        :param add_to_columns: Determines whether this column should
            be added to the internal tracker.
        :type columnname: :class:`str`
        :type add_to_columns: :class:`bool`
        Note: While Thread Safe, this method will have degraded performance if done within threads.
        """
        with column_manipulation_lock:

            if columnname in self.columns:
                raise ValueError(
                    "'{}' column already exists"
                    .format(columnname))
            if isinstance(columndata, FunctionType):
                for row in self.rows:
                    row._addcolumns_func(columnname, columndata)
            else:
                for row in self.rows:
                    row._addcolumns(columnname, columndata)
            self.__columns__ += (columnname,)
            self.__columnsmap__.clear()
            self.__columnsmap__.update(column_crunch_repeat(self.__columns__))
        return self

    def delcolumn(self, columnname):
        with column_manipulation_lock:

            if not (columnname in self.columns):
                raise ValueError(
                    "'{}' column doesn't exist"
                    .format(columnname))

            for row in self.rows:
                row._delcolumns(columnname)

            self.__columns__ = tuple(
                column  for column in self.columns if column != columnname)
            self.__columnsmap__.clear()
            self.__columnsmap__.update(column_crunch_repeat(self.__columns__))

    def rename_column(self, old_column, new_column):
        with column_manipulation_lock:
            if old_column == new_column:
                raise ValueError("Rename is identical to original")
            if not (old_column in self.columns):
                raise ValueError(
                    "'{}' column doesn't exist"
                    .format(old_column))
            if new_column in self.columns:
                raise ValueError(
                    "'{}' already exists, name will cause collision"
                    .format(new_column))


            for row in self.rows:
                row._rename_columns(old_column, new_column)
            _transfer_ = {c: new_column if c == old_column else c for c in self.__columns__}
            self.__columns__ = tuple(
                _transfer_.get(column) for column in self.columns)
            self.__columnsmap__.clear()
            self.__columnsmap__.update(column_crunch_repeat(self.__columns__))

    def __delitem__(self, v):
        del self.__rows__[v]

    def remove_duplicates(self, soft=True):
        """Removes duplicates.
           if soft is true, return a selection
           else: edit this object
        """
        if soft:
            return self.merge(self)
        else:
            self.__rows__ = list(self.merge(self).rows)

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
    """Takes a order list of columns.
       Returns a dictionary of any corrections needed
       Ment for internal use by the library
       """

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