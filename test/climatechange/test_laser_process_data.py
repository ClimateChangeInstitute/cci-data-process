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


from climatechange.file import load_csv
from climatechange.process_data_functions import clean_data
from climatechange.laser import load_txt_file, read_input, load_input,\
    raw_LAICPMS_data, process_data



depth_age_file = os.path.join('csv_files', 'depthAge7617.txt')
laser_file = read_input(os.path.join('csv_files', '1.txt'), 955 , 6008.500 , 6012.500 , 12 , 23)
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
        self.assertEqual(laser_file.file_path, result[0].file_path)
        self.assertEqual(laser_file.laser_time, result[0].laser_time)
        self.assertEqual(laser_file.start_depth, result[0].start_depth)
        self.assertEqual(laser_file.end_depth, result[0].end_depth)
        self.assertEqual(laser_file.washin_time, result[0].washin_time)
        self.assertEqual(laser_file.washout_time, result[0].washout_time)
         
#     def test_clean_LAICPMS_data(self):
#         df = process_data(laser_file, depth_age_file)
#         expected_result=load_csv(os.path.join('csv_files', 'clean_LAICPMS_output.csv'))
#         self.assertEqual(df.columns[0], 'depth (m abs)')
#         self.assertEqual(df.columns[1], 'year')
#         assert_frame_equal(expected_result,df)
#         self.assertEqual(expected_result.shape[0],df.shape[0])
     

            
    def test_combine_laser_data_by_directory(self):
        directory = os.path.join('csv_files', 'test_directory')
        df_1,df_2 = raw_LAICPMS_data(directory, depth_age_file,False)
        self.assertEqual(2972, df_1.shape[0])
        self.assertEqual(6, df_1.shape[1])
        self.assertEqual(2972, df_2.shape[0])
        self.assertEqual(6, df_2.shape[1])
        



        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
