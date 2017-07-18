'''
Created on Jul 18, 2017

@author: Mark Royer
'''
from bottle import route, hook, static_file, run
import os
import tempfile

from climatechange.plot import examplePDFPlot


@route('/download/<filename:path>')
def download_file(filename):
    
    file = tempfile.NamedTemporaryFile('wb', prefix='cci_temp_')    

    examplePDFPlot(file.name)
    
    file.flush()
          
    return static_file(file.name, root='/', download=filename)

if __name__ == '__main__':
    run(host='localhost', port=8080)