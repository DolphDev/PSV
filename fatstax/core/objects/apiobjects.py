from ..output import outputfile
from ..objects import BaseRow, Selection
from ..parsing import parser, excelparser, parser_addrow
from ..utils import multiple_index, _index_function_gen
from ..exceptions.messages import ApiObjectMsg as msg
from types import FunctionType

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

    def enable(self, v):
        for x in self.rows:
            if bool(v(x)):
                +x
    def disable(self, v):
        for x in self.rows:
            if bool(v(x)):
                -x

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, v):
        if isinstance(v, slice):
            return Selection(self.rows[v])
        if isinstance(v, int):
            return (self.rows[v])
        elif isinstance(v, str):
            return (x.getcolumn(v) for x in self.rows)
        elif isinstance(v, tuple):
            return (multiple_index(x,v) for x in self.rows)
        elif isinstance(v, FunctionType):
            return Selection(_index_function_gen(self, v))
        else:
            raise TypeError(msg.getitemmsg.format(type(v)))

    @property
    def outputedrows(self):
        return Selection(filter(lambda x:x.outputrow, self.rows))

    def output(self, loc=None, columns=None, quote_all=None, encoding="utf-8"):
        loc = loc if loc else self.__outputname__
        if not columns:
            raise Exception(msg.outputmsg)
        outputfile(loc, self.rows, columns, quote_all=quote_all, encoding=encoding )
