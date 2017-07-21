'''
Created on Jul 12, 2017

:author: Mark Royer
'''
from enum import Enum
from functools import singledispatch
import re
from typing import Mapping, Tuple, List

from climatechange.file import load_dict_by_package, data_dir, load_dictionary,\
    save_dictionary
import os


@singledispatch
def serialize(val):
    """Default serialize"""
    return str(val)

class HeaderType(Enum):
    '''
    Used to represent the type of information contained in the column of data. 
    For example, 'Dat210617' is of type YEARS, 'depth' is of type DEPTH, and 
    'Na (ppb)' is of type SAMPLE
     
    '''
    YEARS = 'Years'
    DEPTH = 'Depth'
    SAMPLE = 'Sample'
    UNKNOWN = 'Unknown'
    
class Header(object):
    
    htype: HeaderType = HeaderType.UNKNOWN
    
    original_value: str
    
    parsed_value: Tuple[str, str]
        
    def __init__(self,
                 original_value:str,
                 htype:HeaderType,
                 parsed_value:Tuple[str, str]=None,
                 regexp:str=r"\s*(.*?)\s*\(\s*(.*?)\s*\)"):
        self.original_value = original_value
        self.parsed_value = parsed_value 
        if not parsed_value:
            self.parsed_value = self.parse_header(original_value, regexp)
        self.htype = htype
    
    @staticmethod
    def parse_header(rawHeader:str, regexp:str=r"\s*(.*?)\s*\(\s*(.*?)\s*\)") -> 'Header':
        '''
        Parses a header string into a 2-tuple of the header name and unit.
        
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
        
    def __repr__(self, *args, **kwargs):
        '''
        :return: A json-like object.  For example, 
        
        .. code-block:: python
        
            {"original_value": "test", "parsed_value": ["test", null], "htype": "Sample"}
        '''
        return '{"original_value": "%s", "parsed_value": "%s", "htype": "%s"}' % (self.original_value, self.parsed_value, self.htype)
       

class HeaderDictionary(object):
    '''
    Stores and retrieves header values.  Also contains mappings from headers 
    to default values.
    '''

    header_dictionary = {}
    
    unit_dictionary = {}

    def __init__(self, headerDict:Mapping[str, HeaderType]=None, unitDict:Mapping[str, str]=None): 
        '''
        Create a new HeaderDictionary object.
        
        :param headerDict:  Header dictionary to use instead of the default
        :param unitDict: Unit dictionary to use instead of the default
        '''
        if headerDict:
            self.header_dictionary = headerDict
        else:
            self.header_dictionary = self.load_latest_header_dict()
            
                        
        if unitDict:
            self.unit_dictionary = unitDict
        else:
            self.unit_dictionary = load_dict_by_package('unit_dict.json')
  
    def load_latest_header_dict(self) -> Mapping[str, HeaderType]:
        header_file_name = 'header_dict.json'
        header_file_path = os.path.join(data_dir(), header_file_name)
        
        hdict = {}
        if os.path.isfile(header_file_path):
            with open(header_file_path, 'r') as f:
                hdict = load_dictionary(f) 
        else: # Load default header file from package
            hdict = load_dict_by_package(header_file_name)
            # Copy default header file to user data directory
            save_dictionary(hdict, header_file_path)
            
        # Make sure mappings are to header types
        for h, v in hdict.items():
            hdict[h] = HeaderType(v)
            
        return hdict
        

    def get_header_dict(self) -> Mapping[str, HeaderType]:
        '''
        Returns the *already* loaded header dictionary.
        :return: The known header mappings
        '''
        return self.header_dictionary
            
    
    def get_unit_dict(self) -> Mapping[str, str]:
        '''
        Returns the *already* loaded unit dictionary.
        :return: The known unit mappings
        '''
        return self.unit_dictionary
    
        
    def parse_headers(self, rawHeaders:List[str]) -> List[Tuple[str]]:
        '''
        Convert a list of raw header names into a list containing header 
        objects.  For example, the headers
        
        .. code-block:: python
        
            ['Years (BP)', 'Na (ppb)', 'Not Known (hmm)']
        
        would become
        
        .. code-block:: python
        
            [{"original_value": "Years (BP)", 
              "parsed_value": "('Years', 'BP')", 
              "htype": "HeaderType.UNKNOWN"
             }, 
             {"original_value": "Na (ppb)", 
              "parsed_value": "('Na', 'ppb')", 
              "htype": "HeaderType.SAMPLE"
             }, 
             {"original_value": "Not Known (hmm)",
              "parsed_value": "('Not Known', 'hmm')", 
              "htype": "HeaderType.UNKNOWN"
             }
            ]
        
        :param rawHeaders: A list of header names with unit information 
        :return: A list of parsed headers.  If the header is not known, its 
            value is :py:attr:`HeaderType.UNKNOWN`.
        '''
        return [ Header(e, self.header_dictionary.get(e, HeaderType.UNKNOWN)) for e in rawHeaders ]
