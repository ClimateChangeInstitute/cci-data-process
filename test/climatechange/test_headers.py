'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import pkg_resources
import unittest

from climatechange.headers import load_dictionary, HeaderDictionary


class Test(unittest.TestCase):


    def setUp(self):
        self.abcDict = { "a": "a", "b": "a", "c": "c", "d": "c", "e": "e"}
        self.hd = HeaderDictionary()  # Should be the default header dictionaries
        pass

    def tearDown(self):
        pass


    def testLoadDictionary(self):
        
        fileName = os.path.join('json_files', 'nothing.json')
        with open(fileName, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f), "Empty dictionary was expected")
         
        fileName = os.path.join('json_files', 'empty.json')
        with open(fileName, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f), "Empty dictionary was expected")
        
        fileName = os.path.join('json_files', 'abcDict.json')
        with open(fileName, 'r') as f:
            self.assertDictEqual(self.abcDict, load_dictionary(f), "%s dictionary does not match" % f)

    def testHeaderDictionaryCreation(self):
                
        with open(pkg_resources.resource_filename('climatechange', 'header_dict.json')) as file:  # @UndefinedVariable
            self.assertDictEqual(load_dictionary(file), self.hd.get_header_dict(), 'Header dictionaries do not match')
            
        with open(pkg_resources.resource_filename('climatechange', 'unit_dict.json')) as file:  # @UndefinedVariable
            self.assertDictEqual(load_dictionary(file), self.hd.get_unit_dict(), 'Unit dictionaries do not match')
        
        customHd = HeaderDictionary(self.abcDict, self.abcDict)
        
        self.assertEqual(self.abcDict, customHd.get_header_dict())
        
        self.assertEqual('a', customHd.get_header_dict()['a'])
        self.assertEqual('c', customHd.get_header_dict()['d'])
        
        self.assertEqual(self.abcDict, customHd.get_header_dict())
        
    def testParseHeader(self):
        
        self.assertEqual(('Dat210617', None), self.hd.parse_header('Dat210617'))
        self.assertEqual(('Dat011216V2', None), self.hd.parse_header('Dat011216V2'))
        
        self.assertEqual(('depth', 'm abs'), self.hd.parse_header('depth (m abs)'))
        self.assertEqual(('Cond', '+ALU-S/cm'), self.hd.parse_header('Cond (+ALU-S/cm)'))
        self.assertEqual(('Na', 'ppb'), self.hd.parse_header('Na (ppb)'))
        self.assertEqual(('Ca', 'ppb'), self.hd.parse_header('Ca (ppb)'))
        self.assertEqual(('Dust', 'part/ml'), self.hd.parse_header('Dust (part/ml)'))
        self.assertEqual(('NH4', 'ppb'), self.hd.parse_header('NH4 (ppb)'))
        
        # Test with some additional strange spacing
        self.assertEqual(('NO3', 'ppb'), self.hd.parse_header('NO3 (ppb)'))
        self.assertEqual(('NO3', 'ppb'), self.hd.parse_header('  NO3 (  ppb   )    '))
       

    def testParseHeaders(self):
        
        noHeaders = []
        
        testDict = {"test": "test" }
        testUnit = {"ppb" : "ppb"}
        
        testHeaderDict = HeaderDictionary(testDict, testUnit)
        
        self.assertEqual([], testHeaderDict.parse_headers(noHeaders))
        
        oneHeaderNoUnit = ['test']
        
        self.assertEqual([('test',None)], testHeaderDict.parse_headers(oneHeaderNoUnit))
        
        oneHeaderWithUnit = ['test (ppb)']
                
        self.assertEqual([('test','ppb')], testHeaderDict.parse_headers(oneHeaderWithUnit))
        
        oneHeaderWithUnitAndNotExisting = ['test (ppb)', 'test2 Not in (ppb)']
        
        self.assertEqual([('test','ppb'), None], testHeaderDict.parse_headers(oneHeaderWithUnitAndNotExisting))
        
        oneHeaderWithUnitAndNotExistingUnit = ['test (ppb)', 'test (not in unit)']
        
        self.assertEqual([('test','ppb'), ('test', None)], testHeaderDict.parse_headers(oneHeaderWithUnitAndNotExistingUnit))
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
