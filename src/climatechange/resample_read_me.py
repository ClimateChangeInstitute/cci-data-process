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

Process: Resample Input Data to {inc_amt} {label_name} Resolution

Input filename: {file_name}

Years: {years}

Depths: {depths}

Samples: {samples}

Resampled by: {inc_amt} {label_name}

Statistics Ran : {stat_header}

Output Files:
 
{csv_filename}

'''

laser_template = \
'''
ReadMeFile

CCI-Data-Processor
Authors: Mark Royer and Heather Clifford
Date ran: {run_date}

Process: Process and Compile {type} LA-ICP-MS Data

Directory Folder: {directory}

Prefix of Cores: {prefix}

Cores in Directory = {folders}

Depth Age File = {depth_age_file}

Type of Process: {type}


***  Additional Information about Individual Cores & Runs found in file:
         {info_file}

Directory Information:

    Year: {years}
    Year Range: {year_min} - {year_max}

    Depth: {depths}
    Depth Range: {depth_min} - {depth_max}
    
    Resolution: {resolution}
    
    Samples: {samples}
    

Output Files:
 
{csv_filename}

'''

def write_readmefile_to_txtfile(readme:str, output_filename:str):
    with open(output_filename, "w") as text_file:
        text_file.write(readme)
        text_file.flush()



def readme_output_file(resample_template,dc,run_date, inc_amt, label_name, stat_header,file):

    if stat_header == None:
        stat_header = '25%, 50%, 70%, count, max, mean, min, std'
    if type(inc_amt)==str:
        inc_amt = 'file -{}'.format(inc_amt)
        label_name =''
#     output_filename=os.path.join('00README')

    data = {'run_date': run_date,
            'file_name':dc.base_ext,
            'inc_amt':inc_amt,
            'label_name':label_name,
            'years':', '.join(dc.year_headers_name),
            'depths':', '.join(dc.depth_headers_name),
            'samples':', '.join(dc.sample_headers_name),
            'f_base':dc.base,
            'sample_name':dc.sample_headers[0],
            'file_headers':dc.year_headers_label,
            'stat_header':stat_header,
            'csv_filename':'\n'.join(file)}
 

    
    return resample_template.format(**data)



def readme_laser_file(laser_template,directory,prefix,depth_age_file, dc, resolution, run_date,info_file, file, output_type,depth = None):
    
    folders = []
    for folder in os.listdir(directory):
        if folder.startswith(prefix):
            folders.append(os.path.basename(folder))
    if depth:
        d=depth
        d_min =float(dc.df['top_depth'].min())
        d_max =float(dc.df['top_depth'].max())
        
    else:
        d=dc.df.index.name
        d_min =float(dc.df.index.min())
        d_max =float(dc.df.index.max())

    data = {'run_date': run_date,
            'directory':os.path.basename(directory),
            'folders':', '.join(folders),
            'depth_age_file':os.path.basename(depth_age_file),
            'years':', '.join(dc.year_headers_name),
            'depths':d,
            'samples':', '.join(dc.sample_headers_name),
            'resolution':resolution,
            'prefix':prefix,
            'info_file':info_file,
            'year_min':str(int(dc.year_df.min())),
            'year_max':str(int(dc.year_df.max())),
            'depth_min':d_min,
            'depth_max':d_max,
            'csv_filename':os.path.basename(file),
            'type':output_type}
 

    
    return laser_template.format(**data)
    
    
