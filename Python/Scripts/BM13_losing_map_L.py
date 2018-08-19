# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:48:45 2018

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
from QuickMap.QuickMap_RT import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data2'
#folder = 'C:\\Users\\manip.batm\\Documents\\GitKraken\\FPGA_Batch\\Python\\h5'
prefix = 'RT_losing'
Map = RT_fastseq(folder,prefix)
Map.use_AWG = False

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 0.2 # integration time (fastseq divider)
Map.step_wait = 0.       # ms wait after every fastseq

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
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.05
Map.init_val['SAW_{delay}'] = 0.1

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['Trigger','1011'])

Map.sequence.append(['LH3',0.27])
Map.sequence.append(['LH2',0.08])  # load 2 electrons
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',0.15])
Map.sequence.append(['LH2',0.1])

Map.sequence.append(['LP2',+0.])     # Meas
Map.sequence.append(['LH1',0.])  
Map.sequence.append(['LH3',0.])
Map.sequence.append(['LH2',0.1])
Map.sequence.append(['TC',0.])
Map.sequence.append(['BC',0.])
Map.sequence.append(['LV1',+0.])
Map.sequence.append(['LV2',-0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['LH2',-0.05])    # Metastable
Map.sequence.append(['LH1',0.])
Map.sequence.append(['LH3',0.3])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH3',0.])      # Meas
Map.sequence.append(['LH1',0.])
Map.sequence.append(['LH2',0.1])
Map.sequence.append(['Timing',4.])

#Map.sequence.append(['Trigger','1001'])
#Map.sequence.append(['Jump',19])
# Map.sequence.append(['Jump',len(Map.sequence)])

##########################
###	 MAP
##########################
Map.sweep_dim = [51,101,101,10]
Map.init_val['LD1'] = -0.705
Map.init_val['LD2'] = -0.801

Map.ramp_slot(18,'dLH1_{meta}',-0.,0.9,2)
#Map.ramp_slot(17,'dLH2_{meta}',0.15,-0.,2)
Map.ramp_slot(19,'dLH3_{meta}',0.,0.3,1)

#Map.ramp_DAC('LD1',-0.6,-1.05,1)
#Map.ramp_DAC('LD2',-0.6,-1.05,1)
#Map.ramp_RF('SAW_{freq}',2.5,3.1,1)
#Map.ramp_RF('SAW_{power}',0.,25.,2)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()