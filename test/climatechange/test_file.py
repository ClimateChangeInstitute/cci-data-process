'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import unittest

from climatechange.file import load_dictionary, load_csv


class Test(unittest.TestCase):

    def setUp(self):
        self.abcDict = { "a": "a", "b": "a", "c": "c", "d": "c", "e": "e"}
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


    def testReadCSVFile(self):
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        
        self.assertEqual('Dat210617', frame.columns[0], 'First column should be Dat210617')
        
        self.assertEqual(2009.8, frame.values[9][0], "Last value should be 2011.6986319241")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
