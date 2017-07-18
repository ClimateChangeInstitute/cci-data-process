'''
Created on Jul 17, 2017

@author: Mark Royer
'''
import datetime
from matplotlib.backends.backend_pdf import PdfPages

from climatechange.file import get_data_frame_from_csv
import matplotlib.pyplot as plt


def examplePDFPlot():
    '''
    Just a simple example of how to generated multiple page PDF from DataFrames
    '''
    
    df = get_data_frame_from_csv('../../test/csv_files/small.csv')
    
    with PdfPages('pdf_output.pdf') as pdf:
    
        ys = ['Cond (+ALU-S/cm)', 'Na (ppb)', 'Ca (ppb)', 'Dust (part/ml)', 'NH4 (ppb)', 'NO3 (ppb)']
        
        xaxisLabel = 'depth (m we) '
        
        df_indexed = df.set_index(xaxisLabel)
                
        for i in range(len(ys)):
            fig = plt.figure(figsize=(11, 8.5))
            
            plt.plot(df_indexed[ys[i]], '-o', color='C%d' % (i))
            plt.title('The title of plot %d' % (i + 1))
            plt.xlabel('x axis %s' % xaxisLabel)
            plt.ylabel(ys[i])
            plt.legend()
        
            pdf.savefig(fig)
            plt.close()
            
                
        # Meta data for the PdfPages
        d = pdf.infodict()
        d['Title'] = 'CCI Plot'
        d['Author'] = u'Some author'
        d['Subject'] = 'CCI Data Parser output'
        d['Keywords'] = 'CCI UMaine'
        d['CreationDate'] = datetime.datetime.today()
        d['ModDate'] = datetime.datetime.utcnow()

examplePDFPlot()
