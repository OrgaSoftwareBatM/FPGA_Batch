# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:38:49 2018

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from configobj import ConfigObj
import MeasurementBase.measurement_classes as mc

# Import parameters
config_file = ConfigObj('..\\Fridge_settings.ini')
addr_dict = config_file['Instruments']

recording_time_list = ['100ns','200ns','500ns','1us','2us','5us','10us','20us','50us','100us','200us','500us','1ms','2ms','5ms','10ms','20ms','50ms','100ms','200ms','500ms','1s']
mem_size_list = [500,1000,2500,5000,10000,25000,50000,100000,250000,500000,1000000,2500000,5000000,10000000,25000000]

def LeCroy_config():
    ##########################
    ### leCroy 6Zi
    ##########################
    Scope = mc.LeCroy(name='LeCroy',
                 Adress=addr_dict['LeCroy'],
                 NameList='V_{scope,0}',
                 UnitList='V',
                 SourceList='8', #[C1,C2,C3,C4,M1,M2,M3,M4,F1,F2,F3,F4,F5,F6,F7,F8,OTHER]
                 ConversionList='1.0',
                 NChannels=1,
                 RecordingTime=recording_time_list.index('200us'),
                 MemorySize=mem_size_list.index(10000), 
                 SegmentMode=1,
                 NSegment=101,
                 NStep=1)

    return Scope

