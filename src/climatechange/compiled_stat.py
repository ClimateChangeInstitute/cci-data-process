'''
Created on Aug 2, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
from climatechange.headers import Header

class CompiledStat(object):
    '''
    object that contains all of the properties with statistics compiled
    '''
    df:DataFrame
    
    x_header:Header
    
    sample_header:Header
    

    def __init__(self, df:DataFrame,x_header:Header,sample_header:Header):
        '''
        Constructor
        '''
        self.df=df
        self.x_header=x_header
        self.sample_header=sample_header
        
        
        