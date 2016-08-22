from ..utils import cleanup_name, multiple_index, _index_function_gen
from ..exceptions.messages import ApiObjectMsg as msg

from types import FunctionType

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
        return tuple(self.rows[0].keys())

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
