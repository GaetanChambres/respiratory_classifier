import os
import sys
import librosa
import numpy as np
import pickle

pickles_dir = "pickles/"
train_pickle = pickles_dir+"train_NOsymptoms"
test_pickle = pickles_dir+"test_NOsymptoms"

test = pickle.load(open(test_pickle,'rb'))

#Ytest
ytest = np.array([])
for data in test:
    ytest=np.append(ytest,data[-1:])
ysize = len(ytest)
# print(ysize)

ypred = np.random.randint(0,2,ysize)

from sklearn.metrics import classification_report
print("RANDOM CLASSIFICATION RESULTS ON "+str(ysize)+" samples")
print(classification_report(ytest, ypred))
