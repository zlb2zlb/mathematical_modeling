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
from math import acos,asin,sqrt,cos,sin,pi,atan
import math
import numpy as np
import matplotlib.pyplot as plt

## 根据无人机当前位置、步长、方位角，来获得下一时刻的位置
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


    return [azimuth,cos_blue_red]

## 根据蓝机、红机位置以及红机预测下一位置，蓝机选择下一个位置
def gamePosition(location_blue, location_blue_pre, location_red_0, location_red_0_next, location_red_1, location_red_1_next):
    ## 当前 蓝机 可以进行的左转、右转，旋转点
    rotLoc_list = getRotationLocation(location_blue, location_blue_pre)
    getAfterRotationLocation(location_blue=location_blue, rotaion_position=rotLoc_list[0], clockwise=True)## 右转之后到达的点
    getAfterRotationLocation(location_blue=location_blue, rotaion_position=rotLoc_list[1], clockwise=False)## 左转之后到达的点

## 获得蓝机位置点集合
def getPositions(location_red_0,location_red_1,location_blue,iterration_count=400):
    '''获得位置点集合'''
    list_location_red_0_x = []
    list_location_red_0_y = []
    list_location_red_1_x = []
    list_location_red_1_y = []
    list_location_blue_x = []
    list_location_blue_y = []
    count = 0
    while count<iterration_count:
        ## 红方集群位置点更新
        location_red_0_next = getNextLocation(location_blue, location_red_0)
        location_red_1_next = getNextLocation(location_blue, location_red_1)

        ## 蓝机位置更新
        location_blue[0] = location_blue[0] + 0.125
        # location_blue_pre =
        # location_blue_next = gamePosition(location_blue, location_blue_pre, location_red_0, location_red_0_next, location_red_1, location_red_1_next)
        ## 更新后位置进行记录
        list_location_red_0_x.append(location_red_0_next[0])
        list_location_red_0_y.append(location_red_0_next[1])
        list_location_red_1_x.append(location_red_1_next[0])
        list_location_red_1_y.append(location_red_1_next[1])
        list_location_blue_x.append(location_blue[0])
        list_location_blue_y.append(location_blue[1])

        print(list_location_red_0_x[0],list_location_red_0_y[0])
        count += 1

        location_red_0 = location_red_0_next
        location_red_1 = location_red_1_next

    return list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y

## 根据每个飞机的位置点，画出路线图
def drawGraph(list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y):
    '''根据每个飞机的位置点，画出路线图'''
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.title('显示中文标题')
    plt.xlabel("横坐标")
    plt.ylabel("纵坐标")
    my_x_ticks = np.arange(0, 50, 1)
    plt.xticks(my_x_ticks)
    print(list_location_red_0_x,list_location_red_0_y)
    plt.plot(list_location_red_0_x,list_location_red_0_y)
    plt.plot(list_location_red_1_x,list_location_red_1_y)
    plt.plot(list_location_blue_x,list_location_blue_y)
    plt.show()

## 根据蓝机当前位置、旋转点、旋转方向，将蓝机旋转到下一个目标点
def getAfterRotationLocation(location_blue,rotaion_position,step=0.125,R_blue=0.5,clockwise=False):
    '''根据蓝机当前位置、旋转点、旋转方向，将蓝机旋转到下一个目标点'''
    print(step)
    x1 = location_blue[0]
    y1 = location_blue[1]
    x2 = rotaion_position[0]
    y2 = rotaion_position[1]
    theta = step/R_blue  ## 求出弧度
    ## 求出下一个点的位置，默认逆时针旋转，也就是左转
    ## 当 旋转点 在运动方向的左边的时候，逆时针旋转
    ## 当 旋转点 在运动方向的右边的时候，顺时针旋转
    if clockwise:
        theta = - theta
    x = (x1 - x2) * cos(theta) - (y1 - y2) * sin(theta) + x2
    y = (y1 - y2) * cos(theta) + (x1 - x2) * sin(theta) + y2

    return [x, y]

## 获得旋转点，其中旋转点1是为顺时针旋转，旋转点2是为逆时针旋转
def getRotationLocation(location_blue_now,location_blue_pre,turning_radius=0.5):
    '''通过蓝方无人机前一时刻位置和当前位置，求出速度方向，得到斜率'''
    x_pre = location_blue_pre[0]  # 蓝方无人机前一时刻位置
    y_pre = location_blue_pre[1]
    x_now = location_blue_now[0] # 蓝方无人机当前位置
    y_now = location_blue_now[1]

    if (x_now - x_pre) > 0 and (y_now - y_pre) > 0:
        quadrant = 1
    elif (x_now - x_pre) < 0 and (y_now - y_pre) > 0:
        quadrant = 2
    elif (x_now - x_pre) < 0 and (y_now - y_pre) < 0:
        quadrant = 3
    elif (x_now - x_pre) > 0 and (y_now - y_pre) < 0:
        quadrant = 4
    else:
        if (x_now - x_pre) == 0:
            # 向量B'B在 y轴上
            if (y_now - y_pre) > 0:
                rotaion_position_1 = [x_now + turning_radius, 0]
                rotaion_position_2 = [x_now - turning_radius, 0]
            else:
                rotaion_position_1 = [x_now - turning_radius, 0]
                rotaion_position_2 = [x_now + turning_radius, 0]
            return [rotaion_position_1,rotaion_position_2]
        else:
            # 向量B'B在 x轴上
            if (x_now - x_pre) > 0:
                rotaion_position_1 = [0, y_now + turning_radius]
                rotaion_position_2 = [0, y_now - turning_radius]
            else:
                rotaion_position_1 = [0, y_now - turning_radius]
                rotaion_position_2 = [0, y_now + turning_radius]
            return [rotaion_position_1, rotaion_position_2]

    # 当前旋转的的角度
    radian = atan((y_now - y_pre) / (x_now - x_pre))
    if quadrant == 1 or quadrant == 3:
        rotaion_position_1 = [x_now + turning_radius * sin(radian),y_now - turning_radius * cos(radian)]
        rotaion_position_2 = [x_now - turning_radius * sin(radian),y_now + turning_radius * cos(radian)]
    elif quadrant == 2 or quadrant == 4:
        rotaion_position_1 = [x_now - turning_radius * sin(radian),y_now + turning_radius * cos(radian)]
        rotaion_position_2 = [x_now + turning_radius * sin(radian),y_now - turning_radius * cos(radian)]

    return [rotaion_position_1, rotaion_position_2]


## 步长按照 0.5s 来计算各自的 步长距离
location_blue,step_blue,direction_blue = [0, 35],0.125,0
location_red_0,location_red_1 = [50, 50],[50, 20]
#
list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y = getPositions(location_red_0,location_red_1,location_blue)

drawGraph(list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y)


# location_blue = [26, 2]
# location_blue_pre = [25, 1]
# rotLoc_list = getRotationLocation(location_blue, location_blue_pre)
# print(getAfterRotationLocation(location_blue=location_blue, rotaion_position=rotLoc_list[0], clockwise=True))
# print(getAfterRotationLocation(location_blue=location_blue, rotaion_position=rotLoc_list[1], clockwise=False))

# print(getAfterRotationLocation([0,0],[0,1],step=500*1/2*pi))



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







