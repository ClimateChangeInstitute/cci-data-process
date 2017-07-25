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
from climatechange.file import load_csv
import os

#list of values by column, first index is column index, for each you get element of row 

emptyArray = []
singleRowArray = [[5, 3, 4, 5, 3]]
multipleRowArray = [[5.0, 4.0, 3.0, 2.0, 1.0],
                   [2.0, 3.0, 4.0, 5.0, 6.0 ],
                   [1.0, 3.0, 2.0, 5.0, 4.0]]
test_input=[[7, 5, 7], [3, 5, 4], [6, 4, 9]]
test_output=[[6.333333333333333, 7.0, 7, 5, 0.94280904158206336, 3],[4.0, 4.0, 5, 3, 0.81649658092772603, 3],[6.333333333333333, 6.0, 9, 4, 2.0548046676563256, 3]]
# containingNoneArray = [[5.0, None, None, 2.0, 1.0],
#                        [2.0, None, None, 5.0, 6.0 ],
#                        [1.0, None, None, 5.0, 4.0]]
# containingNaNArray = [[5.0, nan, nan, 2.0, 1.0],
#                        [2.0, nan, nan, 5.0, 6.0 ],
#                        [1.0, nan, nan, 5.0, 4.0]]


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

# <<<<<<< HEAD
    def testfindLen(self):
        self.assertAlmostEqual([], findLen(emptyArray))
        self.assertAlmostEqual([5.0], findLen(singleRowArray))
        self.assertAlmostEqual([5.0, 5.0, 5.0], findLen(multipleRowArray))
 

#         pass# =======
#         
    def testcompileStats(self):
        
        self.assertAlmostEqual([], compileStats(emptyArray))
        self.assertAlmostEqual([[4, 4, 5, 3, 0.89442719099991586, 5]], compileStats(singleRowArray))
        self.assertAlmostEqual(test_output, compileStats(test_input))
        
    def testSmallcsv(self):
        
        small_output=[[2009.8, 2009.8, 2011.6, 2008.0, 1.0954451150103279, 19],
                      [2008.3999999999999, 2008.4000000000001, 2012.0, 2004.8, 2.1908902300206643, 19],
                      [0.5966279069999999, 0.59662790700000001, 0.599767442, 0.593488372, 0.0019106600718061043, 19],
                      [1.619, 1.619, 1.6280000000000001, 1.61, 0.0054772255750516448, 19],
                      [9.0, 9.0, 18.0, 0.0, 5.4772255750516612, 19],
                      [41.0, 41.0, 50.0, 32.0, 5.4772255750516612, 19],
                      [6.3684210526315788, 4.0, 14.0, 2.0, 4.1953674491325543, 19],
                      [5.7894736842105265, 7.0, 9.0, 1.0, 2.6072560161054392, 19],
                      [4.3684210526315788, 4.0, 6.0, 2.0, 1.086303549502647, 19],
                      [5.3684210526315788, 5.0, 7.0, 3.0, 1.086303549502647, 19]]
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        self.assertAlmostEqual(small_output,
                               compileStats(frame.transpose().values.tolist()))
        

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
