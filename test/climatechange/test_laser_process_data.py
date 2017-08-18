'''
Created on Aug 11, 2017

@author: Heather
'''
import unittest
import os
from climatechange.laser_data_process import load_input_file,\
    load_laser_txt_file, readFile, combine_laser_data_by_input_file,\
    clean_LAICPMS_data, combine_laser_data_by_directory
from pandas.util.testing import assert_frame_equal
from pandas.core.frame import DataFrame
from climatechange.headers import Header, HeaderType
from climatechange.data_filters import normalize_min_max_scaler
import numpy

depth_age_file=os.path.join('csv_files','depthAge7617.txt')
laser_file=readFile(os.path.join('csv_files','1.txt'), 955 , 6008.500 , 6012.500 , 12 , 23,os.path.join('csv_files','depthAge7617.txt'))
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
    
    def test_load_laser_txt_file(self):
        df=load_laser_txt_file(os.path.join('csv_files','1_test.txt',))
        rows=[['13.1', '2920.818115', '3386072', '516.666687', '1025.583374', '35386.66797'],
              ['14.1', '2952.583252', '3232104.25', '491.75', '967.333313', '43863.5'],
              ['15.1', '2986', '3338235.75', '458.4166565', '842.083313', '45258.16797']]
        headers=['Time', 'Al27', 'Si28', 'Ca44', 'Fe56', 'S32']
        df_output=DataFrame(rows,columns=headers)
        assert_frame_equal(df_output,df)

    
    def test_load_input_file(self):
        result= load_input_file(os.path.join('csv_files','InputFile_1.txt'),depth_age_file)
        self.assertEqual(laser_file.file_path, result[0].file_path)
        self.assertEqual(laser_file.laser_time, result[0].laser_time)
        self.assertEqual(laser_file.start_depth, result[0].start_depth)
        self.assertEqual(laser_file.end_depth, result[0].end_depth)
        self.assertEqual(laser_file.washin_time, result[0].washin_time)
        self.assertEqual(laser_file.washout_time, result[0].washout_time)
        
    def test_combine_laser_data_by_input_file(self):
        input_file=os.path.join('csv_files','Input_File_test.txt')
        df=combine_laser_data_by_input_file(input_file,depth_age_file)
        self.assertEqual(1486, df.shape[0])
        self.assertEqual(7, df.shape[1])
        
                
    def test_load_and_clean_LAICPMS_data(self):
        df=clean_LAICPMS_data(laser_file)
        self.assertEqual(df.columns[0],'depth (m abs)') 
        
    def test_add_year_column(self):
        df=clean_LAICPMS_data(laser_file)
        self.assertEqual(df.columns[1],'year')
        
    def test_combine_laser_data_by_directory(self):
        directory=os.path.join('csv_files','test_directory')
        df_list=combine_laser_data_by_directory(directory,depth_age_file)
        self.assertEqual(2972, df_list[0].shape[0])
        self.assertEqual(7, df_list[0].shape[1])
        self.assertEqual(0, df_list[1].shape[0])
    
    def test_normalize_min_max_scaler(self):
        df=clean_LAICPMS_data(laser_file)
        min_Al_index=numpy.argmin(df.loc[:,'Al27'].values.tolist())
        min_S_index=numpy.argmin(df.loc[:,'S32'].values.tolist())
        df=normalize_min_max_scaler(df)
        self.assertEqual([min_Al_index],df[df['Al27'] == 0].index.tolist())
        self.assertEqual([min_S_index],df[df['S32'] == 0].index.tolist())
        self.assertEqual('depth (m abs)',df.iloc[:,:2].columns[0])
        self.assertEqual('year',df.iloc[:,:2].columns[1])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()