from ..objects import BaseRow, Selection
from ..parsing import parser, parser_addrow
from ..utils import multiple_index, _index_function_gen
from ..utils import column_string, generate_func
from ..exceptions.messages import ApiObjectMsg as msg
from types import FunctionType


class MainSelection(Selection):
    """This extended selection allows the acceptance of the parsing data and the ability
    to delete/add rows in a supported way"""

    __slots__ = ["__outputname__", "__canrefrencecolumn__",
                 "__columns__", "__columnsmap__",
                 "__rows__", "__apimother__"]

    def __init__(self, csvdict=None, columns=None, cls=BaseRow, parsing=parser, outputfile=None, typetranfer=True, *args, **kwargs):
        # Since I close the file after this, the row must be placed into memory
        if "__flag__" in columns:
            raise KeyError("__flag__ is not a supported column")
        self.__apimother__ = self
        self.__outputname__ = outputfile
        if columns is None:
            self.__canrefrencecolumn__ = False
            self.__columns__ = None
            self.__columnsmap__ = None
        else:
            self.__canrefrencecolumn__ = True
            self.__columns__ = columns
            self.__columnsmap__ = {column_string(i+1):
                                   c for i, c in enumerate(self.__columns__)}

        if csvdict is None:
            csvdict = {}
        if csvdict:
            self.__rows__ = list(
                parser(csvdict, cls, typetranfer, *args, **kwargs))
        else:
            self.__rows__ = list()

    def rebuildcolumnsmap(self, columns):
        self.__canrefrencecolumn__ = True
        self.__columns__ = columns
        self.__columnsmap__ = {column_string(i+1):
                               c for i, c in enumerate(self.__columns__)}

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
        """Accepts an excel like letter-number to directly reference a 'cell'

            :param letter: A letter such as "A". Used in the same fashion of spreadsheet software.
            :param number: A number that referencing a position in the index.
            :type letter: str
        """
        if self.__canrefrencecolumn__:
            if number is not None:
                try:
                    return self.rows[number].getcolumn(self.__columnsmap__[letter])
                except KeyError:
                    raise KeyError(
                        "{} is not mapped to any column".format(letter))
                except IndexError as err:
                    raise err
            else:
                try:
                    return self[self.__columnsmap__[letter]]
                except KeyError:
                    raise KeyError(
                        "{} is not mapped to any column".format(letter))
        else:
            raise Exception(
                "Column mapping not supported. Columns must be provided during intialization")

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

    def addrow(self, columns=None, cls=BaseRow, **kwargs):
        r = parser_addrow(columns if columns else self.__columns__, cls)
        self.__rows__.append(r)
        if kwargs:
            for k, v in kwargs.items():
                r.setcolumn(k, v)
        return r

    def __delitem__(self, v):
        del self.__rows__[v]
