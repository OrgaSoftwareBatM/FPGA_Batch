# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

@author: manip.batm
"""

from Stab_diag_Bermousque import StabilityDiagram


##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD1\\data1'
prefix = 'stab_'
Map = StabilityDiagram(folder,prefix)

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 1.  # integration time (fastseq divider)
Map.step_wait = 10.         # ms wait after every fastseq

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.2

### LEFT
Map.init_val['LD1'] = -0.885
Map.init_val['LD2'] = -0.85
Map.init_val['LV1'] = -1.4
Map.init_val['LV2'] = -1.4
Map.init_val['LH1'] = -1.0
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -0.85

### RIGHT
Map.init_val['RD1'] = -1.4
Map.init_val['RD2'] = -0.72
Map.init_val['RV1'] = -1.2
Map.init_val['RV2'] = -1.0
Map.init_val['RH1'] = -0.8
Map.init_val['RH2'] = -1.0
Map.init_val['RH3'] = -0.8

### CHANNEL
Map.init_val['TC'] = -1.2
Map.init_val['BC'] = -1.2

##########################
###	 MAP
##########################
Map.sweep_dim = [1001,1001]
#Map.ramp_DAC('RH3',-0.8,-1.4,0)
#Map.ramp_DAC('RH1',-0.8,-1.4,1)
##Map.ramp_DAC('RD1',-1.18,-1.00,1)
#Map.ramp_DAC('RD1',-1.4,-1.31,1)

Map.ramp_DAC('LH3',-0.85,-1.15,0)
Map.ramp_DAC('LD1',-0.875,-0.855,0)
Map.ramp_DAC('LH1',-0.6,-0.9,1)
Map.ramp_DAC('LD2',-0.85,-0.825,1)


#Map.add_wait('wait_bg',0,10000,1) # (index,ms,axis) wait n ms at index for given axis


Map.build_fastramp()
Map.update_timings()
Map.build_sweep()
Map.build_files()