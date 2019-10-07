###
### GENERAL IMPORTS
###

import os
import csv
import re
import sys
import numpy as np

# personal but general tools :
import utilities.parsing_tools as prsg

import pickle
import tables
from parsing_data_into_csv import parsing_data_to_csv
from split_audio_into_cycles import split_record_in_cycle
from compute_lowlevel_features import essentia_lowlevel_features_computation

from progressbar import ProgressBar
pbar = ProgressBar()

###
### Fonction qui vérifie que le répertoire choisi comme répertoire de travail semble cohérent par rapport à ce qui est attendu
### En l'occurence, on vérifie la présence de fichier ou de dossier, s'il sagit des dossiers déclarés par le variables globales
### et/ou si le fichiers sont de type txt ou wav.
### Si des incohérence sont relevées (dossier strictement vide ou fichier non text et non wav, etc) un erreur est levée et stop l'execution (return 0)
### Si des doutes sur l'arborescence, alors une mise en garde est affichée
### Si tout correspont à l'archi attendue, tout va bien (return 1)
###

def verify_working_directory(directory):
    train_files = prsg.ordering_files(directory)
    if len(train_files) == 0:
        print("ERROR : found no file nor directory")
        print("This may be the wrong folder")
        return 0
    else:
        for filename in train_files:
            path = directory+filename
            # print(path)
            if (os.path.isdir(path)):
                if(filename==CSV_FOLDER_NAME[:-1] or filename==SPLITTED_FOLDER_NAME[:-1]):
                    continue
                else:
                    print("WARNING : found an non initial folder")
                    print("This could be the wrong folder, be carefull !")
                    # return 0
                    continue
            elif(os.path.isfile(path)):
                if (filename.endswith('.txt') or filename.endswith('wav')):
                    # print(filename+" looks like an expected file")
                    continue
                else:
                    print('ERROR : found a non \'txt\' nor \'wav\' file')
                    print("This should be the wrong folder")
                    return 0
            else:
                print("ERROR : found no file nor directory")
                print("This is the wrong folder")
                return 0
        return 1


####################
#  MAIN
####################

TRAIN_FOLDER = "train/"
TEST_FOLDER = "test/"

CSV_FOLDER_NAME = "csv/"
CSV_FILE_NAME = "info.csv"

SPLITTED_FOLDER_NAME = "splitted_cycles/"

FEATURES_FOLDER_NAME = "features/"

arguments = sys.argv


###
### 1st argument -> general folder where everything will happen
### Let's define the different needed folders : train / test / csv / splitted_audio
###

input_train_dir = arguments[1]+TRAIN_FOLDER

input_test_dir = arguments[1]+TEST_FOLDER

out_train_csv = open (arguments[1]+'ft_train.csv','w')
out_test_csv = open (arguments[1]+'ft_test.csv','w')

#########
# TRAIN #
#########

### STEP 3 : Compute features representing audio
################################################
# features_train_dir,status = prsg.verify_folder(input_train_dir,FEATURES_FOLDER_NAME) # Verify if folder already exists and if it is empty or not
list_features = prsg.ordering_files(input_train_dir)
# if(status == 0):
    # print("ERROR : Can not find nor create the asked folder")
    # sys.exit()
# elif(status == 1):
print("TRAIN")
for f in pbar(list_features):
    filename = f[:-4]
    ft_path = input_train_dir+filename
    print(input_train_dir+f)
    if(os.path.isfile(input_train_dir+f)):
        # print(f)
        ft = essentia_lowlevel_features_computation(input_train_dir,f)
        # print(ft)
        out_train_csv.write(filename)
        for val in ft:
            out_train_csv.write(","+val)
        out_train_csv.write("\n")

    # hello += 1
    # pickle.dump(ft, open(ft_path, 'wb'))


########
# TEST #
########

### STEP 3 : Compute features representing audio
################################################
# features_test_dir,status = prsg.verify_folder(input_test_dir,FEATURES_FOLDER_NAME)
list_features = prsg.ordering_files(input_test_dir)
# if(status == 0):
#     print("ERROR : Can not find nor create the asked folder")
# #     sys.exit()
# elif(status == 1):
for f in list_features:
    filename = f[:-4]
    ft_path = input_test_dir+filename
    print(input_test_dir+f)
    if(os.path.isfile(input_test_dir+f)):
        ft = essentia_lowlevel_features_computation(input_test_dir,f)
        out_test_csv.write(filename)
        for val in ft:
            out_test_csv.write(","+val)
        out_test_csv.write("\n")

    # pickle.dump(ft, open(ft_path, 'wb'))
