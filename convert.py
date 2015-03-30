'''
Created on Mar 20, 2015

@author: yury
'''
import os, sys, time
from optparse import OptionParser
from converters import Converter_7z2zip

script_usage = "Usage: %prog [-jN] <input_filepath> <output_filepath>"
#option_0 = {'name': ('-o', '--outfile'), 'dest': 'outfile', 'help': 'resulted file name', 'type': 'string', 'nargs' : 1}
option_1 = {'name' : ('-j', '--threads'), 'dest': 'threads', 'help' : 'number of threads', 'type': 'int', 'default' : 1, 'nargs' : 1}
options = [option_1]





def main(options, arguments):
    input_file = arguments[0]
    output_file = arguments[1]
    
    converter = Converter_7z2zip(input_file, output_file, options.threads)
    
    start_time = time.time()
    try:
        converter.convert()
    finally:
        elapsed = time.time() - start_time
        print "\n\n It took %d seconds to convert" % (elapsed)
    
    


if __name__ == '__main__':
    parser = OptionParser(usage=script_usage)
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)
    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    
    
    if (len(arguments) < 2):
        parser.error("Not enough arguments provided!")
    
    if not (arguments[0] and os.path.isfile(arguments[0])):
        parser.error("Provided path does not point to a valid file!")
    
    if arguments[1] == None:
        parser.error("Output filepath is not specified!")
    
    if os.path.exists(arguments[1]):
        while True:
            user_input = raw_input('The output file already exists. Overwrite (y/n)?: ')
            if user_input.capitalize() == 'YES' or user_input.capitalize() == 'Y':
                break
            elif user_input.capitalize() == 'NO' or user_input.capitalize() == 'N':
                print "Please provide another output path. Exiting!!!"
                exit(1)
    
    
    main(options, arguments)