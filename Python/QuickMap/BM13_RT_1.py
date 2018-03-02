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
prefix = 'RT_sending_'
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
Map.init_val['RD1'] = -0.55
Map.init_val['RD2'] = -1.1
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

Map.sequence.append(['RH2',0.175])  # load 2 electrons
Map.sequence.append(['RH3',0.35])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.35])
Map.sequence.append(['RH2',0.1])

Map.sequence.append(['BC',0.1])  # Metastable
Map.sequence.append(['TC',0.2])
Map.sequence.append(['RV1',-0.15])
Map.sequence.append(['RV2',-0.2]) #10
Map.sequence.append(['RH1',0.1])
Map.sequence.append(['RH2',0.15])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['Trigger','1000'])
Map.sequence.append(['Timing',2.])

#Map.sequence.append(['Trigger','1000'])
Map.sequence.append(['BC',0.1])  # Readout
Map.sequence.append(['TC',0.2])
Map.sequence.append(['RV1',-0.15])
Map.sequence.append(['RV2',-0.2]) 
Map.sequence.append(['RH1',0.1])
Map.sequence.append(['RH2',0.15])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['Timing',2.])
#Map.sequence.append(['Trigger','1000'])
#Map.sequence.append(['Timing',2.])
Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [26,51,51]
Map.ramp_slot(7,'dBC_{meta}',-0.3,0.3,1)
Map.ramp_slot(8,'dTC_{meta}',0.,0.,1)
Map.ramp_slot(9,'dRV1_{meta}',-0.4,0.2,2)
#Map.ramp_slot(10,'dRV2_{meta}',-0.3,-0.3,1)
Map.ramp_slot(11,'dRH1_{meta}',0.1,0.1,1)
Map.ramp_slot(12,'dRH2_{meta}',0.,0.,1)
#Map.ramp_slot(13,'dRH3_{meta}',-0.3,0.3,1)
#Map.ramp_slot(14,'t_{meta}',1.,1.,1)

#Map.ramp_DAC('RD2',-0.65,-1.1,1)
#Map.ramp_DAC('RD1',-0.9,-0.9,1)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)

Map.reconfig_ADC(sampling_rate=250e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()