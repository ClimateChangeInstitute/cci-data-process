'''
Created on Jul 18, 2017

:author: Mark Royer
:author: Heather Clifford
'''
import os

from climatechange import plot
from climatechange.file import get_data_frame_from_csv


def getFolder() -> str:
    return '../../data/KCC_210617'


def select_year_column(df):
    return df


def select_depth_column(df):
    return df


def process_header_data(df):
    
    df = select_year_column(df)
    
    df = select_depth_column(df)
    
    return df


def clean_data(df):
    return df


def create_statistics(df):
    return df


def write_resampled_data_to_csv_files(df):
    pass


def create_pdf(f:str):
    '''
    
    :param f: This is a CSV file
    '''
    print("Creating pdf for %s" % f)
    
    df = get_data_frame_from_csv(f)
    
    df = process_header_data(df)

    df = clean_data(df)

    # Plot all of the raw data
    # year vs each element
    # depth vs each element
    plot.create_pdf(df, f + '.out.pdf')

    df_resampled_stats = create_statistics(df)
    
    write_resampled_data_to_csv_files(df_resampled_stats)
    
    
    
if __name__ == '__main__':
    
    print(os.path.abspath('.'))
    
    folder = getFolder()

    for f in os.listdir(folder):
        if f.endswith('.csv') :
            create_pdf(os.path.join(folder, f))
