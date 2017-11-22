# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 20:25:39 2017

@author: manip.batm
"""

import os,sys
import numpy as np
import MeasurementBase.measurement_classes as mc
from configparser import ConfigParser
import sys
sys.path.insert(0,'..') # import parent directory

""" Fridge specific parameters """
config = ConfigParser()
config.read('../Fridge_settings.ini')
FPGA_address = config.get('Instruments','FPGA')
addressList = {}
keys = ['K2000','K34401A','DSP_lockIn','RS_RF','AWG','ATMDelayLine','RF_Attn']
for key in keys:
    addressList[key] = config.get('Instruments',key)

def DAC_ADC_config():
    ##########################
    ###		 DAC
    ##########################
    DAC_id = {}
    DAC_id['0:0'] = [0,0]
    DAC_id['0:1'] = [0,1]
    DAC_id['0:2'] = [0,2]
    DAC_id['0:3'] = [0,3]
    DAC_id['0:4'] = [0,4]
    DAC_id['0:5'] = [0,5]
    DAC_id['0:6'] = [0,6]
    DAC_id['0:7'] = [0,7]
    DAC_id['1:0'] = [1,0]
    DAC_id['1:1'] = [1,1]
    DAC_id['1:2'] = [1,2]
    DAC_id['1:3'] = [1,3]
    DAC_id['1:4'] = [1,4]
    DAC_id['1:5'] = [1,5]
    DAC_id['1:6'] = [1,6]
    DAC_id['1:7'] = [1,7]
    DAC_id['2:0'] = [2,0]
    DAC_id['2:1'] = [2,1]
    DAC_id['2:2'] = [2,2]
    DAC_id['2:3'] = [2,3]
    DAC_id['2:4'] = [2,4]
    DAC_id['2:5'] = [2,5]
    DAC_id['2:6'] = [2,6]
    DAC_id['2:7'] = [2,7]
    DAC_id['3:0'] = [3,0]
    DAC_id['3:1'] = [3,1]
    DAC_id['3:2'] = [3,2]
    DAC_id['3:3'] = [3,3]
    DAC_id['3:4'] = [3,4]
    DAC_id['3:5'] = [3,5]
    DAC_id['3:6'] = [3,6]
    DAC_id['3:7'] = [3,7]
    DAC_id['4:0'] = [4,0]
    DAC_id['4:1'] = [4,1]
    DAC_id['4:2'] = [4,2]
    DAC_id['4:3'] = [4,3]
    DAC_id['4:4'] = [4,4]
    DAC_id['4:5'] = [4,5]
    DAC_id['4:6'] = [4,6]
    DAC_id['4:7'] = [4,7]
    DAC = {}
    for key in DAC_id.keys():
    	panel = DAC_id[key][0]
    	channel = DAC_id[key][1]
    	DAC[key] = mc.DAC(name = key,
    					 IPAddress = FPGA_address,
    					 unit = 'V',
    					 panel = panel,
    					 channel = channel,
    					 upper_limit = 5.,
    					 lower_limit = -5.,
    					 ms2wait = 1,# ms to wait between each bit (~ 150 uV)
    					 conversion = 1.0,# only for analysis
    					 )
    
    ##########################
    ###		 FastSeq
    ##########################
    fs = mc.FastSequences(IPAddress = FPGA_address,
    		Unit = 'V',
    		fastSequenceDivider = 44444, #averaging time for ramp mode
    		triggerLength = 300, # Trigger length for ramp mode
    		SampleCount = 200, # Number of points for fast sequence mode
    		send_all_points = 0,
    		fast_channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
    		start_ramp_at = 0,
    		upper_limit = 2.,
    		lower_limit = -2.,
    		sequence = np.zeros((2,10)),
    		)
    
    ##########################
    ###		 FPGA_ADC
    ##########################
    ADC = mc.FPGA_ADC(name='FPGA_ADC',
                 address=FPGA_address,
                 name_list='ADC0;ADC1',
                 unit_list='V;V',
                 conv_list='1.0;1.0',
                 channel_list='0;1',
                 range_list='10;10',
                 term_list='DIFF;DIFF',
                 Nchannels=2,
                 sampling_rate=250000,
                 RTaverage=100,
                 trig_mode=0,
                 trig_input=1,
                 trig_edge=0,
                 samples_per_channel=1)
    
    return DAC,fs,ADC