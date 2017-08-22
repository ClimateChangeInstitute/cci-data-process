'''
Created on Jul 13, 2017

:author: Heather
'''

from typing import List

from pandas import DataFrame
import pandas

from climatechange.compiled_stat import CompiledStat
from climatechange.headers import Header, HeaderType
import numpy as np


def create_range_by_year(list_to_inc:List[float], inc_amt: int=1) -> List[float]:
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

# def resampled_years(range_list, year_header):
#     return DataFrame(range_list, columns=[year_header.label])

def resampled_statistics(df:DataFrame, sample_header:Header, index:List[List[float]]):
    appended_data = []
    for i in index:
        appended_data.append(compileStats(df.loc[i, sample_header.name].values))
    return DataFrame(appended_data, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
    # add units to column names
    

def resampled_depths_by_years(index:List[List[float]], depth_columns:DataFrame, depth_column_headers:List[Header]) -> DataFrame:
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




def compileStats(array:List[float]) -> List[float]:
    '''
    compile statistics of each list within a list
    :param array: array of floats
    :return: list of statistics
    '''
    return [np.nanmean(array), np.nanstd(array), np.nanmedian(array), 
            np.nanmax(array), np.nanmin(array), len(array)]


def compile_stats_by_year(df:DataFrame,
                          headers: Header,
                          year_header:Header,
                          sample_header:Header,
                          index:List[List[float]],
                          range_list:List[float],
                          inc_amt:int=1) -> CompiledStat:
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

    depth_column_headers = [ h for h in headers if h.htype == HeaderType.DEPTH ]
    depth_column_headers_names = [ h.name for h in headers if h.htype == HeaderType.DEPTH ]
    depth_columns = DataFrame([df.loc[:, c].values.tolist() for c in df.columns if c in depth_column_headers_names]).transpose()
    
    df_years=DataFrame(range_list, columns=[year_header.label])
    df_depth = resampled_depths_by_years(index, depth_columns, depth_column_headers)
    df_stats = resampled_statistics(df, sample_header, index)
    resampled_data = pandas.concat([df_years, df_depth, df_stats], axis=1)

    return CompiledStat(resampled_data, year_header, sample_header)

