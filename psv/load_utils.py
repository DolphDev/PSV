from .core.objects import Row, banned_columns
from .core.objects.apiobjects import MainSelection
def forbidden_columns(columns):
    for x in columns:
        if x in banned_columns:
            raise ValueError(
                msg.forbidden_column.format(x))


def _new(columns=None, cls=Row, custom_columns=False):
    # Empty Main Selection
    if isinstance(columns, str):
        columns = [columns]
    if columns:
        forbidden_columns(columns)
    if not columns:
        columns = tuple()
    if not isinstance(columns, tuple):
        columns = tuple(columns)
    return MainSelection(columns=columns, cls=cls, custom_columns=custom_columns)

def _safe_load(csvfile, columns, cls, custom_columns):
    # Implements a much slower DictWriter
    import gc
    # This function kills the gc, have to do it pretty
    # much manually due to the gc not firing

    try:
        raw_columns = next(csvfile)
    except StopIteration:
        # This is an Empty File, just use _new
        # pass in columns in case of columns being provided
        return _new(columns=columns)

    # This must be the same len as raw_columns
    finalcolumns = []

    # We don't need to completely clean this up, just prevent unusable columns.
    # PSV will automatically handle collisions
    # We need to keep these as close as possible to the original
    # For custom_columns
    empty_counter = 0
    for x in (x.strip() for x in columns):
        result = x
        if result in banned_columns:
            result = "psv_banned_columns_{}".format(x)
        if not result:
            result = "psv_empty_column_{}".format(empty_counter)
            empty_counter += 1
        finalcolumns.append(result)



    # We are eating our own dog food with this implementation
    # Uses PSV to build out the result
    # This is much slower and should only be used for dirty datasets

    result = _new(columns=finalcolumns, custom_columns=custom_columns)

    x = 0
    for row in csvfile:
        result.addrow(**dict(zip(finalcolumns, row)))
        if x == 50:
            # Does Python not fire gc in loops?
            # TODO: See if there is a more pratical way
            # Prevent memory bloat
            gc.collect()
            x = 0
        else: x += 1

    return result
