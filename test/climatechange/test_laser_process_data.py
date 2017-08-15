'''
Created on Aug 11, 2017

@author: Heather
'''
import unittest
import os
from climatechange.laser_data_process import load_input_file,\
    load_laser_txt_file, readFile, load_and_clean_LAICPMS_data,\
    process_laser_data_by_run, combine_laser_data_by_inputfile
from pandas.util.testing import assert_frame_equal
from pandas.core.frame import DataFrame
from climatechange.file import load_csv
from climatechange.headers import Header, HeaderType
from climatechange.compiled_stat import CompiledStat

laser_file=readFile('1.TXT', 955 , 6008.500 , 6012.500 , 12 , 23 )
depth_age_file='depthAge7617.txt'
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
        df=load_laser_txt_file(os.path.join('csv_files\\ignore_files','1_test.TXT',))
        rows=[['1.240000009536743', '2920.818115234375', '3386072.', '516.6666870117188', '1025.583374023438', '35386.66796875'], ['2.477999925613403', '2952.583251953125', '3232104.25', '491.75', '967.3333129882813', '43863.5'], ['3.717000007629395', '2986.', '3338235.75', '458.4166564941406', '842.0833129882813', '45258.16796875']]
        headers=['Time', 'Al27', 'Si28', 'Ca44', 'Fe56', 'S32']
        df_output=DataFrame(rows,columns=headers)
        assert_frame_equal(df_output,df)

    
    def test_load_input_file(self):
        result= load_input_file(os.path.join('csv_files\\ignore_files','InputFile_1.TXT'))
        self.assertEqual(laser_file.file_name, result[0].file_name)
        self.assertEqual(laser_file.laser_time, result[0].laser_time)
        self.assertEqual(laser_file.start_depth, result[0].start_depth)
        self.assertEqual(laser_file.end_depth, result[0].end_depth)
        self.assertEqual(laser_file.washin_time, result[0].washin_time)
        self.assertEqual(laser_file.washout_time, result[0].washout_time)
        
#     def test_combine_laser_data_by_inputfile(self):
#         input_file=os.path.join('csv_files\\ignore_files','InputFile_1.TXT')
#         df_original,df_filter=combine_laser_data_by_inputfile(input_file,depth_age_file)
#         print(df_original)
#         print(df_filter)
        
    def test_load_and_clean_LAICPMS_data(self):
        df=load_and_clean_LAICPMS_data(laser_file,depth_age_file,os.path.join('csv_files','ignore_files'))
        self.assertEqual(df.columns[0],'depth (m abs)')
        
#     def test_process_laser_data_by_run(self):
#         df_original,df_filter=process_laser_data_by_run(laser_file,depth_age_file,os.path.join('csv_files','ignore_files'))
#         
#         
        
    def test_add_year_column(self):
        df=load_and_clean_LAICPMS_data(laser_file,depth_age_file,os.path.join('csv_files','ignore_files'))
        self.assertEqual(df.columns[1],'year')

        
#     def test_store_background_information(self):
#         input_df=DataFrame([[1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3]],columns=['one','two','three'])
#         expected_result=DataFrame([[1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3],
#                       [1,2,3]],columns=['one','two','three'])
#         result=store_background_information(input_df)
#         assert_frame_equal(expected_result,result)
        
#     def test_compile_statistics_for_LAICPMS_data(self):
#         input_df = load_csv(os.path.join('csv_files','test_input_laser_stats.csv'))
#         output_df=DataFrame([[1,6,3.5,1.707825,3.5,6,1,6]], columns=['top_depth_we_(m)','bottom_depth_we_(m)','Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
#         expected_result=[CompiledStat(output_df,test_depth_we_header,test_sample_header)]
#         result=compile_statistics_for_LAICPMS_data(input_df)
#         assert_frame_equal(expected_result[0].df,result[0].df)
#         self.assertAlmostEqual(expected_result.sample_header.name,result.sample_header.name)
#         
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()