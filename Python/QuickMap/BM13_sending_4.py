# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:48:45 2018

@author: manip.batm
"""

from BM13_RT import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data1'
prefix = 'RT_sending_'
Map = RT_fastseq(folder,prefix)

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.

### LEFT
Map.init_val['LD1'] = -0.6
Map.init_val['LD2'] = -0.795
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -0.9
Map.init_val['LP2'] = -0.85

### RIGHT
Map.init_val['RD1'] = -0.82
Map.init_val['RD2'] = -0.77
Map.init_val['RV1'] = -1.45
Map.init_val['RV2'] = -1.45
Map.init_val['RH1'] = -1.6
Map.init_val['RH2'] = -0.45
Map.init_val['RH3'] = -1.
Map.init_val['RP2'] = -0.85

### CHANNEL
Map.init_val['TC'] = -1.3
Map.init_val['BC'] = -1.15

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2028
Map.init_val['RF0_{power}'] = 15.
Map.init_val['RF1_{freq}'] = 0.1390
Map.init_val['RF1_{power}'] = 12.

### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = 25.
Map.init_val['SAW_{width}'] = 0.05
Map.init_val['SAW_{delay}'] = 0.1

##########################
###	 FASTSEQ + CONF FILE   			
##########################
Map.initial_wait = 1    # ms before everything
Map.ms_per_point = 0.05     # integration time (RT_avg/ADC_freq)
Map.step_wait = 0        # ms wait after every fastseq

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['Trigger','1011'])

Map.sequence.append(['LH3',0.3]) # Load L&R
Map.sequence.append(['RH3',0.3])
Map.sequence.append(['LH2',-0.09])
Map.sequence.append(['RH2',0.025])
Map.sequence.append(['LH3',-0.1])
Map.sequence.append(['RH3',-0.1])
Map.sequence.append(['Timing',0.])

Map.sequence.append(['RP2',0.])
Map.sequence.append(['RV2',-0.3])
Map.sequence.append(['RH3',-0.5])
Map.sequence.append(['TC',+0.2]) # Meta
Map.sequence.append(['RH2',-0.75])
Map.sequence.append(['RH1',+0.1])
Map.sequence.append(['LV2',-0.3])

Map.sequence.append(['Timing',0.5])
Map.sequence.append(['Trigger','1001']) # SAW
Map.sequence.append(['Timing',0.])
Map.sequence.append(['Trigger','1001']) # AWG
Map.sequence.append(['Timing',0.5])

Map.sequence.append(['RP2',0.]) # Charge sensing 
Map.sequence.append(['RH1',0.]) 
Map.sequence.append(['LV2',0.])
Map.sequence.append(['RV2',0.])
Map.sequence.append(['TC',0.])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['LH3',-0.1])
Map.sequence.append(['RH3',-0.1])
Map.sequence.append(['Timing',1.])

Map.sequence.append(['Jump',2])
#Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [51,51,51]
Map.init_val['LD1'] = -0.73
Map.init_val['LD2'] = -0.763
Map.init_val['RD1'] = -0.79
Map.init_val['RD2'] = -0.772

#Map.ramp_slot(5,'dLH2_{load}',-0.09,0.09,2)
#Map.ramp_slot(6,'dRH2_{load}',-0.09,0.09,2)


#
#Map.ramp_slot(11,'t_{wait}',0.,20.,1)
#Map.ramp_slot(18,'t_{wait}',0.,20.,1)
#Map.ramp_slot(18,'t_{wait,R,log}',0.1,10.,2)
#Map.ramp_slot(20,'t_{wait,L}',0.,6.,1)
#Map.ramp_slot(29,'t_{wait}',0.,20.,1)

Map.ramp_slot(10,'dRP2_{meta}',-0.3,0.3,1)
Map.ramp_slot(15,'dRH1_{meta}',-0.3,0.3,2)


#Map.ramp_DAC('LD1',-0.7,-0.85,1)
#Map.ramp_DAC('LD2',-0.7,-0.85,2)
#Map.ramp_DAC('RD1',-0.7,-0.85,1)
#Map.ramp_DAC('RD2',-0.7,-0.85,2)
#Map.ramp_RF('SAW_{freq}',2.6,3.,1)
#Map.ramp_RF('SAW_{power}',15.,25.,3)
#Map.ramp_RF('SAW_{width}',0.01,0.210,2)


Map.reconfig_ADC(sampling_rate=200e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()
