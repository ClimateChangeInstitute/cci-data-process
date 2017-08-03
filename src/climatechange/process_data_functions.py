'''
Created on Jul 24, 2017

:author: Mark Royer
'''

from builtins import float
from math import nan
import os
import time
from typing import List
from typing import List, Tuple

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from numpy import float64
import numpy
from pandas.core.frame import DataFrame

from climatechange.file import load_csv
from climatechange.headers import HeaderDictionary, HeaderType, Header
from climatechange.plot import write_resampled_data_to_csv_files, \
    add_compile_stats_to_pdf
from climatechange.read_me_output import create_readme_output_file
from climatechange.resampleStats import compile_stats_by_year
from climatechange.resample_data_by_depths import compile_stats_by_depth
from climatechange.resample_data_by_depths import compile_stats_by_depth
import datetime
from climatechange.read_me_output import template


def process_header_data(df) -> List[Header]:
    
    hd = HeaderDictionary()
    
    parsedHeaders = hd.parse_headers(list(df.columns))
    
    return parsedHeaders

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def clean_data(df):
    
    # Remove zeroes.  Zeroes go to nan
    values = df.values
    
    for r in values :
        for i in range(len(r)):
            if r[i] == 0:
                r[i] = float64(nan)
    
    # Replace str values with nan
    for r in values :
        for i in range(len(r)):
            if is_number(r[i]):
                r[i] = float64(r[i])
            else:
                r[i] = float64(nan) 
                
    
    df = DataFrame(data=values,
                   index=df.index,
                   columns=df.columns,
                   dtype=float64)
    
    return df

def get_compiled_stats_by_year(inc_amt:int,
                               df:DataFrame,
                               year_headers:List[Header],
                               sample_headers:List[Header],
                               headers:List[Header]) -> DataFrame:
    compiled_stats = []
    for year_name in year_headers:
        cur_year = []
        for sample_name in sample_headers:
            cur_year.append(compile_stats_by_year(df, headers, year_name, sample_name, inc_amt))
        compiled_stats.append(cur_year)
    
    return compiled_stats


def load_and_clean_year_data(f:str, inc_amt:int) -> Tuple[DataFrame, DataFrame, List[Header], List[Header]]:
    df = load_csv(f)
    headers = process_header_data(df)
    df = clean_data(df)
#     print("load and clean data: %s seconds"%(time.time()-start_time_d))
    year_headers = [h.original_value for h in headers if h.htype == HeaderType.YEARS]
    sample_headers = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
    return df, get_compiled_stats_by_year(inc_amt,
                                           df,
                                           year_headers,
                                           sample_headers, headers), year_headers, headers

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
    start_time = time.time()
    print("Creating pdf for %s" % f)

    df, compiled_stats, year_headers, headers = load_and_clean_year_data(f, inc_amt)
    f_base=os.path.splitext(f)[0]
#     print("compile stats: %s seconds"%(time.time()-start_time_d)) 
    for cur_year in compiled_stats:
        for c in cur_year:
            csv_filename=f_base+'_stats_%s_year_resolution_%s_%s.csv' % (inc_amt,
                                                                         c.x_value_name,
                                                                         c.sample_value_name.replace("/", ""))
            write_resampled_data_to_csv_files(c.df,
                                              csv_filename)

    for i in range(len(year_headers)):
        file_name=(f_base+'_plots_%s_year_resolution_%s.pdf' %(inc_amt,year_headers[i]))
        with PdfPages(file_name) as pdf:
            for c in compiled_stats[i]:
                add_compile_stats_to_pdf(f_base,
                                         df,
                                         c.df,
                                         pdf,
                                         c.x_value_name,
                                         c.sample_value_name,
                                         headers,
                                         inc_amt,
                                         'year')    
                pyplot.close()
                
    time_ran=(time.time() - start_time)
    run_date=str(datetime.date.today())
    create_readme_output_file(template,f,time_ran,run_date,inc_amt,'year',year_headers)
#     df = load_csv(f)
#     
#     headers = process_header_data(df)
# 
#     df = clean_data(df)
# 
#     year_headers = [h.original_value for h in headers if h.htype == HeaderType.YEARS]
# 
# #     depth_headers = [h.original_value for h in headers if h.htype == HeaderType.DEPTH]
# # 
# #     sample_headers = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
#     
#     for year_name in year_headers:
#         plot.create_csv_pdf_resampled(f, df, year_name, headers, inc_amt)
# #         for sample_name in sample_headers:
# #             df_resampled_stats = create_statistics(df, headers, year_name, sample_name)
# # #             plot.create_single_pdf(df, year_name, s, df_resampled_stats, f + ('.out.%s.pdf' % (year_name, s.replace("/",""))),bar_year_header=year_name)
# #             write_resampled_data_to_csv_files(df_resampled_stats, f + ('.out.%s.%s.csv' % (year_name, sample_name.replace("/",""))))
# #     
#     

def get_compiled_stats_by_depth(inc_amt:float,
                                df:DataFrame,
                                depth_headers:List[Header],
                                sample_headers:List[Header]) -> DataFrame:
    compiled_stats = []
    for depth_name in depth_headers:
        cur_depth = []
        for sample_name in sample_headers:
            cur_depth.append(compile_stats_by_depth(df, depth_name, sample_name, inc_amt))
        
#             print("compile stats for %s: %s seconds"%(sample_name,time.time()-start_time_d))
        compiled_stats.append(cur_depth)
    
    return compiled_stats


def load_and_clean_depth_data(f:str, inc_amt:float) -> Tuple[DataFrame,
                                                             DataFrame,
                                                             List[Header],
                                                             List[Header]]:
    '''
    
    :param f:
    :param inc_amt:
    :return: 
    '''
    df = load_csv(f)
    headers = process_header_data(df)
    df = clean_data(df)
#     print("load and clean data: %s seconds"%(time.time()-start_time_d))
    depth_headers = [h.original_value for h in headers if h.htype == HeaderType.DEPTH]
    sample_headers = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
    return df, get_compiled_stats_by_depth(inc_amt,
                                           df,
                                           depth_headers,
                                           sample_headers), depth_headers, headers

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
    start_time = time.time()
    print("Creating pdf for %s" % f)
    f_base=os.path.splitext(f)[0]
    df, compiled_stats, depth_headers, headers = load_and_clean_depth_data(f, inc_amt)

#     print("compile stats: %s seconds"%(time.time()-start_time)) 
    for cur_depth in compiled_stats:
        for c in cur_depth:
            csv_filename=f_base+'_stats_%s_inc_resolution_%s_%s.csv' % (inc_amt,
                                                                        c.x_value_name,
                                                                        c.sample_value_name.replace("/", ""))
            write_resampled_data_to_csv_files(c.df,
                                              csv_filename)
#     print("create csvs: %s seconds"%(time.time()-start_time_d))       
    for i in range(len(depth_headers)):
        file_name = (f_base+'_plots_%s_inc_resolution_%s.pdf' %(inc_amt,depth_headers[i]))
        with PdfPages(file_name) as pdf:
            for c in compiled_stats[i]:
                add_compile_stats_to_pdf(f_base,
                                         df,
                                         c.df,
                                         pdf,
                                         c.x_value_name,
                                         c.sample_value_name,
                                         headers,
                                         inc_amt,
                                         'depth')    
                pyplot.close()
                
    time_ran=(time.time() - start_time)
    run_date=str(datetime.date.today())
    create_readme_output_file(template,f,time_ran,run_date,inc_amt,'depth',depth_headers)
#     print("create_pdfs: %s seconds"%(time.time()-start_time_d))            
            
#     for depth_name in depth_headers:
#         plot.create_csv_pdf_resampled(f, df, depth_name, headers,inc_amt)
    
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
    
    df1, compiled_stats1, depth_headers1, headers1 = load_and_clean_depth_data(f1, inc_amt)
    df2, compiled_stats2, depth_headers2, headers2 = load_and_clean_depth_data(f2, inc_amt)

    
    
    # if they have the same sample name, correlate them
    # separate the units from the sample name, and save the sample name Na
    # correlate the two files
    # plot the means by each other, medians, min, max
    
def double_resample_by_depth_intervals(f1:str, f2:str):
    '''
    
    Double Resampler by Depth Intervals

    a. Input: two datasets with corresponding years, depths, samples
    b. $ PYTHONPATH=. python climatechange/process_data.py -di ../test/csv_files/small.csv
        ../test/csv_files/small2.csv

    i. Take depth intervals of one dataset and resample second dataset by first dataset
    depth intervals
    b. Output: correlation between raw data and statistics of the same samples in both datasets

    i. Pdf of correlation between same samples
    
    :param f1:
    :param f2:
    '''
    pass
    
    
def main(files):
    start_time = time.time()
    for f in files:
#         resample_by_years(f,1)
        resample_by_depths(f, 0.04)
    print('done')
    print(" %s seconds to run" % (time.time() - start_time))
    
