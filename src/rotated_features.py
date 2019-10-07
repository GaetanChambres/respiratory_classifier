import os
import csv
import re
import sys
import pickle
import numpy as np

from progressbar import ProgressBar


from compute_lowlevel_features import essentia_lowlevel_features_computation

arguments = sys.argv

TRAIN_FOLDER = "train/"
input_train_dir = arguments[1]+TRAIN_FOLDER
input_train_csv = arguments[1]+"train.csv"
out_train_csv = open (arguments[1]+'ft_train.csv','w')

train_files = []
with open(input_train_csv,'rt')as f:
    data = csv.reader(f)
    for row in data:
        # print(row)
        train_files.append(row[0])
# print(train_files)



TEST_FOLDER = "test/"
input_test_dir = arguments[1]+TEST_FOLDER
input_test_csv = arguments[1]+"test.csv"
out_test_csv = open (arguments[1]+'ft_test.csv','w')

test_files = []
with open(input_test_csv,'rt')as f:
    data = csv.reader(f)
    for row in data:
        test_files.append(row[0])

print("TRAIN")

from os import listdir
from os.path import isfile, join
list_features = [f for f in listdir(input_train_dir) if isfile(join(input_train_dir, f))]
list_features = sorted(list_features)
# print(list_features)

pbar = ProgressBar()
for f in pbar(list_features):
    filename = f[:-4]
    if filename in train_files:
        ft_path = input_train_dir+filename
        ft = essentia_lowlevel_features_computation(input_train_dir,f)
        out_train_csv.write(filename)
        for val in ft:
            out_train_csv.write(","+val)
        out_train_csv.write("\n")

print("TEST")

list_features = [f for f in listdir(input_test_dir) if isfile(join(input_test_dir, f))]
list_features = sorted(list_features)
# print(list_features)

pbar = ProgressBar()
for f in pbar(list_features):
    filename = f[:-4]
    if filename in test_files:
        ft_path = input_test_dir+filename
        ft = essentia_lowlevel_features_computation(input_test_dir,f)
        out_test_csv.write(filename)
        for val in ft:
            out_test_csv.write(","+val)
        out_test_csv.write("\n")
