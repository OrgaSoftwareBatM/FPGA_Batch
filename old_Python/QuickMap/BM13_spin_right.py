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
Map.init_val['LD1'] = -0.6
Map.init_val['LD2'] = -0.795
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -0.9
Map.init_val['LP2'] = -0.85

### RIGHT
Map.init_val['RD1'] = -0.746
Map.init_val['RD2'] = -0.905
Map.init_val['RV1'] = -1.6
Map.init_val['RV2'] = -1.0
Map.init_val['RH1'] = -1.75
Map.init_val['RH2'] = -0.7
Map.init_val['RH3'] = -1.
Map.init_val['RP2'] = -0.85

### CHANNEL
Map.init_val['TC'] = -1.0
Map.init_val['BC'] = -1.0

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2015
Map.init_val['RF0_{power}'] = 15.
Map.init_val['RF1_{freq}'] = 0.1382
Map.init_val['RF1_{power}'] = 12.

### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.05
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

Map.sequence.append(['RH1',-0.1]) # empty
Map.sequence.append(['RH3',0.08])
Map.sequence.append(['Timing',0.])

Map.sequence.append(['RH1',0.0]) # load
Map.sequence.append(['Timing',0.])

Map.sequence.append(['RH3',-0.15]) # Meta
Map.sequence.append(['RH1',+0.187])
#Map.sequence.append(['Timing',0.1])
Map.sequence.append(['RH1',-0.02])
Map.sequence.append(['RH3',0.06])
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['RH3',0.])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['Timing',2.])
Map.sequence.append(['Jump',len(Map.sequence)])

Map.sweep_dim = [40,41,250]
#Map.init_val['RD1'] = -0.715
#Map.init_val['RD2'] = -0.95
Map.init_val['RD1'] = -0.725
Map.init_val['RD2'] = -1.005

#Map.ramp_slot(4,'dRH1_{load}',-0.1 ,0.05,1)
#Map.ramp_slot(4,'t_{load,log}',0.2,20.,2)

#Map.ramp_slot(10,'dRH3_{wait}',-0.25,-0.4,1)
#Map.ramp_slot(9,'dRH1_{wait}',-0.06,0.03,1)
#Map.ramp_slot(6,'dRH3_{wait}',-0.6,0.,2)
#Map.ramp_slot(6,'dRH2_{wait}',-0.1,0.2,1)
#Map.ramp_slot(7,'dRH1_{wait}',0.17,0.23,1)
#Map.ramp_slot(9,'dRH2_{wait}',0.1,-0.8,3)
#Map.ramp_slot(9,'dRH3_{wait}',0.3,-0.6,1)
#Map.ramp_slot(6,'dBC_{wait}',0.3,-0.3,2)
#Map.ramp_slot(10,'dBC_{wait}',0.3,-0.3,2)
#Map.ramp_slot(9,'dRH3_{wait}',+0.3,-0.3,1)
#Map.ramp_slot(8,'t_{wait,log}',0.2,20.,2)
#Map.ramp_slot(8,'t_{wait}',0.,0.2,1)
#Map.ramp_slot(9,'t_{read}',0.,1.,1)
#Map.ramp_slot(9,'t_{wait}',0.,10.,1)
#Map.ramp_slot(6,'t_{wait}',0.,20.,1)

#Map.ramp_slot(8,'dRH1_{read}',-0.06,0.03,1)
#Map.ramp_slot(14,'dLH2_{meas}',-0.,0.03,1)

Map.ramp_DAC('RD1',-0.7625,-0.8075,1)
#Map.ramp_DAC('RD2',-0.955,-1.033,2)
#Map.ramp_RF('SAW_{freq}',2.5,2.8,2)
#Map.ramp_RF('SAW_{power}',15.,25.,2)

Map.reconfig_ADC(sampling_rate=200e3)
ans1 = Map.build_seq()
ans2 = Map.build_sweep()
if ans1 and ans2:
    Map.build_files()