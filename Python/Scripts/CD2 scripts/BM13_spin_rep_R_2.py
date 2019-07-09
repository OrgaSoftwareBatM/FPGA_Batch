# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:48:45 2018

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
from QuickMap.QuickMap_RT_SegmentMode import RT_fastseq
#from QuickMap.QuickMap_RT import RT_fastseq

##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD2\\data2'
#folder = 'C:\\Users\\manip.batm\\Documents\\GitKraken\\FPGA_Batch\\Python\\h5'
prefix = 'RT_spin_segment'
Map = RT_fastseq(folder,prefix)
Map.use_AWG = False

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 1.   # ms before everything
Map.ms_per_point = 0.010 # integration time (RT_avg/ADC_freq)
Map.step_wait = 0.      # ms wait after every fastseq

##########################
###	 INITIAL VALUES
##########################
### BIAS
Map.init_val['Lbias'] = 0.
Map.init_val['Rbias'] = 0.
### LEFT
Map.init_val['LD1'] = -0.705
Map.init_val['LD2'] = -0.82
Map.init_val['LV1'] = -1.45
Map.init_val['LV2'] = -1.45
Map.init_val['LH1'] = -1.9
Map.init_val['LH2'] = -0.75
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
###	 FAST SEQUENCE	
##########################
Map.sequence.append(['Trigger','1110'])
Map.sequence.append(['Timing',1.])
Map.sequence.append(['Trigger','1010'])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['RH2',-0.1])   # LOAD SINGLET
Map.sequence.append(['RH3',0.1])
Map.sequence.append(['RH2',-0.01])
Map.sequence.append(['RH3',-0.15])

Map.sequence.append(['RH3',-0.15])  # SHORT TUNNEL
Map.sequence.append(['RH2',-0.016])
Map.sequence.append(['Timing',0.])

Map.sequence.append(['RH2',0.0])    # CHARGE SENSING
Map.sequence.append(['RH3',-0.15])
Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['Trigger','1010'])

Map.sequence.append(['RH2',-0.1])   # LOAD SINGLET
Map.sequence.append(['RH3',0.1])
Map.sequence.append(['RH2',-0.01])
Map.sequence.append(['RH3',-0.15])

Map.sequence.append(['RH3',-0.15])  # LONG TUNNEL
Map.sequence.append(['RH2',-0.016])
Map.sequence.append(['Timing',0.1])

Map.sequence.append(['RH2',0.0])    # CHARGE SENSING
Map.sequence.append(['RH3',-0.15])
Map.sequence.append(['Trigger','1011'])
Map.sequence.append(['Timing',0.2])
Map.sequence.append(['Trigger','1010'])
    
Map.sequence.append(['Jump',4])
#Map.sequence.append(['Jump',len(Map.sequence)])

##########################
###	 MAP
##########################
#Map.sweep_dim = [12000,10]
Map.sweep_dim = [100,101,101,20]
Map.init_val['RD1'] = -0.746
Map.init_val['RD2'] = -1.

#Map.segment_param = [102.470,88,34]
#Map.segment_param = [105.705, 92, 34]rt
#Map.segment_param = [47.976, 41, 16]
Map.segment_param = [79.080, 28, 15, 47, 15]

#for i in range(101):
#    Map.ramp_slot(9+18*i,'dLH3_{wait,'+str(i)+'}',0.195,0.25,2)
#    Map.ramp_slot(8+18*i,'dLH1_{wait,'+str(i)+'}',0.75,0.66,2)

#Map.ramp_slot(4,'dLH3_{load}',0.22,0.25,2)
#Map.ramp_slot(6,'dRH2_{load}',-0.1,0.05,1)
#Map.ramp_slot(5,'t_{load}',0.1,10.,2,method='log10')
#
#Map.ramp_slot(9,'dRH1_{wait}',-0.15,0.356,1)
#Map.ramp_slot(10,'dRH3_{wait}',-0.45,0.,1)

#Map.ramp_slot(9,'dRH1_{wait}',0.0,0.5,1)
#Map.ramp_slot(11,'dRH2_{wait}',+0.45,-0.3,2)
#Map.ramp_slot(10,'dRH3_{wait}',-0.65,-0.15,1)
#Map.ramp_slot(9,'t_{wait}',0.1,10.,2,method='log10')
#Map.ramp_slot(9,'t_{wait}',8.,8.,1)

#Map.ramp_slot(1,'t_{dummy}',0.1,0.1,1)
#
#Map.ramp_slot(8,'dRH1_{mixing}',0.,0.3,1)
#Map.ramp_slot(13,'dRH2_{crossing,2}',0.,0.3,1)

Map.ramp_slot(9,'dRH2_{short}',-0.6,0.3,1)
Map.ramp_slot(8,'dRH3_{short}',-0.35,0.1,2)

Map.ramp_slot(21,'dRH2_{long}',-0.6,0.3,1)
Map.ramp_slot(20,'dRH3_{long}',-0.35,0.1,2)

#Map.ramp_DAC('RD1',-0.65,-0.8,1)
#Map.ramp_DAC('LD2',-0.75,-0.9,3)

ok_for_launch = Map.build_all()
if ok_for_launch:
    Map.send()