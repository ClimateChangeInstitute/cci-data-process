'''
Created on Aug 2, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
from builtins import str

class CompiledStat(object):
    '''
    object that contains all of the properties with statistics compiled
    '''
    df:DataFrame
    
    x_value_name:str
    
    sample_value_name:str
    

    def __init__(self, df:DataFrame,x_value_name:str,sample_value_name:str):
        '''
        Constructor
        '''
        self.df=df
        self.x_value_name=x_value_name
        self.sample_value_name=sample_value_name
        
        
        