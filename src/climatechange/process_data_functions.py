'''
Created on Jul 24, 2017

:author: Mark Royer
'''

from pandas.core.frame import DataFrame
from typing import List

import numpy

from climatechange import plot, resampleStats
from climatechange.file import load_csv
from climatechange.headers import HeaderDictionary, HeaderType, Header
from climatechange.lstDataframe import lstToDataframe
from climatechange.resampleStats import compile_stats_by_year


def process_header_data(df) -> List[Header]:
    
    hd = HeaderDictionary()
    
    parsedHeaders = hd.parse_headers(list(df.columns))
    
    unknownHeaders = [ h for h in parsedHeaders if h.htype == HeaderType.UNKNOWN ]
    
#     print("All headers are: %s" % parsedHeaders)
#     print("Unknown headers are: %s" % unknownHeaders)
    
    return parsedHeaders

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


def create_statistics(df: DataFrame, headers: List[Header], year:str, sample:str) -> DataFrame:
    return compile_stats_by_year(df, headers, year, sample)
    

def write_resampled_data_to_csv_files(df:DataFrame, file_path:str):
    df.to_csv(file_path)


def create_pdf(f:str):
    '''
    
    :param: f: This is a CSV file
    '''
    print("Creating pdf for %s" % f)
    
    df = load_csv(f)
    
    headers = process_header_data(df)

    df = clean_data(df)

    year_headers = [h.original_value for h in headers if h.htype == HeaderType.YEARS]

    depth_headers = [h.original_value for h in headers if h.htype == HeaderType.DEPTH]

    sample_headers = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]

    for y in year_headers:
        for s in sample_headers:
            df_resampled_stats = create_statistics(df, headers, y, s)

            plot.create_single_pdf(df, y, s, df_resampled_stats, f + ('.out.%s.%s.pdf' % (y, s.replace("/",""))),bar_year_header=y)
            write_resampled_data_to_csv_files(df_resampled_stats, f + ('.out.%s.%s.csv' % (y, s.replace("/",""))))
    
    
    
def main(files):
    
    for f in files:
        create_pdf(f)
    
