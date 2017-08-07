'''
Created on Jul 17, 2017

@author: Mark Royer
'''
import datetime

from matplotlib.backends.backend_pdf import PdfPages
from pandas.core.frame import DataFrame
from typing import List

from climatechange.file import load_csv
from climatechange.headers import Header
import matplotlib.pyplot as plt


def examplePDFPlot(file_name:str):
    '''
    Just a simple example of how to generated multiple page PDF from DataFrames
    '''
     
    df = load_csv('../../test/csv_files/small.csv')
     
    with PdfPages(file_name) as pdf:
     
        ys = ['Cond (+ALU-S/cm)', 'Na (ppb)', 'Ca (ppb)', 'Dust (part/ml)', 'NH4 (ppb)', 'NO3 (ppb)']
         
        xaxisLabel = 'depth (m we) '
         
        df_indexed:DataFrame = df.set_index(xaxisLabel)
                 
        for i in range(len(ys)):
            fig = plt.figure(figsize=(11, 8.5))
             
            fig, tg = plt.subplots(1)
#             ax = df_indexed.plot(x=df_indexed.index.name, y=ys[i], kind='bar', ax=tg)
#             
#             vals = ax.get_xticks()
#             ax.set_xticklabels(['{:.2f}'.format(x) for x in vals])
             
            ax = df[['depth (m we) ', ys[i]]].plot(x='depth (m we) ', kind='bar', ax=tg, color='C%d' % (i))
                         
            ax = df[[ys[i]]].plot(kind='line', linestyle='-', marker='o', ax=ax, color='C%d' % (i + 1))
             
            vals = ax.get_xticks()
            ax.set_xticklabels(['{:.1f}'.format(x) for x in vals])
             
#             df_indexed.plot(x=df_indexed.index.name, y=ys[i], color='red', ax=tg)
#             plt.plot(df_indexed[ys[i]], '-o', color='C%d' % (i))
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
         
 
 
# def add_plot_to_pdf(pdf, df, bar_header, year_headers, sample_headers, count):
#     for y in year_headers:
#         for s in sample_headers:
#             plt.figure(figsize=(11, 8.5))
#             fig, tg = plt.subplots(1)
#             ax = df[[y, bar_header]].plot(x=y, kind='bar', ax=tg, color='C%d' % (count%10))
#             count += 1
#             ax = df[[s]].plot(kind='line', linestyle='-', marker='o', ax=ax, color='C%d' % (count%10))
#             count += 1
#             vals = ax.get_xticks()
#             ax.set_xticklabels(['{:.1f}'.format(x) for x in vals])
#             plt.title('%s vs. %s' % (s, y))
#             plt.xlabel(y)
#             plt.ylabel(s)
#             plt.legend()
#     
#             pdf.savefig(fig)
# 
# def create_csv_pdf_resampled_by_years(df:DataFrame, headers: List[Header], file_name:str, bar_header:str='Mean') -> str:
#     '''
#     Create a pdf file with multiple plots based on the data frame.
#     :param df: The data frame
#     :param file_name: The absolute path of the file
#     :return: The file path of the created PDF
#     '''
#     
#     with PdfPages(file_name) as pdf:
#     
#         year_headers:List[str] = [h.original_value for h in headers if h.htype == HeaderType.YEARS]
#         depth_headers:List[str] = [h.original_value for h in headers if h.htype == HeaderType.DEPTH]
#         
#         sample_headers:List[str] = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
#         
#         add_plot_to_pdf(pdf, df, bar_header, year_headers, sample_headers, 1)
#         offset = len(year_headers)
#         add_plot_to_pdf(pdf, df, bar_header, depth_headers, sample_headers, offset)
#         
#         plt.close()
#             
#                 
#         # Meta data for the PdfPages
#         d = pdf.infodict()
#         d['Title'] = 'CCI Plot'
#         d['Author'] = u'Some author'
#         d['Subject'] = 'CCI Data Parser output'
#         d['Keywords'] = 'CCI UMaine'
#         d['CreationDate'] = datetime.datetime.today()
#         d['ModDate'] = datetime.datetime.utcnow()  
# 
# def create_single_pdf(df:DataFrame,
#                year_name:str,
#                sample_name:str,
#                rdf:DataFrame,
#                file_name:str, 
#                bar_year_header:str='Year',
#                bar_header:str='Mean') -> str:
#     '''
#     Create a pdf file with multiple plots based on the data frame.
#     :param df: The data frame
#     :param file_name: The absolute path of the file
#     :return: The file path of the created PDF
#     '''
#     
#     with PdfPages(file_name) as pdf:
#     
#         plt.figure(figsize=(11, 8.5))
#         fig, tg = plt.subplots(1)   
#         ax = rdf[[bar_year_header, bar_header]].plot(x=bar_year_header, kind='line',color='r', ax=tg)
#         ax = df[[year_name, sample_name]].plot(x=year_name, kind='line',
#                                                linestyle='-',
#                                                color='0.75',
#                                                ax=tg,zorder=-1)
#         vals = ax.get_xticks()
#         ax.set_xticklabels(['{:.1f}'.format(x) for x in vals])
#         
#         plt.title('Resampled %s of %s' % (bar_header, sample_name))
#         plt.xlabel(year_name)
#         plt.ylabel(sample_name)
#         plt.legend()
#         plt.show()
#         pdf.savefig(fig)
#                 
#         # Meta data for the PdfPages
#     d = pdf.infodict()
#     d['Title'] = 'CCI Plot'
#     d['Author'] = u'Some author'
#     d['Subject'] = 'CCI Data Parser output'
#     d['Keywords'] = 'CCI UMaine'
#     d['CreationDate'] = datetime.datetime.today()
#     d['ModDate'] = datetime.datetime.utcnow()


def write_resampled_data_to_csv_files(df:DataFrame, file_path:str):
    df.to_csv(file_path,index=False)

# def add_compile_stats_to_pdf(f:str,
#                              df:DataFrame,
#                              pdf,
#                              x_name:str,
#                              headers:Header,
#                              inc_amt:float,
#                              bar_header:str) -> str:
#     '''
#     
#     :param f: input file path
#     :param df: dataframe of input file
#     :param pdf: pdf file
#     :param x_name: name of year column
#     :param headers: headers of input dataframe
#     :param bar_header: header of statistic to plot
#     
#     :return: csv files with statistics resampled of bar_header, 
#         pdf files of statistics with raw data
#     '''
#     
#     sample_headers = [h.original_value for h in headers if h.htype == HeaderType.SAMPLE]
#     for sample_name in sample_headers:
#         if HeaderDictionary().parse_headers([x_name])[0].htype == HeaderType.YEARS:
#             df_resampled_stats = compile_stats_by_year(df, headers, x_name, sample_name)
#             label_name='Year'
#         else:
#             df_resampled_stats = compile_stats_by_depth(df,x_name, sample_name)
#             label_name='Depth'
#             
#         df_name=df_resampled_stats.columns[0]
#         write_resampled_data_to_csv_files(df_resampled_stats, f + ('_resampled_%s_%s.csv' % (x_name, sample_name.replace("/",""))))

def add_compile_stats_to_pdf(f:str,
                             df:DataFrame,
                             df_resampled_stats:DataFrame,
                             pdf,
                             x_name:str,
                             sample:Header,
                             inc_amt:float,
                             label_name:str,
                             stat_header:str='Mean') -> str:
    '''
    
    :param f: input file path
    :param df: dataframe of input file
    :param pdf: pdf file
    :param x_name: name of year column
    :param headers: headers of input dataframe
    :param stat_header: header of statistic to plot
    
    :return: csv files with statistics resampled of stat_header, 
        pdf files of statistics with raw data
    '''
    print(sample)
    print(sample.htype)
            
    df_name=df_resampled_stats.columns[0]
    plt.figure(figsize=(11, 8.5))
    fig, tg = plt.subplots(1)
    ax = df_resampled_stats[[df_name, stat_header]].plot(x=df_name, kind='line',color='r', ax=tg)
    ax = df[[x_name, sample.name]].plot(x=x_name, kind='line',
                                           linestyle='-',
                                           color='0.75',
                                           ax=tg,zorder=-1)
    vals = ax.get_xticks()
    if label_name=='depth':
        x_str='{:.%sf}' %str(inc_amt)[::-1].find('.')
        ax.set_xticklabels([x_str.format(x) for x in vals])
        plt.xlabel(x_name)
        plt.title('%s: %s inc. %s resolution' % (sample.hclass,inc_amt,label_name))
        #add class name instead of sample name
    else:
        ax.set_xticklabels(['{:.0f}'.format(x) for x in vals])
        plt.xlabel('Year CE')
        plt.title('%s: %s %s resolution' % (sample.hclass,inc_amt,label_name))
    
    plt.ylabel(sample.label)
    plt.legend()    
    pdf.savefig(fig)
    plt.close()

# def create_csv_pdf_resampled(f:str,
#                              df:DataFrame,
#                              x_name:str,
#                              headers:Header,
#                              inc_amt:float,
#                              bar_header:str='Mean')->str:
#     '''
#     Create a pdf file with multiple plots based on the data frame.
#     :param f: input file path
#     :param df: dataframe of input file
#     :param x_name: name of x column (year or depth)
#     :param headers: headers of input dataframe
#     :param bar_header: header of statistic to plot
#     
#     :return: pdf of compiled figures by year,
#         csv file of statistics by sample and year
#     '''
#     file_name=f + ('_resampled_%s.pdf' % x_name)
#     with PdfPages(file_name) as pdf:
#         add_compile_stats_to_pdf(f, df, pdf, x_name, headers,inc_amt, bar_header)    
#         plt.close()
#                     # Meta data for the PdfPages
# #         d = pdf.infodict()
# #         d['Title'] = 'CCI Plot'
# #         d['Author'] = u'Some author'
# #         d['Subject'] = 'CCI Data Parser output'
# #         d['Keywords'] = 'CCI UMaine'
# #         d['CreationDate'] = datetime.datetime.today()
# #         d['ModDate'] = datetime.datetime.utcnow() 
# 
# # if __name__ == '__main__':
# #     examplePDFPlot('test.pdf')
