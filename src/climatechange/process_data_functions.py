'''
Created on Jul 24, 2017

:author: Mark Royer
'''
import os

from climatechange import plot
from climatechange.file import load_csv
from climatechange.headers import HeaderDictionary, HeaderType


def getFolder() -> str:
    return '../../data/KCC_210617'


def select_year_column(df):
    return df


def select_depth_column(df):
    return df


def process_header_data(df):
    
    hd = HeaderDictionary()
    
    unknownHeaders = [ h for h in hd.parse_headers(list(df.columns)) if h.htype == HeaderType.UNKNOWN ]
    
    print("Unknown headers are: %s" % unknownHeaders)
    
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
    
    :param: f: This is a CSV file
    '''
    print("Creating pdf for %s" % f)
    
    df = load_csv(f)
    
    df = process_header_data(df)

    df = clean_data(df)

    # Plot all of the raw data
    # year vs each element
    # depth vs each element
    plot.create_pdf(df, f + '.out.pdf')

    df_resampled_stats = create_statistics(df)
    
    write_resampled_data_to_csv_files(df_resampled_stats)
    
def main():
    
    folder = getFolder()

    for f in os.listdir(folder):
        if f.endswith('.csv') :
            create_pdf(os.path.join(folder, f))
    
