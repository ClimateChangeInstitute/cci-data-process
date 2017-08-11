'''
Created on Aug 10, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
from builtins import str
import pandas
import re
from typing import List
from climatechange.headers import process_header_data
import os
from climatechange.process_data_functions import clean_data
import numpy as np
from pandas.core.series import Series

class LaserFile:
    def __init__(self, file_name, laser_time, start_depth, end_depth, washin_time, washout_time):
        self.file_name = file_name
        self.laser_time = laser_time
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.washin_time = washin_time
        self.washout_time = washout_time
#         self.header = header 
#         self.rows = rows

    def __str__(self):
        return self.file_name
    
    def __repr__(self):
        return self.__str__()

def readFile(file_name, laser_time, start_depth, end_depth, washin_time, washout_time)->LaserFile: #reads information from inputfile
                 
    return LaserFile(file_name, laser_time, start_depth, end_depth, washin_time, washout_time)


def load_input_file(input_file:'str')->List[LaserFile]: #gets information from input file
    """
    """
    result = []
    for line in open(input_file,'rU') :
        if not line.startswith(("#",'"')):
            columns = line.split()
            result.append(readFile(columns[0], float(columns[1]), float(columns[2]), float(columns[3]), float(columns[4]), float(columns[5])))
    return result

def process_laser_data(data_file:str,input_file:str,depth_age_file:str):
    
    laser_files=load_input_file(input_file)
    for f in laser_files:
        load_and_clean_LAICPMS_data(f,depth_age_file,os.path.dirname(input_file))
            
    pass
    
    
def load_laser_txt_file(f:str)->DataFrame:
    
    rows=[]
    with open(f) as f:
        for i,line in enumerate(f):
            if i ==0:
                header = line.split("\t")
                header[0] = "Time"
                for i in range(1,len(header)):
                    header[i] = re.sub("\(.*\)", "", header[i]).strip()
            elif i>5:
                rows.append(line.split())
    return DataFrame(rows,columns=header)

def load_and_clean_LAICPMS_data(f:LaserFile,path:str)->DataFrame:
    df=load_laser_txt_file(os.path.join(path,f.file_name))
    df = clean_data(df)
    df = df[(df['Time'] >f.washin_time) & (df['Time']< f.laser_time-f.washout_time)]
    df=add_depth_column(df,f.start_depth,f.end_depth)


#     df = clean_data(df.drop_duplicates())

    return df

def add_depth_column(df:DataFrame,start_depth:float,end_depth:float)->DataFrame:
    """
    """
    start_depth=start_depth/100
    end_depth=end_depth/100
    inc = (end_depth - start_depth) / (df.shape[0]-1)
    depth_series=Series(np.arange(start_depth, end_depth,inc))
    df.insert(0,'Depth (m abs)', depth_series)
    return df

def add_year_column(df:DataFrame,depth_age_file:str)->DataFrame:
    
    pass


def load_LAICPMS_input_file(input_file:str)->DataFrame:
    pass

def load_depth_age_conversion_file(depth_age_file:str)->DataFrame:
    pass

def assemble_df_for_lasered_segment():
    pass

