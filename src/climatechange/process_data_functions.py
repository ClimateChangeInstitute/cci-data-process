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


def create_statistics(df: DataFrame, headers: List[Header]) -> DataFrame:
    
#     result = resampleStats.compileStats(df.values.tolist())
#     print("Rows is %d " % len(result))
#     print("Columns is %d " % len(result[0]))
    
    compile_stats_by_year(df, headers, 'Dat210617', 'Na (ppb)')
    
    return df
#     return DataFrame(data=resampleStats.compileStats(df.values.tolist()),
#                      index=df.index,
#                      columns=df.columns)


def write_resampled_data_to_csv_files(df):
    pass


def create_pdf(f:str):
    '''
    
    :param: f: This is a CSV file
    '''
    print("Creating pdf for %s" % f)
    
    df = load_csv(f)
    
    headers = process_header_data(df)

    df = clean_data(df)

    df_resampled_stats = create_statistics(df, headers)
    

    # Plot all of the raw data
    # year vs each element
    # depth vs each element
    plot.create_pdf(df, f + '.out.pdf')

    write_resampled_data_to_csv_files(df_resampled_stats)
    
def main(files):
    
    for f in files:
        create_pdf(f)
    
