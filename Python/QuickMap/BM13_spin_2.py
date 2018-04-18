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
prefix = 'RT_spin_'
Map = RT_fastseq(folder,prefix)

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.2
Map.init_val['Rbias'] = 0.2

### LEFT
Map.init_val['LD1'] = -0.65
Map.init_val['LD2'] = -0.82
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -0.65
Map.init_val['LP2'] = -0.85

### RIGHT
Map.init_val['RD1'] = -0.82
Map.init_val['RD2'] = -0.765
Map.init_val['RV1'] = -1.45
Map.init_val['RV2'] = -1.45
Map.init_val['RH1'] = -1.45
Map.init_val['RH2'] = -0.45
Map.init_val['RH3'] = -0.75
Map.init_val['RP2'] = -0.85

### CHANNEL
Map.init_val['TC'] = -1.3
Map.init_val['BC'] = -1.15

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2012
Map.init_val['RF0_{power}'] = -30.
Map.init_val['RF1_{freq}'] = 0.142
Map.init_val['RF1_{power}'] = -30.

### RS
Map.init_val['SAW_{freq}'] = 2.644
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.1
Map.init_val['SAW_{delay}'] = 0.1

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

Map.sequence.append(['LH2',0.01])  # empty
Map.sequence.append(['LH3',0.])
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['LH3',-0.15])

Map.sequence.append(['LH2',+0.005])  # load
Map.sequence.append(['LH3',0.])
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['LH3',-0.15])
Map.sequence.append(['Timing',0.])

Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['LH2',0.])  
Map.sequence.append(['LH3',-0.1])     # meas
Map.sequence.append(['Timing',30.])

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [151,201,2]
#Map.init_val['LD1'] = -0.82
Map.init_val['LD2'] = -0.816
#Map.ramp_slot(5,'dLH2_{load}',-0.,0.3,2)
#Map.ramp_slot(6,'dLH3_{load}',-0.06,0.,2)
#Map.ramp_slot(7,'t_{load}',0.25,5,1)

Map.ramp_slot(9,'t_{wait}',0.1,10.,2)

#Map.ramp_slot(11,'dLH2_{meas}',-0.15,0.15,1)
Map.ramp_slot(11,'dLH2_{meas}',-0.03,-0.03,1)

#Map.ramp_slot(12,'dLH3_{meas}',-0.0024,-0.0024,2)

#Map.ramp_DAC('LD1',-0.7,-1.,1)
#Map.ramp_DAC('LD2',-0.75,-0.9,1)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)

Map.reconfig_ADC(sampling_rate=200e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()