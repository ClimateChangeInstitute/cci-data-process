'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import pkg_resources
import unittest

from climatechange.headers import load_dictionary, HeaderDictionary


class Test(unittest.TestCase):

    abcDict = { "a": "a", "b": "a","c": "c", "d": "c", "e": "e"}

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testLoadDictionary(self):
        
        fileName = os.path.join('json_files','nothing.json')
        with open(fileName,'r') as f:
            self.assertDictEqual({}, load_dictionary(f), "Empty dictionary was expected")
         
        fileName = os.path.join('json_files','empty.json')
        with open(fileName, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f), "Empty dictionary was expected")
        
        fileName = os.path.join('json_files', 'abcDict.json')
        with open(fileName, 'r') as f:
            self.assertDictEqual(self.abcDict, load_dictionary(f), "%s dictionary does not match" % f)

    def testHeaderDictionaryCreation(self):
        
        hd = HeaderDictionary() # Should be the default header dictionaries
        
        with open(pkg_resources.resource_filename('climatechange','header_dict.json')) as file:  # @UndefinedVariable
            self.assertDictEqual(load_dictionary(file), hd.get_header_dict(), 'Header dictionaries do not match')
            
        with open(pkg_resources.resource_filename('climatechange','unit_dict.json')) as file:  # @UndefinedVariable
            self.assertDictEqual(load_dictionary(file), hd.get_unit_dict(), 'Unit dictionaries do not match')
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()