'''
Created on Jul 31, 2017

@author: Heather
'''

from pandas.core.frame import DataFrame
from climatechange.resampleStats import compileStats,find_indices,create_depth_headers
import pandas
from typing import List
import numpy as np
from climatechange.compiled_stat import CompiledStat


def create_range_for_depths(list_to_inc:List[float],inc_amt: int=0.01) -> List[float]:
    '''
    
    :param list_to_inc:
    :param inc_amt:
    '''
    if str(min(list_to_inc))[::-1].find('.')>str(inc_amt)[::-1].find('.'):
        r=str(min(list_to_inc))[::-1].find('.')-1
    else:
        r=str(inc_amt)[::-1].find('.')
    g=np.arange(np.round(min(list_to_inc),r),max(list_to_inc),inc_amt)
    return [round(i,r) for i in g.tolist()]

def find_index_by_increment_for_depths(list_to_inc:List[float],inc_amt:int=0.01)-> List[List[float]]:
    '''
    
    :param list_to_inc:
    :param inc_amt:
    '''
    top_range=create_range_for_depths(list_to_inc,inc_amt)
    bottom_range=[x+inc_amt for x in top_range]
    return [find_indices(list_to_inc,lambda e: e>=top_range[i] and e<bottom_range[i]) for i in range(0,len(top_range))]

def resampled_depths(df_x_sample,depth_name,inc_amt:int=1):
    top_range=create_range_for_depths(df_x_sample.iloc[:,0].values.tolist(),inc_amt)
    bottom_range=[x+inc_amt for x in top_range]
    df=DataFrame([top_range,bottom_range]).transpose()
    df.columns=create_depth_headers([depth_name])
    return df

def resampled_statistics_by_x(df_x_sample,x_name,index):
    appended_data=[]
    for i in index:
        appended_data.extend(compileStats(df_x_sample.iloc[i,[1]].transpose().values.tolist()))
    return DataFrame(appended_data,columns=['Mean','Stdv','Median','Max','Min','Count'])


def resampled_by_inc_depths(df_x_sample:DataFrame,
                    x_name:str,
                    inc_amt: int=0.01) -> DataFrame:
    '''
    :param df:
    :param inc:
    '''
    index=find_index_by_increment_for_depths(df_x_sample.iloc[:,0].values.tolist(),inc_amt)
    df_depths=resampled_depths(df_x_sample,x_name,inc_amt)
    df_stats=resampled_statistics_by_x(df_x_sample,x_name,index)
    return pandas.concat([df_depths,df_stats], axis=1)

def compile_stats_by_depth(df:DataFrame, depth_name:str, sample_name:str, inc_amt:int=0.01) -> CompiledStat:
    '''
    From the given data frame compile statistics (mean, median, min, max, etc) 
    based on the parameters.
    
    :param df: The data to compile stats for
    :param depth_name: The depth column to use for indexing
    :param sample_name: The sample compile to create statistics about
    :param inc_amt: The amount to group the year column by.  For example, 
        2012.6, 2012.4, 2012.2 would all be grouped into the year 2012.
    :return: A new DataFrame containing the resampled statistics for the 
    specified sample and year.
    '''
    
    df_x_sample=pandas.concat([df.loc[:,depth_name], df.loc[:,sample_name]], axis=1)
    resampled_data=resampled_by_inc_depths(df_x_sample, depth_name, inc_amt)
    
    return CompiledStat(resampled_data,depth_name,sample_name)

# def compile_stats_to_csv_pdf(f:str,
#                              df:DataFrame,
#                              pdf,
#                              x_name:str,
#                              headers:Header,
#                              bar_header:str) -> str:
#     '''
#     
#     :param f: input file path
#     :param df: dataframe of input file
#     :param pdf: pdf file
#     :param x_name: name of year column
#     :param headers: headers of input dataframe
#     :param bar_header: header of statistic to plot
#     
#     :return: csv files with statistics resampled of bar_header, 
#         pdf files of statistics with raw data
#     '''
#     
#     sample_headers:List[str] = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
#     for sample_name in sample_headers:
#         df_resampled_stats = compile_stats_by_depth(df, headers, x_name, sample_name)
#         write_resampled_data_to_csv_files(df_resampled_stats, f + ('_resampled_%s_%s.csv' % (x_name, sample_name.replace("/",""))))
#     
#     
#         plt.figure(figsize=(11, 8.5))
#         fig, tg = plt.subplots(1)
#         ax = df_resampled_stats[[x_name, bar_header]].plot(x=x_name, kind='line',color='r', ax=tg)
#         ax = df[[x_name, sample_name]].plot(x=x_name, kind='line',
#                                            linestyle='-',
#                                            color='0.75',
#                                            ax=tg,zorder=-1)
#         vals = ax.get_xticks()
#         ax.set_xticklabels(['{:.0f}'.format(x) for x in vals])
#         plt.title('Resampled %s of %s' % (bar_header, sample_name))
#         plt.xlabel(x_name)
#         plt.ylabel(sample_name)
#         plt.legend()    
#         pdf.savefig(fig)
#         plt.close()
# 
# def create_csv_pdf_of_resampled_stats(f:str,
#                                      df:DataFrame,
#                                      x_name:str,
#                                      headers:Header,
#                                      bar_header:str='Mean')->str:
#     '''
#     Create a pdf file with multiple plots based on the data frame.
#     :param f: input file path
#     :param df: dataframe of input file
#     :param x_name: name of year column
#     :param headers: headers of input dataframe
#     :param bar_header: header of statistic to plot
#     
#     :return: pdf of compiled figures by year,
#         csv file of statistics by sample and year
#     '''
#     file_name=f + ('_resampled_%s.pdf' % x_name)
#     with PdfPages(file_name) as pdf:
#         compile_stats_to_csv_pdf(f, df, pdf, x_name, headers, bar_header)    
#         plt.close()
#         