from .core.output import outputfile
from .core.objects import BaseRow
from .core.parsing import parser, excelparser, parser_addrow
from .core.utils import multiple_index
from types import FunctionType

import csv

class Api(object):
    """This class centralizes the parsing, output, and objects
    functionality of this script"""

    def __init__(self, csvdict=None, cls=BaseRow, parsing=parser, outputfile=None, typetranfer=True, *args, **kwargs):
        #Since I close the file after this, the row must be placed into memory
        self.__outputname__ = outputfile
        if csvdict is None:
            csvdict = {}
        if csvdict:
            self.rows = list(parser(csvdict, cls, typetranfer, *args, **kwargs))
        else:
            self.rows = list()

    def addrow(self, columns, cls=BaseRow):
        r = parser_addrow(columns, cls)
        self.rows.append(r)
        return r

    def single_find(self, func):
        try:
            g = self._find_all(func)
            result = next(g)
            next(g)
            raise Exception("Function returned more than 1 result")
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

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, v):
        if isinstance(v, slice):
            return self.rows[v] 
        if isinstance(v, int):
            return self.rows[v]
        elif isinstance(v, str):
            return (x.getcolumn(v) for x in self.rows)
        elif isinstance(v, tuple):
            return (multiple_index(x,v) for x in self.rows)
        elif isinstance(v, FunctionType):
            for x in self.rows:
                if bool(v(x)):
                    +x
            return self
        else:
            raise TypeError("Row indices must be int, slices, str, tuple, or functions. Not {}".format(type(v)))

    def __delitem__(self, v):
        if isinstance(v, FunctionType):
            for x in self.rows:
                if bool(v(x)):
                    -x
        else:
            del self.rows[v]

    @property
    def outputedrows(self):
        return filter(lambda x:x.outputrow, self.rows)

    def output(self, loc=None, columns=None, quote_all=None, encoding="utf-8"):
        loc = loc if loc else self.__outputname__
        if not columns:
            raise Exception("A ordered list of columns must be supplied to output the file")
        outputfile(loc, self.rows, columns, quote_all=quote_all, encoding=encoding )


def load(f, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetranfer=True):
    with open(f, mode=mode, buffering=buffering,
        encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        data = csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar)
        api = Api(data, outputfiled=outputfile, cls=cls, typetranfer=typetranfer)
    return api

def new(cls=BaseRow, outputfile=None):
    return Api(outputfiled=outputfile, cls=cls)

def column_names(f, cls=BaseRow, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8", errors=None, newline=None, closefd=True, opener=None):
    with open(f, mode=mode, buffering=buffering,
        encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        columns = next(csv.reader(csvfile, delimiter=',', quotechar=quotechar))
    return tuple(columns)
