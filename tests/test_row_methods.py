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

        row = TestRow({"DATA": ""}, {"data":"DATA"})
        row.add_valid_attribute("Test3")
        row.add_valid_attribute("Test4", True)


    def test_add_valid_attribute_test_behavior(self):
        class TestRow(psv.core.objects.rowobjects.BaseRow):
            def construct(self, *args, **kwargs):
                self.add_valid_attribute("Test1")
                self.add_valid_attribute("Test2", True)

        row = TestRow({"DATA": ""}, {"data":"DATA"})
        row.add_valid_attribute("Test3")
        row.add_valid_attribute("Test4", True)

        row.Test3 = None
        with self.assertRaises(AttributeError):
            #TEST 3 was not givin delete rights
            del row.Test3
        row.Test4 = int()
        del row.Test4
        row.Test4 = str()


    def test_add_valid_attribute_fail(self):
        with self.assertRaises(TypeError) as cm:
            psv.core.objects.rowobjects.BaseRow({"DATA": ""}, {"data":"DATA"}).add_valid_attribute("name")

    def test_outputrow_catches_non_bool(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc[0].outputrow("TEST")

    def test_setcolumn_valueerror(self):
        self.construct()
        import random
        import string
        column = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        with self.assertRaises(ValueError) as cm:
            for x in self.csvdoc:
                x.setcolumn(column, "test")

    def test_setcolumn_accept_small_names(self):
        import random
        self.construct()
        for row in self.csvdoc:
            v = random.random()
            row.setcolumn("name", v)
            self.assertEqual(row.getcolumn("name"), v)
    
    def test_setcolumn_accept_small_names_valueerror(self):
        import random
        self.construct()
        for row in self.csvdoc:
            v = random.random()
            with self.assertRaises(ValueError):
                row.setcolumn("name", v, accept_small_names=False)


        
    def test_delcolumn_valueerror(self):
        self.construct()
        import random
        import string

        column = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        with self.assertRaises(ValueError) as cm:
            for x in self.csvdoc:
                x.delcolumn(column)

    def test_delcolumn_accept_small_names_valueerror(self):
        self.construct()
        for row in self.csvdoc:
            with self.assertRaises(ValueError):
                row.delcolumn("name", accept_small_names=False)

    def test_delcolumn_accept_small_names(self):
        self.construct()
        for row in self.csvdoc:
            row.delcolumn("name")
            self.assertEqual(row.getcolumn("name"), "")

    def test_getcolumn_valueerror(self):
        self.construct()
        import random
        import string
        column = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        with self.assertRaises(ValueError) as cm:
            for x in self.csvdoc:
                x.getcolumn(column)

    def test_getcolumn_accept_small_names(self):
        self.construct()
        for x in self.csvdoc:
            with self.assertRaises(ValueError):
                x.getcolumn("name", accept_small_names=False)

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

    def test__repr__(self):
        self.construct()
        try:
            for x in self.csvdoc:
                repr(x)
        except Exception as err:
            self.fail(err) 

    def test__addcolumn(self):
        self.construct()
        for x in self.csvdoc:
            x._addcolumns("TEST")
            x._addcolumns("TEST2", "DATA")

    def test__delcolumn(self):
        self.construct()
        for x in self.csvdoc:
            x._addcolumns("TEST")
            x._delcolumns("Name")
            with self.assertRaises(AttributeError) as cm:
                # Since _addcolumns doesn't add to the trackers
                # This would raise an AttributeError
                x.test
            with self.assertRaises(KeyError) as cm:
                # This is improper API user, this should raise
                # KeyError as the column trackers are not aware
                # That this method was called
                x.name

    def test_addcolumn_func_error(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            for x in self.csvdoc:
                x._addcolumns_func("TEST2")

    def test__addcolumn_func(self):
        import random
        self.construct()
        for x in self.csvdoc:
            a, b = (random.random(), random.random())
            x._addcolumns_func("TEST2", lambda x: (100*a)**(5*b))
            self.assertEqual((100*a)**(5*b), x["TEST2"])

    def test__call__(self):
        self.construct()
        row = self.csvdoc[0]
        self.assertEqual(row("Name"), row.getcolumn("Name"))
        row("Name", "Data")
        self.assertEqual(row("Name"), "Data")
        row("Name", delete=True)
        self.assertEqual(row("Name"), "")

    def test__setattr__attribute_error(self):
        self.construct()
        for row in self.csvdoc:
            with self.assertRaises(AttributeError) as cm:
                row.Price = None

    def test__delattr__attribute_error(self):
        self.construct()
        for row in self.csvdoc:
            with self.assertRaises(AttributeError) as cm:
                del row.Price

    def test__setattr__no_error(self):
        self.construct()
        for row in self.csvdoc:
            row.price = None

    def test__delattr__no_error(self):
        self.construct()
        for row in self.csvdoc:
            del row.price

    def test_update_values(self):
        import random
        self.construct()
        for row in self.csvdoc:
            row.update_values({"Name": random.random()})
        self.construct()
        for row in self.csvdoc:
            row.update_values(**row.longcolumn())
        self.construct()
        for row in self.csvdoc:
            kwargs = row.longcolumn()
            argspack = random.choice(tuple(kwargs.keys()))
            argsvalue = kwargs.pop(argspack)
            args = [{argspack:argsvalue}]

            row.update_values(*args, **kwargs)

    def test_update_values_args_valueerror(self):
        self.construct()
        for x in self.csvdoc:
            with self.assertRaises(ValueError):
                x.update_values({"NOT EXISTING COLUMN": None})

    def test_update_values_kwargs_valueerror(self):
        self.construct()
        for x in self.csvdoc:
            with self.assertRaises(ValueError):
                x.update_values(**{"NOT EXISTING COLUMN": None})


    def test_outputrow_typeerror(self):
        self.construct()
        with self.assertRaises(TypeError):
            self.csvdoc[0].outputrow = "BAD ARG"

    def test_outputrow(self):
        self.construct()
        self.csvdoc[0].outputrow

    def test_outputrow_set(self):
        self.construct()
        self.csvdoc[0].outputrow = True
        self.csvdoc[0].outputrow = False
        self.csvdoc[0].outputrow = True