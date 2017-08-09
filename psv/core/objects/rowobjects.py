from ..utils import asciireplace, limit_text
from ..exceptions.messages import RowObjectMsg as msg
from functools import lru_cache
from tabulate import tabulate
from string import ascii_lowercase, digits

import keyword
accepted_chars = (ascii_lowercase + "_" + digits)


class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""
    __slots__ = ["__delwhitelist__", "__dirstore__", "__output__", "__sawhitelist__"]

    def __init__(self, data, columns_map, *args, **kwargs):
        super(BaseRow, self).__setattr__("__delwhitelist__", 
            BaseRowDefaults.__delwhitelist__)
        super(BaseRow, self).__setattr__("__dirstore__",
            BaseRowDefaults.__dirstore__)
        super(BaseRow, self).__setattr__("__sawhitelist__",
            BaseRowDefaults.__sawhitelist__)
        super(BaseRow, self).__init__(data)
        self[BaseRowDefaults.__psvcolumns__] = columns_map
        self.__output__ = True

        self.construct(*args, **kwargs)

    def __call__(self, column, setvalue=None, delete=False):
        """Alais for .getcolumn() family of methods"""
        if delete:
            self.delcolumn(column, False)
        elif setvalue is None:
            return self.getcolumn(column, False)
        else:
            self.setcolumn(column, setvalue, False)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hashvalue__() == other.__hashvalue__()
        return False

    def __hashvalue__(self):
        """raw data that can be hashed if all contents are hashable"""
        return (tuple((column, self[column])
            for column in filter(lambda x: x != "__psvcolumnstracker__", sorted(self.keys()))))

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
        if not self["__psvcolumnstracker__"].get(attr, False):
            return super(dict, self).__getattribute__(attr)
        else:
            return self[self["__psvcolumnstracker__"][attr]]

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
        if attr in self["__psvcolumnstracker__"].keys():
            self[self["__psvcolumnstracker__"][attr]] = v
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
        if attr in self["__psvcolumnstracker__"].keys():
            self[self["__psvcolumnstracker__"][attr]] = ""
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


    def getcolumn(self, column, accept_small_names=True):
        """Get a cell by the orginal column name

        :param column: The column name. Can only be long form if accept_small_names == False
        :type column: :class:`str`

        :returns: String of the data, or an int/float if a number/decimal.
        :rtype: :class:`str`, :class:`int`, or :class:`float`
        """
        if column in self.keys():
            return (self[column])
        elif accept_small_names:
            s = cleanup_name(column)
            try:
                return getattr(self, s)
            except AttributeError:
                #pass to below bode
                pass 
        if not accept_small_names:
            raise KeyError("'{}'".format(column))
        else:
            raise KeyError("'{}'. Make sure the shorterned columns name have no collisions".format(column))

    def setcolumn(self, column, value, accept_small_names=True):
        """Set a cell by the orginal column name

            :param column: The column name. Can be both long and short form.
            :param value: The data to be set to the specified column
            :type column: :class:`str`

        """

        if column in self.keys():
            self[column] = value
        elif accept_small_names:
            s = cleanup_name(column)
            try:
                self.__setattr__(s, value)
            except AttributeError:
                #pass to below code
                pass
        if not accept_small_names:
            raise KeyError("'{}'".format(column))
        else:
            raise KeyError("'{}'. Make sure the shorterned columns name have no collisions".format(column))

    def delcolumn(self, column, accept_small_names=True):
        """Delete a cell by the orginal column name

        :param column: The column name. Can be both long and short form.
        :type column: :class:`str`

        """
        if column in self.keys():
            self[column] = ""
        elif accept_small_names:
            s = cleanup_name(column)
            try:
                self.__delattr__(s)
            except AttributeError:
                #pass to below code
                pass
        if not accept_small_names:
            raise KeyError("'{}'".format(column))
        else:
            raise KeyError("'{}'. Make sure the shorterned columns name have no collisions".format(column))

    def addcolumn(self, columnname, columndata=""):
        """Adds a column for this row only
            doesn't add to column tracker"""
        if not self.get(columnname):
            self[columnname] = columndata
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
        for k in columns or self.keys():
            if k == "__psvcolumnstracker__":
                continue
            newdict.update({
                k: self[k]})
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

class BaseRowDefaults(object):
    __delwhitelist__ = set()
    __dirstore__ = set(dir(BaseRow))
    __sawhitelist__ = set(("__output__", "outputrow"))
    __psvcolumns__ = '__psvcolumnstracker__'
#This block was in utils, 
# but it relied on a circular reference that re-imported
# a variable everytime this core function was called.
#While less clean, this produces a decent speedup.
non_accepted_key_names = set(tuple(dir(
    BaseRow)) + ("row_obj",) + tuple(keyword.kwlist))
bad_first_char = set(digits)
store_cleanup = {}

@lru_cache(256)
def cleanup_name(s):
    sresult = store_cleanup.get(s, False)
    if sresult: return sresult
    result = "".join(filter(lambda x: x in accepted_chars, s.lower()))
    if not result:
        raise ValueError(msg.non_valid.format(s))
    if result in non_accepted_key_names or result[0] in bad_first_char:
        result = "psv_" + result
    return result
