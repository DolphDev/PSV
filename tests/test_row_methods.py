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
                self.assertTrue((x) == (x))
        except Exception as err:
            self.fail(err)

    def test_n_eq_non_row(self):
        self.construct()
        try:
            for x in self.csvdoc:
                (x) == None
        except Exception as err:
            self.fail(err)

    def test_n_eq_row(self):
        self.construct()
        self.csvdoc.addrow()
        self.assertFalse(self.csvdoc[0] == self.csvdoc[-1])

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
            self.fail("Attribute Error Failed to trigger: No attribute")
        except AttributeError:
            pass

        try:
            self.csvdoc[0].Name
            self.fail("Attribute Error Failed to trigger: Bad row ref")
        except AttributeError:
            pass

    def test__setattr__(self):
        self.construct()
        try: 
            self.csvdoc[0].name1 = 1
            self.fail("Attribute Error Failed to trigger")
        except AttributeError:
            pass
        try:
            self.csvdoc[0].Name = 1
            self.fail("Attribute Error Failed to trigger: Bad row ref")
        except AttributeError:
            pass

        try:
            self.csvdoc[0].keys = 1
            self.fail("Attribute Error Failed to trigger: read only")
        except AttributeError:
            pass

    def test__delattr__(self):
        self.construct()
        try: 
            del self.csvdoc[0].name1
            self.fail("Attribute Error Failed to trigger")
        except AttributeError:
            pass

        try:
            del self.csvdoc[0].Name
            self.fail("Attribute Error Failed to trigger: Bad row ref")
        except AttributeError:
            pass

        try:
            del self.csvdoc[0].keys
            self.fail("Attribute Error Failed to trigger: read only")
        except AttributeError:
            pass


    def test_tabulate(self):
        self.construct()
        try: 
            for x in self.csvdoc:
                x.tabulate()
                x.tabulate(only_ascii=False)

        except Exception as err:
            self.fail(err)

    def test_add_valid_attribute(self):
        class TestRow(psv.core.objects.rowobjects.BaseRow):
            def construct(self, *args, **kwargs):
                self.add_valid_attribute("Test1")
                self.add_valid_attribute("Test2", True)

        row = TestRow({"data":{"org_row":"DATA", "value":""}})
        row.add_valid_attribute("Test3")
        row.add_valid_attribute("Test4", True)

    def test_add_valid_attribute_fail(self):
        with self.assertRaises(TypeError) as cm:
            psv.core.objects.rowobjects.BaseRow({"data":{"org_row":"DATA", "value":""}}).add_valid_attribute("name")


    def test_outputrow_catches_non_bool(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc[0].outputrow("TEST")

    def test_setcolumn_keyerror(self):
        self.construct()
        import random
        import string
        column = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        with self.assertRaises(KeyError) as cm:
            for x in self.csvdoc:
                x.setcolumn(column, "test")
            
    def test_delcolumn_keyerror(self):
        self.construct()
        import random
        import string

        column = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        with self.assertRaises(KeyError) as cm:
            for x in self.csvdoc:
                x.delcolumn(column)

    def test_getcolumn_keyerror(self):
        self.construct()
        import random
        import string
        column = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        with self.assertRaises(KeyError) as cm:
            for x in self.csvdoc:
                x.getcolumn(column)

    def test_outputrow_typerror(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc[0].outputrow("THIS SHOULD ERROR OUT")

    def test__str__(self):
        self.construct()
        try:
            for x in self.csvdoc:
                str(x)
        except Exception as err:
            self.fail(err)


    def test__addcolumn(self):
        self.construct()
        for x in self.csvdoc:
            x.addcolumn("TEST")
            x.addcolumn("TEST2", "DATA")