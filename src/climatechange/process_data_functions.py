'''
Created on Jul 24, 2017

:author: Mark Royer
'''

from builtins import float
import datetime
import logging
from math import isnan
from math import nan
import os
import sys
from typing import List, Tuple

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from numpy import float64
from pandas import DataFrame, Series
from scipy.stats._stats_mstats_common import linregress

from climatechange.compiled_stat import CompiledStat
from climatechange.file import load_csv
from climatechange.headers import HeaderDictionary, HeaderType, Header, \
    load_headers, process_header_data
from climatechange.plot import write_data_to_csv_files, \
    add_compile_stats_to_pdf
from climatechange.readme_output import create_readme_output_file, \
    write_readmefile_to_txtfile, template
from climatechange.resample_data_by_depths import compiled_stats_HR_by_LR, \
    find_index_by_increment,create_range_for_depths, resampled_depths
from climatechange.resample_stats import create_range_by_year,\
    resampled_depths_by_years, resampled_statistics

import matplotlib.pyplot as plt
import numpy as np
import time
import pandas

class DataFile():

    def __init__(self, df:DataFrame=DataFrame(), file_path:str=[]):
        
        self.df = df
        self.file_path = file_path
        self.base=os.path.basename(self.file_path).split('.')[0]
        self.dirname=os.path.dirname(self.file_path)
        self.sample_headers = process_header_data(df, HeaderType.SAMPLE) 
        self.depth_headers = process_header_data(df, HeaderType.DEPTH) 
        self.year_headers = process_header_data(df, HeaderType.YEARS) 

class DataClass():

    def __init__(self, file_path:str=[]):
        
        self.file_path = file_path
        self.df = clean_data(load_csv(self.file_path))
        self.base=os.path.basename(self.file_path).split('.')[0]
        self.dirname=os.path.dirname(self.file_path)
        self.sample_headers = process_header_data(self.df, HeaderType.SAMPLE)
        self.sample_headers_name = [sample.name for sample in self.sample_headers] 
        self.depth_headers = process_header_data(self.df, HeaderType.DEPTH) 
        self.depth_headers_name = [sample.name for sample in self.depth_headers] 
        self.year_headers = process_header_data(self.df, HeaderType.YEARS)
        self.sample_df =self.df[self.sample_headers_name]
        for name in self.depth_headers_name:
            self.sample_df[name] = pandas.Series(self.df[name])
            self.sample_df = self.sample_df.set_index([name])
            break
            

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def clean_data(df):
    
    # Remove zeroes.  Zeroes go to nan
    values = df.values
    

    
    # Replace str values with nan
    for r in values :
        for i in range(len(r)):
            if is_number(r[i]):
                r[i] = float64(r[i])
            else:
                r[i] = float64(nan) 

    for r in values :
        for i in range(len(r)):
            if r[i] == 0:
                r[i] = float64(nan)
                
    
    df = DataFrame(data=values,
                   index=df.index,
                   columns=df.columns,
                   dtype=float64)
    
    return df

def get_compiled_stats_by_year(df:DataFrame, headers:List[Header],inc_amt:int,) -> List[List[CompiledStat]]:
    year_headers = [h for h in headers if h.htype == HeaderType.YEARS]
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]
    
    compiled_stats = []
    for year_header in year_headers:
        range_list=create_range_by_year(df.loc[:,year_header.name].values.tolist(), inc_amt)
        index,top_range=find_index_by_increment(df.loc[:,year_header.name].values.tolist(),range_list)
        df_years=DataFrame(range_list, columns=[year_header.label])
        df_depth=resampled_depths_by_years(df,headers,index)
        cur_year = []
        for sample_header in sample_headers:
            df_stats = resampled_statistics(df, sample_header, index)
            cur_year.append(CompiledStat(pandas.concat([df_years, df_depth, df_stats], axis=1), year_header, sample_header))

        compiled_stats.append(cur_year)
    
    return compiled_stats


def round_values_to_sigfig(df:DataFrame):
    year_round_amt = 0
    depth_round_amt = 4
    sample_round_amt = 3
    df.iloc[:, 0] = [np.round(i, year_round_amt) for i in df.iloc[:, 0]]
    for col in range(1, 5):
        df.iloc[:, col] = [np.round(i, depth_round_amt) for i in df.iloc[:, col]]
    for col in range(5, 10):
        df.iloc[:, col] = [np.round(i, sample_round_amt) for i in df.iloc[:, col]]

    return df

def round_laser_values_to_sigfig(df:DataFrame):
    year_round_amt = 4
    depth_round_amt = 5
    sample_round_amt = 3
    df.iloc[:, 0] = [np.round(i, depth_round_amt) for i in df.iloc[:, 0]]
    for col in range(0, 1):
        df.iloc[:, col] = [np.round(i, year_round_amt) for i in df.iloc[:, col]]
    for col in range(2, 6):
        df.iloc[:, col] = [np.round(i, sample_round_amt) for i in df.iloc[:, col]]

    return df

def round_depth_values_to_sigfig(df:DataFrame):
    depth_round_amt = 4
    sample_round_amt = 3
    for col in range(0, 2):
        df.iloc[:, col] = [np.round(i, depth_round_amt) for i in df.iloc[:, col]]
    for col in range(2, 7):
        df.iloc[:, col] = [np.round(i, sample_round_amt) for i in df.iloc[:, col]]
    return df
    
        
def add_units_to_stats(df:DataFrame, sample_header:Header) -> DataFrame:
    df.rename(columns={'Mean':'mean_%s' % sample_header.label,
                       'Median':'median_%s' % sample_header.label,
                       'Max':'max_%s' % sample_header.label,
                       'Min':'min_%s' % sample_header.label,
                       'Stdv':'stdev_%s' % sample_header.label,
                       'Count':'count_(#pts/inc)'}, inplace=True) 
    return df   


def load_and_clean_year_data(f:str, inc_amt:int) -> Tuple[DataFrame, List[List[CompiledStat]], List[Header]]:
    '''
    Load data from the specified file path, and convert zeroes and strings 
    into :data:`math.nan`.  Finally, create compiled statistics for each sample using the increment amount
     
    :param f: The file path containing the data to load and clean
    :param inc_amt: The amount to group the year column by.  For example, 
        2012.6, 2012.4, 2012.2 would all be grouped into the year 2012.
    '''
    df = load_csv(f)
    headers = process_header_data(df)
    
    # Exit the progam if there are unknown headers
    if [h for h in headers if h.htype == HeaderType.UNKNOWN]:
        sys.exit(0)
#             df = clean_data(df.drop_duplicates())
#     return df.reset_index(drop=True), headers    
    df = clean_data(df)
    df=df[::-1]
    return df, get_compiled_stats_by_year(inc_amt, df, headers), headers


def resample_by_years(f:str, inc_amt:int=1,stat_header:str='Mean'):
    '''
    Resampler by Years
    a. Input: dataset with years, depths, samples
    
    $ PYTHONPATH=. python climatechange/process_data.py -year_name ../test/csv_files/small.csv

    a. Output: csv file with statistics for each sample by years

    i. Pdf of statistics by years with raw data

    1. Mean w/ raw, median w/ raw (by years) on same plot for each year column
    have 1 pdf with mean and median for each sample
    
    :param: f: This is a CSV file
    '''
    logging.info("Creating pdf for %s", f)
    start_time=time.time()

    df, compiled_stats, headers = load_and_clean_year_data(f, inc_amt)

    for cur_year in compiled_stats:

        pdf_filename = (os.path.splitext(f)[0] + '_plots_Resampled_%s_%s_Resolution.pdf' % (inc_amt, cur_year[0].x_header.name))
        with PdfPages(pdf_filename) as pdf:
            for c in cur_year:

                add_compile_stats_to_pdf(os.path.splitext(f)[0],
                                         df,
                                         c.df,
                                         pdf,
                                         c.x_header,
                                         c.sample_header,
                                         inc_amt,
                                         'Year',
                                         stat_header)    
                pyplot.close()
            
                csv_filename = os.path.splitext(f)[0] + '_stats_Resampled_%s_%s_Resolution_for_%s_afterchange.csv' % (inc_amt,
                                                                         c.x_header.label,
                                                                         c.sample_header.hclass.replace("/", ""))

                to_csv_df = add_units_to_stats(round_values_to_sigfig(c.df[:]), c.sample_header)
                write_data_to_csv_files(to_csv_df,
                                              csv_filename)

    readme = create_readme_output_file(template,
                                       f,
                                       headers,
                                       str(datetime.date.today()),
                                       inc_amt,
                                       'Year',
                                       [h.label for h in headers if h.htype == HeaderType.YEARS],
                                       compiled_stats[0][0].df.columns.values.tolist(),
                                       sum(len(c) for c in compiled_stats),
                                       stat_header)
    
    write_readmefile_to_txtfile(readme, os.path.join(os.path.dirname(f), '00README.txt'))
    
    print('Resample by years time:%s min' %((time.time()-start_time)/60.))


def get_compiled_stats_by_depth(df:DataFrame,
                                headers:List[Header],
                                inc_amt:float,) -> List[List[CompiledStat]]:
    '''
    Create statistics for every depth column vs every sample column, which 
    results in a list of compiled statistics of each sample for every depth 
    column. 
    :param inc_amt: The amount to group the depths by
    :param df: The original data
    :param headers: The processed headers for the original data
    :return: A list of statistics for each sample for every depth column
    '''
    depth_headers = [h for h in headers if h.htype == HeaderType.DEPTH]
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]
    compiled_stats = []
    for depth_header in depth_headers:
        cur_depth = []
        range_list=create_range_for_depths(df.loc[:, depth_header.name].values.tolist(),inc_amt)
        index,top_range = find_index_by_increment(df.loc[:, depth_header.name].values.tolist(),range_list) 
        df_depths = resampled_depths(top_range, depth_header, inc_amt)
        for sample_header in sample_headers:
            df_stats = resampled_statistics(df,sample_header, index)
            cur_depth.append(CompiledStat(pandas.concat([df_depths, df_stats], axis=1), depth_header, sample_header))
        compiled_stats.append(cur_depth)
    
    return compiled_stats
    


def load_and_clean_depth_data(f:str, inc_amt:float) -> Tuple[DataFrame,
                                                             List[List[CompiledStat]],
                                                             List[Header]]:
    '''
    
    :param f: The file path of data to load and clean
    :param inc_amt: The increment amount
    :return: A 3-tuple containing the original data, a list of lists of 
        compiled statistics, and the processed data headers from the original 
        data file
    '''
    df = load_csv(f)
    headers = process_header_data(df)
    df = clean_data(df)
    return df, get_compiled_stats_by_depth(df, headers,inc_amt), headers

def resample_by_depths(f:str, inc_amt:float,stat_header:str='Mean'):
    '''
    Resampler by Depths
    
    a. Input: dataset with years, depths, samples
        -input: file, increment amount
    b. $ PYTHONPATH=. python climatechange/process_data.py -d ../test/csv_files/small.csv
    c. Output: csv file with statistics for each sample by depths

    cur_depth. Pdf of statistics by depths with raw data
    
    1. Mean w/ raw, median w/ raw (by depths) on same plot for each year column
    have 1 pdf with mean and median for each sample
    
    :param f: The CSV file containing the data 
    '''
    logging.info("Resampling by depths file:%s, inc_amt:%f, stat_header:%s",
                 f, inc_amt, stat_header)
    
    df, compiled_stats, headers = load_and_clean_depth_data(f, inc_amt)

    
    for cur_depth in compiled_stats:
        file_name = (os.path.splitext(f)[0] + '_plots_Resampled_%s_inc_%s_resolution.pdf' % (inc_amt, cur_depth[0].x_header.name))
        with PdfPages(file_name) as pdf:
            for c in cur_depth:
                add_compile_stats_to_pdf(os.path.splitext(f)[0],
                                         df,
                                         c.df,
                                         pdf,
                                         c.x_header,
                                         c.sample_header,
                                         inc_amt,
                                         'Depth',
                                         stat_header)    
                pyplot.close()
            
                csv_filename = os.path.splitext(f)[0] + '_stats_Resampled %s_inc_%s_Resolution_for_%s.csv' % (inc_amt,
                                                                        c.x_header.label,
                                                                        c.sample_header.label.replace("/", ""))

                to_csv_df = add_units_to_stats(round_depth_values_to_sigfig(c.df[:]), c.sample_header)
                write_data_to_csv_files(to_csv_df,
                                              csv_filename)      

    readme = create_readme_output_file(template,
                                       f,
                                       headers,
                                       str(datetime.date.today()),
                                       inc_amt,
                                       'Depth',
                                       [h.name for h in headers if h.htype == HeaderType.DEPTH] ,
                                       compiled_stats[0][0].df.columns.values.tolist(),
                                       sum(len(c) for c in compiled_stats),
                                       stat_header)
    
    write_readmefile_to_txtfile(readme, os.path.join(os.path.dirname(f), '00README.txt'))     

def remove_nan_from_datasets(d1_stat:Series, d2_stat:Series) -> Tuple[Series, Series]:
    d2_result = []
    d1_result = []
    for i in range(len(d1_stat)):
        if not isnan(d1_stat[i]) and not isnan(d2_stat[i]):
            d1_result.append(d1_stat[i])
            d2_result.append(d2_stat[i])
            
    return Series(d1_result), Series(d2_result)
            
            
def remove_nan_from_data_and_namecolumn(d1_stat:Series, d2_stat:Series) -> Tuple[Series, Series]:
    d2_result = []
    d1_result = []
    for i in range(len(d1_stat)):
        if not isnan(d1_stat[i]):
            d1_result.append(d1_stat[i])
            d2_result.append(d2_stat[i])
                     
                     
    return Series(d1_result), Series(d2_result)

def remove_nan_from_data(d1:Series) -> Series:
    d1_result = []
    for i in range(len(d1)):
        if not isnan(d1[i]):
            d1_result.append(d1[i])
 
    return Series(d1_result).reset_index(drop=True)
                   
def correlate_samples(d1:CompiledStat, d2:CompiledStat, stat_header:str='Mean') -> Tuple[float, float, float, float, float]:
    d1_stat = d1.df.loc[:, stat_header]
    d2_stat = d2.df.loc[:, stat_header]
    
    slope, intercept, r_value, p_value, std_err = linregress(remove_nan_from_datasets(d1_stat, d2_stat))
    return d1.x_header.name, d1.sample_header.name, d2.sample_header.name, slope, intercept, r_value, p_value, std_err

    
def double_resample_by_depths(f1:str, f2:str, inc_amt:float):
    '''
    Double Resampler by Depths

    a. Input: two datasets with corresponding years, depths, samples
    Input: two files, one increment amount
    -call resample_by _depths for each file
    -create new function to correlate, run statistical analysis of both
    b. $ PYTHONPATH=. python climatechange/process_data.py -dd ../test/csv_files/small.csv
    ../test/csv_files/small2.csv
    c. Output: correlation between raw data and statistics of the same samples in both datasets
    i. Pdf of correlation between same samples
    
    :param f1:
    :param f2:
    '''

    unused_df1, compiled_stats1, unused_headers1 = load_and_clean_depth_data(f1, inc_amt)
    unused_df2, compiled_stats2, unused_headers2 = load_and_clean_depth_data(f2, inc_amt)
    f1_file_path = os.path.splitext(f1)[0]
    f2_base = os.path.basename(f2).split('.')[0]
    
    csv_filename = f1_file_path + '_vs_ %s__stat_correlation.csv' % (f2_base)
    

    print(csv_filename)
    corr_stats = []
    for dlist1 in compiled_stats1:
        for dlist2 in compiled_stats2:
            for d1 in dlist1:
                for d2 in dlist2:
                    if d1.x_header.name == d2.x_header.name:
                        print("Processing depth %s" % d1.x_header.name)
 
 
                        # correlate
                        print("correlating %s and %s" % (d1.sample_header.name, d2.sample_header.name))
                        corr_stats.append(correlate_samples(d1, d2))
    df_corr_stats = DataFrame(corr_stats, columns=['depth', 'sample_1', 'sample_2', 'slope', 'intercept', 'r_value', 'p_value', 'std_err'])    
    
    write_data_to_csv_files(df_corr_stats, csv_filename)  


def load_and_clean_dd_data(f:str) -> Tuple[DataFrame, List[Header]]:
    '''
    
    :param f: The file path of data to load and clean
    :return: A 2-tuple containing the cleaned original data,
     and the processed data headers from the original data file
    '''
    df = load_csv(f)
    headers = process_header_data(df)
    df = clean_data(df.drop_duplicates())
    return df.reset_index(drop=True), headers    
 

def correlate_dd_samples(d1:CompiledStat, d2:Series,stat_header:str='Mean') -> Tuple[float, float, float, float, float]:
    d1_stat = d1.df.loc[:, stat_header]
     
    slope, intercept, r_value, p_value, std_err = linregress(remove_nan_from_datasets(d1_stat, d2))
    return d1.x_header.name, d1.sample_header.name, d2.name, slope, intercept, r_value, p_value, std_err

def correlate_laser_stats(d1:CompiledStat, data_file:DataFile, sample_header:Header) -> Tuple[float, float, float, List[float]]:
    
    r_val=[]
    equation=[]
    d2=data_file.df[sample_header.name]
    for stat_header in d1.df.columns[2:5]:
        if not stat_header=='Stdv':
            d1_stat = d1.df.loc[:, stat_header]
            if len(d1_stat)!= len(d2):
                print(d1_stat)
                print(d2)
            slope, intercept, r_value, p_value, std_err = linregress(d1_stat, d2)
            r_val.append(round(r_value,4))
            equation.append('y= %.5f * x + %.4f'%(slope,intercept))
    return (d1.sample_header.hclass, sample_header.hclass)+ tuple(r_val)+tuple(equation)

def correlate_stats(d1:CompiledStat, data_file:DataFile, sample_header:Header) -> Tuple[float, float, float, List[float]]:
    
    r_val=[]
    d2=data_file.df[sample_header.name]
    for stat_header in d1.df.columns[2:7]:
        if not stat_header=='Stdv':
            d1_stat = d1.df.loc[:, stat_header]
            slope, intercept, r_value, p_value, std_err = linregress(d1_stat, d2)
            r_val.append(round(r_value,4))
    return (d1.x_header.name,d1.sample_header.name, sample_header.name)+ tuple(r_val)
                                                                    
def plot_corr_stats(d1:CompiledStat,
                        d2:DataFrame,
                        sample_header:Header,
                        stat_header:'str',
                        pdf_cs):
    
    plt.figure(figsize=(11, 8.5))
    fig,ax=plt.subplots()

    ax2=ax.twinx()
    lns1=ax.plot(d1.df['top_'+d1.x_header.label],d1.df[stat_header],'b.-',label=d1.sample_header.hclass)
    lns2=ax2.plot(d2[d1.x_header.name],d2.loc[:,sample_header.name],'r.-',label=sample_header.hclass)
    ax.set_xlabel(d1.x_header.label)
    ax.set_ylabel(d1.sample_header.label)
    ax2.set_ylabel(sample_header.label)
    plt.title('HR %s: %s vs. LR %s'% (d1.sample_header.hclass,stat_header,sample_header.hclass))
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)
    pdf_cs.savefig(fig)
    plt.close()
    
def plot_corr_stats_directory(d1:CompiledStat,
                        d2:DataFrame,
                        sample_header:Header,
                        stat_header:'str',
                        pdf_cs):
    
    plt.figure(figsize=(11, 8.5))
    fig,ax=plt.subplots()

    ax2=ax.twinx()
    lns1=ax.plot(d1.df['top_'+d1.x_header.label],d1.df[stat_header],'b-',label=d1.sample_header.hclass)
    lns2=ax2.plot(d2[d1.x_header.name],d2.loc[:,sample_header.name],'r-',label=sample_header.hclass)
    ax.set_xlabel(d1.x_header.label)
    ax.set_ylabel(d1.sample_header.label)
    ax2.set_ylabel(sample_header.label)
    plt.title('HR %s: %s vs. LR %s'% (d1.sample_header.hclass,stat_header,sample_header.hclass))
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)
    pdf_cs.savefig(fig)
    plt.close()

def plot_linregress_of_samples(d1:CompiledStat,
                               d2:Series,
                               sample_header:Header,
                               stat_header,
                               pdf):
    d1_stat = d1.df.loc[:, stat_header]
    d2 = d2[:-1]
    slope, intercept, r_value, unused_p_value, unused_std_err = linregress(remove_nan_from_datasets(d1_stat, d2))
    plt.figure(figsize=(11, 8.5))
    fig, ax = plt.subplots()
    ax.scatter(d1_stat, d2, label='data')
    ax.plot(d1_stat, intercept + slope * d1_stat, 'r', label='line-regression r={:.4f}'.format(r_value))
    plt.xlabel(d1.sample_header.label)
    plt.ylabel(sample_header.label)
    plt.title('Correlation of %s and %s' % (d1.sample_header.hclass, sample_header.hclass))
    plt.legend()
    pdf.savefig(fig)
    plt.close()
    


def resample_HR_by_LR(f1:str, f2:str, createPDF=False, createCSV=False):
    '''
    
    Double Resampler by Depth Intervals

    a. Input: two datasets with corresponding years, depths, samples
    b. $ PYTHONPATH=. python climatechange/process_data.py -di ../test/csv_files/small.csv
        ../test/csv_files/small2.csv

    i. Take depth intervals of one dataset and resample second dataset by first dataset
    depth intervals
    b. Output: correlation between raw data and statistics of the same samples in both datasets
    
    c. correlates only the depth intervals that correspond with both datasets
    ex: correlation between CompiledStat.df['Mean']=[2.5 4.5 6.5 8.5 1] and
    CompiledStat.df['top depth']=[1,2,3,4,5],CompiledStat.df['bottom depth']=[2,3,4,5,6] 
    df_LR[sample]=[1,2,3,4,5,6], df_LR[depth]=[1,2,3,4,5,6] will only account 
    for the depth of 1-5 and not 6.
    

    i. Pdf of correlation between same samples
    
    :param f1:
    :param f2:
    '''
    f_HR,f_LR=find_HR_and_LR_df(f1,f2)
    csv_folder = os.path.join(os.path.dirname(f_HR.file_path), 'Resample_HR_by_LR')
    
    compiled_stats_of_df_HR = compiled_stats_HR_by_LR(f_HR.df, f_LR.df)
    
    if createPDF:
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
        pdf_corr_stats = os.path.join(csv_folder,'%s_vs_ %s__plots.pdf' % (f_HR.base,f_LR.base))
        with PdfPages(pdf_corr_stats) as pdf_cs:
            for cs_list in compiled_stats_of_df_HR:
                for cs in cs_list:
                    for sh_LR in f_LR.sample_headers:
                        if (sh_LR.hclass==cs.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity') \
                            | (cs.sample_header.hclass=='Dust') | (cs.sample_header.hclass=='Conductivity'):
                            for stat_header in cs.df.columns[2:5]:
                                if not stat_header=='Stdv':
                                    plot_corr_stats(cs,f_LR.df,sh_LR,stat_header,pdf_cs)
                                    pyplot.close()
        
    
    corr_allstats=[]  
    for cs_list in compiled_stats_of_df_HR:
        for cs in cs_list:
            for sh_LR in f_LR.sample_headers:
                if (sh_LR.hclass==cs.sample_header.hclass) | (sh_LR.hclass=='Dust') | (sh_LR.hclass=='Conductivity') \
                        | (cs.sample_header.hclass=='Dust') | (cs.sample_header.hclass=='Conductivity'):
#                     print("Processing %s" % cs.x_header.name)
#                     print("correlating %s and %s" % (cs.sample_header.hclass, sh_LR.hclass))
                    corr_allstats.append(correlate_stats(cs, f_LR, sh_LR))
    
    df_corr_allstats = DataFrame(corr_allstats, columns=['depth', 'sample_1', 'sample_2', 'r_value:Mean', 'r_value:Median','r_value:Max','r_value:Min'])    
    
    if createCSV:
#         find_gaps(f_HR.df, f_LR.df, csv_folder, f_HR.base)
        csv_filename = os.path.join(csv_folder,'%s_vs_ %s__stat_correlation.csv' % (f_HR.base,f_LR.base))
        write_data_to_csv_files(df_corr_allstats, csv_filename)
    
    return df_corr_allstats
    
    
def find_HR_and_LR_df(f1:str,f2:str)->Tuple[DataFile,DataFile]:
    
    df1, unused_headers1 = load_and_clean_dd_data(f1)
    df2, unused_headers2 = load_and_clean_dd_data(f2)

    dh_1 = process_header_data(df1, HeaderType.DEPTH)
    dh_2 = process_header_data(df2, HeaderType.DEPTH)
    
    for depth1 in dh_1:
        for depth2 in dh_2:
            if depth1.name==depth2.name:
                
                df_HR, df_LR = (df1, df2) if (df1[depth1.name].iloc[-1]-df1[depth1.name].iloc[0]/df1.shape[0]) < \
                    (df2[depth2.name].iloc[-1]-df2[depth2.name].iloc[0]/df2.shape[0]) else (df2, df1)
        
                f_HR,f_LR = (f1, f2) if (df1[depth1.name].iloc[-1]-df1[depth1.name].iloc[0]/df1.shape[0]) < \
                    (df2[depth2.name].iloc[-1]-df2[depth2.name].iloc[0]/df2.shape[0]) else (f2, f1)
            break

        df_LR=df_LR[(df_LR[depth1.name]>=min(df_HR[depth1.name])) & (df_LR[depth1.name] <=max(df_HR[depth1.name]))]
        df_HR=df_HR[(df_HR[depth1.name]>=min(df_LR[depth1.name])) & (df_HR[depth1.name] <=max(df_LR[depth1.name]))]

    return DataFile(df_HR.reset_index(drop=True),f_HR),DataFile(df_LR.reset_index(drop=True),f_LR)


    

    
def load_and_store_header_file(path:str):
    print("Adding headers from %s to header dictionary." % path) 
    new_headers = load_headers(path)
    
    hd = HeaderDictionary()
    
    all_new = []
    all_replaced = []
    for h in new_headers:
        old_h = hd.add_header(h)
        if old_h:
            print("Replaced existing header")
            print("Old header: %s" % old_h)
            all_replaced.append(old_h)
        else:
            all_new.append(h)
        print("New header: %s" % h)
    
    hd.save_dictionary()
    
    print("Finished importing new headers")
    print("Imported %d new headers and "
          "replaced %d old headers with new definitions" % (len(all_new),
                                                            len(all_replaced)))
            

def plot_samples_by_year(f:str, interval:List=[]):
    
    dc = DataClass(f)
    if not interval == []:
        pdf_file = os.path.join(dc.dirname,('plot_%s_year_%.0f-%.0f.pdf'%(dc.base,interval[0],interval[1])))
    else:
        pdf_file = os.path.join(dc.dirname,('plot_%s_year.pdf'%(dc.base)))
    with PdfPages(pdf_file) as pdf:
        for year in dc.year_headers:
            for sample in dc.sample_headers:
                plot_samples(dc,sample,year,pdf, interval)
    os.startfile(pdf_file)
        
        
def plot_samples_by_depth(f:str, interval:List=[]):
    
    dc = DataClass(f)
    if not interval == []:
        pdf_file = os.path.join(dc.dirname,('plot_%s_depth_%.3f-%.3f.pdf'%(dc.base,interval[0],interval[1])))
    else:
        pdf_file = os.path.join(dc.dirname,('plot_%s_depth.pdf'%(dc.base)))
        
    with PdfPages(pdf_file) as pdf:
        for depth in dc.depth_headers:
            for sample in dc.sample_headers:
                plot_samples(dc, sample, depth, pdf, interval)
    os.startfile(pdf_file)
        
    
      
def plot_samples(dc:DataClass, sample_header:Header, x_header:Header, pdf, interval:List=[]):
    '''
    
    :param dc: DataClass Object
    :param pdf: pdf file
    :param x_header: name of x (depth or year) column
    :param sample header: headers of input sample

    :return: pdf file of data by sample
    '''
   
    if not interval == []:
        df = dc.df[(dc.df[x_header.name] >= interval[0]) & (dc.df[x_header.name] <= interval[1])]
    else:
        df = dc.df
        
        
    plt.figure(figsize=(11, 8.5))
    fig, tg = plt.subplots(1)
    ax = df[[x_header.name, sample_header.name]].plot(x=x_header.name, kind='line',
                                           linestyle='-',
                                           color='b',
                                           ax=tg,zorder=-1)
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:.0f}'.format(x) for x in vals])
    plt.xlabel(x_header.label)
    plt.title('%s Data' % (sample_header.hclass))
    plt.ylabel(sample_header.label)
    plt.legend()    
    pdf.savefig(fig)
    plt.close()
    
    

 

    

    
# def main(files):
#     start_time = time.time()
#     for f in files:
#         resample_by_years(f, 10)
# #         resample_by_depths(f, 0.04)
#     print('done')
#     print(" %s seconds to run" % (time.time() - start_time))
#     
