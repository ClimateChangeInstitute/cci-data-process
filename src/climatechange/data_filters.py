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


def replace(sample_series:Series, stds:int)->Series:
    sample_series[np.abs(sample_series - sample_series.mean()) > stds * sample_series.std()] = np.nan
    return sample_series

def replace_outliers_with_nan(df:DataFrame,num_std:int)->DataFrame:
    headers=process_header_data(df)
    sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
    for sample_header in sample_headers:
        df.loc[:,sample_header] = df.loc[:,sample_header].transform(lambda g: replace(g, num_std))
    return df

def savgol_smooth_filter(df:DataFrame,sample_header:Header,x_header:Header):
    headers=process_header_data(df)
    window_length=df.shape[0]
    sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
    for sample_header in sample_headers:
        df.loc[:,sample_header.name] = savgol_filter(df.loc[:,sample_header.name], window_length, 3)

    return df


def normalize_min_max_scaler(df:DataFrame)->DataFrame:
    x = df.iloc[:,2:].values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_norm=pandas.DataFrame(x_scaled,columns=df.iloc[:,2:].columns)
    return pandas.concat((df.iloc[:,:2],df_norm),axis=1)

