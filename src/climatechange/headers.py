'''
Created on Jul 12, 2017

:author: Mark Royer
'''
import re
from typing import Mapping, Tuple, List

from climatechange.file import load_dict_by_package


class HeaderDictionary(object):
    '''
    Stores and retrieves header values.  Also contains mappings from headers to default values.
    '''

    header_dictionary = {}
    
    unit_dictionary = {}

    def __init__(self, headerDict:Mapping[str, str]=None, unitDict:Mapping[str, str]=None): 
        '''
        Create a new HeaderDictionary object.
        
        :param headerDict:  Header dictionary to use instead of the default
        :param unitDict: Unit dictionary to use instead of the default
        '''
        if headerDict:
            self.header_dictionary = headerDict
        else:
            self.header_dictionary = load_dict_by_package('header_dict.json')
            
        if unitDict:
            self.unit_dictionary = unitDict
        else:
            self.unit_dictionary = load_dict_by_package('unit_dict.json')
  

    def get_header_dict(self) -> Mapping[str, str]:
        '''
        :return: The known header mappings
        '''
        return self.header_dictionary
    
    def get_unit_dict(self) -> Mapping[str, str]:
        '''
        :return: The known unit mappings
        '''
        return self.unit_dictionary
    
    def parse_header(self, rawHeader:str, regexp:str=r"\s*(.*?)\s*\(\s*(.*?)\s*\)") -> Tuple[str, str]:
        '''
        
        :param rawHeader: A header possibly with unit specified between 
            parentheses
        :param regexp: If supplied, a regular expression for parsing the raw 
            header.  The regular expression should contain two capture groups.
        :return: A 2-tuple containing the header and possibly the unit
        '''
        # Match anything between 'header (unit)' and remove white space
        match = re.match(regexp, rawHeader)
        
        if match:
            return match.group(1, 2)
        else:
            return (rawHeader, None)  
        
    def parse_headers(self, rawHeaders:List[str]) -> List[Tuple[str]]:
        '''
        
        :param rawHeaders: A list of header names with unit information
        :return: A list of parsed headers.  If the header is not known, then 
            None is placed in its position
        '''
        
        # Parse headers into name and unit
        result = map(self.parse_header, rawHeaders)
        # Replace unmapped headers with None
        result = map(lambda e: e if e[0] in self.header_dictionary else None, result)
        # Replace unknown units with None
        result = map(lambda e: (e[0], self.unit_dictionary.get(e[1])) if e else None, result)
        
        # Make sure the result is a list 
        return list(result)
        
    
    
