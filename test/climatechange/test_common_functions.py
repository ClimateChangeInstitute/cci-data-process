'''
Created on Oct 19, 2017

@author: Heather
'''
import unittest
from pandas.core.frame import DataFrame
from math import nan
from climatechange.common_functions import clean_data, index_by_increment,\
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
    
 
          
    def test_index_by_increment(self):
        inc_amt = 1
        expected_output = [list(range(0, 871, inc_amt))]
        range_list = create_range_by_year(input_test_zeros_and_numbers.loc[:, 'Dat210617'].values.tolist(), inc_amt)
        index = index_by_increment(input_test_zeros_and_numbers.loc[:, 'Dat210617'].values.tolist(), range_list)
        self.assertEqual(expected_output, index)
    
    def test_find_index_of_depth_intervals(self):
        larger_df = load_csv(os.path.join('csv_files', 'test_input_dd_2.csv'))
        smaller_df = load_csv(os.path.join('csv_files', 'test_input_dd_1.csv'))
        result = index_by_increment(larger_df.loc[:, 'depth (m we)'].values.tolist(), smaller_df.loc[:, 'depth (m we)'].values.tolist())
        expected_result = [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
        self.assertEqual(expected_result, result)
        

        
    def test_find_index_by_increment_for_depth(self):
        inc_amt = 0.01
        expected_result = [list(range(0, 29)), list(range(29, 56))]
        input_test = load_csv(os.path.join('csv_files', 'input_depths.csv'))
        input_test = clean_data(input_test)
        range_list = create_range_for_depths(input_test.loc[:, 'depth (m we)'].values.tolist(), inc_amt)
        result = index_by_increment(input_test.loc[:, 'depth (m we)'].values.tolist(), range_list)
        self.assertEqual(expected_result, result)
        
    def test_find_index_by_increment_with_blanks(self):
        list_to_inc = [1, 2, 6, 7, 8]
        range_list = [1, 3, 5, 7, 9]
        result= index_by_increment(list_to_inc, range_list)
        self.assertEqual([[0, 1], [2], [3, 4]], result)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()