'''
Created on Aug 10, 2017

@author: Heather
'''
from builtins import str
import os
import re
from typing import List

from matplotlib.backends.backend_pdf import PdfPages
import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series

from climatechange.headers import process_header_data, HeaderType, Header
from climatechange.process_data_functions import clean_data
import matplotlib.pyplot as plt
import numpy as np


class LaserFile:
    def __init__(self, file_path, laser_time, start_depth, end_depth, 
                 washin_time, washout_time, depth_age_file):
        self.file_path = file_path
        self.laser_time = laser_time
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.washin_time = washin_time
        self.washout_time = washout_time
        self.depth_age_file = depth_age_file
        self.raw_data = load_laser_txt_file(file_path)
        self.processed_data = clean_LAICPMS_data(self)


    def __str__(self):
        return self.file_path
    
    def __repr__(self):
        return self.__str__()
    



def readFile(file_path, laser_time, start_depth, end_depth, washin_time, 
             washout_time, depth_age_file) -> LaserFile:  # reads information from inputfile
                 
    return LaserFile(file_path, laser_time, start_depth, end_depth, washin_time, washout_time, depth_age_file)


def load_input_file(input_file:str, depth_age_file:str) -> List[LaserFile]:  # gets information from input file
    """
    """
    result = []
    input_folder = os.path.dirname(input_file)
    for line in open(input_file, 'rU') :
        if not line.startswith(("#", '"')):
            columns = line.split()
            result.append(readFile(os.path.join(input_folder, columns[0]),
                                   float(columns[1]),
                                   float(columns[2]),
                                   float(columns[3]),
                                   float(columns[4]),
                                   float(columns[5]),
                                   depth_age_file))
    return result

    
def load_laser_txt_file(file_path:str) -> DataFrame:
    
    rows = []
    with open(file_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                header = line.split("\t")
                header[0] = "Time"
                for i in range(1, len(header)):
                    header[i] = re.sub("\(.*\)", "", header[i]).strip()
            elif i > 5:
                rows.append(line.split())
    return DataFrame(rows, columns=header)



def process_laser_data_by_run(f:LaserFile) -> DataFrame:
    '''
    
    :param f:
    :param depth_age_file:
    :param path:
    
    :return: csv:original data, csv:filtered data, pdf: og data vs. filtered by depth
        list of list of stats 
    '''
    pdf_filename = '_original_vs._filtered_laser_data.pdf'

#     df_filter=filter_LAICPMS_data(laser_run_df)
    headers = process_header_data(f.processed_data)
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]
    depth_headers = [h for h in headers if h.htype == HeaderType.DEPTH]
    
    with PdfPages(pdf_filename) as pdf:
        for depth_header in depth_headers:
            for sample_header in sample_headers:
                filter_and_plot_laser_data_by_segment(f.processed_data, depth_header, sample_header, pdf)
# 
    
# def combine_laser_data(directory:str):
#     
#     df_original, df_filter=combine_laser_data_by_inputfile(input_file, depth_age_file)

def combine_laser_data_by_input_file(input_file:str, depth_age_file:str) -> DataFrame:
      
    laser_files = load_input_file(input_file, depth_age_file)
    df = DataFrame()
    
    for f in laser_files:
        process_laser_data_by_run(f)
        df = df.append(f.processed_data, ignore_index=True)
    return df



def filter_and_plot_laser_data_by_segment(df_original:DataFrame,
                           depth_header:Header,
                           sample_header:Header,
                           pdf):
    fig = plt.figure(figsize=(11, 8.5))
    plt.plot(df_original.loc[:, depth_header.name], df_original.loc[:, sample_header.name], label='original data')
#     plt.plot(df_filter.loc[:, depth_header.name],df_filter.loc[:, sample_header.name],label='filtered data')
    plt.xlabel(depth_header.label)
    plt.ylabel(sample_header.label)
    plt.title('Comparison of original and filtered data of %s' % (sample_header.hclass))
    plt.legend()
    pdf.savefig(fig)
    plt.close()
    
    
    

def clean_LAICPMS_data(f:LaserFile) -> DataFrame:  
    df = clean_data(f.raw_data)
    df = df[(df['Time'] > f.washin_time) & (df['Time'] < f.laser_time - f.washout_time)]
    df = df.reset_index(drop=True)
    df = add_depth_column(df, f.start_depth, f.end_depth)
    df = add_year_column(df, f.depth_age_file)
    df = df.drop('Time', 1)
    return df

# def filter_LAICPMS_data(df:DataFrame)->DataFrame:
#     df_filter=df[:]
#     
#     df_filter=replace_outliers_with_nan(df_filter)
#     
#     return df_filter

def add_depth_column(df:DataFrame, start_depth:float, end_depth:float) -> DataFrame:
    """
    """
    start_depth = start_depth / 100
    end_depth = end_depth / 100
    inc = (end_depth - start_depth) / (df.shape[0])
    depth_series = Series(np.arange(start_depth, end_depth, inc))
    df.insert(0, 'depth (m abs)', depth_series)
    return df

def add_year_column(df:DataFrame, depth_age_file:str) -> DataFrame:
    depth_age_df = pandas.read_table(depth_age_file)
    year_series = Series(np.interp(df['depth (m abs)'], depth_age_df['depth (m abs)'], depth_age_df['year']))
    df.insert(1, 'year', year_series)
    return df

# def store_background_information(f:LaserFile,df:DataFrame)->DataFrame:
#     background_df=df.copy()
#     background_df=background_df.loc[0:11,:]
#     #somehow label the background df with f
#     return background_df
# 
# def statistics_of_background_information(bg_info:DataFrame):
#     pass

# def compile_statistics_for_LAICPMS_data(df:DataFrame)->List[CompiledStat]:
#     '''
#     From the given data frame compile statistics (mean, median, min, max, etc) 
#     based on the parameters.
# 
#     '''
#     headers=process_header_data(df)
#     depth_headers=[h for h in headers if h.htype == HeaderType.DEPTH]
#     sample_headers=[h for h in headers if h.htype == HeaderType.SAMPLE]
#      
#     result_list = []
#     for depth_header in depth_headers:    
#         depth_df=DataFrame([[np.min(df.loc[:,depth_header.name]),np.max(df.loc[:,depth_header.name])]])
#         for sample_header in sample_headers:
#             current_stats = []
#             current_stats.extend(compileStats([df.loc[:,sample_header.name].tolist()]))
#             current_df = DataFrame(current_stats, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
#             comp_stat=CompiledStat(pandas.concat((depth_df,current_df),axis=1),depth_header,sample_header)
#         result_list.append(comp_stat)
#     return result_list

#     


