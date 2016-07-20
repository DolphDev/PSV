from . import parsing
from .objects import MasterRow, UpdateRow, ScrappedDataRow
from .output import outputfile
from .utils import (sku_update, productimageurl, description,
					update_master_description, scrappeddata_property)


class FatStax(object):
	"""This class centralizes the parsing, output, and objects
	functionality of this script"""

	def __init__(self, mastercsv, updatecsv, scrappeddata):
		#Since I close the file after this, the row must be looped over
		self.masterrow = list(parsing.parser(mastercsv, MasterRow))
		self.updaterow = list(parsing.parser(updatecsv, UpdateRow))
		self.scrappeddata = list(parsing.xlsxparser(scrappeddata, ScrappedDataRow))

	def output(self, master=None, update=None, master_columns=None, update_columns=None):
		if master:
			if not master_columns:
				raise Exception("master_columns must be supplied to output MASTER")
			outputfile(master, self.masterrow, master_columns)
		if update:
			if not update_columns:
				raise Exception("update_columns must be supplied to output UPDATE")
			outputfile(update, self.updaterow, update_columns)

