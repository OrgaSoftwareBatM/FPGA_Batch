# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 17:12:44 2016

@author: shintaro
"""

import numpy as np

def array2rampSequence(array=np.zeros((2,301))):
    asize = array.shape[1]+2
    ramp_array = np.zeros((2,asize),dtype=np.double)
    ramp_array[:,0]=[101,0] #Lower all the trigger
    ramp_array[:,1:asize-1]=array[:,:]
    ramp_array[:,asize-1] = [103,asize-1] # Jump to own
    
    return ramp_array
    
def createRamp(points=301,
               fast_channels=[0],
               initial=[0],
               final=[-0.3],
               ):
    no_channels = len(fast_channels)
    seq_size = no_channels*points
    if seq_size > 4094:
        print('Sequence size exceeds maximum')
        
    array = np.zeros((2,seq_size),dtype=np.double)
    for i, channel in enumerate(fast_channels):
        array[0,i:seq_size-no_channels+1+i:no_channels]=channel
        array[1,i:seq_size-no_channels+1+i:no_channels]=np.linspace(initial[i],final[i],num=points,dtype=np.double)
        
    rarray = array2rampSequence(array=array)
    
    return rarray
    
def addDefaultPartOfFastSeq(array=np.zeros((2,20))):
    asize = array.shape[1]+5
    farray = np.zeros((2,asize),dtype=np.double)
    farray[:,0]=[101, 15] # Higher trigger 1 ~ 4
    farray[:,1]=[102, 1] # wait 1 ms
    farray[:,2]=[101, 0] # Lower all the trigger
    farray[:,3]=[102, 1] # wait 1ms
    farray[:,4:asize-1] = array[:,:]
    farray[:,asize-1]=[103,asize-1]
    
    return farray

if __name__=='__main__':
#    print createRamp()[1,1000:]
    pass