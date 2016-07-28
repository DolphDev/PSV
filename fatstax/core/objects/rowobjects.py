from .utils import multireplace


class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""

    def __init__(self, data, *args, **kwargs):
        super(BaseRow, self).__init__(data)
        self.construct(*args, **kwargs)

    def construct(self, *args, **kwargs):
        pass

    def getcolumn(self, v):
        "Get column by the orginal column name"
        return self.longcolumn[v]

    def setcolumn(self, a, v):
        s = multireplace(a.lower(), " ", "(", ")", "/", "\\")
        if s in self.keys():
            self.__setattr__(s, v)
        else:
            raise Exception("Key not valid")


    def __getattribute__(self, attr):
        if attr in super(BaseRow, self).keys():
            return (self[attr]["value"])
        else:
            return super(dict, self).__getattribute__(attr)

    def __setattr__(self, attr, v):
        """Allows setting new data to row
        is called if row does not have specially 
        defined set behavior"""
        try:
            if attr in super(BaseRow, self).keys():
                self[attr]["value"] = v
            else:
                super(BaseRow, self).__setattr__(attr, v)

        except (KeyError, AttributeError):
            super(BaseRow, self).__setattr__(attr, v)


    @property
    def longcolumn(self):
        """Generates a Dict that uses orginal names of 
        the column, used for output"""
        newdict = {}
        for k in self.keys():
            newdict.update({self[k]["org_name"]: self[k]["value"]})
        return newdict

