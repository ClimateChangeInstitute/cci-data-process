'''
A collection of functions for filtering data.

:author: Heather Clifford
:author: Mark Royer
'''

from pandas import DataFrame
from pandas import Series
import pandas
import pprint
from sklearn import preprocessing
from typing import List, Any, Tuple, Callable, Type

from numpy import float64
from scipy.signal import savgol_filter, medfilt, spline_filter, gauss_spline, wiener

from climatechange.headers import process_header_data, HeaderType
import numpy as np


def replace(s:Series, val:float64=np.nan, num_std:float=3) -> Series:
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

##############################################################################
############## PLACE DATA FILTER FUNCTIONS AFTER THIS LINE ###################
##############################################################################

def filter_registry():
    '''
    Create the filter function filter_decorator and registry
    '''
    registry = {}
    def filter_decorator(label:str):
        '''
        Use this decorator (called `filter_function`) with a label to indicate 
        that a function is used for filtering processed data.
        
        :param label: The name used for the filter function in the registry
        '''
        def registrar(func): # actually processes the function
            registry[label] = func
            return func
        return registrar
    filter_decorator.all = registry
    return filter_decorator
filter_function = filter_registry()

@filter_function("replace_outliers")
def replace_outliers(df:DataFrame, val:float64=np.nan, num_std:float=3) -> DataFrame:
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

@filter_function("savgol")
def savgol_smooth_filter(df:DataFrame):
    '''
    Apply the  Savitzky-Golay filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    window_length = df.shape[0]
    if window_length % 2 == 0:  # window_length must be odd
        window_length = window_length - 1
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    savgol_func = lambda x: savgol_filter(x, window_length, 3)
    df[sample_header_names] = df[sample_header_names].transform(savgol_func)

    return df

@filter_function("medfilt")
def medfilt_filter(df:DataFrame, val:int=3):
    '''
    Apply the  Median filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    medfilt_func = lambda x: medfilt(x, val)
    df[sample_header_names] = df[sample_header_names].transform(medfilt_func)

    return df

@filter_function("spline")
def spline_filter(df:DataFrame, val:float=5.0):
    '''
    Apply the  spline filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    spline_filter_func = lambda x: spline_filter(x, val)
    df[sample_header_names] = df[sample_header_names].transform(spline_filter_func)

    return df


# TODO: Figure out if the default val is Ok
@filter_function("gauss_spline")
def gauss_spline_filter(df:DataFrame, val:float=3.0):
    '''
    Apply the  spline filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    gauss_spline_filter_func = lambda x: gauss_spline(x, val)
    df[sample_header_names] = df[sample_header_names].transform(gauss_spline_filter_func)

    return df


@filter_function("wiener")
def wiener_filter(df:DataFrame):
    '''
    Apply the  spline filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    wiener_func = lambda x: wiener(x)
    df[sample_header_names] = df[sample_header_names].transform(wiener_func)

    return df


@filter_function("norm_min_max")
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


@filter_function("standardize_scaler")
def standardize_scaler(df:DataFrame) -> DataFrame:
    '''
    standardize dataframe by mean and std
    doesn't take nan values
    :param df:
    '''
    x = df.iloc[:, 2:].values
    scaler = preprocessing.StandardScaler()
    x_scaled = scaler.fit_transform(x)
    df_norm = pandas.DataFrame(x_scaled, columns=df.iloc[:, 2:].columns)
    return pandas.concat((df.iloc[:, :2], df_norm), axis=1)


@filter_function("robust_scaler")
def robust_scaler(df:DataFrame) -> DataFrame:
    x = df.iloc[:, 2:].values
    robust_scaler = preprocessing.RobustScaler(quantile_range=(25, 75))
    x_scaled = robust_scaler.fit_transform(x)
    df_norm = pandas.DataFrame(x_scaled, columns=df.iloc[:, 2:].columns)
    return pandas.concat((df.iloc[:, :2], df_norm), axis=1)


@filter_function("scaler")
def scaler(df:DataFrame) -> DataFrame:
    x = df.iloc[:, 2:].values
    x_scaled = preprocessing.scale(x)
    df_norm = pandas.DataFrame(x_scaled, columns=df.iloc[:, 2:].columns)
    return pandas.concat((df.iloc[:, :2], df_norm), axis=1)


@filter_function("fill_missing")
def fill_missing_values(df:DataFrame) -> DataFrame:
    
    x = df.iloc[:, 2:].values
    imp = preprocessing.Imputer(missing_values='NaN', strategy='mean', axis=0)
    x_fill = imp.fit_transform(x)
    df_norm = pandas.DataFrame(x_fill, columns=df.iloc[:, 2:].columns)
    return pandas.concat((df.iloc[:, :2], df_norm), axis=1)



def adjust_data_by_background(df:DataFrame,
                                 background_stats:DataFrame,
                                 stat:str='Mean') -> DataFrame:
    df = df.copy()

    for col in background_stats:
            df[col] = df[col] - background_stats.loc[stat, col]
    
    return df

def adjust_data_by_stats(df:DataFrame,
                            df_stats:DataFrame,
                            stat:str='Mean') -> DataFrame: 
    df = df.copy()

    for col in df_stats:
            df[col] = df[col] - df_stats.loc[stat, col]
    
    return df   
    
    
if __name__ == '__main__':
    filter_functions = list(filter_function.all.keys())
    filter_functions.sort()
    print("Registered filter functions:")
    pprint.pprint(filter_functions)
