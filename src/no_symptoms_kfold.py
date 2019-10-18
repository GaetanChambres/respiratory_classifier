import sys
import pandas as pd
import numpy as np
import xgboost as xgb
import csv as csv
import random as rd
import sklearn.metrics as sklm

def csv_nb_cols(fname,delimiter):
    line = fname.readline()
    data = line.split(delimiter)
    nb_col = len(data)
    return nb_col

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def processing(features,labels):
    ft_size = len(features)
    lb_size = len(labels)

    indexes = np.zeros(lb_size)
    cpt=0
    for i in range(0,len(indexes)):
        indexes[i]=cpt
        cpt+=1

    selected_features = []
    selected_labels = []
    tmp = []

    for i in range(0,ft_size):
        if labels[i] == 0:
            selected_features.append(features[i])
            selected_labels.append(labels[i])
            tmp.append(i)
    indexes = np.delete(indexes,tmp)

    # selected labels count
    # unique, counts = np.unique(selected_labels, return_counts=True)
    # print(dict(zip(unique, counts)))

    expected = len(selected_labels)
    j=0
    while j != expected:
        random_index = rd.randint(0,len(indexes)-1)
        if labels[random_index] == 1:
            selected_features.append(features[random_index])
            selected_labels.append(labels[random_index])
            indexes = np.delete(indexes,random_index)
            j+=1

    # selected labels count
    # unique, counts = np.unique(selected_labels, return_counts=True)
    # print(dict(zip(unique, counts)))

    selected_features = np.asarray(selected_features)
    selected_labels = np.asarray(selected_labels)

    return selected_features,selected_labels


arguments = sys.argv
dir = arguments[1]


print("-- Loading train files")
input_train = dir+"ft_train.csv"
info_train = dir+"/train.csv"
with open(input_train) as f1:
    nbcols_train = csv_nb_cols(f1,delimiter = ",")
    # print(nbcols_train)

features_train = np.loadtxt(input_train, delimiter=",", skiprows = 0, usecols=range(1,nbcols_train))
# print(train_dataset)
labels_train = np.loadtxt(info_train,delimiter = ',',skiprows = 0, usecols=range(1,2))
# labels = train_info[:,0:1]

features_train,labels_train = processing(features_train,labels_train)

# labels count
unique, counts = np.unique(labels_train, return_counts=True)
print("Train class counter :"+str(dict(zip(unique, counts))))

print("-- Loading test files")
input_test = dir+"ft_test.csv"
info_test = dir+"/test.csv"
with open(input_test) as f1:
    nbcols_test = csv_nb_cols(f1,delimiter = ",")
    # print(nbcols_train)

features_test = np.loadtxt(input_test, delimiter=",", skiprows = 0, usecols=range(1,nbcols_test))
# print(train_dataset)
labels_test = np.loadtxt(info_test,delimiter = ',',skiprows = 0, usecols=range(1,2))
# labels = train_info[:,0:1]

features_test,labels_test = processing(features_test,labels_test)

# labels count
unique, counts = np.unique(labels_test, return_counts=True)
print("Test class counter :"+str(dict(zip(unique, counts))))

tree = xgb.XGBClassifiertree = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
n_jobs=1, nthread=None, objective='binary:logistic', random_state=0,
reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=1)

print("-- Training model")
tree.fit(features_train,labels_train)

# xgb.plot_importance(tree,max_num_features = 25)
from matplotlib import pyplot
# xgb.plot_tree(model)
# pyplot.show()
print()

preds = tree.predict(features_test)
predictions = [round(value) for value in preds]
print("-- Testing model")
from sklearn.metrics import accuracy_score
# print(preds)
accuracy = accuracy_score(labels_test, preds)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

from sklearn.metrics import classification_report
print(classification_report(labels_test, preds))
