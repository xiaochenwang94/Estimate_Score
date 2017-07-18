#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/5 下午2:58

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

data = pd.read_csv('./tmp_data/new.csv', header=0)
data['shopPower'] = data['shopPower']/5
data['shopPower'].astype(int)
print(data['shopPower'])

train_xy, test = train_test_split(data, test_size=0.3, random_state=1)

y = train_xy.shopPower
X = train_xy.drop(['shopPower'], axis=1)
test_y = test.shopPower
test_X = test.drop(['shopPower'], axis=1)

xgb_train = xgb.DMatrix(X, label=y)
xgb_test = xgb.DMatrix(test)

params = {
    'booster':'gbtree',
    'objective':'multi:softmax',
    'num_class':11,
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
num_rounds = 50
watchlist = [(xgb_train, 'train')]

model = xgb.train(plst, xgb_train, num_rounds, watchlist, early_stopping_rounds=100)
model.save_model('./model/xgbEst.model')
print('best best_ntree_limit', model.best_ntree_limit)

preds = model.predict(xgb_test,ntree_limit=model.best_ntree_limit)
np.savetxt('xgb_est.csv', np.c_[range(1,len(test)+1), preds], delimiter=',', header='Id, shopPower', comments='', fmt='%d')
cost_time = time.time() - start_time
print('xgboost success!', '\n', 'cost time:',cost_time,'(s)')
