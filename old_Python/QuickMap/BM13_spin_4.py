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
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.

### LEFT
Map.init_val['LD1'] = -0.65
Map.init_val['LD2'] = -0.83
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
Map.init_val['RF0_{freq}'] = 0.2028
Map.init_val['RF0_{power}'] = 15.
Map.init_val['RF1_{freq}'] = 0.1390
Map.init_val['RF1_{power}'] = 12.

### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.30
Map.init_val['SAW_{delay}'] = 0.1

##########################
###	 FASTSEQ + CONF FILE   			
##########################
Map.initial_wait = 1    # ms before everything
Map.ms_per_point = 0.05    # integration time (RT_avg/ADC_freq)
Map.step_wait = 0        # ms wait after every fastseq

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])

Map.sequence.append(['LH3',-0.01]) # empty
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH2',0.05]) # load
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH3',-0.35]) # wait
Map.sequence.append(['LH2',0.05])
Map.sequence.append(['LV2',-0.])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','1101'])
Map.sequence.append(['LV2',-0.])

Map.sequence.append(['Trigger','1001'])
Map.sequence.append(['LH2',0.058])  
Map.sequence.append(['LH3',-0.03])
Map.sequence.append(['Timing',5.])

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [100,31,250]
Map.init_val['LD1'] = -0.69
Map.init_val['LD2'] = -0.832
#Map.ramp_slot(3,'dLH2_{load}',0.03,0.09,1)
#Map.ramp_slot(1,'dLH3_{load}',-0.03,0.03,2)
#Map.ramp_slot(6,'t_{load}',0.,0.2,1)

Map.ramp_slot(5,'dLH3_{wait}',-0.35,-0.35,1)
#Map.ramp_slot(7,'dLH2_{wait}',-0.3,0.3,2)
#Map.ramp_slot(9,'dLV1_{wait}',-0.3,0.15,2)
#Map.ramp_slot(10,'dLH1_{wait}',-0.15,0.15,2)
#Map.ramp_slot(8,'t_{wait,log}',0.1,10.,2)
Map.ramp_slot(8,'t_{wait}',0.,15.,1)

#Map.ramp_slot(10,'dLH2_{meas}',0.0535,0.0535,2)
#Map.ramp_slot(12,'dLH2_{meas}',0.015,0.075,1)


#Map.ramp_DAC('LD1',-0.6,-0.9,2)
#Map.ramp_DAC('LD2',-0.75,-0.9,2)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)
#Map.ramp_RF('SAW_{power}',-30.,25.,2)

Map.reconfig_ADC(sampling_rate=200e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()