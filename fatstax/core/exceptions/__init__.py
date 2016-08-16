from . import messages

class BCSV_BASE_EXCEPTION(Exception):
    pass

class RowError(BCSV_BASE_EXCEPTION):
    pass

class DeletedRow(RowError):
    pass
