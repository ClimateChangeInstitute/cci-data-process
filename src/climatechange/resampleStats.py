'''
Created on Jul 13, 2017

:author: Heather
'''

from pandas.core.frame import DataFrame
from typing import List

from climatechange.headers import Header, HeaderType
import numpy as np
import pandas
from climatechange.find_index_by_increments import resample_by_inc


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
#     result=[findMean(array), findMedian(array), findMax(array), findMin(array), findStd(array), findLen(array)]
    return [ list(x) for x in zip(findMean(array),
                                  findMedian(array),
                                  findMax(array),
                                  findMin(array),
                                  findStd(array),
                                  findLen(array))]


def compile_stats_by_year(df:DataFrame, headers: Header, yc:str, sc:str, inc_amt:int=1) -> DataFrame:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc) 
    based on the parameters.
    
    :param df: The data to compile sats for
    :param yc: The year column to use for indexing
    :param sc: The sample compile to create statistics about
    :param inc_amt: The amount to group the year column by.  For example, 
        2012.6, 2012.4, 2012.2 would all be grouped into the year 2012.
    :return: A new DataFrame containing the resampled statistics for the 
    specified sample and year.
    '''
    
    year_column = df.loc[:,yc]
    sample_column = df.loc[:,sc]
    
    depth_column_header = [ h.original_value for h in headers if h.htype == HeaderType.DEPTH ]
    depth_columns = []
    for c in df.columns:
        if c in depth_column_header:
            depth_columns.append(df.loc[:,c])    
    
    print(pandas.concat([year_column, sample_column], axis=1).values)
    resampled_data=resample_by_inc(pandas.concat([year_column, sample_column], axis=1), inc_amt)
    print (resampled_data)
    
    return df