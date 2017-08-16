'''
Created on Aug 11, 2017

@author: Heather
'''

from pandas import DataFrame
from pandas import Series
from scipy.signal import savgol_filter

from climatechange.headers import process_header_data, HeaderType, Header
import numpy as np


def replace(sample_series:Series, stds:int)->Series:
    sample_series[np.abs(sample_series - sample_series.mean()) > stds * sample_series.std()] = np.nan
    return sample_series

def replace_outliers_with_nan(df:DataFrame)->DataFrame:
    headers=process_header_data(df)
    sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
    for sample_header in sample_headers:
        df.loc[:,sample_header] = df.loc[:,sample_header].transform(lambda g: replace(g, 3))
    return df

def savgol_smooth_filter(df_filter:DataFrame,sample_header:Header,x_header:Header):

    window_length=df_filter.shape[0]

    y_savgol = savgol_filter(df_filter.loc[:,sample_header.name], window_length, 3)

    return y_savgol

