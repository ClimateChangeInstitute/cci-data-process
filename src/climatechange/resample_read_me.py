'''
Created on Oct 18, 2017

@author: Heather
'''


import os

from climatechange.headers import HeaderType


resample_template = \
'''
ReadMeFile

CCI-Data-Processor
Authors: Mark Royer and Heather Clifford
Date ran: {run_date}

Process: Resample Input Data to {inc_amt} {label_name} by {stat_header} Resolution

Input filename: {file_name}
Years: {years}
Depths: {depths}
Samples: {samples}

Output Files:
 
{csv_filename}

'''

def write_readmefile_to_txtfile(readme:str, output_filename:str):
    with open(output_filename, "w") as text_file:
        text_file.write(readme)
        text_file.flush()
        

def readme_output_file(resample_template,dc,run_date, inc_amt, label_name, stat_header,file):


#     output_filename=os.path.join('00README')

    data = {'run_date': run_date,
            'file_name':dc.base_ext,
            'inc_amt':inc_amt,
            'label_name':label_name,
            'years':dc.year_headers_name,
            'depths':dc.depth_headers_name,
            'samples':dc.sample_headers_name,
            'f_base':dc.base,
            'sample_name':dc.sample_headers[0],
            'file_headers':dc.year_headers_label,
            'stat_header':stat_header,
            'csv_filename':'\n'.join(file)}
 

    
    return resample_template.format(**data)
    
