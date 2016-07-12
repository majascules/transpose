import argparse
import csv
import os
import pip
import sys
import time


def import_package(package):
    try:
        return __import__(package)
    except ImportError:
           pip.main(['install', package])
           print("Installing required package",package)
    return __import__(package)
       
       
def parseArguments():
    parser = argparse.ArgumentParser(prog='Multran', description='Multipurpose Transposer. Takes a spreadsheet with at least two columns, one with a key, one with multiple delimited values, and transposes that data into a user specified shape', epilog="Copyright 2016 Esmaeil Khaksari. This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.")
    parser.add_argument('--verbose','-v', action='store_true', required=False, help='Provides additional information during program execution.')
    parser.add_argument('--input','-i', action='store', required=True, help='The path and filename of the target file.')
    parser.add_argument('--output','-o', action='store', required=False, help='The path and filename of the desired output file. Defaults to output.txt if not specified.')
    # parser.add_argument('--mode','-m', action='store', required=False, help='Transposition type: otm: one-to-many, mto: many-to-one, nd: n-dimension. See readme for descriptions of each.')
    # parser.add_argument('--key-column','-k', action='store', help='The column that contains the key', required=False)
    # parser.add_argument('--transpose-column','-t', action='store', help='The number of the column to be transposed', required=False)
    # parser.add_argument('--delimiter','-d', action='store', help='Delimiter; if not supplied defaults to |',required=False)
    args = parser.parse_args()
    return args


def openInputFile(args):
    if args.input is not None:
        inputfile = open(os.path.join(__location__,args.input))
        print ("Opening:",inputfile.name) if args.verbose else None
    else:
        print("Null Input Filename")
        sys.exit()
    return inputfile
    
    
def openOutputFile(args):
    if args.output is not None:
        outputfile = open(os.path.join(__location__,args.output),'w')
    else:
        outputfile = open(os.path.join(__location__,'output.txt'),'w')    
    print("Opening:",outputfile.name) if args.verbose else None
    return outputfile


def readInputFile(inputfile):
    print ("Reading CSV data in:",inputfile.name) if args.verbose else None
    csv_f = csv.reader(inputfile)
    data=list(csv_f)
    return data
    

#Setup Timer & Counter Variables
end_time=0
start_time=time.time()
rows=0
values_transposed=0

#Parse Command Line Arguments
args = parseArguments()

#Get Script Path
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Check for tqdm dependency
if __name__ == '__main__':
    tqdm = import_package('tqdm')
    from tqdm import *


#Open & read input file
input_file=openInputFile(args)
data = readInputFile(input_file)
row_count = len(data)

#Open & instantiate csv-writer for output
output_file = openOutputFile(args)
wr = csv.writer(output_file, quoting=csv.QUOTE_ALL)

#Parse Input file and Get Name/Value Tuplets using wrapper to provide a status bar
print ("Parsing:") if args.verbose else None
for row in tqdm(data,total=row_count,disable=(not args.verbose)):

    #Decode URL, Parse URL for Path, and truncate to filename
    #Then Add filename to array filenames
    key = (row[0])
    value = (row[1])
    values = value.split(" | ")
    #values = np.array(value)
    for v in values:
        row=key+v
        wr.writerow([key,v])
        values_transposed +=1
    rows +=1

print (rows,"rows transposed to",values_transposed,"values in:",time.time()-start_time,"seconds") if args.verbose else None
print ("Done.") if args.verbose else None
input_file.close()
output_file.close()
