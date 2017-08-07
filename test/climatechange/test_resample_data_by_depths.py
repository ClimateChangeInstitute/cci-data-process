'''
Created on Jul 31, 2017

@author: Heather
'''
import unittest
from pandas.core.frame import DataFrame
from pandas.util.testing import assert_frame_equal
from climatechange.file import load_csv
from climatechange.process_data_functions import process_header_data, clean_data
from climatechange.resample_data_by_depths import resampled_depths,create_range_for_depths,\
    find_index_by_increment_for_depths,resampled_by_inc_depths,compile_stats_by_depth
import os
from climatechange.resample_stats import create_depth_headers
from climatechange.headers import HeaderType, Header
import pandas
import warnings

test_sample_header=Header("Cond (+ALU-S/cm)", HeaderType.SAMPLE,"Conductivity","alu-s/cm","Cond_(+ALU-S/cm)")
test_depth_we_header=Header("depth (m we)", HeaderType.DEPTH,"Depth","meters","depth_we_(m)")
test_depth_abs_header=Header("depth (m abs) ", HeaderType.DEPTH,"Depth","meters","depth_abs_(m)")

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def test_create_range_for_depths(self):
        inc_amt=0.01
        expected_result=[0.605,0.615]
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        result=create_range_for_depths(input_test.loc[:,'depth (m we)'].values.tolist(),inc_amt)
        self.assertEqual(expected_result,result)
        
    def test_create_range_for_depths_2(self):
        inc_amt=0.01
        expected_result=[1.64,1.65,1.66,1.67,1.68,1.69]
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        result=create_range_for_depths(input_test.loc[:,'depth (m abs)'].values.tolist(),inc_amt)
        self.assertEqual(expected_result,result)
    
    def test_create_range_for_depths_inc(self):
        inc_amt=0.005
        expected_result=[0.605,0.610,0.615,0.620]
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        result=create_range_for_depths(input_test.loc[:,'depth (m we)'].values.tolist(),inc_amt)
        self.assertEqual(expected_result,result)
        
    def test_create_range_for_depths_inc_decimals(self):
        inc_amt=0.0005
        expected_result=[0.6051,0.6056,0.6061,0.6066,0.6071,0.6076,0.6081,0.6086,0.6091,0.6096]
        input_test = load_csv(os.path.join('csv_files','input_depth_decimal.csv'))
        input_test = clean_data(input_test)
        result=create_range_for_depths(input_test.loc[:,'depth (m we) '].values.tolist(),inc_amt)
        self.assertEqual(expected_result,result)
    
    def test_create_resample_depth_headers(self):
        expected_result=['top_depth_we_(m)','bottom_depth_we_(m)']
        input_test = load_csv(os.path.join('csv_files','input_depth_decimal.csv'))
        input_test = clean_data(input_test)
        headers = process_header_data(input_test)
        depth_headers = [h.name for h in headers if h.htype == HeaderType.DEPTH]
        result=create_depth_headers([test_depth_we_header])
        self.assertEqual(expected_result,result)
        
    def test_find_index_by_increment_for_depth(self):
        inc_amt=0.01
        expected_result=[list(range(0,29)),list(range(29,56))]
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        result=find_index_by_increment_for_depths(input_test.loc[:,'depth (m we)'].values.tolist(),inc_amt)
        self.assertEqual(expected_result,result)
    
    def test_resampled_depths(self):
        inc_amt=0.01
        expected_result = DataFrame([[0.605,0.615],[0.615,0.625]],columns=['top_depth_we_(m)', 'bottom_depth_we_(m)'])
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        df_x_sample=pandas.concat([input_test.loc[:,'depth (m we)'],input_test.loc[:,'Cond (+ALU-S/cm)']], axis=1)
        result=resampled_depths(df_x_sample,test_depth_we_header,inc_amt)
        assert_frame_equal(expected_result,result)
        
    def test_resampled_by_inc_depths(self):
        inc_amt=0.01
        expected_result=load_csv(os.path.join('csv_files','output_bydepth.csv'))
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        df_x_sample=pandas.concat([input_test.loc[:,'depth (m we)'],input_test.loc[:,'Cond (+ALU-S/cm)']], axis=1)
        result=resampled_by_inc_depths(df_x_sample,test_depth_we_header,inc_amt)
        assert_frame_equal(expected_result,result)
        
    def test_compile_stats_by_depth(self):
        input_test = load_csv(os.path.join('csv_files','input_depths.csv'))
        input_test = clean_data(input_test)
        expected_result = load_csv(os.path.join('csv_files','output_bydepth.csv'))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)   
            result = compile_stats_by_depth(input_test,test_depth_we_header, test_sample_header,0.01)
        assert_frame_equal(expected_result, result.df)
        
#     def test_append_compile_stats_by_depth(self):
#         df = load_csv(os.path.join('csv_files','input_depths.csv'))
#         headers = process_header_data(df)
#         df = clean_data(df)
#         depth_headers = [h.name for h in headers if h.htype == HeaderType.DEPTH]
#         sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
#         compiled_stats = []
#         inc_amt=0.01
#     
#         for depth_name in depth_headers:
#             for sample_name in sample_headers:
#                 compiled_stats.append(compile_stats_by_depth(df, depth_name, sample_name, inc_amt))
#         print(compiled_stats)
#         print(len(compiled_stats))
#         print(len(depth_headers))
#         print(len(sample_headers))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()