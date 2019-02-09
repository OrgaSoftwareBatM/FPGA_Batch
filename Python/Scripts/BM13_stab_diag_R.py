# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
from QuickMap.QuickMap_ramp import StabilityDiagram

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data2'
#folder = 'C:\\Users\\manip.batm\\Documents\\GitKraken\\FPGA_Batch\\Python\\h5'
prefix = 'stab'
Map = StabilityDiagram(folder,prefix)

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 0.05 # integration time (fastseq divider)
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
Map.init_val['SAW_{power}'] = -60.
Map.init_val['SAW_{width}'] = 0.05
Map.init_val['SAW_{delay}'] = 0.1

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',0])
Map.sequence.append(['Trigger','0011'])


Map.sequence.append(['RH2',-0.1])   # LOAD RIGHT
Map.sequence.append(['RH3',0.12])
#Map.sequence.append(['RH2',-0.025]) # 2
Map.sequence.append(['RH2',+0.06]) # 4
Map.sequence.append(['RH3',-0.3])
Map.sequence.append(['RH2',0.3])
Map.sequence.append(['RH1',0.3])
Map.sequence.append(['RH3',-0.8])
Map.sequence.append(['RH2',0.])

##########################
###	 MAP
##########################

Map.sweep_dim = [801,401]
Map.init_val['LD1'] = -0.731
Map.init_val['LD2'] = -0.829
Map.init_val['RD1'] = -0.6
Map.init_val['RD2'] = -1.025



#Map.ramp_DAC('RH3',-0.7,-1.,0,init_at=-1.0)
#Map.ramp_DAC('RH3',-0.9,-0.75,0,init_at=-1.0)
#Map.ramp_DAC('RH3',-1.3,-1.9,0,init_at=-1.0)
#Map.ramp_DAC('RH1',-1.45,-2.05,0,init_at=-1.75)
#Map.ramp_DAC('RH2',-1.,-0.4,0,init_at=-0.7)
#Map.ramp_DAC('RH1',-1.9,-1.,1)


#Map.ramp_DAC('RD1',-0.7,-0.85,1)
#Map.ramp_DAC('RD2',-1.07,-1.03,1)

#Map.ramp_slot(3,'dRH1_{load}',-0.15,0.15,1)
#Map.ramp_slot(3,'dRH1',0.365,0.395,1)
Map.ramp_slot(6,'dRH3',-0.3,-0.9,1)
#Map.ramp_slot(7,'dRH2',-0.3,0.3,1)
#Map.ramp_slot(8,'dRH1',-0.3,0.6,1)


#Map.ramp_DAC('RD1',-0.55,-1.1,1)
Map.ramp_DAC('RD2',-0.55,-1.1,0)

#Map.ramp_DAC('RD1',-0.75,-0.68,1)
#Map.ramp_DAC('RD2',-0.97,-0.92,1)

#Map.ramp_RF('RF0_{freq}',0.195,0.210,1)
#Map.ramp_RF('RF0_{power}',15.,0.,1)
#Map.ramp_RF('RF1_{freq}',0.120,0.145,1)
#Map.ramp_RF('RF1_{power}',0.,0.2,2)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()