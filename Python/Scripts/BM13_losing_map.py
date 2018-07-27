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
# folder = 'D:\\BaptisteData\\BM13\\CD2\\data2'
folder = 'C:\\Users\\manip.batm\\Documents\\GitKraken\\FPGA_Batch\\Python\\h5'
prefix = 'RT_losing'
Map = RT_fastseq(folder,prefix)
Map.use_AWG = True

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
Map.init_val['LD1'] = -0.715
Map.init_val['LD2'] = -0.830
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.8
Map.init_val['LH3'] = -0.6
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
Map.init_val['SAW_{delay}'] = 800.

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['LH3',-0.6])
Map.sequence.append(['LH2',0.])
Map.sequence.append(['Trigger','1011'])

Map.sequence.append(['RH1',0.])  # load 2 electrons
Map.sequence.append(['RH3',0.1])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.3])
Map.sequence.append(['RH1',-0.])

Map.sequence.append(['RP2',+0.])     # Meas
Map.sequence.append(['RH1',0.])  
Map.sequence.append(['RH3',-0.3])
Map.sequence.append(['RH2',-0.])
Map.sequence.append(['TC',0.])
Map.sequence.append(['BC',0.])
Map.sequence.append(['RV1',+0.])
Map.sequence.append(['RV2',-0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['RH2',0.])    # Metastable
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH3',-0.6])
Map.sequence.append(['Timing',1.])

Map.sequence.append(['RH3',-0.3])      # Meas
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['Trigger','1001'])
Map.sequence.append(['Jump',19])
# Map.sequence.append(['Jump',len(Map.sequence)])

##########################
###	 MAP
##########################
Map.sweep_dim = [80,51,51]
Map.init_val['RD1'] = -0.632
Map.init_val['RD2'] = -1.
#Map.ramp_slot(5,'dRH1_{load}',-0.2,0.,2)
#Map.ramp_slot(6,'dRH3_{load}',0.08,0.1,2)


#Map.ramp_slot(19,'dRH2_{meta}',-0.,-1.2,3)
Map.ramp_slot(20,'dRH1_{meta}',+0.6,-0.3,2)
Map.ramp_slot(21,'dRH3_{meta}',-0.6,0.3,1)

#Map.ramp_DAC('RD1',-0.6,-0.81,1)
#Map.ramp_DAC('RD2',-0.65,-1.1,2)
#Map.ramp_RF('SAW_{freq}',2.5,3.1,1)
#Map.ramp_RF('SAW_{power}',0.,25.,2)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()