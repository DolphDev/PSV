from .utils import multireplace

class InnerRow(object):
    "Represents the data of a objects"

class BaseRow(object):
    """This Base Class represents a row in a spreadsheet"""

    def __init__(self, data):
        self.data = data

    def __getitem__(self, v):
        "Get column by the orginal column name"
        return self.longcolumn[v]

    def __setitem__(self, a, v):
        s = multireplace(a.lower(), " ", "(", ")")
        if s in self.data.keys():
            self.__setattr__(s, v)
        

    def __getattr__(self, attr): 
        """Allows dynamic access to rows
        This allows algorathic access to rows
        in a pythonic style"""
        try:
            if attr in self.__dict__["data"]:
                return self.data[attr]["value"]
        except KeyError:
            raise AttributeError('\'{}\' has no attribute \'{}\''.format(
            type(self), attr))
        raise AttributeError('\'{}\' has no attribute \'{}\''.format(
            type(self), attr))

    def __setattr__(self, attr, v):
        """Allows setting new data to row
        is called if row does not have specially 
        defined set behavior"""
        try:
            if attr in self.__dict__["data"]:
                self.data[attr]["value"] = v
        except (KeyError, AttributeError):
            super(BaseRow, self).__setattr__(attr, v)

    def setattr(self, attr, v):
        super(BaseRow, self).__setattr__(attr, v)

    @property
    def longcolumn(self):
        """Generates a Dict that uses orginal names of 
        the column, used for output"""
        newdict = {}
        for k in self.data.keys():
            newdict.update({self.data[k]["org_name"]: self.data[k]["value"]})
        return newdict
