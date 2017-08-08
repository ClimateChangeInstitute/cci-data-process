'''
Created on Jul 12, 2017

@author: Mark Royer
'''
import os
import unittest

from climatechange.file import load_dictionary, load_csv, data_dir, save_dictionary
from climatechange.headers import HeaderEncoder, to_headers, HeaderType, Header
from climatechange.process_data_functions import process_header_data
from climatechange.read_me_output import create_readme_output_file


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
        frame = load_csv(os.path.join('csv_files', 'small.csv'))
        
        self.assertEqual('Dat210617', frame.columns[0], 'First column should be Dat210617')
        
        self.assertEqual(2009.8, frame.values[9][0], "Last value should be 2011.6986319241")
        
        
    def test_string_format(self):
        input_template="""\
        Date ran:{run_date}
        another variable:{var}
        """
        time_ran=[60,70]
        run_date='2017-08-03'
        var='variable'
        data = {'run_date': run_date,'var':var}
        output_template="""\
        Date ran:2017-08-03
        another variable:variable
        """
        result=input_template.format(**data)
        self.assertEqual(result,output_template)
         
                
    def testcreate_readme_output_file_tester(self):
        input_template=\
"""
Date ran:{run_date}
  
Process: Resample Input Data to {inc_amt} {label_name} Resolution
  
Input filename: {file_name}
Years: {years}
Depths: {depths}
Samples: {samples}
"""
        file=os.path.join('csv_files', 'small.csv')
        df = load_csv(file)
        f='small.csv'
        headers = process_header_data(df)
        run_date='2017-08-03'
        inc_amt=1
        label_name='year'
        stat_header='Mean'
        num_csvfiles=12
        year_headers = [h.name for h in headers if h.htype == HeaderType.YEARS]
        result=create_readme_output_file(input_template,f,headers,run_date,inc_amt,label_name,year_headers,num_csvfiles,stat_header)
        expected_result=\
"""
Date ran:2017-08-03
  
Process: Resample Input Data to 1 year Resolution
  
Input filename: small.csv
Years: ['Dat210617', 'Dat011216V2']
Depths: ['depth (m we) ', 'depth (m abs)']
Samples: ['Cond (+ALU-S/cm)', 'Na (ppb)', 'Ca (ppb)', 'Dust (part/ml)', 'NH4 (ppb)', 'NO3 (ppb)']
"""
        self.assertEqual(result,expected_result)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
