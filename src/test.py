import os
import csv
import re
import sys
import pickle
import tables
import numpy as np
import utilities.parsing_tools as prsg
import models.model as model
from parsing_data_into_csv import parsing_data_to_csv
from split_audio_into_cycles import split_record_in_cycle
from compute_lowlevel_features import essentia_lowlevel_features_computation

TRAIN_FOLDER = "train/"
TEST_FOLDER = "test/"
CSV_FOLDER_NAME = "csv/"
CSV_FILE_NAME = "info.csv"
SPLITTED_FOLDER_NAME = "splitted_cycles/"
FEATURES_FOLDER_NAME = "features/"

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

def kind_of_features():

    return 0



####################
#  MAIN
####################

arguments = sys.argv

input_train_dir = arguments[1]+TRAIN_FOLDER
# csv_train_dir = input_train_dir+CSV_FOLDER_NAME
# cycles_train_dir = input_train_dir+SPLITTED_FOLDER_NAME

input_test_dir = arguments[1]+TEST_FOLDER
# csv_test_dir = input_test_dir+CSV_FOLDER_NAME
# cycles_test_dir = input_test_dir+SPLITTED_FOLDER_NAME

diag_file = arguments[2]


if not (verify_working_directory(input_train_dir) or verify_working_directory(input_test_dir)):
    print("ERROR : Wrong folders")
    sys.exit()

# TRAIN
#######
csv_train_dir, status = prsg.verify_folder(input_train_dir,CSV_FOLDER_NAME)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    # csv_creation(input_train_dir,diag_file,csv_train_dir,CSV_FILE_NAME,"TRAIN : ")
    parsing_data_to_csv(input_train_dir,diag_file,csv_train_dir,CSV_FILE_NAME)

#  TEST
#######
csv_test_dir,status = prsg.verify_folder(input_test_dir,CSV_FOLDER_NAME)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    # csv_creation(input_test_dir,diag_file,csv_test_dir,CSV_FILE_NAME,"TEST : ")
    parsing_data_to_csv(input_test_dir,diag_file,csv_test_dir,CSV_FILE_NAME)

# TRAIN
cycles_train_dir,status = prsg.verify_folder(input_train_dir,SPLITTED_FOLDER_NAME)
csv_train_file=csv_train_dir+CSV_FILE_NAME
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    # splitting_audio(input_train_dir,csv_train_file,cycles_train_dir,"TRAIN : ")
    split_record_in_cycle(input_train_dir,csv_train_file,cycles_train_dir)

# TEST
cycles_test_dir,status = prsg.verify_folder(input_test_dir,SPLITTED_FOLDER_NAME)
csv_test_file=csv_test_dir+CSV_FILE_NAME
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    # splitting_audio(input_test_dir,csv_test_file,cycles_test_dir,"TEST : ")
    split_record_in_cycle(input_test_dir,csv_test_file,cycles_test_dir)

features_test_dir,status = prsg.verify_folder(input_test_dir,FEATURES_FOLDER_NAME)
list_files = prsg.ordering_files(cycles_test_dir)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    for f in list_files:
        ft_path = features_test_dir+f[:-4]
        ft = essentia_lowlevel_features_computation(cycles_test_dir,f)
        pickle.dump(ft, open(ft_path, 'wb'))

#
#
# At this point, data + features are ok
# Next step is to import model and prepare input
#
#
test = "../../../database/debug/test/features/"
l = prsg.ordering_files(test)
dim1 = len(l)
tmp = pickle.load(open(test+l[0],'rb'))
dim2 = len(tmp)
array = np.zeros((dim1,dim2))
# print("ARRAY OK ?")
# print(array)
print(array.shape)
# print(type(array[0]))
# print(type(array[0,0]))
cpt=0
for f in l:
    tmp = pickle.load(open(test+f,'rb'))
    tmparray = np.asarray(tmp)
    array[cpt] = tmparray
    cpt+=1

#
#
#  at this point, all pickles files are packed in the array
#
#

csv_path = "../../../database/debug/test/csv/info.csv"
# crackles = np.loadtxt(csv_path,delimiter = ',',skiprows = 0,usecols=range(4,5))
# print(crackles)
wheezes = np.loadtxt(csv_path,delimiter = ',',skiprows = 0,usecols=range(5,6))
print(len(wheezes))
# print(wheezes)
# print(type(wheezes[0]))

# tree = model.create_xgb_model()

import xgboost as xgb

tree = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
n_jobs=1, nthread=None, objective='binary:logistic', random_state=0,
reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=1)


print("oooooooooooooooooooooooooooooook")
print()

tree.fit(array, wheezes)
