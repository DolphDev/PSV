from ..utils import cleanup_name, multiple_index, limit_text
from ..utils import  _index_function_gen, generate_func, asciireplace
from ..exceptions.messages import ApiObjectMsg as msg

from types import FunctionType
from tabulate import tabulate

class Selection(object):

    __slots__ = ["__rows__"]


    def __init__(self, selection):
        self.__rows__ = (selection)

        if not self.rows:
            Exception("Selection Error")

    @property
    def rows(self):
        if not isinstance(self.__rows__, tuple):
            self.__rows__ = tuple(self.__rows__)
            return self.__rows__
        else:
            return self.__rows__

    @property
    def columns(self):
        return sorted(tuple(self.rows[0].longcolumn().keys()))

    def single_find(self, f=None, **kwargs):
        try:
            result = None
            func = generate_func(f, kwargs)
            g = self._find_all(func)
            result = next(g)
            next(g)
            raise Exception(msg.singlefindmsg)
        except StopIteration:
            return result

    def find(self, f=None, **kwargs):
        try:
            func = generate_func(f, kwargs)
            g = self._find_all(func)
            return next(g)
        except StopIteration:
            return None

    def _find_all(self, func):
        for x in self.rows:
            if func(x):
                yield x

    def find_all(self, f=None, **kwargs):
        func = generate_func(f, kwargs)
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

    def enable(self, f=None, **kwargs):
        v = generate_func(f, kwargs)
        for x in self.rows:
            if bool(v(x)):
                +x
        return self

    def disable(self, f=None, **kwargs):
        v = generate_func(f, kwargs)
        for x in self.rows:
            if bool(v(x)):
                -x
        return self

    def flip(self, f=None, **kwargs):
        v = generate_func(f, kwargs)
        for x in self.rows:
            if bool(v(x)):
                ~x
        return self

    def select(self, f=None, **kwargs):
        if not f and not kwargs:
            return Selection(self.__rows__)
        func = generate_func(f, kwargs)
        return self[func]

    def grab(self, *args):
        arg = tuple(args)
        if len(arg) > 1:
            return tuple(self[arg])
        elif len(arg) == 1:
            return tuple(self[arg[0]])
        else:
            raise Exception("Empty Grab")

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
    def outputtedrows(self):
        return Selection(filter(lambda x:x.outputrow, self.rows))

    @property
    def nonoutputtedrows(self):
        return Selection(filter(lambda x: not x.outputrow, self.rows))

    def tabulate(self, limit=100, format="grid", only_ascii=True, columns=None, text_limit=None):
        data = [x.longcolumn() for x in self.rows[:limit]]
        sortedcolumns = self.columns if not columns else columns
        result = tabulate(
            [sortedcolumns] + [[limit_text(x[c], text_limit) for c in sortedcolumns] for x in data],
            headers="firstrow", 
            tablefmt=format)
        if only_ascii:
            return asciireplace(result)
        return result