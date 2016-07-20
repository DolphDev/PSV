from .core.output import outputfile


class FatStax(object):
	"""This class centralizes the parsing, output, and objects
	functionality of this script"""

	def __init__(self, mastercsv):
		#Since I close the file after this, the row must be fully placed into memory
		self.rows = list(parsing.parser(mastercsv, MasterRow))


	def output(self, master=None, update=None, columns=None, update_columns=None):
		if not master_columns:
			raise Exception("master_columns must be supplied to output MASTER")
		outputfile(master, self.masterrow, master_columns)