# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:48:45 2018

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
from QuickMap.QuickMap_RT_Scope import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data2'
#folder = 'C:\\Users\\manip.batm\\Documents\\GitKraken\\FPGA_Batch\\Python\\h5'
prefix = 'RT_spin_scope'
Map = RT_fastseq(folder,prefix)
Map.use_AWG = True

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
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.05
Map.init_val['SAW_{delay}'] = 0.1

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',0.1])

for i in range(100):
    Map.sequence.append(['Trigger','1010'])
    Map.sequence.append(['LH3',0.29])  # Unload
    Map.sequence.append(['LH2',0.07])  # load 2 electrons
    Map.sequence.append(['LH3',-0.05])
    Map.sequence.append(['LH2',-0.05])
    Map.sequence.append(['LH1',0.5])
    #Map.sequence.append(['LH3',0.10])
    #Map.sequence.append(['Timing',0.1])  # decay (with T+)
    
    Map.sequence.append(['LH3',0.15])
    #Map.sequence.append(['LH1',0.5])
    Map.sequence.append(['Timing',0.1]) # Manip
    Map.sequence.append(['Trigger','1000'])
    #Map.sequence.append(['LH1',0.5])
    Map.sequence.append(['LH3',-0.05])
    
    Map.sequence.append(['LH1',0.])
    Map.sequence.append(['LH2',0.084]) # reservoir
    Map.sequence.append(['LH3',0.22])
    Map.sequence.append(['Timing',0.1])
    
    Map.sequence.append(['LH3',0.15]) # read
    Map.sequence.append(['LH2',0.1])
    Map.sequence.append(['Trigger','1001'])
    Map.sequence.append(['Timing',0.2])

#Map.sequence.append(['Jump',2])
#Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['Jump',len(Map.sequence)])

##########################
###	 MAP
##########################
Map.sweep_dim = [100,500]
#Map.sweep_dim = [1000,5000]
Map.init_val['LD1'] = -0.707
Map.init_val['LD2'] = -0.83

#Map.ramp_slot(4,'dLH3_{load}',0.22,0.25,2)
#Map.ramp_slot(4,'dLH2_{load}',0.0,0.07,2)
#Map.ramp_slot(5,'t_{load}',0.1,10.,2,method='log10')
#
#Map.ramp_slot(8,'dLH3_{wait}',-0.05,0.14,2)
#Map.ramp_slot(8,'dLH2_{wait}',-0.15,0.15,1)
#Map.ramp_slot(9,'t_{wait}',0.1,10.,2,method='log10')
#Map.ramp_slot(9,'t_{wait}',8.,8.,1)

Map.ramp_slot(1,'t_{dummy}',0.1,0.1,1)
#
#Map.ramp_slot(8,'dLH3_{AWG}',0.15,0.21,2)

#Map.ramp_slot(10,'dLH3_{read}',0.22,0.22,2)
#Map.ramp_slot(13,'dLH2_{read}',0.,0.12,1)

#Map.ramp_DAC('LD1',-0.6,-0.75,1)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()