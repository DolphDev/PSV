from ..utils import cleanup_name, asciireplace, limit_text
from ..exceptions.messages import RowObjectMsg as msg
from .formulas import Formula

from tabulate import tabulate

class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""

    __slots__ = ["__output__", "__flag__"]

    def __init__(self, data, *args, **kwargs):
        self.__flag__ = 2
        super(BaseRow, self).__init__(data)
        self.__output__ = True
        self(flag=1).construct(*args, **kwargs)
        self.resetflag()

    def __call__(self, flag=1):
        #flag 1 == dict_mode
        #flag 2 == psv_mode
        self.__flag__ = flag
        return self

    def resetflag(self, to=2):
        return self(flag=to)

    def construct(self, *args, **kwargs):
        """This method can be used by inherited objects of :class:`BaseRow`""" 
        pass

    def formula(self, columnname, func, rowref=None, **kwargs):
        """Replaces a cell with a formula

            :param columnname: Name of the column.
            :param func: Function that accepts 1 argument and optionally kwargs.
            :param rowref: The referenced row. Defaults to the current row.
            :param kwargs: Parameters that will be supplied to the function when ran.
            :type columnname: :class:`str`
            :type func: :class:`FunctionType`

            :returns: Nothing
            :rtype: :class:`NoneType`
        """
        if rowref is None:
            rowref = self
        self.setcolumn(columnname, Formula(func, rowref, **kwargs))

    def getformula(self, columnname):
        """Get Formula

            :param columnname: Gets the result of a formula. Used when 
            formulas referenced other formulas

        """
        try:
            return self.getcolumn(columnname).call()
        except ValueError:
            raise ValueError(
                msg.getformulamsg.format(columnname))

    @property
    def outputrow(self):
        """Returns a boolean of the current output flag for this row"""
        return self.__output__

    @outputrow.setter
    def outputrow(self, v):
        if not isinstance(v, bool):
            raise TypeError(msg.outputrowmsg.format(bool, type(v)))
        self.__output__ = v

    def __getitem__(self, key):
        if self.__flag__ == 1:
            result = super(BaseRow, self).__getitem__(key)
            self.resetflag()
            return result
        elif self.__flag__ == 2:
            result = self(flag=1)[key]["value"]
            return result
        else:
            raise Exception("Missing Flag")

    def __setitem__(self, key, v):
        if self.__flag__ == 1:
            super(BaseRow, self).__setitem__(key, v)
            self.resetflag()
        elif self.__flag__ == 2:
            result = self(flag=1).update({key: 
                {"value": v, "org_name": self(flag=1)[key]["org_name"]}})
            self.resetflag()
            return result
        else:
            raise Exception("Missing Flag")

    def __delitem__(self, key):
        if self.__flag__ == 1:
            super(BaseRow, self).__delitem__(key)
            self.resetflag()
        elif self.__flag__ == 2:
            self.__delattr__(key)
        else:
            raise Exception("Missing Flag")


    def getcolumn(self, column):
        """Get a cell by the orginal column name

        :param column: The column name. Can be both long and short form.
        :type column: :class:`str`

        :returns: String of the data, or an int/float if a number/decimal.
        :rtype: :class:`str`, :class:`int`, or :class:`float`
        """
        s = cleanup_name(column)
        if s in self.keys():
            return getattr(self, s)
        else:
            raise KeyError("{}".format(column))

    def setcolumn(self, column, value):
        """Set a cell by the orginal column name

            :param column: The column name. Can be both long and short form.
            :param value: The data to be set to the specified column
            :type column: :class:`str`

        """
        s = cleanup_name(column)
        if s in self.keys():
            self.__setattr__(s, value)
        else:
            raise Exception("{}".format(column))

    def delcolumn(self, column):
        """Delete a cell by the orginal column name

        :param column: The column name. Can be both long and short form.
        :type column: :class:`str`

        """

        s = cleanup_name(column)
        if s in self.keys():
            self.__delattr__(s)
        else:
            raise KeyError("{}".format(column))

    def __repr__(self):
        return "<'{rowname}':{columnamount}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())
            )

    def __str__(self):
        return "<'{rowname}':{columnamount}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())
            )

    def __pos__(self):
        self.outputrow = True
        return self

    def __neg__(self):
        self.outputrow = False
        return self

    def __invert__(self):
        self.outputrow = not (self.outputrow)
        return self

    def __getattribute__(self, attr):
        if not (attr in super(BaseRow, self).keys()) or self.__flag__ == 1:
            result = super(dict, self).__getattribute__(attr)
            return result
        else:
            result = (self(flag=1)[attr]["value"])
            return result

    def __getattr__(self, attr):
        s = cleanup_name(attr)
        if s in super(BaseRow, self).keys():
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

    def __setattr__(self, attr, v):
        """Allows setting of rows and attributes (Makes a row empty) by using =
            statement"""

        s = cleanup_name(attr)
        if attr in super(BaseRow, self).keys():
            self(flag=1)[attr]["value"] = v
            self.resetflag()
        elif s in super(BaseRow, self).keys():
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
            super(BaseRow, self).__setattr__(attr, v)

    def __delattr__(self, attr):
        """Allows deletion of rows and attributes (Makes a row empty) by using
        del statement"""
        s = cleanup_name(attr)
        if attr in super(BaseRow, self).keys():
            self(flag=1)[attr]["value"] = ""
        elif s in super(BaseRow, self).keys():
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
            super(BaseRow, self).__delattr__(attr)

    def addcolumn(self, columnname, columndata=""):
        """Adds a column for this row only"""
        short_cn = cleanup_name(columnname)
        if not self.get(short_cn):
            self[short_cn] = {"org_name":columnname, "value":columndata}
        else:
            raise Exception("Column already exists.")
        
    def longcolumn(self, columns=None):
        """
            :params columns: A collection of columns, if supplied the method 
                will return only the specified columns.
            :type columns: :class:`tuple`, :class:`list`

            :returns: Generates a :class:`dict` that uses orginal names of 
                the column.
            :rtype: :class:`dict`
        """
        newdict = {}
        if columns:
            shortcolumns_check = [cleanup_name(x) for x in columns]
        for k in self.keys():
            if columns:
                if not (k in shortcolumns_check):
                    continue
            newdict.update({self[k]["org_name"]: self[k]["value"]})

        return newdict

    def tabulate(self, format="grid", only_ascii=True, columns=None, text_limit=None):
        """Integrates tabulate library with psv

            :param format: A valid format for :class:`tabulate` library.
            :only_ascii: If :data:`True`, only return ascii characters.
            :param columns: Collection of column names that will be included in the 
                tabulating.
            :param text_limit: The number of characters to include per cell.
            :type format: :class:`str`

        """ 
        data = self.longcolumn()
        sortedcolumns = sorted(data) if not columns else columns

        result = tabulate(
            [sortedcolumns] + [[limit_text(data[c], text_limit) for c in sortedcolumns]],
            headers="firstrow", 
            tablefmt=format)
        if only_ascii:
            return asciireplace(result)
        else:
            return result