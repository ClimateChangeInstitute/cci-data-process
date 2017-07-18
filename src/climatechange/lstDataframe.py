'''
Created on Jul 18, 2017

@author: Heather
'''
import pandas as pd 
from typing import List
from pandas.core.frame import DataFrame

def lstToDataframe(array:List[List[float]]) -> DataFrame:
    return pd.DataFrame(array).transpose()