# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:48:45 2018

@author: manip.batm
"""

from RT_fastseq_Bermousque import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD1\\data1'
prefix = 'RT_'
Map = RT_fastseq(folder,prefix)

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.2
Map.init_val['Rbias'] = 0.2

### LEFT
Map.init_val['LD1'] = -0.55
Map.init_val['LD2'] = -1.04
Map.init_val['LV1'] = -1.15
Map.init_val['LV2'] = -1.25
Map.init_val['LH1'] = -1.3
Map.init_val['LH2'] = -0.8
Map.init_val['LH3'] = -1.35

### RIGHT
Map.init_val['RD1'] = -0.55
Map.init_val['RD2'] = -1.1
Map.init_val['RV1'] = -1.15
Map.init_val['RV2'] = -1.2
Map.init_val['RH1'] = -1.3
Map.init_val['RH2'] = -0.8
Map.init_val['RH3'] = -1.35

### CHANNEL
Map.init_val['TC'] = -1.45
Map.init_val['BC'] = -1.45

##########################
###	 FASTSEQ + CONF FILE   			
##########################
Map.initial_wait = 1    # ms before everything
Map.ms_per_point = 0.2     # integration time (RT_avg/ADC_freq)
Map.step_wait = 0        # ms wait after every fastseq

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1])

Map.sequence.append(['RH2',0.175])  # load 2 electrons
Map.sequence.append(['RH3',0.35])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.35])
Map.sequence.append(['RH2',0.1])

Map.sequence.append(['BC',0.1])
Map.sequence.append(['TC',0.])
Map.sequence.append(['RV1',-0.1])
Map.sequence.append(['RV2',0.1]) #10
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.125])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.1])
Map.sequence.append(['Timing',5.])

Map.sequence.append(['Trigger','1000'])
Map.sequence.append(['RH3',-0.35])
Map.sequence.append(['Timing',1.])

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [5,201,151]
#Map.ramp_slot(9,'BC_{meta}',0.3,-0.3,1)
#Map.ramp_slot(10,'RV1_{meta}',0.05,0.05,2)
#Map.ramp_slot(11,'RH2_{meta}',-0.1,0.2,2)
#Map.ramp_slot(12,'RH3_{meta}',-0.35,-0.35,1)
Map.ramp_slot(14,'RH3_{meta}',-0.2,0.1,1)
Map.ramp_slot(15,'t_{meta}',0.01,10,2)
Map.ramp_DAC('RD2',-1.12,-1.12,2)

Map.reconfig_ADC(sampling_rate=250e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()