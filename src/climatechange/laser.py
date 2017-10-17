'''
Created on Oct 5, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
import os
from typing import List, Tuple
import re

from climatechange.process_data_functions import clean_data



import pandas
import numpy
from pandas import Series

class LaserInput:
    def __init__(self, file_path, laser_time, start_depth, end_depth,
                 washin_time, washout_time):
        self.file_path = file_path
        self.base=os.path.basename(self.file_path).split('.')[0]
        self.dirname=os.path.basename(os.path.dirname(os.path.dirname(self.file_path)))
        self.laser_time = laser_time
        self.start_depth = start_depth
        self.start_depth_m = (start_depth/100)
        self.end_depth = end_depth
        self.end_depth_m = (end_depth/100)
        self.washin_time = washin_time
        self.washout_time = washout_time
        self.raw_data = load_txt_file(file_path)
        self.info_dict = {'KCCID':self.dirname,'text_file':self.base,'top_depth':self.start_depth_m,'bottom_depth':self.end_depth_m,'laser_time':self.laser_time}
        self.info = DataFrame([self.info_dict],columns=self.info_dict.keys())
        
def read_input(file_path, laser_time, start_depth, end_depth, washin_time,
             washout_time) -> LaserInput:
                 
    return LaserInput(file_path, laser_time, start_depth, end_depth, washin_time, washout_time)


def load_txt_file(file_path:str) -> DataFrame:
    
    rows = []
    if not (os.path.splitext(file_path)[1]=='.txt') | (os.path.splitext(file_path)[1]=='.TXT'):
        file_path = file_path + '.txt'

    with open(file_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                header = line.split("\t")
                header[0] = "Time"
                for i in range(1, len(header)):
                    header[i] = re.sub("\(.*\)", "", header[i]).strip()
            elif i > 5:
                rows.append(line.split())
    return DataFrame(rows, columns=header)

def load_input(input_file:str) -> List[LaserInput]:  # gets information from input file
    """
    """
    result = []
    input_folder = os.path.dirname(input_file)
    with open(input_file, 'r') as f:
        for line in f:
            if not line.startswith(("#", '"')):
                columns = line.split()
                result.append(read_input(os.path.join(input_folder, columns[0]),
                                       float(columns[1]),
                                       float(columns[2]),
                                       float(columns[3]),
                                       float(columns[4]),
                                       float(columns[5])))
    return result

# def remove_nan(s1:Series, s2:DataFrame) -> Tuple[Series, Series]:
# 
#     df = s2.join(DataFrame(s1))
#     df = df.dropna()
# 
#     return df[s1.name]

def to_csv(directory,df,filename):  
    csv_folder = os.path.join(directory, 'csv_files')
    if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)  
            

    df.to_csv(os.path.join(csv_folder,filename))
    os.startfile(os.path.join(csv_folder,filename))

def add_depth_column(df:DataFrame, start_depth:float, end_depth:float) -> DataFrame:
    """
    """
    start_depth = start_depth / 100
    end_depth = end_depth / 100
    inc = (end_depth - start_depth) / (df.shape[0])
    depth_series = Series(numpy.arange(start_depth, end_depth, inc))
    df.insert(0, 'depth (m abs)', depth_series)
    return df

def add_year_column(df:DataFrame, depth_age_file:str) -> DataFrame:
    
    depth_age_df = pandas.read_table(depth_age_file)
    year_series = Series(numpy.interp(df['depth (m abs)'], depth_age_df['depth (m abs)'], depth_age_df['year']))
    df.insert(1, 'year', year_series)
    return df

def process_data(f:LaserInput,depth_age_file) -> DataFrame:  
    df = clean_data(f.raw_data)
    df = df[(df['Time'] > f.washin_time) & (df['Time'] < f.laser_time - f.washout_time)]
    df = df.reset_index(drop=True)
    df = df.drop('Time', 1)
    df = add_depth_column(df, f.start_depth, f.end_depth)
    df = add_year_column(df, depth_age_file)
    df = df.round(5)
    
    return df


def raw_data(directory,depth_age_file,prefix = 'KCC', csv = True):
    dfMR = DataFrame()
    dfLR= DataFrame() 
    df = DataFrame()
    

   
    for folder in os.listdir(directory):
        if folder.startswith(prefix):

            for input_folder in sorted(os.listdir(os.path.join(directory,folder))):
                if input_folder.startswith('Input'):
                    for file in sorted(os.listdir(os.path.join(directory,folder,input_folder))):
                        if (file.startswith('InputFile_1')) |(file.startswith('Input') & file.endswith('1')) | (file.startswith('Input') & file.endswith('MR')) | \
                            (file.startswith('Input') & file.endswith('1.txt')) | (file.startswith('Input') & file.endswith('MR.txt')) :
#                             print(file)
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            for f in laser_files:
                                df = df.append(f.info,ignore_index=True)
                                dfMR = dfMR.append(process_data(f,depth_age_file),ignore_index=True)

                        elif (file.startswith('InputFile_2')) |(file.startswith('Input') & file.endswith('2')) | (file.startswith('Input') & file.endswith('LR')) | \
                            (file.startswith('Input') & file.endswith('2.txt')) | (file.startswith('Input') & file.endswith('LR.txt')) :
                            
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            for f in laser_files:
                                dfLR = dfLR.append(process_data(f,depth_age_file),ignore_index=True)
                                
    dfMR = dfMR.set_index(['depth (m abs)'])
    dfLR = dfLR.set_index(['depth (m abs)'])
    if csv: 
        to_csv(directory,dfMR,'LA-ICP-MS_raw_MR.csv')
        to_csv(directory,dfLR,'LA-ICP-MS_raw_LR.csv')
        to_csv(directory,df,'full_core_information.csv')
    # add read me file
    return dfMR,dfLR

                             