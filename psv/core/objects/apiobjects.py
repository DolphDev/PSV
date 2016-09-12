from ..output import outputfile
from ..objects import BaseRow, Selection
from ..parsing import parser, parser_addrow
from ..utils import multiple_index, _index_function_gen
from ..utils import column_string, generate_func
from ..exceptions.messages import ApiObjectMsg as msg
from types import FunctionType

class Api(Selection):
    """This class centralizes the parsing, output, and objects
    functionality of this script"""

    __slots__ = ["__outputname__", "__canrefrencecolumn__", 
                 "__columns__", "__columnsmap__", 
                 "__rows__"]

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

    def rebuildcolumnsmap(self, columns):
        self.__canrefrencecolumn__ = True
        self.__columns__ = columns
        self.__columnsmap__ = {column_string(i+1): 
                c for i,c in enumerate(self.__columns__)}

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
        self.rebuildcolumnsmap(v)

    def getcell(self, letter, number=None):
        """Accepts an excel like letter-number to directly reference a 'cell'"""
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

    def __delitem__(self, v):
        del self.__rows__[v]

    def sort(self, keyfunc):
        self.__rows__ = sorted(self.__rows__, key=keyfunc)

    def output(self, loc=None, columns=None, quote_all=None, encoding="utf-8"):
        loc = loc if loc else self.__outputname__
        if not columns:
            columns = self.__columns__
        outputfile(loc, self.rows, columns, quote_all=quote_all, encoding=encoding )
