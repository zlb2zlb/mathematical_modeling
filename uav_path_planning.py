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
import math,random
import numpy as np
import matplotlib.pyplot as plt

## 根据无人机当前位置、步长、方位角，来获得下一时刻的位置
import win32api

import win32con
count = 0
min_count = 100000

def getNextLocation(location_blue,location_red,step_red=0.05,location_red_another=None):
    '''根据无人机当前位置、步长、方位角，来获得下一时刻的位置'''
    location_blue_x = float(location_blue[0])
    location_blue_y = float(location_blue[1])
    location_red_x = float(location_red[0])
    location_red_y = float(location_red[1])

    distance = sqrt((location_blue_x - location_red_x)**2 + (location_blue_y - location_red_y)**2)
    delta_x = (location_blue_x - location_red_x) * (step_red / distance)
    delta_y = (location_blue_y - location_red_y) * (step_red / distance)
    location_red_x_next = location_red_x + delta_x
    location_red_y_next = location_red_y + delta_y

    ## 判断是否会撞机
    # if location_red_another:
    #     location_red_x_another = float(location_red_another[0])
    #     location_red_y_another = float(location_red_another[1])
    #     ## 如果会撞机，调整
    #     red2redDistance = sqrt((location_red_x_another - location_red_x)**2 + (location_red_y_another - location_red_y)**2)
    #     while red2redDistance<0.03:




    return [location_red_x_next,location_red_y_next]

## 计算收益
def getGain(location_blue, location_red_0, location_red_1):
    distance_b =  50 - location_blue[0]
    distance_br1 = sqrt((location_blue[0] - location_red_0[0])**2 + (location_blue[1] - location_red_0[1])**2)
    distance_br2 = sqrt((location_blue[0] - location_red_1[0])**2 + (location_blue[1] - location_red_1[1])**2)

    gain = 10/(distance_b) - (2 / (distance_br1 - 0.4)**3) - (2 / (distance_br2 - 0.4)**3)
    # print("{}----{}----{}----{}".format(distance_b, distance_br1, distance_br2,gain))
    return gain


## 根据蓝机、红机位置以及红机预测下一位置，蓝机选择下一个位置
def gamePosition(location_blue, location_blue_pre, location_red_0, location_red_0_next, location_red_1, location_red_1_next,board):
    ## 当前 蓝机 可以进行的左转、右转，旋转点
    # print(board)
    rotLoc_list = getRotationLocation(location_blue, location_blue_pre)
    location_rotLocR1 = getAfterRotationLocation(location_blue=location_blue, rotaion_position=rotLoc_list[0], step=0.0625, clockwise=True)## 右转之后到达的点
    location_rotLocR2 = getAfterRotationLocation(location_blue=location_blue, rotaion_position=rotLoc_list[1], step=0.0625, clockwise=False)## 左转之后到达的点
    location_forward = [location_blue[0] + (location_blue[0] - location_blue_pre[0]),location_blue[1] + (location_blue[1] - location_blue_pre[1])]
    loc_list = [location_rotLocR1,location_rotLocR2,location_forward]

    ## 如果超出区域边界或与红机距离小于0.3，则排除此位置
    # for loc in loc_list:
    #     if loc[1] > 70 or loc[1] < 0 :
    #         loc_list.remove(loc)

    ## 计算 收益
    # print("---------------------{}----{}----{}".format(location_rotLocR1, location_rotLocR2, location_forward))
    if location_rotLocR1[1]>board or location_rotLocR1[1]<0:
        gain_location_rotLocR1 = float('-inf')
    else:
        gain_location_rotLocR1 = getGain(location_rotLocR1,location_red_0_next,location_red_1_next)
    if location_rotLocR1[1]>board or location_rotLocR1[1]<0:
        gain_location_rotLocR2 = float('-inf')
    else:
        gain_location_rotLocR2 = getGain(location_rotLocR2, location_red_0_next, location_red_1_next)
    if location_forward[1]>board or location_forward[1]<0:
        gain_location_forward = float('-inf')
    else:
        gain_location_forward = getGain(location_forward, location_red_0_next, location_red_1_next)


    ## 根据收益选择最大的方案
    if gain_location_forward > gain_location_rotLocR1 and gain_location_forward > gain_location_rotLocR2:
        return location_forward
    elif gain_location_rotLocR1> gain_location_forward and gain_location_rotLocR1 > gain_location_rotLocR2:
        return  location_rotLocR1
    else:
        return location_rotLocR2


## 获得蓝机位置点集合
def getPositions(location_red_0,location_red_1,location_blue,iterration_count=400):
    '''获得位置点集合'''
    global count
    list_location_red_0_x = []
    list_location_red_0_y = []
    list_location_red_1_x = []
    list_location_red_1_y = []
    list_location_blue_x = []
    list_location_blue_y = []
    count = 0
    location_blue_pre = []
    ## 随机赋值
    location_blue_pre.append(location_blue[0] + random.uniform(-0.0625,0.0625))
    location_blue_pre.append(location_blue[1] + random.uniform(0.0,0.0625))
    while count<iterration_count:
        ## 红方集群位置点更新
        location_red_0_next = getNextLocation(location_blue, location_red_0)
        location_red_1_next = getNextLocation(location_blue, location_red_1)

        ## 蓝机位置更新
        # location_blue[0] = location_blue[0] + 0.0625

        location_blue_next = gamePosition(location_blue, location_blue_pre, location_red_0, location_red_0_next, location_red_1, location_red_1_next,board=17)

        ## 更新后位置进行记录
        list_location_red_0_x.append(location_red_0_next[0])
        list_location_red_0_y.append(location_red_0_next[1])
        list_location_red_1_x.append(location_red_1_next[0])
        list_location_red_1_y.append(location_red_1_next[1])
        list_location_blue_x.append(location_blue_next[0])
        list_location_blue_y.append(location_blue_next[1])

        # print(list_location_red_0_x[0],list_location_red_0_y[0])
        count += 1

        ## 更新位置
        location_red_0 = location_red_0_next
        location_red_1 = location_red_1_next
        location_blue_pre = location_blue
        location_blue = location_blue_next
        # print("{}".format(location_blue))
        ## 到达攻防目标区域后结束
        if location_blue[0] >= 50:
            break
    return list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y

## 根据每个飞机的位置点，画出路线图
def drawGraph(list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y,t):
    '''根据每个飞机的位置点，画出路线图'''
    global min_count,count
    ## 判断 若最终点未到达边界旁，则不再画图
    if list_location_blue_x[-1] < 30:
        return
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.title('蓝方突防，红方拦截')
    plt.xlabel("横坐标")
    plt.ylabel("纵坐标")
    my_x_ticks = np.arange(1, 51, 1)
    plt.xticks(my_x_ticks)
    print(len(list_location_red_0_x))
    # print(list_location_red_0_x,list_location_red_0_y)
    plt.plot(list_location_red_0_x,list_location_red_0_y,color='red')
    plt.plot(list_location_red_1_x,list_location_red_1_y,color='pink')
    plt.plot(list_location_blue_x,list_location_blue_y,color='blue')
    plt.text(0, -3, r'$t=%.2f$'%(t * 0.25))
    plt.show()

## 根据蓝机当前位置、旋转点、旋转方向，将蓝机旋转到下一个目标点
def getAfterRotationLocation(location_blue,rotaion_position,step=0.0625,R_blue=0.5,clockwise=False):
    '''根据蓝机当前位置、旋转点、旋转方向，将蓝机旋转到下一个目标点'''
    # print(step)
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


## 步长按照 0.25s 来计算各自的 步长距离
list_positions = []
location_blue,step_blue,direction_blue = [0, 0],0.0625,0
location_red_0,location_red_1 = [50, 0],[50, 0]

## 第一题，求蓝方无人机最优突防策略
for i in range(100):
    list_location_red_0_x,list_location_red_0_y,\
    list_location_red_1_x,list_location_red_1_y,\
    list_location_blue_x,list_location_blue_y = getPositions(location_red_0,location_red_1,location_blue,iterration_count=1440)
    if count<1440:
        drawGraph(list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y)
    count = 0
    drawGraph(list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y,t=count)


## 第二题，求最短时间策略
for i in range(1,38):
    location_blue,step_blue,direction_blue = [0, 0],0.0625,0
    location_red_0,location_red_1 = [50, 0],[50, 0]
    # list_positions = []
    print(location_blue)
    for i in range(100):
        list_location_red_0_x,list_location_red_0_y,\
        list_location_red_1_x,list_location_red_1_y,\
        list_location_blue_x,list_location_blue_y = getPositions(location_red_0,location_red_1,location_blue,iterration_count=1440)
        if min_count > count:
            list_positions=[list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y]
            min_count = count
        drawGraph(list_location_red_0_x,list_location_red_0_y,list_location_red_1_x,list_location_red_1_y,list_location_blue_x,list_location_blue_y,t=count)
drawGraph(list_positions[0],list_positions[1],list_positions[2],list_positions[3],list_positions[4],list_positions[5],t=min_count)







