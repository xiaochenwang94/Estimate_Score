#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/17 下午8:51

base Info
"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'


import shlex


def process_data(file):
    headers = [
        'shopId',
        'shopName',
        'shopGlat',
        'shopGlng',
        'shopPower',
        'shopType',
        'mainCategoryName',
        'categoryURLName',
        'shopGroupId',
        'categoryName',
        'price',
        'comNum']
    outfile = './data_processed/%s_food_price_processed.csv' % file[:-4]
    output = open(outfile, 'w')
    for header in headers:
        if header == 'comNum':
            output.write(header + '\n')
        else:
            output.write(header + ',')
    infile = './data/%s' % file
    num = 1
    with open(infile) as f:
        for line in f.readlines():
            # print(line)
            print(num)
            num += 1
            line = line.replace("：",":")
            line = shlex.shlex(line, posix=True)
            line.whitespace = ','
            line.whitespace_split = True
            words = list(line)
            for word in words:
                ws = word.split(':')
                ws[0] = ws[0].strip()
                ws[1] = ws[1].replace('"', '').strip()
                if ws[0] in headers:
                    if ws[0] == 'comNum':
                        ws[1] = ws[1].replace('条评论', '')
                        output.write(ws[1] + '\n')
                    else:
                        if ws[1] == '':
                            ws[1] = 'NULL'
                        output.write(ws[1] + ',')
                elif ws[0] == '人均':
                    if ws[1] == '':
                        ws[1] = 'NULL'
                    ws[1] = ws[1].replace('元', '')
                    output.write(ws[1] + ',')
    output.close()

process_data('shopInfo美食.txt')