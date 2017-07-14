'''
Created on Jul 13, 2017

@author: Heather
'''
import unittest
from climatechange.resampleStats import findMean
from climatechange.resampleStats import findMedian
from climatechange.resampleStats import findMax
from climatechange.resampleStats import findMin
from climatechange.resampleStats import findStd
from climatechange.resampleStats import findPtsYear
from climatechange.resampleStats import compileStats

array = [[5, 3, 4, 5, 3]]
array1=[[]]
array2=[[5, 3, 4, 5, 3],[1, 2, 3, 4],[4, 4]]

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

# test for all functions with same name
    def testfindMean(self):       
        result = findMean(array)
        self.assertAlmostEqual([4], result)     
        pass
    
    def testfindMedian(self):       
        result=findMedian(array)
        self.assertAlmostEqual([4], result)        
        pass
    
    def testfindMax(self):
        result=findMax(array)
        self.assertAlmostEqual([5],result)
        pass
    
    def testfindMin(self):    
        result=findMin(array)
        self.assertAlmostEqual([3],result)        
        pass
    
    def testfindStd(self):
        result=findStd(array)
        self.assertAlmostEqual([0.894427190999915860],result)
        pass
    
    def testfindPtsYear(self):
        result=findPtsYear(array)
        self.assertAlmostEqual([5],result)
        pass
        
    def testcompileStats(self):
        result=compileStats(array)
        self.assertAlmostEqual([[4],[4], [5], [3], [0.89442719099991586], [5]], result)
        pass
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()