from .core.output import outputfile
from .core.objects import BaseRow
from .core.parsing import parser, excelparser, parser_addrow
from .utils import argstotuple, multiple_index

class FatStax(object):
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

    def __getitem__(self, v):
        if isinstance(v, int):
            return self.rows[v]
        elif isinstance(v, str):
            return (x.getcolumn(v) for x in self.rows)
        elif isinstance(v, tuple):
            return (multiple_index(x,v) for x in self.rows)
        else:
            super(self, FatStax).__getitem__(v)

    def output(self, loc=None, columns=None, quote_all=None, encoding="LATIN-1"):
        if not columns:
            raise Exception("A ordered list of columns must be supplied to output the file")
        outputfile(loc, self.rows, columns, quote_all=quote_all, encoding=encoding )
