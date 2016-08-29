from ..utils import cleanup_name
from ..exceptions.messages import RowObjectMsg as msg
from ..exceptions import DeletedRow as DeletedRow_Err
from .formulas import Formula

class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""

    __slots__ = ["__output__"]

    def __init__(self, data, *args, **kwargs):
        super(BaseRow, self).__init__(data)
        self.construct(*args, **kwargs)
        self.__output__ = True

    def construct(self, *args, **kwargs):
        pass

    @property
    def is_deleted(self):
        return False

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
        return "<'{}':{}'>".format(
            self.__class__.__name__,
            len(self.keys()))

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
        try:
            if attr in super(BaseRow, self).keys():
                self[attr]["value"] = v
            else:
                super(BaseRow, self).__setattr__(attr, v)

        except (KeyError, AttributeError):
            super(BaseRow, self).__setattr__(attr, v)

    def __delattr__(self, attr):
        """Allows deletion of rows and attributes (Makes a row empty) by using
        del statement"""
        try:
            if attr in super(BaseRow, self).keys():
                self[attr]["value"] = ""
            else:
                super(BaseRow, self).__delattr__(attr)

        except (KeyError, AttributeError):
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

class DeletedRow(object):

    __slots__ = []

    @property
    def outputrow(self):
        return False

    @property
    def is_deleted(self):
        return True

    def __getitem__(self, v):
        raise DeletedRow_Err("Row is deleted")

    def __getattr__(self, attr):
        raise DeletedRow_Err("Row is deleted")

    def __getattribute__(self, attr):
        if attr in ["outputrow", "is_deleted"]:
            return super(DeletedRow, self).__getattribute__(attr)
        raise DeletedRow_Err("Row is deleted")


    def __pos__(self):
        raise DeletedRow_Err("Row is deleted")


    def __neg__(self):
        raise DeletedRow_Err("Row is deleted")


    def __invert__(self):
        raise DeletedRow_Err("Row is deleted")
