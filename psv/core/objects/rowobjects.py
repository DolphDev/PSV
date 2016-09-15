from ..utils import cleanup_name, asciireplace, limit_text
from ..exceptions.messages import RowObjectMsg as msg
from .formulas import Formula

from tabulate import tabulate

class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""

    __slots__ = ["__output__"]

    def __init__(self, data, *args, **kwargs):
        super(BaseRow, self).__init__(data)
        self.construct(*args, **kwargs)
        self.__output__ = True

    def construct(self, *args, **kwargs):
        pass

    def formula(self, columnname, func, rowref=None, **kwargs):
        if rowref is None:
            rowref = self
        self.setcolumn(columnname, Formula(func, rowref, **kwargs))

    def getformula(self, columnname):
        """Get Formula"""
        try:
            return self.getcolumn(columnname).call()
        except ValueError:
            raise ValueError(
                msg.getformulamsg.format(columnname))

    @property
    def outputrow(self):
        return self.__output__

    @outputrow.setter
    def outputrow(self, v):
        if not isinstance(v, bool):
            raise TypeError(msg.outputrowmsg.format(bool, type(v)))
        self.__output__ = v

    def getcolumn(self, v):
        "Get column by the orginal column name"
        s = cleanup_name(v)
        if s in self.keys():
            return getattr(self, s)
        else:
            raise KeyError("{}".format(v))

    def setcolumn(self, a, v):
        s = cleanup_name(a)
        if s in self.keys():
            self.__setattr__(s, v)
        else:
            raise Exception("{}".format(a))

    def delcolumn(self, v):
        s = cleanup_name(a)
        if s in self.keys():
            self.__delattr__(s, v)
        else:
            raise KeyError("{}".format(a))

    def __repr__(self):
        return "<'{rowname}':{columnamount}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())
            )

    def __str__(self):
        data = self.longcolumn()
        sortedcolumns = sorted(data)

        return tabulate(
            [sortedcolumns] + [[data[c] for c in sortedcolumns]],
            headers="firstrow", 
            tablefmt="grid")

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
        if not (attr in super(BaseRow, self).keys()):
            return super(dict, self).__getattribute__(attr)
        else:
            return (self[attr]["value"])

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
        """Allows setting new data to row
        is called if row does not have specially 
        defined set behavior"""
        s = cleanup_name(attr)
        if attr in super(BaseRow, self).keys():
            self[attr]["value"] = v
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
            self[attr]["value"] = ""
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
        """Adds a column"""
        short_cn = cleanup_name(columnname)
        if not self.get(short_cn):
            self[short_cn] = {"org_name":columnname, "value":columndata}
        else:
            raise Exception("Column already exists.")
        
    def longcolumn(self, columns=None):
        """Generates a Dict that uses orginal names of 
        the column, used for output"""
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