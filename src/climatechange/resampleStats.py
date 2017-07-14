'''
Created on Jul 13, 2017

@author: Heather
'''
import csv

import numpy as np
from typing import List


# year=[2011, 2010, 2009, 2008, 2007, 2006]
# chem1=[5, 6, 2, 99, 20, 2]
# chem2=[34, 28, 222, 2343, 23, 43]
# array=[year,chem1, chem2]

# dataframetolist


def findMean(array:List[List[float]]) -> List[float]:
    '''
    find mean of each list within a list
    :param array: list of lists, 2D array of floats
    :return: list of means of each list
    '''
# find mean of data points within a single increment of the data set
    Mean = []
    for i in array:
        y = np.nanmean(i)
        if i == 0:
            Mean = y
        else:
            Mean.append(y)  
    return Mean

def findMedian(array:List[List[float]]) -> List[float]:
# find median of data points within a single increment of the data set
    Median = []
    for i in array:
        y = np.nanmedian(i)
        if i == 0:
            Median = y
        else:
            Median.append(y)            
    return Median
       

def findMax(array:List[List[float]]) -> List[float]:
# find max of data points within a single increment of the data set
    Max = []
    for i in array:
        y = max(i)
        if i == 1:
            Max = y
        else:
            Max.append(y)            
    return Max
      

def findMin(array:List[List[float]]) -> List[float]:
# find min of data points within a single increment of the data set
    Min = []
    for i in array:
        y = min(i)
        if i == 1:
            Min = y
        else:
            Min.append(y)            
    return Min
      

def findStd(array:List[List[float]]) -> List[float]:
# find std of data points within a single increment of the data set
    Std = []
    for i in array:
        y = np.std(i)
        if i == 1:
            Std = y
        else:
            Std.append(y)     
    return Std

def findPtsYear(array:List[List[float]]) -> List[float]:
# find # of data points within a single increment of the data set
    Pts = []
    for i in array:
        y = len(i)
        if i == 1:
            Pts = y
        else:
            Pts.append(y)     
    return Pts   

def compileStats(array:List[List[float]]) -> List[List[float]]:
# compiles all statistics for all yearly increments
    Mean = findMean(array)
    Median = findMedian(array)
    Max = findMax(array)
    Min = findMin(array)
    Std = findStd(array)
    Pts = findPtsYear(array)
    comStats = [Mean, Median, Max, Min, Std, Pts]
    return comStats

# def outputCSV(alldata, outputFile):
# # outputs compiled data to csv file
#     with open(outputFile, "wb") as f:
#         write = csv.writer(f)
#         write.writerow(('Mean', 'Median', 'Max', 'Min', 'Stdv', '#ofPts'))
#         write.writerows(alldata)

# array=inputArray('C:\Users\Heather\Documents\ColleGnifetti\KCCData\Pascal_NewTimeScale_MasterFiles\KCC_CFAmaster20170621_Part1.csv')

# alldata = zip(*compileStats(array))

# outputCSV(alldata, "C:\Users\Heather\Documents\ColleGnifetti\Python\outputStats_test4.csv")
    
