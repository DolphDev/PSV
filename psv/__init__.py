from .core.objects.apiobjects import MainSelection
from .core.objects import BaseRow, banned_columns
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


def load(f, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=True,
         csv_size_max=None, csv_max_row=None):
    """Loads a file into psv

        :param cls: The class that will be used for csv data.
        :type cls: :class:`BaseRow` (or class that inherits it)

    """
    if csv_size_max:
        csv_size_limit(csv_size_max)

    if not csv_max_row:
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = csv.DictReader(
                csvfile, delimiter=delimiter, quotechar=quotechar)
            api = MainSelection(data, columns=column_names(csvfile.name, cls, quotechar, delimiter,
                                                           mode, buffering, encoding, errors, newline, closefd, opener),
                                outputfiled=outputfile, cls=cls, typetransfer=typetransfer)
    else:
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = itertools.islice(csv.DictReader(
                csvfile, delimiter=delimiter, quotechar=quotechar), csv_max_row)
            api = MainSelection(data, columns=column_names(csvfile.name, cls, quotechar, delimiter,
                                                           mode, buffering, encoding, errors, newline, closefd, opener),
                                outputfiled=outputfile, cls=cls, typetransfer=typetransfer)
    return api


def loaddir(f, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"', mode='r', buffering=-1,
            encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=True,
            csv_size_max=None):
    """Loads a directory of .csv files"""
    if csv_size_max:
        csv_size_limit(csv_size_max)
    data = []
    columns = None
    for files in glob.glob(f+"*.csv"):
        if not columns:
            columns = column_names(files)
        with open(files, mode=mode, buffering=buffering,
                  encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = data + list(csv.DictReader(csvfile,
                                              delimiter=delimiter, quotechar=quotechar))
    forbidden_columns(columns)
    return MainSelection(data, columns=columns, outputfiled=outputfile, cls=cls, typetransfer=typetransfer)


def loads(csvdoc, columns=None, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"',
          typetransfer=True, csv_size_max=None, newline="\n"):
    was_str = False
    if csv_size_max:
        csv_size_limit(csv_size_max)
    if isinstance(csvdoc, str):
        was_str = True
        data = csv.DictReader(csvdoc.split(newline),
                              delimiter=delimiter, quotechar=quotechar)
        if not columns:
            columns = tuple(next(csv.reader(csvdoc.split(
                newline), delimiter=delimiter, quotechar=quotechar)))
    else:
        data = csvdoc
    if columns:
        forbidden_columns(columns)
    elif (not columns) and isinstance(csvdoc, dict):
        forbidden_columns(csvdoc.keys())
    api = MainSelection(data, columns=(
        columns), outputfiled=outputfile, cls=cls, typetransfer=typetransfer)
    return api


def new(cls=BaseRow, columns=None, outputfile=None,
        csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max)
    if columns:
        forbidden_columns(columns)
    return MainSelection(columns=columns, outputfiled=outputfile, cls=cls)


def column_names(f, cls=BaseRow, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8",
                 errors=None, newline=None, closefd=True, opener=None,
                 csv_size_max=None, check_columns=True):
    if csv_size_max:
        csv_size_limit(csv_size_max)
    with open(f, mode=mode, buffering=buffering,
              encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        columns = next(csv.reader(csvfile, delimiter=',', quotechar=quotechar))
    if check_columns:
        forbidden_columns(columns)
    return tuple(columns)

def forbidden_columns(columns):
    for x in columns:
        if x in banned_columns:
            raise ValueError(msg.forbidden_column(x))
