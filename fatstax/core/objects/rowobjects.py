
class BaseRow(object):
    """This Base Class represents a row in a csv document"""

    def __init__(self, data):
        super(BaseRow, self).__setattr__("data", data)

    def __getitem__(self, v):
        return self.longcolumn[v]


    def __getattr__(self, attr):
        """Allows dynamic access to rows
        This allows algorathic access to rows
        in a pythonic style"""
        if attr in self.data:
            return self.data[attr]["value"]
        
        raise AttributeError('\'{}\' has no attribute \'{}\''.format(
            type(self), attr))

    def __setattr__(self, attr, v):
        """Allows setting new data to row
        is called if row does not have specially 
        defined set behavior"""
        try:
            if attr in self.data:
                self.data[attr]["value"] = v
        except AttributeError:
            super(BaseRow, self).__setattr__(attr, v)

    @property
    def longcolumn(self):
        """Generates a Dict that uses orginal names of 
        the column, used for output"""
        newdict = {}
        for k in self.data.keys():
            newdict.update({self.data[k]["org_name"]: self.data[k]["value"]})
        return newdict
