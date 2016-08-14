from ..utils import cleanup_name



class Selection(object):

    __slots__ = ["rows"]


    def __init__(self, selection):
        self.rows = tuple(selection)
        if not self.rows:
            Exception("Selection Error")

    @property
    def columns(self):
        return tuple(self.rows[0].keys())

    def __getattr__(self, attr):
        s = cleanup_name(attr)
        if attr in self.columns:
            return self[attr]
        if s in self.columns:
            raise AttributeError((
                "{}{}"
                .format(
                '\'{}\' has no attribute \'{}\''.format(
                    type(self), attr),
                ". However, '{s}' is an existing condensed ".format(s=s) + 
                "column name. Only the condensed version is supported."
                .format(s=s)
                )))
        else:
            raise AttributeError('\'{}\' has no attribute \'{}\''.format(
        type(self), attr))

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
            return (_index_function_gen(self, v))
        else:
            raise TypeError("Row indices must be int, slices, str, tuple, or functions. Not {}".format(type(v)))
