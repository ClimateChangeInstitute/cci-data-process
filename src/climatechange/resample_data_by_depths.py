'''
Created on Jul 31, 2017

@author: Heather
'''

from typing import List, Tuple

from pandas import DataFrame
import pandas

from climatechange.compiled_stat import CompiledStat
from climatechange.headers import Header, HeaderType, process_header_data
from climatechange.resample_stats import compileStats, create_depth_headers,\
    resampled_statistics
import numpy as np
import logging


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

def find_index_by_increment(list_to_inc:List[float], range_list:List[float]) -> Tuple[List[List[int]],List[float]]:
    '''

    :param list_to_inc:
    :param inc_amt:
    '''
    result = []
    top_range = []
    range_list_size = len(range_list)
    prev = 0
    for i in range(range_list_size - 1):
        tmp = []
        for j in range(prev, len(list_to_inc)):
            e = list_to_inc[j]
            if e >= range_list[i] and e < range_list[i + 1]:
                tmp.append(j)
                prev = j + 1
        if not tmp:
            logging.warn('no values between [%f,%f)', range_list[i], range_list[i + 1])
        else: 
            result.append(tmp)
            top_range.append(range_list[i])
        
    tmp = []
    for j in range(prev, len(list_to_inc)):
        e = list_to_inc[j]
        if e >= range_list[range_list_size-1]:
            tmp.append(j)
    if not tmp:
        logging.warn('no values > %f',range_list[range_list_size-1])
    else:
        result.append(tmp)
        top_range.append(range_list[range_list_size-1])
            
    return result, top_range

def resampled_depths(top_range:List[float], depth_header:Header, inc_amt):

    bottom_range = [x + inc_amt for x in top_range]
    
    df = DataFrame([top_range, bottom_range]).transpose()
    df.columns = create_depth_headers([depth_header])
    return df



def create_top_bottom_depth_dataframe(df:DataFrame, depth_header:Header) -> DataFrame:

    new_depth_headers = create_depth_headers([depth_header])

    list_depth = []
    for i in range(0, df.shape[0] - 1):
        list_depth.append([df.loc[i, depth_header.name], df.loc[i + 1, depth_header.name]])
    return DataFrame(list_depth, columns=new_depth_headers)


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
                index,top_range = find_index_by_increment(larger_df.loc[:, depth_header_s.name].tolist(), smaller_df.loc[:, depth_header_l.name].tolist())
                depth_df = create_top_bottom_depth_dataframe(smaller_df, depth_header_s)
                depth_samples = []
                for sample_header in sample_headers_larger:
                    current_stats = []
                    for i in index:
                        current_stats.append(compileStats(larger_df.loc[i, sample_header.name].tolist()))
                    current_df = DataFrame(current_stats, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
                    comp_stat = CompiledStat(pandas.concat((depth_df, current_df), axis=1), depth_header_l, sample_header)
                    depth_samples.append(comp_stat)
        result_list.append(depth_samples)
    return result_list


def create_top_bottom_depth_dataframe_for_laser_file(df:DataFrame, depth_header:Header) -> DataFrame:

    new_depth_headers = create_depth_headers([depth_header])

    list_depth = []
    for i in range(0, df.shape[0] - 1):
        list_depth.append([df.loc[i, depth_header.name], df.loc[i + 1, depth_header.name]])
    return DataFrame(list_depth, columns=new_depth_headers)
