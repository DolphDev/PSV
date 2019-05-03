from .core.objects import Row, banned_columns
from .core.objects.apiobjects import MainSelection
from .core.exceptions.messages import LoadingMsg as msg

import io
import csv

def fill_empty(n, lst):
    x = len(lst)
    for _ in lst:
        yield _
    yield from ("" for b in range(n - x))

def csv_size_limit(size):
    """Changes the csv field size limit.
        :param size: The size limit of the csv data. 
        :type size: :class:`type`
    """
    csv.field_size_limit(size)

def forbidden_columns(columns, msg=msg):
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
        csvfile = io.StringIO(csvdoc)
        data = csv.DictReader(csvfile,
                              delimiter=delimiter, quotechar=quotechar)
        if not columns:
            columns = column_names_str(csvdoc, delimiter=delimiter, quotechar=quotechar)
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

def convert_to_psv(finalcolumns, csvfile):
    lenfinal_column = len(finalcolumns)
    for row in csvfile:
        yield dict(zip(finalcolumns, fill_empty(lenfinal_column, row)))

def figure_out_columns(columns):
    finalcolumns = []

    # We don't need to completely clean this up, just prevent unusable columns.
    # PSV will automatically handle collisions
    # We need to keep these as close as possible to the original
    empty_counter = 0
    for x in (x.strip() for x in columns):
        result = x
        if result in banned_columns:
            result = "psv_banned_columns_{}".format(x)
        if not result:
            result = "psv_empty_column_{}".format(empty_counter)
            empty_counter += 1
        finalcolumns.append(result)
    return finalcolumns

def _safe_load(csvfile, columns, cls, custom_columns):
    # Implements a much slower DictWriter
    # This function kills the gc, have to do it pretty
    # much manually due to the gc not firing

    try:
        raw_columns = next(csvfile)
    except StopIteration:
        # This is an Empty File, just use _new
        # pass in columns in case of columns being provided
        return _new(columns=columns)


    finalcolumns = figure_out_columns(columns)
    dataset = tuple(convert_to_psv(finalcolumns, csvfile))
    return _loads(dataset, finalcolumns)

def column_names(f, cls=Row, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8",
                 errors=None, newline=None, closefd=True, opener=None,
                 csv_size_max=None, check_columns=True, custom_columns=None):
    """loads file"""
    if custom_columns:
        if check_columns:
            forbidden_columns(custom_columns)
        return custom_columns
    if csv_size_max:
        csv_size_limit(csv_size_max)
    with open(f, mode=mode, buffering=buffering,
              encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        try:
            columns = next(csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar))
        except StopIteration:
            columns = []
    if check_columns:
        forbidden_columns(columns)
    return tuple(columns)


def _column_names_io(f, cls=Row, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8",
                 errors=None, newline=None, closefd=True, opener=None,
                 csv_size_max=None, check_columns=True, custom_columns=None):
    # INTERAL ONLY
    if custom_columns:
        if check_columns:
            forbidden_columns(custom_columns)
        return custom_columns
    if csv_size_max:
        csv_size_limit(csv_size_max)

    # IO Varient, Internal use
    csvfile = f
    csvfile.seek(0)
    try:
        columns = next(csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar))
    except StopIteration:
        columns = []
    if check_columns:
        forbidden_columns(columns)
    csvfile.seek(0)
    return tuple(columns)

def column_names_str(csvdoc, cls=Row, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8",
                 errors=None, newline=None, closefd=True, opener=None,
                 csv_size_max=None, check_columns=True, custom_columns=None):
    # String Based loading doesn't currently 
    # Support custom columns
    # TODO: Fully implement this
    # if custom_columns:
    #    if check_columns:
    #        forbidden_columns(custom_columns)
    #    return custom_columns
    if csv_size_max:
        csv_size_limit(csv_size_max)
    csvfile = io.StringIO(csvdoc)

    try:
        columns = next(csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar))
    except StopIteration:
        columns = []
    if check_columns:
        forbidden_columns(columns)
    return tuple(columns)