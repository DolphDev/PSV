import csv
import io
from types import FunctionType


def outputfile(f, rows, columnnames, quote_all=True, encoding="utf-8"):
    if not (isinstance(columnnames, list) or isinstance(columnnames, tuple)):
        raise ValueError(
            "Provided Columns must be a list was {}".format(type(columnnames)))
    with f if isinstance(f, io._io._IOBase) else open(f, 'w', encoding=encoding, newline='') as csvfile:
        fieldnames = columnnames
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL if quote_all else 0)
        writer.writeheader()
        for x in rows:
            if x.outputrow:
                writer.writerow(x.longcolumn(columnnames))


def outputstr(rows, columnnames, quote_all, encoding="utf-8"):
    if not (isinstance(columnnames, list) or isinstance(columnnames, tuple)):
        raise ValueError(
            "Provided Columns must be a list was {}".format(type(columnnames)))
    with io.StringIO() as csvfile:
        fieldnames = columnnames
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL if quote_all else 0)
        writer.writeheader()
        for x in rows:
            if x.outputrow:
                writer.writerow(x.longcolumn(columnnames))
        return csvfile.getvalue()
