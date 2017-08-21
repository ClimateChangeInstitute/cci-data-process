'''
Created on Jul 31, 2017

@author: Heather
'''

from typing import List

from pandas import DataFrame, Series
import pandas

from climatechange.compiled_stat import CompiledStat
from climatechange.headers import Header, HeaderType, process_header_data
from climatechange.resample_stats import compileStats, find_indices, create_depth_headers,\
    resampled_statistics
import numpy as np


def create_range_for_depths(list_to_inc:List[float], inc_amt: float=0.01) -> List[float]:
    '''

    :param list_to_inc:
    :param inc_amt:
    '''
    if str(min(list_to_inc))[::-1].find('.') > str(inc_amt)[::-1].find('.'):

        r = str(min(list_to_inc))[::-1].find('.') - 1
    else:
        r = str(inc_amt)[::-1].find('.')
    g = np.arange(np.round(min(list_to_inc), r), max(list_to_inc), inc_amt)
    return [round(i, r) for i in g.tolist()]

def find_index_by_increment(list_to_inc:List[float], range_list:List[float], inc_amt:float=0.01) -> List[List[float]]:
    '''

    :param list_to_inc:
    :param inc_amt:
    '''
    result = []
    range_list_size = len(range_list)
    prev = 0
    for i in range(range_list_size-1):
        tmp = []
        for j in range(prev, len(list_to_inc)):
            e = list_to_inc[j]
            if e >= range_list[i] and e < range_list[i + 1]:
                tmp.append(j)
                prev = j + 1
        result.append(tmp)
    
    tmp = []
    for j in range(prev, len(list_to_inc)):
        e = list_to_inc[j]
        if e >= range_list[range_list_size-1]:
            tmp.append(j)
    result.append(tmp)
    
    return result 

def resampled_depths(range_list:List[float], depth_header:Header, inc_amt):
    top_range = range_list
    bottom_range = [x + inc_amt for x in top_range]
    
    df = DataFrame([top_range, bottom_range]).transpose()
    df.columns = create_depth_headers([depth_header])
    return df

def compile_stats_by_depth(df:DataFrame,
                           depth_header:Header,
                           sample_header:Header,
                           index:List[List[int]],
                           range_list:List[float],
                           inc_amt:float) -> CompiledStat:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc)
    based on the parameters.

    :param df: The data to compile stats for
    :param depth_header: The depth column to use for indexing
    :param sample_header: The sample compile to create statistics about
    :param index: The index that will be compiled for the provided depth
    :param inc_amt: The amount to group the year column by. For example,
        2012.6, 2012.4, 2012.2 would all be grouped into the year 2012.
    :return: A new DataFrame containing the resampled statistics for the
        specified sample and year.
    '''

    df_depths = resampled_depths(range_list, depth_header, inc_amt)
    df_stats = resampled_statistics(df,sample_header, index)
    resampled_data = pandas.concat([df_depths, df_stats], axis=1)

    return CompiledStat(resampled_data, depth_header, sample_header)


def find_index_of_depth_intervals(depth_large:Series, depth_small:Series) -> List[List[int]]:
    '''
    Find the indices of intervals in the larger series such that they are 
    between that of the smaller. 
    
    :param depth_large: Depth columns of larger dataset with smaller increment
    :param depth_small: Depth columns of smaller dataset with larger increment
    '''
    bottom_depth = []
    for i in range(depth_small.size - 1):
        bottom_depth.append(depth_small.loc[i + 1])
    index = [find_indices(depth_large, lambda e: e >= depth_small[i] and e < depth_small[i + 1]) for i in range(0, len(depth_small) - 1)]
    return index

def compiled_stats_by_dd_intervals(larger_df:DataFrame, smaller_df:DataFrame) -> List[List[CompiledStat]]:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc)
    based on the parameters.

    :param df1:Larger Dataframe with smaller intervals to create a compiled stat
    :param df2:Smaller Dataframe with larger intervals to create index of intervals
    :return: A list of list of CompiledStat containing the resampled statistics for the
    specified sample and depth by the depth interval from df2.
    '''
    depth_headers_larger = process_header_data(larger_df, HeaderType.DEPTH)
    depth_headers_smaller = process_header_data(smaller_df, HeaderType.DEPTH)
    sample_headers_larger = process_header_data(larger_df, HeaderType.SAMPLE)

    result_list = []
    for depth_header_l in depth_headers_larger:
        for depth_header_s in depth_headers_smaller:
            if depth_header_l == depth_header_s:
                index = find_index_of_depth_intervals(larger_df.loc[:, depth_header_s.name], smaller_df.loc[:, depth_header_l.name])
                depth_df = create_top_bottom_depth_dataframe(smaller_df, depth_header_s)
                depth_samples = []
                for sample_header in sample_headers_larger:
                    current_stats = []
                    for i in index:
                        current_stats.extend(compileStats([larger_df.loc[i, sample_header.name].tolist()]))
                    current_df = DataFrame(current_stats, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
                    comp_stat = CompiledStat(pandas.concat((depth_df, current_df), axis=1), depth_header_l, sample_header)
                    depth_samples.append(comp_stat)
        result_list.append(depth_samples)
    return result_list

def create_top_bottom_depth_dataframe(df:DataFrame, depth_header:Header) -> DataFrame:

    new_depth_headers = create_depth_headers([depth_header])

    list_depth = []
    for i in range(0, df.shape[0] - 1):
        list_depth.append([df.loc[i, depth_header.name], df.loc[i + 1, depth_header.name]])
    return DataFrame(list_depth, columns=new_depth_headers)

def create_top_bottom_depth_dataframe_for_laser_file(df:DataFrame, depth_header:Header) -> DataFrame:

    new_depth_headers = create_depth_headers([depth_header])

    list_depth = []
    for i in range(0, df.shape[0] - 1):
        list_depth.append([df.loc[i, depth_header.name], df.loc[i + 1, depth_header.name]])
    return DataFrame(list_depth, columns=new_depth_headers)
