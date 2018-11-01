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
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.

### LEFT
Map.init_val['LD1'] = -0.6
Map.init_val['LD2'] = -0.795
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.8
Map.init_val['LH3'] = -0.6
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
Map.init_val['RF0_{freq}'] = 0.2028
Map.init_val['RF0_{power}'] = 15.
Map.init_val['RF1_{freq}'] = 0.1382
Map.init_val['RF1_{power}'] = 12.

### RS
Map.init_val['SAW_{freq}'] = 2.79
Map.init_val['SAW_{power}'] = -30.
Map.init_val['SAW_{width}'] = 0.05
Map.init_val['SAW_{delay}'] = 0.1

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1])
Map.sequence.append(['Trigger','0011'])

#Map.sequence.append(['RH3',0.08])
#Map.sequence.append(['RH1',0.])  # load 2 electrons
#Map.sequence.append(['Timing',1.])  # Meas
#Map.sequence.append(['LH3',-0.3])
#Map.sequence.append(['LH2',+0.3])
#Map.sequence.append(['RH1',+0.])
#Map.sequence.append(['RV2',+0.15])
#Map.sequence.append(['RH2',0.0])
#Map.sequence.append(['RH1',0.15])
#Map.sequence.append(['RV2',-0.15])
#Map.sequence.append(['BC',+0.3])
#Map.sequence.append(['RH2',-0.1])
#Map.sequence.append(['RH1',0.3])
#Map.sequence.append(['RV2',0.])
#Map.sequence.append(['Timing',1.])  # Meas
Map.build_pre_ramp_seq()
##########################
###	 MAP
##########################
Map.sweep_dim = [401,401]
Map.init_val['LD1'] = -0.715
Map.init_val['LD2'] = -0.83
Map.init_val['LV1'] = -1.6
Map.init_val['LV2'] = -1.3
Map.init_val['LH1'] = -1.6
Map.init_val['LH2'] = -0.65
Map.init_val['LH3'] = -0.9

#Map.ramp_DAC('RH3',-0.8,-1.25,0)
#Map.ramp_DAC('RH3',-1.25,-0.8,0,init_at=-1.0)
#Map.ramp_DAC('RH1',-1.6,-1.3,0,init_at=-1.75)
#Map.ramp_DAC('RH1',-2.2,-1.,1)
##Map.ramp_DAC('RH1',-2.2,-1.3,1)
##Map.ramp_DAC('RH2',-0.7,-0.4,1)

Map.ramp_DAC('LD1',-0.56,-0.725,1)
#Map.ramp_DAC('LD2',-0.823,-0.8,0)
#Map.ramp_DAC('LD2',-0.81,-0.84,1)

Map.ramp_DAC('LH3',-0.5,-0.8,0)
#Map.ramp_DAC('LH2',-0.9,-0.3,1)
Map.ramp_DAC('LH1',-2.2,-1.3,1)

#Map.ramp_DAC('RD2',-0.955,-0.915,0)
#Map.ramp_DAC('RD2',-0.95,-1.1,1)
#Map.ramp_DAC('RD2',-0.94,-1.06,1)
#Map.ramp_DAC('LD1',-0.5,-1.,0)
#Map.ramp_DAC('LD2',-0.5,-1.,1)
#Map.ramp_DAC('RH2',-0.3,-0.6,1)

#Map.ramp_slot(3,'dRH2_{load}',-0.15,0.15,1)

#Map.ramp_slot(7,'dRH1',-0.15,0.6,1)
#Map.ramp_slot(6,'dRH3',-0.6,-0.,2)
#Map.ramp_slot(10,'dRP2',-0.15,0.15,1)
#Map.ramp_slot(6,'dRH3',0.2,-0.25,2)
#Map.ramp_slot(9,'dTC',-0.15,+0.15,1)
#Map.ramp_slot(8,'dRV2',-0.15,+0.15,1)
#Map.ramp_slot(9,'dRH2',-0.15,+0.15,1)
#Map.ramp_slot(9,'dRV1',-0.,-0.3,2)
#Map.ramp_slot(12,'dRH1',0.,0.75,1)
#Map.ramp_slot(13,'dRH2',-0.75,-0.3,1)
#Map.ramp_slot(11,'dRH3',-0.3,0.3,1)
#Map.ramp_slot(11,'dRH1',0.,0.035,1)
#Map.ramp_slot(12,'dRV2',0.,-0.3,1)
#Map.ramp_slot(10,'dTC',-0.3,+0.3,2)
#Map.ramp_slot(11,'dBC',-0.3,+0.3,2)
#Map.ramp_slot(12,'dRV1',0.,0.,1)
#Map.ramp_slot(13,'dRV2',0.,0.3,1)
#Map.ramp_DAC('LD1',-0.6,-1.15,0)
#Map.ramp_DAC('LD2',-0.6,-1.15,1)
#Map.ramp_DAC('RD1',-0.65,-0.8,0)
#Map.ramp_DAC('RD2',-0.6,-1.15,1)
#Map.ramp_DAC('RD2',-0.55,-1.05,1)

#Map.ramp_DAC('LD1',-0.55,-1.05,0)
#Map.ramp_DAC('LD2',-0.55,-1.05,1)


#Map.ramp_RF('RF0_{freq}',0.195,0.210,1)
#Map.ramp_RF('RF0_{power}',15.,0.,1)
#Map.ramp_RF('RF1_{freq}',0.120,0.145,1)
#Map.ramp_RF('RF1_{power}',15.,0.,1)

Map.build_fastramp()
Map.update_timings()
Map.build_sweep()
Map.build_files()