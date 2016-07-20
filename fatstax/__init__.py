from .core.output import outputfile
from .core.objects import BaseRow
from .core.parsing import parser, excelparser, parser_addrow


class FatStax(object):
    """This class centralizes the parsing, output, and objects
    functionality of this script"""

    def __init__(self, mastercsv, cls=BaseRow, parsing=parser):
        #Since I close the file after this, the row must be placed into memory
        self.rows = list(parser(mastercsv, cls))

    def addrow(self, columns, cls=BaseRow):
        r = parser_addrow(columns, cls)
        self.rows.append(r)
        return r


    def output(self, loc=None, columns=None):
        if not columns:
            raise Exception("master_columns must be supplied to output file")
        outputfile(loc, self.rows, columns)
