'''
Created on Jul 18, 2017

@author: Heather
'''
from climatechange.resampleStats import compileStats
from pandas import DataFrame
import pandas as pd

def create_range_by_inc(lst,inc):
    #creates lists of years incrementally by input of increment
    #lst must be Years
    return [x for x in range(int(min(lst)),int(max(lst))+1,inc)], [x+1 for x in range(int(min(lst)),int(max(lst))+1,inc)]

def find_indices(lst,condition):
    #find indices of the specific condition called
    return [j for j, elem in enumerate(lst) if condition(elem)]

def find_index_by_increment(lst,inc):
    ytop,ybot=create_range_by_inc(lst,inc)
    return [ytop,[find_indices(lst,lambda e: e>=ytop[i] and e<ybot[i]) for i in range(0,len(ytop))]]

        
def resample_by_inc(df,inc_amt):
    '''
    
    :param df:
    :param inc:
    '''
    years,ind=find_index_by_increment(df.iloc[:,0].values.tolist(),inc_amt)
    appended_data=[]
    for i in ind:
        appended_data.extend(compileStats(df.iloc[i,[1]].transpose().values.tolist()))
    return pd.concat([DataFrame(years, columns=['Year']), DataFrame(appended_data,columns=['Mean','Median','Max','Min','Stdv','Count'])], axis=1)

def resampled_data_to_csv(df):
    pass 