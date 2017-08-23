'''
Created on Jul 13, 2017

@author: Heather
'''
from math import nan
import os
import unittest
import warnings

from numpy.testing.utils import assert_almost_equal
from pandas import DataFrame
import pandas
from pandas.util.testing import assert_frame_equal

from climatechange.file import load_csv
from climatechange.headers import HeaderType, Header, process_header_data
from climatechange.laser_data_process import clean_LAICPMS_data, readFile
from climatechange.process_data_functions import clean_data, \
    load_and_clean_dd_data
from climatechange.resample_data_by_depths import find_index_by_increment
from climatechange.resample_stats import compileStats, compile_stats_by_year, resampled_depths_by_years, \
    create_range_by_year, create_depth_headers, resampled_statistics
import numpy as np


# list of values by column, first index is column index, for each you get element of row 
inc_amt = 1
emptyArray = [[]]
nanArray = [[np.NaN, np.nan, np.nan]]
singleRowArray = [5, 3, 4, 5, 3]
multipleRowArray = [[5.0, 4.0, 3.0, 2.0, 1.0],
                   [2.0, 3.0, 4.0, 5.0, 6.0 ],
                   [1.0, 3.0, 2.0, 5.0, 4.0]]
test_input = [[7, 5, 7], [3, 5, 4], [6, 4, 9]]
test_output = [[6.333333333333333, 0.94280904158206336, 7.0, 7, 5, 3],
               [4.0, 0.81649658092772603, 4.0, 5, 3, 3],
               [6.333333333333333, 2.0548046676563256, 6.0, 9, 4, 3]]


test_depth_we_header = Header("depth (m we)", HeaderType.DEPTH, "Depth", "meters", "depth_we_(m)")
test_sample_header = Header("Cond (+ALU-S/cm)", HeaderType.SAMPLE, "Conductivity", "alu-s/cm", "Cond_(+ALU-S/cm)")
test_year_header = Header("Dat210617", HeaderType.YEARS, "Years", "CE", "Year_Dat210617_(CE)")
input_test_zeros_and_numbers = load_csv(os.path.join('csv_files', 'input_test_zeros_and_numbers.csv'))
input_test_zeros_and_numbers = clean_data(input_test_zeros_and_numbers)

headers = process_header_data(input_test_zeros_and_numbers)
depth_column_headers = [ h for h in headers if h.htype == HeaderType.DEPTH ]
test_depth_column_headers_name = [ h.name for h in headers if h.htype == HeaderType.DEPTH ]
depth_columns = DataFrame([input_test_zeros_and_numbers.loc[:, c].values.tolist() for c in input_test_zeros_and_numbers.columns if c in test_depth_column_headers_name]).transpose()


input_test_zeros = load_csv(os.path.join('csv_files', 'input_test_zeros.csv'))
input_test_zeros = clean_data(input_test_zeros)
headers_zeros = process_header_data(input_test_zeros)

laser_file = readFile(os.path.join('csv_files', '1_test.txt'), 955 , 6008.500 , 6012.500 , 12 , 23, os.path.join('csv_files', 'depthAge7617.txt'))
laser_file_df = clean_LAICPMS_data(laser_file)


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

 
    def testcompileStats(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)        
#           assert_almost_equal([[]], compileStats(emptyArray))
            assert_almost_equal([4, 0.8944271, 4, 5, 3, 5], compileStats(singleRowArray))
            for i in range(len(test_input)):
                np.testing.assert_array_almost_equal(test_output[i], compileStats(test_input[i]))

                        
    def test_resample_statistics(self):
        df = DataFrame([5., 3., 4., 5., 3.], columns=["Cond (+ALU-S/cm)"])
        df = clean_data(df)
        df2 = DataFrame([5., 3., 4., 5., 3., 5., 3., 4., 5., 3.], columns=["Cond (+ALU-S/cm)"])
        index = [[0, 1, 2, 3, 4]]        
        index2 = [[0, 1, 2, 3, 4] , [5, 6, 7, 8, 9]]
        result = resampled_statistics(df, test_sample_header, index)
        expected_result = DataFrame([[4., 0.894427, 4., 5., 3., 5]], columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
        assert_frame_equal(expected_result, result)
    
        result2 = resampled_statistics(df2, test_sample_header, index2)
        expected_result2 = DataFrame([[4., 0.894427, 4., 5., 3., 5], [4., 0.894427, 4., 5., 3., 5]], columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
        assert_frame_equal(expected_result2, result2)
    
    def testSmallcsv(self):
        small_output = [[2009.8000000, 1.0954451, 2009.8000000, 2011.5999999, 2008.0000000, 19.0000000],
                      [2008.3999999, 2.1908902, 2008.4000000, 2012.0000000, 2004.8000000, 19.0000000],
                      [0000.5966279, 0.0019106, 0000.5966279, 0000.5997674, 0000.5934883, 19.0000000],
                      [0001.6190000, 0.0054772, 0001.6190000, 0001.6280000, 0001.6100000, 19.0000000],
                      [0009.0000000, 5.4772255, 0009.0000000, 0018.0000000, 0000.0000000, 19.0000000],
                      [0041.0000000, 5.4772255, 0041.0000000, 0050.0000000, 0032.0000000, 19.0000000],
                      [0006.3684210, 4.1953674, 0004.0000000, 0014.0000000, 0002.0000000, 19.0000000],
                      [0005.7894736, 2.6072560, 0007.0000000, 0009.0000000, 0001.0000000, 19.0000000],
                      [0004.3684210, 1.0863035, 0004.0000000, 0006.0000000, 0002.0000000, 19.0000000],
                      [0005.3684210, 1.0863035, 0005.0000000, 0007.0000000, 0003.0000000, 19.0000000]]
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        for i in range(len(small_output)):
            np.testing.assert_array_almost_equal(small_output[i],
                                                 compileStats(frame.iloc[:, i].values.tolist()))
        
    def test_create_depth_headers(self):
        input_test = [Header("depth (m we)", HeaderType.DEPTH, "Depth", "meters", "depth_we_(m)")]
        input_empty = []
        expected_output = ['top_depth_we_(m)',
                         'bottom_depth_we_(m)']
        result = create_depth_headers(input_test)
        result_empty = create_depth_headers(input_empty)
        self.assertListEqual(expected_output, result)
        self.assertListEqual([], result_empty)
        
    def test_clean_data(self):
        input_test = DataFrame([['str', 0, 1],
                              [4, 5, 6],
                              [7, 'str', 0]])
        expected_output = DataFrame([[nan, nan, 1],
                                   [4, 5, 6],
                                   [7, nan, nan]])
        result = clean_data(input_test)
        
        assert_frame_equal(expected_output, result)
    
    def test_load_and_clean_data(self):
        f = os.path.join('csv_files', 'test_load_and_clean_data.csv')
        df, headers = load_and_clean_dd_data(f)
        output_df = DataFrame([[1., 2., 3., 4.], [3., 4., 5., 6.]], columns=['depth (m we)', 'depth (m abs)', 'Na (ppb)', 'Ca (ppb)'])
        assert_frame_equal(output_df, df)

    def test_create_range_by_inc(self):
        expected_output = [2011]
        result = create_range_by_year(input_test_zeros_and_numbers.loc[:, 'Dat210617'].values.tolist(), inc_amt)
        self.assertEqual(expected_output, result)  
          
    def test_index_by_increment(self):
        expected_output = [list(range(0, 871, inc_amt))]
        range_list = create_range_by_year(input_test_zeros_and_numbers.loc[:, 'Dat210617'].values.tolist(), inc_amt)
        index, unused_top_range = find_index_by_increment(input_test_zeros_and_numbers.loc[:, 'Dat210617'].values.tolist(), range_list)
        self.assertEqual(expected_output, index)
    
    def test_resampled_depths_by_years(self):            
        expected_result = DataFrame([[0.593488372], [0.916582279], [1.61], [2.48]]).transpose()
        expected_result.columns = ['top_depth_we_(m)', 'bottom_depth_we_(m)', 'top_depth_abs_(m)', 'bottom_depth_abs_(m)']
        df_year_sample = pandas.concat([input_test_zeros_and_numbers.loc[:, test_year_header.name], input_test_zeros_and_numbers.loc[:, test_sample_header.name]], axis=1)
        range_list = create_range_by_year(df_year_sample.iloc[:, 0].values.tolist(), inc_amt)
        index, unused_top_range = find_index_by_increment(df_year_sample.iloc[:, 0].values.tolist(), range_list)       
        result = resampled_depths_by_years(index, depth_columns, depth_column_headers)
        assert_frame_equal(expected_result, result)
        
        
    def test_compile_stats_by_year(self):
        expected_result = load_csv(os.path.join('csv_files', 'output_test_zeros_and_numbers.csv')) 
        range_list = create_range_by_year(input_test_zeros_and_numbers.loc[:, test_year_header.name].values.tolist(), inc_amt)
        index, unused_top_range = find_index_by_increment(input_test_zeros_and_numbers.loc[:, test_year_header.name].values.tolist(), range_list)
        result = compile_stats_by_year(input_test_zeros_and_numbers, headers, test_year_header, test_sample_header, index, range_list, inc_amt)
        assert_frame_equal(expected_result, result.df)
        
    def test_empty_rows(self):

        expected_result = load_csv(os.path.join('csv_files', 'output_test_zeros.csv')) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            range_list = create_range_by_year(input_test_zeros.loc[:, test_year_header.name].values.tolist(), inc_amt)
            index, unused_top_range = find_index_by_increment(input_test_zeros.loc[:, test_year_header.name].values.tolist(), range_list)
            result = compile_stats_by_year(input_test_zeros, headers_zeros, test_year_header, test_sample_header, index, range_list)
        assert_frame_equal(expected_result, result.df)
         
    def test_partial_empty_rows(self):
        expected_result = load_csv(os.path.join('csv_files', 'output_test_zeros_and_numbers.csv'))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            range_list = create_range_by_year(input_test_zeros_and_numbers.loc[:, test_year_header.name].values.tolist(), inc_amt)
            index, unused_top_range = find_index_by_increment(input_test_zeros_and_numbers.loc[:, test_year_header.name].values.tolist(), range_list)
            result = compile_stats_by_year(input_test_zeros_and_numbers, headers, test_year_header, test_sample_header, index, range_list)
        assert_frame_equal(expected_result, result.df)
    
    def create_stats_headers(self):
        expected_result = load_csv(os.path.join('csv_files', 'output_test_zeros_and_numbers.csv'))   
        result = compile_stats_by_year(input_test_zeros_and_numbers, headers, test_year_header, test_sample_header)
        assert_frame_equal(expected_result.columns, result.columns) 
    
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
