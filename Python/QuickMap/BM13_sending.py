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
Map.init_val['LD1'] = -0.695
Map.init_val['LD2'] = -0.795
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.3
Map.init_val['LH2'] = -0.8
Map.init_val['LH3'] = -1.
Map.init_val['LP2'] = -0.55

### RIGHT
Map.init_val['RD1'] = -0.82
Map.init_val['RD2'] = -0.77
Map.init_val['RV1'] = -1.45
Map.init_val['RV2'] = -1.45
Map.init_val['RH1'] = -1.3
Map.init_val['RH2'] = -0.8
Map.init_val['RH3'] = -1.
Map.init_val['RP2'] = -0.55

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
Map.init_val['SAW_{power}'] = 25.
Map.init_val['SAW_{width}'] = 0.3
Map.init_val['SAW_{delay}'] = 500.

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

Map.sequence.append(['LH2',0.2])  # load left
Map.sequence.append(['LH3',0.4])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',-0.2])
Map.sequence.append(['LH2',0.])

Map.sequence.append(['LP2',-0.3])
Map.sequence.append(['LH1',-0.3])  
Map.sequence.append(['LH2',-0.3])
Map.sequence.append(['LH3',-0.4])
Map.sequence.append(['LV1',0.])
Map.sequence.append(['LV2',0.])

Map.sequence.append(['Trigger','1011'])

Map.sequence.append(['RH2',0.3])  # load right
Map.sequence.append(['RH3',0.25])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['RH2',0.])

Map.sequence.append(['RP2',-0.3])     # Meas
Map.sequence.append(['RH1',-0.])  
Map.sequence.append(['RH2',-0.])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['TC',-0.])
Map.sequence.append(['BC',-0.])
Map.sequence.append(['RV1',-0.])
Map.sequence.append(['RV2',-0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['RP2',-0.3])    # Metastable
Map.sequence.append(['RH1',-0.3])  
Map.sequence.append(['RH2',-0.3])
Map.sequence.append(['RH3',-0.4])
Map.sequence.append(['TC',0.15])
Map.sequence.append(['BC',-0.])
Map.sequence.append(['RV1',-0.3])
Map.sequence.append(['RV2',-0.3])
Map.sequence.append(['Timing',1.])

Map.sequence.append(['RP2',-0.3])     # Meas
Map.sequence.append(['RH1',-0.])  
Map.sequence.append(['RH2',-0.])
Map.sequence.append(['RH3',-0.2])
Map.sequence.append(['TC',-0.])
Map.sequence.append(['BC',-0.])
Map.sequence.append(['RV1',-0.])
Map.sequence.append(['RV2',-0.])
Map.sequence.append(['Timing',4.])

Map.sequence.append(['Trigger','1001'])
Map.sequence.append(['Jump',27])

Map.sweep_dim = [80,201,2]
Map.init_val['LD1'] = -0.795
Map.init_val['LD2'] = -0.7
Map.init_val['RD1'] = -0.810
Map.init_val['RD2'] = -0.757
Map.ramp_slot(1,'dLH2_{load}',0.,0.2,2)
#Map.ramp_slot(2,'dLH3_{load}',0.4,0.4,2)

#Map.ramp_slot(13,'dRH2_{load}',0.3,0.3,1)
#Map.ramp_slot(14,'dRH3_{load}',0.25,0.25,2)

#Map.ramp_slot(27,'dRP2_{meta}',-0.3,-0.3,1)
#Map.ramp_slot(28,'dRH1_{meta}',-0.45,0.45,2)
#Map.ramp_slot(29,'dRH2_{meta}',-0.45,0.45,1)
#Map.ramp_slot(30,'dRH3_{meta}',-0.,-0.6,1)
#Map.ramp_slot(31,'dTC_{meta}',-0.45,0.45,2)
#Map.ramp_slot(32,'dBC_{meta}',-0.3,0.3,1)
#Map.ramp_slot(33,'dRV1_{meta}',-0.3,0.3,2)
#Map.ramp_slot(34,'dRV2_{meta}',0.,0.,1)

Map.ramp_DAC('LD1',-0.7,-0.85,1)
#Map.ramp_DAC('LD2',-0.7,-0.85,2)
#Map.ramp_DAC('RD1',-0.7,-0.85,1)
#Map.ramp_DAC('RD2',-0.7,-0.85,1)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)


Map.reconfig_ADC(sampling_rate=250e3)
Map.build_seq()
Map.build_sweep()
Map.build_files()