from .core.output import outputfile
from .core.objects import BaseRow
from .core.parsing import parser, xlsxparser

class FatStax(object):
	"""This class centralizes the parsing, output, and objects
	functionality of this script"""

	def __init__(self, mastercsv, cls=BaseRow, parsing=parser):
		#Since I close the file after this, the row must be fully placed into memory
		self.rows = list(parser(mastercsv, cls))


	def output(self, loc=None, columns=None):
		if not columns:
			raise Exception("master_columns must be supplied to output MASTER")
		outputfile(loc, self.rows, columns)
