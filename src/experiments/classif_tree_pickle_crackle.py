# terminate called after throwing an instance of 'std::bad_alloc'
# what():  std::bad_alloc

# May run out of memory 


import pickle
import numpy as np

xtrain=pickle.load(open('./data/train_samples.pickle','rb'))
ytrain=pickle.load(open('./data/train_labels.pickle','rb'))

xtest=pickle.load(open('./data/test_samples.pickle','rb'))
ytest=pickle.load(open('./data/test_labels.pickle','rb'))

print(xtrain.shape, ytrain.shape)




import xgboost as xgb

tree = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
n_jobs=1, nthread=None, objective='binary:logistic', random_state=0,
reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=1)

tree.fit(xtrain, ytrain)

preds = tree.predict(xtest)
predictions = [round(value) for value in preds]

from sklearn.metrics import accuracy_score
accuracy = accuracy_score(ytest, preds)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
