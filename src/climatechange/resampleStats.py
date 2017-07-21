'''
Created on Jul 13, 2017

:author: Heather
'''

import numpy as np
from typing import List

# dataframetolist
# matplotlib- graph age by depth

def findMean(array:List[List[float]]) -> List[float]:
    '''
    find mean value of each list within a list
    :param array: list of lists, 2D array of floats
    :return: list of mean values for each list
    '''
    return [np.nanmean(i) for i in array]  

def findMedian(array:List[List[float]]) -> List[float]:
    '''
    find median value of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of median values for each list
    '''
    return [np.nanmedian(i) for i in array]
       
def findMax(array:List[List[float]]) -> List[float]:
    '''
    find maximum value of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of maximum values for each list
    '''
    return [max(i) for i in array]
      
def findMin(array:List[List[float]]) -> List[float]:
    '''
    find minimum value of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of minimum values for each list
    '''     
    return [min(i) for i in array]

def findStd(array:List[List[float]]) -> List[float]:
    '''
    find standard deviation value of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of standard deviation values for each list
    '''
    return [np.std(i) for i in array]

def findLen(array:List[List[float]]) -> List[float]:
    '''
    find length of list within each list within a list
    :param array: list of lists, 2D array floats
    :return: list of lengths of each list
    '''  
    return [len(i) for i in array]  

def compileStats(array:List[List[float]]) -> List[List[float]]:
    '''
    compile statistics of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of statistics for each list
    '''
    return [findMean(array), findMedian(array), findMax(array), findMin(array), findStd(array), findLen(array)]