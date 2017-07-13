'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import pandas as pd
from pandas.core.frame import DataFrame

def get_data_frame_from_csv(csvFileName: str) -> DataFrame:
    return pd.read_csv(csvFileName,sep=',')
