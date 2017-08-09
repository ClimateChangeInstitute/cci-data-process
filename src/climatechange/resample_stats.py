'''
Created on Jul 13, 2017

:author: Heather
'''

from pandas.core.frame import DataFrame
from typing import List
from climatechange.headers import Header, HeaderType
import numpy as np
import pandas
from climatechange.compiled_stat import CompiledStat


def create_range_by_inc(list_to_inc:List[float], inc_amt: int=1) -> List[float]:
    '''
    
    :param list_to_inc:
    :param inc_amt:
    '''
    # creates lists of years incrementally by input of increment
    # list_years must be Years
    x = min(list_to_inc)
    y = max(list_to_inc)
    return [i for i in range(round(x), round(y), inc_amt)]

def find_indices(list_to_inc, condition) -> List[int]:
    '''
    
    :param list_to_inc:
    :param condition:
    '''
    return [i for i, elem in enumerate(list_to_inc) if condition(elem)]


def find_index_by_increment(list_to_inc:List[float], inc_amt:int=1) -> List[List[float]]:
    '''
    
    :param list_to_inc:
    :param inc_amt:
    '''
    top_range = create_range_by_inc(list_to_inc, inc_amt)
    bottom_range = [x + inc_amt for x in top_range]
    return [find_indices(list_to_inc, lambda e: e >= top_range[i] and e < bottom_range[i]) for i in range(0, len(top_range))]


def create_depth_headers(list_headers: List[Header]) -> List[str]:
    '''
    Expected output should look like
    
    ['top depth (m we)','bottom depth (m we)','top depth (m abs)','bottom depth (m abs)']

    :param list_headers: list of headers, example: ['depth (m we)','depth (m abs)']
    '''
    result = []
    for i in list_headers:
        result.append('top_' + i.label)
        result.append('bottom_' + i.label)
    
    return result

def resampled_years(df_year_sample, year_header, inc_amt:int=1):
    return DataFrame(create_range_by_inc(df_year_sample.iloc[:, 0].values.tolist(), inc_amt), columns=[year_header.label])

def resampled_statistics_by_years(df_year_sample,sample_header, index):
    appended_data = []
    for i in index:
        appended_data.extend(compileStats(df_year_sample.iloc[i, [1]].transpose().values.tolist()))
    return DataFrame(appended_data, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
    #add units to column names

def resampled_depths_by_years(index, depth_columns:DataFrame, depth_column_headers:List[Header]) -> DataFrame:
    append_depth = []
    for i in index:
        min_depth = depth_columns.iloc[i, :].min()
        max_depth = depth_columns.iloc[i, :].max()
        combined = []       
        for j in range(min_depth.size):
            combined.append(min_depth.iloc[j])
            combined.append(max_depth.iloc[j])
        append_depth.append(combined)

    return DataFrame(append_depth, columns=create_depth_headers(depth_column_headers))

def resampled_by_inc_years(df_year_sample:DataFrame,
                    sample_header:Header,
                    year_header:Header,
                    depth_columns:DataFrame,
                    depth_column_headers:List[Header],
                    inc_amt: int=1) -> DataFrame:
    '''
    :param df:
    :param inc:
    '''
    index = find_index_by_increment(df_year_sample.iloc[:, 0].values.tolist(), inc_amt)
    df_years = resampled_years(df_year_sample, year_header, inc_amt)
    df_depth = resampled_depths_by_years(index, depth_columns, depth_column_headers)
    df_stats = resampled_statistics_by_years(df_year_sample,sample_header, index)
    return pandas.concat([df_years, df_depth, df_stats], axis=1)
    

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
    return [np.nanmax(i) for i in array]
      
def findMin(array:List[List[float]]) -> List[float]:
    '''
    find minimum value of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of minimum values for each list
    '''     
    return [np.nanmin(i) for i in array]

def findStd(array:List[List[float]]) -> List[float]:
    '''
    find standard deviation value of each list within a list
    :param array: list of lists, 2D array floats
    :return: list of standard deviation values for each list
    '''
    return [np.nanstd(i) for i in array]

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
                                  findStd(array),
                                  findMedian(array),
                                  findMax(array),
                                  findMin(array),
                                  findLen(array))]


def compile_stats_by_year(df:DataFrame, headers: Header, year_header:Header, sample_header:Header, inc_amt:int=1) -> CompiledStat:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc) 
    based on the parameters.
    
    :param df: The data to compile statistics for
    :param year_header: The year column to use for indexing
    :param sample_header: The sample_header compile to create statistics about
    :param inc_amt: The amount to group the year column by.  For example, 
        2012.6, 2012.4, 2012.2 would all be grouped into the year 2012.
    :return: A new DataFrame containing the resampled statistics for the 
        specified sample_header and year.
    '''
    
    year_column = df.loc[:, year_header.name]
    sample_column = df.loc[:, sample_header.name]
    
    depth_column_headers = [ h for h in headers if h.htype == HeaderType.DEPTH ]
    depth_column_headers_names=[ h.name for h in headers if h.htype == HeaderType.DEPTH ]
    depth_columns = DataFrame([df.loc[:, c].values.tolist() for c in df.columns if c in depth_column_headers_names]).transpose()
    
    df_year_sample = pandas.concat([year_column, sample_column], axis=1)
    resampled_data = resampled_by_inc_years(df_year_sample, sample_header,year_header, depth_columns, depth_column_headers, inc_amt)
    
    return CompiledStat(resampled_data,year_header,sample_header)
