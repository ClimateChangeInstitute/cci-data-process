'''
Created on Jul 12, 2017

@author: Mark Royer
'''
from builtins import ValueError
import json
import logging
import os
import unittest

import numpy
from pandas.core.frame import DataFrame

from climatechange.file import load_dict_by_package
from climatechange.headers import HeaderDictionary, HeaderType, Header, to_headers, \
    load_headers, HeaderEncoder, process_header_data


class Test(unittest.TestCase):


    def setUp(self):
        self.a = Header("a", HeaderType.YEARS, "aclass", "aunit", "alabel")
        self.c = Header("c", HeaderType.SAMPLE, "cclass", "cunit", "clabel")
        self.d = Header("d", HeaderType.SAMPLE, "dclass", "dunit", "dlabel")
        self.e = Header("e", HeaderType.YEARS, "eclass", "eunit", "elabel")
        self.unknown_header = Header("not known", HeaderType.UNKNOWN, None, None, None)
        self.abcDict = { "a": self.a,
                         "b": self.a,
                         "c": self.c,
                         "d": self.d,
                         "e": self.e}
        self.hd = HeaderDictionary()  # Should be the default header dictionaries

    def tearDown(self):
        pass

    def testHeaderEqual(self):
        h1 = Header('test', HeaderType.YEARS, 'Years', 'BP', 'Year (BP)')
        h2 = Header('test', HeaderType.YEARS, 'Years', 'BP', 'Year (BP)')
        h3 = Header('test3', HeaderType.YEARS, 'Years', 'BP', 'Year (BP)')
        
        self.assertTrue(h1 == h1)
        self.assertTrue(h1 == h2)
        self.assertTrue(h2 == h1)
        self.assertFalse(h1 == h3)
        self.assertFalse(h3 == h1)
        self.assertFalse(h3 == h2)
        self.assertFalse(h1 == object())
        
    def testHeaderEncoder(self):
        
        objstr = json.dumps([ h for (_,h) in self.abcDict.items()], cls=HeaderEncoder)
        expstr = ''.join(['[{"name": "a", "type": "Years", "class": "aclass", "unit": "aunit", "label": "alabel"},',
                          ' {"name": "a", "type": "Years", "class": "aclass", "unit": "aunit", "label": "alabel"},',
                          ' {"name": "c", "type": "Sample", "class": "cclass", "unit": "cunit", "label": "clabel"},',
                          ' {"name": "d", "type": "Sample", "class": "dclass", "unit": "dunit", "label": "dlabel"},',
                          ' {"name": "e", "type": "Years", "class": "eclass", "unit": "eunit", "label": "elabel"}]'])
                   
        self.assertEqual(expstr, objstr)
        
        self.assertRaises(NotImplementedError, HeaderEncoder().default, object())     


    def testHeaderDictionaryCreation(self):
                
        h_dict = load_dict_by_package('header_dict.json', obj_hook=to_headers)
        self.assertDictEqual(h_dict,
                             self.hd.get_header_dict(),
                             'Header dictionaries do not match')
        

        self.assertDictEqual(load_dict_by_package('unit_dict.json'),
                             self.hd.get_unit_dict(),
                             'Unit dictionaries do not match')
        
        customHd = HeaderDictionary(self.abcDict, self.abcDict)
        
        self.assertEqual(self.abcDict, customHd.get_header_dict())
        
        self.assertEqual(self.a, customHd.get_header_dict()['a'])
        self.assertEqual(self.d, customHd.get_header_dict()['d'])
        
        self.assertEqual(self.abcDict, customHd.get_header_dict())
        
    def testParseHeader(self):
        
        self.assertEqual(('Dat210617', None), Header.parse_header('Dat210617'))
        self.assertEqual(('Dat011216V2', None), Header.parse_header('Dat011216V2'))
        
        self.assertEqual(('depth', 'm abs'), Header.parse_header('depth (m abs)'))
        self.assertEqual(('Cond', '+ALU-S/cm'), Header.parse_header('Cond (+ALU-S/cm)'))
        self.assertEqual(('Na', 'ppb'), Header.parse_header('Na (ppb)'))
        self.assertEqual(('Ca', 'ppb'), Header.parse_header('Ca (ppb)'))
        self.assertEqual(('Dust', 'part/ml'), Header.parse_header('Dust (part/ml)'))
        self.assertEqual(('NH4', 'ppb'), Header.parse_header('NH4 (ppb)'))
        
        # Test with some additional strange spacing
        self.assertEqual(('NO3', 'ppb'), Header.parse_header('NO3 (ppb)'))
        self.assertEqual(('NO3', 'ppb'), Header.parse_header('  NO3 (  ppb   )    '))
       

    def testParseHeaders(self):
        
        noHeaders:Map[str, HeaderType] = []
        
        test_years = Header("test years (BP)", HeaderType.YEARS, "Years", "BP", "test_years_(BP)")
        test_depth = Header("test depth (m)", HeaderType.DEPTH, "Depth", "m", "test_depth_(m)")
        test_sample_nounit = Header("test_sample", HeaderType.SAMPLE, "Sample", None, "test_sample")
        test_sample = Header("test_sample (ppb)", HeaderType.SAMPLE, "Sample", "ppb", "test_sample_(ppb)")
        testDict:Map[str, Header] = {"test years (BP)": test_years,
                                         "test depth (m)": test_depth,
                                         "test_sample": test_sample_nounit,
                                         "test_sample (ppb)" : test_sample}
        testUnit:Map[str, str] = {"ppb" : "ppb"}
        
        testHeaderDict = HeaderDictionary(testDict, testUnit)
        
        self.assertEqual([], testHeaderDict.parse_headers(noHeaders))
        
        oneHeaderNoUnit = ['test_sample']
        
        self.assertListEqual([test_sample_nounit], testHeaderDict.parse_headers(oneHeaderNoUnit))
        
        oneHeaderWithUnit = ['test_sample (ppb)']
                
        self.assertListEqual([test_sample], testHeaderDict.parse_headers(oneHeaderWithUnit))
        
        oneHeaderWithUnitAndNotExisting = ['test_sample (ppb)', 'test2 Not in (ppb)']
        
        self.assertListEqual([test_sample,
                              Header('test2 Not in (ppb)', HeaderType.UNKNOWN, None, None, None)],
                             testHeaderDict.parse_headers(oneHeaderWithUnitAndNotExisting))
        
        oneHeaderWithUnitAndOneWithoutUnit = ['test_sample (ppb)', 'test_sample']
        
        self.assertListEqual([test_sample, test_sample_nounit],
                             testHeaderDict.parse_headers(oneHeaderWithUnitAndOneWithoutUnit))
            
    def testAddHeader(self):
        
        self.assertRaises(ValueError, self.hd.add_header, self.unknown_header)     
        
        hdict = HeaderDictionary(self.abcDict)
        
        self.assertEqual(self.a,
                         hdict.add_header(self.a),
                         "Previous header should be returned")
        
        h = Header("test", HeaderType.YEARS, "Years", "CE", "test_(BP)")

        self.assertEqual(None,
                         hdict.add_header(h),
                         "New header should return None")
        
        self.assertEqual(h,
                         hdict.add_header(h),
                         "Previous header should be returned")
        
    def testLoadHeaders(self):
        
        h1 = Header("Sr (ng/L)",HeaderType.SAMPLE,"Sr","ng/L","Sr_(ng/L)")
        h_last = Header("K (ug/L)",HeaderType.SAMPLE,"K", "ug/L","K_(ug/L)")
        
        with open(os.path.join('csv_files','header_input.csv'), 'r') as f:
            headers = load_headers(f)
            self.assertEqual(h1, headers[0], "First header is Strontium")
            self.assertEqual(h_last, headers[len(headers)-1], "Last header is Potasium")
        

    def testProcessHeaderData(self):
        
        unknown_headers = ['test_sample (ppb)', 'test2 Not in (ppb)']
        
        df = DataFrame(numpy.random.randn(10,2), columns=unknown_headers)
        
        logging.disable(logging.CRITICAL)
        headers = process_header_data(df)
        
        self.assertEqual(HeaderType.UNKNOWN, headers[0].htype)
        self.assertEqual(HeaderType.UNKNOWN, headers[1].htype)
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
