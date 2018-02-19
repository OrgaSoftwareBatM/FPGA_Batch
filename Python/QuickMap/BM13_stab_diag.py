# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

@author: manip.batm
"""

from BM13_ramp_reflecto import StabilityDiagram


##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD1\\data1'
prefix = 'stabRF_'
Map = StabilityDiagram(folder,prefix)

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.2
Map.init_val['Rbias'] = 0.2

### LEFT
Map.init_val['LD1'] = -0.55
Map.init_val['LD2'] = -1.04
Map.init_val['LV1'] = -1.15
Map.init_val['LV2'] = -1.25
Map.init_val['LH1'] = -1.3
Map.init_val['LH2'] = -0.8
Map.init_val['LH3'] = -1.35

### RIGHT
Map.init_val['RD1'] = -0.55
Map.init_val['RD2'] = -1.1
Map.init_val['RV1'] = -1.15
Map.init_val['RV2'] = -1.2
Map.init_val['RH1'] = -1.3
Map.init_val['RH2'] = -0.8
Map.init_val['RH3'] = -1.35

### CHANNEL
Map.init_val['TC'] = -1.45
Map.init_val['BC'] = -1.45

### REFLECTO
Map.init_val['RF0_{freq}'] = 0.2012
Map.init_val['RF0_{power}'] = -30.
Map.init_val['RF1_{freq}'] = 0.142
Map.init_val['RF1_{power}'] = -30.

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 0.2 # integration time (fastseq divider)
Map.step_wait = 0.       # ms wait after every fastseq

##########################
###	 FASTSEQ 			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1])
Map.sequence.append(['Trigger','1000'])

Map.sequence.append(['RH2',0.175])  # load 2 electrons
Map.sequence.append(['RH3',0.35])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['RH3',-0.35])
Map.sequence.append(['RH2',0.1])

Map.sequence.append(['BC',0.1])
Map.sequence.append(['TC',0.])
Map.sequence.append(['RV1',-0.1])
Map.sequence.append(['RV2',0.1])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RH2',0.125])

Map.build_pre_ramp_seq()
##########################
###	 MAP
##########################
Map.sweep_dim = [401,401]
#Map.ramp_DAC('LH3',-1.7,-1.35,0,init_at=-1.35)
#Map.ramp_DAC('LH2',-0.8,-0.5,1)
#Map.ramp_DAC('LD2',-1.0•4,-1.06,1)
#Map.ramp_DAC('LH1',-1.3,-1.0,2)

Map.ramp_DAC('RH3',-1.7,-1.25,0,init_at=-1.35)
#Map.ramp_DAC('RH2',-0.8,-0.5,1)
Map.ramp_DAC('RD1',-0.7,-0.7,1)
Map.ramp_DAC('RD2',-0.75,-0.75,1)
#Map.ramp_DAC('RH1',-1.3,-1.0,2)

Map.ramp_slot(8,'dBC',0.,0.,1)
Map.ramp_slot(9,'dTC',0.,0.,1)
Map.ramp_slot(10,'dRV1',-0.25,-0.25,1)
Map.ramp_slot(11,'dRV2',-0.2,-0.2,1)
Map.ramp_slot(12,'dRH1',-0.05,0.25,1)
#Map.ramp_slot(12,'dRH1',-0.05,-0.05,1)
Map.ramp_slot(13,'dRH2',-0.1,-0.1,1)

#Map.ramp_RF('RF1_{freq}',0.2012,0.240,1)

#Map.ramp_DAC('RH3',-1.15,-1.6,0,init_at=-1.6)
#Map.ramp_DAC('RH1',-1.45,-1.,0,init_at=-1.3)
##Map.ramp_DAC('RH2',-0.7,-0.55,1)
#Map.ramp_DAC('RD1',-0.85,-0.89,1)
##Map.ramp_DAC('RH2',-0.9,-0.6,1)
##Map.ramp_DAC('RD2',-0.95,-0.95,1)
##Map.ramp_DAC('RH2',-0.85,-0.55,1)
##Map.ramp_DAC('RH2',-0.85,-0.55,1)
##Map.ramp_DAC('RV1',-1.2,-1.2,1)
##Map.ramp_DAC('RV1',-1.15,-1.25,2)
#
##Map.ramp_slot(3,'dRH1_{load}',-0.12,-0.12,1)
##
##Map.ramp_slot(7,'dRH1',-0.2,0.1,1)
#Map.ramp_slot(8,'dRH2',-0.6,-0.15,1)
#Map.ramp_slot(9,'dRV1',-0.2,-0.2,1)
#Map.ramp_slot(10,'dRV2',-0.2,-0.2,1)
#Map.ramp_slot(11,'dBC',-0.2,-0.2,1)
#Map.ramp_slot(12,'dTC',-0.2,-0.2,1)

#Map.ramp_DAC('RH3',-0.9,-0.9,1)
#Map.ramp_DAC('RH1',-0.9,-1.5,1)
##Map.ramp_DAC('RD2',-1.115,-1.08,1)
#Map.ramp_DAC('RD2',-1.0975,-1.0975,1)
#Map.ramp_DAC('RD1',-0.7,-1.3,0)


#Map.add_wait('wait_bg',0,10000,1) # (index,ms,axis) wait n ms at index for given axis

Map.build_fastramp()
Map.update_timings()
Map.build_sweep()
Map.build_files()