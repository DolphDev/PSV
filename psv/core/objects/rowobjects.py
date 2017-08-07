from ..utils import asciireplace, limit_text
from ..exceptions import RowError, FlagError
from ..exceptions.messages import RowObjectMsg as msg

from tabulate import tabulate
from string import ascii_lowercase, digits

import keyword
accepted_chars = (ascii_lowercase + "_" + digits)


class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""
    __slots__ = ["__delwhitelist__", "__dirstore__", "__output__", "__sawhitelist__"]

    def __init__(self, data, *args, **kwargs):
        super(BaseRow, self).__setattr__("__delwhitelist__", set())
        super(BaseRow, self).__setattr__("__dirstore__", (set(dir(self))))
        super(BaseRow, self).__setattr__("__sawhitelist__", set(("__output__", "outputrow")))
        super(BaseRow, self).__init__(data)
        self.__output__ = True

        self.construct(*args, **kwargs)

    def __call__(self, column, setvalue=None, delete=False):
        """Alais for .getcolumn() family of methods"""
        if delete:
            self.delcolumn(column)
        elif setvalue is None:
            return self.getcolumn(column)
        else:
            self.setcolumn(column, setvalue)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hashvalue__() == other.__hashvalue__()
        return False

    def __hashvalue__(self):
        """raw data that can be hashed if all contents are hashable"""
        return (tuple((column, self[column]["value"]) for column in sorted(self.keys())))

    def __repr__(self):
        return "<'{rowname}':{columnamount}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())
        )

    def __str__(self):
        rv = "<'{rowname}':{columnamount}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())
        )
        return rv

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
        if not super(BaseRow, self).get(attr, False):
            return super(dict, self).__getattribute__(attr)
        else:
            result = (self[attr]["value"])
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
            raise AttributeError(msg.attribute_missing.format(
                type(self), attr))

    def __setattr__(self, attr, v):
        """Allows setting of rows and attributes by using =
            statement"""
        s = cleanup_name(attr)
        if attr in self.keys():
            self[attr]["value"] = v
        elif s in self.keys():
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
            if attr in self.__sawhitelist__:
                super(BaseRow, self).__setattr__(attr, v)
            elif attr in self.__dirstore__:
                raise AttributeError(
                    msg.attribute_readonly.format(classname=self.__class__, attr=attr))
            else:
                raise AttributeError(msg.attribute_missing.format(
                type(self), attr))

    def __delattr__(self, attr):
        """Allows deletion of rows and attributes (Makes a row empty) by using
        del statement"""
        s = cleanup_name(attr)
        if attr in self.keys():
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
            if attr in self.__delwhitelist__:
                super(BaseRow, self).__delattr__(attr)
            elif attr in self.__dirstore__:
                raise AttributeError(
                    msg.attribute_readonly.format(classname=self.__class__, attr=attr))
            else:
                raise AttributeError(msg.attribute_missing.format(
                type(self), attr))

    def add_valid_attribute(self, attr, deletable=False):
        "Used by classes that inherit to add attributes to the whitelists"
        if self.__class__ is BaseRow:
            raise TypeError(msg.inherited_rows)
        super(BaseRow, self).__setattr__(
            "__sawhitelist__", set(self.__sawhitelist__ | set((attr,))))
        if deletable:
            super(BaseRow, self).__setattr__(
                "__delwhitelist__", set(self.__delwhitelist__ | set((attr,))))


    def construct(self, *args, **kwargs):
        """This method can be used by inherited objects of :class:`BaseRow` as if it was __init__"""
        pass

    @property
    def outputrow(self):
        """Returns a boolean of the current output flag for this row"""
        return self.__output__

    @outputrow.setter
    def outputrow(self, v):
        if not isinstance(v, bool):
            raise TypeError(msg.outputrowmsg.format(bool, type(v)))
        self.__output__ = v


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
            raise KeyError("{}".format(column))

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

    def addcolumn(self, columnname, columndata=""):
        """Adds a column for this row only"""
        short_cn = cleanup_name(columnname)
        if not self.get(short_cn):
            self[short_cn] = {
                "org_name": columnname, "value": columndata}
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
            newdict.update(
                {self[k]["org_name"]: self[k]["value"]})
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
            [sortedcolumns] +
            [[limit_text(data[c], text_limit) for c in sortedcolumns]],
            headers="firstrow",
            tablefmt=format)
        if only_ascii:
            return asciireplace(result)
        else:
            return result

#This block was in utils, 
# but it relied on a circular reference that re-imported
# a variable everytime this core function was called.
#While less clean, this produces a decent speedup.
non_accepted_key_names = set(tuple(dir(
    BaseRow)) + ("row_obj",) + tuple(keyword.kwlist))
bad_first_char = set(digits)
store_cleanup = {}


def cleanup_name(s):
    sresult = store_cleanup.get(s, False)
    if sresult: return sresult
    result = "".join(filter(lambda x: x in accepted_chars, s.lower()))
    if not result:
        raise ValueError(msg.non_valid.format(s))
    if result in non_accepted_key_names or result[0] in bad_first_char:
        result = "psv_" + result
    store_cleanup.update({s:result})
    return result
