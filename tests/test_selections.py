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

csv_empty = """Name,Price,Available,Company
,,,
,,,
,,,
,,,
,,,
,,,
,,,
"""

csv_test_falsey = """Name,Price,Available,Company
Product 1,,1,Yahoo
,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,
Product 1,10,,Yahoo
Product 1,10,1,Yahoo
"""

csv_matching_short = """Name,name,na-me,nAmE
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
Product 1,10,1,Yahoo
"""

special = "TEST,test,TEst"
    
csv_row_obj = """ROW_OBJ,TEST
TEST,TEST"""


class psv_selections_test(unittest.TestCase):

    def construct(self):
        self.csvdoc = psv.loads(csv, typetransfer=True)

    def test_delete_rows(self):
        self.construct()
        try:
            del self.csvdoc.rows[0]
        except Exception as err:
            self.fail(err)

    def test_index(self):
        self.construct()
        self.csvdoc.index("Name")
        self.csvdoc.index("Name", "Price")

    def test_transform(self):
        self.construct()
        self.csvdoc.transform("name", lambda x: 1)
        for row in self.csvdoc:
            self.assertEqual(1, row.name)

    def test_process(self):
        self.construct()
        self.csvdoc.process()


    def test_delete_rows_deleter(self):
        self.construct()
        try:
            del self.csvdoc[0]
        except Exception as err:
            self.fail(err)

    def test_delete_rows_getitem(self):
        self.construct()
        try:
            del self.csvdoc[0]
        except Exception as err:
            self.fail(err)

    def test_select_accepts_func(self):
        self.construct()
        try:
            self.csvdoc.select(lambda x: True)
        except Exception as err:
            self.fail(str(err))

    def test_select_function_generation(self):
        self.construct()
        try:
            self.csvdoc.select()
            self.csvdoc.select("name")
            self.csvdoc.select(name="Product 1")
            self.csvdoc.select(name=True)
            self.csvdoc.select(name=False)
            self.csvdoc.select("name", price=10)
            self.csvdoc.select("name", price=lambda p: p > 10)
            self.csvdoc.select("name", price=10, company="Yahoo", available=1)
            self.csvdoc.select("name", price=10, company="Yahoo", available=True)
            self.csvdoc.select("name", price=10, company="Yahoo", available=False)
            self.csvdoc.select("name", price=10, company=True, available=1)
            self.csvdoc.select("name", price=True, company=False, available=1)
            self.csvdoc.select("name", price=False, company="Yahoo", available=1)


            self.csvdoc.select(lambda x: False, price=10)
            self.csvdoc.select(lambda x: True, price=None)

        except Exception as err:
            self.fail(str(err))

    def test_any_select_function_generation(self):
        self.construct()
        try:
            self.csvdoc.any()
            self.csvdoc.any("name")
            self.csvdoc.any(name="Product 1")
            self.csvdoc.any(name=True)
            self.csvdoc.any(name=False)
            self.csvdoc.any("name", price=10)
            self.csvdoc.any("name", price=lambda p: p > 10)
            self.csvdoc.any("name", price=10, company="Yahoo", available=1)
            self.csvdoc.any("name", price=10, company="Yahoo", available=True)
            self.csvdoc.any("name", price=10, company="Yahoo", available=False)
            self.csvdoc.any("name", price=10, company=True, available=1)
            self.csvdoc.any("name", price=True, company=False, available=1)
            self.csvdoc.any("name", price=False, company="Yahoo", available=1)
            self.csvdoc.any(lambda x: False, price=10)
            self.csvdoc.any(lambda x: True, price=None)
            self.csvdoc.any(lambda x: False, price=True)
            self.csvdoc.any(lambda x: True, price=False)
        except Exception as err:
            self.fail(str(err))

    def test_select_function_generation_results(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.select("name")), 7)
        self.assertEqual(len(self.csvdoc.select(lambda x: x.name)), 7)
        self.assertEqual(len(self.csvdoc.select(name="Product 1")), 1)
        self.assertEqual(len(self.csvdoc.select(name=True)), 7)
        self.assertEqual(len(self.csvdoc.select(name=False)), 0)
        self.assertEqual(len(self.csvdoc.select("name", price=10)), 2)
        self.assertEqual(len(self.csvdoc.select("name", price=10, company=True)), 2)
        self.assertEqual(len(self.csvdoc.select("name", price=10, company=False)), 0)

        self.assertEqual(len(self.csvdoc.select(lambda x: x.name, price=10)), 2)
        self.assertEqual(len(self.csvdoc.select("name", price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.select(lambda x: x.name, price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.select("name", price=10, company="Yahoo", available=1)), 1)
    
    def test_any_select_function_generation_results(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.any("name")), 7)
        self.assertEqual(len(self.csvdoc.any(lambda x: x.name)), 7)
        self.assertEqual(len(self.csvdoc.any(name="Product 1")), 1)
        self.assertEqual(len(self.csvdoc.any(name=True)), 7)
        self.assertEqual(len(self.csvdoc.any(name=False)), 0)

        self.assertEqual(len(self.csvdoc.any("name", price=10)), 7)
        self.assertEqual(len(self.csvdoc.any("name", price=10, company=True)), 7)
        self.assertEqual(len(self.csvdoc.any("name", price=10, company=False)), 7)

        self.assertEqual(len(self.csvdoc.any(lambda x: x.name, price=10)), 7)
        self.assertEqual(len(self.csvdoc.any("name", price=lambda p: p > 10)), 7)
        self.assertEqual(len(self.csvdoc.any(lambda x: x.name, price=lambda p: p > 10)), 7)
        self.assertEqual(len(self.csvdoc.any("name", price=10, company="Yahoo", available=1)), 7)


    def test_safe_select_accepts_func(self):
        self.construct()
        try:
            self.csvdoc.safe_select(lambda x: True)
        except Exception as err:
            self.fail(str(err))

    def test_safe_select_function_generation(self):
        self.construct()
        try:
            self.csvdoc.safe_select()
            self.csvdoc.safe_select("name")
            self.csvdoc.safe_select(name="Product 1")
            self.csvdoc.safe_select("name", price=10)
            self.csvdoc.safe_select("name", price=lambda p: p > 10)
            self.csvdoc.safe_select("name", price=10, company="Yahoo", available=1)
            self.csvdoc.safe_select(lambda x: False, price=10)
            self.csvdoc.safe_select(lambda x: True, price=None)
        except Exception as err:
            self.fail(str(err))

    def test_any_safe_select_function_generation(self):
        self.construct()
        try:
            self.csvdoc.safe_any()
            self.csvdoc.safe_any("name")
            self.csvdoc.safe_any(name="Product 1")
            self.csvdoc.safe_any("name", price=10)
            self.csvdoc.safe_any("name", price=lambda p: p > 10)
            self.csvdoc.safe_any("name", price=10, company="Yahoo", available=1)
            self.csvdoc.safe_any(lambda x: False, price=10)
            self.csvdoc.safe_any(lambda x: True, price=None)


        except Exception as err:
            self.fail(str(err))


    def test_safe_select_function_generation_results(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.safe_select("name")), 7)
        self.assertEqual(len(self.csvdoc.safe_select(lambda x: x.name)), 7)
        self.assertEqual(len(self.csvdoc.safe_select(name="Product 1")), 1)
        self.assertEqual(len(self.csvdoc.safe_select("name", price=10)), 2)
        self.assertEqual(len(self.csvdoc.safe_select(lambda x: x.name, price=10)), 2)
        self.assertEqual(len(self.csvdoc.safe_select("name", price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.safe_select(lambda x: x.name, price=lambda p: p > 10)), 4)
        self.assertEqual(len(self.csvdoc.safe_select("name", price=10, company="Yahoo", available=1)), 1)        


    def test_any_safe_select_function_generation_results(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.safe_any("name")), 7)
        self.assertEqual(len(self.csvdoc.safe_any(lambda x: x.name)), 7)
        self.assertEqual(len(self.csvdoc.safe_any(name="Product 1")), 1)
        self.assertEqual(len(self.csvdoc.safe_any("name", price=10)), 7)
        self.assertEqual(len(self.csvdoc.safe_any(lambda x: x.name, price=10)), 7)
        self.assertEqual(len(self.csvdoc.safe_any("name", price=lambda p: p > 10)), 7)
        self.assertEqual(len(self.csvdoc.safe_any(lambda x: x.name, price=lambda p: p > 10)), 7)
        self.assertEqual(len(self.csvdoc.safe_any("name", price=10, company="Yahoo", available=1)), 7)

    def test_no_output(self):
        self.construct()
        self.csvdoc.no_output()
        self.assertEqual(self.csvdoc.lenoutput(), 0)

    def test_all_output(self):
        self.construct()
        self.csvdoc.no_output()
        self.csvdoc.all_output()
        self.assertEqual(self.csvdoc.lenoutput(), 7)

    def test_flip_output(self):
        self.construct()
        self.csvdoc[:3].no_output()
        self.csvdoc.flip_output()
        self.assertEqual(self.csvdoc.lenoutput(), 3)

    def test_lenoutput(self):
        self.construct()
        try:
            self.csvdoc.lenoutput()
        except Exception as err:
            self.fail(str(err))

    def test_len_no_output(self):
        self.construct()
        try:
            self.csvdoc.len_no_output()
        except Exception as err:
            self.fail(str(err))

    def test_columns(self):
        self.construct()
        try:
            self.csvdoc.columns
        except Exception as err:
            self.fail(str(err))

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
        self.assertTrue(isinstance(self.csvdoc.grab("name", psv.ROW_OBJ)[0][1], psv.core.objects.rowobjects.BaseRow))
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

    def test_single_find_valueerror(self):
        self.construct()
        with self.assertRaises(ValueError) as cm:
            print(self.csvdoc.single_find(available=1))

    def test_single_find_any_valueerror(self):
        self.construct()
        with self.assertRaises(ValueError) as cm:
            self.csvdoc.single_find_any(available=1)

    def test_find_any(self):
        self.construct()
        self.assertTrue(bool(self.csvdoc.find_any(name="Product 1", price=lambda x: None)))
        self.assertFalse(bool(self.csvdoc.find_any(name="INVALID NAME")))

    def test_findall_any(self):
        self.construct()
        self.assertEqual(len(self.csvdoc.find_all_any(company="Yahoo", price=lambda x: None)), 4)
        self.assertFalse(bool(self.csvdoc.find_all_any(company="INVALID COMPANY")))

    def test_single_find_any(self):
        self.construct()
        self.assertTrue(bool(self.csvdoc.single_find_any(name="Product 1", price=lambda x: None)))
        self.assertFalse(bool(self.csvdoc.single_find_any(name="INVALID NAME")))
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

    def test_merge_valueerror(self):
        self.construct()
        with self.assertRaises(ValueError) as cm:
            self.csvdoc.merge(psv.new())


    def test_safe_merge(self):
        self.construct()
        try:
            self.csvdoc.safe_merge(self.csvdoc[:int(len(self.csvdoc)/2)])
        except Exception as err:
            self.fail(err)


    def test_non_hash_merge(self):
        self.construct()
        try:
            self.csvdoc.non_hash_merge(self.csvdoc[:int(len(self.csvdoc)/2)])
        except Exception as err:
            self.fail(err)

    def test_columns_setterworks(self):
        self.construct()
        self.csvdoc.columns
        self.csvdoc.__columns__ = ["Hello 5"]
    
    def test_addrow(self):
        self.construct()
        row = self.csvdoc.addrow()
        self.assertEqual(row, self.csvdoc[-1])

    def test_addcolumn(self):
        self.construct()
        self.csvdoc.addcolumn("Test-Row-1")
        self.assertTrue("Test-Row-1" in self.csvdoc.columns)
        self.assertTrue("testrow1" in self.csvdoc.__columnsmap__.keys())

    def test_addcolumn_sel(self):
        self.construct()
        sel = self.csvdoc.select()
        sel.addcolumn("Test-Row-1")
        self.assertTrue("Test-Row-1" in sel.columns)
        self.assertTrue("testrow1" in sel.__columnsmap__.keys())


    def test_addcolumn_func(self):
        self.construct()
        self.csvdoc.addcolumn("Test-Row-1", lambda x: 1+2)
        self.assertTrue("Test-Row-1" in self.csvdoc.columns)
        self.assertTrue("testrow1" in self.csvdoc.__columnsmap__.keys())
        self.assertTrue(all(x.testrow1 == 3 for x in self.csvdoc))

    def test_addcolumn_func_sel(self):
        self.construct()
        self.csvdoc = self.csvdoc.select()
        self.csvdoc.addcolumn("Test-Row-1", lambda x: 1+2)
        self.assertTrue("Test-Row-1" in self.csvdoc.columns)
        self.assertTrue("testrow1" in self.csvdoc.__columnsmap__.keys())
        self.assertTrue(all(x.testrow1 == 3 for x in self.csvdoc))

 
    def test_delcolumn(self):
        self.construct()
        self.csvdoc.addcolumn("Test-Row-1") #This is covered in seperate test
        self.csvdoc.delcolumn("Test-Row-1")
        self.assertFalse("Test-Row-1" in self.csvdoc.columns)
        self.assertFalse("testrow1" in self.csvdoc.__columnsmap__.keys())

    def test_delcolumn_sel(self):
        self.construct()
        self.csvdoc = self.csvdoc.select()
        self.csvdoc.addcolumn("Test-Row-1") #This is covered in seperate test
        self.csvdoc.delcolumn("Test-Row-1")
        self.assertFalse("Test-Row-1" in self.csvdoc.columns)
        self.assertFalse("testrow1" in self.csvdoc.__columnsmap__.keys())

    def test_delcolumn_valueerror(self):
        self.construct()
        with self.assertRaises(ValueError) as cm:
            self.csvdoc.delcolumn("Test-Row-1")


    def test_addrow_kw(self):
        import random
        self.construct()
        row = self.csvdoc.addrow(**({x:random.randint(1,100) for x in self.csvdoc.columns} ))
        self.assertEqual(row, self.csvdoc[-1])

    def test__columnsmap__(self):
        self.construct()
        try:
            self.csvdoc.__columnsmap__
        except Exception as err:
            self.fail(str(err))

    def test__columnsmap___select(self):
        self.construct()
        try:
            self.csvdoc.select().__columnsmap__
        except Exception as err:
            self.fail(str(err))

    def test_repeat_columns(self):
        try:
            api = psv.loads(special)
        except Exception as err:
            self.fail(str(err))

    def test_badgetitem_main(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc[None]


    def test_badgetitem_select(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc.select()[None]


    def test_addcolumn_failure(self):
        TEST = psv.new("TEST")
        with self.assertRaises(ValueError) as cm:
            TEST.addcolumn("TEST")      

    def test_utils_multiindex(self):
        test = psv.loads(csv_row_obj)
        value = test.grab("ROW_OBJ", psv.ROW_OBJ)
        self.assertTrue(isinstance(value[0][0], str))
        self.assertTrue(isinstance(value[0][1], psv.core.objects.rowobjects.BaseRow))

    def test_multiindex_typeerror(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc.grab(False, None)

    def test_badgrab_valueerror(self):
        self.construct()
        with self.assertRaises(ValueError) as cm:
            self.csvdoc.grab(*tuple())

    def test_badgrab_valueerror_unique(self):
        self.construct()
        with self.assertRaises(ValueError) as cm:
            self.csvdoc.unique(*tuple())

    def test_remove_duplicates_selection(self):
        test = psv.loads(csv_repeat).select()
        try:
            test = test.remove_duplicates()
        except Exception as err:
            self.fail(str(err))
        self.assertEqual(len(test), 1)

    def test_remove_duplicates_hard_selection(self):
        test = psv.loads(csv_repeat).select()
        try:
            test.remove_duplicates(soft=False)
        except Exception as err:
            self.fail(str(err))
        self.assertEqual(len(test), 1)

    def test_remove_duplicates_main_selection(self):
        test = psv.loads(csv_repeat)
        try:
            test = test.remove_duplicates()
        except Exception as err:
            self.fail(str(err))
        self.assertEqual(len(test), 1)

    def test_remove_duplicates_hard_main_selection(self):
        test = psv.loads(csv_repeat)
        try:
            test.remove_duplicates(soft=False)
        except Exception as err:
            self.fail(str(err))
        self.assertEqual(len(test), 1)


    def test_arg_select(self):
        test = psv.loads(csv_empty)
        try:
            self.assertEqual(len(test.select("Name")),0)
        except Exception as exc:
            self.fail(str(exc))

    def test_column_attributes(self):
        self.construct()
        try:
            self.csvdoc.columns_attributes
        except Exception as err:
            self.fail(err)

    def test_columns_mapping(self):
        self.construct()
        try:
            self.csvdoc.columns_mapping
        except Exception as err:
            self.fail(err)


    def test_columns(self):
        self.construct()
        self.csvdoc.columns
    
    # def test_select_typeerror(self):
    #     self.construct()
    #     with self.assertRaises(TypeError) as cm:
    #         self.csvdoc.select(tuple())


    def test_loading_valueerror_emptyfile_cleanupname(self):
        import io
        with open("tests/dataset-only-one-empty/emptyfile.csv", "w") as f:
            f.write(" \nDATA")


        with open("tests/dataset-only-one-empty/emptyfile.csv", "r") as f:
            with self.assertRaises(ValueError) as cm:
                psv.load(f)

    def test_loading_valueerror_emptyfile(self):
        import io
        with open("tests/dataset-only-one-empty/emptyfile.csv", "w") as f:
            f.write("\nDATA")


        with open("tests/dataset-only-one-empty/emptyfile.csv", "r") as f:
            with self.assertRaises(ValueError) as cm:
                psv.load(f)


    def test_typeerror_any(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc.any(1)

    def test_typeerror_select(self):
        self.construct()
        with self.assertRaises(TypeError) as cm:
            self.csvdoc.select(1)

    def test_translate_type_attributeError_works(self):
        from psv.core.utils import translate_type
        self.assertEquals(translate_type(None), None)

    def test_delrow(self):
        self.construct()
        del self.csvdoc[0]

    def test_delrow_attr(self):
        self.construct()
        del self.csvdoc.rows[1]

    def test_psv_column_crunch(self):
        api = psv.loads(csv_matching_short)
        api.addcolumn("name_3")
        with self.assertRaises(ValueError):
            api[0].getcolumn("NAME")

    def test_psv_column_crunch_columns_mapping(self):
        api = psv.loads(csv_matching_short)
        api.addcolumn("name_3")
        api.columns_mapping

    def test_columns_sel(self):
        self.construct()
        self.csvdoc.select().columns

    def test_merge_results(self):
        test1 = psv.new(columns=["TEST"])

        for i in range(1000):
            test1.addrow(test=i)


        sel1, sel2 = test1[:250], test1[750:]

        print(len(sel1), len(sel2))

        self.assertEqual(len(sel1.merge(sel2)), 500)


    def test_merge_results(self):
        test1 = psv.new(columns=["TEST"])


        for i in range(1000):
            test1.addrow(test=i)


        sel1, sel2 = test1[:250], test1[750:]

        self.assertEqual(len(sel1.safe_merge(sel2)), 500)

    def test_merge_results(self):
        test1 = psv.new(columns=["TEST"])

        for i in range(1000):
            test1.addrow(test=i)


        sel1, sel2 = test1[:250], test1[750:]

        self.assertEqual(len(sel1.non_hash_merge(sel2)), 500)

    def test_loads(self):
        small_static_csv = """Name,Price,Available,Company
        Product 1,10,1,Yahoo
        Product 2,15,0,Microsoft
        Product 3,1,1,Google
        Product 4,20,0,Yahoo
        Product 5,25,1,Yahoo
        Product 6,30,1,Google
        Product 7,10,0,Yahoo
        """

        psv.loads([])

    def test_merge_typeerror(self):
        self.construct()
        self.csvdoc[0].name = set()
        with self.assertRaises(TypeError):
            self.csvdoc.merge(self.csvdoc)

    def test_fast_find_valueerror(self):
        self.construct()
        with self.assertRaises(ValueError):
            self.csvdoc.fast_find(name=None, product=None)

    def test_fast_find(self):
        self.construct()
        assert self.csvdoc.fast_find(name="Product 1")

    def test_non_hash_merge_typeerror(self):
        self.construct()
        a = psv.new()
        b = psv.new()
        with self.assertRaises(ValueError):
            a.non_hash_merge(b)


    def test_non_hash_merge(self):
        self.construct()
        a = self.csvdoc[:5].no_output()
        b = self.csvdoc[5:]
        api = a.non_hash_merge(b)
        for x in a:
            assert x.outputrow == False



    def test_outputtedrows(self):
        self.construct()
        self.csvdoc.outputtedrows

    def test_non_outputted_rows(self):
        self.construct()
        self.csvdoc.nonoutputtedrows

    def test_cls_acceptance_non_class(self):
        with self.assertRaises(ValueError):
            api = psv.new("TEST", "TEST")


    def test_cls_acceptance_class(self):
        class DummyClass: pass
        with self.assertRaises(ValueError):
            api = psv.new("TEST", DummyClass)

    def test_addrow_class(self):
        class DummyClass: pass
        api = psv.new("TEST")
        with self.assertRaises(TypeError):
            rrow = api.addrow(cls=DummyClass)

    def test_addrow_string(self):
        api = psv.new("TEST")
        with self.assertRaises(ValueError):
            rrow = api.addrow(cls="TEST")

    # def test_addrow_other(self):
    #     from collections import namedtuple
    #     api = psv.new("TEST")
    #     with self.assertRaises(ValueError):
    #         rrow = api.addrow(cls=)

    # def test_addrow_CLSROW(self):
    #     api = psv.new("TEST")
    #     with self.assertRaises(TypeError):
    #         rrow = api.addrow(cls=None)

    def test_addrow_OTHERTYPEROW(self):
        from psv.core.objects import Row
        class BadRow(Row):
            def __init__(self, *args, **kwargs):
                raise TypeError
        api = psv.new("TEST")
        with self.assertRaises(TypeError):
            rrow = api.addrow(cls=BadRow)