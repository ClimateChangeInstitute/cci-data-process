'''
Created on Oct 18, 2017

@author: Heather
'''
import logging

from climatechange.common_functions import to_csv, DataClass
from climatechange.resample_read_me import readme_output_file, resample_template,write_readmefile_to_txtfile
import datetime
import os
from pandas import DataFrame
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from climatechange.headers import Header, process_header_str
import numpy
import pandas


from typing import List
from pandas.core.series import Series

#######################################################################################3
'''

RESAMPLE BY YEARS

'''

def resample(by:str,f:str,stat:str='Mean', inc_amt:int=1, by_name:str =None,output = True):
    '''
    Resampler by Years or Depths
    a. Input: dataset with years, depths, samples
    
    $ PYTHONPATH=. python climatechange/process_data.py -year_name ../test/csv_files/small.csv

    a. Output: csv file with statistics for each sample by years/depths

    :param: f: This is a CSV file
    '''
    logging.info("Creating pdf for %s", f)
    dc = DataClass(f)
    if (by == 'year') | (by == 'Year')|(by == 'y')|(by == 'Y'):
        if by_name:
            headers = process_header_str(by_name)
        else:
            headers = dc.year_headers
        x=0
    elif (by == 'depth') | (by == 'Depth')|(by == 'd')|(by == 'D'):
        if by_name:
            headers = process_header_str(by_name)
        else:
            headers = dc.depth_headers
        x=1
    
    all_files = []
    dfs = []
    for h in headers:
        if x == 0:
            df = by_years(dc, h,inc_amt,stat)
        else:
            df = by_depths(dc, h,inc_amt,stat)
        dfs.append(df)
            
        if stat:
            file ='{}_resample_by_{}_{}_{}.csv'.format(dc.base,inc_amt,h.label,'_'.join(stat))
        else:
            file = '{}_resample_by_{}_{}_stats.csv'.format(dc.base,inc_amt,h.label)
            

#         pdf_file= '{}_resampled_by_{}_{}_resolution_for_{}.pdf'.format(h.label, inc_amt,h.unit,'_'.join(stat))
        all_files.append(file)
        if output:
            
            to_csv(dc.dirname,df,file)
    
            readme = readme_output_file(resample_template,
                                        dc,
                                        str(datetime.date.today()),
                                        inc_amt,
                                        by,
                                        stat,
                                        all_files)
            write_readmefile_to_txtfile(readme, os.path.join(dc.dirname, '00README_resample_{}_{}_{}_resolution.txt'.format(h.label,inc_amt,by)))
            

    return dfs

# def plot_resampled(df:DataFrame,filename:str,directory: str):
#     
#     folder = os.path.join(directory, 'pdf_files')
#     if not os.path.exists(folder):
#             os.makedirs(folder) 
# 
#     cmap = plt.get_cmap('ocean')
#     with PdfPages(os.path.join(folder,filename)) as pdf:
# 
#         for i,col in enumerate(df):
#             ax = df[col].plot(figsize=(10,6),color=cmap(i / float(len(df.columns)+3)))
#             
#             ax.set_ylabel(col)
#             plt.tight_layout()
#             fig = plt.gcf()
# 
#             pdf.savefig(fig)
#             plt.close()
#     os.startfile(os.path.join(folder,filename))

#####################################################################################################

def create_range_by_year(list_to_inc:List[float], inc_amt: int=1) -> List[float]:
    '''
    
    :param list_to_inc:
    :param inc_amt:
    '''
    # creates lists of years incrementally by input of increment
    # list_years must be Years
    x = min(list_to_inc)
    y = max(list_to_inc)
    return [i for i in range(round(x), round(y), inc_amt)]

def by_years(dc:DataClass,depth_header:Header,inc_amt:int=1,stat:List[str] = None, year = None):
    
    range_list=create_range_by_year(dc.df.loc[:,depth_header.name].values.tolist(), inc_amt)

    dc_df = dc.sample_df.set_index(dc.df[depth_header.name])


    stat_list = []
    for s in dc.sample_headers:
        df = DataFrame()
        for i in range_list:
            idx =  dc_df[( dc_df.index >=i) & ( dc_df.index < i+1)]
            df = df.append(idx[s.name].describe(),ignore_index = True)
            
        if stat:
            df = df[stat]   
            df.columns = [s.label+'_'+col for col in df]
            stat_list.append(df)

        else:
            df.columns = [s.label+'_'+col for col in df]
            stat_list.append(df)

    
    stat_df =pandas.concat(stat_list,axis=1)
    df_years = Series(range_list, name=depth_header.label).astype(float)
    stat_df = stat_df.set_index(df_years)

    return stat_df


def depth_columns(dc:DataClass,year_header:Header, inc_amt:int):
    
    range_list=create_range_by_year(dc.df.loc[:,year_header].values.tolist(), inc_amt)

    depth_df = dc.depth_df.set_index(dc.df[year_header])

    topd_df=DataFrame()
    bottomd_df = DataFrame()

    for i in range_list:

        d_idx = depth_df[(depth_df.index >=i) & (depth_df.index < i+1)]

        topd_df = topd_df.append([d_idx.apply(lambda x: numpy.nanmin(x))],ignore_index = True)
        bottomd_df = bottomd_df.append([d_idx.apply(lambda x: numpy.nanmax(x))],ignore_index = True)


    topd_df.columns = ['top_'+ str(col) for col in dc.depth_headers_label]
    bottomd_df.columns = ['bottom_'+ str(col) for col in dc.depth_headers_label]
    
    df = pandas.concat([topd_df,bottomd_df],axis=1)
    cols = df.columns.tolist()
   
    if len(cols)==4:
        cols = [cols[0], cols[2],cols[1] , cols[3]]
    if len(cols)>4:
        logging.error('need less depths')


    return df[cols].round(5)

###############################################################################################

def by_depths(dc:DataClass,depth_header:Header,inc_amt:float,stat:List[str] = None):

    range_list=create_range_for_depths(dc.df.loc[:,depth_header.name].values.tolist(), inc_amt)

    print("reached.")

    dc_df = dc.sample_df.set_index(dc.df[depth_header.name])

    stat_list = []
    for s in dc.sample_headers:
        df = DataFrame()
        for i in range_list:
            idx = dc_df[(dc_df.index >=i) & (dc_df.index < i+1)]
            df = df.append(idx[s.name].describe(),ignore_index = True)
            
        if stat:
            df = df[stat]   
            df.columns = [s.label+'_'+col for col in df]
            stat_list.append(df)

        else:
            df.columns = [s.label+'_'+col for col in df]
            stat_list.append(df)

    
    stat_df =pandas.concat(stat_list,axis=1)

    df_depths = Series(range_list, name=depth_header.label).astype(float)
    stat_df = stat_df.set_index(df_depths)


    return stat_df

def create_range_for_depths(list_to_inc:List[float], inc_amt: float=0.01) -> List[float]:
    '''

    :param list_to_inc:
    :param inc_amt:
    '''
    if str(min(list_to_inc))[::-1].find('.') > str(inc_amt)[::-1].find('.'):

        r = str(min(list_to_inc))[::-1].find('.') - 1
    else:
        r = str(inc_amt)[::-1].find('.')
    g = numpy.arange(numpy.round(min(list_to_inc), r), max(list_to_inc), inc_amt)
    
    return [round(i, r) for i in g.tolist()]

#####################################################################################################





def find_match(dc:DataClass,dclr:DataClass)-> List[Header]:
    '''
    Find matching depth columns within each dataclass 
    '''
    match = []
    for hr in dc.depth_headers:
        for lr in dclr.depth_headers:
            if hr.name == lr.name:
                match.append(hr)
    return match

# 
def resample_by(filename:str,resample_by:str,stat:List[str] = None,depth:str = None,output = False):
    '''
    From the given data frame compile statistics (mean, median, min, max, etc)
    based on the parameters.
 
    :param df1:Larger Dataframe with smaller intervals to create a compiled stat
    :param df2:Smaller Dataframe with larger intervals to create index of intervals
    :return: A list of list of CompiledStat containing the resampled statistics for the
    specified sample and depth by the depth interval from df2.
    '''
    
    dc = DataClass(filename)
    dc_by = DataClass(resample_by)
    if depth:
        headers = process_header_str(depth)
    else:
        headers = find_match(dc, dc_by)
    
    headers_by=[]
    resample = [] 
    all_files =[]
    for h in headers:
        hr = dc.sample_df.set_index(dc.df[h.name])
        lr = dc_by.sample_df.set_index(dc_by.df[h.name])
        
        lr =lr[(lr.index >=min(hr.index)) & (lr.index <=max(hr.index))]



        stat_dict=[]
        for s in dc.sample_headers:
            df = DataFrame()
            if lr.empty:
                return [df]
            for i in range(len(lr.index.tolist())-1):

                idx = hr[(hr.index >=lr.index[i]) & (hr.index < lr.index[i+1])]

                df = df.append(idx[s.name].describe(),ignore_index = True)
                
            if stat:
                df = df[stat]   
                df.columns = [s.label+'_'+col for col in df]
                stat_dict.append(df)
                file ='{}_resample_by_{}_{}_{}.csv'.format(dc.base,dc_by.base,h.label,'_'.join(stat))
            else:
                df.columns = [s.label+'_'+col for col in df]
                stat_dict.append(df)
                file = '{}_resample_by_{}_{}.csv'.format(dc.base,dc_by.base,h.label)
        all_files.append(file)
           
        stat_df =pandas.concat(stat_dict,axis=1)
        stat_df = stat_df.set_index([lr.index[:-1]])

        stat_df.index.name=h.label
        if output:
            to_csv(dc.dirname,stat_df,file)
            
            readme = readme_output_file(resample_template,
                                        dc,
                                        str(datetime.date.today()),
                                        dc_by.base,
                                        'depth',
                                        stat,
                                        all_files)
            write_readmefile_to_txtfile(readme, os.path.join(dc.dirname, '00README_resample_{}_by_{}.txt'.format(h.label,dc_by.base)))
            

            
    headers_by.append(stat_df)
    return headers_by


