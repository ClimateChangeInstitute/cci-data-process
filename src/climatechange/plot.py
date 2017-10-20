'''
Created on Jul 17, 2017

@author: Mark Royer
'''


from matplotlib.backends.backend_pdf import PdfPages



from climatechange.headers import Header
import matplotlib.pyplot as plt
import os
from climatechange.common_functions import DataClass
from typing import List


def plot_samples_by_year(f:str, interval:List=[]):
    
    dc = DataClass(f)
    if not interval == []:
        pdf_file = os.path.join(dc.dirname,('plot_%s_year_%.0f-%.0f.pdf'%(dc.base,interval[0],interval[1])))
    else:
        pdf_file = os.path.join(dc.dirname,('plot_%s_year.pdf'%(dc.base)))
    with PdfPages(pdf_file) as pdf:
        for year in dc.year_headers:
            for sample in dc.sample_headers:
                plot_samples(dc,sample,year,pdf, interval)
    os.startfile(pdf_file)
        
        
def plot_samples_by_depth(f:str, interval:List=[]):
    
    dc = DataClass(f)
    if not interval == []:
        pdf_file = os.path.join(dc.dirname,('plot_%s_depth_%.3f-%.3f.pdf'%(dc.base,interval[0],interval[1])))
    else:
        pdf_file = os.path.join(dc.dirname,('plot_%s_depth.pdf'%(dc.base)))
        
    with PdfPages(pdf_file) as pdf:
        for depth in dc.depth_headers:
            for sample in dc.sample_headers:
                plot_samples(dc, sample, depth, pdf, interval)
    os.startfile(pdf_file)
        
    
     
def plot_samples(dc:DataClass, sample_header:Header, x_header:Header, pdf, interval:List=[]):
    '''
    
    :param dc: DataClass Object
    :param pdf: pdf file
    :param x_header: name of x (depth or year) column
    :param sample header: headers of input sample

    :return: pdf file of data by sample
    '''
   
    if not interval == []:
        df = dc.df[(dc.df[x_header.name] >= interval[0]) & (dc.df[x_header.name] <= interval[1])]
    else:
        df = dc.df
        
        
    plt.figure(figsize=(11, 8.5))
    fig, tg = plt.subplots(1)
    ax = df[[x_header.name, sample_header.name]].plot(x=x_header.name, kind='line',
                                           linestyle='-',
                                           color='b',
                                           ax=tg,zorder=-1)
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:.0f}'.format(x) for x in vals])
    plt.xlabel(x_header.label)
    plt.title('%s Data' % (sample_header.hclass))
    plt.ylabel(sample_header.label)
    plt.legend()    
    pdf.savefig(fig)
    plt.close()

                  
#         # Meta data for the PdfPages
#         d = pdf.infodict()
#         d['Title'] = 'CCI Plot'
#         d['Author'] = u'Some author'
#         d['Subject'] = 'CCI Data Parser output'
#         d['Keywords'] = 'CCI UMaine'
#         d['CreationDate'] = datetime.datetime.today()
#         d['ModDate'] = datetime.datetime.utcnow()
#           
#   


 
# # if __name__ == '__main__':
# #     examplePDFPlot('test.pdf')
