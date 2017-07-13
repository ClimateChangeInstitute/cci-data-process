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
        frame = get_data_frame_from_csv(os.path.join('..', 'KCC_210617', 'KCC_CFAmaster20170621_Part1.csv'))
        print(frame.columns)
        


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
