#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/10 下午8:10

base Info
"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'

import os
import pandas as pd

file_path = './data_processed/'
files = os.listdir(file_path)
output_file = '%sall_data.csv' % file_path

headers = [
        'shopId',
        'shopName',
        'shopGlng',
        'shopGlat',
        'shopPower',
        'shopType',
        'mainCategoryName',
        'categoryURLName',
        'shopGroupId',
        'categoryName',
        'comNum']
out = open(output_file, 'w')
for header in headers:
    if header != 'comNum':
        out.write(header+',')
    else:
        out.write(header+'\n')
for file in files:
    if '美食' in file:
        continue
    if 'light' in file:
        continue
    if file != 'all_data.csv':
        print(file)
        data = pd.read_csv('%s%s'%(file_path, file), header=0)
        data.to_csv(output_file, header=False, mode='a+', index=False)

