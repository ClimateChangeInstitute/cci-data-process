'''
Created on Jul 31, 2017

@author: Heather
'''

from pandas.core.frame import DataFrame
from climatechange.resample_stats import compileStats, find_indices, create_depth_headers
import pandas
from typing import List
import numpy as np
from climatechange.compiled_stat import CompiledStat
from climatechange.headers import Header


def create_range_for_depths(list_to_inc:List[float], inc_amt: int=0.01) -> List[float]:
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

def find_index_by_increment_for_depths(list_to_inc:List[float], inc_amt:int=0.01) -> List[List[float]]:
    '''
    
    :param list_to_inc:
    :param inc_amt:
    '''
    top_range = create_range_for_depths(list_to_inc, inc_amt)
    bottom_range = [x + inc_amt for x in top_range]
    return [find_indices(list_to_inc, lambda e: e >= top_range[i] and e < bottom_range[i]) for i in range(0, len(top_range))]

def resampled_depths(df_x_sample, depth_header:Header, inc_amt:int=1):
    top_range = create_range_for_depths(df_x_sample.iloc[:, 0].values.tolist(), inc_amt)
    bottom_range = [x + inc_amt for x in top_range]
    df = DataFrame([top_range, bottom_range]).transpose()
    df.columns = create_depth_headers([depth_header])
    return df

def resampled_statistics_by_x(df_x_sample, index):
    appended_data = []
    for i in index:
        appended_data.extend(compileStats(df_x_sample.iloc[i, [1]].transpose().values.tolist()))
    return DataFrame(appended_data, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])


def resampled_by_inc_depths(df_x_sample:DataFrame,
                    depth_header:Header,
                    inc_amt:float) -> DataFrame:
    '''
    :param df:
    :param inc:
    '''
    index = find_index_by_increment_for_depths(df_x_sample.iloc[:, 0].values.tolist(), inc_amt)
    df_depths = resampled_depths(df_x_sample, depth_header, inc_amt)
    df_stats = resampled_statistics_by_x(df_x_sample, index)
    return pandas.concat([df_depths, df_stats], axis=1)

def compile_stats_by_depth(df:DataFrame, depth_header:Header, sample_header:Header, inc_amt:float) -> CompiledStat:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc) 
    based on the parameters.
    
    :param df: The data to compile stats for
    :param depth_header: The depth column to use for indexing
    :param sample_header: The sample compile to create statistics about
    :param inc_amt: The amount to group the year column by.  For example, 
        2012.6, 2012.4, 2012.2 would all be grouped into the year 2012.
    :return: A new DataFrame containing the resampled statistics for the 
    specified sample and year.
    '''
    
    df_x_sample = pandas.concat([df.loc[:, depth_header.name], df.loc[:, sample_header.name]], axis=1)
    resampled_data = resampled_by_inc_depths(df_x_sample, depth_header, inc_amt)
    
    return CompiledStat(resampled_data, depth_header, sample_header)
