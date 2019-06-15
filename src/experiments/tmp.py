import os
import sys
import librosa
import numpy as np
import pickle
from progressbar import ProgressBar

pbar = ProgressBar()
CYCLES_FOLDER = "splitted_cycles/"
CSV_PATH = "csv/info.csv"

# Function that return an alphabetically ordered list
# of the files included in a given directory
###########################################################################
def ordering_files(directory):
    return(sorted(os.listdir(directory)))
##########################################################################


arguments = sys.argv
input_dir = arguments[1]

cycles_path = input_dir+CYCLES_FOLDER
csv_file = input_dir+CSV_PATH

files_list = ordering_files(cycles_path)

crackles = np.loadtxt(csv_file,delimiter = ',',skiprows = 0,usecols=range(5,6))
cpt=0

mylist=[]
for r in range(0,len(files_list)):
    mylist.append(0)
# print(len(mylist))
# print(mylist)

for f1 in pbar(files_list): #pbar is progressbar; only visual

    y, sr = librosa.load(cycles_path+f1)
    # print("sampling rate = ",sr)

    # print("label =")
    # print(crackles[cpt])
    # print("values =")
    # print(y)

    a = np.append(y,crackles[cpt]) #add label after the values

    # print("append of values and label :")
    # print(a)

    mylist[cpt]=a #save the final array into a list of arrays

    # print(("final list"))
    # print(mylist)

    cpt+=1

print(len(mylist)) #should give the number of files
# print(mylist)

pickle.dump(mylist,open('train_crackles','wb'))

print("Finished")
