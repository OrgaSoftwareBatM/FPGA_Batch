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
prefix = 'RT_losing_'
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
Map.init_val['LV1'] = -1.3
Map.init_val['LV2'] = -1.4
Map.init_val['LH1'] = -1.2
Map.init_val['LH2'] = -0.8
Map.init_val['LH3'] = -1.35

### RIGHT
Map.init_val['RD1'] = -1.095
Map.init_val['RD2'] = -0.758
Map.init_val['RV1'] = -1.3
Map.init_val['RV2'] = -1.4
Map.init_val['RH1'] = -1.2
Map.init_val['RH2'] = -0.65
Map.init_val['RH3'] = -1.3

### CHANNEL
Map.init_val['TC'] = -1.35
Map.init_val['BC'] = -1.35

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2012
Map.init_val['RF0_{power}'] = -30.
Map.init_val['RF1_{freq}'] = 0.142
Map.init_val['RF1_{power}'] = -30.

### RS
Map.init_val['SAW_{freq}'] = 2.641
Map.init_val['SAW_{power}'] = 25.
Map.init_val['SAW_{width}'] = 0.1


##########################
###	 TIMINGS			
##########################
Map.initial_wait = 1    # ms before everything
Map.ms_per_point = 0.2     # integration time (RT_avg/ADC_freq)
Map.step_wait = 0        # ms wait after every fastseq

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1])
Map.sequence.append(['Trigger','1100'])

Map.sequence.append(['RH2',0.02])  # load 2 electrons
Map.sequence.append(['RH3',0.5])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.25])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['BC',-0.1])
Map.sequence.append(['TC',-0.1])
Map.sequence.append(['RV1',0.])
Map.sequence.append(['RV2',+0.1])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['Timing',4.])  # Meas

Map.sequence.append(['RH2',-0.25])  # Metastable
Map.sequence.append(['RH1',-0.1])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['Timing',4.])  # Meas

Map.sequence.append(['RH2',-0.22])  # SAW
Map.sequence.append(['RH1',-0.2])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','1000'])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['Timing',4.])  # Meas

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [80,201,201]
Map.ramp_slot(14,'dRH2_{meta}',0.,-0.45,2)
Map.ramp_slot(15,'dRH1_{meta}',-0.3,0.15,1)
Map.ramp_slot(20,'dRH2_{SAW}',0.,-0.45,2)
Map.ramp_slot(21,'dRH1_{SAW}',-0.3,0.15,1)

#Map.ramp_DAC('RD1',-1.095,-1.095,1)
#Map.ramp_DAC('RD2',-0.758,-0.758,1)
#Map.ramp_RF('SAW_{freq}',2.5,2.7,1)
#Map.ramp_RF('SAW_{power}',15.,25.,1)

Map.reconfig_ADC(sampling_rate=250e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()