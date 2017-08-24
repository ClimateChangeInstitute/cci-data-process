'''
Created on Aug 24, 2017

:author: Mark Royer
'''
import unittest
from climatechange.process_data import setup_argument_parser
import sys
from _pytest.config import ArgumentError


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_setup_argument_parser(self):
        
        pvm = "program_version_message"
        parser = setup_argument_parser(pvm, "program_license")
        
#         sys.argv = sys.argv[0] + ['-c','/tmp','/tmp/depth_age_file.csv','True','True','KCC']
        
        # -c or --combine-laser
        args = parser.parse_args(['-c','/tmp','/tmp/depth_age_file.csv','True','True','KCC'])
        
        directory, depth_age_file, create_pdf, create_csv, folder_prefix, = args.combine_laser
        
        self.assertEqual('/tmp', directory)
        self.assertEqual('/tmp/depth_age_file.csv', depth_age_file)
        self.assertEqual('True', create_pdf)
        self.assertEqual('True', create_csv)
        self.assertEqual('KCC', folder_prefix)

        # -d or --depth
        args = parser.parse_args(['-d','/tmp/depth_file.csv'])
        
        depth_file = args.depth_file
        
        self.assertEqual('/tmp/depth_file.csv', depth_file)

        # -dd or --depth-depth
        args = parser.parse_args(['-dd','/tmp/depth_file1.csv','/tmp/depth_file2.csv'])
        
        depth_file1, depth_file2 = args.depth_files
        
        self.assertEqual('/tmp/depth_file1.csv', depth_file1)
        self.assertEqual('/tmp/depth_file2.csv', depth_file2)

        # -di or --double-interval
        args = parser.parse_args(['-di','/tmp/interval_file1.csv','/tmp/interval_file2.csv'])
        
        interval_file1, interval_file2 = args.interval_files
        
        self.assertEqual('/tmp/interval_file1.csv', interval_file1)
        self.assertEqual('/tmp/interval_file2.csv', interval_file2)

#         TODO: Make this match the setup argrument parser
#         # -f or --filter 
#         args = parser.parse_args(['replace_outliers'])
#         
#         directory, depth_age_file, create_pdf, create_csv, folder_prefix, = args.combine_laser
#         
#         self.assertEqual('/tmp', directory)
#         self.assertEqual('/tmp/depth_age_file.csv', depth_age_file)
#         self.assertEqual('True', create_pdf)
#         self.assertEqual('True', create_csv)
#         self.assertEqual('KCC', folder_prefix)

        # -i or --inc_amt
        args = parser.parse_args(['-i','1.1'])
        
        inc_amt = args.inc_amt
        
        self.assertEqual('1.1', inc_amt)
        
        # -l or --load
        args = parser.parse_args(['-l','/tmp/headers_file.csv'])
        
        headers_file = args.headers_file
        
        self.assertEqual('/tmp/headers_file.csv', headers_file)
        
        # -v or -vv indicates INFO and DEBUG verbosity
        args = parser.parse_args(['-v'])
        self.assertEqual(1, args.verbose)
        args = parser.parse_args(['-vv'])
        self.assertEqual(2, args.verbose)

        # -y or --year
        args = parser.parse_args(['-y','/tmp/year_file.csv'])
        
        year_file = args.year_file
        year_inc_amt = int(args.inc_amt) # should have a default value of 1
        self.assertEqual('/tmp/year_file.csv', year_file)
        self.assertEqual(1, year_inc_amt)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()