import sys
import os
import csv
import numpy as np
from progressbar import ProgressBar
pbar = ProgressBar()
out_csv_file = ""
# import utilities.parsing_tools as prsg

# Function that return an alphabetically ordered list
# of the files included in a given directory
###########################################################################
def ordering_files(directory):
    return(sorted(os.listdir(directory)))
##########################################################################
# Function that returns the number of lines from a given file
###########################################################################
def nb_lines(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
##########################################################################


cycles_path = ""
csv_path = "ICBHI_final_database/test/csv-info/test-info.csv"

# files_list = ordering_files(cycles_path)

names = np.loadtxt(csv_path,dtype=str,delimiter=',',skiprows=0,usecols=range(0,1))
pathologies = np.loadtxt(csv_path,delimiter = ',',skiprows=0,usecols=range(3,4))
print(pathologies) #list of int from 0 to 6

crackles = np.loadtxt(csv_path,delimiter=',',skiprows=0,usecols=range(4,5))
wheezes = np.loadtxt(csv_path,delimiter=',',skiprows=0,usecols=range(5,6))
print(crackles) #list of int from 0 to 1
print(wheezes) #list of int from 0 to 1

i=0
c_cpt=w_cpt=h_cpt=0
old_name=""
old_name=names[i][:3]
# for f1 in pbar(files_list):
while i != nb_lines(csv_path):
    if old_name != names[i][:3]:
        if(c_cpt!=0 or w_cpt!=0):
            if(h_cpt!=0):
                print("found record named "+old_name+" with "+str(c_cpt+w_cpt)+ " symptomatic and "+str(h_cpt)+" asymptomatic cycles")
        h_cpt=0
        c_cpt=0
        w_cpt=0
        old_name=names[i][:3]
    if (int(crackles[i])==0 and int(wheezes[i])==0):
        h_cpt+=1
    else:
        if (int(crackles[i])==1):
            c_cpt+=1
        if (int(wheezes[i])==1):
            w_cpt+=1
    i+=1
