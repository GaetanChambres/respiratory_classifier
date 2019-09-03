##############################
# Ce fichier rassemble l'intégralité des fonctions permettant de tester de la classification de cycles respiratoires selon différents paramètres.
# Des "sécurités" sont mises en places pour éviter de répéter des étapes longues et fastidieuses
# Pour plus de détail sur le fonctionnement, voir dans les commentaires
##############################

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
import models.model as model
from parsing_data_into_csv import parsing_data_to_csv
from split_audio_into_cycles import split_record_in_cycle
from compute_lowlevel_features import essentia_lowlevel_features_computation

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
# csv_train_dir = input_train_dir+CSV_FOLDER_NAME
# cycles_train_dir = input_train_dir+SPLITTED_FOLDER_NAME

input_test_dir = arguments[1]+TEST_FOLDER
# csv_test_dir = input_test_dir+CSV_FOLDER_NAME
# cycles_test_dir = input_test_dir+SPLITTED_FOLDER_NAME

### 2nd argument -> complete path to the diagnostic text file, necessary to process the CSV files
diag_file = arguments[2]

##### VERIFICATION OF THE FOLDERS, TRAIN & TEST
if not (verify_working_directory(input_train_dir) or verify_working_directory(input_test_dir)):
    print("ERROR : Wrong folders")
    sys.exit()
#####

#########
# TRAIN #
#########

### STEP 1 : Preparing CSV file
################################################
csv_train_dir, status = prsg.verify_folder(input_train_dir,CSV_FOLDER_NAME) # Verify if folder already exists and if it is empty or not
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    parsing_data_to_csv(input_train_dir,diag_file,csv_train_dir,CSV_FILE_NAME) # create csv file according to the input and the diag file. Kind of csv is given by the choosen lib imported.

### STEP 2 : Preparing Audio by splitting cycles
################################################
csv_train_file=csv_train_dir+CSV_FILE_NAME # define the name of the folder according to the previous step
cycles_train_dir,status = prsg.verify_folder(input_train_dir,SPLITTED_FOLDER_NAME) # Verify if folder already exists and if it is empty or not
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    split_record_in_cycle(input_train_dir,csv_train_file,cycles_train_dir)

### STEP 3 : Compute features representing audio
################################################
features_train_dir,status = prsg.verify_folder(input_train_dir,FEATURES_FOLDER_NAME) # Verify if folder already exists and if it is empty or not
list_features = prsg.ordering_files(cycles_train_dir)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    for f in list_features:
        ft_path = features_train_dir+f[:-4]
        ft = essentia_lowlevel_features_computation(cycles_train_dir,f)
        pickle.dump(ft, open(ft_path, 'wb'))

########
# TEST #
########

### STEP 1 : Preparing CSV file
################################################
csv_test_dir,status = prsg.verify_folder(input_test_dir,CSV_FOLDER_NAME)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    # csv_creation(input_test_dir,diag_file,csv_test_dir,CSV_FILE_NAME,"TEST : ")
    parsing_data_to_csv(input_test_dir,diag_file,csv_test_dir,CSV_FILE_NAME)

### STEP 2 : Preparing Audio by splitting cycles
################################################
cycles_test_dir,status = prsg.verify_folder(input_test_dir,SPLITTED_FOLDER_NAME)
csv_test_file=csv_test_dir+CSV_FILE_NAME
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    # splitting_audio(input_test_dir,csv_test_file,cycles_test_dir,"TEST : ")
    split_record_in_cycle(input_test_dir,csv_test_file,cycles_test_dir)

### STEP 3 : Compute features representing audio
################################################
features_test_dir,status = prsg.verify_folder(input_test_dir,FEATURES_FOLDER_NAME)
list_features = prsg.ordering_files(cycles_test_dir)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    for f in list_features:
        ft_path = features_test_dir+f[:-4]
        ft = essentia_lowlevel_features_computation(cycles_test_dir,f)
        pickle.dump(ft, open(ft_path, 'wb'))

###

### At this point, data + features are ok
### Next step is to prepare the input (pickles files)

###

# just to simplify syntax
train = features_train_dir
test = features_test_dir

#########
# TRAIN #
#########

l = prsg.ordering_files(train) #list all the pickle files in train

dim1 = len(l)
tmp = pickle.load(open(train+l[0],'rb')) # open the first pickle
dim2 = len(tmp) # take the size of the opened pickle
array_train = np.zeros((dim1,dim2)) # create a 2 dim array : total of pickles * size of 1 pickle
# print("ARRAY OK ?")
# print(array)
# print(array.shape)
# print(type(array[0]))
# print(type(array[0,0]))

cpt=0
for f in l:
    tmp = pickle.load(open(train+f,'rb'))
    tmparray = np.asarray(tmp)
    array_train[cpt] = tmparray
    cpt+=1


########
# TEST #
########

l2 = prsg.ordering_files(test)

dim1 = len(l2)
tmp2 = pickle.load(open(test+l2[0],'rb'))
dim2 = len(tmp2)
array_test = np.zeros((dim1,dim2))
# print("ARRAY OK ?")
# print(array)
# print(array.shape)
# print(type(array[0]))
# print(type(array[0,0]))

cpt=0
for f in l2:
    tmp = pickle.load(open(test+f,'rb'))
    tmparray = np.asarray(tmp)
    array_test[cpt] = tmparray
    cpt+=1

###

### At this point, all pickles files are opened and packed in the array
### Next step is to import model classify

###

csv_path = csv_train_file
# crackles = np.loadtxt(csv_path,delimiter = ',',skiprows = 0,usecols=range(4,5))
# print(crackles)
wheezes = np.loadtxt(csv_path,delimiter = ',',skiprows = 0,usecols=range(5,6))
# print(len(wheezes))
print(wheezes)
# print(type(wheezes[0]))

# tree = model.create_xgb_model()

import models.model as mdl

model = mdl.create_model()
y = np.loadtxt(csv_test_file,delimiter = ',',skiprows = 0,usecols=range(5,6))
mdl.train_model(model,array_train,wheezes,array_test,y)

#
# import xgboost as xgb
#
# tree = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
# colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
# max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
# n_jobs=1, nthread=None, objective='binary:logistic', random_state=0,
# reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=1)
#
#
# tree.fit(array_train, wheezes)
#
# preds = tree.predict(array_test)
# predictions = [round(value) for value in preds]
#
# from sklearn.metrics import accuracy_score
# y = np.loadtxt(csv_test_file,delimiter = ',',skiprows = 0,usecols=range(5,6))
# accuracy = accuracy_score(y, preds)
# print("Accuracy: %.2f%%" % (accuracy * 100.0))
