'''
Created on Jul 31, 2017

@author: Heather
'''

from typing import List, Tuple

from pandas import DataFrame
import pandas

from climatechange.compiled_stat import CompiledStat
from climatechange.headers import Header, HeaderType, process_header_data
from climatechange.resample_stats import compileStats, create_depth_headers
import numpy as np
import logging
from climatechange.plot import write_data_to_csv_files
import os


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
    logging.debug("find_index_by_increment: range_list=%s", range_list)
    result = []
    top_range = []
    gaps=[]
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
            logging.warning('no values between [%f,%f)', range_list[i], range_list[i + 1])
            gaps.append([range_list[i], range_list[i + 1]])
        else: 
            result.append(tmp)
            top_range.append(range_list[i])
        
    tmp = []
    for j in range(prev, len(list_to_inc)):
        e = list_to_inc[j]
        if e >= range_list[range_list_size-1]:
            tmp.append(j)
    if not tmp:
        logging.warning('no values > %f',range_list[range_list_size-1])
    else:
        result.append(tmp)
        top_range.append(range_list[range_list_size-1])
       
    return result, top_range


def find_gaps(df_HR:DataFrame, df_LR:DataFrame, pdf_folder:str,file:str) -> Tuple[List[List[int]],List[float]]:
    '''

    :param list_to_inc:
    :param inc_amt:
    '''
    depth_headers_HR = process_header_data(df_HR, HeaderType.DEPTH)
    depth_headers_LR = process_header_data(df_LR, HeaderType.DEPTH)

    
    for dh_HR in depth_headers_HR:
        for dh_LR in depth_headers_LR:
            if dh_HR == dh_LR:
                csv_gaps=os.path.join(pdf_folder,'%s_%s_gaps.csv'%(file,dh_LR.label))
                list_to_inc=df_HR.loc[:, dh_HR.name].tolist()
                range_list=df_LR.loc[:, dh_LR.name].tolist()
                gaps=[]
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
                        gaps.append([range_list[i], range_list[i + 1]])
                        
                write_data_to_csv_files(DataFrame(gaps,columns=[('gap_start'),('gap_end')]),csv_gaps)

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


def compiled_stats_HR_by_LR(df_HR:DataFrame, df_LR:DataFrame) -> List[List[CompiledStat]]:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc)
    based on the parameters.

    :param df1:Larger Dataframe with smaller intervals to create a compiled stat
    :param df2:Smaller Dataframe with larger intervals to create index of intervals
    :return: A list of list of CompiledStat containing the resampled statistics for the
    specified sample and depth by the depth interval from df2.
    '''
    depth_headers_HR = process_header_data(df_HR, HeaderType.DEPTH)
    depth_headers_LR = process_header_data(df_LR, HeaderType.DEPTH)
    sample_headers_HR = process_header_data(df_HR, HeaderType.SAMPLE)

    result_list = []
    for dh_HR in depth_headers_HR:
        for dh_LR in depth_headers_LR:
            if dh_HR == dh_LR:
                index,top_range = find_index_by_increment(df_HR.loc[:, dh_HR.name].tolist(), df_LR.loc[:, dh_LR.name].tolist())
                depth_df = create_top_bottom_depth_dataframe(df_LR, dh_LR)
                depth_samples = []
                for sample_header in sample_headers_HR:
                    current_stats = []
                    for i in index:
                        current_stats.append(compileStats(df_HR.loc[i, sample_header.name].tolist()))
                    current_df = DataFrame(current_stats, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
                    comp_stat = CompiledStat(pandas.concat((depth_df, current_df), axis=1), dh_HR, sample_header)
                    depth_samples.append(comp_stat)
        result_list.append(depth_samples)
    return result_list

