'''
Created on Jul 13, 2017

@author: Heather
'''
from math import isnan, nan
import os
import unittest
import warnings

from pandas.core.frame import DataFrame
from pandas.util.testing import assert_frame_equal

from climatechange.file import load_csv
from climatechange.headers import HeaderType
from climatechange.process_data_functions import clean_data, process_header_data
from climatechange.resampleStats import compileStats, compile_stats_by_year, \
    resampled_by_inc_years, find_index_by_increment, resampled_depths_by_years, \
    create_range_by_inc
from climatechange.resampleStats import findLen
from climatechange.resampleStats import findMax
from climatechange.resampleStats import findMean, create_depth_headers
from climatechange.resampleStats import findMedian
from climatechange.resampleStats import findMin
from climatechange.resampleStats import findStd
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
test_output = [[6.333333333333333, 0.94280904158206336,7.0, 7, 5,  3], [4.0,0.81649658092772603, 4.0, 5, 3,  3], [6.333333333333333,2.0548046676563256, 6.0, 9, 4,  3]]
# containingNoneArray = [[5.0, None, None, 2.0, 1.0],
#                        [2.0, None, None, 5.0, 6.0 ],
#                        [1.0, None, None, 5.0, 4.0]]
# containingNaNArray = [[5.0, nan, nan, 2.0, 1.0],
#                        [2.0, nan, nan, 5.0, 6.0 ],
#                        [1.0, nan, nan, 5.0, 4.0]]


class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

# test for all functions with same name
    def testfindMean(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.assertAlmostEqual([], findMean(emptyArray))
            self.assertAlmostEqual([4.0], findMean(singleRowArray))
            self.assertTrue(isnan(findMean(nanArray)[0]))
            self.assertAlmostEqual([3.0, 4.0, 3.0], findMean(multipleRowArray))
        
            str_input=[['f','r','6']]
            self.assertRaises(TypeError, findMean, str_input)

        
        # Maybe throw an error?
        # self.assertAlmostEqual([None, None, None], findMean(containingNoneArray))
        
        # Similarly what to do with nan values?
        # self.assertAlmostEqual([nan, nan, nan], findMean(containingNaNArray))
    
        # Also assume that 2D array is rectangular shape? No funny business. :-)
    
    def testfindMedian(self):     
            self.assertAlmostEqual([], findMedian(emptyArray))
            self.assertAlmostEqual([4.0], findMedian(singleRowArray))
            self.assertAlmostEqual([3.0, 4.0, 3.0], findMedian(multipleRowArray))
    
    def testfindMax(self):
            self.assertAlmostEqual([], findMax(emptyArray))
            self.assertAlmostEqual([5.0], findMax(singleRowArray))
            self.assertAlmostEqual([5.0, 6.0, 5.0], findMax(multipleRowArray))
    
    def testfindMin(self): 
            self.assertAlmostEqual([], findMin(emptyArray))
            self.assertAlmostEqual([3.0], findMin(singleRowArray))
            self.assertAlmostEqual([1.0, 2.0, 1.0], findMin(multipleRowArray))
    
    def testfindStd(self):
        self.assertAlmostEqual([], findStd(emptyArray))
        self.assertAlmostEqual([0.894427190999915860], findStd(singleRowArray))
        self.assertAlmostEqual([1.4142135623730951, 1.4142135623730951, 1.4142135623730951], findStd(multipleRowArray))

    def testfindLen(self):
        self.assertAlmostEqual([], findLen(emptyArray))
        self.assertAlmostEqual([5.0], findLen(singleRowArray))
        self.assertAlmostEqual([5.0, 5.0, 5.0], findLen(multipleRowArray))
 
    def testcompileStats(self):        
        self.assertAlmostEqual([], compileStats(emptyArray))
        self.assertAlmostEqual([[4, 0.89442719099991586, 4, 5, 3, 5]], compileStats(singleRowArray))
        self.assertAlmostEqual(test_output, compileStats(test_input))
        
    def testSmallcsv(self):
        small_output=[[2009.8, 1.0954451150103279, 2009.8, 2011.5999999999999, 2008.0, 19], 
         [2008.3999999999999, 2.1908902300206643, 2008.4000000000001, 2012.0, 2004.8, 19], 
         [0.5966279069999999, 0.0019106600718061043, 0.59662790700000001, 0.59976744199999998, 0.59348837200000004, 19], 
         [1.619, 0.0054772255750516448, 1.619, 1.6280000000000001, 1.6100000000000001, 19], 
         [9.0, 5.4772255750516612, 9.0, 18.0, 0.0, 19], 
         [41.0, 5.4772255750516612, 41.0, 50.0, 32.0, 19], 
         [6.3684210526315788, 4.1953674491325543, 4.0, 14.0, 2.0, 19], 
         [5.7894736842105265, 2.6072560161054392, 7.0, 9.0, 1.0, 19], 
         [4.3684210526315788, 1.086303549502647, 4.0, 6.0, 2.0, 19], 
         [5.3684210526315788, 1.086303549502647, 5.0, 7.0, 3.0, 19]]
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        self.assertAlmostEqual(small_output,
                               compileStats(frame.transpose().values.tolist()))
        
    def test_create_depth_headers(self):
        input_test=['depth (m we)','depth (m abs)']
        input_empty=[]
        expected_output=['top depth (m we)','bottom depth (m we)','top depth (m abs)','bottom depth (m abs)']
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
