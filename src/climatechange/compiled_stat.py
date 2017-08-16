'''
Created on Aug 2, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
from climatechange.headers import Header

class CompiledStat(object):
    '''
    Contains a :py:class:`pandas.core.frame.DataFrame` that contains **Mean**,
    **Stdv**, **Median**, **Max**, **Min**, and **Count**.
    '''

    '''
    :ivar df: Contains columns [Mean,Stdv, Median, Max, Min, and Count]
    '''
    df:DataFrame

    '''
    :ivar x_header: The header information for the index column
    '''
    x_header:Header

    '''
    :ivar sample_header: The header information for the compiled statistics
    '''
    sample_header:Header


    def __init__(self, df:DataFrame,x_header:Header,sample_header:Header):
        '''

        :param df: Contains columns Mean,Stdv, Median, Max, Min, and Count
        :param x_header: The index column
        :param sample_header: The header the statistics are based on
        '''
        self.df=df
        self.x_header=x_header
        self.sample_header=sample_header
