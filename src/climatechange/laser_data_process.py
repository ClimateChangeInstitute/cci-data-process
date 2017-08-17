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
from climatechange.resample_stats import compileStats
from climatechange.data_filters import replace_outliers_with_nan,\
    normalize_min_max_scaler


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
        self.background_info=compileStats(self.raw_data.iloc[0:11,1:].transpose().values.tolist())
        self.stats=compileStats(self.processed_data.iloc[:,2:].transpose().values.tolist())
        self.filtered_data=filtered_laser_data(self.processed_data)
        self.normalized_data=normalize_min_max_scaler(self.processed_data)

    def __str__(self):
        return self.file_path
    
    def __repr__(self):
        return self.__str__()
    

def readFile(file_path, laser_time, start_depth, end_depth, washin_time, 
             washout_time, depth_age_file) -> LaserFile:
                 
    return LaserFile(file_path, laser_time, start_depth, end_depth, washin_time, washout_time, depth_age_file)


def load_input_file(input_file:str, depth_age_file:str) -> List[LaserFile]:  # gets information from input file
    """
    """
    result = []
    input_folder = os.path.dirname(input_file)
    for line in open(input_file, 'r') :
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



def process_laser_data_by_run(f:LaserFile,pdf_folder:str) -> DataFrame:
    '''
    
    :param f:
    :param depth_age_file:
    :param path:
    
    :return: csv:original data, csv:filtered data, pdf: og data vs. filtered by depth
        list of list of stats 
    '''

    dir_name=os.path.basename(f.file_path)
    pdf_filename = pdf_folder+dir_name+'_original_vs._filtered_laser_data.pdf'

#     df_filter=filter_LAICPMS_data(laser_run_df)
    headers = process_header_data(f.processed_data)
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]
    depth_headers = [h for h in headers if h.htype == HeaderType.DEPTH]
    
    with PdfPages(pdf_filename) as pdf:
        for depth_header in depth_headers:
            for sample_header in sample_headers:
                filter_and_plot_laser_data(f.processed_data, depth_header, sample_header, pdf)


def combine_laser_data_by_input_file(input_file:str, depth_age_file:str,create_PDF=False) -> DataFrame:
      
    laser_files = load_input_file(input_file, depth_age_file)
    df = DataFrame()
    
    if create_PDF:
        pdf_folder=os.path.dirname(input_file)+'PDF_plots'
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        
    
    for f in laser_files:
        df = df.append(f.processed_data, ignore_index=True)
        if create_PDF:
            process_laser_data_by_run(f,pdf_folder)
        
        
    return df



def combine_laser_data_by_directory(directory:str,prefix:str,depth_age_file:str,create_PDF=False):
    '''
    
    :param directory:
    :param prefix:
    :param depth_age_file:
    
    - folders in directory should be named accordingly 
        that a dictionary sort will put them in correct order of appending
    - will lexicographical sort folders in directory
    '''
    input_1='InputFile_1'
    input_2='InputFile_2'
    df1=DataFrame()
    df2=DataFrame()
    
    if create_PDF:
        pdf_folder=os.path.join(directory,'PDF_plots')
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

    for folder in sorted(os.listdir(directory)):
        if folder.startswith(prefix):
            for file in sorted(os.listdir(os.path.join(directory,folder))):
                if file.startswith(input_1):
                    df1=df1.append(combine_laser_data_by_input_file(os.path.join(directory,folder,file),
                                                                    depth_age_file,create_PDF), ignore_index=True)
                elif file.startswith(input_2):
                    df2=df2.append(combine_laser_data_by_input_file(os.path.join(directory,folder,file),
                                                                    depth_age_file,create_PDF), ignore_index=True)
                    
    return df1,df2
                    
    #plot each sample by depth
                    
    
def process_laser_data_by_directory(df:DataFrame,pdf_folder,create_PDF=False):


    pdf_filename = os.path.join(pdf_folder,'all_original_vs._filtered_laser_data.pdf')
    if os.path.exists(pdf_filename):
        pdf_filename = os.path.join(pdf_folder,'all_original_vs._filtered_laser_data_2.pdf')
        
#     df_filter=filter_LAICPMS_data(laser_run_df)
    headers = process_header_data(df)
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]
    depth_headers = [h for h in headers if h.htype == HeaderType.DEPTH]
    
    with PdfPages(pdf_filename) as pdf:
        for depth_header in depth_headers:
            for sample_header in sample_headers:
                filter_and_plot_laser_data(df, depth_header, sample_header, pdf)



def filter_and_plot_laser_data(df:DataFrame,
                           depth_header:Header,
                           sample_header:Header,
                           pdf):
    fig = plt.figure(figsize=(11, 8.5))
    plt.plot(df.loc[:, depth_header.name], df.loc[:, sample_header.name], label='original data')
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

def filtered_laser_data(df:DataFrame)->DataFrame:
    df_filter=df[:]
     
    df_filter=replace_outliers_with_nan(df_filter,2)
     
    return df_filter

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



#     

