'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import unittest

from climatechange.file import load_dict_by_package
from climatechange.headers import HeaderDictionary, HeaderType, Header


class Test(unittest.TestCase):


    def setUp(self):
        self.abcDict = { "a": "a", "b": "a", "c": "c", "d": "c", "e": "e"}
        self.hd = HeaderDictionary()  # Should be the default header dictionaries
        pass

    def tearDown(self):
        pass

    def testHeaderDictionaryCreation(self):
                
        h_dict = load_dict_by_package('header_dict.json')
        
        for h, v in h_dict.items():
            h_dict[h] = HeaderType(v)

        self.assertDictEqual(h_dict, self.hd.get_header_dict(), 'Header dictionaries do not match')

        self.assertDictEqual(load_dict_by_package('unit_dict.json'), self.hd.get_unit_dict(), 'Unit dictionaries do not match')
        
        customHd = HeaderDictionary(self.abcDict, self.abcDict)
        
        self.assertEqual(self.abcDict, customHd.get_header_dict())
        
        self.assertEqual('a', customHd.get_header_dict()['a'])
        self.assertEqual('c', customHd.get_header_dict()['d'])
        
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
        
        testDict:Map[str, HeaderType] = {"test years (BP)": HeaderType.YEARS,
                                         "test depth (m)": HeaderType.DEPTH,
                                         "test_sample": HeaderType.SAMPLE,
                                         "test_sample (ppb)" : HeaderType.SAMPLE}
        testUnit:Map[str, str] = {"ppb" : "ppb"}
        
        testHeaderDict = HeaderDictionary(testDict, testUnit)
        
        self.assertEqual([], testHeaderDict.parse_headers(noHeaders))
        
        oneHeaderNoUnit = ['test_sample']
        
        self.assertEqual(str([Header('test_sample', HeaderType.SAMPLE, ('test_sample', None))]),
                         str(testHeaderDict.parse_headers(oneHeaderNoUnit)))
        
        oneHeaderWithUnit = ['test_sample (ppb)']
                
        self.assertEqual(str([Header(oneHeaderWithUnit[0], HeaderType.SAMPLE, ('test_sample', 'ppb'))]),
                         str(testHeaderDict.parse_headers(oneHeaderWithUnit)))
        
        oneHeaderWithUnitAndNotExisting = ['test_sample (ppb)', 'test2 Not in (ppb)']
        
        self.assertEqual(str([Header(oneHeaderWithUnitAndNotExisting[0], HeaderType.SAMPLE, ('test_sample', 'ppb')),
                              Header(oneHeaderWithUnitAndNotExisting[1], HeaderType.UNKNOWN, ('test2 Not in', 'ppb'))]),
                         str(testHeaderDict.parse_headers(oneHeaderWithUnitAndNotExisting)))
        
        oneHeaderWithUnitAndNotExistingUnit = ['test_sample (ppb)', 'test_sample (not in unit)']
        
        self.assertEqual(str([Header(oneHeaderWithUnitAndNotExistingUnit[0], HeaderType.SAMPLE, ('test_sample', 'ppb')),
                          Header(oneHeaderWithUnitAndNotExistingUnit[1], HeaderType.UNKNOWN, ('test_sample', 'not in unit'))]),
                         str(testHeaderDict.parse_headers(oneHeaderWithUnitAndNotExistingUnit)))
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
