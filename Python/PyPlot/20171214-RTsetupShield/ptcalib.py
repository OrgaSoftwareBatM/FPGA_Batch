# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

#R, Ttable = np.loadtxt('PT100.txt')
def Tpt(Rt):
    R0 = 100
    a = 0.00385
    T = (Rt/R0 - 1)/a
    return T