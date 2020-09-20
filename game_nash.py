#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/9/18 10:32
# @Author  : zlb
# @Email   : 15967924690@163.com
# @File    : game_nash.py
# @Software: PyCharm

import nashpy as nash

A = [[1, 2], [3, 0]]
B = [[0, 2], [3, 1]]

game = nash.Game(A, B)

for eq in game.support_enumeration():
    print(eq)

print(game[[0, 1], [1, 0]])

