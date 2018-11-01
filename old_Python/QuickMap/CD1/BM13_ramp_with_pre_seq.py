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
prefix = 'stab_2e_'
Map = StabilityDiagram(folder,prefix)

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 0.2  # integration time (fastseq divider)
Map.step_wait = 0.         # ms wait after every fastseq

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.2
Map.init_val['Rbias'] = 0.2

### LEFT
Map.init_val['LD1'] = -0.885
Map.init_val['LD2'] = -0.85
Map.init_val['LV1'] = -1.25
Map.init_val['LV2'] = -1.6
Map.init_val['LH1'] = -0.9
Map.init_val['LH2'] = -0.6
Map.init_val['LH3'] = -0.6

### RIGHT
Map.init_val['RD1'] = -1.0316
Map.init_val['RD2'] = -0.902
Map.init_val['RV1'] = -1.3
Map.init_val['RV2'] = -1.3
Map.init_val['RH1'] = -1.3
Map.init_val['RH2'] = -0.6
Map.init_val['RH3'] = -1.3

### CHANNEL
Map.init_val['TC'] = -1.3
Map.init_val['BC'] = -1.3

##########################
###	 FASTSEQ			
##########################
Map.sequence.append(['Trigger','1111'])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','0000'])
Map.sequence.append(['RH1',0.])

Map.sequence.append(['RH2',-0.2])
Map.sequence.append(['RH3',0.4])
Map.sequence.append(['Timing',0.05])
Map.sequence.append(['RH3',0.])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['Timing',0.45])

Map.sequence.append(['RH2',-0.063])
Map.sequence.append(['RH3',0.35])
Map.sequence.append(['Timing',0.05])
Map.sequence.append(['RH3',0.])
Map.sequence.append(['RH2',0.])
Map.sequence.append(['Timing',0.45])


Map.sequence.append(['RH2',0.])
Map.sequence.append(['RH1',0.])
Map.sequence.append(['RV1',-0.1])
Map.sequence.append(['BC',-0.1])
Map.sequence.append(['TC',0.])

Map.build_pre_ramp_seq()
##########################
###	 MAP
##########################
Map.sweep_dim = [201,201]
#Map.ramp_DAC('RH3',-0.8,-1.25,0)
#Map.ramp_DAC('RD2',-0.98,-0.96,1)
#Map.ramp_DAC('RH2',-0.55,-0.85,1)
#Map.ramp_DAC('RD1',-0.75,-0.75,1)
Map.ramp_DAC('RH3',-1.3,-1.6,0)
#Map.ramp_DAC('RH1',-1.6,-1.3,0)
Map.ramp_DAC('RD2',-0.83,-0.76,1)
#Map.ramp_DAC('RH2',-0.6,-0.6,1)
Map.ramp_DAC('RD1',-0.92,-0.97,0)
#Map.ramp_slot(15,'dRH1',0.,-0.3,1)
Map.ramp_slot(16,'dRH2',0.,-0.3,1)
#Map.ramp_slot(17,'dRH1',0.,-0.3,1)
#Map.ramp_slot(17,'dRV1',0.,0.,1)
#Map.ramp_slot(18,'dBC',0.,0.,1)
#Map.ramp_slot(19,'dTC',0.,0.,1)

#Map.ramp_DAC('RH3',-0.9,-0.9,1)
#Map.ramp_DAC('RH1',-0.9,-1.5,1)
##Map.ramp_DAC('RD2',-1.115,-1.08,1)
#Map.ramp_DAC('RD2',-1.0975,-1.0975,1)
#Map.ramp_DAC('RD1',-0.7,-1.3,0)

#Map.ramp_DAC('LH3',-1.2,-0.6,0)
#Map.ramp_DAC('LH1',-1.5,-0.9,1)
#Map.ramp_DAC('LD2',-0.68,-0.71,0)
#Map.ramp_DAC('LD1',-0.83,-0.90,1)


#Map.add_wait('wait_bg',0,10000,1) # (index,ms,axis) wait n ms at index for given axis


Map.build_fastramp()
Map.update_timings()
Map.build_sweep()
Map.build_files()