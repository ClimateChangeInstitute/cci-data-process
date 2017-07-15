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
from math import nan

emptyArray = []
singleRowArray = [[5, 3, 4, 5, 3]]
multipleRowArray = [[5.0, 4.0, 3.0, 2.0, 1.0],
                   [2.0, 3.0, 4.0, 5.0, 6.0 ],
                   [1.0, 3.0, 2.0, 5.0, 4.0]]
containingNoneArray = [[5.0, None, None, 2.0, 1.0],
                       [2.0, None, None, 5.0, 6.0 ],
                       [1.0, None, None, 5.0, 4.0]]
containingNaNArray = [[5.0, nan, nan, 2.0, 1.0],
                       [2.0, nan, nan, 5.0, 6.0 ],
                       [1.0, nan, nan, 5.0, 4.0]]



class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

# test for all functions with same name
    def testfindMean(self):
        self.assertAlmostEqual([], findMean(emptyArray))
        self.assertAlmostEqual([4.0], findMean(singleRowArray))
        self.assertAlmostEqual([3.0, 4.0, 3.0], findMean(multipleRowArray))
        
        # Maybe throw an error?
        # self.assertAlmostEqual([None, None, None], findMean(containingNoneArray))
        
        # Similarly what to do with nan values?
        # self.assertAlmostEqual([nan, nan, nan], findMean(containingNaNArray))
    
        # Also assume that 2D array is rectangular shape? No funny business. :-)
    
    def testfindMedian(self):       
        result = findMedian(singleRowArray)
        self.assertAlmostEqual([4], result)
    
    def testfindMax(self):
        result = findMax(singleRowArray)
        self.assertAlmostEqual([5], result)
    
    def testfindMin(self):    
        result = findMin(singleRowArray)
        self.assertAlmostEqual([3], result)
    
    def testfindStd(self):
        result = findStd(singleRowArray)
        self.assertAlmostEqual([0.894427190999915860], result)
    
    def testfindPtsYear(self):
        result = findPtsYear(singleRowArray)
        self.assertAlmostEqual([5], result)
        
    def testcompileStats(self):
        result = compileStats(singleRowArray)
        self.assertAlmostEqual([[4], [4], [5], [3], [0.89442719099991586], [5]], result)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
