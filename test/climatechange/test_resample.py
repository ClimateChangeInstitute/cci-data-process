'''
Created on Oct 18, 2017

@author: Heather
'''
import unittest
from pandas import DataFrame
import os
from pandas.util.testing import assert_frame_equal

from climatechange.headers import process_header_str
from climatechange.resample import resample,depth_columns, find_match, resample_by,\
    by_years, by_depths, create_range_for_depths, create_range_by_year

from climatechange.common_functions import DataClass, clean_data,\
    load_csv
    
    
# dc = DataClass(os.path.join('csv_files','input', 'small.csv'))
small_file = os.path.join('csv_files','input', 'small.csv')
dc = DataClass(small_file)
output_small_file = os.path.join('csv_files','output','Year_Dat210617_(CE)_resampled_by_1_year_resolution_for_mean.csv')
output_small_file2 = os.path.join('csv_files','output','Year_Dat210617_(CE)_resampled_by_2_year_resolution_for_mean.csv')
output_small_filem = os.path.join('csv_files','output','Year_Dat210617_(CE)_resampled_by_1_year_resolution_for_max_std.csv')
output_small_file_depth = os.path.join('csv_files','output','small_resample_by_0.001_depth_abs_(m)_mean.csv')
output_small_file_01 = os.path.join('csv_files','output','small_resample_by_0.01_depth_abs_(m)_max_count.csv')
input_test_zeros_and_numbers = clean_data(load_csv(os.path.join('csv_files', 'input_test_zeros_and_numbers.csv')))



output_by_LR = os.path.join('csv_files','output','resample_by_LR_output.csv')
f_HR = os.path.join('csv_files', 'test_input_dd_2.csv')
f_LR = os.path.join('csv_files', 'test_input_dd_1.csv')
dc_LR = DataClass(f_LR)
dc_HR = DataClass(f_HR)
depth_header, = process_header_str('depth (m abs)')
year_header,=process_header_str('Dat210617')
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass
    
    def test_resample(self):
        df = resample('y',small_file,['mean'],1,'Dat210617',False)
#         print(df)
        
  
    
    def test_depth_columns(self):
        expected_result = DataFrame([[0.59837,0.59977, 1.624, 1.628],[0.59663,0.59802,1.619,1.623],[0.59488,0.59628,1.614,1.618],[ 0.59349,0.59453,1.610,1.613]])
        expected_result.columns=['top_depth_we_(m)',  'bottom_depth_we_(m)',  'top_depth_abs_(m)','bottom_depth_abs_(m)']
        df= depth_columns(dc,'Dat210617',1)
        assert_frame_equal(df,expected_result)
        
    def test_by_years(self):

        
        df = by_years(dc,year_header,1,['mean'],year_header)
        expected_result = clean_data(load_csv(output_small_file))
        expected_result = expected_result.set_index('Year_Dat210617_(CE)')
        assert_frame_equal(df, expected_result)
         
        df2 = by_years(dc,year_header,2,['mean'],year_header)
        expected_result2 = clean_data(load_csv(output_small_file2))
        expected_result2 = expected_result2.set_index('Year_Dat210617_(CE)')
        assert_frame_equal(df2, expected_result2)
             
        dfm = by_years(dc,year_header,1,['max','std'],year_header)
        expected_resultm = clean_data(load_csv(output_small_filem))
        expected_resultm = expected_resultm.set_index('Year_Dat210617_(CE)')
        assert_frame_equal(dfm, expected_resultm)

    def test_by_depths(self):
        
        inc_amt = 0.001
        stat = ['mean']
        df = by_depths(dc,depth_header,inc_amt,stat)
        expected_result = clean_data(load_csv(output_small_file_depth))
        expected_result = expected_result.set_index(depth_header.label)
        assert_frame_equal(df, expected_result)
        
    def test_by_depths_01(self):
        inc_amt = 0.01
        stat = ['max','count']
        df = by_depths(dc,depth_header,inc_amt,stat)

        expected_result = clean_data(load_csv(output_small_file_01))
        expected_result = expected_result.set_index(depth_header.label)
        assert_frame_equal(df, expected_result)
        
    def test_create_range_for_depths(self):
        inc_amt = 0.01
        expected_result = [0.605, 0.615]
        input_test = load_csv(os.path.join('csv_files', 'input_depths.csv'))
        input_test = clean_data(input_test)
        result = create_range_for_depths(input_test.loc[:, 'depth (m we)'].values.tolist(), inc_amt)
        self.assertEqual(expected_result, result)
        
    def test_create_range_for_depths_2(self):
        inc_amt = 0.01
        expected_result = [1.64, 1.65, 1.66, 1.67, 1.68, 1.69]
        input_test = load_csv(os.path.join('csv_files', 'input_depths.csv'))
        input_test = clean_data(input_test)
        result = create_range_for_depths(input_test.loc[:, 'depth (m abs)'].values.tolist(), inc_amt)
        self.assertEqual(expected_result, result)
    
    def test_create_range_for_depths_inc(self):
        inc_amt = 0.005
        expected_result = [0.605, 0.610, 0.615, 0.620]
        input_test = load_csv(os.path.join('csv_files', 'input_depths.csv'))
        input_test = clean_data(input_test)
        result = create_range_for_depths(input_test.loc[:, 'depth (m we)'].values.tolist(), inc_amt)
        self.assertEqual(expected_result, result)
        
    def test_create_range_for_depths_inc_decimals(self):
        inc_amt = 0.0005
        expected_result = [0.6051, 0.6056, 0.6061, 0.6066, 0.6071, 0.6076, 0.6081, 0.6086, 0.6091, 0.6096]
        input_test = load_csv(os.path.join('csv_files', 'input_depth_decimal.csv'))
        input_test = clean_data(input_test)
        result = create_range_for_depths(input_test.loc[:, 'depth (m we) '].values.tolist(), inc_amt)
        self.assertEqual(expected_result, result)
    
    def test_create_range_by_inc(self):
        inc_amt = 1
        expected_output = [2011]
        result = create_range_by_year(input_test_zeros_and_numbers.loc[:, 'Dat210617'].values.tolist(), inc_amt)
        self.assertEqual(expected_output, result) 



    def test_resample_by(self):
        depth_header, = process_header_str('depth (m abs)')
        df =resample_by(f_HR,f_LR,['mean'],'depth (m abs)',False)
        expected_result = load_csv(os.path.join('csv_files','output','test_input_dd_2_depth_abs_(m)_resample_by_test_input_dd_1_mean.csv')).astype(float)
        expected_result = expected_result.set_index(depth_header.label)
        assert_frame_equal(df,expected_result)

        df2 =resample_by(f_HR,f_LR,['mean','std'],'depth (m abs)',False)
        expected_result2 = load_csv(os.path.join('csv_files','output','test_input_dd_2_resample_by_test_input_dd_1_depth_abs_(m)_mean_std.csv')).astype(float)
        expected_result2 = expected_result2.set_index(depth_header.label)
        assert_frame_equal(df2,expected_result2)
        

        df1 =resample_by(f_HR,f_LR,None,'depth (m abs)',False)
        expected_result1 = load_csv(os.path.join('csv_files','output','test_input_dd_2_depth_abs_(m)_resample_by_test_input_dd_1.csv')).astype(float)
        expected_result1 = expected_result1.set_index(depth_header.label)
        assert_frame_equal(df1,expected_result1)



    def test_find_match(self):
        depth_header_abs, = process_header_str('depth (m abs)')
        depth_header_we, = process_header_str('depth (m we)')
        result=find_match(dc_HR,dc_LR)
        self.assertEqual(result,[depth_header_we,depth_header_abs])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()