#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 8:36
# @Author  : zlb
# @Email   : 15967924690@163.com
# @File    : algorithm.py
# @Software: PyCharm

def cal_pai_mc(n=1000000):
    "蒙特卡洛 随机选择算法 随机"
    import random
    for i in range(0, n+1):
         x = random.uniform(0, 1)
         y = random.uniform(0, 1)



