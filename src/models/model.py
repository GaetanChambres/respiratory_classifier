import xgboost as xgb

def create_model() :

    model = xgb.XGBClassifiertree = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
    colsample_bytree=1, gamma=0, learning_rate=0.1, max_delta_step=0,
    max_depth=3, min_child_weight=1, missing=None, n_estimators=100,
    n_jobs=1, nthread=None, objective='binary:logistic', random_state=0,
    reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None, silent=True, subsample=1)

    return model

def prepare_data(train_dir,test_dir,csv_train_path,csv_train_path,label_col) :

    l = prsg.ordering_files(train_dir)
    dim1 = len(l)
    tmp = pickle.load(open(train_dir+l[0],'rb'))
    dim2 = len(tmp)
    data_train = np.zeros((dim1,dim2)) # creating the features array for train
    cpt=0
    for f in l:
        tmp = pickle.load(open(train_dir+f,'rb'))
        tmparray = np.asarray(tmp)
        data_train[cpt] = tmparray
        cpt+=1


    l2 = prsg.ordering_files(test_dir)
    dim1 = len(l2)
    tmp2 = pickle.load(open(test_dir+l2[0],'rb'))
    dim2 = len(tmp2)
    data_test = np.zeros((dim1,dim2)) # creating the features array for test
    cpt=0
    for f in l2:
        tmp = pickle.load(open(test+f,'rb'))
        tmparray = np.asarray(tmp)
        data_test[cpt] = tmparray
        cpt+=1


    labels_train = np.loadtxt(csv_train_path, delimiter = ',',skiprows=0,usecols=range(label_col-1,label_col))
    labels_test = np.loadtxt(csv_test_path, delimiter = ',',skiprows=0,usecols=range(label_col-1,label_col))

    return data_train, labels_train, data_test, labels_train

def train_model(model,data_train,labels_train):

    model.fit(data_train, labels_train)

    preds = tree.predict(array_test)
    predictions = [round(value) for value in preds]

    from sklearn.metrics import accuracy_score
    y = np.loadtxt(csv_test_file,delimiter = ',',skiprows = 0,usecols=range(5,6))
    accuracy = accuracy_score(y, preds)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
