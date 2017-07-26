'''
Created on Jul 13, 2017

:author: Heather
'''

from pandas.core.frame import DataFrame
from typing import List

from climatechange.headers import Header, HeaderType
import numpy as np
import pandas


def create_range_by_inc(lst,inc):
    #creates lists of years incrementally by input of increment
    #lst must be Years
    return [x for x in range(int(min(lst)),int(max(lst))+1,inc)], [x+1 for x in range(int(min(lst)),int(max(lst))+1,inc)]

def find_indices(lst,condition):
    #find indices of the specific condition called
    return [j for j, elem in enumerate(lst) if condition(elem)]

def find_index_by_increment(lst,inc):
    ytop,ybot=create_range_by_inc(lst,inc)
    return [ytop,[find_indices(lst,lambda e: e>=ytop[i] and e<ybot[i]) for i in range(0,len(ytop))]]

def create_depth_headers(list_headers: List[str])-> List[str]:
    '''
    Expected output should look like
    
    ['top depth (m we)','bottom depth (m we)','top depth (m abs)','bottom depth (m abs)']

    :param list_headers: list of headers, example: ['depth (m we)','depth (m abs)']
    '''
    result = []
    for i in list_headers:
        result.append('top ' + i)
        result.append('bottom ' + i)
    
    return result

def resample_by_inc(df_year_sample:DataFrame,
                    yc:str,
                    depth_columns:DataFrame,
                    depth_column_headers:List[str],
                    inc_amt: int=1) -> DataFrame:
    '''
    
    :param df:
    :param inc:
    '''
    years,ind=find_index_by_increment(df_year_sample.iloc[:,0].values.tolist(),inc_amt)
    appended_data=[]
    append_depth=[]
    for i in ind:
        min_depth=depth_columns.iloc[i,:].min()
        max_depth=depth_columns.iloc[i,:].max()
        combined=[]
        
        for j in range(min_depth.size):
            combined.append(min_depth.iloc[j])
            combined.append(max_depth.iloc[j])
        append_depth.append(combined)
        appended_data.extend(compileStats(df_year_sample.iloc[i,[1]].transpose().values.tolist()))
    df_years=DataFrame(years, columns=[yc])
    # find name of year resampled by
    df_depth=DataFrame(append_depth,columns=create_depth_headers(depth_column_headers))
    # find name of depths resampled by
    df_stats=DataFrame(appended_data,columns=['Mean','Median','Max','Min','Stdv','Count'])
    print(pandas.concat([df_years,df_depth,df_stats], axis=1))
    return pandas.concat([df_years,df_depth,df_stats], axis=1)


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
    
    depth_column_headers = [ h.original_value for h in headers if h.htype == HeaderType.DEPTH ]
    depth_columns=DataFrame([df.loc[:,c].values.tolist() for c in df.columns if c in depth_column_headers]).transpose()
    df_year_sample=pandas.concat([year_column, sample_column], axis=1)
    resampled_data=resample_by_inc(df_year_sample,yc,depth_columns,depth_column_headers,inc_amt)
    
    return resampled_data