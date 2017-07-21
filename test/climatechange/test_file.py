'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import unittest

from climatechange.file import load_dictionary, load_csv, data_dir, save_dictionary


class Test(unittest.TestCase):

    def setUp(self):
        self.abcDict = { "a": "a", "b": "a", "c": "c", "d": "c", "e": "e"}
        pass


    def tearDown(self):
        pass

    def testLoadDictionary(self):
        
        file_name = os.path.join('json_files', 'nothing.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f), "Empty dictionary was expected")
         
        file_name = os.path.join('json_files', 'empty.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f), "Empty dictionary was expected")
        
        file_name = os.path.join('json_files', 'abcDict.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual(self.abcDict, load_dictionary(f), "%s dictionary does not match" % f)

    def testSaveDictionary(self):
        
        file_name = 'cci_test_file_delete_me.json'
        file_path = os.path.join(data_dir(), file_name)
        
        save_dictionary({}, file_path)
        with open(file_path, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f))
        os.remove(file_path)
        
        save_dictionary(self.abcDict, file_path)
        with open(file_path, 'r') as f:
            self.assertDictEqual(self.abcDict, load_dictionary(f))
        os.remove(file_path)

    def testReadCSVFile(self):
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        
        self.assertEqual('Dat210617', frame.columns[0], 'First column should be Dat210617')
        
        self.assertEqual(2009.8, frame.values[9][0], "Last value should be 2011.6986319241")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
