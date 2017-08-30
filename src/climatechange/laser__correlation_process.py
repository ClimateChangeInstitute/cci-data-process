'''
Created on Aug 28, 2017

@author: Heather
'''
from builtins import str
import os
import re
from typing import List, Tuple

from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame, Series
import pandas

from climatechange.headers import process_header_data, HeaderType, Header
from climatechange.plot import write_data_to_csv_files
from climatechange.process_data_functions import clean_data, correlate_stats,\
    plot_corr_stats, DataFile, correlate_laser_stats

import matplotlib.pyplot as plt
import numpy as np
from climatechange.laser_data_process import load_input_file, CombinedLaser,\
    LaserFile, combine_laser_data_by_input_file, plot_laser_data_by_directory
from climatechange.resample_data_by_depths import compiled_stats_HR_by_LR,\
    find_gaps
from matplotlib import pyplot
from climatechange.file import load_csv



def process_laser_data_by_input_file(input_file:str, depth_age_file:str, LR_file:str,createPDF) -> DataFrame:
      
    laser_files = load_input_file(input_file, depth_age_file)

    corr_stats=[]
    
    for f in laser_files:

        corr_stats.extend(resample_laser_by_LR(f, LR_file,createPDF))

    return corr_stats



def resample_laser_by_LR(f:LaserFile, LR_file:str,createPDF):
    '''
    
    Resample laser data by lower resolution

    a. Input: two datasets with corresponding years, depths, samples
    b. $ PYTHONPATH=. python climatechange/process_data.py -di ../test/csv_files/small.csv
        ../test/csv_files/small2.csv

    i. Take depth intervals of one dataset and resample second dataset by first dataset
    depth intervals
    b. Output: correlation between raw data and statistics of the same samples in both datasets
    
    '''
    f_LR=load_and_clean_LR(LR_file,f.processed_data)
    
    compiled_stats_of_df_laser = compiled_stats_HR_by_LR(f.processed_data, f_LR.df)
    
#     if createCSV:
#         find_gaps(f.processed_data, f_LR.df, pdf_folder, f.base)
    pdf_folder = os.path.join(os.path.dirname(os.path.dirname(f.file_path)), 'PDF_plots')
    
    if createPDF:
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        pdf_corr_stats = os.path.join(pdf_folder,'%s-%s_vs_ %s__plots.pdf' % (f.dirname,f.base,f_LR.base))
        with PdfPages(pdf_corr_stats) as pdf_cs:
            for cs_list in compiled_stats_of_df_laser:
                for cs in cs_list:
                    for sh_LR in f_LR.sample_headers:
                        if (sh_LR.hclass==cs.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity') \
                            | (cs.sample_header.hclass=='Dust') | (cs.sample_header.hclass=='Conductivity'):
                            for stat_header in cs.df.columns[2:5]:
                                if not stat_header=='Stdv':
                                    plot_corr_stats(cs,f_LR.df,sh_LR,stat_header,pdf_cs)
                                    pyplot.close()
        
    
    corr_stats=[]  
    for cs_list in compiled_stats_of_df_laser:
        for cs in cs_list:
            for sh_LR in f_LR.sample_headers:
                if (sh_LR.hclass==cs.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity') \
                        | (cs.sample_header.hclass=='Dust') | (cs.sample_header.hclass=='Conductivity'):


                    corr_stats.append((f.dirname,
                                       f.base,
                                       round((f.start_depth/100),4),
                                       round((f.end_depth/100),4),
                                       (round((f.end_depth/100),4)-round((f.start_depth/100),4)))+correlate_laser_stats(cs, f_LR,sh_LR))

    return corr_stats


def laser_data_process(directory:str,
                       depth_age_file:str,
                       LR_file:str,
                       createPDF=False,
                       createCSV=False,
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
    input_MR = 'InputFile_1'
    input_LR = 'InputFile_2'
    combined_laser_MR = CombinedLaser()
    combined_laser_LR = CombinedLaser()
    corr_stats_MR=[]
    corr_stats_LR=[]
 
    for folder in sorted(os.listdir(directory)):
        if folder.startswith(prefix):
            for file in sorted(os.listdir(os.path.join(directory, folder))):
                if file.startswith(input_MR):
                    combined_laser_MR = combined_laser_MR.append(combine_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                                  depth_age_file,
                                                                                                  createPDF))
                    
                    corr_stats_MR.extend(process_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                          depth_age_file,
                                                                                          LR_file,createPDF))


                    
                elif file.startswith(input_LR):
                    
                    combined_laser_LR = combined_laser_LR.append(combine_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                                  depth_age_file,
                                                                                                  createPDF), ignore_index=True)
                    corr_stats_LR.extend(process_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                          depth_age_file,
                                                                                          LR_file, createPDF))
    
    
    df_MR = DataFrame(corr_stats_MR)   
    df_LR = DataFrame(corr_stats_LR)
    all_dfs = [df_MR,df_LR]


    for df in all_dfs:
        df.columns = ['core ID','filename','top_depth_m_(abs)','end_depth_m_(abs)','length_m_(abs)', 'laser_sample', 'LR_sample', 'r_value:Mean', 'r_value:Median','linear equation:Mean','linear equation:Median']

    df_corr_stats=pandas.concat(all_dfs).reset_index(drop=True)
    if createPDF:
        pdf_folder = os.path.join(directory, 'PDF_plots')
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)  
        plot_laser_data_by_directory(combined_laser_MR.df,prefix, pdf_folder)
        plot_laser_data_by_directory(combined_laser_LR.df,prefix, pdf_folder)
#     
    if createCSV:
        csv_folder = os.path.join(directory, 'CSV_files')
        
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
            
        write_data_to_csv_files(combined_laser_MR.df, os.path.join(csv_folder, ('%s_laser_MR_%s.csv'%(prefix,os.path.basename(directory)))))
        write_data_to_csv_files(combined_laser_LR.df, os.path.join(csv_folder, ('%s_laser_LR_%s.csv'%(prefix,os.path.basename(directory)))))           
        csv_filename = os.path.join(csv_folder,'%s_and %s__statistical_correlation.csv' % (os.path.basename(directory),os.path.basename(LR_file).split('.')[0]))
        write_data_to_csv_files(df_corr_stats, csv_filename)
        
    return combined_laser_MR.df,combined_laser_LR.df


def load_and_clean_LR(LR_file:str, df_laser:DataFrame)->Tuple[DataFile,DataFile]:


    df_LR = load_csv(LR_file)
    df_LR = clean_data(df_LR)

    dh_LR = process_header_data(df_LR, HeaderType.DEPTH)
    dh_laser = process_header_data(df_laser, HeaderType.DEPTH)
    
    for depth1 in dh_LR:
        for depth2 in dh_laser:
            if depth1.name==depth2.name:
                
                df_LR=df_LR[(df_LR[depth1.name]>=min(df_laser[depth1.name])) & (df_LR[depth1.name] <=max(df_laser[depth1.name]))]
                break

    return DataFile(df_LR.reset_index(drop=True),LR_file)


