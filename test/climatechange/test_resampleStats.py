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
from climatechange.resampleStats import findLen
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


# <<<<<<< HEAD
# array = [[5, 3, 4, 5, 3]]
# emptyArray=[[]]
# array2=[[5, 3, 4, 5, 3],[1, 2, 3, 4],[4, 4]]
# =======
# >>>>>>> 4c142717fc0652688d62af2005ca61521146fe48

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
        self.assertAlmostEqual([], findMedian(emptyArray))
        self.assertAlmostEqual([4.0], findMedian(singleRowArray))
        self.assertAlmostEqual([3.0, 4.0, 3.0], findMedian(multipleRowArray))
    
    def testfindMax(self):
        self.assertAlmostEqual([], findMax(emptyArray))
        self.assertAlmostEqual([5.0], findMax(singleRowArray))
        self.assertAlmostEqual([5.0, 6.0, 5.0], findMax(multipleRowArray))
    
    def testfindMin(self):    
        self.assertAlmostEqual([], findMin(emptyArray))
        self.assertAlmostEqual([3.0], findMin(singleRowArray))
        self.assertAlmostEqual([1.0, 2.0, 1.0], findMin(multipleRowArray))
    
    def testfindStd(self):
        self.assertAlmostEqual([], findStd(emptyArray))
        self.assertAlmostEqual([0.894427190999915860], findStd(singleRowArray))
        self.assertAlmostEqual([1.4142135623730951, 1.4142135623730951, 1.4142135623730951], findStd(multipleRowArray))

<<<<<<< HEAD
    def testfindLen(self):
        self.assertAlmostEqual([], findStd(emptyArray))
        self.assertAlmostEqual([5.0], findStd(singleRowArray))
        self.assertAlmostEqual([5.0, 5.0, 5.0] findStd(multipleRowArray))
 

#         pass
# =======
#     def testfindPtsYear(self):
#         result = findPtsYear(singleRowArray)
#         self.assertAlmostEqual([5], result)
# >>>>>>> 4c142717fc0652688d62af2005ca61521146fe48
#         
    def testcompileStats(self):
        self.assertAlmostEqual([[], [], [], [], [], []], compileStats(emptyArray))
        self.assertAlmostEqual([[4], [4], [5], [3], [0.89442719099991586], [5]], compileStats(singleRowArray))
        self.assertAlmostEqual([[3.0, 4.0, 3.0], [3.0, 4.0, 3.0],[5.0, 6.0, 5.0],[1.0, 2.0, 1.0], [1.4142135623730951, 1.4142135623730951, 1.4142135623730951], [5.0, 5.0, 5.0]], compileStats(multipleRowArray))
        
        
        
        
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
