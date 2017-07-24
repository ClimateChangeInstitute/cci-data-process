'''
Created on Jul 24, 2017

:author: Mark Royer
'''

from pandas.core.frame import DataFrame

import numpy

from climatechange import plot
from climatechange.file import load_csv
from climatechange.headers import HeaderDictionary, HeaderType


def process_header_data(df):
    
    hd = HeaderDictionary()
    
    parsedHeaders = hd.parse_headers(list(df.columns))
    
    unknownHeaders = [ h for h in parsedHeaders if h.htype == HeaderType.UNKNOWN ]
    
    print("All headers are: %s" % parsedHeaders)
    print("Unknown headers are: %s" % unknownHeaders)
    
    return df

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def clean_data(df):
    
    # Remove zeroes.  Zeroes go to nan
    values = df.values
    
    for r in values :
        for i in range(len(r)):
            if r[i] == 0:
                r[i] = numpy.nan
    
    # Replace str values with nan
    for r in values :
        for i in range(len(r)):
            if not is_number(r[i]):
                r[i] = numpy.nan 
    
    df = DataFrame(data=values, index=df.index, columns=df.columns)
    
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
    
def main(files):
    
    for f in files:
        create_pdf(f)
    
