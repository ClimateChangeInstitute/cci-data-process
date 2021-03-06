'''
A collection of interfaces for working with files.

:author: Mark Royer
'''
import json
from json.encoder import JSONEncoder
import os
from pip.utils import appdirs
import pkg_resources
import sys
from typing import Mapping, IO, Any, Callable, Sequence

from pandas.core.frame import DataFrame

import pandas as pd
import logging


APPNAME = 'CCI-DATA-PROCESSOR'
APPAUTHOR = 'CCI'


def data_dir() -> str:
    directory = appdirs.user_data_dir(APPNAME, APPAUTHOR)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def load_dictionary(file:IO[str], obj_hook:Callable=None) -> Mapping[str, Any]:
    '''
    Load the specified JSON file. If empty, then a warning message is raised 
    and an empty dictionary is returned.  If loading the JSON file from a 
    package, you may want use :py:meth:`climatechange.file.load_dict_by_package` 
    instead of this method.
    
    :param file: The JSON file that will be loaded
    :param obj_hook: If specified, this method will be used for creating 
        objects from the JSON file.
    :return: A Python dictionary object
    '''
    result = {}
    try:
        array = json.load(file, object_hook=obj_hook)

        if isinstance(array, Sequence):
            for r in array:
                result[r.name] = r # The name of the header is the dictionary key
        elif isinstance(array, Mapping):
            pass # do nothing
        else:
            logging.warning("Loaded an unknown dictionary file type.", file=sys.stderr)
    except ValueError:
        contents = file.read()
        if len(contents) > 0:  # File was not empty and still could not read
            logging.warning("Warning unable to parse file %s" % file)
    
    return result
    
def save_dictionary(dictionary:Mapping[str, Any],
                    file_path:str,
                    enc_cls:JSONEncoder=None):
    with open(file_path, 'w') as f:
        json.dump([ h for (_,h) in dictionary.items()], f, cls=enc_cls)


def load_dict_by_package(file_name:str,
                         package:str='climatechange',
                         obj_hook:Callable=None) -> Mapping:
    '''
    Loads the specified file from the given package.  If the file is empty, 
    then a warning message is given and an empty dictionary is returned.
    
    :param package: The package containing the file
    :param file_name: The name of the dictionary file to load
    :param obj_hook: If specified, this method will be used for creating 
        objects from the JSON file.
    :return: A Python dictionary object
    '''
    with open(pkg_resources.resource_filename(package, file_name)) as file:  # @UndefinedVariable
        return load_dictionary(file, obj_hook=obj_hook)

def load_csv(file_name: str) -> DataFrame:
    '''
    Loads a CSV file into a :py:class:`pandas.core.frame.DataFrame` object. 
    
    :param file_name: The name of the CSV file
    :return: A DataFrame object
    '''
    return pd.read_csv(file_name, sep=',')
