'''
Created on Jul 18, 2017

@author: Heather
'''
import unittest
from climatechange.lstDataframe import lstToDataframe

emptyArray = []
singleRowArray = [[5, 3, 4, 5, 3]]
multipleRowArray = [[5.0, 4.0, 3.0, 2.0, 1.0],
                   [2.0, 3.0, 4.0, 5.0, 6.0 ],
                   [1.0, 3.0, 2.0, 5.0, 4.0]]
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

    def testlstToDataframe(self):
#         single = lstToDataframe(singleRowArray)
#         print(frame.columns)
        self.assertEqual(5, lstToDataframe(singleRowArray).iloc[0][0], 'value should be 5')
        self.assertEqual(3.0, lstToDataframe(multipleRowArray).iloc[1][1], 'value should be 6')

    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()