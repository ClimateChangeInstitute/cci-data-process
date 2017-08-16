'''
Created on Jul 31, 2017

@author: Heather
'''
import unittest
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from climatechange.file import load_csv
from climatechange.process_data_functions import clean_data,\
    correlate_samples, remove_nan_from_datasets
from climatechange.resample_data_by_depths import resampled_depths,create_range_for_depths,\
    find_index_by_increment_for_depths,resampled_by_inc_depths,compile_stats_by_depth,\
    compiled_stats_by_dd_intervals, find_index_of_depth_intervals
import os
from climatechange.resample_stats import create_depth_headers
from climatechange.headers import HeaderType, Header
import pandas
from pandas import Series
import warnings
from climatechange.compiled_stat import CompiledStat
import numpy as np
from pandas.testing import assert_series_equal
from climatechange.data_filters import replace_outliers_with_nan

test_sample_header=Header("Cond (+ALU-S/cm)", HeaderType.SAMPLE,"Conductivity","alu-s/cm","Cond_(+ALU-S/cm)")
test_depth_we_header=Header("depth (m we)", HeaderType.DEPTH,"Depth","meters","depth_we_(m)")
test_depth_abs_header=Header("depth (m abs) ", HeaderType.DEPTH,"Depth","meters","depth_abs_(m)")
x=[1,2,3,4,5]
y=[2,7,2,2,4]
expected_result = load_csv(os.path.join('csv_files','test_output_dd.csv'))
test_x_compiledstat=CompiledStat(DataFrame(x,columns=['Mean']),test_depth_we_header,test_sample_header)
test_y_compiledstat=CompiledStat(DataFrame(y,columns=['Mean']),test_depth_we_header,test_sample_header)
test_output_dd=CompiledStat(expected_result,test_depth_we_header,test_sample_header)

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
    
    def test_find_index_of_depth_intervals(self):
        larger_df = load_csv(os.path.join('csv_files','test_input_dd_2.csv'))
        smaller_df = load_csv(os.path.join('csv_files','test_input_dd_1.csv'))
        result=find_index_of_depth_intervals(larger_df.loc[:,'depth (m we)'],smaller_df.loc[:,'depth (m we)'])
        expected_result=[[1,2],[3,4],[5,6],[7,8],[9]]
        self.assertEqual(expected_result, result)
        
    def test_compile_stats_by_dd_intervals(self):
        larger_df = load_csv(os.path.join('csv_files','test_input_dd_2.csv'))
        smaller_df = load_csv(os.path.join('csv_files','test_input_dd_1.csv'))      
        compiled_stat_of_larger_df=compiled_stats_by_dd_intervals(larger_df,smaller_df)
        self.assertEqual(2, len(compiled_stat_of_larger_df))
        self.assertEqual(3, len(compiled_stat_of_larger_df[0]))
        assert_frame_equal(test_output_dd.df, compiled_stat_of_larger_df[0][0].df)
        self.assertEqual(test_output_dd.sample_header, compiled_stat_of_larger_df[0][0].sample_header)
        self.assertEqual(test_output_dd.x_header, compiled_stat_of_larger_df[0][0].x_header)
        
    def test_replace_outliers_with_nans(self):
        input_df=DataFrame([800000.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],columns=['Ca (ppb)'])
        output_result=DataFrame([np.nan,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],columns=['Ca (ppb)'])
        result=replace_outliers_with_nan(input_df)
        assert_frame_equal(output_result,result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()