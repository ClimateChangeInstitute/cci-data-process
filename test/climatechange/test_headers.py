'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import pkg_resources
import unittest

from climatechange.headers import load_dictionary, HeaderDictionary


abcDict = { "a": "a", "b": "a", "c": "c", "d": "c", "e": "e"}

class Test(unittest.TestCase):


    def setUp(self):
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
            self.assertDictEqual(abcDict, load_dictionary(f), "%s dictionary does not match" % f)

    def testHeaderDictionaryCreation(self):
        
        hd = HeaderDictionary()  # Should be the default header dictionaries
        
        with open(pkg_resources.resource_filename('climatechange', 'header_dict.json')) as file:  # @UndefinedVariable
            self.assertDictEqual(load_dictionary(file), hd.get_header_dict(), 'Header dictionaries do not match')
            
        with open(pkg_resources.resource_filename('climatechange', 'unit_dict.json')) as file:  # @UndefinedVariable
            self.assertDictEqual(load_dictionary(file), hd.get_unit_dict(), 'Unit dictionaries do not match')
        
        hd = HeaderDictionary(abcDict, abcDict)
        
        self.assertEqual(abcDict, hd.get_header_dict())
        
        self.assertEqual('a', hd.get_header_dict()['a'])
        self.assertEqual('c', hd.get_header_dict()['d'])
        
        self.assertEqual(abcDict, hd.get_header_dict())
        
    def testParseHeader(self):

        hd = HeaderDictionary()  # Default header dictionary
        
        self.assertEqual(('Dat210617', None), hd.parse_header('Dat210617'))
        self.assertEqual(('Dat011216V2', None), hd.parse_header('Dat011216V2'))
        
        self.assertEqual(('depth', 'm abs'), hd.parse_header('depth (m abs)'))
        self.assertEqual(('Cond', '+ALU-S/cm'), hd.parse_header('Cond (+ALU-S/cm)'))
        self.assertEqual(('Na', 'ppb'), hd.parse_header('Na (ppb)'))
        self.assertEqual(('Ca', 'ppb'), hd.parse_header('Ca (ppb)'))
        self.assertEqual(('Dust', 'part/ml'), hd.parse_header('Dust (part/ml)'))
        self.assertEqual(('NH4', 'ppb'), hd.parse_header('NH4 (ppb)'))
        
        # Test with some additional strange spacing
        self.assertEqual(('NO3', 'ppb'), hd.parse_header('NO3 (ppb)'))
        self.assertEqual(('NO3', 'ppb'), hd.parse_header('  NO3 (  ppb   )    '))
       

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
