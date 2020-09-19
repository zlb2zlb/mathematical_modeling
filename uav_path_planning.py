#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/9/19 9:02
# @Author  : zlb
# @Email   : 15967924690@163.com
# @File    : uav_path_planning.py
# @Software: PyCharm

# 步长按照时间来计算 0.5s
# 设定蓝色机位置float[x,y],  location_blue,step_blue,direction_blue,velocity_blue
# 当前红色机群位置float[x,y]  location_red_0,location_red_1,velocity_red_0,velocity_red
# 红色机群朝蓝色机移动步长  step_red_0、step_red_1
from math import acos,asin,sqrt
import numpy as np

def getNextLocation(location_blue,location_red,step=0.1):
    '''根据无人机当前位置、步长、方位角，来获得下一时刻的位置'''
    ## step 默认 0.1km
    location_blue_x = float(location_blue[0])
    location_blue_y = float(location_blue[1])
    location_red_x = float(location_red[0])
    location_red_y = float(location_red[1])

    distance = sqrt((location_blue_x - location_red_x)**2 + (location_blue_y - location_red_y)**2)
    delta_x = (location_blue_x - location_red_x) * (step / distance)
    delta_y = (location_blue_y - location_red_y) * (step / distance)
    location_red_x_next = location_red_x + delta_x
    location_red_y_next = location_red_y + delta_y

    return [location_red_x_next,location_red_y_next]

def getAzimuth(location_blue,location_red):
    '''根据蓝方无人机和红方无人机的当前位置，获得对象相位角'''
    location_blue_x = float(location_blue[0])
    location_blue_y = float(location_blue[1])
    location_red_x = float(location_red[0])
    location_red_y = float(location_red[1])

    vect_red_blue_x = location_blue_x - location_red_x
    vect_red_blue_y = location_blue_y - location_red_y
    vect_stand_x = 1
    vect_stand_y = 0

    print(location_blue, location_red, (vect_red_blue_x,vect_red_blue_y))
    # 求 cosθ
    cos_blue_red = (vect_red_blue_x*vect_stand_x+vect_red_blue_y*vect_stand_y)\
                   /(sqrt(vect_red_blue_x**2 + vect_red_blue_y**2)*sqrt(vect_stand_x**2 + vect_stand_y**2))
    azimuth = acos(cos_blue_red)

    # 求sinθ
    # sin_blue_red


    return azimuth,cos_blue_red


## 步长按照 0.5s 来计算各自的 步长距离
location_blue,step_blue,direction_blue = [0, 35],0.125,0
location_red_0,location_red_1 = [50, 50],[50, 20]
count = 300

list_location_red_0_x = []
list_location_red_0_y = []
list_location_red_1_x = []
list_location_red_1_y = []
list_location_blue_x = []
list_location_blue_y = []
while count:
    location_red_0 = getNextLocation(location_blue, location_red_0)
    location_red_1 = getNextLocation(location_blue, location_red_1)
    list_location_red_0_x.append(location_red_0[0])
    list_location_red_0_y.append(location_red_0[1])
    list_location_red_1_x.append(location_red_1[0])
    list_location_red_1_y.append(location_red_1[1])
    location_blue[0] = location_blue[0] + 0.125
    list_location_blue_x.append(location_blue[0])
    list_location_blue_y.append(location_blue[1])
    print(list_location_red_0_x[0],list_location_red_0_y[0])
    count -= 1

import matplotlib.pyplot as plt
import numpy as np

# list_location_red_1_x=[1,2,3,4,5,6,2,3,4,6,7,5,7]
# list_location_red_1_y=[2,3,4,5,8,9,2,1,3,4,5,2,4]
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.title('显示中文标题')
plt.xlabel("横坐标")
plt.ylabel("纵坐标")
# x=np.arange(0,len(list_location_red_1_x))+1
# x[0]=1
my_x_ticks = np.arange(0, 50, 1)
plt.xticks(my_x_ticks)
plt.plot(list_location_red_0_x,list_location_red_0_y)
plt.plot(list_location_red_1_x,list_location_red_1_y)
plt.plot(list_location_blue_x,list_location_blue_y)
plt.show()
# # 获得方位角
# azimuth_red_0 = getAzimuth(location_blue,location_red_0)
# azimuth_red_1 = getAzimuth(location_blue,location_red_1)
#
# # 打印方位角
# print(location_blue,location_red_0,azimuth_red_0)
# print(location_blue,location_red_1,azimuth_red_1)


# 通过向量求 sinθ
# v1 = (np.cross(np.array([-50,-15]),np.array([1,0])))
# v2 = (np.cross(np.array([-50,15]),np.array([1,0])))
# print(v1,v2)
# sin_ = v / (sqrt(50**2 + 15**2))
# print(asin(v1 / (sqrt(50**2 + 15**2))))
# print(asin(v2 / (sqrt(50**2 + 15**2))))
# print(v1 / (sqrt(50**2 + 15**2)))
# print(v2 / (sqrt(50**2 + 15**2)))







