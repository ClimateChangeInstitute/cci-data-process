'''
Created on Aug 2, 2017

@author: Heather
'''

template=
'''
Template for text file for README file:

Cci-data-processor
Authors:
Date ran:
Time to run:

Input filename: CFA..
Process: Resampled to {inc_amt} Year Resolution
Years Resampled: Dat7123, Dat234V2
Depths: depth(m we), depth(m abs)
Samples: Na(ppb), Ca(ppb)

Output Files:
[# of output csv files] CSV files created

Ex. Of name of csv files
(name of file).resampledby_{inc_amt}_years_yearname_samplename

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
