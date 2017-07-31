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
            self.csvdoc.select("name", price=10, company="Yahoo", available=1)
        except Exception as err:
            self.fail(str(err))

    def test_select_function_generation_results(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.select("name")), 7)
        self.assertEqual(len(self.csvdoc.select(lambda x: x.name)), 7)
        self.assertEqual(len(self.csvdoc.select(name="Product 1")), 1)
        self.assertEqual(len(self.csvdoc.select("name", price=10)), 2)
        self.assertEqual(len(self.csvdoc.select(lambda x: x.name, price=10)), 2)
        self.assertEqual(len(self.csvdoc.select("name", price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.select(lambda x: x.name, price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.select("name", price=10, company="Yahoo", available=1)), 1)

    def test_no_output(self):
        self.construct()
        self.csvdoc.no_output()
        self.assertEqual(self.csvdoc.lenoutput(), 0)

    def test_all_output(self):
        self.construct()
        self.csvdoc.no_output()
        self.csvdoc.all_output()
        self.assertEqual(self.csvdoc.lenoutput(), 7)

    def test_all_output(self):
        self.construct()
        self.csvdoc[:3].no_output()
        self.csvdoc.flip_output()
        self.assertEqual(self.csvdoc.lenoutput(), 3)


    def test_enable(self):
        self.construct()
        self.csvdoc.no_output()
        self.csvdoc.enable(name="Product 1")
        self.assertEqual(self.csvdoc.lenoutput(), 1)

    def test_disable(self):
        self.construct()
        self.csvdoc.disable(name="Product 1")
        self.assertEqual(self.csvdoc.lenoutput(), 6)

    def test_flip(self):
        self.construct()
        self.csvdoc.flip(name="Product 1")
        self.assertEqual(self.csvdoc.lenoutput(), 6)

    def test_grab(self):
        self.construct()
        self.assertEqual(tuple(self.csvdoc["name"]), self.csvdoc.grab("name"))
        self.assertEqual(tuple(self.csvdoc["name", "price"]), self.csvdoc.grab("name", "price"))

    def test_unique(self):
        self.construct()
        self.assertEqual(set(self.csvdoc["name"]), self.csvdoc.unique("name"))
        self.assertEqual(set(self.csvdoc["name", "price"]), self.csvdoc.unique("name", "price"))

    def test_indexing(self):
        self.construct()
        self.assertTrue(isinstance(self.csvdoc.grab("name", "ROW_OBJ")[0][1], psv.core.objects.rowobjects.BaseRow))
        try:
            self.csvdoc.grab("ROW_OBJ")
            self.csvdoc.fail("PSV did not catch incorrect ROW_OBJ use")
        except:
            pass

        self.assertTrue(isinstance(self.csvdoc[0],  psv.core.objects.rowobjects.BaseRow))

    def test_tabulating(self):
        self.construct()
        try:
            self.csvdoc.tabulate()
            self.csvdoc.tabulate(format="html", limit=10, only_ascii=False, text_limit=1000, remove_newline=False)
        except Exception as err:
            self.fail(str(err))

    def test_find(self):
        self.construct()
        self.assertTrue(bool(self.csvdoc.find(name="Product 1")))
        self.assertFalse(bool(self.csvdoc.find(name="INVALID NAME")))

    def test_findall(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.find_all(company="Yahoo")), 4)
        self.assertFalse(bool(self.csvdoc.find_all(company="INVALID COMPANY")))

    def test_single_find(self):
        self.construct()
        self.assertTrue(bool(self.csvdoc.single_find(name="Product 1")))
        self.assertFalse(bool(self.csvdoc.single_find(name="INVALID NAME")))
        try:
            self.csvdoc.find(company="Yahoo")
            self.fail("Single Find did not raise exception for duplicates")
        except Exception:
            pass

    def test_merge(self):
        self.construct()
        try:
            self.csvdoc.merge(self.csvdoc[:int(len(self.csvdoc)/2)])
        except Exception as err:
            self.fail(err)

    def test_safe_merge(self):
        self.construct()
        try:
            self.csvdoc.merge(self.csvdoc[:int(len(self.csvdoc)/2)], safe=True)
        except Exception as err:
            self.fail(err)


    def test_non_hash_merge(self):
        self.construct()
        try:
            self.csvdoc.non_hash_merge(self.csvdoc[:int(len(self.csvdoc)/2)])
        except Exception as err:
            self.fail(err)

    def test_columns(self):
        self.construct()
        self.csvdoc.columns
        self.csvdoc.columns = ["Hello 5"]
    
    def test_addrow(self):
        self.construct()
        row = self.csvdoc.addrow()
        self.assertEqual(row, self.csvdoc[-1])






