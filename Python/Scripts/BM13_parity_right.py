# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:14:47 2019

@author: manip.batm
"""

import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
from QuickMap.QuickMap_RT_SegmentMode import RT_fastseq
#from QuickMap.QuickMap_RT import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data2'
prefix = 'RT_parity_right'
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
Map.init_val['LP2'] = -0.85
### RIGHT
Map.init_val['RD1'] = -0.763
Map.init_val['RD2'] = -1.
Map.init_val['RV1'] = -1.6
Map.init_val['RV2'] = -1.0
Map.init_val['RH1'] = -1.75
Map.init_val['RH2'] = -0.7
Map.init_val['RH3'] = -1.
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

Map.sequence.append(['Trigger','1110'])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','1010'])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['RH2',-0.1])   # LOAD RIGHT
Map.sequence.append(['RH3',0.12])
#Map.sequence.append(['RH2',-0.1])
Map.sequence.append(['RH2',-0.02])
Map.sequence.append(['RH3',-0.15])

#Map.sequence.append(['RH2',+0.3])    # MIXING POS RIGHT
#Map.sequence.append(['RH1',+0.45])
#Map.sequence.append(['RH3',-0.15])    #Baptiste
#Map.sequence.append(['RH2',0.102])

Map.sequence.append(['RH2',-0.02])    # MIXING POS RIGHT
Map.sequence.append(['RH3',-0.35])    #Baptiste
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',-0.02])

Map.sequence.append(['Trigger','1000']) # MIX R
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['RH2',0.3])
Map.sequence.append(['RH1',+0.])
Map.sequence.append(['RH2',-0.039])

Map.sequence.append(['Trigger','1010']) # DECAY
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['Timing',0.02])

Map.sequence.append(['RH2',+0.3])   # BACK RIGHT
Map.sequence.append(['RH3',-0.15])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.])

#Map.sequence.append(['RH2',-0.36]) # TUNNEL SELECTIVE R
#Map.sequence.append(['RH2',-0.345]) # TUNNEL SELECTIVE R
Map.sequence.append(['RH2',0]) # TUNNEL SELECTIVE R
Map.sequence.append(['RH2',0.])

Map.sequence.append(['Trigger','1011']) # CHARGE SENSING
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['Jump',4])


#Map.sweep_dim = [100,51,200]
#Map.sweep_dim = [50,201,13,4]
#Map.sweep_dim = [12000,10]
Map.sweep_dim = [200,101,200]

Map.init_val['LD1'] = -0.702
Map.init_val['LD2'] = -0.822
Map.init_val['RD1'] = -0.7
Map.init_val['RD2'] = -1.0

Map.segment_param = [50.991,42,18]

#Map.ramp_slot(15,'dRH2_{read}',0.3,0.4,2)
#Map.ramp_Bfield('B_Z',0.015,+0.150,3)

#Map.ramp_slot(5,'dRH3_{load}',0.06,0.15,2)
Map.ramp_slot(4,'dRH2_{load}',-0.12,0.06,1)

# SYMMETRIC
#Map.ramp_slot(9,'dRH1_{wait}',-0.1,0.65,1)
#Map.ramp_slot(10,'dRH3_{wait}',-0.75,0.,1)

# DETUNING
#Map.ramp_slot(9,'dRH1_{wait}',0.05,0.35,2)
#Map.ramp_slot(10,'dRH3_{wait}',-0.3,-0.6,2)


#Map.ramp_slot(15,'dRH1_{wait}',0.5,0.38,1)
#Map.ramp_slot(16,'dRH2_{wait}',0.,0.24,1)


ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()