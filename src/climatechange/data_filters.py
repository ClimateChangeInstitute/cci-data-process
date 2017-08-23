'''
A collection of functions for filtering data.

:author: Heather Clifford
:author: Mark Royer
'''

from numpy import float64
from pandas import DataFrame
from pandas import Series
import pandas
from scipy.signal import savgol_filter
from sklearn import preprocessing

from climatechange.headers import process_header_data, HeaderType
import numpy as np
from typing import List


def replace(s:Series, val:float64=np.nan, num_std:float=2) -> Series:
    '''
    Replace any values greater than or less than the number of specified 
    standard deviations with :py:data:`np.nan`.  Modifications occur in-place.
    
    :param s: A series that will have outliers removed
    :param val: The new value for outliers
    :param num_std: The number of standard deviations to use as a threshold
    :return: The modified series with :py:data:`np.nan` replacing outliers
    '''
    mean, std = s.mean(), s.std()
    outliers = (s - mean).abs() > num_std * std
    s[outliers] = val
    return s
 
def replace_outliers(df:DataFrame, val:float64=np.nan, num_std:float=2) -> DataFrame:
    '''
    Replace the outliers in the data on a column based calculation.  The mean 
    and standard deviation for each column is calculated to use.
    
    :param df: The data to replace outliers in
    :param val: The new value to use (the default is :data:`np.nan`)
    :param num_std: The number of standard deviations to use as a threshold
    :return: Data with values outside the threshold replaced
    '''
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    df[sample_header_names] = df[sample_header_names].transform(lambda s: replace(s, val, num_std))
    return df

def savgol_smooth_filter(df:DataFrame):
    '''
    Apply the  Savitzky-Golay filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    window_length = df.shape[0]
    if window_length % 2 == 0: # window_length must be odd
        window_length = window_length - 1
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    savgol_func = lambda x: savgol_filter(x, window_length, 3)
    df[sample_header_names] = df[sample_header_names].transform(savgol_func)

    return df

def normalize_min_max_scaler(df:DataFrame) -> DataFrame:
    '''
    Normalize dataframe by min and max
    doesn't take nan values
    :param df:
    '''
    x = df.iloc[:, 2:].values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_norm = pandas.DataFrame(x_scaled, columns=df.iloc[:, 2:].columns)
    return pandas.concat((df.iloc[:, :2], df_norm), axis=1)

def adjust_data_by_background(df:DataFrame,
                                 background_stats:DataFrame,
                                 stat:str='Mean')->DataFrame:
    df=df.copy()

    for col in background_stats:
            df[col]=df[col]-background_stats.loc[stat,col]
    
    return df

def adjust_data_by_stats(df:DataFrame,
                            df_stats:DataFrame,
                            stat:str='Mean')->DataFrame: 
    df=df.copy()

    for col in df_stats:
            df[col]=df[col]-df_stats.loc[stat,col]
    
    return df   
    
    
    
    
    
    
    pass
    
    
