'''
Created on Jul 12, 2017

:author: Mark Royer
'''
from enum import Enum
import json
import logging
import os
import re
import textwrap
from typing import Mapping, List, Any, Sequence, IO

import pandas

from climatechange.file import load_dict_by_package, data_dir, load_dictionary, \
    save_dictionary
from pandas import DataFrame


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
    
class HeaderEncoder(json.JSONEncoder):
    '''
    Used to dump Header information
    '''
    def default(self, obj:Any):
        '''
        Write out  types as simply the string representation.  **Note** this 
        does not write out any object other than :class:`Header` types.
         
        :param obj: Object to be save
        '''
        if type(obj) == Header:
            return eval(str(obj))
        else:
            raise NotImplementedError

class Header(object):
    '''
    A header parsed by the system.  This object contains the raw header, the 
    type of header, the class of the unit (which is basically a subcategory), 
    the unit, and a label used for plotting.
    
    :ivar str: The raw header value, for example, "Dat210617"
    :ivar htype: The type of the column data as determined from the 
        header_dict.json file
    :ivar hclass: The class/subcategory of the header, for example, "Years"
    :ivar unit: The unit of the, for example, "CE"
    :ivar label: The label used for plotting the data, for example, 
        "Year_Dat210617_CE" 
    '''
    
    name: str
    
    htype: HeaderType = HeaderType.UNKNOWN
    
    hclass: str
    
    unit: str
    
    label: str
    
    def __init__(self,
                 name:str,
                 htype:HeaderType,
                 hclass:str,
                 unit:str,
                 label:str) -> None:
        self.name = name
        self.htype = htype 
        self.hclass = hclass
        self.unit = unit
        self.label = label
        
    
    @staticmethod
    def parse_header(rawHeader:str, regexp:str=r"\s*(.*?)\s*\(\s*(.*?)\s*\)") -> Sequence[str]:
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
        
    def __repr__(self):
        '''
        Return a JSON-like object. For example, 
        
        .. code-block:: python
        
            '{"name": "%s", "type": "%s",' "class": "%s", "unit": "%s", "label": "%s"}'
            
        :return: A JSON-like object
        '''
        return ('{"name": "%s", "type": "%s",'
                ' "class": "%s", "unit": "%s", "label": "%s"}') \
                % (self.name, self.htype.value, self.hclass, self.unit, self.label)    
     
    def __eq__(self, other):
        '''
        Overriding this method allows us to easily compare Header objects.
        
        :param other: Header object to compare to
        :return: True IFF the two objects have equal values
        '''
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

def to_headers(d:Mapping[str, str]) -> Header:
    '''
    Use this function to specify how a header should be loaded.
    
    :param d: A dictionary of header information
    :return: A fully instantiated header object
    '''
    return Header(d['name'], HeaderType(d['type']), d['class'], d['unit'], d['label'])
          

class HeaderDictionary(object):
    '''
    Stores and retrieves header values.  Also contains mappings from headers 
    to default values.
    '''
    
    header_file_name = 'header_dict.json'
    header_file_path = os.path.join(data_dir(), header_file_name)

    header_dictionary:Mapping[str, Header] = {}

    def __init__(self, headerDict:Mapping[str, Header]=None) -> None: 
        '''
        Create a new HeaderDictionary object.
        
        :param headerDict:  Header dictionary to use instead of the default
        '''
        if headerDict:
            self.header_dictionary = headerDict
        else:
            self.header_dictionary = self.load_latest_header_dict()
            
  
    def load_latest_header_dict(self) -> Mapping[str, Header]:
        
        hdict:Mapping[str, Header] = {}
        if os.path.isfile(self.header_file_path):
            with open(self.header_file_path, 'r') as f:
                hdict = load_dictionary(f, obj_hook=to_headers) 
        else:  # Load default header file from package
            hdict = load_dict_by_package(self.header_file_name, obj_hook=to_headers)
            # Copy default header file to user data directory
            save_dictionary(hdict, self.header_file_path, enc_cls=HeaderEncoder)
            
        return hdict
        

    def get_header_dict(self) -> Mapping[str, Header]:
        '''
        Returns the **already** loaded header dictionary.
        
        :return: The known header mappings
        '''
        return self.header_dictionary
            
    
    def get_unit_dict(self) -> Mapping[str, str]:
        '''
        Returns the **already** loaded unit dictionary.
        
        :return: The known unit mappings
        '''
        return self.unit_dictionary
    
        
    def parse_headers(self, rawHeaders:List[str]) -> List[Header]:
        '''
        Convert a list of raw header names into a list containing header 
        objects.  For example, the headers
        
        .. code-block:: python
        
            ['Years (BP)', 'Na (ppb)', 'Not Known (hmm)']
        
        would become
        
        .. code-block:: python
        
            [{"name": "Years (BP)",  
              "htype": "HeaderType.UNKNOWN",
              "hclass": "Years",
              "unit": "BP",
              "label": "Years_(BP)"
             }, 
             {"name": "Na (ppb)", 
              "htype": "HeaderType.SAMPLE"
              "hclass": "Sample,
              "unit": "ppb",
              "label": "Na_(ppb)"
             }, 
             {"name": "Not Known (hmm)",
              "htype": "HeaderType.UNKNOWN"
              "hclass": None,
              "unit": None,
              "label": None
             }
            ]
            
        The result is generated by performing lookups on the dictionary of 
        headers. 
        
        :param rawHeaders: A list of header names with unit information 
        :return: A list of parsed headers.  If the header is not known, its 
            value is :py:attr:`HeaderType.UNKNOWN`.
        '''
        
        result = []
        for s in rawHeaders:
            h = self.header_dictionary.get(s)
            if not h:
                h = Header(s, HeaderType.UNKNOWN, None, None, None)
            result.append(h)
        return result

    def add_header(self, h:Header) -> Header:
        '''
        Adds the given header to the dictionary. This is only the in memory 
        dictionary, if you want the dictionary persisted, you must save the 
        dictionary to disk. Throws a ValueError if the given header is an 
        Unknown type.
        
        :param h: The new header to add
        :return: None or the previous value if a header with the same name 
            already existed
        '''
        if h.htype is HeaderType.UNKNOWN:
            raise ValueError("Unwilling to add unknown header type")
            
        previous = self.header_dictionary.get(h.name)
        self.header_dictionary[h.name] = h
        return previous

       
    def save_dictionary(self, file_path:str=None):
        '''
        Persist the current dictionary.  If no file path is specified, then the 
        default dictionary location is used.
        
        :param file_path: The path to the dictionary
        '''
        if file_path is None:
            file_path = self.header_file_path
        save_dictionary(self.get_header_dict(), file_path, enc_cls=HeaderEncoder)


def load_headers(file_name:IO[str]) -> List[Header]:
    '''
    Loads headers into a list from a CSV file.  Each row should contain name,
    type, class, unit, and label data.
    
    :param file_name: The name of a CSV file containing header information
    :return: A list containing the headers
    '''
    df = pandas.read_csv(file_name, sep=',')
    
    result = []
    for r in df.values:
        result.append(Header(r[0], HeaderType(r[1]), r[2], r[3], r[4]))
    
    return result

default_dictionary = HeaderDictionary()

def process_header_data(df:DataFrame,
                        header_type:HeaderType=None,
                        header_dict:HeaderDictionary=default_dictionary) -> List[Header]:
    '''
    Use the default dictionary to process the data column headers.  If a 
    :class:`HeaderType` is specified, only the matching types are returned 
    in the result.  See :class:`Header` for additional information.
    
    :param df: Data containing column headers to process
    :param header_type: The type of headers to return 
    :param header_dict: Optional header dictionary to use instead of the default
    :return: The processed column headers
    '''
    
    parsedHeaders = header_dict.parse_headers(df.columns.tolist())
    
    unknown_headers = [h for h in parsedHeaders if h.htype == HeaderType.UNKNOWN ]
    if unknown_headers:
        logging.error("The following unknown headers were found.")
        for h in unknown_headers:
            logging.error(h.name)
        logging.error(textwrap.dedent("""
        Please import the headers by using a CSV file containing rows of the 
        following format:
        
        name1, type1, class1, unit1, label1
        name2, type2, class2, unit2, label2
        name3, type3, class3, unit3, label3
        ...
        
        Run the program again using the -l flag to import the header information.
        For example,
        
        PYTHONPATH=src python climatechange/process_data.py -l your_csv_file.csv
        """))
            
    if header_type:
        return [h for h in parsedHeaders if h.htype is header_type]
    else:
        return parsedHeaders
