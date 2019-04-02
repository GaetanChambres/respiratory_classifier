import os
import csv
import re
import sys
import utilities.parsing_tools as prsg
import xgboost.model as model
from parsing_data_into_csv import parsing_data_to_csv
from split_audio_into_cycles import split_record_in_cycle

TRAIN_FOLDER = "train/"
TEST_FOLDER = "test/"
CSV_FOLDER_NAME = "csv/"
CSV_FILE_NAME = "info.csv"
SPLITTED_FOLDER_NAME = "splitted_cycles/"

def verify_folder(directory):
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
                    print("ERROR : found an unexpected folder")
                    print("This may be the wrong folder")
                    return 0
            elif(os.path.isfile(path)):
                if (filename.endswith('.txt') or filename.endswith('wav')):
                    # print(filename+" looks like an expected file")
                    continue
                else:
                    print('ERROR : found a non \'txt\' nor \'wav\' file')
                    print("This may be the wrong folder")
                    return 0
            else:
                # print("ERROR : found no file nor directory")
                print("This may be the wrong folder")
                return 0
        return 1

def csv_creation(input_dir,diag_file,csv_dir,csv_filename,status):
    if not (os.path.exists(csv_dir)):
        print(status+"CSV folder does not exist")
        parsing_data_to_csv(input_dir,diag_file,csv_dir,csv_filename)
        print(status+"In the CSV folder, creation of the file :"+csv_filename+"\n")
    elif(len(os.listdir(csv_dir) ) == 0):
        print(status+"CSV file does not exist")
        parsing_data_to_csv(input_dir,diag_file,csv_dir,csv_filename)
        print(status+"In the CSV folder, creation of the file :"+csv_filename+"\n")
    else:
        print(status+"CSV already existing\n")

def splitting_audio(input_dir,csv_file,output_dir,status):
    print(output_dir)
    if not (os.path.exists(output_dir)):
        print(status+"output folder does not exist")
        print(status+"let split audio into cycles")
        split_record_in_cycle(input_dir,csv_file,output_dir)
        print(status+"Audio splitted into cycles in the folder :"+output_dir+"\n")
    elif(len(os.listdir(output_dir) ) == 0):
        print(status+"CSV file does not exist")
        print(status+"let split audio into cycles")
        split_record_in_cycle(input_dir,csv_file,output_dir)
        print(status+"Audio splitted into cycles in the folder :"+output_dir+"\n")
    else:
        print(status+"CSV already existing\n")



arguments = sys.argv

input_train_dir = arguments[1]+TRAIN_FOLDER
csv_train_dir = input_train_dir+CSV_FOLDER_NAME
cycles_train_dir = input_train_dir+SPLITTED_FOLDER_NAME

input_test_dir = arguments[1]+TEST_FOLDER
csv_test_dir = input_test_dir+CSV_FOLDER_NAME
cycles_test_dir = input_test_dir+SPLITTED_FOLDER_NAME

diag_file = arguments[2]


if not (verify_folder(input_train_dir) or verify_folder(input_test_dir)):
    print("ERROR : Wrong folders")
    sys.exit()

# TRAIN
train_files = prsg.ordering_files(input_train_dir)
csv_creation(input_train_dir,diag_file,csv_train_dir,CSV_FILE_NAME,"TRAIN : ")
#  TEST
test_files = prsg.ordering_files(input_test_dir)
csv_creation(input_test_dir,diag_file,csv_test_dir,CSV_FILE_NAME,"TEST : ")

# TRAIN
csv_train_file=csv_train_dir+CSV_FILE_NAME
# print("hayaaaaaaaaaaaaaa")
# splitting_audio(input_train_dir,csv_train_file,cycles_train_dir,"TRAIN : ")
# # TEST
# csv_test_file=csv_test_dir+CSV_FILE_NAME
# splitting_audio(input_test_dir,csv_test_file,cycles_test_dir,"TEST : ")
