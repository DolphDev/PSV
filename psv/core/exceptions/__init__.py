from . import messages


class PSV_BASE_EXCEPTION(Exception):
    pass


class RowError(PSV_BASE_EXCEPTION):
    pass


class FlagError(RowError):
    pass


class SelectionError(PSV_BASE_EXCEPTION):
    pass


class ApiError(SelectionError):
    pass
