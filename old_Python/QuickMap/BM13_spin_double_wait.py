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
Map.init_val['SAW_{freq}'] = 2.644
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.1
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

Map.sequence.append(['LH2',0.055]) # load
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH3',-0.1]) # wait 1
Map.sequence.append(['Timing',2.])

Map.sequence.append(['LH3',-0.2]) # wait 2
Map.sequence.append(['Timing',15.])

Map.sequence.append(['LH3',-0.1]) # wait 3
Map.sequence.append(['Timing',1.])

Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['LH2',0.0560])  
Map.sequence.append(['LH3',-0.03])
Map.sequence.append(['Timing',5.])

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [100,21,3,250]
Map.init_val['LD1'] = -0.69
Map.init_val['LD2'] = -0.832
#Map.ramp_slot(3,'dLH2_{load}',0.03,0.09,1)
#Map.ramp_slot(1,'dLH3_{load}',-0.01,0.01,2)
#Map.ramp_slot(6,'t_{load}',0.1,0.1,2)

#Map.ramp_slot(5,'dLH3_{wait,1}',-0.1,-0.4,1)
#Map.ramp_slot(6,'t_{wait,1,log}',0.2,20.,2)
#Map.ramp_slot(6,'t_{wait,1}',0.,15.,2)

#Map.ramp_slot(7,'dLH3_{wait,2}',-0.1,-0.4,1)
Map.ramp_slot(8,'t_{wait,2,log}',0.2,20.,2)
#Map.ramp_slot(8,'t_{wait,2}',0.,15.,1)

#Map.ramp_slot(9,'dLH3_{wait,3}',-0.1,-0.4,1)
#Map.ramp_slot(10,'t_{wait,3,log}',0.1,10.,2)
Map.ramp_slot(10,'t_{wait,3}',0.,15.,1)

#Map.ramp_slot(12,'dLH2_{meas}',0.0535,0.0535,2)
#Map.ramp_slot(12,'dLH2_{meas}',0.03,0.06,1)


#Map.ramp_DAC('LD1',-0.6,-0.9,2)
#Map.ramp_DAC('LD2',-0.75,-0.9,1)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)

Map.reconfig_ADC(sampling_rate=200e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()