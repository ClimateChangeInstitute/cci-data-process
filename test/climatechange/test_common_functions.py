'''
Created on Oct 19, 2017

@author: Heather
'''
import unittest
from pandas.core.frame import DataFrame
from math import nan
from climatechange.common_functions import clean_data,\
    load_csv
from pandas.util.testing import assert_frame_equal
from climatechange.resample import create_range_by_year, create_range_for_depths
import os

input_test_zeros_and_numbers = clean_data(load_csv(os.path.join('csv_files', 'input_test_zeros_and_numbers.csv')))
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass
    
    def test_clean_data(self):
        input_test = DataFrame([['str', 0, 1],
                              [4, 5, 6],
                              [7, 'str', 0]])
        expected_output = DataFrame([[nan, nan, 1],
                                   [4, 5, 6],
                                   [7, nan, nan]])
        result = clean_data(input_test)
        
        assert_frame_equal(expected_output, result)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()