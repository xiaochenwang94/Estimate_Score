#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/17 下午8:37

__file__

    train_model.py

__description__

    This file trains various models

__author__

    Xiaochen Wang < xiaochenwang94@gmail.com >

"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'

import sys
import csv
import os
import numpy as np
import pandas as pd
import xgboost as xgb
from scipy.sparse import hstack
## sklearn
from sklearn.base import BaseEstimator
from sklearn.datasets import load_svmlight_file, dump_svmlight_file
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, LassoCV, LassoLars, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPRegressor

all_data = pd.read_csv('../tmp_data/final_data.csv')
all_data['shopPower'] = all_data['shopPower']/10
train, test = train_test_split(all_data, test_size=0.3, random_state=1)

y_train = train.shopPower
X_train = train.drop(['shopPower'], axis=1)
y_test = test.shopPower
X_test = test.drop(['shopPower'], axis=1)

def rmse_cv(model):
    # predicted = cross_val_predict(model, X_train, y_train, cv=10)
    # rmse = np.sqrt(metrics.mean_squared_error(y_train, predicted))
    rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring='neg_mean_squared_error', cv=10))
    return rmse

# Ridge model
# rmse = 0.903333472866, 0.883236055734
def ridge():
    alphas = [0.05, 0.1, 0.3, 1, 3, 5, 10 ,15, 30, 50, 75]
    cv_ridge = [rmse_cv(Ridge(alpha=alpha)).mean() for alpha in alphas]
    cv_ridge = pd.Series(cv_ridge, index=alphas)
    print(cv_ridge.min())
    print(cv_ridge.argmin())
    model = Ridge(alpha=cv_ridge.argmin())
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, preds))
    print(rmse)


# Lasso
# rmse = 0.832105056562
def lasso():
    model_lasso = LassoCV(alphas=[1, 0.1, 0.001, 0.0005]).fit(X_train, y_train)
    print(rmse_cv(model_lasso).min())

# xgboost
# rmse = 0.495967809013
def xgboost_reg():
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test)

    model_xgb = xgb.XGBRegressor(n_estimators=360, max_depth=8, learning_rate=0.1, eval_metric=['rmse'])
    model_xgb.fit(X_train, y_train)
    xgb_preds = model_xgb.predict(X_test)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, xgb_preds))
    print(rmse)

# SVR
# 0.75441199608
def svr_reg():
    svr = SVR(kernel='rbf', gamma=0.1)
    svr.fit(X_train, y_train)
    preds = svr.predict(X_test)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, preds))
    print(rmse)

# mlp
# 1.881883663
def mlp_reg():
    mlp = MLPRegressor()
    mlp.fit(X_train, y_train)
    preds = mlp.predict(X_test)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, preds))
    print(rmse)

mlp_reg()