from .core.objects.apiobjects import MainSelection
from .core.objects import Row, banned_columns
from .core.exceptions.messages import LoadingMsg as msg


import csv
import io
import glob
import itertools


def csv_size_limit(size):
    """Changes the csv field size limit.
        :param size: The size limit of the csv data. 
        :type size: :class:`type`
    """
    csv.field_size_limit(size)


def load(f, cls=Row, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=False,
         csv_size_max=None, csv_max_row=None, custom_columns=None):
    """Loads a file into psv

        :param cls: The class that will be used for csv data.
        :type cls: :class:`BaseRow` (or class that inherits it)

        Note: Due to way python's internal csv library works,
            identical headers will overwrite and only the last header will available.


    """
    if csv_size_max:
        csv_size_limit(csv_size_max)

    if not csv_max_row:
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = csv.DictReader(
                csvfile, delimiter=delimiter, quotechar=quotechar)
            api = MainSelection(data, columns=column_names(csvfile.name, cls, quotechar, delimiter,
                                                           mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns),
                                 cls=cls, typetransfer=typetransfer, custom_columns=bool(custom_columns))
    else:
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = itertools.islice(csv.DictReader(
                csvfile, delimiter=delimiter, quotechar=quotechar), csv_max_row)
            api = MainSelection(data, columns=column_names(csvfile.name, cls, quotechar, delimiter,
                                                           mode, buffering, encoding, errors, newline, closefd, opener,
                                                           custom_columns=custom_columns),
                                 cls=cls, typetransfer=typetransfer, custom_columns=bool(custom_columns))
    return api


def loaddir(f, cls=Row, delimiter=",", quotechar='"', mode='r', buffering=-1,
            encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=False,
            csv_size_max=None, filetype="*.csv"):
    """Loads a directory of .csv files

        Note: Due to way python's internal csv library works,
            identical headers will overwrite and only the last header will available.

    """
    if csv_size_max:
        csv_size_limit(csv_size_max)
    data = []
    columns = None
    for files in glob.glob(f+filetype):
        if not columns:
            columns = column_names(files)
        with open(files, mode=mode, buffering=buffering,
                  encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = data + list(csv.DictReader(csvfile,
                                              delimiter=delimiter, quotechar=quotechar))
    if columns != None:
        forbidden_columns(columns)
    return MainSelection(data, columns=columns,  cls=cls, typetransfer=typetransfer)


def loads(csvdoc, columns=None, cls=Row, delimiter=",", quotechar='"',
          typetransfer=False, csv_size_max=None, newline="\n"):
    """Loads csv, but as a python string

        Note: Due to way python's internal csv library works, identical headers will overwrite each other.
    """
    if csv_size_max:
        csv_size_limit(csv_size_max)
    if isinstance(csvdoc, str):
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


def new(columns=None, cls=Row,
        csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max)
    if isinstance(columns, str):
        columns = [columns]
    if columns:
        forbidden_columns(columns)
    return MainSelection(columns=columns, cls=cls)


def column_names(f, cls=Row, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8",
                 errors=None, newline=None, closefd=True, opener=None,
                 csv_size_max=None, check_columns=True, custom_columns=None):
    if custom_columns:
        if check_columns:
            forbidden_columns(custom_columns)
        return custom_columns
    if csv_size_max:
        csv_size_limit(csv_size_max)
    with open(f, mode=mode, buffering=buffering,
              encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        try:
            columns = next(csv.reader(csvfile, delimiter=',', quotechar=quotechar))
        except StopIteration:
            columns = []
    if check_columns:
        forbidden_columns(columns)
    return tuple(columns)

def forbidden_columns(columns):
    for x in columns:
        if x in banned_columns:
            raise ValueError(
                msg.forbidden_column.format(x))
