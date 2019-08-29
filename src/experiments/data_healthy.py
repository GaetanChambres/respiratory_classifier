#
#
#
# ce fichier trie les cycles respiratoires d'un dossier donné en identifiant
# les cycles sains sans symptomes (label=0) des cycles pathologiques sans symptomes (label=1)
# On sauve une liste de listes qui contienent les données audio des cycles suivi de leur label
# on exporte cette liste sous format pickle
#
#
#


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

# creation of the final list, with len(files_list) the size (the number of files)
for r in range(0,len(files_list)):
    mylist.append(0)
# print(len(mylist))
# print(mylist)

for f1 in pbar(files_list): #pbar is progressbar; only visual

    y, sr = librosa.load(cycles_path+f1) # open the audio file
    # print("sampling rate = ",sr)

    # print("label =")
    # print(pathologies[cpt])
    # print("values =")
    # print(y)

    if(pathologies[cpt]==7): #if pathology is healthy
        if ( (int(crackles[cpt])==0) and (int(wheezes[cpt])==0) ): #if there is NO crackle AND NO wheeze
            # print(cpt)
            cpt0+=1 #add 1 to the number of healthy records whithout symptoms
            # a = np.append(y,pathologies[cpt]) #add patho label after the audio values
            a = np.append(y,0) #add 0 to labelize healthy record
            mylist[cpt]=a #save the final array into a list of arrays
        else:
            print("encoutered a cycle healthy with symptoms")
    else:
        if ( (int(crackles[cpt])==0) and (int(wheezes[cpt])==0) ): #if pathology IS NOT healthy, but no symptoms
            cpt1+=1 #add 1 to the number of pathological records whithout symptoms
            # a = np.append(y,pathologies[cpt]) #add patho label after the audio values
            a = np.append(y,1) #add 1 to labelize healthy record
            mylist[cpt]=a #save the final array into a list of arrays

    cpt+=1

# print(len(mylist)) #should give the number of files
# print(mylist)

pickle.dump(mylist,open('pickles/test_NOsymptoms','wb'))
print("healthy cycles without symptoms",cpt0)
print("pathological cycles whithout symptoms : ",cpt1)
print("Finished")
