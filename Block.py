#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/11 上午11:01

base Info
"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'

import numpy as np
import pandas as pd

from math import radians, cos, sin, asin, sqrt

class Block(object):

    def __init__(self, data, step=1):
        self.step = 1
        self.data = data
        self.start_lng, self.end_lng, self.start_lat, self.end_lat = self.get_range()
        self.lng_step = (self.end_lng - self.start_lng) / 100
        self.lat_step = (self.end_lat - self.start_lat) / 100
        self.shops_divide = []

    def get_range(self):
        return self.data['shopGlng'].min(), self.data['shopGlng'].max(), \
               self.data['shopGlat'].min(), self.data['shopGlat'].max()

    @staticmethod
    def get_distance(lng1, lat1, lng2, lat2):
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * 6371
        return dis

    # 横向纵向距离98 94km 所以划分100*100个格子，每个格子大小约为1km*1km
    def divide_square(self):

        for i in range(101):
            row = []
            for j in range(101):
                tmp = []
                row.append(tmp)
            self.shops_divide.append(row)
        num = 0
        for index in self.data.index:
            lng = self.data.loc[index].shopGlng
            lat = self.data.loc[index].shopGlat
            i_index = int((lng - self.start_lng) / self.lng_step)
            j_index = int((lat - self.start_lat) / self.lat_step)
            # print(i_index, j_index, lng, lat)
            self.shops_divide[i_index][j_index].append(self.data.loc[index])
            if num % 1000 ==0:
                print(num, i_index, j_index)
            num += 1
        print('finished')
        # return self.shops_divide
        # for i in range(100):
        #     for j in range(100):
        #         if len(self.shops_divide[i][j]) != 0:
        #             print(len(self.shops_divide[i][j]), i, j)

    def get_square(self, lng, lat):
        i_index = int((lng - self.start_lng)/self.lng_step)
        j_index = int((lat - self.start_lat)/self.lat_step)
        if i_index > 100 or j_index > 100:
            return []
        return self.shops_divide[i_index][j_index]

if __name__ == '__main__':
    data = pd.read_csv('./tmp_data/all.csv', header=0)
    # data = data.dropna()
    # print(data.describe())
    block = Block(data)
    print(block.get_range())
    block.divide_square()