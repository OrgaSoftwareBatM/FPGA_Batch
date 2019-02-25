# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:48:45 2018

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
prefix = 'RT_spin_transfer'
Map = RT_fastseq(folder,prefix)
Map.use_AWG = True

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
Map.init_val['RF0_{power}'] = 15.
Map.init_val['RF1_{freq}'] = 0.1382
Map.init_val['RF1_{power}'] = 12.
### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = +25.
Map.init_val['SAW_{width}'] = 0.150
Map.init_val['SAW_{delay}'] = 1.1

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1110'])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','1010'])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH2',-0.05])  # LOAD LEFT
Map.sequence.append(['LH3',0.29])
Map.sequence.append(['LH2',-0.05])
#Map.sequence.append(['LH2',0.07])
Map.sequence.append(['LH3',-0.3])

Map.sequence.append(['RH2',-0.1])   # LOAD RIGHT
Map.sequence.append(['RH3',0.12])
#Map.sequence.append(['RH2',-0.05])
Map.sequence.append(['RH2',-0.02])
Map.sequence.append(['RH3',-0.15])

Map.sequence.append(['LH2',0.])    # RECEIVING POS LEFT
Map.sequence.append(['LH1',0.5])
Map.sequence.append(['LH2',+0.2])
Map.sequence.append(['LH3',-0.3])

Map.sequence.append(['RH2',0.3])    # MIXING POS RIGHT
Map.sequence.append(['RH3',-0.65])
Map.sequence.append(['RH1',0.05])
Map.sequence.append(['RH2',0.])

Map.sequence.append(['Trigger','1000']) # MIX R
Map.sequence.append(['Timing',0.02])
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['RH1',0.2])  # SENDING POS
Map.sequence.append(['Trigger','1000']) # SEND
Map.sequence.append(['Timing',0.02])
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['LH2',0.02])
Map.sequence.append(['LH3',0.12])
Map.sequence.append(['Trigger','1000']) # MIX L
Map.sequence.append(['Timing',0.02])
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['LH3',-0.3])   # BACK LEFT
Map.sequence.append(['LH2',0.0])

Map.sequence.append(['RH2',0.3])   # BACK RIGHT
Map.sequence.append(['RH3',-0.15])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.])

Map.sequence.append(['Trigger','1011']) # CHARGE SENSING
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['LH2',-0.3])
Map.sequence.append(['LH3',0.15]) # TUNNEL SELECTIVE L
Map.sequence.append(['LH3',-0.3])
Map.sequence.append(['LH2',0.0])

Map.sequence.append(['RH2',-0.36]) # TUNNEL SELECTIVE R
Map.sequence.append(['RH2',0.])

#Map.sequence.append(['RH2',-0.]) # DUMMY (CHARGE) R
#Map.sequence.append(['RH2',0.])

Map.sequence.append(['Trigger','1011']) # CHARGE SENSING
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['Trigger','1010'])
Map.sequence.append(['LH1',0.])
 
Map.sequence.append(['Jump',4])
#Map.sequence.append(['Jump',len(Map.sequence)])

#Map.sweep_dim = [12000,10]
#Map.sweep_dim = [101,200]
Map.sweep_dim = [49,2,20000]
#Map.sweep_dim = [20,201,2]
#Map.sweep_dim = [145,20,2,100]
Map.init_val['LD1'] = -0.731
Map.init_val['LD2'] = -0.829
Map.init_val['RD1'] = -0.7
Map.init_val['RD2'] = -1.04

#Map.segment_param = [71.824, 64, 17]
#Map.segment_param = [75.051, 68, 17]
Map.segment_param = [100.906, 60, 17, 32, 17]
#Map.segment_param = [152.234, 49, 47]
#Map.segment_param = [89.871, 49, 47]
#Map.segment_param = [94.087, 54, 17]
#Map.segment_param = [94.095, 86, 17]

#Map.ramp_slot(6,'dLH2_{load}',-0.05,0.07,1)
#Map.ramp_slot(6,'dLH2_{load}',-0.1,0.2,1)

#Map.ramp_slot(9,'dRH3_{load}',0.06,0.15,3)
#Map.ramp_slot(10,'dRH2_{load}',-0.12,0.06,2)

#Map.ramp_slot(16,'dRH2_{crossing}',0.,0.3,1)

#Map.ramp_slot(13,'dLH1_{wait}',0.3,0.75,2)
#Map.ramp_slot(14,'dLH2_{wait}',-0.45,+0.3,2)
#Map.ramp_slot(15,'dLH3_{wait}',-0.45,+0.3,1)
#Map.ramp_slot(19,'dBC_{wait}',-0.3,0.3,2)

#Map.ramp_slot(18,'dRH1_{wait}',-0.1,-0.1,1)
#Map.ramp_slot(18,'dRH1_{wait}',-0.3,0.6,3)
#Map.ramp_slot(20,'dRH2_{wait}',0.3,-0.3,2)
#Map.ramp_slot(17,'dRH3_{wait}',-0.15,-0.75,4)
#
#Map.ramp_slot(20,'dRH1_{mixing}',-0.15,0.15,2)
#Map.ramp_slot(20,'dRH1_{mixing}',0.,-0.05,1)
#Map.ramp_slot(18,'dRH1_{sending}',-0.3,0.6,2)
#Map.ramp_slot(21,'dRH1_{sending}',-0.3,0.3,1)
#Map.ramp_slot(22,'dRH1_{sending}',-0.3,0.3,1)
#Map.ramp_slot(23,'dRH1_{sending}',0.15,0.3,1)

#Map.ramp_slot(27,'dLH2_{mixing}',0.02,-0.15,1)

#Map.ramp_slot(25,'dLH2_{read}',0.03,0.09,2)
#Map.ramp_slot(45,'dRH2_{read}',-0.3,-0.45,2)

#Map.ramp_DAC('LD1',-0.6,-0.75,2)
#Map.ramp_DAC('LD2',-0.75,-0.9,1)

#Map.ramp_DAC('RD1',-0.65,-0.8,1)
#Map.ramp_DAC('RD2',-0.85,-1.15,1)

#Map.ramp_RF('SAW_{freq}',2.76,2.82,1)
#Map.ramp_RF('SAW_{power}',25.,20.,2)
#Map.ramp_RF('SAW_{width}',0.03,0.13,2)

#Map.ramp_Bfield('B_Z',0.0045,-0.06,2)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()
