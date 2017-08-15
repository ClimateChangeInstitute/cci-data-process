'''
Created on Aug 11, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
from pandas import Series
from climatechange.headers import process_header_data, HeaderType
import numpy as np
from scipy.interpolate import UnivariateSpline

def replace(sample_series:Series, stds:int)->Series:
    sample_series[np.abs(sample_series - sample_series.mean()) > stds * sample_series.std()] = np.nan
    return sample_series

def replace_outliers_with_nan(df:DataFrame)->DataFrame:
    headers=process_header_data(df)
    sample_headers=[h.name for h in headers if h.htype == HeaderType.SAMPLE]
    for sample_header in sample_headers:
        df.loc[:,sample_header] = df.loc[:,sample_header].transform(lambda g: replace(g, 3))
    return df



