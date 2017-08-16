'''
Created on Aug 2, 2017

@author: Heather
'''
from climatechange.headers import HeaderType
import os
template=\
'''
ReadMeFile

CCI-Data-Processor
Authors: Mark Royer and Heather Clifford
Date ran:{run_date}

Process: Resample Input Data to {inc_amt} {label_name} Resolution

Input filename: {file_name}
Years: {years}
Depths: {depths}
Samples: {samples}

Output Files:
[{#csvfiles}] CSV files created

Ex. Of CSV file name: 
{f_base}_stats_Resampled_{inc_amt}_{x_name}_Resolution_for_{sample_name}.csv

For each {label_name} and Sample, CSV files containing:
{file_headers}


[{#PDFfiles}] PDF files created

Ex. of PDF filename:
{f_base}_plots_Resampled_{inc_amt}_{x_name}_Resolution.pdf

For Each {label_name}, PDF files containing:
-Plot for Each Sample with:
    Raw Sample Data vs. {label_name}
    Resampled {stat_header} Data vs. {inc_amt} {label_name} Resolution
'''
def write_readmefile_to_txtfile(readme:str,output_filename:str):
    with open(output_filename, "w") as text_file:
        text_file.write(readme)
        text_file.flush()
        

def create_readme_output_file(template,f,headers,run_date,inc_amt,label_name,x_headers,file_headers,num_csvfiles,stat_header):
    year_headers = [h.name for h in headers if h.htype == HeaderType.YEARS]
    depth_headers = [h.name for h in headers if h.htype == HeaderType.DEPTH]
    sample_headers = [h.name for h in headers if h.htype == HeaderType.SAMPLE]
    num_pdffiles=len(file_headers)
    f_base=os.path.basename(f)
    
#     output_filename=os.path.join('00README')
    data = {'run_date': run_date,
            'file_name':os.path.basename(f),
            'inc_amt':inc_amt,
            'label_name':label_name,
            'years':year_headers,
            'depths':depth_headers,
            'samples':sample_headers,
            '#csvfiles':num_csvfiles,
            '#PDFfiles':num_pdffiles,
            'f_base':os.path.splitext(f_base)[0],
            'x_name':file_headers[0],
            'sample_name':sample_headers[0],
            'file_headers':file_headers,
            'stat_header':stat_header}
 

    
    return template.format(**data)
    