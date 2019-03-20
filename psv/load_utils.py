from .core.objects import Row, banned_columns
from .core.objects.apiobjects import MainSelection
from .core.exceptions.messages import LoadingMsg as msg

import io
import csv

def csv_size_limit(size):
    """Changes the csv field size limit.
        :param size: The size limit of the csv data. 
        :type size: :class:`type`
    """
    csv.field_size_limit(size)

def forbidden_columns(columns):
    for x in columns:
        if x in banned_columns:
            raise ValueError(
                msg.forbidden_column.format(x))



def _loads(csvdoc, columns=None, cls=Row, delimiter=",", quotechar='"',
          typetransfer=False, csv_size_max=None, newline="\n"):
    """Loads csv, but as a python string

        Note: Due to way python's internal csv library works, identical headers will overwrite each other.
    """
    if csv_size_max:
        csv_size_limit(csv_size_max)
    if isinstance(csvdoc, str):
        csvfile = io.StringIO()
        csvfile.write(csvdoc)
        data = csv.DictReader(csvdoc.split(newline),
                              delimiter=delimiter, quotechar=quotechar)
        if not columns:
            columns = tuple(next(csv.reader(csvdoc.split(
                newline), delimiter=delimiter, quotechar=quotechar)))
    else:
        data = csvdoc
    if columns:
        forbidden_columns(columns)
    elif (not columns) and isinstance(csvdoc, tuple):
        forbidden_columns(csvdoc[0].keys())
    api = MainSelection(data, columns=(
        columns),  cls=cls, typetransfer=typetransfer)
    return api



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

def _add_row(finalcolumns, row):
    # Attempt to force the gc
    result.addrow(**dict(zip(finalcolumns, row)))

def convert_to_psv(finalcolumns, csvfile):
    for row in csvfile:
        yield dict(zip(finalcolumns, row))


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


    dataset = tuple(convert_to_psv(finalcolumns, csvfile))
    return _loads(dataset, finalcolumns)
