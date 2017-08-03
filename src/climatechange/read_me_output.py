'''
Created on Aug 2, 2017

@author: Heather
'''

template=
'''
Template for text file for README file:

CCI-data-processor
Authors: Mark Royer and Heather Clifford
Date ran:{date}
Time to run:{time}

Input filename: {file_name}
Process: Resample Input Data to {inc_amt} {label_name} Resolution
Years: {years}
Depths: {depths}
Samples: {samples}

Output Files:
[{#csvfiles}] CSV files created

Ex. Of name of csv file name: 
{f_base}_stats_{inc_amt}_inc_resolution_{x_name}_{sample_name}.csv

For each {label_name} and sample, CSV files containing:
{year_file_headers}
{stat_headers}
if resampled by depth:
{depth_file_headers}
{stat_headers}


[{#ofPDFfiles}] PDF files created

Ex. of name of pdf files
(name of file).resampledto_inc_amt_year_resolution_for_nameofdepth

For each Year, PDF files containing:
raw sample data vs. years
resampled mean data vs. resampled years
'''
