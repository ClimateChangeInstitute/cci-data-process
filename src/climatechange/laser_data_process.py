'''
Created on Aug 10, 2017

@author: Heather
'''
from builtins import str
import os
import re
from typing import List

from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame, Series
import pandas

from climatechange.data_filters import replace_outliers
from climatechange.headers import process_header_data, HeaderType, Header
from climatechange.plot import write_data_to_csv_files
from climatechange.process_data_functions import clean_data
from climatechange.resample_stats import compileStats
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
        self.background_info = compileStats(self.raw_data.iloc[0:11, 1:].transpose().values.tolist())
        self.stats = compileStats(self.processed_data.iloc[:, 2:].transpose().values.tolist())
#         self.filtered_data = filtered_laser_data(self.processed_data)
#         self.normalized_data=normalize_min_max_scaler(self.processed_data)

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



def plot_laser_data_by_run(f:LaserFile, pdf_folder:str) -> DataFrame:
    '''
    
    :param f:
    :param depth_age_file:
    :param path:
    
    :return: csv:original data, csv:filtered data, pdf: og data vs. filtered by depth
        list of list of stats 
    '''

    file_name = os.path.basename(f.file_path).split('.')[0]
    folder_name = os.path.basename(os.path.dirname(f.file_path))
    
    pdf_filename = os.path.join(pdf_folder, '%s-%s_original_vs._filtered_laser_data.pdf' % (folder_name, file_name))

#     df_filter=filter_LAICPMS_data(laser_run_df)
    sample_headers = process_header_data(f.processed_data, HeaderType.SAMPLE)
    depth_headers = process_header_data(f.processed_data, HeaderType.DEPTH)
    
    with PdfPages(pdf_filename) as pdf:
        for depth_header in depth_headers:
            for sample_header in sample_headers:
                plot_laser_data(f.processed_data, depth_header, sample_header, pdf)


def combine_laser_data_by_input_file(input_file:str, depth_age_file:str, create_PDF=False) -> DataFrame:
      
    laser_files = load_input_file(input_file, depth_age_file)
    df = DataFrame()
    
#     if create_PDF:
#         pdf_folder=os.path.join(os.path.dirname(os.path.dirname(input_file)),'PDF_plots')
#         if not os.path.exists(pdf_folder):
#             os.makedirs(pdf_folder)
        
    for f in laser_files:

        df = df.append(f.processed_data, ignore_index=True)
#         if create_PDF:
#             plot_laser_data_by_run(f,pdf_folder)
        
    return df



def combine_laser_data_by_directory(directory:str,
                                    depth_age_file:str,
                                    create_PDF=False,
                                    create_CSV=False,
                                    prefix:str='KCC'):
    '''
    Combine the laser data in the specified `directory`.  The folders with the 
    specified `prefix` in `directory` are processed in lexicographical order.
    
    :param directory: The root directory to process
    :param depth_age_file: The path to the depth age file
    :param create_PDF: If specified as `True`, PDFs will be generated 
    :param filtered_data: If specified as `True`, data will be filtered.  
        Currently this involves removing data points that are beyond 2 standard 
        deviations.
    :param create_CSV: If specified as `True`, CSV files will be generated for 
        the  data
    :param prefix: The prefix of the folders containing laser data to be 
        processed
    '''
    input_1 = 'InputFile_1'
    input_2 = 'InputFile_2'
    df1 = DataFrame()
    df2 = DataFrame()

    for folder in sorted(os.listdir(directory)):
        if folder.startswith(prefix):
            for file in sorted(os.listdir(os.path.join(directory, folder))):
                if file.startswith(input_1):
                    df1 = df1.append(combine_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                    depth_age_file, create_PDF), ignore_index=True)
                elif file.startswith(input_2):
                    df2 = df2.append(combine_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                    depth_age_file, create_PDF), ignore_index=True)
    
    if create_PDF:
        pdf_folder = os.path.join(directory, 'PDF_plots')
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)  
        plot_laser_data_by_directory(df1, pdf_folder)
        plot_laser_data_by_directory(df2, pdf_folder)
    
    if create_CSV:
        csv_folder = os.path.join(directory, 'CSV_files')
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
            #change names
        write_data_to_csv_files(df1, os.path.join(csv_folder, 'laser_filename.csv'))
        write_data_to_csv_files(df2, os.path.join(csv_folder, 'laser_filename2.csv'))           

    return df1, df2
    # plot each sample by depth
                    
    
def plot_laser_data_by_directory(df:DataFrame, pdf_folder):

    pdf_filename = os.path.join(pdf_folder, 'all_original_data_1.pdf')
    if os.path.exists(pdf_filename):
        pdf_filename = os.path.join(pdf_folder, 'all_original_data_2.pdf')
        
    sample_headers = process_header_data(df, HeaderType.SAMPLE)
    depth_headers = process_header_data(df, HeaderType.DEPTH)
    
    with PdfPages(pdf_filename) as pdf:
        for depth_header in depth_headers:
            for sample_header in sample_headers:
                plot_laser_data(df, depth_header, sample_header, pdf)
                
                
def plot_filtered_laser_data_by_directory(df:DataFrame, pdf_folder):

    pdf_filename = os.path.join(pdf_folder, 'all_filtered_data_1.pdf')
    if os.path.exists(pdf_filename):
        pdf_filename = os.path.join(pdf_folder, 'all_filtered_data_2.pdf')
            
    sample_headers = process_header_data(df, HeaderType.SAMPLE)
    depth_headers = process_header_data(df, HeaderType.DEPTH)
    
    with PdfPages(pdf_filename) as pdf:
        for depth_header in depth_headers:
            for sample_header in sample_headers:
                plot_laser_data(df, depth_header, sample_header, pdf)



def plot_laser_data(df:DataFrame,
                           depth_header:Header,
                           sample_header:Header,
                           pdf):
    fig = plt.figure(figsize=(11, 8.5))
    plt.semilogy(df.loc[:, depth_header.name], df.loc[:, sample_header.name])
    plt.xlabel(depth_header.label)
    plt.ylabel(sample_header.label)
    plt.title('LA-ICP-MS-%s' % (sample_header.hclass))
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

def filtered_laser_data(df:DataFrame) -> DataFrame:
    '''
    Filter the given data by removing data points that are outside of 2 
    standard deviations of the mean and replacing them with :data:`np.nan`. 
    Modification occur in-place.
    
    :param df: The data to be processed.
    :return: The modified data
    '''
    return replace_outliers(df)

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




