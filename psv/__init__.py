from .core.objects.apiobjects import Api
from .core.objects import BaseRow


import csv
import io
import glob


def csv_size_limit(size):
    csv.field_size_limit(size)

def load(f, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetranfer=True, 
         csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max)

    with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
        encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        data = csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar)
        api = Api(data, columns=column_names(csvfile.name, cls, quotechar, delimiter,
            mode, buffering, encoding, errors, newline, closefd, opener), 
            outputfiled=outputfile, cls=cls, typetranfer=typetranfer)
    return api

def loaddir(f, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetranfer=True, 
         csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max)
    data = []
    columns = None
    for files in glob.glob(f+"*.csv"):
        if not columns:
            columns = column_names(files)
        with open(files, mode=mode, buffering=buffering,
            encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            data = data + list(csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar))
    return Api(data, columns=columns ,outputfiled=outputfile, cls=cls, typetranfer=typetranfer)

def loads(csvdoc, columns=None, cls=BaseRow, outputfile=None, delimiter=",", quotechar='"', 
          typetranfer=True, csv_size_max=None, newline="\n"):
    if csv_size_max:
        csv_size_limit(csv_size_max)  
    if isinstance(csvdoc, str):
        data = csv.DictReader(csvdoc.split(newline), delimiter=delimiter, quotechar=quotechar)
        if not columns:
            columns = tuple(next(csv.reader(csvdoc.split(newline), delimiter=delimiter, quotechar=quotechar)))
    else:
        data = csvdoc
    api = Api(data, columns=(columns), outputfiled=outputfile, cls=cls, typetranfer=typetranfer)
    return api

def new(cls=BaseRow, columns=None, outputfile=None,
        csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max) 
    return Api(columns=columns, outputfiled=outputfile, cls=cls)

def column_names(f, cls=BaseRow, quotechar='"', delimiter=",", mode='r', buffering=-1, encoding="utf-8",
                errors=None, newline=None, closefd=True, opener=None,
                csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max) 
    with open(f, mode=mode, buffering=buffering,
        encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
        columns = next(csv.reader(csvfile, delimiter=',', quotechar=quotechar))
    return tuple(columns)


