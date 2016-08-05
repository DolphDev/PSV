from .core.output import outputfile
from .core.objects import BaseRow
from .core.parsing import parser, excelparser, parser_addrow
from .utils import multiple_index
from types import FunctionType

import csv

class Api(object):
    """This class centralizes the parsing, output, and objects
    functionality of this script"""

    def __init__(self, csvdict=None, cls=BaseRow, parsing=parser, *args, **kwargs):
        #Since I close the file after this, the row must be placed into memory
        if csvdict is None:
            csvdict = {}
        if csvdict:
            self.rows = list(parser(csvdict, cls, *args, **kwargs))
        else:
            self.rows = list()

    def addrow(self, columns, cls=BaseRow):
        r = parser_addrow(columns, cls)
        self.rows.append(r)
        return r

    def flipoutput(self):
        for x in self.rows:
            ~x
        return self

    def __len__(self):
        return len(self.rows)

    def lenoutput(self):
        return len(tuple(filter(lambda x: x.outputrow, self.rows)))

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
        if not columns:
            raise Exception("A ordered list of columns must be supplied to output the file")
        outputfile(loc, self.rows, columns, quote_all=quote_all, encoding=encoding )


def load(f, cls=BaseRow, delimiter=",", quotechar='"', mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    with open(f, mode=mode, buffering=buffering,
        encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        columns = csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar)
        api = Api(columns, cls=cls)
    return api

def columns_names(f, cls=BaseRow, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    with open(f, mode=mode, buffering=buffering,
        encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        columns = next(csv.reader(csvfile, delimiter=',', quotechar=quotechar))
    return columns
