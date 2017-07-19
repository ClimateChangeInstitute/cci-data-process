'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import pandas as pd
from pandas.core.frame import DataFrame
import os
os.chdir('C:\\Users\\Heather\\Documents\\GitHub\\cci-data-process\\test\\csv_files')
import json
import numpy as np
import HeaderDictionary


def lstToDataframe(lst):
    return pd.DataFrame(lst).transpose()

def incAnnual(lst):
    #creates lists of years incrementally by 1 year,
    #lst must be Years
    return [x for x in range(int(min(lst)),int(max(lst))+1,1)], [x+1 for x in range(int(min(lst)),int(max(lst))+1,1)]

def find_indices(lst,condition):
    #find indices of the specific condition called
    return [j for j, elem in enumerate(lst) if condition(elem)]

def annualIndices(lst):
    ytop,ybot=incAnnual(lst)
    return [ytop,[find_indices(lst,lambda e: e>=ytop[i] and e<ybot[i]) for i in range(0,len(ytop))]]

def get_data_frame_from_csv(csvFileName: str) -> DataFrame:
    '''
    
    :param csvFileName:
    '''
    return pd.read_csv(csvFileName,sep=',')

def findMean(array:List[List[float]]) -> List[float]:
    '''
    find mean value of each list within a list
    :param array: list of lists, 2D array of floats
    :return: list of mean values for each list
    '''
    return [np.nanmean(i) for i in array]  

small=get_data_frame_from_csv('small.csv')

os.chdir('C:\\Users\\Heather\\Documents\\GitHub\\cci-data-process\\src\\climatechange')
#data = json.load(open('header_dict.json', 'r'))

data = HeaderDictionary().get_header_dict()


for i in list(small.columns.values):
    for j in data.keys():
        if i == j:
            if data[j]=='Years':
                g=list(small[i])

yr=annualIndices(g)
df=lstToDataframe(yr)

#for column in small:
#    for elem,frame in enumerate(small[column]):
#        for indx,value in enumerate(df[1]):
#            print (indx)
#            print(value)
#            print(list(small.iloc[value,[0]]))
#            print(list(small.iloc[indx,[0]]))
##            for num in value:
#                h=findMean(small[column][num])
#                if column==0
#                    meann=findMean(small[column][num])
#                else:
#                    meann.append(h) 

#for column,name in enumerate(small):
#    for value,indx in enumerate(df[1]):
##        print(list(small.iloc[value,[0]]))
#        x=small.iloc[indx,[column]]
#        new_p=pd.np.array(x)
#        j=new_p.tolist()
#        c.append(j)
#        print (new_p)
#        print(j)
#        g[column]=new_p
        
        
#        meann=findMean(pd.np.array(small.iloc[indx,[column]]))
        
        