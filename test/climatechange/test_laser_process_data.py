'''
Created on Aug 11, 2017

@author: Heather
'''
import os
import unittest

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from climatechange.headers import Header, HeaderType

from climatechange.laser import load_txt_file, read_input, load_input, raw_data,\
    add_year_column, add_depth_column, process_laser_data, resample_laser_by,\
    resample_data, run_data
from climatechange.common_functions import clean_data, load_csv, to_csv



depth_age_file = os.path.join('csv_files', 'depthAge7617.txt')
f= read_input(os.path.join('csv_files', '1.txt'), 955 , 6008.500 , 6012.500 , 12 , 23)
test_sample_header = Header("Cond (+ALU-S/cm)", HeaderType.SAMPLE, "Conductivity", "alu-s/cm", "Cond_(+ALU-S/cm)")
test_depth_we_header = Header("depth (m we)", HeaderType.DEPTH, "Depth", "meters", "depth_we_(m)")
test_depth_abs_header = Header("depth (m abs) ", HeaderType.DEPTH, "Depth", "meters", "depth_abs_(m)")
test_process_laser= os.path.join('csv_files','output','process_laser_data_test.csv')
                 
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass
    
    def test_load_txt_file(self):
        df = load_txt_file(os.path.join('csv_files', '1_test.txt',))
        rows = [['13.1', '2920.818115', '3386072', '516.666687', '1025.583374', '35386.66797'],
              ['14.1', '2952.583252', '3232104.25', '491.75', '967.333313', '43863.5'],
              ['15.1', '2986', '3338235.75', '458.4166565', '842.083313', '45258.16797']]
        headers = ['Time', 'Al27', 'Si28', 'Ca44', 'Fe56', 'S32']
        df_output = DataFrame(rows, columns=headers)
        assert_frame_equal(df_output, df)

    
    def test_read_input(self):
        result = load_input(os.path.join('csv_files', 'InputFile_1.txt'))
        self.assertEqual(f.file_path, result[0].file_path)
        self.assertEqual(f.laser_time, result[0].laser_time)
        self.assertEqual(f.start_depth, result[0].start_depth)
        self.assertEqual(f.end_depth, result[0].end_depth)
        self.assertEqual(f.washin_time, result[0].washin_time)
        self.assertEqual(f.washout_time, result[0].washout_time)
         
    def test_clean_LAICPMS_data(self):
        df = process_laser_data(f, depth_age_file)
#         to_csv(f.dirname,df,'process_laser_data_test.csv',False)
        expected_result=load_csv(test_process_laser)
        self.assertEqual(df.columns[0], 'depth (m abs)')
        self.assertEqual(df.columns[1], 'year')
        assert_frame_equal(expected_result,df)
        self.assertEqual(expected_result.shape[0],df.shape[0])
       
    def test_add_year_column(self):
        df = clean_data(f.raw_data)
        df = df[(df['Time'] > f.washin_time) & (df['Time'] < f.laser_time - f.washout_time)]
        df = df.reset_index(drop=True)
        df = df.drop('Time', 1)
        df = add_depth_column(df, f.start_depth_m, f.end_depth_m)
        df = add_year_column(df,depth_age_file)
        self.assertEqual(df.columns[1], 'year')
        df=df.round(5)
        
        expected_result=load_csv(test_process_laser)
        self.assertEqual(df.columns[0], 'depth (m abs)')
        
        assert_frame_equal(expected_result,df)
            
    def test_raw_data(self):
        directory = os.path.join('csv_files', 'test_directory')
        df_1,df_2 = raw_data(directory, depth_age_file,'KCC',False)
        self.assertEqual(2972, df_1.shape[0])
        self.assertEqual(6, df_1.shape[1])
        self.assertEqual(2972, df_2.shape[0])
        self.assertEqual(6, df_2.shape[1])
        
    def test_resample_laser_by(self):
        directory = os.path.join('csv_files', 'test_directory')
        by = os.path.join('csv_files','KCC_CFA.csv')
        df_1,df_2 = resample_data(directory, by,depth_age_file,'KCC','depth (m abs)',False)
        self.assertEqual(156, df_1.shape[0])
        self.assertEqual(6, df_1.shape[1])
        self.assertEqual(156, df_2.shape[0])
        self.assertEqual(6, df_2.shape[1])
        
    def test_run_data(self):
        directory = os.path.join('csv_files', 'test_directory')
        df_1,df_2 = run_data(directory,depth_age_file,'KCC','depth (m abs)',True)
        self.assertEqual(4, df_1.shape[0])
        self.assertEqual(11, df_1.shape[1])
        self.assertEqual(4, df_2.shape[0])
        self.assertEqual(11, df_2.shape[1])
         
        



        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
