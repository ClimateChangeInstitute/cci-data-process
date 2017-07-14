'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import json
import pkg_resources
import re
from typing import IO, Mapping, Tuple, List


def load_dictionary(file:IO[str]) -> Mapping[str, str]:
    
    try:
        result = json.load(file)
    except ValueError:
        contents = file.read()
        if len(contents) > 0:  # File was not empty and still could not read
            print("Warning unable to parse file %s" % file)
        result = {}
    
    return result

class HeaderDictionary(object):
    '''
    Stores and retrieves header values.  Also contains mappings from headers to default values.
    '''

    header_dictionary = {}
    
    unit_dictionary = {}

    def __init__(self, headerDict:Mapping[str, str]=None, unitDict:Mapping[str, str]=None): 
        '''
        Create a new HeaderDictionary object.
        
        @param headerDict:  Header dictionary to use instead of the default
        @param unitDict: Unit dictionary to use instead of the default
        '''
        if headerDict:
            self.header_dictionary = headerDict
        else:
            with open(pkg_resources.resource_filename('climatechange', 'header_dict.json')) as f:  # @UndefinedVariable
                self.header_dictionary = load_dictionary(f)
            
        if unitDict:
            self.unit_dictionary = unitDict
        else:
            with open(pkg_resources.resource_filename('climatechange', 'unit_dict.json')) as f:  # @UndefinedVariable
                self.unit_dictionary = load_dictionary(f)
  

    def get_header_dict(self) -> Mapping[str, str]:
        '''
        @return: The known header mappings
        '''
        return self.header_dictionary
    
    def get_unit_dict(self) -> Mapping[str, str]:
        '''
        @return: The known unit mappings
        '''
        return self.unit_dictionary
    
    def parse_header(self, rawHeader:str) -> Tuple[str, str]:
        '''
        
        @param rawHeader: A header possibly with unit specified between parentheses
        @return: A 2-tuple containing the header and possibly the unit  
        '''
        
        # Match anything between 'header (unit)' and remove white space
        match = re.match(r"\s*(.*?)\s*\(\s*(.*?)\s*\)", rawHeader)
        
        if match:
            return match.group(1, 2)
        else:
            return (rawHeader, None)  
        
    def parse_headers(self, rawHeaders:List[str]) -> List[Tuple[str]]:
        '''
        
        @param rawHeaders: A list of header names with unit information
        @return: A list of parsed headers.  If the header is not known, then None is placed in its position
        '''
        return list(map(lambda e: e if e[0] in self.header_dictionary else None, map(self.parse_header, rawHeaders)))
        
    
    
