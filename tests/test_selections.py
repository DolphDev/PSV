import psv
import unittest

csv = """Name,Price,Available,Company
Product 1,10,1,FatStax
Product 2,15,0,Red Funnel Consulting
Product 3,1,1,Google
Product 4,20,0,FatStax
Product 5,25,1,FatStax
Product 6,30,1,Google
Product 7,10,0,FatStax
"""

# These Tests make sure that Nationstates obj keeps concurrent all object values

class psv_selections_test(unittest.TestCase):

    def construct(self):
        self.csvdoc = psv.loads(csv)


    def test_select_accepts_func(self):
        self.construct()
        try:
            self.csvdoc.select(lambda x: True)
        except Exception as err:
            self.fail(str(err))

    def test_select_function_generation(self):
        self.construct()
        try:
            self.csvdoc.select("name")
            self.csvdoc.select(name="Product 1")
            self.csvdoc.select("name", price=10)
            self.csvdoc.select("name", price=lambda p: p > 10)
            self.csvdoc.select("name", price=10, company="FatStax", available=1)
        except Exception as err:
            self.fail(str(err))

    def test_select_function_generation_results(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.select("name")), 7)
        self.assertEqual(len(self.csvdoc.select(name="Product 1")), 1)
        self.assertEqual(len(self.csvdoc.select("name", price=10)), 2)
        self.assertEqual(len(self.csvdoc.select("name", price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.select("name", price=10, company="FatStax", available=1)), 1)
