'''
Created on Jul 24, 2017

:author: Mark Royer
'''

from builtins import float
import datetime
import logging
from math import isnan
from math import nan
from matplotlib import pyplot
import os
import time
from typing import List, Tuple

from matplotlib.backends.backend_pdf import PdfPages
from numpy import float64
from pandas import DataFrame
from pandas import Series
from scipy.stats._stats_mstats_common import linregress

from climatechange.compiled_stat import CompiledStat
from climatechange.data_filters import replace_outliers_with_nan
from climatechange.file import load_csv
from climatechange.headers import HeaderDictionary, HeaderType, Header, \
    load_headers, process_header_data
from climatechange.plot import write_resampled_data_to_csv_files, \
    add_compile_stats_to_pdf
from climatechange.readme_output import create_readme_output_file, \
    write_readmefile_to_txtfile, template
from climatechange.resample_data_by_depths import compile_stats_by_depth, \
    compiled_stats_by_dd_intervals
from climatechange.resample_stats import compile_stats_by_year
import matplotlib.pyplot as plt
import numpy as np


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

def get_compiled_stats_by_year(inc_amt:int, df:DataFrame, headers:List[Header]) -> List[List[CompiledStat]]:
    year_headers = [h for h in headers if h.htype == HeaderType.YEARS]
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]
    compiled_stats = []
    for year_header in year_headers:
        cur_year = []
        for sample_header in sample_headers:
            cur_year.append(compile_stats_by_year(df, headers, year_header, sample_header, inc_amt))
        compiled_stats.append(cur_year)
    
    return compiled_stats

def find_round_values():
    pass

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
    df = load_csv(f)
    headers = process_header_data(df)
    df = clean_data(df)
    return df, get_compiled_stats_by_year(inc_amt, df, headers), headers


def resample_by_years(f:str, inc_amt:int=1):
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
    logging.info("Creating pdf for %s" % f)

    df, compiled_stats, headers = load_and_clean_year_data(f, inc_amt)
    f_base = os.path.splitext(f)[0]
    num_csvfiles = sum(len(c) for c in compiled_stats)
    stat_header = 'Mean'
    file_headers = compiled_stats[0][0].df.columns.values.tolist()
    print(file_headers)
    

    for cur_year in compiled_stats:
        for c in cur_year:
            csv_filename = f_base + '_stats_Resampled_%s_%s_Resolution_for_%s.csv' % (inc_amt,
                                                                         c.x_header.label,
                                                                         c.sample_header.hclass.replace("/", ""))
            to_csv_df = round_values_to_sigfig(c.df[:])
            to_csv_df = add_units_to_stats(to_csv_df, c.sample_header)
            write_resampled_data_to_csv_files(to_csv_df,
                                              csv_filename)

    year_headers = [h.label for h in headers if h.htype == HeaderType.YEARS]

    for i in range(len(year_headers)):
        file_name = (f_base + '_plots_Resampled_%s_%s_Resolution.pdf' % (inc_amt, year_headers[i]))
        with PdfPages(file_name) as pdf:
            for c in compiled_stats[i]:
                add_compile_stats_to_pdf(f_base,
                                         df,
                                         c.df,
                                         pdf,
                                         c.x_header,
                                         c.sample_header,
                                         inc_amt,
                                         'Year',
                                         stat_header)    
                pyplot.close()
                
    run_date = str(datetime.date.today())
    output_path = os.path.dirname(f)
    readme = create_readme_output_file(template, f, headers, run_date, inc_amt, 'Year', year_headers, file_headers, num_csvfiles, stat_header)
    write_readmefile_to_txtfile(readme, os.path.join(output_path, '00README.txt'))



def get_compiled_stats_by_depth(inc_amt:float,
                                df:DataFrame,
                                headers:List[Header]) -> List[List[CompiledStat]]:
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
    for depth_name in depth_headers:
        cur_depth = []
        for sample_name in sample_headers:
            cur_depth.append(compile_stats_by_depth(df, depth_name, sample_name, inc_amt))
        
#             print("compile stats for %s: %s seconds"%(sample_name,time.time()-start_time_d))
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
#     print("load and clean data: %s seconds"%(time.time()-start_time_d))
    return df, get_compiled_stats_by_depth(inc_amt, df, headers), headers

def resample_by_depths(f:str, inc_amt:float):
    '''
    Resampler by Depths
    
    a. Input: dataset with years, depths, samples
        -input: file, increment amount
    b. $ PYTHONPATH=. python climatechange/process_data.py -d ../test/csv_files/small.csv
    c. Output: csv file with statistics for each sample by depths

    cur_depth. Pdf of statistics by depths with raw data
    
    1. Mean w/ raw, median w/ raw (by depths) on same plot for each year column
    have 1 pdf with mean and median for each sample
    
    :param f:This is a CSV file
    '''
    print("Creating pdf for %s" % f)
    
    print(f)
    df, compiled_stats, headers = load_and_clean_depth_data(f, inc_amt)
    
    stat_header = 'Mean'
    num_csvfiles = sum(len(c) for c in compiled_stats)
    file_headers = compiled_stats[0][0].df.columns.values.tolist()
    f_base = os.path.splitext(f)[0]
    
    for cur_depth in compiled_stats:
        for c in cur_depth:
            csv_filename = f_base + '_stats_Resampled %s_inc_%s_Resolution_for_%s.csv' % (inc_amt,
                                                                        c.x_header.label,
                                                                        c.sample_header.label.replace("/", ""))
            to_csv_df = round_depth_values_to_sigfig(c.df[:])
            to_csv_df = add_units_to_stats(to_csv_df, c.sample_header)
            write_resampled_data_to_csv_files(to_csv_df,
                                              csv_filename)      

    depth_headers = [h.name for h in headers if h.htype == HeaderType.DEPTH] 
    for i in range(len(depth_headers)):
        file_name = (f_base + '_plots_Resampled_%s_inc_%s_resolution.pdf' % (inc_amt, depth_headers[i]))
        with PdfPages(file_name) as pdf:
            for c in compiled_stats[i]:
                add_compile_stats_to_pdf(f_base,
                                         df,
                                         c.df,
                                         pdf,
                                         c.x_header,
                                         c.sample_header,
                                         inc_amt,
                                         'Depth',
                                         stat_header)    
                pyplot.close()
            
    run_date = str(datetime.date.today())
    output_path = os.path.dirname(f)
    readme = create_readme_output_file(template, f, headers, run_date, inc_amt, 'Depth', depth_headers, file_headers, num_csvfiles, stat_header)
    write_readmefile_to_txtfile(readme, os.path.join(output_path, '00README.txt'))     

def remove_nan_from_datasets(d1_stat:Series, d2_stat:Series) -> Tuple[Series, Series]:
    d2_result = []
    d1_result = []
    for i in range(len(d1_stat)):
        if not isnan(d1_stat[i]) and not isnan(d2_stat[i]):
            d1_result.append(d1_stat[i])
            d2_result.append(d2_stat[i])
                     
    return Series(d1_result), Series(d2_result)
                   
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
    
    write_resampled_data_to_csv_files(df_corr_stats, csv_filename)  


def load_and_clean_dd_data(f:str) -> Tuple[DataFrame, List[Header]]:
    '''
    
    :param f: The file path of data to load and clean
    :return: A 2-tuple containing the cleaned original data,
     and the processed data headers from the original data file
    '''
    df=load_csv(f)
    headers = process_header_data(df)
    df = clean_data(df.drop_duplicates())
    return df.reset_index(drop=True), headers    
 

def correlate_dd_samples(d1:CompiledStat, d2:Series, stat_header:str='Mean') -> Tuple[float, float, float, float, float]:
    d1_stat = d1.df.loc[:, stat_header]
     
    slope, intercept, r_value, p_value, std_err = linregress(remove_nan_from_datasets(d1_stat, d2))
    return d1.x_header.name, d1.sample_header.name, d2.name, slope, intercept, r_value, p_value, std_err

def plot_linregress_of_samples(d1:CompiledStat,
                               d2:Series,
                               sample_header:Header,
                               stat_header,
                               pdf):
    d1_stat = d1.df.loc[:, stat_header]
    d2=d2[:-1]
    slope, intercept, r_value, unused_p_value, unused_std_err = linregress(remove_nan_from_datasets(d1_stat, d2))
    plt.figure(figsize=(11, 8.5))
    fig,ax=plt.subplots()
    ax.scatter(d1_stat, d2,label='data')
    ax.plot(d1_stat, intercept + slope*d1_stat, 'r',label='line-regression r={:.4f}'.format(r_value))
    plt.xlabel(d1.sample_header.label)
    plt.ylabel(sample_header.label)
    plt.title('Correlation of %s and %s'% (d1.sample_header.hclass,sample_header.hclass))
    plt.legend()
    pdf.savefig(fig)
    plt.close()
    
# def plot_2_samples_vs_depth(d1:CompiledStat,
#                                d2:Series,
#                                sample_header:Header,
#                                stat_header,
#                                pdf):
#     d1_stat = d1.df.loc[:, stat_header]
#     d2=d2[:-1]
#     plt.figure(figsize=(11, 8.5))
#     fig,ax=plt.subplots()
#     ax.plot(d1.df.loc[:, d1.x_header.name],d1_stat,label='d1')
#     ax.plot(d1.df.loc[:, d1.x_header.name],d2,label='d2'))
#     plt.xlabel(d1.x_header.label)
#     plt.title('Plot of %s and %s'% (d1.sample_header.hclass,sample_header.hclass))
#     plt.legend()
#     pdf.savefig(fig)
#     plt.close()
    
    
def double_resample_by_depth_intervals(f1:str, f2:str):
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
    smaller_df[sample]=[1,2,3,4,5,6], smaller_df[depth]=[1,2,3,4,5,6] will only account 
    for the depth of 1-5 and not 6.
    

    i. Pdf of correlation between same samples
    
    :param f1:
    :param f2:
    '''

    stat_header='Median'
    df1, unused_headers1 = load_and_clean_dd_data(f1)
    df2, unused_headers2 = load_and_clean_dd_data(f2)
    f1_file_path = os.path.splitext(f1)[0]
    f2_base = os.path.basename(f2).split('.')[0]
    csv_filename = f1_file_path + '_vs_ %s__stat_correlation_removeoutliers_median.csv' % (f2_base)
    pdf_filename = f1_file_path + '_vs_ %s__plot_correlation_removeoutliers_median.pdf' % (f2_base)

    larger_df, smaller_df = (df1, df2) if df1.shape[0] > df2.shape[0] else (df2, df1)
    larger_df=replace_outliers_with_nan(larger_df)
    
    compiled_stats_of_larger_df = compiled_stats_by_dd_intervals(larger_df, smaller_df)
    headers = process_header_data(smaller_df)
    sample_headers = [h for h in headers if h.htype == HeaderType.SAMPLE]

    corr_stats = []
    with PdfPages(pdf_filename) as pdf:
        for dlist1 in compiled_stats_of_larger_df:
            # list of compiled stat objects with depth and header names
            for d1 in dlist1:
                # compiled_stat_object with df, depth name, and sample name
                        for sample_header in sample_headers:
                            print("Processing depth %s" % d1.x_header.name)
                            # correlate
                            print("correlating %s and %s" % (d1.sample_header.name, sample_header.name))
                            corr_stats.append(correlate_dd_samples(d1, smaller_df.loc[:, sample_header.name],stat_header))
                            plot_linregress_of_samples(d1,smaller_df.loc[:, sample_header.name],sample_header,stat_header,pdf)
#                             plot_2_samples_by_depth(d1,smaller_df.loc[:, sample_header.name],sample_header,stat_header,pdf)
    df_corr_stats = DataFrame(corr_stats, columns=['depth', 'sample_1', 'sample_2', 'slope', 'intercept', 'r_value', 'p_value', 'std_err'])    
        
    write_resampled_data_to_csv_files(df_corr_stats, csv_filename)
    
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
            
    
# def main(files):
#     start_time = time.time()
#     for f in files:
#         resample_by_years(f, 10)
# #         resample_by_depths(f, 0.04)
#     print('done')
#     print(" %s seconds to run" % (time.time() - start_time))
#     
