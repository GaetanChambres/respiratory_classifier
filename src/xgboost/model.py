import xgboost as xgb

def create_xgb_model(base_score='0.5', booster='gbtree', colsample_bylevel='1',
colsample_bytree='1', gamma='0', learning_rate='0.1', max_delta_step='0',
max_depth='3', min_child_weight='1', missing='None', n_estimators='100',
n_jobs='1', nthread='None', objective='binary:logistic', random_state='0',
reg_alpha='0', reg_lambda='1', scale_pos_weight='1', seed='None', silent='True', subsample='1') :

    model = xgb.XGBClassifier(base_score=base_score, booster=booster, colsample_bylevel=colsample_bylevel,
       colsample_bytree=colsample_bytree, gamma=gamma, learning_rate=learning_rate, max_delta_step=max_delta_step,
       max_depth=max_depth, min_child_weight=min_child_weight, missing=missing, n_estimators=n_estimators,
       n_jobs=n_jobs, nthread=nthread, objective=objective, random_state=random_state,
       reg_alpha=reg_alpha, reg_lambda=reg_lambda, scale_pos_weight=scale_pos_weight, seed=seed, silent=silent, subsample=subsample)

    return model

#  MAIN

# xgbmodel = create_xgb_model()
#
# print(xgbmodel)
