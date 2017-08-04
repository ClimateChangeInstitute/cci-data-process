'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import unittest

from climatechange.file import load_dict_by_package
from climatechange.headers import HeaderDictionary, HeaderType, Header, to_headers


class Test(unittest.TestCase):


    def setUp(self):
        self.a = Header("a",HeaderType.YEARS, "aclass", "aunit", "alabel")
        self.c = Header("c",HeaderType.SAMPLE, "cclass", "cunit", "clabel")
        self.d = Header("d",HeaderType.SAMPLE, "dclass", "dunit", "dlabel")
        self.e = Header("e",HeaderType.YEARS, "eclass", "eunit", "elabel")
        self.abcDict = { "a": self.a,
                         "b": self.a,
                         "c": self.c,
                         "d": self.d,
                         "e": self.e}
        self.hd = HeaderDictionary()  # Should be the default header dictionaries

    def tearDown(self):
        pass

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
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
