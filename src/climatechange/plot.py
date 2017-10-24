'''
Created on Jul 17, 2017

@author: Mark Royer
'''


from matplotlib.backends.backend_pdf import PdfPages



from climatechange.headers import Header, process_header_str
import matplotlib.pyplot as plt
import os
from climatechange.common_functions import DataClass
from typing import List
import subprocess


def plot_samples_by_year(f:str, interval:List=[]):
    
    dc = DataClass(f)
    folder = os.path.join(dc.dirname, 'Output_Files')
    if not os.path.exists(folder):
        os.makedirs(folder)  

    
    for y in dc.year_headers:
        if not interval == []:
            pdf_file = os.path.join(folder,('plot_%s_%.0f-%.0f.pdf'%(y.label,interval[0],interval[1])))
        else:
            pdf_file = os.path.join(folder,('plot_%s.pdf'%(y.label)))
        with PdfPages(pdf_file) as pdf:
            for i,sample in enumerate(dc.sample_headers):
                plot_samples(i,dc,sample,y,pdf, interval)
        try:
            os.startfile(pdf_file)
        except:
            subprocess.call(['open',pdf_file])
        
        
def plot_samples_by_depth(f:str, interval:List=[]):
    
    dc = DataClass(f)
    folder = os.path.join(dc.dirname, 'Output_Files')
    if not os.path.exists(folder):
        os.makedirs(folder)  

    for d in dc.depth_headers:
        if not interval == []:
            pdf_file = os.path.join(folder,('plot_%s_%.3f-%.3f.pdf'%(d.label,interval[0],interval[1])))
        else:
            pdf_file = os.path.join(folder,('plot_%s.pdf'%(d.name)))
        
            with PdfPages(pdf_file) as pdf:
                for i,sample in enumerate(dc.sample_headers):
                    plot_samples(i,dc, sample, d, pdf, interval)
        try:
            os.startfile(pdf_file)
        except:
            subprocess.call(['open',pdf_file])
        
        
    
     
def plot_samples(i:int,dc:DataClass, sample_header:Header, x_header:Header, pdf, interval:List=[]):
    '''
    
    :param dc: DataClass Object
    :param pdf: pdf file
    :param x_header: name of x (depth or year) column
    :param sample header: headers of input sample

    :return: pdf file of data by sample
    '''
   
    if not interval == []:
        df = dc.df[(dc.df[x_header.name] >= interval[0]) & (dc.df[x_header.name] <= interval[1])]
        df = df.set_index(x_header.name)
    else:
        df = dc.df
        df = df.set_index(x_header.name)
    cmap = plt.get_cmap('ocean')
    ax = df[sample_header.name].plot(figsize=(12,6),color=cmap(i / float(len(dc.sample_headers_name)+3)))    
    ax.set_ylabel(sample_header.label)
    ax.set_xlabel(x_header.label)
    plt.tight_layout()
    fig = plt.gcf()
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
