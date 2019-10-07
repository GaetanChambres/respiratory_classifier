
import os
import sys
import librosa
import numpy as np
import pickle
from shutil import copyfile
from progressbar import ProgressBar

pbar = ProgressBar()

# Function that return an alphabetically ordered list
# of the files included in a given directory
###########################################################################
def ordering_files(directory):
    return(sorted(os.listdir(directory)))
##########################################################################
def create_patho_folder(target,split):
    patho_folder = target+"patho"+str(split)+"/"
    os.makedirs(patho_folder, exist_ok=True)
    return patho_folder



arguments = sys.argv
input_dir = arguments[1]

list = input_dir.split("/")
target_value = list[2]
target = target_value+"/"

if target_value == "train":
    max_n_files = 133
    final_file_name = "balanced_train_NOsymptoms"
    label = np.loadtxt("data/balanced_data/train.csv",delimiter = ',',skiprows = 0,usecols=range(1,2))
if target_value == "test":
    max_n_files = 170
    final_file_name = "balanced_test_NOsymptoms"
    label = np.loadtxt("data/balanced_data/test.csv",delimiter = ',',skiprows = 0,usecols=range(1,2))


split = 0

healthy_folder = input_dir+"healthy/"
os.makedirs(healthy_folder, exist_ok=True)

patho_folder = create_patho_folder(input_dir,split)

print(label)

files_list = ordering_files(input_dir)
cpt=0
tmp=0
for f in pbar(files_list):
    if(os.path.isfile(input_dir+f)):
        if( (int(label[cpt])==0)):
            copyfile(input_dir+f,healthy_folder+f)
            cpt+=1
        elif(int(label[cpt])==1):
            if(tmp!=max_n_files):
                tmp+=1
                copyfile(input_dir+f,patho_folder+f)
                cpt+=1
            else:
                tmp=0
                split +=1
                patho_folder = create_patho_folder(input_dir,split)
                copyfile(input_dir+f,patho_folder+f)
                cpt+=1
