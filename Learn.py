#!/usr/bin/env
# coding:utf-8
"""
Created on 17/7/18 上午8:42

base Info
"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'

import shlex

str = shlex.shlex("ab,'987,23462,sdfh',daslfjl:iosjfo", posix=True)
str.whitespace = ','
str.whitespace_split = True
b = list(str)
print(b)