'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import json
from pandas.core.frame import DataFrame
from typing import Mapping, IO
import warnings

import pandas as pd
import pkg_resources

def load_dictionary(file:IO[str]) -> Mapping[str, str]:
    '''
    Load the specified JSON file. If empty, then a warning message is raised 
    and an empty dictionary is returned.  If loading the JSON file from a 
    package, you may want use :py:meth:`climatechange.load_dictionary_package` 
    instead of this method.
    :param file: The JSON file that will be loaded
    :return: A Python dictionary object
    '''
    result = {}
    try:
        result = json.load(file)
    except ValueError:
        contents = file.read()
        if len(contents) > 0:  # File was not empty and still could not read
            warnings.warn("Warning unable to parse file %s" % file)
    
    return result

def load_dict_by_package(file_name:str, package:str='climatechange') -> Mapping[str, str]:
    '''
    Loads the specified file from the given package.  If the file is empty, 
    then a warning message is given and an empty dictionary is returned.
    
    :param package: The package containing the file
    :param file_name: The name of the dictionary file to load
    :return: A Python dictionary object
    '''
    with open(pkg_resources.resource_filename(package, file_name)) as file:  # @UndefinedVariable
        return load_dictionary(file)
    

def get_data_frame_from_csv(csvFileName: str) -> DataFrame:
    '''
    
    :param csvFileName:
    '''
    return pd.read_csv(csvFileName, sep=',')
