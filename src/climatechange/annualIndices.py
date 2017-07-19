'''
Created on Jul 18, 2017

@author: Heather
'''
def increments_by_year(lst):
    #creates lists of years incrementally by 1 year,
    #lst must be Years
    return [x for x in range(int(min(lst)),int(max(lst))+1,1)], [x+1 for x in range(int(min(lst)),int(max(lst))+1,1)]

def find_indices(lst,condition):
    #find indices of the specific condition called
    return [j for j, elem in enumerate(lst) if condition(elem)]

def index_by_year(lst):
    ytop,ybot=increments_by_year(lst)
    return [ytop,[find_indices(lst,lambda e: e>=ytop[i] and e<ybot[i]) for i in range(0,len(ytop))]]

