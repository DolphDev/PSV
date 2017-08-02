from ..output import outputfile, outputstr
from ..utils import multiple_index, limit_text
from ..utils import _index_function_gen, generate_func, asciireplace
from ..exceptions import SelectionError
from ..exceptions.messages import ApiObjectMsg as msg

from types import FunctionType
from tabulate import tabulate


class Selection(object):

    __slots__ = ["__rows__", "__apimother__"]

    def __init__(self, selection, api_mother):
        self.__rows__ = (selection)
        self.__apimother__ = api_mother

        if not self.rows:
            Exception("Selection Error")

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

    def merge(self, *args, safe_merge=False, quick_merge=True, force_saftey=True):
        """Merges selctions


           Note: This Merge relies on all data in a row being hashable, use non_hash_merge if you
           can't guarantee this

           Saftey Note: You will lose saftey on some of Selection's functionality 
           (such as creating selections) or finding a row if all rows don't have the same exact columns)
           
        """
        try:
            if (not all(self.__apimother__ is x.__apimother__ for x in args)) and force_saftey:
                raise TypeError("Merge by default only accepts rows from same origin")

            if safe_merge:
                out = self
                for x in args:
                    out = out + x
                return out
            elif quick_merge:
                return Selection(tuple(self._merge(args)), self.__apimother__)

            else:
                return self.merge(*args, safe_merge=True)
        except TypeError as exc:
            raise TypeError(
                "{} - Use the non_hash_merge to merge rows with non-hashable datatypes.".format(exc))

    def safe_merge(self, *args):
        """This is much slower but is hashes rows as processed instead of preprocessing them"""
        return self.merge(self, *args, safe_merge=True)

    def non_hash_merge(self, *args):
        """This merge uses the exploits the __output__ flag of a row instead of it's hashed contents
           This allows merging of of rows that contain unhashable mutable data such as sets or dict.
           This doesn't remove duplicate rows but is slightly faster and can handle all datatyps.

           Note: This function is effectively single-threaded and editing the outputflag during
           while its running will effect results of the merge.
        """
        if not all(self.__apimother__ is x.__apimother__ for x in args):
            raise Exception("non_hash_merge only accepts rows from same origin")
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

    def __add__(self, sel):
        return Selection(set(
            tuple(self.rows) + tuple(sel.rows)), self.__apimother__)

    @property
    def rows(self):
        if not isinstance(self.__rows__, tuple):
            self.__rows__ = tuple(self.__rows__)
            return self.__rows__
        else:
            return self.__rows__

    @property
    def columns(self):
        return self.__apimother__.__columns__

    @columns.setter
    def columns(self, v):
        self.__apimother__.__columns__ = v

    def single_find(self, selectionfirstarg_data=None, **kwargs):
        """Find a single row based off search criteria given.
            will raise error if returns more than one result"""
        try:
            result = None
            func = generate_func(selectionfirstarg_data, kwargs)
            g = self._find_all(func)
            result = next(g)
            next(g)
            raise Exception(msg.singlefindmsg)
        except StopIteration:
            return result

    def find(self, selectionfirstarg_data=None, **kwargs):
        try:
            func = generate_func(selectionfirstarg_data, kwargs)
            g = self._find_all(func)
            return next(g)
        except StopIteration:
            return None

    def _find_all(self, func):
        for x in self.rows:
            if func(x):
                yield x

    def find_all(self, selectionfirstarg_data=None, **kwargs):
        func = generate_func(selectionfirstarg_data, kwargs)
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
        """
        if not selectionfirstarg_data and not kwargs:
            return Selection(self.__rows__, self.__apimother__)
        func = generate_func(selectionfirstarg_data, kwargs)
        return self[func]

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
            raise SelectionError(msg.badgrab)

    def remove_duplicates(self, soft=True):
        """Removes duplicates.
           if soft is true, return a selection
           else: edit this object
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
            raise Exception("Empty Grab")

    def fast_add(self, sel):
        """faster than __add__, but doesn't guarantee no repeats."""
        return Selection(tuple(self.rows) + tuple(sel.rows), self.__apimother__)

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

    def addcolumn(self, columnname, columndata="", add_to_columns=True):
        """Adds a column
        :param columnname: Name of the column to add.
        :param columndata: The default value of the new column.
        :param add_to_columns: Determines whether this column should
            be added to the internal tracker.
        :type columnname: :class:`str`
        :type add_to_columns: :class:`bool`
        """
        for row in self.rows:
            row.addcolumn(columnname, columndata)
        if add_to_columns:
            self.columns += (columnname,)
        return self

    @property
    def outputtedrows(self):
        return Selection(filter(lambda x: x.outputrow, self.rows), self.__apimother__)

    @property
    def nonoutputtedrows(self):
        return Selection(filter(lambda x: not x.outputrow, self.rows), self.__apimother__)

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

    def output(self, loc=None, columns=None, quote_all=None, encoding="utf-8"):
        if not columns:
            columns = self.columns
        outputfile(loc, self.rows, columns,
                   quote_all=quote_all, encoding=encoding)

    def outputs(self, columns=None, quote_all=None, encoding="utf-8"):
        """Outputs to str"""
        if not columns:
            columns = self.columns
        return outputstr(self.rows, columns, quote_all=quote_all, encoding=encoding)
