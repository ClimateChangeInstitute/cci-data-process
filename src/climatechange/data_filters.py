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

def replace(s:Series, num_std:float) -> Series:
    '''
    Replace any values greater than or less than the number of specified 
    standard deviations with :py:data:`np.nan`.  Modifications occur in-place.
    
    :param s: A series that will have outliers removed
    :param num_std: The number of standard deviations to use as a threshold
    :return: The modified series with :py:data:`np.nan` replacing outliers
    '''
    mean, std = s.mean(), s.std()
    outliers = (s - mean).abs() > num_std * std
    s[outliers] = np.nan
    return s
 
def replace_outliers_with_nan(df:DataFrame, num_std:float) -> DataFrame:
    headers = process_header_data(df)
    sample_headers = [h.name for h in headers if h.htype == HeaderType.SAMPLE]
    df[sample_headers] = df[sample_headers].transform(lambda s: replace(s, num_std))
    return df

def savgol_smooth_filter(df:DataFrame, sample_header:Header, x_header:Header):
    headers = process_header_data(df)
    window_length = df.shape[0]
    sample_headers = [h.name for h in headers if h.htype == HeaderType.SAMPLE]
    df[sample_headers] = df[sample_headers].transform(lambda x: savgol_filter(x, window_length, 3))

    return df

def normalize_min_max_scaler(df:DataFrame) -> DataFrame:
    x = df.iloc[:, 2:].values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_norm = pandas.DataFrame(x_scaled, columns=df.iloc[:, 2:].columns)
    return pandas.concat((df.iloc[:, :2], df_norm), axis=1)

