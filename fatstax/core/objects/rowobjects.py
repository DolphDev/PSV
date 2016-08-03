from .utils import multireplace


class BaseRow(dict):
    """This Base Class represents a row in a spreadsheet"""

    def __init__(self, data, *args, **kwargs):
        super(BaseRow, self).__init__(data)
        self.construct(*args, **kwargs)
        self.__output__ = True

    def construct(self, *args, **kwargs):
        pass

    @property
    def outputrow(self):
        return self.__output__

    @outputrow.setter
    def outputrow(self, v):
        if not isinstance(v, bool):
            raise TypeError("output must be {}, not {}".format(bool, type(v)))
        self.__output__ = v

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

    def __delattr__(self, attr):
        """Allows deletion of rows and attributes (Makes a row empty) by using
        del statement"""
        try:
            if attr in super(BaseRow, self).keys():
                self[attr]["value"] = ""
            else:
                super(BaseRow, self).__delattr__(attr)

        except (KeyError, AttributeError):
            super(BaseRow, self).__delattr__(attr)


    def addcolumn(self, columnname, columndata=""):
        self[multireplace(columnname.lower(), " ", "(", ")", "/", "\\")] = {"org_name":columnname, "value":columndata}
        
    @property
    def longcolumn(self):
        """Generates a Dict that uses orginal names of 
        the column, used for output"""
        newdict = {}
        for k in self.keys():
            newdict.update({self[k]["org_name"]: self[k]["value"]})
        return newdict

