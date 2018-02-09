# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

@author: manip.batm
"""

from Pre_ramp_seq_Bermousque import StabilityDiagram


##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD1\\data1'
prefix = 'stab_'
Map = StabilityDiagram(folder,prefix)

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 1.  # integration time (fastseq divider)
Map.step_wait = 0.        # ms wait after every fastseq

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.2
Map.init_val['Rbias'] = 0.2

### LEFT
Map.init_val['LD1'] = -0.55
Map.init_val['LD2'] = -0.
Map.init_val['LV1'] = -1.3
Map.init_val['LV2'] = -1.5
Map.init_val['LH1'] = -1.
Map.init_val['LH2'] = -0.85
Map.init_val['LH3'] = -0.7

### RIGHT
Map.init_val['RD1'] = -1.21
Map.init_val['RD2'] = -0.55
Map.init_val['RV1'] = -1.2
Map.init_val['RV2'] = -1.3
Map.init_val['RH1'] = -1.
Map.init_val['RH2'] = -0.85
Map.init_val['RH3'] = -0.7

### CHANNEL
Map.init_val['TC'] = -1.5
Map.init_val['BC'] = -1.5

##########################
###	 FASTSEQ			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','0000'])

#Map.sequence.append(['RH1',0.])
#Map.sequence.append(['RH2',0.015])
#Map.sequence.append(['RH3',0.7])
#
#Map.sequence.append(['RH3',0.])
#Map.sequence.append(['RH1',0.])
#Map.sequence.append(['RH2',0.])
#Map.sequence.append(['RV1',0.])
#Map.sequence.append(['RV2',0.])
#Map.sequence.append(['BC',0.])
#Map.sequence.append(['TC',0.])
#Map.sequence.append(['Timing',1.])
Map.build_pre_ramp_seq()
##########################
###	 MAP
##########################
Map.sweep_dim = [1001,1001]
Map.ramp_DAC('LH3',-1.1,-0.8,0)
Map.ramp_DAC('LH2',-0.6,-0.3,1)
#Map.ramp_DAC('LH1',-0.7,-0.7,1)
#Map.ramp_DAC('LD1',-0.55,-0.55,1)
Map.ramp_DAC('LD1',-1.055,-1.07,1)

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