'''
Created on Aug 11, 2017

@author: Heather
'''

from pandas import DataFrame
from pandas import Series
from scipy.signal import savgol_filter
from sklearn import preprocessing

from climatechange.headers import process_header_data, HeaderType, Header
import numpy as np
import pandas


# def replace(s:Series, stds:int)->Series:
#     s[np.abs(s - np.nanmean(s)) > stds * np.nanstd(s)] = np.nan
#     print(s[np.abs(s - np.nanmean(s)) > stds * np.nanstd(s)])
#     return s



def replace(s:Series):
    mean, std = s.mean(), s.std()
    outliers = (s - mean).abs() > 3*std
    s[outliers] = np.nan
    return s

def replace_outliers_with_nan(df:DataFrame)->DataFrame:
    headers=process_header_data(df)
    sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
    df[sample_headers]=df[sample_headers].transform(replace)
    return df

def savgol_smooth_filter(df:DataFrame,sample_header:Header,x_header:Header):
    headers=process_header_data(df)
    window_length=df.shape[0]
    sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
    df[sample_headers]=df[sample_headers].transform(lambda x: savgol_filter(x, window_length, 3))

    return df

def normalize_min_max_scaler(df:DataFrame)->DataFrame:
    x = df.iloc[:,2:].values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_norm=pandas.DataFrame(x_scaled,columns=df.iloc[:,2:].columns)
    return pandas.concat((df.iloc[:,:2],df_norm),axis=1)

