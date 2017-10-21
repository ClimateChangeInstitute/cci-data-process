'''
Created on Oct 5, 2017

@author: Heather
'''
from pandas.core.frame import DataFrame
import os
from typing import List
import re
import pandas
import numpy as np
from pandas import Series
from climatechange.common_functions import to_csv, clean_data, FrameClass,\
    DataClass
from climatechange.resample_read_me import readme_laser_file, laser_template,\
    write_readmefile_to_txtfile
import datetime
from climatechange.headers import process_header_str
from climatechange.resample import find_match
import numpy

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

        
def add_depth_column(df:DataFrame, start_depth:float, end_depth:float) -> DataFrame:
    """
    """
    inc = (end_depth - start_depth) / (df.shape[0])
    depth_series = Series(np.arange(start_depth, end_depth, inc))
    df.insert(0, 'depth (m abs)', depth_series)
    return df

def add_year_column(df:DataFrame, depth_age_file:str) -> DataFrame:
    
    depth_age_df = pandas.read_table(depth_age_file)
    year_series = Series(np.interp(df['depth (m abs)'], depth_age_df['depth (m abs)'], depth_age_df['year']))
    df.insert(1, 'year', year_series)
    return df

def process_laser_data(f:LaserInput,depth_age_file) -> DataFrame:  
    df = clean_data(f.raw_data)
    df = df[(df['Time'] > f.washin_time) & (df['Time'] < f.laser_time - f.washout_time)]
    df = df.reset_index(drop=True)
    df = df.drop('Time', 1)
    df = add_depth_column(df, f.start_depth_m, f.end_depth_m)
    df = add_year_column(df, depth_age_file)
    df = df.round(5)
    
    return df
        
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
                depth_header = line.split("\t")
                depth_header[0] = "Time"
                for i in range(1, len(depth_header)):
                    depth_header[i] = re.sub("\(.*\)", "", depth_header[i]).strip()
            elif i > 5:
                rows.append(line.split())
    return DataFrame(rows, columns=depth_header)

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



def raw_data(directory,depth_age_file,prefix = 'KCC', output = True):
    '''
    
    Compiles all raw LA-ICP-MS data within the specified directory that share the
        specified prefix, compiles age and depth according to specified depth_age file
    '''
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
                            
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            
                            for f in laser_files:
                                df = df.append(f.info,ignore_index=True)
                                dfMR = dfMR.append(process_laser_data(f,depth_age_file),ignore_index=True)

                        elif (file.startswith('InputFile_2')) |(file.startswith('Input') & file.endswith('2')) | (file.startswith('Input') & file.endswith('LR')) | \
                            (file.startswith('Input') & file.endswith('2.txt')) | (file.startswith('Input') & file.endswith('LR.txt')) :
                            
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            
                            for f in laser_files:
                                dfLR = dfLR.append(process_laser_data(f,depth_age_file),ignore_index=True)
                                
    dfMR = dfMR.set_index(['depth (m abs)'])
    dfLR = dfLR.set_index(['depth (m abs)'])
    if output: 
        to_csv(directory,dfMR,'LA-ICP-MS_raw_MR.csv')
        to_csv(directory,dfLR,'LA-ICP-MS_raw_LR.csv')
        info_file = 'full_core_information.csv'
        to_csv(directory,df,info_file,False)
        
        readmeMR=readme_laser_file(laser_template, directory, prefix, depth_age_file, FrameClass(dfMR), 'Medium', str(datetime.date.today()),info_file, 'LA-ICP-MS_raw_MR.csv','Raw')
        readmeLR=readme_laser_file(laser_template, directory, prefix, depth_age_file, FrameClass(dfLR),'Low', str(datetime.date.today()),info_file,'LA-ICP-MS_raw_LR.csv','Raw')
        
        write_readmefile_to_txtfile(readmeMR,os.path.join(directory, 'Output_Files','00README_Raw_Medium_Resolution.txt'))
        write_readmefile_to_txtfile(readmeLR, os.path.join(directory, 'Output_Files','00README_Raw_Low_Resolution.txt'))

    return dfMR,dfLR



#####################################################################################################
# RESAMPLE LASER DATA
#####################################################################################################

def resample_data(directory:str,by:str,depth_age_file:str,prefix = 'KCC', depth ='depth (m abs)',output = True):
    '''
    
    Compiles all raw LA-ICP-MS data within the specified directory that share the
        specified prefix, compiles age and depth according to specified depth_age file
    '''
    dfMR = DataFrame()
    dfLR= DataFrame() 
    df = DataFrame()
    by = DataClass(by)

   
    for folder in os.listdir(directory):
        if folder.startswith(prefix):

            for input_folder in sorted(os.listdir(os.path.join(directory,folder))):
                if input_folder.startswith('Input'):
                    for file in sorted(os.listdir(os.path.join(directory,folder,input_folder))):
                        if (file.startswith('InputFile_1')) |(file.startswith('Input') & file.endswith('1')) | (file.startswith('Input') & file.endswith('MR')) | \
                            (file.startswith('Input') & file.endswith('1.txt')) | (file.startswith('Input') & file.endswith('MR.txt')) :
                            
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            
                            for f in laser_files:
                                df = df.append(f.info,ignore_index=True)
                                dfMR = dfMR.append(resample_laser_by(process_laser_data(f,depth_age_file), by.df,depth))

                        elif (file.startswith('InputFile_2')) |(file.startswith('Input') & file.endswith('2')) | (file.startswith('Input') & file.endswith('LR')) | \
                            (file.startswith('Input') & file.endswith('2.txt')) | (file.startswith('Input') & file.endswith('LR.txt')) :
                            
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            
                            for f in laser_files:
                                dfLR = dfLR.append(resample_laser_by(process_laser_data(f,depth_age_file), by.df,depth))
                                

    if output: 
        output ='Raw_Resampled_by_{}'.format(by.base)
        to_csv(directory,dfMR,'LA-ICP-MS_{}_MR.csv'.format(output))
        to_csv(directory,dfLR,'LA-ICP-MS_{}_LR.csv'.format(output))
        
        info_file = 'full_core_information.csv'
        if not os.path.isfile(os.path.join(directory,'Output_Files',info_file)):
            to_csv(directory,df,info_file,False)
        
        readmeMR=readme_laser_file(laser_template, directory, prefix, depth_age_file, FrameClass(dfMR), 'Medium', str(datetime.date.today()),info_file, 'LA-ICP-MS_raw_MR.csv',output)
        readmeLR=readme_laser_file(laser_template, directory, prefix, depth_age_file, FrameClass(dfLR),'Low', str(datetime.date.today()),info_file,'LA-ICP-MS_raw_LR.csv',output)
        
        write_readmefile_to_txtfile(readmeMR,os.path.join(directory, 'Output_Files','00README_{}_Medium_Resolution.txt'.format(output)))
        write_readmefile_to_txtfile(readmeLR, os.path.join(directory, 'Output_Files','00README_{}_Low_Resolution.txt'.format(output)))

    return dfMR,dfLR

def resample_laser_by(df:DataFrame, by:DataFrame,depth):
    '''
    From the given data frame compile statistics (mean, median, min, max, etc)
    based on the parameters.
 
    :param df1:Larger Dataframe with smaller intervals to create a compiled stat
    :param df2:Smaller Dataframe with larger intervals to create index of intervals
    :return: A list of list of CompiledStat containing the resampled statistics for the
    specified sample and depth by the depth interval from df2.
    
    can only have one depth matching
    '''
    
    dc=FrameClass(df)
    dc_by=FrameClass(by)
    if depth:
        header, = process_header_str(depth)
    else:
        header, = find_match(dc, dc_by)

    df = df.set_index(header.name)
    by= by.set_index(header.name)
    by =by[(by.index >=min(df.index)) & (by.index <=max(df.index))]


    new_df = DataFrame()
    if by.empty:
        return new_df
    for i in range(len(by.index.tolist())-1):

        idx = df[(df.index >=by.index[i]) & (df.index <= by.index[i+1])]

        new_df = new_df.append(idx.apply(lambda x: numpy.nanmean(x)),ignore_index = True)

    new_df =new_df.set_index(by.index[:-1])
    
    return new_df

#####################################################################################################
# LASER DATA FOR EACH RUN
#####################################################################################################


def run_data(directory:str,depth_age_file:str,prefix = 'KCC', depth ='depth (m abs)',output = True):
    '''
    
    Compiles all raw LA-ICP-MS data within the specified directory that share the
        specified prefix, compiles age and depth according to specified depth_age file
    '''
    dfMR = DataFrame()
    dfLR= DataFrame() 
    df_info = DataFrame()
   
    for folder in os.listdir(directory):
        if folder.startswith(prefix):

            for input_folder in sorted(os.listdir(os.path.join(directory,folder))):
                if input_folder.startswith('Input'):
                    for file in sorted(os.listdir(os.path.join(directory,folder,input_folder))):
                        if (file.startswith('InputFile_1')) |(file.startswith('Input') & file.endswith('1')) | (file.startswith('Input') & file.endswith('MR')) | \
                            (file.startswith('Input') & file.endswith('1.txt')) | (file.startswith('Input') & file.endswith('MR.txt')) :
                            
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                            
                            for f in laser_files:
                                dc = FrameClass(process_laser_data(f,depth_age_file))                          

                                dfMR = dfMR.append(pandas.concat([f.info,dc.sample_year_df.mean().to_frame().transpose()],axis=1),ignore_index=True)


                        elif (file.startswith('InputFile_2')) |(file.startswith('Input') & file.endswith('2')) | (file.startswith('Input') & file.endswith('LR')) | \
                            (file.startswith('Input') & file.endswith('2.txt')) | (file.startswith('Input') & file.endswith('LR.txt')) :
                             
                            laser_files = load_input(os.path.join(directory,folder,input_folder,file))
                             
                            for f in laser_files:
                                dc = FrameClass(process_laser_data(f,depth_age_file))                          

                                dfLR = dfLR.append(pandas.concat([f.info,dc.sample_year_df.mean().to_frame().transpose()],axis=1),ignore_index=True)

    if output: 
        output ='Raw_by_Run'
        to_csv(directory,dfMR,'LA-ICP-MS_{}_MR.csv'.format(output),False)
        to_csv(directory,dfLR,'LA-ICP-MS_{}_LR.csv'.format(output),False)
         
        info_file = 'full_core_information.csv'
        if not os.path.isfile(os.path.join(directory,'Output_Files',info_file)):
            to_csv(directory,df_info,info_file,False)
         
        readmeMR=readme_laser_file(laser_template, directory, prefix, depth_age_file, FrameClass(dfMR), 'Medium', str(datetime.date.today()),info_file, 'LA-ICP-MS_{}_MR.csv'.format(output),output,'depth (m abs)')
        readmeLR=readme_laser_file(laser_template, directory, prefix, depth_age_file, FrameClass(dfLR),'Low', str(datetime.date.today()),info_file,'LA-ICP-MS_{}_LR.csv'.format(output),output,'depth (m abs)')
         
        write_readmefile_to_txtfile(readmeMR,os.path.join(directory, 'Output_Files','00README_{}_Medium_Resolution.txt'.format(output)))
        write_readmefile_to_txtfile(readmeLR, os.path.join(directory, 'Output_Files','00README_{}_Low_Resolution.txt'.format(output)))

    return dfMR,dfLR


                             