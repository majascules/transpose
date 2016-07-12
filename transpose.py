import csv
import os
import sys
import time
from tqdm import *

#Setup Timer Variables
start_time=time.time()
end_time=0

#Setup Counter Variables
rows=0
values_transposed=0

#Print Start Message to STDOUT
print ("Processing file",sys.argv[1])

#Parse 1st STDIN Argument as Input Filename
f = open(sys.argv[1])

#Parse 2nd STDIN Arguemnt as Output Filename
output = open(sys.argv[2],'w')

#Instantiate CSV Reader and the read in data
csv_f = csv.reader(f)
data=list(csv_f)

#Instantiate CSV Writer
wr=csv.writer(output, quoting=csv.QUOTE_ALL)

#Count Rows in Input File
row_count = len(data)

#Parse Input file and Get Name/Value Tuplets
#using tqdm wrapper to provide a status bar
#for row in csv_f:
for row in tqdm(data,total=row_count):
    
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
    
print (rows,"rows transposed to",values_transposed,"values in:",time.time()-start_time,"seconds")
print ("Done.")
f.close()
