'''
Created on Aug 28, 2017

@author: Heather
'''
from builtins import str
import os

from typing import List, Tuple

from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame, Series
import pandas

from climatechange.headers import process_header_data, HeaderType, Header
from climatechange.plot import write_data_to_csv_files
from climatechange.process_data_functions import clean_data, correlate_stats,\
    plot_corr_stats, DataFile, correlate_laser_stats, plot_corr_stats_directory,\
    DataClass, to_same_length, remove_nan_from_datasets

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from climatechange.laser_data_process import load_input_file, CombinedLaser,\
    LaserFile, combine_laser_data_by_input_file, plot_laser_data_by_directory
from climatechange.resample_data_by_depths import compiled_stats_HR_by_LR,\
    find_gaps, index_by_increment,\
    create_top_bottom_depth_dataframe
from matplotlib import pyplot
from climatechange.file import load_csv
from climatechange.compiled_stat import CompiledStat
import matplotlib.mlab as mlab
from climatechange.data_filters import default_filters
from scipy.stats import linregress
from climatechange.resample_stats import compileStats

class DFClass():
    
    def __init__(self, df:DataFrame,key):
        

        self.df = df
        self.name = key.__name__
        self.sample_headers = process_header_data(self.df, HeaderType.SAMPLE) 
        self.depth_headers = process_header_data(self.df, HeaderType.DEPTH) 
        self.year_headers = process_header_data(self.df, HeaderType.YEARS) 
    



def compiled_stats_laser_by_LR(f_HR:DFClass, f_LR:DataFile) -> List[List[CompiledStat]]:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc)
    based on the parameters.

    :param df1:Larger Dataframe with smaller intervals to create a compiled stat
    :param df2:Smaller Dataframe with larger intervals to create index of intervals
    :return: A list of list of CompiledStat containing the resampled statistics for the
    specified sample and depth by the depth interval from df2.
    '''
    
    df1,df2 = to_same_length(f_HR.df.copy(),f_LR.df.copy())
    result_list = []
    for dh_HR in f_HR.depth_headers:
        for dh_LR in f_LR.depth_headers:
            if dh_HR == dh_LR:
                index = index_by_increment(f_HR.df.loc[:, dh_HR.name].tolist(), f_LR.df.loc[:, dh_LR.name].tolist())
                depth_df = create_top_bottom_depth_dataframe(f_LR.df, dh_LR)
                
                depth_samples = []
                for sample_header in f_HR.sample_headers:
                    
                    current_stats = []
                    for i in index:
                        current_stats.append(compileStats(f_HR.df.loc[i, sample_header.name].tolist()))
                        
                    current_df = DataFrame(current_stats, columns=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count'])
                    comp_stat = CompiledStat(pandas.concat((depth_df, current_df), axis=1), dh_HR, sample_header)
                    depth_samples.append(comp_stat)
        result_list.append(depth_samples)
    return result_list


def process_laser_data_by_input_file(input_file:str, depth_age_file:str, LR_file:str,createPDF, filters_to_apply = default_filters) -> DataFrame:
      
    laser_files = load_input_file(input_file, depth_age_file,default_filters)

    corr_stats=[]
    
    for f in laser_files:

        corr_stats.extend(resample_laser_by_LR(f, LR_file,createPDF))

    return corr_stats



def resample_laser_by_LR(f:LaserFile, LR_file:str, createPDF):
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
#     pdf_folder = os.path.join(os.path.dirname(os.path.dirname(f.file_path)), 'PDF_plots')
    
    if createPDF:
        pdf_folder = os.path.join(os.path.dirname(os.path.dirname(f.file_path)), 'PDF_plots')
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        pdf_corr_stats = os.path.join(pdf_folder,'%s-%s_vs_ %s__plots_savgol.pdf' % (f.dirname,f.base,f_LR.base))
        with PdfPages(pdf_corr_stats) as pdf_cs:
            for cs_list in compiled_stats_of_df_laser:
                for cs in cs_list:
                    for sh_LR in f_LR.sample_headers:
                        if not (cs.sample_header.hclass == 'Si') | (cs.sample_header.hclass == 'S'):
                            if (sh_LR.hclass==cs.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity') \
                            | (cs.sample_header.hclass=='Dust') | (cs.sample_header.hclass=='Conductivity'):
                                plot_corr_stats(cs,f_LR.df,sh_LR,'Mean',pdf_cs)
                                pyplot.close()
        
    
    corr_stats=[]  
    for cs_list in compiled_stats_of_df_laser:
        for cs in cs_list:
            for sh_LR in f_LR.sample_headers:
                if not (cs.sample_header.hclass == 'Si') | (cs.sample_header.hclass == 'S'):
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
                       prefix:str='KCC',
                       filters_to_apply = default_filters):
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
                                                                                                  createPDF,filters_to_apply))
                    
                    corr_stats_MR.extend(process_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                          depth_age_file,
                                                                                          LR_file,createPDF,filters_to_apply))


                    
                elif file.startswith(input_LR):
                    
                    combined_laser_LR = combined_laser_LR.append(combine_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                                  depth_age_file,
                                                                                                  createPDF,filters_to_apply))
                    corr_stats_LR.extend(process_laser_data_by_input_file(os.path.join(directory, folder, file),
                                                                                          depth_age_file,
                                                                                          LR_file, createPDF,filters_to_apply))
    
 
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
        plot_laser_directory_resampled_by_LR(combined_laser_MR,LR_file,pdf_folder,'MR')
        plot_laser_directory_resampled_by_LR(combined_laser_LR,LR_file,pdf_folder,'LR')
        histogram_laser_data(combined_laser_MR,LR_file,pdf_folder,'MR')
        histogram_laser_data(combined_laser_LR,LR_file,pdf_folder,'LR')

    if createCSV:
        csv_folder = os.path.join(directory, 'CSV_files')
        
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
            
        write_data_to_csv_files(combined_laser_MR.df, os.path.join(csv_folder, ('%s_laser_MR_%s_savgol.csv'%(prefix,os.path.basename(directory)))))
        write_data_to_csv_files(combined_laser_LR.df, os.path.join(csv_folder, ('%s_laser_LR_%s_savgol.csv'%(prefix,os.path.basename(directory)))))           
        csv_filename = os.path.join(csv_folder,'%s_and %s__statistical_correlation_savgol.csv' % (os.path.basename(directory),os.path.basename(LR_file).split('.')[0]))
        write_data_to_csv_files(df_corr_stats, csv_filename)
        
    return combined_laser_MR.df,combined_laser_LR.df






def plot_laser_directory_resampled_by_LR(combined_laser:CombinedLaser,LR_file:str,pdf_folder:str,resolution:str):
    
    f_LR=load_and_clean_LR(LR_file,combined_laser.df)
    
    compiled_stats_of_df_HR = compiled_stats_HR_by_LR(combined_laser.df, f_LR.df)
    
    pdf_corr_stats = os.path.join(pdf_folder,'laser_%s_vs_%s_plots_savgol.pdf' % (resolution,f_LR.base))
    with PdfPages(pdf_corr_stats) as pdf_cs:
        for cs_list in compiled_stats_of_df_HR:
            for cs in cs_list:
                for sh_LR in f_LR.sample_headers:
                    if not (cs.sample_header.hclass == 'Si') | (cs.sample_header.hclass == 'S'):
                        if (sh_LR.hclass==cs.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity') \
                            | (cs.sample_header.hclass=='Dust') | (cs.sample_header.hclass=='Conductivity'):
                            plot_corr_stats_directory(cs,f_LR.df,sh_LR,'Mean',pdf_cs)
                            pyplot.close()
                                
                                
def histogram_laser_data(combined_laser:CombinedLaser,LR_file:str,pdf_folder:str,resolution:str):
    
    f_LR=load_and_clean_LR(LR_file,combined_laser.df)

    compiled_stats_of_df_HR = compiled_stats_HR_by_LR(combined_laser.df, f_LR.df)
    
    pdf_hist = os.path.join(pdf_folder,'laser_%s_hist_plots.pdf' % (resolution))
    with PdfPages(pdf_hist) as pdf:
        for cs_list in compiled_stats_of_df_HR:
            for cs in cs_list:
                for stat_header in cs.df.columns[2:5]:
                    if not stat_header=='Stdv':
                        plot_histogram(cs,stat_header,pdf)
                        pyplot.close()
                        
    pdf_hist_LR = os.path.join(pdf_folder,'CFA_%s_hist_plots.pdf' % (resolution))
    with PdfPages(pdf_hist_LR) as pdf:
        for sample_header in f_LR.sample_headers:
            plot_histogram_LR(f_LR.df,sample_header,pdf)
            pyplot.close()


def plot_histogram_LR(df:DataFrame,
                    sample_header:Header,
                    pdf):

    plt.figure(figsize=(11, 8.5))
    fig,ax=plt.subplots()

    mu = df[sample_header.name].mean()
    sigma = df[sample_header.name].std()

    num_bins = 100

    n, bins, patches = ax.hist(df[sample_header.name].dropna(), num_bins, normed=1)

    y = mlab.normpdf(bins, mu, sigma)

    ax.plot(bins, y, '--')
    ax.set_xlabel('Concentration')
    ax.set_ylabel('Probability density')
    ax.set_title('CFA_%s_Concentration_Distribution'%(sample_header.hclass))
    pdf.savefig(fig)
    plt.close()
    
def plot_histogram(d1:CompiledStat,
                        stat_header:str,
                        pdf):

    plt.figure(figsize=(11, 8.5))
    fig,ax=plt.subplots()

    mu = d1.df[stat_header].mean()
    sigma = d1.df[stat_header].std()

    num_bins = 100

    n, bins, patches = ax.hist(d1.df[stat_header].dropna(), num_bins, normed=1)

    y = mlab.normpdf(bins, mu, sigma)

    ax.plot(bins, y, '--')
    ax.set_xlabel('Normalized intensity')
    ax.set_ylabel('Probability density')
    ax.set_title('LAICPMS_%s_%s_Intensity_Distribution'%(d1.sample_header.hclass,stat_header))
    pdf.savefig(fig)
    plt.close()

    

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

    


def filtered_df(laser_file:LaserFile)-> List[DataFrame]:
    
    return [DFClass(val,key) for key, val in laser_file.filter_data.items()]



def compile_corr_stats_of_filtered_df(f:LaserFile,f_LR:DataClass):
    
    
    filtered = filtered_df(f)
    
    compiled_correlation = []
    for df_class in filtered:
        df1,df2 = to_same_length(df_class.df.copy(),f_LR.df.copy())

        cs_filter = compiled_stats_HR_by_LR(df1,df2)

        corr_stats=[]  
        for cs_list in cs_filter:
            for HR in cs_list:
                for sh_LR in f_LR.sample_headers:
                    if not (HR.sample_header.hclass == 'Si') | (HR.sample_header.hclass == 'S'):
                        if (sh_LR.hclass==HR.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity'):
                            r_val =[df_class.name, f.dirname, f.base]
                            r_val.extend(correlate_mean(HR, df2, sh_LR))
#                             print(r_val)

                             
                            corr_stats.append(r_val)
        corr_stats_df = DataFrame(corr_stats)
        corr_stats_df.columns = ['filter','coreID','filename','laser_sample','CFA_sample','r_value'] 
#         print(corr_stats_df)             
        compiled_correlation.append(corr_stats_df)

    return compiled_correlation

def correlate_mean(d1:CompiledStat, LR_df:DataFrame, sample_header:Header) -> Tuple[float, float, float, List[float]]:

    s1,s2 = remove_nan_from_datasets(d1.df['Mean'], LR_df[sample_header.name])

    if (check_all_nan(s1) == True) | (check_all_nan(s2) == True):
        return [d1.sample_header.hclass, sample_header.hclass, np.nan]
    else:
        slope, intercept, r_value, p_value, std_err = linregress(s1,s2)
        return [d1.sample_header.hclass, sample_header.hclass, r_value]
 

def find_mean_r_val(filtered_df:List[DataFrame]):
    
    mean_r_val = [np.nanmean(df['r_value']) for df in filtered_df]
#     print(mean_r_val)
    m = max(mean_r_val)
#     print(m)
    if not np.isnan(m):
        max_val = pd.Series(m, index = ['max_mean'])
        max_df = [filtered_df[i] for i, j in enumerate(mean_r_val) if j == m]  
#         print(max_df) 
        max_series = max_df[0].ix[1,0:3]
        max_series = max_series.append(max_val)
        max_series_df = DataFrame([max_series], columns = ['filter','coreID','filename','max_mean'] )
        return  max_series_df
    else:
        
        nan_series = filtered_df[0].ix[1,0:3]
        nan_all = pd.Series('all_nans')
        nan_series = nan_series.append(nan_all)
        nan_df = DataFrame([nan_series],columns = ['filter','coreID','filename','max_mean'] )
        return nan_df
        
def check_all_nan(iterable):
    all_nan = True
    for item in iterable:
        if not np.isnan(item):
            all_nan= False
            break
    return all_nan

        
def compare_correlated_stats(input_file, depth_age_file, LR_file,filters_to_apply):
    
    laser_files = load_input_file(input_file, depth_age_file, filters_to_apply)
    f_LR = DataClass(LR_file)
    
    filter_df = DataFrame()
    for f in laser_files:

        filter_df = filter_df.append(find_mean_r_val(compile_corr_stats_of_filtered_df(f,f_LR)))

    return filter_df
        
    
        
        
def laser_correlate_process(directory:str,
                       depth_age_file:str,
                       LR_file:str,
                       prefix:str='KCC',
                       filters_to_apply = default_filters):

    input_MR = 'InputFile_1'
    input_LR = 'InputFile_2'

    corr_stats_MR=DataFrame()
    corr_stats_LR=DataFrame()
    
    for folder in sorted(os.listdir(directory)):
        if folder.startswith(prefix):
            for file in sorted(os.listdir(os.path.join(directory, folder))):
                if file.startswith(input_MR):

                    corr_stats_MR = corr_stats_MR.append(compare_correlated_stats(os.path.join(directory, folder, file),
                                                                                          depth_age_file,
                                                                                          LR_file,
                                                                                          filters_to_apply))
                elif file.startswith(input_LR):
                    
                    corr_stats_LR = corr_stats_LR.append(compare_correlated_stats(os.path.join(directory, folder, file),
                                                                                          depth_age_file,
                                                                                          LR_file, 
                                                                                          filters_to_apply))
    all_dfs = [corr_stats_MR,corr_stats_LR]

    for df in all_dfs:
        df.columns = ['filter','coreID','filename','max_mean']

    df_corr_stats=pandas.concat(all_dfs).reset_index(drop=True)
    
    create_CSV_in_folder(directory, df_corr_stats,LR_file)


def create_CSV_in_folder(directory:str, to_csv:DataFrame, LR_file):

    csv_folder = os.path.join(directory, 'CSV_files')
    
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
   
    csv_filename = os.path.join(csv_folder,'%s_and %s_filter_correlation.csv' % (os.path.basename(directory),os.path.basename(LR_file).split('.')[0]))
    write_data_to_csv_files(to_csv, csv_filename)
        

        
        
        
        
        
        
        
        
        
        
    
    







