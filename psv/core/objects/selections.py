from ..output import outputfile, outputstr
from ..utils import multiple_index, limit_text
from ..utils import _index_function_gen, asciireplace, generate_func, generate_func_any, ROW_OBJ
from ..exceptions.messages import ApiObjectMsg as msg

from types import FunctionType
from tabulate import tabulate

from threading import RLock

SelectionLock = RLock()
NonHashMergeLock = RLock()

class Selection(object):

    __slots__ = ["__rows__", "__apimother__"]

    def __init__(self, selection, api_mother):
        self.__rows__ = (selection)
        self.__apimother__ = api_mother

    def __add__(self, sel):
        return Selection((
            tuple(self.rows) + tuple(sel.rows)), self.__apimother__)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, v):
        if isinstance(v, slice):
            return Selection(self.rows[v], self.__apimother__)
        if isinstance(v, int):
            return (self.rows[v])
        elif isinstance(v, str):
            return (x.getcolumn(v) for x in self.rows)
        elif isinstance(v, tuple):
            return (multiple_index(x, v) for x in self.rows)
        elif isinstance(v, FunctionType):
            return Selection(_index_function_gen(self, v), self.__apimother__)
        else:
            raise TypeError(msg.getitemmsg.format(type(v)))

    @property
    def rows(self):
        if not isinstance(self.__rows__, tuple):
            self.process()
            return self.__rows__
        else:
            return self.__rows__

    def process(self):
        """Processes the Selection, then returns it

           Use this if chaining selections but you still need the parent
            for later usage. Or if their are mulitple chains from the 
            same parent selection

        """
        if not isinstance(self.__rows__, tuple):
            with SelectionLock:
                self.__rows__ = tuple(self.__rows__)
        return self

    @property
    def columns(self):
        return self.__apimother__.columns

    @property
    def __columnsmap__(self):
        return self.__apimother__.__columnsmap__

    @property
    def columns_mapping(self):
        return {v:k for k,v in self.__columnsmap__.items()}

    @property
    def columns_attributes(self):
        return list(self.__columnsmap__.keys())

    @property
    def addcolumn(self):
        """Adds a column
        :param columnname: Name of the column to add.
        :param columndata: The default value of the new column.
        :param add_to_columns: Determines whether this column should
            be added to the internal tracker.
        :type columnname: :class:`str`
        :type add_to_columns: :class:`bool`
        Note: Rows that are being accessed by another thread will error out
            if accessed during the brief time addcolumn is updating.

        Note: This will affect the entire MainSelection, not just this
         selection

        """    
        return self.__apimother__.addcolumn

    @property
    def delcolumn(self):
        return self.__apimother__.delcolumn

    @property
    def rename_column(self):
        return self.__apimother__.rename_column
    

    def transform(self, column, func):
        for row in self.rows:
            row.setcolumn(column, func(row.getcolumn(column)))
        return self

    def _merge(self, args):
        maps = []
        for con in (self,) + args:
            maps.append({(x.__hashvalue__()):x for x in con.rows})
        master = {}
        for d in maps:
            master.update(d)
        keys = set(master.keys())
        for key in keys:
            yield master[key]

    def merge(self, *args, force_safety=True):
        """Merges selections
           
           Note: This merge's algorithm relies on the uniqueness of the rows.
            duplicate rows will be only represented by 1 row. 

           Note: This Merge relies on all data in a row being hashable, use non_hash_merge if you
           can't guarantee this.
           
        """
        try:
            if force_safety:
                if (not all(self.__apimother__ is x.__apimother__ for x in args)):
                    raise ValueError("Merge by default only accepts rows from same origin")
            return Selection(tuple(self._merge(args)), self.__apimother__)
        except TypeError as exc:
            raise TypeError(
                "{} - Use the non_hash_merge to merge rows with non-hashable datatypes.".format(exc))

    def safe_merge(self, *args):
        """This is much slower but is hashes rows as processed instead of preprocessing them"""
        out = self
        for x in args:
            out = out + x
        return out

    def non_hash_merge(self, *args):
        """This merge uses the exploits the __output__ flag of a row instead of it's hashed contents
           This allows merging of of rows that contain unhashable mutable data such as sets or dict.
           This doesn't remove duplicate rows but is slightly faster and can handle all datatyps.

           Note: This merge is effectively single-threaded and editing the outputflag during
            running will effect results of the merge and may have unattended conquences on the
            state of this selection.
        """
        with NonHashMergeLock:
            if not all(self.__apimother__ is x.__apimother__ for x in args):
                raise ValueError("non_hash_merge only accepts rows from same origin")
            outputstore = tuple(x.__output__ for x in self.__apimother__)
            self.__apimother__.no_output() 
            for x in ((self,) + args):
                for row in x:
                    +row
            result = self.__apimother__.outputtedrows

            for x, row in zip(outputstore, self.__apimother__.rows):
                if x:
                    +row
                else:
                    -row
        return result

    def _find_all(self, func):
        for x in self.rows:
            if func(x):
                yield x

    def single_find(self, selectionfirstarg_data=None, **kwargs):
        """Find a single row based off search criteria given.
            will raise error if returns more than one result'"""
        try:
            result = None
            func = generate_func(selectionfirstarg_data, kwargs)
            g = self._find_all(func)
            result = next(g)
            next(g)
            raise ValueError(msg.singlefindmsg)
        except StopIteration:
            return result
    
    def single_find_any(self, selectionfirstarg_data=None, **kwargs):
        """Find a single row based off search criteria given.
            Only one condition needs to be Trues.
            will raise error if returns more than one result"""
        try:
            result = None
            func = generate_func_any(selectionfirstarg_data, kwargs)
            g = self._find_all(func)
            result = next(g)
            next(g)
            raise ValueError(msg.singlefindmsg)
        except StopIteration:
            return result
    
    def find(self, selectionfirstarg_data=None, **kwargs):
        try:
            func = generate_func(selectionfirstarg_data, kwargs)
            g = self._find_all(func)
            return next(g)
        except StopIteration:
            return None

    def find_any(self, selectionfirstarg_data=None, **kwargs):
        try:
            func = generate_func_any(selectionfirstarg_data, kwargs)
            g = self._find_all(func)
            return next(g)
        except StopIteration:
            return None

    def fast_find(self, **kwargs):
        """Much faster find. Returns the last row the fulfilled any kwargs. Only accept one kwargs.
            Note: All keynames must be unique to be used effectively, else latest row will be returned"""
        if len(kwargs) != 1:
            raise ValueError(msg.badfastfind)
        k, v = tuple(kwargs.items())[0]
        index_value = self.index(k)
        return index_value.get(v)

    def find_all(self, selectionfirstarg_data=None, **kwargs):
        func = generate_func(selectionfirstarg_data, kwargs)
        return tuple(self._find_all(func))

    def find_all_any(self, selectionfirstarg_data=None, **kwargs):
        func = generate_func_any(selectionfirstarg_data, kwargs)
        return tuple(self._find_all(func))

    def flip_output(self):
        """flips all output boolean for all rows in this selection"""
        for x in self.rows:
            ~x
        return self

    def no_output(self):
        """Sets all rows to not output"""
        for x in self.rows:
            -x
        return self

    def all_output(self):
        """Sets all rows to output"""
        for x in self.rows:
            +x
        return self

    def lenoutput(self):
        return len(tuple(filter(lambda x: x.outputrow, self.rows)))

    def len_no_output(self):
        return len(tuple(filter(lambda x: not x.outputrow, self.rows)))

    def enable(self, selectionfirstarg_data=None, **kwargs):
        v = generate_func(selectionfirstarg_data, kwargs)
        for x in self.rows:
            if bool(v(x)):
                +x
        return self

    def disable(self, selectionfirstarg_data=None, **kwargs):
        v = generate_func(selectionfirstarg_data, kwargs)
        for x in self.rows:
            if bool(v(x)):
                -x
        return self

    def flip(self, selectionfirstarg_data=None, **kwargs):
        v = generate_func(selectionfirstarg_data, kwargs)
        for x in self.rows:
            if bool(v(x)):
                ~x
        return self

    def select(self, selectionfirstarg_data=None, **kwargs):
        """Method for selecting part of the csv document.
            generates a function based of the parameters given.
            All conditions must be true for a row to be selected
            Uses Lazy Loading, doesn't process till needed.

        """
        if not selectionfirstarg_data and not kwargs:
            return Selection(self.__rows__, self.__apimother__)
        func = generate_func(selectionfirstarg_data, kwargs)
        return self[func]

    def any(self, selectionfirstarg_data=None, **kwargs):
        """Method for selecting part of the csv document.
            generates a function based of the parameters given.
            only one condition must be True for the row to be
             selected.


            Uses Lazy Loading, doesn't process till needed.
        """
        if not selectionfirstarg_data and not kwargs:
            return Selection(self.__rows__, self.__apimother__)
        func = generate_func_any(selectionfirstarg_data, kwargs)
        return self[func]

    def safe_select(self, selectionfirstarg_data=None, **kwargs):
        """Method for selecting part of the csv document.
            generates a function based off the parameters given.

            This instantly processes the select instead of 
                lazily loading it at a later time.
                Preventing race conditions under most uses cases.
                if the same select is being worked on in multiple 
                threads or other cases such as rows being edited
                before the selected is processed.

        """
        if not selectionfirstarg_data and not kwargs:
            return Selection(self.__rows__, self.__apimother__)
        func = generate_func(selectionfirstarg_data, kwargs)
        return self._safe_select(func)

    def safe_any(self, selectionfirstarg_data=None, **kwargs):
        """Method for selecting part of the csv document.
            generates a function based off the parameters given.
            only one condition must be True for the row to be selected.

            This instantly processes the select instead of 
                lazily loading it at a later time.
                Preventing race conditions under most uses cases.
                if the same select is being worked on in multiple 
                threads or other cases such as rows being edited
                before the selected is processed.
        """
        if not selectionfirstarg_data and not kwargs:
            return Selection(self.__rows__, self.__apimother__)
        func = generate_func_any(selectionfirstarg_data, kwargs)
        return self._safe_select(func)

    def grab(self, *args):
        """Grabs specified columns from every row

        :returns: :class:`tuple` of the result.

        """
        arg = tuple(args)
        if len(arg) > 1:
            return tuple(self[arg])
        elif len(arg) == 1:
            return tuple(self[arg[0]])
        else:
            raise ValueError(msg.badgrab)

    def remove_duplicates(self, soft=True):
        """Removes duplicates rows
           if soft is true, return a selection
           else: edit this object

           Note: All rows must contain hashable data
        """
        if soft:
            return self.merge(self)
        else:
            self.__rows__ = self.merge(self).rows
        

    def unique(self, *args):
        """Grabs specified columns from every row

        :returns: :class:`set` of the result.

        """
        arg = tuple(args)
        if len(arg) > 1:
            return set(self[arg])
        elif len(arg) == 1:
            return set(self[arg[0]])
        else:
            raise ValueError(msg.badgrab)


    def _safe_select(self, func):
        return Selection(tuple(_index_function_gen(self, func)), self.__apimother__)

    def index(self, keyname, keyvalue=None):
        """ Indexs a Column to a dict """
        if keyvalue is None:
            return dict(self[keyname, ROW_OBJ])
        else:
            return dict(self[keyname, keyvalue])

    @property
    def outputtedrows(self):
        return self.safe_select(lambda x: x.outputrow)


    @property
    def nonoutputtedrows(self):
        return self.safe_select(lambda x: not x.outputrow)


    def tabulate(self, limit=100, format="grid", only_ascii=True,
                 columns=None, text_limit=None, remove_newline=True):

        data = [x.longcolumn() for x in self.rows[:limit]]
        sortedcolumns = self.columns if not columns else columns
        if remove_newline:
            for i, longcolumn in enumerate(data):
                for key in longcolumn:
                    if isinstance(longcolumn[key], str):
                        longcolumn[key] = longcolumn[key].replace("\n", "")
        result = tabulate(
            [sortedcolumns] + [[limit_text(x[c], text_limit)
                                for c in sortedcolumns] for x in data],
            headers="firstrow",
            tablefmt=format)
        if only_ascii:
            return asciireplace(result)
        return result

    def output(self, f=None, columns=None, quote_all=None, encoding="utf-8"):
        if not columns:
            columns = self.columns
        outputfile(f, self.rows, columns,
                   quote_all=quote_all, encoding=encoding)

    def outputs(self, columns=None, quote_all=None, encoding="utf-8"):
        """Outputs to str"""
        if not columns:
            columns = self.columns
        return outputstr(self.rows, columns, quote_all=quote_all, encoding=encoding)
