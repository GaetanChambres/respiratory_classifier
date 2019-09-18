
import os
import sys
import librosa
import numpy as np
import pickle
from progressbar import ProgressBar

pbar = ProgressBar()

CYCLES_FOLDER = "splitted_cycles/"
CSV_PATH = "csv/info.csv"
dest_folder = "data/balanced_data/"

# Function that return an alphabetically ordered list
# of the files included in a given directory
###########################################################################
def ordering_files(directory):
    return(sorted(os.listdir(directory)))
##########################################################################

arguments = sys.argv
input_dir = arguments[1]

list = input_dir.split("/")
target_value = list[6]
target = target_value+"/"

if target_value == "train":
    max_n_files = 133
    final_file_name = "balanced_train_NOsymptoms"
if target_value == "test":
    max_n_files = 170
    final_file_name = "balanced_test_NOsymptoms"


dest_path = dest_folder+target
os.makedirs(dest_path, exist_ok=True)


cycles_path = input_dir+CYCLES_FOLDER
csv_file = input_dir+CSV_PATH

files_list = ordering_files(cycles_path)

pathologies = np.loadtxt(csv_file,delimiter = ',',skiprows = 0,usecols=range(3,4))
print(pathologies) #list of int from 0 to 6

crackles = crackles = np.loadtxt(csv_file,delimiter = ',',skiprows = 0,usecols=range(4,5))
print(crackles) #list of int from 0 to 1

wheezes = np.loadtxt(csv_file,delimiter = ',',skiprows = 0,usecols=range(5,6))
print(wheezes) #list of int from 0 to 1

cpt=0
cpt0=0
cpt1=0
mylist=[]
labels =[]

output = dest_folder+target_value+".csv"
out_file = open(output, "w")


from shutil import copyfile

for f1 in pbar(files_list): #pbar is progressbar; only visual
    if f1.startswith("156") or f1.startswith("218"):
    # if f1.startswith("5000") or f1.startswith("5000"):
        print("unwanted file detected")
    else:

        if(pathologies[cpt]==7): #if pathology is healthy
            if ( (int(crackles[cpt])==0) and (int(wheezes[cpt])==0) ): #if there is NO crackle AND NO wheeze
                # print(cpt)
                cpt0+=1 #add 1 to the number of healthy records whithout symptoms
                copyfile(cycles_path+f1,dest_path+f1)
                y, sr = librosa.load(cycles_path+f1) # open the audio file
                a = np.append(y,0) #add 0 to labelize healthy record
                mylist.append(a)
                out_file.write(f1[:-4]+",0\n")
            else:
                print("encoutered a cycle healthy with symptoms")

        else:
            if ( (int(crackles[cpt])==0) and (int(wheezes[cpt])==0) ): #if pathology IS NOT healthy, but no symptoms
                if cpt1!=max_n_files:
                    cpt1+=1 #add 1 to the number of pathological records whithout symptoms
                    copyfile(cycles_path+f1,dest_path+f1)
                    y, sr = librosa.load(cycles_path+f1) # open the audio file
                    a = np.append(y,1) #add 0 to labelize healthy record
                    mylist.append(a)
                    out_file.write(f1[:-4]+",1\n")

    cpt+=1
print("healthy cycles without symptoms",cpt0)
print("pathological cycles whithout symptoms : ",cpt1)
print("total interesting values should be : ",cpt0+cpt1)
print("total is actually : ",len(mylist)) #should give the number of files

pickle.dump(mylist,open('pickles/'+final_file_name,'wb'))


# cpt_tmp = 0
# files_list2 = ordering_files(dest_path)
# for f2 in files_list2:
#     if f2.startswith("156") or f2.startswith("218"):
#         os.remove(dest_path+f2)
#         cpt_tmp+=1
# print(str(cpt_tmp)+" files removed for no horse")
# print("FINAL interesting values are : ",cpt0+cpt1-cpt_tmp)

print("Finished")
