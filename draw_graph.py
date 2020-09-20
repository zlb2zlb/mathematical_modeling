#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/9/19 16:09
# @Author  : zlb
# @Email   : 15967924690@163.com
# @File    : draw_graph.py
# @Software: PyCharm
import matplotlib.pyplot as plt
import numpy as np

list1=[1,2,3,4,5,6,2,3,4,6,7,5,7]
list2=[2,3,4,5,8,9,2,1,3,4,5,2,4]
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.title('显示中文标题')
plt.xlabel("横坐标")
plt.ylabel("纵坐标")
x=np.arange(0,len(list1))+1
x[0]=1
my_x_ticks = np.arange(1, 14, 1)
plt.xticks(my_x_ticks)
plt.plot(list1,list1)
plt.plot(list1,list2)
plt.show()