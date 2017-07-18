#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/5 上午10:23

base Info
"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'


import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.cross_validation import train_test_split

import time
start_time = time.time()

train = pd.read_csv('Digit_Recognizer/train.csv')
test = pd.read_csv('Digit_Recognizer/test.csv')

train_xy, val = train_test_split(train, test_size=0.3, random_state=1)

y = train_xy.label
X = train_xy.drop(['label'], axis=1)
val_y = val.label
val_X = val.drop(['label'], axis=1)

xgb_val = xgb.DMatrix(val_X, label=val_y)
xgb_train = xgb.DMatrix(X, label=y)
xgb_test = xgb.DMatrix(test)

params = {
    'booster':'gbtree',
    'objective':'multi:softmax',
    'num_class':10,
    'gamma':0.1,
    'max_depth':12,
    'lambda':2,
    'subsample':0.7,
    'colsample_bytree':0.7,
    'min_child_weight':3,
    'silent':0,
    'eta':0.007,
    'seed':1000,
    'nthread':7,
}

plst = list(params.items())
num_rounds = 5
watchlist = [(xgb_train, 'train'), (xgb_val, 'val')]

model = xgb.train(plst, xgb_train, num_rounds, watchlist, early_stopping_rounds=100)
model.save_model('./model/xgb.model')
print('best best_ntree_limit', model.best_ntree_limit)

preds = model.predict(xgb_test,ntree_limit=model.best_ntree_limit)
np.savetxt('xgb_submission.csv', np.c_[range(1,len(test)+1), preds], delimiter=',', header='ImageId,Label', comments='', fmt='%d')
cost_time = time.time() - start_time
print('xgboost success!', '\n', 'cost time:',cost_time,'(s)')