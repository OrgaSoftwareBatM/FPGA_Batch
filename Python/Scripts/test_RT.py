# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:35:38 2019

@author: manip.batm
"""


import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
#from QuickMap.QuickMap_RT_SegmentMode import RT_fastseq
from QuickMap.QuickMap_RT import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD3\\data1'
prefix = 'test_RT'
Map = RT_fastseq(folder,prefix)
Map.use_AWG = False
##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 1.   # ms before everything
Map.ms_per_point = 0.01 # integration time (RT_avg/ADC_freq)
Map.step_wait = 0.      # ms wait after every fastseq

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.
### LEFT
Map.init_val['LD1'] = -0.705
Map.init_val['LD2'] = -0.82
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.9
Map.init_val['LH2'] = -0.75
Map.init_val['LH3'] = -0.9
Map.init_val['LP1'] = -0.85
Map.init_val['LP2'] = -0.85
### RIGHT
Map.init_val['RD1'] = -0.763
Map.init_val['RD2'] = -1.
Map.init_val['RV1'] = -1.6
Map.init_val['RV2'] = -1.0
Map.init_val['RH1'] = -1.75
Map.init_val['RH2'] = -0.7
Map.init_val['RH3'] = -1.
Map.init_val['RP1'] = -0.85
Map.init_val['RP2'] = -0.85
### CHANNEL
Map.init_val['TC'] = -1.
Map.init_val['BC'] = -1.
### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2028
Map.init_val['RF0_{power}'] = -60
Map.init_val['RF1_{freq}'] = 0.1382
Map.init_val['RF1_{power}'] = -60
### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = -60.
Map.init_val['SAW_{width}'] = 0.150
Map.init_val['SAW_{delay}'] = 1.1

##########################
###	 FASTSEQ 			
##########################

Map.sequence.append(['Trigger out',[],'1111111111'])
Map.sequence.append(['Timing','1us',10])
Map.sequence.append(['Trigger out',[],'1110111111'])
Map.sequence.append(['Trigger in','1000000000','0000000000'])
Map.sequence.append(['Trigger out',[],'0000000000'])
Map.sequence.append(['Timing','1us',10])

Map.sequence.append(['Jump',1000,0])
Map.sequence.append(['End',[],[]])


Map.sweep_dim = [10000,2000]
#Map.sweep_dim = [50,201,13,4]
#Map.sweep_dim = [12000,10]

Map.segment_param = [46.093,38,17]

#Map.ramp_slot(15,'dRH2_{read}',0.3,0.4,2)
#Map.ramp_Bfield('B_Z',0.015,+0.035,2)

#Map.ramp_slot(5,'dRH3_{load}',0.06,0.15,2)
#Map.ramp_slot(4,'dRH2_{load}',-0.12,0.06,1)

# SYMMETRIC
#Map.ramp_slot(9,'dRH1_{wait}',-0.1,0.65,1)
#Map.ramp_slot(10,'dRH3_{wait}',-0.75,0.,1)

# DETUNING
#Map.ramp_slot(9,'dRH1_{wait}',0.05,0.35,2)
#Map.ramp_slot(10,'dRH3_{wait}',-0.3,-0.6,2)


#Map.ramp_slot(9,'dRH1_{wait}',0.42,0.4,1)
#Map.ramp_slot(11,'dRH2_{wait}',0.15,0.2,1)


ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()