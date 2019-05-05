from .core.objects.apiobjects import MainSelection
from .core.objects import Row, banned_columns
from .core.exceptions.messages import LoadingMsg as msg
from .load_utils import _new, _loads, _safe_load, csv
from .load_utils import (csv_size_limit, column_names, column_names_str,
                        _column_names_io, figure_out_columns, forbidden_columns)

import io
import glob
import itertools






def load(f, cls=Row, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=False,
         csv_size_max=None, csv_max_row=None, custom_columns=None, close_file=False):
    """Loads a file into psv

        :param cls: The class that will be used for csv data.
        :type cls: :class:`BaseRow` (or class that inherits it)

        Note: Due to way python's internal csv library works,
            identical headers will overwrite and only the last header will available.


    """
    if csv_size_max:
        csv_size_limit(csv_size_max)

    if isinstance(f, io._io._IOBase) and not close_file:
        csvfile = f
        if csv_max_row:
            data = itertools.islice(csv.DictReader(
                csvfile, delimiter=delimiter, quotechar=quotechar), csv_max_row)
        else:
            data = csv.DictReader(
                csvfile, delimiter=delimiter, quotechar=quotechar)
        result = MainSelection(data, columns=_column_names_io(csvfile, cls, quotechar, delimiter,
                                                       mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns),
                             cls=cls, typetransfer=typetransfer, custom_columns=bool(custom_columns))      
    else:                            
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as csvfile:
            if csv_max_row:
                data = itertools.islice(csv.DictReader(
                    csvfile, delimiter=delimiter, quotechar=quotechar), csv_max_row)
            else:
                data = csv.DictReader(
                    csvfile, delimiter=delimiter, quotechar=quotechar)
            result = MainSelection(data, columns=_column_names_io(csvfile, cls, quotechar, delimiter,
                                                           mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns),
                                 cls=cls, typetransfer=typetransfer, custom_columns=bool(custom_columns))

    return result


def loaddir(f, cls=Row, delimiter=",", quotechar='"', mode='r', buffering=-1,
            encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=False,
            csv_size_max=None, filetype="*.csv"):
    """Loads a directory of .csv files

        Note: Due to way python's internal csv library works,
            identical headers will overwrite and only the last header will available.
    """
    # TODO: Modernize this function
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
    return _loads(csvdoc, columns=columns, cls=cls, delimiter=delimiter, quotechar=quotechar,
          typetransfer=typetransfer, csv_size_max=csv_size_max, newline=newline)

def safe_load(f, cls=Row, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=False,
         csv_size_max=None, csv_max_row=None, custom_columns=None, close_file=False):
    
    """This safetly reads more dirty datasets. It can handle: Duplicate, missing, and unsupported headers.
    """

    if csv_size_max:
        csv_size_limit(csv_size_max)

    if isinstance(f, io._io._IOBase) and not close_file:
        csvfile = csv.reader(f, delimiter=',', quotechar=quotechar)
        columns = _column_names_io(f, cls, quotechar, delimiter,
            mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns, check_columns=False)
        if csv_max_row:
            # +1 to keep identical behavior as .load()
            data = _safe_load(itertools.islice(csvfile, csv_max_row+1), columns, cls, custom_columns)
        else:
            data = _safe_load(csvfile, columns, cls, custom_columns)
        result = data  
    else:                            
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as raw_csvfile:
            columns = _column_names_io(raw_csvfile, cls, quotechar, delimiter,
                mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns, check_columns=False)
            csvfile = csv.reader(raw_csvfile, delimiter=delimiter, quotechar=quotechar)

            if csv_max_row:
                data = _safe_load(itertools.islice(csvfile, csv_max_row+1), columns, cls, custom_columns)

            else:
                data = _safe_load(csvfile, columns, cls, custom_columns)

            result = data

    return result

def opencsv(f, cls=Row, delimiter=",", quotechar='"', mode='r', buffering=-1,
         encoding="utf-8", errors=None, newline=None, closefd=True, opener=None, typetransfer=False,
         csv_size_max=None, csv_max_row=None, custom_columns=None, close_file=False):

    if csv_size_max:
        csv_size_limit(csv_size_max)

    if isinstance(f, io._io._IOBase) and not close_file:
        #csvfile = csv.reader(f, delimiter=',', quotechar=quotechar)
        columns = _column_names_io(f, cls, quotechar, delimiter,
            mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns)
        if columns == figure_out_columns(columns):
            return load(f, cls=cls, delimiter=delimiter, quotechar=quotechar, mode=mode, buffering=buffering, encoding=encoding,
                errors=errors, newline=newline, closefd=closefd, opener=opener, typetransfer=typetransfer, csv_size_max=csv_size_max,
                csv_max_row=csv_max_row, custom_columns=custom_columns, close_file=close_file)

        else:
            return safe_load(f, cls=cls, delimiter=delimiter, quotechar=quotechar, mode=mode, buffering=buffering, encoding=encoding,
                errors=errors, newline=newline, closefd=closefd, opener=opener, typetransfer=typetransfer, csv_size_max=csv_size_max,
                csv_max_row=csv_max_row, custom_columns=custom_columns, close_file=close_file)
        
    else:                            
        with f if isinstance(f, io._io._IOBase) else open(f, mode=mode, buffering=buffering,
                                                          encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener) as raw_csvfile:
            columns = _column_names_io(raw_csvfile, cls, quotechar, delimiter,
                mode, buffering, encoding, errors, newline, closefd, opener, custom_columns=custom_columns)

            if columns == figure_out_columns(columns):
                return load(f, cls=cls, delimiter=delimiter, quotechar=quotechar, mode=mode, buffering=buffering, encoding=encoding,
                    errors=errors, newline=newline, closefd=closefd, opener=opener, typetransfer=typetransfer, csv_size_max=csv_size_max,
                    csv_max_row=csv_max_row, custom_columns=custom_columns, close_file=False)

            else:
                return safe_load(f, cls=cls, delimiter=delimiter, quotechar=quotechar, mode=mode, buffering=buffering, encoding=encoding,
                    errors=errors, newline=newline, closefd=closefd, opener=opener, typetransfer=typetransfer, csv_size_max=csv_size_max,
                    csv_max_row=csv_max_row, custom_columns=custom_columns, close_file=False)
            

def new(columns=None, cls=Row,
        csv_size_max=None):
    if csv_size_max:
        csv_size_limit(csv_size_max)
    return _new(columns=columns, cls=cls)




