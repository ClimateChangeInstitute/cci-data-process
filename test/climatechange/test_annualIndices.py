'''
Created on Jul 18, 2017

@author: Heather
'''
import unittest

from climatechange.resampleStats import create_range_by_inc
from climatechange.resampleStats import find_indices
from climatechange.resampleStats import find_index_by_increment
from climatechange.resampleStats import resampled_years
from climatechange.resampleStats import resampled_depths_by_years
from climatechange.resampleStats import resampled_statistics_by_years
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from climatechange.file import load_csv
import pandas as pd
from anaconda_project.internal.conda_api import result
 
frame = load_csv('/Users/Heather/Documents/GitHub/cci-data-process/test/csv_files/small.csv')
out_frame= load_csv('/Users/Heather/Documents/GitHub/cci-data-process/test/csv_files/output_test_small.Dat210617.Na(ppb).csv')
lst=frame.transpose().values.tolist()
years=frame.loc[:,'Dat210617']
data=frame.loc[:,'Na (ppb)']
resamp_years=[2008,2009,2010,2011]

df_year_sample=pd.concat([years, data], axis=1)


index=[[0,1],[2,3,4]]
expected_depth_columns=[[1,2,2,3],[3,5,4,6]]



depth_column_headers=['depth (m we)','depth (m abs)']
expected_depth_column_headers=['top depth (m we)','bottom depth (m we)','top depth (m abs)','bottom depth (m abs)']
inc_amt=1
yc='Year'


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def test_create_range_by_inc(self):
        j=create_range_by_inc(years,inc_amt)
        self.assertEqual(resamp_years,j)

    def test_find_indices(self):
        lst=[0,3,5,6,7,20]
        #find indices of the specific condition called
        t=find_indices(lst,lambda e: e>10)
        self.assertEqual([5],t)

    def test_index_by_increment(self):
        expected_output=[[14, 15, 16, 17, 18], [9, 10, 11, 12, 13], [4, 5, 6, 7, 8], [0, 1, 2, 3]]
        index=find_index_by_increment(years, inc_amt)
        self.assertEqual(expected_output, index)
        
#     def test_resampled_years(self):
#         expected_output=DataFrame(years,columns=[yc])
#         print(expected_output)
#         result=resampled_years(df_year_sample, yc, inc_amt)
#         print(result)
#         assert_frame_equal(expected_output, result)
    
#     def test_resampled_depths_by_years(self):
#         depth_columns=pd.concat([frame.loc[:,'depth (m we)'],frame.loc[:,'depth (m abs)']],axis=1)
#         output_depth_columns=pd.concat([out_frame.loc[:,'top depth (m we)'],out_frame.loc[:,'bottom depth (m we)'],
#                                 out_frame.loc[:,'top depth (m abs)'],out_frame.loc[:,'bottom depth (m abs)']],axis=1)
#         result=resampled_depths_by_years(df_year_sample, index, depth_columns, depth_column_headers)
#         assert_frame_equal(output_depth_columns,result)
    
#     def test_resampled_statistics_by_years(self):
#         result=resampled_statistics_by_years(df_year_sample, yc, index)
#         print(result)
#         expected_output==pd.concat([out_frame.loc[:,'Mean'],
#                                     out_frame.loc[:,'Median'],
#                                     out_frame.loc[:,'Max'],
#                                     out_frame.loc[:,'Min'],
#                                     out_frame.loc[:,'Stdv'],
#                                     out_frame.loc[:,'Count']],axis=1),
#         print(expected_output)
#         assert_frame_equal(expected_output, result)
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()