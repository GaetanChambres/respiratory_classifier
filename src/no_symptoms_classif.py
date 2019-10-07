import pandas as pd
import numpy as np
import xgboost as xgb
import csv as csv
# from sklearn.model_selection import train_test_split
import sklearn.metrics as sklm

import warnings
warnings.filterwarnings("ignore")

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

print("LF -- LOADING FILES")
# input_train = "./experiments/data/balanced_data/ft_train.csv"
# info_train = "./experiments/data/balanced_data/train.csv"
input_train = "./experiments/data/samples/ft_train.csv"
info_train = "./experiments/data/samples/train.csv"

# input_test = "./experiments/data/balanced_data/ft_test.csv"
# info_test = "./experiments/data/balanced_data/test.csv"
input_test = "./experiments/data/samples/ft_test.csv"
info_test = "./experiments/data/samples/test.csv"

with open(input_train) as f1:
    nbcols_train = csv_nb_cols(f1,delimiter = ",")
    # print(nbcols_train)
with open(input_test) as f2:
    nbcols_test = csv_nb_cols(f2,delimiter = ",")
    # print(nbcols_test)

print("LF -- Loading train files")
features_train = np.loadtxt(input_train, delimiter=",", skiprows = 0, usecols=range(1,nbcols_train))
# print(train_dataset)
labels_train = np.loadtxt(info_train,delimiter = ',',skiprows = 0, usecols=range(1,2))
# labels = train_info[:,0:1]


print("LF -- Loading test files")
features_test = np.loadtxt(input_test, delimiter=",", skiprows = 0, usecols=range(1,nbcols_test))
# print(features_test)
labels_test = np.loadtxt(info_test,delimiter = ',', skiprows = 0, usecols=range(1,2))
# print(labels_test)

tree = xgb.XGBClassifiertree = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
n_jobs=1, nthread=None, objective='binary:logistic', random_state=0,
reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=1)

tree.fit(features_train,labels_train)

xgb.plot_importance(tree,max_num_features = 25)
from matplotlib import pyplot
# xgb.plot_tree(model)
pyplot.show()
print()

preds = tree.predict(features_test)
predictions = [round(value) for value in preds]

from sklearn.metrics import accuracy_score
print(preds)
accuracy = accuracy_score(labels_test, preds)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

from sklearn.metrics import classification_report
print(classification_report(labels_test, preds))
