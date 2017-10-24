#!/usr/local/bin/python
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
from argparse import ArgumentParser, RawTextHelpFormatter
from argparse import RawDescriptionHelpFormatter
import os
import sys


import logging
import textwrap

from climatechange.plot import plot_samples_by_depth, plot_samples_by_year
from climatechange.laser import raw_data
from climatechange.resample import resample, resample_by
from climatechange.headers import load_and_store_header_file
from laser import resample_data



__all__ = []
__version__ = 0.1
__date__ = '2017-07-24'
__updated__ = '2017-08-25'


def setup_argument_parser(program_version_message, program_license):
    '''
    Create and set up an argument parser.  Make sure that any arguments added to 
    the parser are added to the test framework.
    
    :param program_version_message: Program version
    :param program_license: The program license
    :return: Fully setup argument parser
    '''
    parser = ArgumentParser(description=program_license,
                            formatter_class=RawTextHelpFormatter)#RawDescriptionHelpFormatter)
    
    # Order lexicographically using the short option for sanity!

    parser.add_argument("-d",
                        "--depth",
                        dest="depth_file",
                        action="store",
                        nargs=2,
                        metavar=('CSV_FILE', 'STATISTIC'),
                        help="resample %(dest)s by depth [default: %(default)s]")
    
#     parser.add_argument("-dd",
#                         "--double-depth",
#                         dest="depth_files",
#                         action="store",
#                         nargs=2,
#                         help="resample %(dest)s by depth")
    
    parser.add_argument("-by",
                        "--resample_by",
                        dest="interval_files",
                        action="store",
                        nargs=3,
                        metavar=('to_resample_file', 'resample_by_file','statistics'),
                        help="resample %(dest)s to the lower resolution of the two files")

#     parser.add_argument("-f",
#                         "--filter",
#                         dest="filters",
#                         action="append",
#                         nargs='+',
#                         help="Apply filters to processed data.  "
#                         "Multiple filters with optional parameters may be specified.  "
#                         "The following filter functions are available:\n" + filter_function.help())
#         
    parser.add_argument("-i",
                        "--inc_amt",
                        dest="inc_amt",
                        action="store",
                        default=1,
                        help="the size of the resampling increment [default: %(default)s]")
    
    parser.add_argument("-int",
                        "--interval",
                        dest="interval",
                        action="store",
                        nargs=2,
                        metavar=('top_interval','bottom_interval'),
                        help="the interval to be plotted [default: %(default)s]")
    
    parser.add_argument("-hf",
                        "--header",
                        dest="headers_file",
                        action="store",
                        help="load the headers of the CSV and store them in the header dictionary.  "
                             "This file should contain rows of (name, type, class, unit, label)")
    
    
    parser.add_argument("-pd",
                        "--plot_depth",
                        dest="plot_depth_files",
                        action="store",
                        help="%(dest)s by depth [default: %(default)s]")
    
    parser.add_argument("-py",
                        "--plot_year",
                        dest="plot_year_files",
                        action="store",
                        help="%(dest)s by year [default: %(default)s]")\
                        
    parser.add_argument("-l",
                        "--raw_laser_data",
                        dest="raw_laser_data",
                        action="store",
                        nargs=3,
                        metavar=('DIRECTORY', 'DEPTH_AGE_FILE', 'FOLDER_PREFIX'),
                        help="compiles %(dest) [default: %(default)s]")
    
    parser.add_argument("-rl",
                        "--resample_laser",
                        dest="resample_laser_data",
                        action="store",
                        nargs=4,
                        metavar=('DIRECTORY', 'DEPTH_AGE_FILE', 'FOLDER_PREFIX','RESAMPLE_BY'),
                        help="compiles %(dest) [default: %(default)s]")

#     parser.add_argument("-f",
#                         "--filter_LAICPMS_directory",
#                         dest="filter_directory",
#                         action="store",
#                         nargs=4,
#                         metavar=('DIRECTORY', 'DEPTH_AGE_FILE','CORR_FILE', 'FOLDER_PREFIX'),
#                         help="compiles %(dest) [default: %(default)s]")
    
    

    parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                        help=textwrap.dedent(
                 """set verbosity level [default: %(default)s]\n
                    Increasing the verbosity level increases what is logged.  For example,\n
                    specifying -v outputs INFO level and -vv outputs DEBUG level messages."""))
    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version=program_version_message)
    parser.add_argument("-y",
                        "--year",
                        dest="year_file",
                        action="store",
                        nargs=2,
                        metavar=('CSV_FILE', 'STATISTIC'),
                        help="resample %(dest)s by years and depth [default: %(default)s]")
    return parser

def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv

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
        parser = setup_argument_parser(program_version_message, program_license)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

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

        
        inc_amt = float(args.inc_amt)
        stats = ['mean','std', 'min', 'max', '25%', '50%', '75%', 'all']
        
        
        if args.interval:
            interval = [float(args.interval[0]),float(args.interval[1])]
        
        # No program arguments provided. Abort!
        if len(argv) <= 1 and argv == sys.argv:
            parser.print_help()
            sys.exit(0)

        # We can load new headers from a file and then continue
        if args.headers_file:
            load_and_store_header_file(args.headers_file)
        
        
        ######################################################################
        ################ Data Processing Flags Below Here ####################
        ####### Generally the order these are processed shouldn't matter #####
        ######################################################################
        

#         if args.depth_files: 
#             double_resample_by_depths(args.depth_files[0],
#                                       args.depth_files[1],
#                                       inc_amt)
        if args.plot_depth_files:
            file = args.plot_depth_files

            if args.interval:
                plot_samples_by_depth(file,interval)
            else:
                plot_samples_by_depth(file)
                
        
        if args.plot_year_files:
            file = args.plot_year_files

            if args.interval:
                plot_samples_by_year(file,interval)
            else:
                plot_samples_by_year(file)
                
        if args.raw_laser_data:
            directory, depth_age_file, prefix = args.raw_laser_data
            raw_data(directory, depth_age_file, prefix)
        
        if args.resample_laser_data:
            directory, depth_age_file, prefix,by = args.resample_laser_data
            resample_data(directory, by,depth_age_file, prefix)
            
#             
        if args.interval_files:
            if args.inc_amt:
                logging.warning("Specified increment amount %d is not used "
                             "when resampling by depth intervals.", inc_amt)
            
            resample_file,by_file,stat = args.interval_files
            stat =str(stat).split(',')
            for i in stat: 
                if not i in stats:
                    logging.error('Statistic specified is not option, options include {}'.format(', '.join(stats)))
                    sys.exit()
            if len(stat)==1:
                stat=stat[0]
                if stat == 'all':
                    stat=None
            
            
            resample_by(resample_file,by_file,stat) 
            
             
        
        if args.year_file:
            
            year_file,stat = args.year_file
            stat =str(stat).split(',')
            for i in stat: 
                if not i in stats:
                    logging.error('Statistic specified is not option, options include {}'.format(', '.join(stats)))
                    sys.exit()
            if len(stat)==1:
                stat=stat[0]
                if stat == 'all':
                    stat=None        
            
            if year_file.endswith('.csv'): 
          
                resample('year',year_file,stat, int(inc_amt))
            else:
                raise Exception("The specified year_file must be a CSV file.")
        
        if args.depth_file:
            
            depth_file,stat = args.depth_file
            stat =str(stat).split(',')
            for i in stat: 
                if not i in stats:
                    logging.error('Statistic specified is not option, options include {}'.format(', '.join(stats)))
                    sys.exit()
            if len(stat)==1:
                stat=stat[0]
                if stat == 'all':
                    stat=None
            
            if depth_file.endswith('.csv'):
                resample('depth',depth_file, stat,inc_amt)
            else:
                raise Exception("The specified depth_file must be a CSV file.")
                
    except Exception as e:
        if logging.getLevelName(logging.getLogger().level) == 'DEBUG':
            raise
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2




if __name__ == "__main__":
    #!/usr/bin/python

    sys.exit(main())
    
