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
prefix = 'RT_losing_'
Map = RT_fastseq(folder,prefix)

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.

### LEFT
Map.init_val['LD1'] = -0.736
Map.init_val['LD2'] = -0.752
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -0.9
Map.init_val['LP2'] = -0.85

### RIGHT
Map.init_val['RD1'] = -0.763
Map.init_val['RD2'] = -1.
Map.init_val['RV1'] = -1.6
Map.init_val['RV2'] = -1.0
Map.init_val['RH1'] = -1.75
Map.init_val['RH2'] = -0.7
Map.init_val['RH3'] = -1.
Map.init_val['RP2'] = -0.85

### CHANNEL
Map.init_val['TC'] = -1.
Map.init_val['BC'] = -1.

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2031
Map.init_val['RF0_{power}'] = 15.
Map.init_val['RF1_{freq}'] = 0.1382
Map.init_val['RF1_{power}'] = 12.

### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = 25.
Map.init_val['SAW_{width}'] = 0.05
Map.init_val['SAW_{delay}'] = 800.


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
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['Trigger','1011'])

Map.sequence.append(['LH2',-0.14])  # load 2 electrons
Map.sequence.append(['LH3',0.3])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',0.])
Map.sequence.append(['LH2',0.])

Map.sequence.append(['LP2',+0.])     # Meas
Map.sequence.append(['LH1',0.])  
Map.sequence.append(['LH3',0.])
Map.sequence.append(['LH2',-0.])
Map.sequence.append(['TC',0.])
Map.sequence.append(['BC',0.])
Map.sequence.append(['LV1',+0.])
Map.sequence.append(['LV2',-0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['LH2',-0.22])    # Metastable
Map.sequence.append(['LH1',0.])
Map.sequence.append(['LH3',+0.3])
Map.sequence.append(['Timing',1.])

Map.sequence.append(['LH3',0.])      # Meas
Map.sequence.append(['LH1',0.])
Map.sequence.append(['LH2',0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['Jump',17])

Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [80,51,51]
Map.init_val['LD1'] = -0.736
Map.init_val['LD2'] = -0.752
#Map.ramp_slot(3,'dLH2_{load}',-0.14,-0.22,2)
#Map.ramp_slot(4,'dLH3_{load}',0.4,0.4,2)

#Map.ramp_slot(17,'dLP2_{meta}',-0.3,-0.3,1)
#Map.ramp_slot(18,'dLH1_{meta}',-0.3,0.3,1)
Map.ramp_slot(17,'dLH2_{meta}',-0.45,0.15,2)
Map.ramp_slot(19,'dLH3_{meta}',0.15,0.45,1)
#Map.ramp_slot(21,'dTC_{meta}',-0.3,0.3,2)
#Map.ramp_slot(22,'dBC_{meta}',-0.3,0.3,2)

#Map.ramp_slot(23,'dLV1_{meta}',-0.3,0.3,1)
#Map.ramp_slot(24,'dLV2_{meta}',0.,0.,1)

#Map.ramp_DAC('LD1',-0.55,-0.85,1)
#Map.ramp_DAC('LD2',-0.65,-0.95,2)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)


#Map.ramp_RF('RF0_{freq}',0.195,0.210,1)
#Map.ramp_RF('RF0_{power}',15.,0.,2)

Map.reconfig_ADC(sampling_rate=200e3)
ans1 = Map.build_seq()
ans2 = Map.build_sweep()
if ans1 and ans2:
    Map.build_files()