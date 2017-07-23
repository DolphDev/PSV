import psv
import unittest

csv = """Name,Price,Available,Company
Product 1,10,1,Yahoo
Product 2,15,0,Microsoft
Product 3,1,1,Google
Product 4,20,0,Yahoo
Product 5,25,1,Yahoo
Product 6,30,1,Google
Product 7,10,0,Yahoo
"""

csv_repeat = """Name,Price,Available,Company
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
"""



class psv_selections_test(unittest.TestCase):

    def construct(self):
        self.csvdoc = psv.loads(csv)
        self.csv_repeat = psv.loads(csv_repeat)

    def test_hash(self):
        self.construct()
        try:
            for x in self.csvdoc:
                hash(x)
        except Exception as err:
            self.fail(err)

    def test_hash_value(self):
        self.construct()
        try:
            for x in self.csvdoc:
                (x).__hashvalue__()
        except Exception as err:
            self.fail(err)

    def test_eq(self):
        self.construct()
        try:
            for x in self.csvdoc:
                (x) == (x)
        except Exception as err:
            self.fail(err)

    def test_hash_value(self):
        self.construct()
        try:
            for x in self.csvdoc:
                (x).__hashvalue__()
        except Exception as err:
            self.fail(err)

    def test__getattr__(self):
        self.construct()
        try: 
            self.csvdoc[0].name1
            self.fail("Attribute Error Failed to trigger")
        except AttributeError:
            pass

    def test__setattr__(self):
        self.construct()
        try: 
            self.csvdoc[0].name1 = 1
            self.fail("Attribute Error Failed to trigger")
        except AttributeError:
            pass

    def test__delattr__(self):
        self.construct()
        try: 
            del self.csvdoc[0].name1
            self.fail("Attribute Error Failed to trigger")
        except AttributeError:
            pass

    def test_tabulate(self):
        self.construct()
        try: 
            self.csvdoc.tabulate()
        except Exception as err:
            self.fail(err)