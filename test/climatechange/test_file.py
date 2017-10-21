'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import unittest

from climatechange.file import load_dictionary, data_dir, save_dictionary
from climatechange.headers import HeaderEncoder, to_headers, HeaderType, Header,process_header_data

from climatechange.common_functions import load_csv, DataClass, FrameClass
from climatechange.resample_read_me import readme_output_file, readme_laser_file


class Test(unittest.TestCase):

    def setUp(self):
        self.a = Header("a",HeaderType.YEARS, "aclass", "aunit", "alabel")
        self.b = Header("b",HeaderType.YEARS, "aclass", "aunit", "alabel")
        self.c = Header("c",HeaderType.DEPTH, "cclass", "cunit", "clabel")
        self.d = Header("d",HeaderType.SAMPLE, "dclass", "dunit", "dlabel")
        self.e = Header("e",HeaderType.SAMPLE, "eclass", "eunit", "elabel")
        self.abc_dict = {"a": self.a,
                         "b": self.b,
                         "c": self.c,
                         "d": self.d,
                         "e": self.e}
        pass


    def tearDown(self):
        pass

    def testLoadDictionary(self):
        
        file_name = os.path.join('json_files', 'nothing.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual({},
                                 load_dictionary(f, obj_hook=to_headers),
                                 "Empty dictionary was expected")
         
        file_name = os.path.join('json_files', 'empty.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual({},
                                 load_dictionary(f, obj_hook=to_headers),
                                 "Empty dictionary was expected")
        
        file_name = os.path.join('json_files', 'abc_dict.json')
        with open(file_name, 'r') as f:
            self.assertDictEqual(self.abc_dict,
                                 load_dictionary(f, obj_hook=to_headers),
                                 "%s dictionary does not match" % f)

    def testSaveDictionary(self):
        
        file_name = 'cci_test_file_delete_me.json'
        file_path = os.path.join(data_dir(), file_name)
        
        save_dictionary({}, file_path)
        with open(file_path, 'r') as f:
            self.assertDictEqual({}, load_dictionary(f))
        os.remove(file_path)
        
        save_dictionary(self.abc_dict, file_path, enc_cls=HeaderEncoder)
        with open(file_path, 'r') as f:
            self.assertDictEqual(self.abc_dict, load_dictionary(f, obj_hook=to_headers))
        os.remove(file_path)
        
        save_dictionary(self.abc_dict, file_path, enc_cls=HeaderEncoder)
        with open(file_path, 'r') as f:
            self.assertDictEqual(self.abc_dict, load_dictionary(f, obj_hook=to_headers))
        os.remove(file_path)

    def testReadCSVFile(self):
        frame = load_csv(os.path.join('csv_files','input', 'small.csv'))
        
        self.assertEqual('Dat210617', frame.columns[0], 'First column should be Dat210617')
        
        self.assertEqual(2009.8, frame.values[9][0], "Last value should be 2011.6986319241")
        
        
    def test_string_format(self):
        input_template="""\
        Date ran:{run_date}
        another variable:{var}
        """
        run_date='2017-08-03'
        var='variable'
        data = {'run_date': run_date,'var':var}
        output_template="""\
        Date ran:2017-08-03
        another variable:variable
        """
        result=input_template.format(**data)
        self.assertEqual(result,output_template)
         
                
                
                
    def test_readme_output_file_tester(self):
        input_template=\
"""
Date ran:{run_date}
   
Process: Resample Input Data to {inc_amt} {label_name} Resolution
   
Input filename: {file_name}
Years: {years}
Depths: {depths}
Samples: {samples}
"""
        f=os.path.join('csv_files','input', 'small.csv')
        run_date='2017-08-03'
        inc_amt=1
        file=['files']
        label_name='year'
        stat_header=['mean']

        result=readme_output_file(input_template,DataClass(f),run_date, inc_amt, label_name, stat_header,file)
        expected_result=\
"""
Date ran:2017-08-03
   
Process: Resample Input Data to 1 year Resolution
   
Input filename: small.csv
Years: Dat210617, Dat011216V2
Depths: depth (m we) , depth (m abs)
Samples: Cond (+ALU-S/cm), Na (ppb), Ca (ppb), Dust (part/ml), NH4 (ppb), NO3 (ppb)
"""
        self.assertEqual(result,expected_result)
        
        
    def test_readme_output_laser_file(self):
        input_laser_template=\
"""
ReadMeFile

CCI-Data-Processor
Authors: Mark Royer and Heather Clifford
Date ran: {run_date}

Process: Process and Compile {type} LA-ICP-MS Data

Directory Folder: {directory}

Prefix of Cores: {prefix}

Cores in Directory = {folders}

Depth Age File = {depth_age_file}

***  Additional Information about Individual Cores & Runs found in file:
         {info_file}

Directory Information:

    Year: {years}
    Year Range: {year_max} - {year_min}

    Depth: {depths}
    Depth Range: {depth_min} - {depth_max}
    
    Resolution: {resolution}
    
    Samples: {samples}


Output Files:

{csv_filename}

"""
        directory=os.path.join('csv_files','test_directory')
        dc = FrameClass(load_csv(os.path.join(directory,'csv_files','LA-ICP-MS_raw_LR.csv')))
        dc.df =dc.df.set_index(['depth (m abs)'])
        resolution = 'Medium'
        prefix='KCC'
        depth_age_file = 'depth_age_file.csv'
        info_file ='info_file.csv'
        run_date='2017-08-03'
        file ='LA-ICP-MS_raw_LR.csv'
        output_type = 'Raw'
        

        result=readme_laser_file(input_laser_template,directory,prefix,depth_age_file, dc, resolution, run_date,info_file, file,output_type)
        
        expected_result=\
"""
ReadMeFile

CCI-Data-Processor
Authors: Mark Royer and Heather Clifford
Date ran: 2017-08-03

Process: Process and Compile Raw LA-ICP-MS Data

Directory Folder: test_directory

Prefix of Cores: KCC

Cores in Directory = KCC1, KCC2

Depth Age File = depth_age_file.csv

***  Additional Information about Individual Cores & Runs found in file:
         info_file.csv

Directory Information:

    Year: year
    Year Range: 676 - 654

    Depth: depth (m abs)
    Depth Range: 60.085 - 60.255
    
    Resolution: Medium
    
    Samples: Na23, Mg25, Cu63, Pb208, Sn118


Output Files:

LA-ICP-MS_raw_LR.csv

"""

        self.assertEqual(result,expected_result)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
