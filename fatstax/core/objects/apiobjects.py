from ..output import outputfile
from ..objects import BaseRow, Selection, DeletedRow
from ..parsing import parser, excelparser, parser_addrow
from ..utils import multiple_index, _index_function_gen, column_string
from ..exceptions.messages import ApiObjectMsg as msg
from types import FunctionType

class Api(object):
    """This class centralizes the parsing, output, and objects
    functionality of this script"""

    def __init__(self, csvdict=None, columns=None,cls=BaseRow, parsing=parser, outputfile=None, typetranfer=True, *args, **kwargs):
        #Since I close the file after this, the row must be placed into memory
        self.__outputname__ = outputfile
        if columns is None:
            self.__canrefrencecolumn__ = False
            self.__columns__ = None
            self.__columnsmap__ = None
        else:
            self.__canrefrencecolumn__ = True
            self.__columns__ = columns
            self.__columnsmap__ = {column_string(i+1): 
                c for i,c in enumerate(self.__columns__)}


        if csvdict is None:
            csvdict = {}
        if csvdict:
            self.__rows__ = list(parser(csvdict, cls, typetranfer, *args, **kwargs))
        else:
            self.__rows__ = list()

    def rebuildcellmap(self, columns):
        self.__canrefrencecolumn__ = True
        self.__columns__ = columns
        self.__columnsmap__ = {column_string(i+1): 
                c for i,c in enumerate(self.__columns__)}

    @property
    def rows(self):
        return self.__rows__

    @rows.deleter
    def rows(self, v):
        del self[v]

    def getcell(self, letter, number=None):
        """Accepts an excel like letter number cell systems"""
        if self.__canrefrencecolumn__:
            if number is not None:
                try:
                    return self.rows[number].getcolumn(self.__columnsmap__[letter])
                except KeyError:
                    raise KeyError("{} is not mapped to any column".format(letter))
                except IndexError as err:
                    raise err
            else:
                try:
                    return self[self.__columnsmap__[letter]]
                except KeyError:
                    raise KeyError("{} is not mapped to any column".format(letter))
        else:
            raise Exception("Column mapping not supported. Columns must be provided during intialization")

    def setcell(self, letter, number, value):
        try:
            return self.rows[number].setcolumn(self.__columnsmap__[letter], val)
        except KeyError:
            raise KeyError("{} is not mapped to any column".format(letter))
        except IndexError as err:
            raise err       

    def delcell(self, letter, number):
        try:
            return self.rows[number].delcolumn(self.__columnsmap__[letter])
        except KeyError:
            raise KeyError("{} is not mapped to any column".format(letter))
        except IndexError as err:
            raise err       

    def addrow(self, columns=None, cls=BaseRow):
        r = parser_addrow(columns if columns else self.__columns__, cls)
        self.__rows__.append(r)
        return r

    def single_find(self, func):
        try:
            g = self._find_all(func)
            result = next(g)
            next(g)
            raise Exception(msg.singlefindmsg)
        except StopIteration:
            return result

    def find(self, func):
        try:
            g = self._find_all(func)
            return next(g)
        except StopIteration:
            return None

    def _find_all(self, func):
        for x in self.rows:
            if func(x):
                yield x

    def find_all(self, func):
        return tuple(self._find_all(func))

    def flipoutput(self):
        for x in self.rows:
            ~x
        return self

    def no_output(self):
        for x in self.rows:
            -x
        return self

    def all_output(self):
        for x in self.rows:
            +x
        return self

    def lenoutput(self):
        return len(tuple(filter(lambda x: x.outputrow, self.rows)))

    def enable(self, f):
        for x in self.rows:
            if bool(f(x)):
                +x
    def disable(self, f):
        for x in self.rows:
            if bool(f(x)):
                -x

    def flip(self, f):
        for x in self.rows:
            if bool(f(x)):
                ~x

    def select(self, f):
        return self[f]

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, v):
        if isinstance(v, slice):
            return Selection(self.rows[v])
        if isinstance(v, int):
            return (self.rows[v])
        elif isinstance(v, str):
            return (x.getcolumn(v) for x in filter(lambda x:not x.is_deleted, self.rows))
        elif isinstance(v, tuple):
            return (multiple_index(x,v) for x in filter(lambda x:not x.is_deleted, self.rows))
        elif isinstance(v, FunctionType):
            return Selection(_index_function_gen(self, v))
        else:
            raise TypeError(msg.getitemmsg.format(type(v)))

    def __delitem__(self, v):
        self.__rows__[v] = DeletedRow()

    @property
    def outputtedrows(self):
        return Selection(filter(lambda x:x.outputrow, self.rows))

    @property
    def nonoutputtedrows(self):
        return Selection(filter(lambda x: not x.outputrow, self.rows))


    def output(self, loc=None, columns=None, quote_all=None, encoding="utf-8"):
        loc = loc if loc else self.__outputname__
        if not columns:
            columns = self.__columns__
        outputfile(loc, self.rows, columns, quote_all=quote_all, encoding=encoding )
