from .core.objects import Row, banned_columns
from .core.objects.apiobjects import MainSelection



def _new(columns=None, cls=Row):
    # Empty Main Selection
    if isinstance(columns, str):
        columns = [columns]
    if columns:
        forbidden_columns(columns)
    if not columns:
        columns = tuple()
    if not isinstance(columns, tuple):
        columns = tuple(columns)
    return MainSelection(columns=columns, cls=cls)

def _safe_load(csvfile, columns, cls):
    # Implements a much slower DictWriter
    try:
        columns = next(csvfile)
    except StopIteration:
        # This is an Empty File, just use _new
        # pass in columns in case of columns being provided
        return _new(columns=columns)

    # This must be the same len
    cleaned_up_columns = [x.strip() for x in columns]
    finalcolumns = []
    # We don't need to completely clean this up, just prevent unusable columns
    empty_counter = 0
    for x in cleaned_up_columns:
        result = x
        if result in banned_columns:
            result = "psv_banned_columns_{}".format(x)
        if not result:
            result = "psv_empty_column_{}".format(empty_counter)
            empty_counter += 1
        final.append(result)



    # We are eating our own dog food with this method
    # Uses PSV to build out the result
    # This is much slower and only used for dirty datasets

    result = _new(columns=finalcolumns)

    for row in csvfile:
        result.addrow(**dict(zip(finalcolumns, row)))

    return result
