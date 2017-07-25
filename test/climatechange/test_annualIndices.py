'''
Created on Jul 18, 2017

@author: Heather
'''
import unittest
from climatechange.find_index_by_increments import find_indices
from climatechange.find_index_by_increments import find_index_by_increment
from climatechange.find_index_by_increments import create_range_by_inc
# import os

# from climatechange.file import get_data_frame_from_csv


lst=[6, 9, 23, 3, 2, 8, 9, 3, 5]
years=[2011.6,2011.2,2011,2010.6,2010.2,2010,2009,2008.4,2008.1]
inc=1

# for i in list(frame.column.values)
#     for list of names in header_dict.json
#     if they match, rename headers using the Key
#     -store units
#     if more than one year, send notice to user to choose one
#     - use year chosen to be put into index by year
#     -if header is depth, more than one depth, 
#         run index by year through depths, choose minimum and maximum depths in index
#     if header is chemistry, run statistics through each, store in seperate csv files
#     - 

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def test_create_range_by_inc(self):
        j,k=create_range_by_inc(years,inc)
        self.assertEqual([2008,2009, 2010, 2011],j)
        self.assertEqual([2009, 2010,2011,2012],k)

    def test_find_indices(self):
        #find indices of the specific condition called
        t=find_indices(lst,lambda e: e>10)
        self.assertEqual([2],t,'value should be 3')

    def test_index_by_year(self):
        ytop,ind=find_index_by_increment(years, inc)
        self.assertEqual([2008,2009,2010,2011], ytop)
        self.assertEqual([[7,8],[6],[3,4,5],[0,1,2]], ind)      
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()