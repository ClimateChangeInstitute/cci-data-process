#!/usr/local/bin/python3.6
# encoding: utf-8
'''
The Climate Change Institute Data Processor

The Climate Change Data Processor is a tool for cleaning, resampling, and
packaging data gathered by CCI scientists.

A number of statistical routines are applied to the loaded data.  The results 
are written to CSV files along with PDFs containing plotted data.  

:author: Mark Royer
:author: Heather Clifford


:contact: andrei.kurbotov@maine.edu
'''
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os
import sys

from climatechange.process_data_functions import resample_by_years, \
    resample_by_depths, load_and_store_header_file, double_resample_by_depths,\
    double_resample_by_depth_intervals
import logging
import textwrap


__all__ = []
__version__ = 0.1
__date__ = '2017-07-24'
__updated__ = '2017-07-24'

PROFILE = 1

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Heather Clifford, Andrei Kurbatov, and Mark Royer on %s.
  Copyright 2017 Climate Change Institute. All rights reserved.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        
        
        parser.add_argument("-y",
                            "--year",
                            dest="year_file",
                            action="store",
                            help="resample %(dest)s by years and depth [default: %(default)s]")

        parser.add_argument("-d",
                            "--depth",
                            dest="depth_file",
                            action="store",
                            help="resample %(dest)s by depth [default: %(default)s]")
        
        parser.add_argument("-dd",
                            "--double-depth",
                            dest="depth_files",
                            action="store",
                            nargs=2,
                            help="resample %(dest) by depth")
        
        parser.add_argument("-di",
                            "--double-interval",
                            dest="interval_files",
                            action="store",
                            nargs=2,
                            help="resample %(dest) to the higher resolution of the two files")
        
        parser.add_argument("-i",
                            "--inc_amt",
                            dest="inc_amt",
                            action="store",
                            default=1,
                            help="the size of the resampling increment [default: %(default)s]")
        
        parser.add_argument("-l",
                            "--load",
                            dest="headers_file",
                            action="store",
                            help="load the headers of the CSV and store them in the header dictionary.  "
                                 "This file should contain rows of (name, type, class, unit, label)")
        
        parser.add_argument("-r",
                            "--recursive",
                            dest="recurse",
                            action="store_true",
                            help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v",
                            "--verbose",
                            dest="verbose",
                            action="count",
                            help=textwrap.dedent("""set verbosity level [default: %(default)s]\n
                            Increasing the verbosity level increases what is logged.  For example,\n
                            specifying -v outputs INFO level and -vv outputs DEBUG level messages."""))
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

#         parser.add_argument(dest="paths", default=".", help="paths to folder(s) with data file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

#         paths = args.paths
        verbose = args.verbose
        
        inc_amt = float(args.inc_amt)
        
        if verbose and verbose > 0:
            logger = logging.getLogger()
            level = 'WARN'
            if verbose == 1:
                level = 'INFO'
            elif verbose == 2:
                level = 'DEBUG'
            else:
                logging.error('Unknown verbosity level %d. Exiting', verbose)
                sys.exit(-1)
            logger.setLevel(level)
            
            logging.info("Using verbosity of %s for logging.", level)
        
        if args.headers_file:
            load_and_store_header_file(args.headers_file)
            return
        
        if args.depth_files: 
            double_resample_by_depths(args.depth_files[0],
                                      args.depth_files[1],
                                      inc_amt)
            
        if args.interval_files:
            if args.inc_amt:
                logging.warn("Specified increment amount %d is not used "
                             "when resampling by depth intervals.", inc_amt)
            double_resample_by_depth_intervals(args.interval_files[0],
                                      args.interval_files[1])    
        
        if args.year_file:
            
            year_file = args.year_file
            
            if year_file.endswith('.csv'):            
                resample_by_years(year_file, int(inc_amt))
            else:
                print("The specified year_file must be a CSV file.", file=sys.stderr)
                sys.exit(-1)
        
        if args.depth_file:
            
            depth_file = args.depth_file
            
            if depth_file.endswith('.csv'):
                resample_by_depths(depth_file, inc_amt)
            else:
                print("The specified depth_file must be a CSV file.", file=sys.stderr)
                sys.exit(-1)
                

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if logging.getLogger().getlevel() == 'DEBUG':
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
    
