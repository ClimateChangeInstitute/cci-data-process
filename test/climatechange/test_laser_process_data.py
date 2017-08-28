'''
Created on Aug 11, 2017

@author: Heather
'''
import os
import unittest

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal, assert_almost_equal,\
    assert_series_equal

from climatechange.headers import Header, HeaderType
from climatechange.laser_data_process import load_input_file, \
    load_laser_txt_file, readFile, combine_laser_data_by_input_file, \
    clean_LAICPMS_data, combine_laser_data_by_directory
from climatechange.resample_stats import compileStats
from climatechange.data_filters import adjust_data_by_background,\
    adjust_data_by_stats
from climatechange.plot import write_data_to_csv_files
from climatechange.file import load_csv
from climatechange.process_data_functions import clean_data


depth_age_file = os.path.join('csv_files', 'depthAge7617.txt')
laser_file = readFile(os.path.join('csv_files', '1.txt'), 955 , 6008.500 , 6012.500 , 12 , 23, os.path.join('csv_files', 'depthAge7617.txt'))
test_sample_header = Header("Cond (+ALU-S/cm)", HeaderType.SAMPLE, "Conductivity", "alu-s/cm", "Cond_(+ALU-S/cm)")
test_depth_we_header = Header("depth (m we)", HeaderType.DEPTH, "Depth", "meters", "depth_we_(m)")
test_depth_abs_header = Header("depth (m abs) ", HeaderType.DEPTH, "Depth", "meters", "depth_abs_(m)")

                 
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass
    
    def test_load_laser_txt_file(self):
        df = load_laser_txt_file(os.path.join('csv_files', '1_test.txt',))
        rows = [['13.1', '2920.818115', '3386072', '516.666687', '1025.583374', '35386.66797'],
              ['14.1', '2952.583252', '3232104.25', '491.75', '967.333313', '43863.5'],
              ['15.1', '2986', '3338235.75', '458.4166565', '842.083313', '45258.16797']]
        headers = ['Time', 'Al27', 'Si28', 'Ca44', 'Fe56', 'S32']
        df_output = DataFrame(rows, columns=headers)
        assert_frame_equal(df_output, df)

    
    def test_load_input_file(self):
        result = load_input_file(os.path.join('csv_files', 'InputFile_1.txt'), depth_age_file)
        self.assertEqual(laser_file.file_path, result[0].file_path)
        self.assertEqual(laser_file.laser_time, result[0].laser_time)
        self.assertEqual(laser_file.start_depth, result[0].start_depth)
        self.assertEqual(laser_file.end_depth, result[0].end_depth)
        self.assertEqual(laser_file.washin_time, result[0].washin_time)
        self.assertEqual(laser_file.washout_time, result[0].washout_time)
        
    def test_combine_laser_data_by_input_file(self):
        input_file = os.path.join('csv_files', 'Input_File_test.txt')
        comb_laser = combine_laser_data_by_input_file(input_file, depth_age_file)
        self.assertEqual(1486, comb_laser.df.shape[0])
        self.assertEqual(7, comb_laser.df.shape[1])
        
    def test_clean_LAICPMS_data(self):
        df = clean_LAICPMS_data(laser_file)
        expected_result=load_csv(os.path.join('csv_files', 'clean_LAICPMS_output.csv'))
        expected_result=clean_data(expected_result)
        self.assertEqual(df.columns[0], 'depth (m abs)')
        self.assertEqual(df.columns[1], 'year')
        assert_frame_equal(expected_result,df)
        self.assertEqual(expected_result.shape[0],df.shape[0])
    
    def test_adjust_data_by_mean(self):
        df=load_csv(os.path.join('csv_files', 'adjust_mean_input.csv'))
        df_stats=DataFrame({i:compileStats(df[i].tolist()) for i in df.columns[2:]},
                    index=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
        result=adjust_data_by_stats(df,df_stats)
        expected_result=load_csv(os.path.join('csv_files', 'adjust_mean_output.csv'))
        assert_frame_equal(expected_result,result)
            
    def test_combine_laser_data_by_directory(self):
        directory = os.path.join('csv_files', 'test_directory')
        df_1,df_2 = combine_laser_data_by_directory(directory, depth_age_file)
        self.assertEqual(2972, df_1.shape[0])
        self.assertEqual(7, df_1.shape[1])
        self.assertEqual(2972, df_2.shape[0])
        self.assertEqual(7, df_2.shape[1])
        
#     def test_laser_file(self):
#         self.assertEqual(laser_file.file_path,laser_file)
        
    def test_laser_file_background_info(self):
        result=laser_file.background_stats
        x=DataFrame({i:compileStats(laser_file.raw_data.loc[0:12, i].tolist()) for i in laser_file.raw_data.iloc[0:13, 1:]},
                    index=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
        assert_frame_equal(x, result)

    def test_laser_file_stats(self):
        result=laser_file.stats
        x=DataFrame({i:compileStats(laser_file.processed_data[i].tolist()) for i in laser_file.processed_data.columns[2:]},
                    index=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
        assert_frame_equal(x, result)
        
    def test_adjust_laser_file_by_background(self):
        bg_stats=laser_file.background_stats
        proc_data=laser_file.processed_data.copy()
        df_output=adjust_data_by_background(laser_file.processed_data,laser_file.background_stats)
        self.assertEqual(df_output.iloc[0,2],proc_data.iloc[0,2]-bg_stats.loc['Mean','Al27'])    

#     def test_plot_data_filters(self):
#         
#         
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
