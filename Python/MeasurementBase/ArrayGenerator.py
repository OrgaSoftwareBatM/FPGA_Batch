# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:52:59 2016

@author: shintaro
"""
import numpy as np

"""------------------------------
Define different sweep modes
---------------------------------"""
# sweep type
sweeptype = ['Linear','1/x','log10','1_pos']
# Linear: equal space in linear between initial and final, Standard sweep
# 1/x: equal space in 1/x between initial and final, This is useful for Schubnikov de haas measurement.
# log10: equal space in log10 between initial and final , Just implemented but not sure it is useful or not.
# 1_pos: Insert single value to 1 point of certain dimension, This is useful to insert AWG event, trigger or custom wait time during the measurement

def ArrayGenerator(dims = [101], axis=0, initial = -0.1, final = -0.2, method = 'Linear'):
    if not method in sweeptype:
        method = 'Linear'
        
    if method == 'Linear':
        array = np.moveaxis(np.ones(tuple(dims), dtype=np.float), axis, -1)
        array *= np.linspace(initial, final, num=dims[axis], dtype=np.float)
        array = np.moveaxis(array, -1, axis)
    elif method == '1/x':
        array = np.moveaxis(np.ones(tuple(dims), dtype=np.float), axis, -1)
        array *= np.reciprocal(np.linspace(1/initial,1/final,num=dims[axis],dtype=np.float))
        array = np.moveaxis(array, -1, axis)
    elif method == 'log10':
        array = np.moveaxis(np.ones(tuple(dims), dtype=np.float), axis, -1)
        array *= np.power(10, np.linspace(np.log10(initial),np.log10(final),num=dims[axis],dtype=np.float))
        array = np.moveaxis(array, -1, axis)
    elif method == '1_pos':
        """ initial specify the position in the product up to axis, final specifies the value to be inserted """
        array = np.zeros(tuple(dims), dtype=np.float)
        repetition = np.prod(np.array(dims[0:axis+1]))
        if initial == -1:
            initial = repetition -1
        sl = np.array(range(0, array.size, repetition), dtype=np.int) + initial
        array = array.reshape(-1, order='F')
        array[sl.astype(np.int)]=final
        array = array.reshape(tuple(dims), order='F')
    return array