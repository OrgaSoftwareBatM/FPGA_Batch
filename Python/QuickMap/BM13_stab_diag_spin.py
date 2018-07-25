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
Map.ms_per_point = 0.1 # integration time (fastseq divider)
Map.step_wait = 0.       # ms wait after every fastseq

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
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',0.1])
Map.sequence.append(['Trigger','0011'])

Map.sequence.append(['LH2',-0.09])  # Load L&R
Map.sequence.append(['RH2',0.01])
Map.sequence.append(['LH3',0.3])
Map.sequence.append(['RH3',0.3])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH3',-0.5]) # Meta
Map.sequence.append(['RH3',-0.4])
Map.sequence.append(['TC',+0.25])
Map.sequence.append(['LH2',0.])
Map.sequence.append(['RH2',-0.65])
Map.sequence.append(['RV1',+0.1])
Map.sequence.append(['LV2',-0.3])
Map.sequence.append(['RV2',-0.3])

Map.sequence.append(['Timing',0.1])
Map.sequence.append(['Trigger','0001'])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['RV1',0.]) # Charge sensing
Map.sequence.append(['LV2',0.])
Map.sequence.append(['RV2',0.])
Map.sequence.append(['TC',0.])
Map.sequence.append(['LH2',-0.2])
Map.sequence.append(['RH2',-0.35])
Map.sequence.append(['LH3',0.])
Map.sequence.append(['RH3',-0.])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['LH2',0.]) # Spin
Map.sequence.append(['LH3',0.])
Map.sequence.append(['Timing',0.1])

Map.build_pre_ramp_seq()

##########################
###	 MAP
##########################
Map.sweep_dim = [501,501]
#Map.init_val['LD1'] = -0.55
#Map.init_val['LD2'] = -0.83
#Map.ramp_DAC('LH3',-0.7,-1.,0)
#Map.ramp_DAC('LH2',-0.3,-0.6,1)
####Map.ramp_DAC('LH1',-1.6,-1.6,1)

#Map.ramp_DAC('LD2',-0.815,-0.795,1)
#
#Map.ramp_DAC('LH3',-0.5,-0.8,0)
Map.ramp_DAC('LH3',-0.9,-0.6,0,init_at=-0.9)
#Map.ramp_DAC('LH1',-1.0,-1.6,0,init_at=-1.3)
#Map.ramp_DAC('LH2',-0.45,-0.75,1)
#Map.ramp_DAC('LD1',-0.6,-0.65,1)
Map.ramp_DAC('LD2',-0.84,-0.825,1)

#Map.ramp_slot(3,'dLH2_{load}',0.14,0.21,2)

Map.ramp_slot(28,'dLH2',0.1,-0.05,1)
#Map.ramp_slot(8,'dLP2',-0.,-0.6,2)
#Map.ramp_slot(9,'dLH1',-0.3,0.6,2)
#Map.ramp_slot(10,'dTC',-0.3,+0.,2)
#Map.ramp_slot(11,'dBC',-0.3,+0.,2)
#Map.ramp_slot(12,'dLV1',-0.3,+0.3,2)
#Map.ramp_slot(13,'dLV2',-0.3,+0.3,2)
#Map.ramp_DAC('LD1',-0.55,-0.7,2)





#Map.ramp_DAC('RH3',-1.3,-0.7,0,init_at=-1.)
#Map.ramp_DAC('RH3',-0.7,-1.15,0,init_at=-1.)
#Map.ramp_DAC('RH2',-0.3,-0.6,1)
#Map.ramp_DAC('RH2',-0.504,-0.504,1)
#Map.ramp_DAC('RH1',-1.6,-1.3,0)
#Map.ramp_DAC('RD1',-0.842,-0.842,1)
#Map.ramp_DAC('RD2',-0.79,-0.82,1)



#Map.ramp_slot(3,'dRH2_{load}',0.275,0.31,2)

#Map.ramp_slot(7,'dRH2',-0.15,-0.15,1)
#Map.ramp_slot(9,'dRH1',-0.3,0.3,1)
#Map.ramp_slot(10,'dTC',-0.3,+0.15,1)
#Map.ramp_slot(11,'dBC',-0.3,+0.15,1)

#Map.ramp_DAC('LD1',-0.55,-1.,0)
#Map.ramp_DAC('LD2',-0.55,-1.,1)

#Map.ramp_DAC('TC',-1.3,-1.,2)
#Map.ramp_DAC('BC',-1.,-1,2)


#Map.ramp_RF('RF1_{freq}',0.135,0.145,1)
#Map.ramp_RF('RF1_{power}',20.,0.,1)

Map.build_fastramp()
Map.update_timings()
Map.build_sweep()
Map.build_files()