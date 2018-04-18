# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

@author: manip.batm
"""

from BM13_ramp_reflecto import StabilityDiagram


##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data1'
prefix = 'stab_'
Map = StabilityDiagram(folder,prefix)

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 0.5 # integration time (fastseq divider)
Map.step_wait = 0.       # ms wait after every fastseq

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
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1])
Map.sequence.append(['Trigger','0011'])

Map.sequence.append(['LH2',0.05])  # load 2 electrons
Map.sequence.append(['LH3',-0.01])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['LH3',-0.01])
Map.sequence.append(['LH2',0.05])
Map.sequence.append(['LH1',-0.])
#Map.sequence.append(['TC',0.])
#Map.sequence.append(['BC',0.])
#Map.sequence.append(['LV1',-0.])
#Map.sequence.append(['LV2',0.])
Map.sequence.append(['Timing',1.])  # Meas

Map.build_pre_ramp_seq()
##########################
###	 MAP
##########################
Map.sweep_dim = [201,201]
Map.init_val['LD1'] = -0.55
Map.init_val['LD2'] = -0.72
#Map.ramp_DAC('LH3',-0.5,-0.8,0)
#Map.ramp_DAC('LH2',-0.45,O-0.75,1)
#Map.ramp_DAC('LH1',-1.6,-1.6,1)
#Map.ramp_DAC('LD2',-0.835,-0.805,1)
#
#Map.ramp_DAC('LH3',-0.75,-1.05,0,init_at=-0.65)
#Map.ramp_DAC('LH3',-0.5,-0.8,0)
#Map.ramp_DAC('LH2',-0.45,-0.75,1)
#Map.ramp_DAC('RH1',-1.6,-1.3,0)
#Map.ramp_DAC('RD1',-0.842,-0.842,1)
#Map.ramp_DAC('LD2',-0.83,-0.85,1)

#Map.ramp_slot(7,'dLH2',0.05,-0.15,1)
#Map.ramp_slot(8,'dLH1',-0.15,+0.15,1)

Map.ramp_DAC('LD1',-0.55,-1.,0)
Map.ramp_DAC('LD2',-0.55,-1.,1)

#Map.ramp_DAC('TC',-1.3,-1.,2)
#Map.ramp_DAC('BC',-1.,-1,2)


Map.build_fastramp()
Map.update_timings()
Map.build_sweep()
Map.build_files()