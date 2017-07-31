
class RowObjectMsg:

    getformulamsg = "'{}' cell is not a formula."
    outputrowmsg = "output must be {}, not {}"
    flagmessage = "Missing Flag"
    attribute_readonly = "'{classname}' object attribute '{attr}' is read-only. Note: '{attr}' is likely method/class attribute and not part of this row's data"
    attribute_missing = "'{}' has no attribute '{}'"
    inherited_rows = "Only inherited Rows can use add_valid_attribute"

class ApiObjectMsg:

    singlefindmsg = "Function returned more than 1 result"
    getitemmsg = "Row indices must be int, slices, str, tuple, or functions. Not {}"
    outputmsg = "A ordered list of columns must be supplied to output the file"
    badgrab = "Empty Grab. Lack of arguments were supplied to grab method."

