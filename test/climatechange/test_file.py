'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import unittest

from climatechange.file import get_data_frame_from_csv


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testReadCSVFile(self):
        frame = get_data_frame_from_csv(os.path.join('csv_files', 'small.csv'))
        print(frame.columns)
        
        self.assertEqual('Dat210617', frame.columns[0], 'First column should be Dat210617')
        
        self.assertEqual(2011.6986319241, frame.values[9][0], "Last value should be 2011.6986319241")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
