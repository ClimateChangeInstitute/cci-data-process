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
from climatechange.headers import Header, HeaderType, process_header_data
from pandas import Series


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

def resampled_depths(df_x_sample:DataFrame, depth_header:Header, inc_amt):
    top_range = create_range_for_depths(df_x_sample.iloc[:, 0].values.tolist(), inc_amt)
    bottom_range = [x + inc_amt for x in top_range]
#     if len(index_to_remove)>0:
#         for i in sorted(index_to_remove, reverse=True):
# 
#             del top_range[i]
#             del bottom_range[i]
    df = DataFrame([top_range, bottom_range]).transpose()
    df.columns = create_depth_headers([depth_header])
    return df

def resampled_statistics_by_x(df_x_sample,inc_amt):
    index = find_index_by_increment_for_depths(df_x_sample.iloc[:, 0].values.tolist(), inc_amt)
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
   
#     print(index)
#     index_to_remove=[index.index(i) for i in index if len(i)<1 or i[0]==0]
#     index = [i for i in index if len(i)>1]
#     print(index)
#     print(index_to_remove)

            
    df_depths = resampled_depths(df_x_sample, depth_header, inc_amt)
#     df_depths = resampled_depths(df_x_sample, depth_header, inc_amt,index_to_remove)   
    df_stats = resampled_statistics_by_x(df_x_sample, inc_amt)
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


#for resample by depth intervals
#









         
def find_index_of_depth_intervals(depth_large:Series,depth_small:Series)->List[List[int]]:    
    '''
    
    :param depth_large:depth columns of larger dataset with smaller increment
    :param depth_small:depth columns of smaller dataset with larger increment
    '''
    bottom_depth=[]
    for i in range(depth_small.size-1):
        bottom_depth.append(depth_small.loc[i+1])
    index=[find_indices(depth_large, lambda e: e >= depth_small[i] and e < depth_small[i+1]) for i in range(0, len(depth_small)-1)] 
    return index
 
def compiled_stats_by_dd_intervals(larger_df:DataFrame,smaller_df:DataFrame) -> List[List[CompiledStat]]:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc) 
    based on the parameters.
     
    :param df1:Larger Dataframe with smaller intervals to create a compiled stat
    :param df2:Smaller Dataframe with larger intervals to create index of intervals
    :return: A list of list of CompiledStat containing the resampled statistics for the 
    specified sample and depth by the depth interval from df2.
    '''
    headers_larger=process_header_data(larger_df)
    headers_smaller=process_header_data(smaller_df)
    depth_headers_larger=[h for h in headers_larger if h.htype == HeaderType.DEPTH]
    depth_headers_smaller=[h for h in headers_smaller if h.htype == HeaderType.DEPTH]
    sample_headers_larger=[h for h in headers_larger if h.htype == HeaderType.SAMPLE]
     
    result_list = []
    for depth_header_l in depth_headers_larger:
        for depth_header_s in depth_headers_smaller:
            if depth_header_l==depth_header_s:    
                index=find_index_of_depth_intervals(larger_df.loc[:,depth_header_s.name],smaller_df.loc[:,depth_header_l.name])
                depth_df=create_top_bottom_depth_dataframe(smaller_df,depth_header_s)
                depth_samples=[]
                for sample_header in sample_headers_larger:
                    current_stats = []
                    for i in index:
                        current_stats.extend(compileStats([larger_df.loc[i,sample_header.name].tolist()]))
                    current_df = DataFrame(current_stats, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
                    comp_stat=CompiledStat(pandas.concat((depth_df,current_df),axis=1),depth_header_l,sample_header)
                    depth_samples.append(comp_stat)
        result_list.append(depth_samples)
    return result_list

def create_top_bottom_depth_dataframe(df:DataFrame,depth_header:Header)->DataFrame:
    
    new_depth_headers=create_depth_headers([depth_header])
    
    list_depth = []
    for i in range(0, df.shape[0]-1):
        list_depth.append([df.loc[i,depth_header.name],df.loc[i+1,depth_header.name]])
    return DataFrame(list_depth,columns=new_depth_headers)


