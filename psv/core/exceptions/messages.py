
class RowObjectMsg:

    outputrowmsg = "output must be {}, not {}"
    flagmessage = "Missing Flag"
    attribute_readonly = "'{classname}' object attribute '{attr}' is read-only. Note: '{attr}' is likely method/class attribute and not part of this row's data"
    attribute_missing = "'{}' has no attribute '{}'"
    inherited_rows = "Only inherited Objects can use add_valid_attribute"
    non_valid = "'{}' cannot be shorten to a python valid attribute, and therefore is an invalid column name"

class ApiObjectMsg:

    singlefindmsg = "Function returned more than 1 result"
    getitemmsg = "Row indices must be int, slices, str, tuple, or functions. Not {}"
    outputmsg = "A ordered list of columns must be supplied to output the file"
    badgrab = "Empty Grab. Lack of arguments were supplied to grab method."
    badcls = "cls argument must be {} or subclass of it. Was {}"
    badfastfind = "Multiple Keywords are not supported for fast_find()"

class LoadingMsg:

    forbidden_column = "'{}' is a forbidden column name, due to it being reserved by psv internally"