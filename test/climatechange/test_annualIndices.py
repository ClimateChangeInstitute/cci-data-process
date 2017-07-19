'''
Created on Jul 18, 2017

@author: Heather
'''
import unittest

from climatechange.annualIndices import increments_by_year
from climatechange.annualIndices import find_indices
from climatechange.annualIndices import index_by_year

lst=[6, 9, 23, 3, 2, 8, 9, 3, 5]
years=[2011.6,2011.2,2011,2010.6,2010.2,2010,2009,2008.4,2008.1]
# frame = get_data_frame_from_csv(os.path.join('csv_files', 'small.csv'))
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def test_increments_by_year(self):
        j,k=increments_by_year(years)
        self.assertEqual([2008,2009, 2010, 2011],j)
        self.assertEqual([2009, 2010,2011,2012],k)

    def test_find_indices(self):
        #find indices of the specific condition called
        t=find_indices(lst,lambda e: e>10)
        self.assertEqual([2],t,'value should be 3')

    def test_index_by_year(self):
        ytop,ind=index_by_year(years)
        self.assertEqual([2008,2009,2010,2011], ytop, 'no')
        self.assertEqual([[7,8],[6],[3,4,5],[0,1,2]], ind, 'no')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()