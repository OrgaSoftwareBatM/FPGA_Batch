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
Map.init_val['LD1'] = -0.94
Map.init_val['LD2'] = -0.946
Map.init_val['LV1'] = -1.15
Map.init_val['LV2'] = -1.15
Map.init_val['LH1'] = -1.3
Map.init_val['LH2'] = -0.65
Map.init_val['LH3'] = -1.3

### RIGHT
Map.init_val['RD1'] = -1.02
Map.init_val['RD2'] = -0.852
Map.init_val['RV1'] = -1.15
Map.init_val['RV2'] = -1.15
Map.init_val['RH1'] = -1.3
Map.init_val['RH2'] = -0.65
Map.init_val['RH3'] = -1.3

### CHANNEL
Map.init_val['TC'] = -1.45
Map.init_val['BC'] = -1.45

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2012
Map.init_val['RF0_{power}'] = -30.
Map.init_val['RF1_{freq}'] = 0.142
Map.init_val['RF1_{power}'] = -30.

### RS
Map.init_val['SAW_{freq}'] = 2.644
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.1

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
Map.sequence.append(['Trigger','1000'])

Map.sequence.append(['RH2',0.02])  # load 2 electrons
Map.sequence.append(['RH3',0.25])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['RH1',0.2])
Map.sequence.append(['Timing',4.])  # Meas
Map.sequence.append(['BC',0.3])
Map.sequence.append(['TC',0.3])
Map.sequence.append(['RV1',-0.05])
Map.sequence.append(['RV2',-0.05])

Map.sequence.append(['RH2',0.])
Map.sequence.append(['RH3',-0.2])  # Metastable
Map.sequence.append(['RH1',-0.])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['BC',0.])
Map.sequence.append(['TC',0.])
Map.sequence.append(['RH1',0.2])
Map.sequence.append(['RV1',0.])
Map.sequence.append(['RV2',0.])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['Timing',4.])  # Meas

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [51,51,51]
#Map.init_val['LD1'] = -0.80
#Map.init_val['LD2'] = -0.825
#Map.ramp_slot(3,'dLH1_{load}',0.04,+0.04,1)
Map.ramp_slot(14,'dRH2_{meta}',-0.45,0.15,2)
Map.ramp_slot(15,'dRH3_{meta}',-0.45,0.15,1)
#Map.ramp_slot(16,'dLH1_{meta}',-0.3,0.15,1)
#Map.ramp_slot(9,'dLH2_{load}',0.,0.12,1)
#Map.ramp_slot(10,'dLH3_{load}',0.35,0.35,1)

#Map.ramp_DAC('LD1',-0.75,-0.9,2)
#Map.ramp_DAC('LD2',-0.75,-0.9,1)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)

Map.reconfig_ADC(sampling_rate=250e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()