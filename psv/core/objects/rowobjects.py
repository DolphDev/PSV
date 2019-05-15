from ..utils import asciireplace, limit_text
from ..exceptions.messages import RowObjectMsg as msg
from functools import lru_cache
from tabulate import tabulate
from string import ascii_lowercase, digits
from types import FunctionType


import keyword
accepted_chars = (ascii_lowercase + "_" + digits)


class Row(dict):
    """This Class represents a row in a spreadsheet
        This object is a highly specialized dict, meant to allow
        extremely quick and easy access/manipulation to row data
        at an acceptable memory cost. 

    """

    __slots__ = ["__delwhitelist__", "__output__", "__sawhitelist__"]

    def __init__(self, data, columns_map, *args, **kwargs):
        # These are used to 
        super(Row, self).__setattr__("__delwhitelist__", 
            RowDefaults.__delwhitelist__)
        super(Row, self).__setattr__("__sawhitelist__",
            RowDefaults.__sawhitelist__)
        super(Row, self).__init__(data)
        self[RowDefaults.__psvcolumns__] = columns_map
        self._set_outputrow(True)

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
        #Returns True if content is the same as the
        if isinstance(other, self.__class__):
            return self.__hashvalue__() == other.__hashvalue__()
        return False

    def __hashvalue__(self):
        """raw data that can be hashed if all contents are hashable
           or can be used for comparison
        """
        return (tuple((column, self[column])
            for column in filter(lambda x: x != "__psvcolumnstracker__", sorted(self.keys()))))

    def __repr__(self):
        return "<{rowname}:{columnamount} object at {hexloc}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())-1,
            hexloc=hex(id(self)).upper().replace("X", "x")
        )

    def __str__(self):
        return "<{rowname}:{columnamount} object at {hexloc}>".format(
            rowname=self.__class__.__name__,
            columnamount=len(self.keys())-1,
            hexloc=hex(id(self)).upper().replace("X", "x")
        )

    def __pos__(self):
        self._set_outputrow(True)
        return self

    def __neg__(self):
        self._set_outputrow(False)
        return self

    def __invert__(self):
        self._set_outputrow(not (self.outputrow))
        return self

    def __getattribute__(self, attr):
        if not self["__psvcolumnstracker__"].get(attr, False):
            return super(dict, self).__getattribute__(attr)
        else:
            return self[self["__psvcolumnstracker__"][attr]]

    def __getattr__(self, attr):
        """Handles all exception handeling when __getattribute__ fails"""
        s = cleanup_name(attr)
        if s in self["__psvcolumnstracker__"].keys():
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
            statement

            Note: Setting class Attributes is not optimized, this dict has specialized around
                dynamic attribute (from row data) access. Regular Attribute Setting may be much slower.
            """
        s = cleanup_name(attr)
        try:
            self[self["__psvcolumnstracker__"][attr]] = v
        except KeyError:
            if attr in self.__sawhitelist__:
                super(Row, self).__setattr__(attr, v)
            else:
                keys = self["__psvcolumnstracker__"].keys() 
                if s in keys:
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
                    # A somewhat hacky implementation of Dict's restriction of editing it's
                    # Attributes.
                    if attr in dir(self):
                        raise AttributeError(
                            msg.attribute_readonly.format(classname=self.__class__, attr=attr))
                    else:
                        raise AttributeError(msg.attribute_missing.format(
                        type(self), attr))

    def __delattr__(self, attr):
        """Allows deletion of rows and attributes (Makes a row an empty string) by using
        del statement"""
        s = cleanup_name(attr)
        try:
            self[self["__psvcolumnstracker__"][attr]] = ""
        except KeyError:
            if attr in self.__delwhitelist__:
                super(Row, self).__delattr__(attr)
            else:
                keys = self["__psvcolumnstracker__"].keys()
                if s in keys:
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

                    if attr in dir(self):
                        raise AttributeError(
                            msg.attribute_readonly.format(classname=self.__class__, attr=attr))
                    else:
                        raise AttributeError(msg.attribute_missing.format(
                        type(self), attr))

    def add_valid_attribute(self, attr, deletable=False):
        """Used by classes that inherit to add attributes to the whitelists
            Note: Row should only be inherited if no other option is available.
            These attributes being accessed will be notably slower due to the implementation.
            Memory Usage may also be much higher, as the whitelists will no longer be a 
             static variable.
        """
        if self.__class__ is Row:
            raise TypeError(msg.inherited_rows)
        super(Row, self).__setattr__(
            "__sawhitelist__", set(self.__sawhitelist__ | set((attr,))))
        if deletable:
            super(Row, self).__setattr__(
                "__delwhitelist__", set(self.__delwhitelist__ | set((attr,))))


    def construct(self, *args, **kwargs):
        """This method can be used by inherited objects of :class:`Row` as if it was __init__
           Note: Row should only be inherited if no other option is available. It cause
            memory bloat issues and can be notably slower.

        """
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

    def _set_outputrow(self, v):
        """Fast Internal way to set output flags
           Doesn't check for bad input, meant for internal use only
           Much faster than the setter
        """
        super(Row, self).__setattr__("__output__", v)

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
            if self["__psvcolumnstracker__"].get(column):
                return getattr(self, column)
        if not accept_small_names:
            raise ValueError("'{}'".format(column))
        else:
            raise ValueError("'{}'. Make sure the shorterned columns name have no collisions".format(column))

    def setcolumn(self, column, value, accept_small_names=True):
        """Set a cell by the orginal column name

            :param column: The column name. Can be both long and short form.
            :param value: The data to be set to the specified column
            :type column: :class:`str`

        """
        if column in self.keys():
            self[column] = value
            return
        elif accept_small_names:
            if self["__psvcolumnstracker__"].get(column):
                self.__setattr__(column, value)
                return
        if not accept_small_names:
            raise ValueError("'{}'".format(column))
        else:
            raise ValueError("'{}'. Make sure the shorterned columns name have no collisions".format(column))

    def delcolumn(self, column, accept_small_names=True):
        """Delete a cell by the orginal column name

        :param column: The column name. Can be both long and short form.
        :type column: :class:`str`

        """
        if column in self.keys():
            self[column] = ""
            return
        elif accept_small_names:
            if self["__psvcolumnstracker__"].get(column):
                self.__delattr__(column)
                return
        if not accept_small_names:
            raise ValueError("'{}'".format(column))
        else:
            raise ValueError("'{}'. Make sure the shorterned columns name have no collisions".format(column))

    def _addcolumns(self, columnname, columndata=""):
        """Adds a column for this row only doesn't add to column tracker

        Warning: Internal Method, API/Behavior may change without notice"""
        self[columnname] = columndata

    def _addcolumns_func(self, columnname, columnfunc):
        self[columnname] = columnfunc(self)


    def _delcolumns(self, columnname, columndata=""):
        """Adds a column for this row only
            doesn't add to column tracker

        Warning: Internal Method, API/Behavior may change without notice"""

        del self[columnname]

    def _rename_columns(self, old_columnname, new_columnname):

        self[new_columnname] = self[old_columnname]
        del self[old_columnname]

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

    def update_values(self, *arg, **kwargs):
        """Safe way to use a .update() like method on rows, checks header columns

        """
        keys = set(self.keys())
        if arg:
            for x in arg:
                xkeys = set(x.keys())
                if xkeys.issubset(keys):
                    self.update(x)
                else:
                    raise ValueError(
                        "'{}' contains columns not in this row currently"
                        .format(x)
                        )
        if kwargs:
            kwkeys = set(kwargs.keys())
            if kwkeys.issubset(keys):
                self.update(kwargs)
            else:
                raise ValueError(
                    "'{}' contains columns not in this row currently"
                    .format(kwargs)
                    )


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

class RowDefaults(object):
    """Contains Static Variables the Row uses
        to prevent rampant memory waste.
    """
    __delwhitelist__ = set()
    __sawhitelist__ = {"__output__", "outputrow"}
    
    # This is inlined in most of the library due to speed constraints.
    __psvcolumns__ = '__psvcolumnstracker__'

# For backwards compability, will be removed in the future
# Refering Row as BaseRow is considered Depreciated
BaseRow = Row

    
#This block was in utils, 
# but it relied on a circular reference that re-imported
# a variable everytime this core function was called.
#While less clean, this produces a decent speedup.
banned_columns = {RowDefaults.__psvcolumns__,}
non_accepted_key_names = set(tuple(dir(
    Row)) + ("row_obj", RowDefaults.__psvcolumns__, 
    RowDefaults.__psvcolumns__) + tuple(keyword.kwlist))
bad_first_char = set(digits)

@lru_cache(1024)
def cleanup_name(s):
    result = "".join(filter(lambda x: x in accepted_chars, s.lower()))
    if not result:
        raise ValueError(msg.non_valid.format(s))
    if result in non_accepted_key_names or result[0] in bad_first_char:
        result = "psv_" + result
    return result
