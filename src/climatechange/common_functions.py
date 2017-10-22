'''
Created on Oct 18, 2017

@author: Heather
'''
import os
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame
from climatechange.headers import process_header_data, HeaderType
import pandas
from numpy import float64
from math import nan, isnan
import logging
from typing import List, Tuple
import numpy
from pandas.core.series import Series
import datetime

class DataClass():

    def __init__(self, file_path:str=[]):
        
        self.file_path = file_path
        self.df = clean_data(load_csv(self.file_path))
#         self.df_multi = clean_data(load_csv(self.file_path))
        
        
        self.base=os.path.basename(self.file_path).split('.')[0]
        self.base_ext=os.path.basename(self.file_path)
        self.dirname=os.path.dirname(self.file_path)
        self.sample_headers = process_header_data(self.df, HeaderType.SAMPLE)
        self.sample_headers_dict = {'name':[sample.name for sample in self.sample_headers],'label':[sample.label for sample in self.sample_headers]}
        
        self.sample_headers_name = [i.name for i in self.sample_headers]
        self.sample_headers_label = [i.label for i in self.sample_headers] 
        self.depth_headers = process_header_data(self.df, HeaderType.DEPTH) 
        self.depth_headers_name = [i.name for i in self.depth_headers] 
        self.depth_headers_label = [i.label for i in self.depth_headers] 
        self.year_headers = process_header_data(self.df, HeaderType.YEARS)
        self.year_headers_name = [i.name for i in self.year_headers] 
        self.year_headers_label = [i.label for i in self.year_headers] 
        self.sample_df =self.df[self.sample_headers_name]
        self.depth_df =self.df[self.depth_headers_name]
        self.headers = process_header_data(self.df)
        self.names = [i.name for i in self.headers]
        self.value = [i.htype.value for i in self.headers]  
           
        self.df_multi.columns = [self.value,self.names]

        self.dx =self.df_multi.xs('Sample',axis=1).describe().T

class FrameClass():
     
    def __init__(self, df:DataFrame):
         
 
        self.df = df
        self.sample_headers = process_header_data(self.df, HeaderType.SAMPLE)
        self.sample_headers_name = [i.name for i in self.sample_headers]
        self.sample_headers_label = [i.label for i in self.sample_headers] 
        self.depth_headers = process_header_data(self.df, HeaderType.DEPTH) 
        self.depth_headers_name = [i.name for i in self.depth_headers] 
        self.depth_headers_label = [i.label for i in self.depth_headers] 
        self.year_headers = process_header_data(self.df, HeaderType.YEARS)
        self.year_headers_name = [i.name for i in self.year_headers] 
        self.year_headers_label = [i.label for i in self.year_headers]
        self.sample_df =self.df[self.sample_headers_name]
        self.depth_df =self.df[self.depth_headers_name]
        self.year_df =self.df[self.year_headers_name]
        self.sample_year_df =self.df[self.year_headers_name + self.sample_headers_name]
        self.year_sample_headers = self.year_headers +self.sample_headers 

     

   
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
        
def clean_data(df):
    
    # Remove zeroes.  Zeroes go to nan
    values = df.values
    

    
    # Replace str values with nan
    for r in values :
        for i in range(len(r)):
            if is_number(r[i]):
                r[i] = float64(r[i])
            else:
                r[i] = float64(nan) 

    for r in values :
        for i in range(len(r)):
            if r[i] == 0:
                r[i] = float64(nan)
                
    
    df = DataFrame(data=values,
                   index=df.index,
                   columns=df.columns,
                   dtype=float64)
    
    return df

def load_csv(file_name: str) -> DataFrame:
    '''
    Loads a CSV file into a :py:class:`pandas.core.frame.DataFrame` object. 
    
    :param file_name: The name of the CSV file
    :return: A DataFrame object
    '''
    return pandas.read_csv(file_name, sep=',')

def to_csv(directory:str,df:DataFrame,filename:str='output_file.csv',idx = True):  
    csv_folder = os.path.join(directory, 'Output_Files')
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)  
        
    if  not os.path.isfile(os.path.join(directory,'Output_Files','00README.txt')):
        with open(os.path.join(directory,'Output_Files','00README.txt'),'w') as f:
            f.write('ReadMeFile\n\nCCI-Data-Processor\nAuthors: Mark Royer and Heather Clifford\n\nOutput Files from cci-data-processor\n\n')
            f.write('Date Added\t\t\t\t\tFile Added\n')
    else:
        with open(os.path.join(directory, 'Output_Files','00README.txt'),'a') as f:
            f.write('{}\t\t\t{}\n'.format(datetime.datetime.now().strftime("%m/%d/%Y %I:%M%p"),filename))
        

    df.to_csv(os.path.join(csv_folder,filename),index = idx)
    os.startfile(os.path.join(csv_folder,filename))
    
    
def index_by_increment(list_to_inc:List[float], range_list:List[float]) -> Tuple[List[List[int]],List[float]]:
    '''

    :param list_to_inc:
    :param inc_amt:
    '''
    logging.debug("find_index_by_increment: range_list=%s", range_list)
    result = []

    gaps=[]
    range_list_size = len(range_list)
    prev = 0
    for i in range(range_list_size - 1):
        tmp = []
        for j in range(prev, len(list_to_inc)):
            e = list_to_inc[j]
            if e >= range_list[i] and e < range_list[i + 1]:
                tmp.append(j)
                prev = j + 1
        if not tmp:
            logging.warning('no values between [%f,%f)', range_list[i], range_list[i + 1])
            gaps.append([range_list[i], range_list[i + 1]])
        else: 
            result.append(tmp)
        
    tmp = []
    for j in range(prev, len(list_to_inc)):
        e = list_to_inc[j]
        if e >= range_list[range_list_size-1]:
            tmp.append(j)
    if not tmp:
        logging.warning('no values > %f',range_list[range_list_size-1])
    else:
        result.append(tmp)
       
    return result

