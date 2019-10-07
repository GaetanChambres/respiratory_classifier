import os
import sys
import librosa
import numpy as np
import pickle
from progressbar import ProgressBar

# Function that return an alphabetically ordered list
# of the files included in a given directory
###########################################################################
def ordering_files(directory):
    return(sorted(os.listdir(directory)))
##########################################################################
dest_folder = "data/samples/"

arguments = sys.argv
input_dir = arguments[1]

list = input_dir.split("/")
target_value = list[2]
target = target_value+"/"

if target_value == "train":
    final_file_name = "train_split.pickle"
    n_max = 14
if target_value == "test":
    final_file_name = "test_split.pickle"
    n_max = 7

output = dest_folder+target+"packed/"+target_value+"_split.csv"
out_file = open(output, "w")

label0 = input_dir+"healthy/"
mylist=[]

healthy_list = ordering_files(label0)

pbar = ProgressBar()
for f in pbar(healthy_list):
    y, sr = librosa.load(label0+f) # open the audio file
    a = np.append(y,0) #add 0 to labelize healthy record
    mylist.append(a)
    out_file.write(f[:-4]+",0\n")

pbar = ProgressBar()
from random import randint
split = randint(0,n_max)
print("folder selected for split is number "+str(split))
label1 = input_dir+"patho"+str(split)+"/"
patho_list = ordering_files(label1)

for f in pbar(patho_list):
    y, sr = librosa.load(label1+f) # open the audio file
    a = np.append(y,1) #add 0 to labelize healthy record
    mylist.append(a)
    out_file.write(f[:-4]+",1\n")

pickle.dump(mylist,open(dest_folder+target+"packed/"+final_file_name,'wb'))
