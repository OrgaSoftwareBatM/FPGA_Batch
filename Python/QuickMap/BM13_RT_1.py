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
Map.init_val['LD1'] = -0.
Map.init_val['LD2'] = -0.
Map.init_val['LV1'] = -1.3
Map.init_val['LV2'] = -1.5
Map.init_val['LH1'] = -1.
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -1.2

### RIGHT
Map.init_val['RD1'] = -1.21
Map.init_val['RD2'] = -0.55
Map.init_val['RV1'] = -1.2
Map.init_val['RV2'] = -1.3
Map.init_val['RH1'] = -1.
Map.init_val['RH2'] = -0.85
Map.init_val['RH3'] = -0.7

### CHANNEL
Map.init_val['TC'] = -1.5
Map.init_val['BC'] = -1.5

##########################
###	 FASTSEQ + CONF FILE   			
##########################
Map.initial_wait = 1    # ms before everything
Map.ms_per_point = 0.2     # integration time (RT_avg/ADC_freq)
Map.step_wait = 0        # ms wait after every fastseq

Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1])
Map.sequence.append(['Trigger','1000'])

Map.sequence.append(['LH2',0.])
Map.sequence.append(['LH3',0.3])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',-0.1])
Map.sequence.append(['LH2',0.2])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['LH2',0.])
Map.sequence.append(['LH3',0.3])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',-0.1])
Map.sequence.append(['LH2',0.2])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['LH2',0.])
Map.sequence.append(['LH3',0.3])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',-0.1])
Map.sequence.append(['LH2',0.2])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [76,201,2]
Map.ramp_slot(9,'Xload',0.,0.3,1)
Map.ramp_slot(10,'Yload',0.3,0.3,1)
Map.ramp_DAC('LD2',-1.022,-1.022,1)

Map.reconfig_ADC(sampling_rate=250e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()