import psv
import unittest

from hypothesis.strategies import text, integers, lists, floats
from hypothesis import given, settings
import string
from random import randint

import os
filenames = ["tests/dataset-folder/", "tests/dataset-only-one/"]
for filename in filenames:
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
del os

small_static_csv = """Name,Price,Available,Company
Product 1,10,1,Yahoo
Product 2,15,0,Microsoft
Product 3,1,1,Google
Product 4,20,0,Yahoo
Product 5,25,1,Yahoo
Product 6,30,1,Google
Product 7,10,0,Yahoo
"""

class psv_load_tests(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(psv_load_tests, self).__init__(*args, **kwargs)
        self.is_populated = False

    @given(lists(text(min_size=5, max_size=20, alphabet=string.ascii_letters), max_size=20, min_size=3))
    @given(integers(5,500))
    @settings(max_examples=1)
    def generate_data_str(self, columns, l):
        columns = tuple(set(columns))
        def _gen():
            for x in range(l):
                store = {}
                for column in columns:
                    #Determine the kind of data to be used
                    number = randint(1,3)
                    if number == 1:
                        store[column] = text(min_size=3, max_size=30, alphabet=string.ascii_letters).example()
                    elif number == 2:
                        store[column] = integers(1, 10000).example()
                    elif number == 3:
                        store[column] = floats().example()
                yield store
        self.csvloads_dict_tuple = tuple(_gen())
        self.csvloads_dict_columns = columns
        import io
        import csv
        with io.StringIO() as csvfile:
            fieldnames = self.csvloads_dict_columns
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for item in self.csvloads_dict_tuple:
                writer.writerow(item)
            self.csvloads_str = csvfile.getvalue()

    def generate_data_str_nonrandom(self, columns, l):
        columns = tuple(set(columns))
        def _gen():
            for x in range(l):
                store = {}
                for column in columns:
                    number = randint(1,3)
                    if number == 1:
                        store[column] = text(min_size=3, max_size=30, alphabet=string.ascii_letters).example()
                    elif number == 2:
                        store[column] = integers(1, 10000).example()
                    elif number == 3:
                        store[column] = floats(1, 10000).example()
                yield store
        self.csvloads_dict_tuple = tuple(_gen())
        self.csvloads_dict_columns = columns
        import io
        import csv
        with io.StringIO() as csvfile:
            fieldnames = self.csvloads_dict_columns
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for item in self.csvloads_dict_tuple:
                writer.writerow(item)
            self.csvloads_str = csvfile.getvalue()

    def populate_folders(self):
        if self.is_populated:
            return None
        else:
            self.is_populated = True

        import csv
        columns = lists(text(min_size=5, max_size=20, alphabet=string.ascii_letters), max_size=20, min_size=2).example()
        for x in range(1,6):
            self.generate_data_str_nonrandom(columns, randint(1,50))
            with open("tests/dataset-folder/psv-tests-"+str(x)+".csv", 'w+', encoding="UTF-8", newline='') as csvfile:
                fieldnames = columns
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for item in self.csvloads_dict_tuple:
                    writer.writerow(item)
        self.generate_data_str()

        with open("tests/dataset-only-one/test.csv", 'w+', encoding="UTF-8", newline='') as csvfile:
            fieldnames = self.csvloads_dict_columns
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for item in self.csvloads_dict_tuple:
                writer.writerow(item)


    def test_loads_str(self):
        self.generate_data_str()
        try:
            api = psv.loads(self.csvloads_str)
            api = psv.loads(self.csvloads_str, csv_size_max=2**24)
        except Exception as err:
            self.fail(str(err))
        self.assertTrue(bool(api.__columns__))

    def test_loads_dict(self):
        self.generate_data_str()
        try:
            api = psv.loads(self.csvloads_dict_tuple)
            api = psv.loads(self.csvloads_dict_tuple, csv_size_max=2**24)
        except Exception as err:
            self.fail(str(err))
        self.assertFalse(bool(api.__columns__))

    def test_loaddir(self):
        self.populate_folders()
        try:
            api = psv.loaddir("tests/dataset-folder/")
            api = psv.loaddir("tests/dataset-folder/", csv_size_max=2**24 )

        except Exception as err:
            self.fail(str(err))

    def test_load(self):
        self.populate_folders()
        try:
            api = psv.load("tests/dataset-only-one/test.csv")
            api = psv.load("tests/dataset-only-one/test.csv", custom_columns=api.columns[:2])
            api = psv.load("tests/dataset-only-one/test.csv", typetransfer=True)
            api = psv.load("tests/dataset-only-one/test.csv", custom_columns=api.columns[:2], typetransfer=True)

            api = psv.load("tests/dataset-only-one/test.csv", csv_size_max=2**24)

            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"))
            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"), custom_columns=api.columns[:2])
            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"), typetransfer=True)
            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"), custom_columns=api.columns[:2], typetransfer=True)
            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"), csv_size_max=2**24)
            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"), close_file=True)


        except Exception as err:
            self.fail(str(err))

    def test_load_maxrow(self):
        self.populate_folders()
        try:
            api = psv.load("tests/dataset-only-one/test.csv", csv_max_row=100)
            api2 = psv.load(open("tests/dataset-only-one/test.csv", "r", encoding="UTF-8"), csv_max_row=100)
        except Exception as err:
            self.fail(str(err))


    def test_output_methods(self):
        self.generate_data_str()
        api = psv.loads(self.csvloads_str)
        try:
            api.outputs(quote_all=False)
            api.outputs(quote_all=True)
            api.output("TEST-OUTPUT-1.csv", quote_all=False)
            api.output("TEST-OUTPUT-1.csv", quote_all=True)
        except Exception as err:
            self.fail(str(err))

        try:
            api.outputs(columns={"NOT SUPPORTED TYPE",})
        except ValueError:
            #TEST Passed
            pass

        try:
            api.output("NAME.csv", columns={"NOT SUPPORTED TYPE",})
            self.fail("Output Method failed to catch unsupported type")
        except ValueError:
            #Test Passed
            pass

    def test_getcolumn_random_data(self):
        self.populate_folders()
        try:
            api = psv.load("tests/dataset-only-one/test.csv")
            for row in api:
                for c in api.columns:
                    row.getcolumn(c)
        except Exception as err:
            self.fail(str(err))

    def test_setcolumn_random_data(self):
        self.populate_folders()
        try:
            api = psv.load("tests/dataset-only-one/test.csv")
            for row in api:
                for c in api.columns:
                    row.setcolumn(c, None)
        except Exception as err:
            self.fail(str(err))

    def test_delcolumn_random_data(self):
        self.populate_folders()
        try:
            api = psv.load("tests/dataset-only-one/test.csv")
            for row in api:
                for c in api.columns:
                    row.delcolumn(c)
        except Exception as err:
            self.fail(str(err))

    @given(lists(text(min_size=5, max_size=20, alphabet=string.ascii_letters), max_size=20, min_size=3))
    @settings(max_examples=1)
    def test_api_new(self, columns):
        try:
            psv.new()
            psv.new(csv_size_max=2**24)
            psv.new(columns=columns)
            psv.new(columns=columns, csv_size_max=2**24)

            psv.new("TEST")
            psv.new("TEST", csv_size_max=2**24)

        except Exception as err:
            self.fail(str(err))

    def test_api_new_invalid_columns(self):
        with self.assertRaises(ValueError) as cm:
            psv.new(columns=["#$%^&*"]).addrow()

    def test_csv_size_max(self):
        try:
            psv.csv_size_limit(2**24)
        except Exception as err:
            self.fail(str(err))

    def test_forbidden_columns(self):
        with self.assertRaises(ValueError) as cm:
            psv.new(columns=["__psvcolumnstracker__"]).addrow()

    def test_loading_valueerror_emptyfile(self):
        self.populate_folders()
        with open("tests/dataset-only-one/emptyfile.csv", "w") as f:
            f.write(" \nDATA")

        with open("tests/dataset-only-one/emptyfile.csv", "r") as f:
            with self.assertRaises(ValueError) as cm:
                psv.load(f)

    def test_loading_column_names(self):
        self.populate_folders()
        with open("tests/dataset-only-one/emptyfile1.csv", "w") as f:
            f.write("")

        assert psv.column_names("tests/dataset-only-one/emptyfile1.csv") == tuple()  
        assert psv.column_names("tests/dataset-only-one/emptyfile1.csv", csv_size_max=2**24) == tuple()

    def test_loading_column_names(self):
        self.populate_folders()
        with open("tests/dataset-only-one/emptyfile2.csv", "w") as f:
            f.write("")

        assert psv.column_names("tests/dataset-only-one/emptyfile2.csv") == tuple()  
        assert psv.column_names("tests/dataset-only-one/emptyfile2.csv", csv_size_max=2**24) == tuple()

    def test_loading_emptyfile(self):
        self.populate_folders()
        with open("tests/dataset-only-one/emptyfile2.csv", "w") as f:
            f.write("")

        assert psv.load("tests/dataset-only-one/emptyfile2.csv").columns == list()  
        assert psv.load("tests/dataset-only-one/emptyfile2.csv", csv_size_max=2**24).columns == list()