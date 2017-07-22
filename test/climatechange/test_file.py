'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import unittest

from climatechange.file import load_dictionary, load_csv, data_dir, save_dictionary
from climatechange.headers import HeaderEncoder, to_headers


class Test(unittest.TestCase):

    def setUp(self):
        self.abc_dict = to_headers({"a": "Years",
                                  "b": "Years",
                                  "c": "Depth",
                                  "d": "Depth",
                                  "e": "Sample"})
        pass


    def tearDown(self):
        pass

    def testLoadDictionary(self):
        
        file_name = os.path.join('json_files', 'nothing.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual({},
                                 load_dictionary(f, obj_hook=to_headers),
                                 "Empty dictionary was expected")
         
        file_name = os.path.join('json_files', 'empty.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual({},
                                 load_dictionary(f, obj_hook=to_headers),
                                 "Empty dictionary was expected")
        
        file_name = os.path.join('json_files', 'abc_dict.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual(self.abc_dict,
                                 load_dictionary(f, obj_hook=to_headers),
                                 "%s dictionary does not match" % f)

    def testSaveDictionary(self):
        
        file_name = 'cci_test_file_delete_me.json'
        file_path = os.path.join(data_dir(), file_name)
        
        save_dictionary({}, file_path)
        with open(file_path, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f))
        os.remove(file_path)
        
        save_dictionary(self.abc_dict, file_path, enc_cls=HeaderEncoder)
        with open(file_path, 'r') as f:
            self.assertDictEqual(self.abc_dict, load_dictionary(f, obj_hook=to_headers))
        os.remove(file_path)
        
        save_dictionary(self.abc_dict, file_path, enc_cls=HeaderEncoder)
        with open(file_path, 'r') as f:
            self.assertDictEqual(self.abc_dict, load_dictionary(f, obj_hook=to_headers))
        os.remove(file_path)

    def testReadCSVFile(self):
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        
        self.assertEqual('Dat210617', frame.columns[0], 'First column should be Dat210617')
        
        self.assertEqual(2009.8, frame.values[9][0], "Last value should be 2011.6986319241")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
