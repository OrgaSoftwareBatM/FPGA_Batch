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
#folder = 'C:\\Users\\manip.batm\\Documents\\GitKraken\\FPGA_Batch\\Python\\h5'
prefix = 'RT_spin_segment'
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
Map.init_val['SAW_{power}'] = -60.
Map.init_val['SAW_{width}'] = 0.1
Map.init_val['SAW_{delay}'] = 5.1

##########################
###	 FAST SEQUENCE	
##########################
Map.sequence.append(['Trigger','1110'])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','1010'])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['RH2',-0.1])   # LOAD SINGLET
Map.sequence.append(['RH3',0.12])
#Map.sequence.append(['RH2',-0.1])   # 0e
Map.sequence.append(['RH2',-0.02])  # 2e
#Map.sequence.append(['RH2',+0.025])  # 4e
Map.sequence.append(['RH3',-0.15])

Map.sequence.append(['RH2',0.3])    # WORMHOLE
Map.sequence.append(['RH1',0.2])

#Map.sequence.append(['RH2',0.])    # NOT WORMHOLE
#Map.sequence.append(['RH1',-0.15])

Map.sequence.append(['RH3',-0.3])
Map.sequence.append(['Trigger','1000']) # AWG
Map.sequence.append(['RH2',+0.0])

Map.sequence.append(['RH2',0.3])    # WORMHOLE
Map.sequence.append(['RH1',0.45])

#Map.sequence.append(['RH2',0.])    # NOT WORMHOLE
#Map.sequence.append(['RH1',-0.15])

Map.sequence.append(['RH3',-0.15])
Map.sequence.append(['RH1',0.])

Map.sequence.append(['RH2',-0.35]) # TUNNEL SELECTIVE
#Map.sequence.append(['RH2',-0.15]) # TUNNEL SELECTIVE
#Map.sequence.append(['RH2',-0]) # TUNNEL SELECTIVE
Map.sequence.append(['RH2',0.])

Map.sequence.append(['RH3',-0.15]) # CHARGE SENSING
Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['Trigger','1010'])
Map.sequence.append(['Jump',4])

##########################
###	 MAP
##########################
#Map.sweep_dim = [12000,10]
Map.sweep_dim = [29,13,1000]
#Map.sweep_dim = [101,5000]
Map.init_val['LD1'] = -0.731
Map.init_val['LD2'] = -0.829
Map.init_val['RD1'] = -0.7
Map.init_val['RD2'] = -1.0

#Map.segment_param = [47.063, 40, 17]
Map.segment_param = [45.450, 37, 17]
#Map.segment_param = [48.682, 40, 17]

#Map.ramp_slot(5,'dRH3_{load}',0.22,0.25,2)
#Map.ramp_slot(6,'dRH2_{load}',-0.1,0.05,1)

#Map.ramp_slot(8,'dRH2_{crossing}',0.,0.3,1)

#Map.ramp_slot(13,'dRH1_{wait}',-0.15,0.6,1)
#Map.ramp_slot(12,'dRH2_{wait}',0.3,-0.3,1)
#Map.ramp_slot(10,'dRH3_{wait}',-0.15,-0.45,2)
#

#Map.ramp_slot(10,'dRH1_{wait}',-0.3,0.,1)

#Map.ramp_slot(18,'dRH2_{spin2charge}',-0.19,-0.1,2)
#Map.ramp_slot(15,'dRH3_{spin2charge}',-0.35,0.1,3)

#Map.ramp_DAC('RD1',-0.65,-0.95,1)
#Map.ramp_DAC('RD2',-0.65,-0.8,1)

#Map.ramp_RF('SAW_{freq}',2.6,3.,1)
#Map.ramp_RF('SAW_{power}',-15,10.,1)
#Map.ramp_RF('SAW_{width}',0.03,0.13,2)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()