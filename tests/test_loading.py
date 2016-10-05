import psv
import unittest
from hypothesis.strategies import text, integers, lists, dictionaries, choices
from hypothesis import given, settings
import string
from random import randint




class psv_load_test(unittest.TestCase):


    @given(columns=lists(text(min_size=5, max_size=20, alphabet=string.ascii_letters), max_size=20, min_size=2))
    @given(L=integers(5,500))
    @settings(max_examples=1)
    def generate_data_str(self, columns=None, l=None):
        columns = tuple(set(columns))
        def _gen():
            for x in range(l):
                store = {}
                for column in columns:
                    store[column] = text(min_size=3, max_size=30, alphabet=string.ascii_letters).example()
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
        columns = lists(text(min_size=5, max_size=20, alphabet=string.ascii_letters), max_size=20, min_size=2).example()
        for x in range(1,6):
            self.generate_data_str(columns=columns, l=randint(1,50))
            with open("psv-tests-"+str(x)+".csv", 'w', encoding=encoding, newline='') as csvfile:
                fieldnames = columns
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL if quote_all else 0)
                writer.writeheader()
                for items in self.csvloads_dict_tuple:
                    writer.writerow(item)

    def test_loads_str(self):
        self.generate_data_str()
        try:
            api = psv.loads(self.csvloads_str)
        except Exception as err:
            self.fail(str(err))
        self.assertTrue(bool(api.__columns__))

    def test_loads_dict(self):
        self.generate_data_str()
        try:
            api = psv.loads(self.csvloads_dict_tuple)
        except Exception as err:
            self.fail(str(err))
        self.assertFalse(bool(api.__columns__))


class psv_load_test(unittest.TestCase):

    @given(data=lists(text(min_size=5, max_size=25, alphabet=string.ascii_letters), max_size=30, min_size=1))
    @settings(max_examples=1)
    def generate_data_dir(self, data=None, files=[1,2,3]):
        def _gen():
            for x in range(l):
                store = {}
                for column in columns:
                    store[column] = text(min_size=3, max_size=30, alphabet=string.ascii_letters).example()
                yield store
        self.csvloads_dict_tuple = tuple(_gen())
        self.csvloads_dict_columns = columns
        import io
        import csv

def test(a):
    print(a)

