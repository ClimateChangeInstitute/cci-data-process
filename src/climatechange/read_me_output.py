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

Ex. Of name of csv files
({f_base}.resampledby_{inc_amt}_years_yearname_samplename

For each Year and sample, CSV files containing: 
Years at {inc_amt} Year Resolution
top depth (m we) bottom depth (m we)
top depth(m abs) bottom depth (m abs)
Mean, Standard Deviation, Median, Maximum, Minimum, Count

[# of PDF files] PDF files created

Ex. of name of pdf files
(name of file).resampledto_inc_amt_year_resolution_for_nameofdepth

For each Year, PDF files containing:
raw sample data vs. years
resampled mean data vs. resampled years
'''
