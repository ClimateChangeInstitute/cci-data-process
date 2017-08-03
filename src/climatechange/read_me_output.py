'''
Created on Aug 2, 2017

@author: Heather
'''
from climatechange.headers import HeaderType
import os
template=\
'''
ReadMeFile

CCI-data-processor
Authors: Mark Royer and Heather Clifford
Date ran:{date}
Time to run:{time}

Process: Resample Input Data to {inc_amt} {label_name} Resolution

Input filename: {file_name}
Years: {years}
Depths: {depths}
Samples: {samples}

Output Files:
[{#csvfiles}] CSV files created

Ex. Of name of csv file name: 
{f_base}_stats_{inc_amt}_inc_resolution_{x_name}_{sample_name}.csv

For each {label_name} and sample, CSV files containing:
{file_headers}
% need if statement in code
{stat_headers}


[{#PDFfiles}] PDF files created

Ex. of name of pdf file name:
{f_base}_plots_{inc_amt}_{label_name}_resolution_{x_name}.pdf

For each {label_name}, PDF files containing:
-plot for each sample with:
    raw sample data vs. {label_name}
    resampled mean data vs. {inc_amt}_{label_name}_resolution
'''
# def write_readmefile_to_csv(readme:str,output_filename):
#     data = ['a,x', 'b,y', 'c,z']
#     f = open('data.csv', 'wb')
#     w = csv.writer(f, delimiter = ',')
#     w.writerows([x.split(',') for x in data])
#     f.close()

def create_readme_output_file(template,f,headers,time_ran,run_date,inc_amt,label_name,file_headers):
    stat_headers=['Mean', 'Stdv', 'Median', 'Max', 'Min', 'Count']
    year_headers = [h.original_value for h in headers if h.htype == HeaderType.YEARS]
    depth_headers = [h.original_value for h in headers if h.htype == HeaderType.DEPTH]
    sample_headers = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
    num_csvfiles=len(file_headers)*len(sample_headers)
    num_pdffiles=len(file_headers)
    
#     output_filename=os.path.join('00README')
    data = {'run_date': run_date,
            'time': time_ran,
            'file_name':f,
            'inc_amt':inc_amt,
            'label_name':label_name,
            'years':year_headers,
            'depths':depth_headers,
            'samples':sample_headers,
            '#csvfiles':num_csvfiles,
            '#PDFfiles':num_pdffiles,
            'f_base':os.path.splitext(f)[0],
            'x_name':file_headers[0],
            'sample_name':sample_headers[0],
            'file_headers':file_headers,
            'stat_headers':stat_headers}
 

    result=template.format(**data)
    print(result)
    return result
    