import os
import csv
import re
import sys
import utilities.parsing_tools as prsg
import xgboost.model as model
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

features_train_dir,status = prsg.verify_folder(input_test_dir,FEATURES_FOLDER_NAME)
list_files = prsg.ordering_files(cycles_train_dir)
if(status == 0):
    print("ERROR : Can not find nor create the asked folder")
    sys.exit()
elif(status == 1):
    for f in list_files:
        print("1")
        print(cycles_train_dir)
        ft = essentia_lowlevel_features_computation(cycles_train_dir,f)
        print(ft)
        print("2")
        print(features_train_dir+f)
        print("3")
        # pickle.dump(ft, open(cyc, 'wb'))
