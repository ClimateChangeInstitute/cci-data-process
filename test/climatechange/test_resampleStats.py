'''
Created on Jul 13, 2017

@author: Heather
'''
from math import isnan, nan
import os
import unittest
import warnings

from numpy.testing.utils import assert_almost_equal
from pandas.core.frame import DataFrame
from pandas.util.testing import assert_frame_equal

from climatechange.file import load_csv
from climatechange.headers import HeaderType
from climatechange.process_data_functions import clean_data, process_header_data
from climatechange.resample_stats import compileStats, compile_stats_by_year, \
    resampled_by_inc_years, find_index_by_increment, resampled_depths_by_years, \
    create_range_by_inc, findMean, findMedian, findMax, findMin, findStd, \
    findLen, create_depth_headers
import numpy as np
import pandas as pd


# list of values by column, first index is column index, for each you get element of row 
inc_amt=1
emptyArray = []
nanArray=[[np.NaN, np.nan, np.nan]]
singleRowArray = [[5, 3, 4, 5, 3]]
multipleRowArray = [[5.0, 4.0, 3.0, 2.0, 1.0],
                   [2.0, 3.0, 4.0, 5.0, 6.0 ],
                   [1.0, 3.0, 2.0, 5.0, 4.0]]
test_input = [[7, 5, 7], [3, 5, 4], [6, 4, 9]]
test_output = [[6.333333333333333, 0.94280904158206336,7.0, 7, 5,  3],
               [4.0,0.81649658092772603, 4.0, 5, 3,  3],
               [6.333333333333333,2.0548046676563256, 6.0, 9, 4,  3]]


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def testfindMean(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            assert_almost_equal([], findMean(emptyArray))
            assert_almost_equal([4.0], findMean(singleRowArray))
            self.assertTrue(isnan(findMean(nanArray)[0]))
            assert_almost_equal([3.0, 4.0, 3.0], findMean(multipleRowArray))
        
            str_input=[['f','r','6']]
            self.assertRaises(TypeError, findMean, str_input)
    
    def testfindMedian(self):     
            assert_almost_equal([], findMedian(emptyArray))
            assert_almost_equal([4.0], findMedian(singleRowArray))
            assert_almost_equal([3.0, 4.0, 3.0], findMedian(multipleRowArray))
    
    def testfindMax(self):
            assert_almost_equal([], findMax(emptyArray))
            assert_almost_equal([5.0], findMax(singleRowArray))
            assert_almost_equal([5.0, 6.0, 5.0], findMax(multipleRowArray))
    
    def testfindMin(self): 
            assert_almost_equal([], findMin(emptyArray))
            assert_almost_equal([3.0], findMin(singleRowArray))
            assert_almost_equal([1.0, 2.0, 1.0], findMin(multipleRowArray))
    
    def testfindStd(self):
        assert_almost_equal([], findStd(emptyArray))
        assert_almost_equal([0.8944271], findStd(singleRowArray))
        assert_almost_equal([1.4142135, 1.4142135, 1.4142135], findStd(multipleRowArray))

    def testfindLen(self):
        assert_almost_equal([], findLen(emptyArray))
        assert_almost_equal([5.0], findLen(singleRowArray))
        assert_almost_equal([5.0, 5.0, 5.0], findLen(multipleRowArray))
 
    def testcompileStats(self):        
        assert_almost_equal([], compileStats(emptyArray))
        assert_almost_equal([[4, 0.8944271, 4, 5, 3, 5]], compileStats(singleRowArray))
        assert_almost_equal(test_output, compileStats(test_input))
        
    def testSmallcsv(self):
        small_output=[[2009.8000000, 1.0954451, 2009.8000000, 2011.5999999, 2008.0000000, 19.0000000],
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
        assert_almost_equal(small_output, compileStats(frame.transpose().values.tolist()))
        
    def test_create_depth_headers(self):
        input_test=['depth (m we)','depth (m abs)']
        input_empty=[]
        expected_output=['top depth (m we)',
                         'bottom depth (m we)',
                         'top depth (m abs)',
                         'bottom depth (m abs)']
        result=create_depth_headers(input_test)
        result_empty=create_depth_headers(input_empty)
        self.assertListEqual(expected_output, result)
        self.assertListEqual([],result_empty)
        
    def test_clean_data(self):
        input_test=DataFrame([['str', 0, 1],
                              [4, 5, 6],
                              [7, 'str', 0]])
        expected_output=DataFrame([[nan, nan, 1],
                                   [4, 5, 6],
                                   [7, nan, nan]])
        result=clean_data(input_test)
        
        assert_frame_equal(expected_output, result)
    
    
    def test_create_range_by_inc(self):
        expected_output=[2011]
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        input_test = clean_data(input_test)
        result=create_range_by_inc(input_test.loc[:,'Dat210617'].values.tolist(),inc_amt)
        self.assertEqual(expected_output,result)  
          
    def test_index_by_increment(self):
        expected_output=[list(range(0,871,inc_amt))]
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        index=find_index_by_increment(input_test.loc[:,'Dat210617'].values.tolist(), inc_amt)
        self.assertEqual(expected_output, index)
    
    def test_resampled_depths_by_years(self):      
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        input_test = clean_data(input_test)
        
        headers = process_header_data(input_test)
        depth_column_headers = [ h.name for h in headers if h.htype == HeaderType.DEPTH ]
        depth_columns=DataFrame([input_test.loc[:,c].values.tolist() for c in input_test.columns if c in depth_column_headers]).transpose()
        expected_result=DataFrame([[0.593488372],[0.916582279],[1.61],[2.48]]).transpose()
        expected_result.columns=['top depth (m we) ','bottom depth (m we) ','top depth (m abs)','bottom depth (m abs)']
        df_year_sample=pd.concat([input_test.loc[:,'Dat210617'], input_test.loc[:,'Cond (+ALU-S/cm)']], axis=1)
        index=find_index_by_increment(df_year_sample.iloc[:,0].values.tolist(),inc_amt)       
        result=resampled_depths_by_years(index, depth_columns, depth_column_headers)
        assert_frame_equal(expected_result,result)
        
    def test_resampled_by_inc_years(self): 
        expected_result = load_csv(os.path.join('csv_files','output_test_zeros_and_numbers.csv')) 
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        input_test=clean_data(input_test)
        headers = process_header_data(input_test)
        depth_column_headers = [ h.name for h in headers if h.htype == HeaderType.DEPTH ]
        depth_columns=DataFrame([input_test.loc[:,c].values.tolist() for c in input_test.columns if c in depth_column_headers]).transpose()
        df_year_sample=pd.concat([input_test.loc[:,'Dat210617'], input_test.loc[:,'Cond (+ALU-S/cm)']], axis=1)
        result=resampled_by_inc_years(df_year_sample,'Dat210617',depth_columns,depth_column_headers,inc_amt)
        assert_frame_equal(expected_result, result)
        
    def test_compile_stats_by_year(self):
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        input_test=clean_data(input_test)
        expected_result = load_csv(os.path.join('csv_files','output_test_zeros_and_numbers.csv')) 
        headers = process_header_data(input_test)
        result=compile_stats_by_year(input_test, headers, 'Dat210617', 'Cond (+ALU-S/cm)', inc_amt)
        assert_frame_equal(expected_result, result.df)
        
    def test_empty_rows(self):

        expected_result = load_csv(os.path.join('csv_files','output_test_zeros.csv')) 
        input_test = load_csv(os.path.join('csv_files','input_test_zeros.csv'))
        input_test = clean_data(input_test)
        headers = process_header_data(input_test)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            result = compile_stats_by_year(input_test, headers, 'Dat210617', 'Cond (+ALU-S/cm)')
        assert_frame_equal(expected_result, result.df)
         
    def test_partial_empty_rows(self):
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        input_test = clean_data(input_test)
        expected_result = load_csv(os.path.join('csv_files','output_test_zeros_and_numbers.csv'))   
        headers = process_header_data(input_test)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            result = compile_stats_by_year(input_test, headers, 'Dat210617', 'Cond (+ALU-S/cm)')
        assert_frame_equal(expected_result, result.df)
    
    def create_stats_headers(self):
        input_test = load_csv(os.path.join('csv_files','input_test_zeros_and_numbers.csv'))
        input_test = clean_data(input_test)
        expected_result = load_csv(os.path.join('csv_files','output_test_zeros_and_numbers.csv'))   
        headers = process_header_data(input_test)
        result = compile_stats_by_year(input_test, headers, 'Dat210617', 'Cond (+ALU-S/cm)')
        assert_frame_equal(expected_result.columns, result.columns)     
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
