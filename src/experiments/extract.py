import os
import sys
import librosa
import numpy as np
import pickle

thearray = pickle.load(open("pickles/test_NOsymptoms",'rb'))

print(len(thearray))
print()

thearray2 = pickle.load(open("pickles/test_labels",'rb'))

print(len(thearray2))
print()

array = pickle.load(open("pickles/train_NOsymptoms",'rb'))

print(len(array))
print()

array2 = pickle.load(open("pickles/train_labels",'rb'))

print(len(array))
print()
# print(array)


tmpT = pickle.load(open("pickles/pickles_files/train_crackles",'rb'))
tmpt = pickle.load(open("pickles/pickles_files/test_crackles",'rb'))

print(tmpT)
# print(tmpt.shape)

#
# for i in range(0,len(thearray)-1):
#     print(len(thearray[i]))
