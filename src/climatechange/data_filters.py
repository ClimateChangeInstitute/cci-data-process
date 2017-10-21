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


from numpy import float64
from scipy.signal import savgol_filter, medfilt, spline_filter, gauss_spline, wiener, butter
# from scipy.signal import cspline1d,qspline1d
from climatechange.headers import process_header_data, HeaderType
import numpy as np
from typing import Mapping, Callable
import inspect
from scipy.signal.bsplines import cubic, bspline
from scipy.signal.signaltools import filtfilt, lfilter
from scipy.interpolate.fitpack2 import UnivariateSpline


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


def filter_func_to_string(label:str, f:Callable) -> str:
    
    # These are only the parameters after the DataFrame.
    # The first parameter should be a data frame.
    params = [str(p).replace('pandas.core.frame.','') for p in inspect.signature(f).parameters.values()]
    
    return label + '(' + ', '.join(params) + ')'
    

def filters_to_string(ff:Mapping[str, Callable]) -> str:  # @ReservedAssignment
    result_str = ''
    for label, f in ff.items():
        result_str += filter_func_to_string(label, f)
        result_str += '\n'
    return result_str

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
        def registrar(func):  # actually processes the function
            registry[label] = func
            return func
        return registrar
    filter_decorator.all = registry
    filter_decorator.help = lambda:filters_to_string(registry)
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
def savgol_smooth_filter(df:DataFrame, window_length:int = 7):
    '''
    Apply the  Savitzky-Golay filter to the columns of the supplied data.  
    The filter is only applied to columns that appear as samples in the default 
    header dictionary. Modifications occur in-place.
    
    :param df: The data to filter
    :return: The resampled data
    '''
    if window_length % 2 == 0:  # window_length must be odd
        window_length = window_length - 1
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    savgol_func = lambda x: savgol_filter(x, window_length, 1)
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


@filter_function("filtfilt")
def filtfilt_filter(df:DataFrame) -> DataFrame:
    
    b, a = butter(2,0.02)
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    filt_filt_func = lambda x: filtfilt(b,a,x)
    df[sample_header_names] = df[sample_header_names].transform(filt_filt_func)

    return df

@filter_function("lfilt")
def lfilter_filter(df:DataFrame) -> DataFrame:
    
    b, a = butter(2,0.1)
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    lfilter_func = lambda x: lfilter(b,a,x)
    df[sample_header_names] = df[sample_header_names].transform(lfilter_func)

    return df


def _processed_data(df:DataFrame):
    return df    

def univariate_spline(df:DataFrame,var =45):

    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    depth = 'depth (m abs)'

    x = df[depth]
    xs = np.linspace(min(x), max(x),var)
    xs_dict = {depth:pandas.Series(xs)}
    
    for sample_header_name in sample_header_names:
        y = df[sample_header_name]
        spl = UnivariateSpline(x, y)
        new_spl = pandas.Series(spl(xs))
        spline_xs = {sample_header_name:new_spl}
        xs_dict.update(spline_xs)
    spline_df = pandas.concat(xs_dict,axis=1)


    colnames = spline_df.columns.tolist()

    colnames = colnames[-1:] + colnames[:-1]

    spline_df = spline_df[colnames]
    return spline_df


##############################################################################
############## PLACE DATA SCALERS FUNCTIONS AFTER THIS LINE ###################
##############################################################################



@filter_function("scaler")
def scaler(df:DataFrame) -> DataFrame:
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    scaler_scaler = lambda x: preprocessing.scale(x)
    df[sample_header_names] = df[sample_header_names].transform(scaler_scaler)

    return df

    
def normalize_data(df:DataFrame):
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    df[sample_header_names] = df[sample_header_names].transform(lambda X: (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0)))
    return df

@filter_function("robust_scaler")
def robust_scaler(df:DataFrame) -> DataFrame:
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    rob_scaler = lambda x: preprocessing.robust_scale(x.to_frame()).flatten()
    df[sample_header_names] = df[sample_header_names].transform(rob_scaler)

    return df

@filter_function("quantile_transform")
def quantile_transform_scaler(df:DataFrame) -> DataFrame:
    
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    quant_trans = lambda x: preprocessing.quantile_transform(x.to_frame()).flatten()
    df[sample_header_names] = df[sample_header_names].transform(quant_trans)

    return df


@filter_function("norm_min_max")
def normalize_min_max_scaler(df:DataFrame) -> DataFrame:
    '''
    Normalize dataframe by min and max
    doesn't take nan values
    :param df:
    '''
    sample_header_names = [h.name for h in process_header_data(df, HeaderType.SAMPLE)]
    min_max_scaler = lambda x: preprocessing.minmax_scale(x)
    df[sample_header_names] = df[sample_header_names].transform(min_max_scaler)

    return df



# default_filters = [(processed_data,),(wiener_filter,),(robust_scaler,),(medfilt_filter,)]  

default_filters = [(_processed_data,),(savgol_smooth_filter,),(medfilt_filter,),(filtfilt_filter,),(univariate_spline,50)]  
# default_filters = [(processed_data,),(savgol_smooth_filter,),(savgol_smooth_filter_wl,),(wiener_filter,),(robust_scaler,),(medfilt_filter,),(scaler,),(filtfilt_filter,),(lfilter_filter,),(univariate_spline,),(univariate_spline_60,),(univariate_spline_50,)]  
# default_filters = [(savgol_smooth_filter_wl,)]    
# default_filters = [(univariate_spline,),(univariate_spline_60,),(univariate_spline_50,)]
# default_filters = [(processed_data,)]
     
# 
# if __name__ == '__main__':
#     filter_functions = list(filter_function.all.keys())
#     filter_functions.sort()
#     print("Registered filter functions:")
#     pprint.pprint(filter_functions)
