'''
Created on Jul 31, 2017

@author: Heather
'''
import unittest
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from climatechange.file import load_csv
from climatechange.process_data_functions import process_header_data, clean_data,\
    correlate_samples, remove_nan_from_datasets
from climatechange.resample_data_by_depths import resampled_depths,create_range_for_depths,\
    find_index_by_increment_for_depths,resampled_by_inc_depths,compile_stats_by_depth
import os
from climatechange.resample_stats import create_depth_headers
from climatechange.headers import HeaderType, Header
import pandas
from pandas import Series
import warnings
from climatechange.compiled_stat import CompiledStat
import numpy as np
from pandas.testing import assert_series_equal

test_sample_header=Header("Cond (+ALU-S/cm)", HeaderType.SAMPLE,"Conductivity","alu-s/cm","Cond_(+ALU-S/cm)")
test_depth_we_header=Header("depth (m we)", HeaderType.DEPTH,"Depth","meters","depth_we_(m)")
test_depth_abs_header=Header("depth (m abs) ", HeaderType.DEPTH,"Depth","meters","depth_abs_(m)")
x=[1,2,3,4,5]
y=[2,7,2,2,4]
test_x_compiledstat=CompiledStat(DataFrame(x,columns=['Mean']),test_depth_we_header,test_sample_header)
test_y_compiledstat=CompiledStat(DataFrame(y,columns=['Mean']),test_depth_we_header,test_sample_header)

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
        index_to_remove=[]
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
        
#     def test_remove_index_if_less_than_one(self):
#         inc_amt=0.001
#         input_test = load_csv(os.path.join('csv_files','input_depth_index.csv'))
#         expected_result = load_csv(os.path.join('csv_files','output_depth_index.csv'))
#         input_test = clean_data(input_test)
#         print(expected_result)
#         df_x_sample=pandas.concat([input_test.loc[:,'depth (m abs)'],input_test.loc[:,'Cond (+ALU-S/cm)']], axis=1)
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore", category=RuntimeWarning)  
#             result=resampled_by_inc_depths(df_x_sample,test_depth_abs_header,inc_amt)
#         print(result)
#         assert_frame_equal(expected_result, result)
#         
        
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

    def test_correlate_samples(self):
        depth1,sample1,sample2,slope_r, intercept_r, r_value_r, p_value_r, std_err_r=correlate_samples(test_x_compiledstat,test_y_compiledstat)
        slope=-0.1
        d1='Cond (+ALU-S/cm)'
        d2='Cond (+ALU-S/cm)'
        depth='depth (m we)'
        r_value=-0.07216878364870323
        p_value=0.908191677213
        intercept=3.7
        std_err=0.797913946906
        self.assertAlmostEqual(slope_r, slope)
        self.assertAlmostEqual(intercept_r, intercept)
        self.assertAlmostEqual(r_value_r,r_value)
        self.assertAlmostEqual(p_value_r, p_value)
        self.assertAlmostEqual(std_err_r, std_err)
        self.assertAlmostEqual(sample1, d1)
        self.assertAlmostEqual(sample2, d2)
        self.assertAlmostEqual(depth1, depth)
    
    def test_correlate_samples_opposite(self):
        depth1,sample1,sample2,slope_r, intercept_r, r_value_r, p_value_r, std_err_r=correlate_samples(test_y_compiledstat,test_x_compiledstat)
        slope=-0.0520833333333
        d1='Cond (+ALU-S/cm)'
        d2='Cond (+ALU-S/cm)'
        depth='depth (m we)'
        r_value=-0.07216878364870323
        p_value=0.908191677213
        intercept=3.17708333333
        std_err=0.41558018068
        self.assertAlmostEqual(slope_r, slope)
        self.assertAlmostEqual(intercept_r, intercept)
        self.assertAlmostEqual(r_value_r,r_value)
        self.assertAlmostEqual(p_value_r, p_value)
        self.assertAlmostEqual(std_err_r, std_err)
        self.assertAlmostEqual(sample1, d1)
        self.assertAlmostEqual(sample2, d2)
        self.assertAlmostEqual(depth1, depth)
    
    
    def test_remove_nan_from_datasets(self):
        input1=Series([1,2,3,4,np.nan,6,7])
        input2=Series([1,np.nan,3,4,5,6,np.nan])
        expected_result=Series([1.0,3.0,4.0,6.0])
        result1,result2=remove_nan_from_datasets(input1,input2)
        assert_series_equal(expected_result,result1)
        assert_series_equal(expected_result,result2)
        

#     def test_compile_stats_by_dd_intervals(self):
#         input_test1 = load_csv(os.path.join('csv_files','test_input_dd_1.csv'))
#         input_test2 = load_csv(os.path.join('csv_files','test_input_dd_2.csv'))
#         expected_result = load_csv(os.path.join('csv_files','test_output_dd.csv'))
#         compiled_stat_small_inc=compile_stats_by_dd_intervals(input_test1,input_test2)
#         
#         
#         



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()