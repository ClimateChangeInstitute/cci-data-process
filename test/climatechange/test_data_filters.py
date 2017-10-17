'''
Created on Aug 18, 2017

:author: Mark Royer
'''
import math
import os
import unittest

import numpy
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from climatechange.data_filters import normalize_min_max_scaler, \
    replace_outliers, savgol_smooth_filter, filter_function, filters_to_string,\
    normalize_data, medfilt_filter,\
    wiener_filter, robust_scaler, default_filters
from climatechange.file import load_csv
from climatechange.process_data_functions import clean_data
from climatechange.laser import read_input, process_laser_data


depth_age_file = os.path.join('csv_files', 'depthAge7617.txt')
laser_file = read_input(os.path.join('csv_files', '1.txt'),
                    955 ,
                    6008.500 ,
                    6012.500 ,
                    12 ,
                    23)
test_filter_df = DataFrame([list(range(3)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(0, 3))])
test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
        

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_filters_to_string(self):
        
        def f1(df:DataFrame, x:int=1)->DataFrame:
            pass
        
        filters = {'f1': f1}
        
        result = filters_to_string(filters)
        
        self.assertEqual("f1(df:DataFrame, x:int=1)\n", result)
        
        # TODO: Add a few more tests
    
    def test_adding_filter_function(self):
        
        @filter_function('test_filter')
        def test_filter_function(df:DataFrame, val:int=1) -> DataFrame:
            pass # Do nothing
        
        self.assertTrue('test_filter' in filter_function.all)
        
    def test_replace_outliers(self):
         
        column_names = ['depth (m we)', 'Ca (ppb)']
        input_df = DataFrame([[800000., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
                              [800000., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]]).transpose()
        output_result = DataFrame([[800000., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
                                 [math.nan, 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]]).transpose()
        output_result.columns = column_names
        input_df.columns = column_names
         
        result = replace_outliers(input_df)
        assert_frame_equal(output_result, result)
     
    def test_normalize_min_max_scaler(self):
        df = process_laser_data(laser_file,depth_age_file)
        min_Al_index = numpy.argmin(df.loc[:, 'Al27'].values.tolist())
        min_S_index = numpy.argmin(df.loc[:, 'S32'].values.tolist())
        df = normalize_min_max_scaler(df)
        self.assertEqual([min_Al_index], df[df['Al27'] == 0].index.tolist())
        self.assertEqual([min_S_index], df[df['S32'] == 0].index.tolist())
        self.assertEqual('depth (m abs)', df.iloc[:, :2].columns[0])
        self.assertEqual('year', df.iloc[:, :2].columns[1])


#     def test_savgol_smooth_filter(self):
#         
#         df = DataFrame([list(range(3)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(0, 3))])
#         df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
#         
#         expected_df = DataFrame([[0, 1.385714, 2.385714],
#                                  [6, 5.457143, 6.457143],
#                                  [3, 6.314286, 7.314286],
#                                  [6, 5.457143, 6.457143],
#                                  [3, 5.028571, 6.028571],
#                                  [0, 0.742857, 1.742857]])
#         expected_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
#       
#         result_df = savgol_smooth_filter(df)
#         
#         assert_frame_equal(expected_df, result_df)

    def test_normalize_data(self):
        input_df = load_csv(os.path.join('csv_files', 'normalize_input.csv'))
        input_df=clean_data(input_df)
        result = normalize_data(input_df)
        expected_result = load_csv(os.path.join('csv_files', 'normalize_output.csv'))
        assert_frame_equal(expected_result,result)
        
        
        
    def test_medfilt_filter(self):
        test_filter_df = DataFrame([list(range(3)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(0, 3))])
        test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']

        result_df = medfilt_filter(test_filter_df)
        
        expected_df = DataFrame([[0, 1.0, 2.],
                                 [6, 4., 5.],
                                 [3, 7., 8.],
                                 [6, 4., 5.],
                                 [3, 4., 5.],
                                 [0, 1., 2.]])
        expected_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']

        assert_frame_equal(expected_df, result_df)
        
#     def test_cubic_filter(self):
#         test_filter_df = DataFrame([list(range(3)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(0, 3))])
#         test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
# 
#         result_df = cubic_spline_filter(test_filter_df)
#         print(result_df)
#         
#         expected_df = DataFrame([[0, 1.0, 2.],
#                                  [6, 4., 5.],
#                                  [3, 7., 8.],
#                                  [6, 4., 5.],
#                                  [3, 4., 5.],
#                                  [0, 1., 2.]])
#         expected_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']

#         assert_frame_equal(expected_df, result_df)
        
#     def test_spline_filter(self):
#         test_filter_df = DataFrame([list(range(3)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(0, 3))])
#         test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
#         result_df = spline_filter(test_filter_df)
# 
#         expected_df = DataFrame([[0, 1.0, 2.],
#                                  [6, 4., 5.],
#                                  [3, 7., 8.],
#                                  [6, 4., 5.],
#                                  [3, 4., 5.],
#                                  [0, 1., 2.]])
#         expected_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
#  
#         assert_frame_equal(expected_df, result_df)
        
#     def test_gauss_spline_filter(self):
#         test_filter_df = DataFrame([list(range(3)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(6, 9)),
#                         list(range(3, 6)),
#                         list(range(0, 3))])
#         test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
#         result_df = gauss_spline_filter(test_filter_df)
# 
#         expected_result = DataFrame([[0,1.541803e-01,1.712789e-03],
#                                  [6,8.295189e-33,  1.403461e-42],
#                                  [3, 2.608574e-11,  3.576248e-17],
#                                  [6,8.295189e-33,  1.403461e-42],
#                                  [3,2.608574e-11,  3.576248e-17],
#                                  [0, 1.541803e-01,  1.712789e-03]])
#         expected_result.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
# 
#         assert_frame_equal(expected_result, result_df)
    
    def test_wiener_filter(self):
        test_filter_df = DataFrame([list(range(3)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(0, 3))])
        test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
        result_df = wiener_filter(test_filter_df)

        expected_result = DataFrame([[0, 1.826873,  2.611111],
                                 [6,4.629630,  5.351852],
                                 [3, 6.000000,  7.000000],
                                 [6,5.000000,  6.000000],
                                 [3,4.000000,  5.000000],
                                 [0, 1.666667,  2.333333]])
        expected_result.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']

        assert_frame_equal(expected_result, result_df)
        
        
    def test_min_max_scaler(self):
        test_filter_df = DataFrame([list(range(3)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(0, 3))])

        test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
        result_df = normalize_min_max_scaler(test_filter_df)
        expected_result = DataFrame([[0,  0.0,   0.0],
                                 [6,1.0 ,  1.0],
                                 [3, 0.5,   0.5],
                                 [6,1.0,   1.0],
                                 [3,0.5,   0.5],
                                 [0, 0.0,   0.0]])
        expected_result.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']

        assert_frame_equal(expected_result, result_df)
        
            
    def test_robust_scaler(self):
        test_filter_df = DataFrame([list(range(3)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(6, 9)),
                        list(range(3, 6)),
                        list(range(0, 3))])

        test_filter_df.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']
        result_df = robust_scaler(test_filter_df)
        expected_result = DataFrame([[0, -0.666667,  -0.666667 ],
                                 [6,0.666667, 0.666667],
                                 [3, 0.,   0.],
                                 [6,0.666667,   0.666667],
                                 [3,0.,   0.],
                                 [0,-0.666667 ,-0.666667 ]])
        expected_result.columns = ['depth (m we)', 'Ca (ppb)', 'Al27']

        assert_frame_equal(expected_result, result_df)
        
    
        
        
    
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
