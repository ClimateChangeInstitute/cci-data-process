'''
A collection of interfaces for working with files.

:author: Mark Royer
'''
import json
import os
from pip.utils import appdirs
from typing import Mapping, IO, Any
import warnings

from pandas.core.frame import DataFrame
import pkg_resources

import pandas as pd


APPNAME = 'CCI-DATA-PROCESSOR'
APPAUTHOR = 'CCI'

def data_dir() -> str:
    directory = appdirs.user_data_dir(APPNAME, APPAUTHOR)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def load_dictionary(file:IO[str]) -> Mapping[str, str]:
    '''
    Load the specified JSON file. If empty, then a warning message is raised 
    and an empty dictionary is returned.  If loading the JSON file from a 
    package, you may want use :py:meth:`climatechange.file.load_dict_by_package` 
    instead of this method.
    
    :param: file: The JSON file that will be loaded
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

    
def save_dictionary(dictionary:Mapping[str, Any], file_path:str):
    with open(file_path, 'w') as f:
        json.dump(dictionary, f)


def load_dict_by_package(file_name:str, package:str='climatechange') -> Mapping[str, str]:
    '''
    Loads the specified file from the given package.  If the file is empty, 
    then a warning message is given and an empty dictionary is returned.
    
    :param: package: The package containing the file
    :param: file_name: The name of the dictionary file to load
    :return: A Python dictionary object
    '''
    with open(pkg_resources.resource_filename(package, file_name)) as file:  # @UndefinedVariable
        return load_dictionary(file)

def load_csv(file_name: str) -> DataFrame:
    '''
    Loads a CSV file into a :py:class:`pandas.core.frame.DataFrame` object. 
    
    :param: file_name: The name of the CSV file
    :return: A DataFrame object
    '''
    return pd.read_csv(file_name, sep=',')
