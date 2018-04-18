# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 20:25:39 2017

@author: manip.batm
"""

import os,sys
sys.path.append('..')
import numpy as np
import MeasurementBase.measurement_classes as mc

# Merlin parameters
FPGA_address = '192.168.137.11'
addressList = {'K2000':'0:17','K34401A':'0:17','DSP_lockIn':'0:12','RS_RF':'0:28','AWG':'192.168.0.4', 'ATMDelayLine':'COM3'}
    
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
    					 upper_limit = 0.5,
    					 lower_limit = -2.,
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
    		fast_channels = [16,1,2,3,4,5,6,8,9,10,11,12,13,14,17,18],
    		start_ramp_at = 0,
    		upper_limit = 2,
    		lower_limit = -2,
    		sequence = np.zeros((2,10)),
    		)
    
    ##########################
    ###		 ADC
    ##########################
    ADC = mc.ADC(name='ADC',
    		unit='V',
    		Range={'+/-0.2V':0, '+/-1V':1, '+/-5V':5, '+/-10V':10}['+/-10V'],
    		NofChannels=1,
    		NameList='ADC0',
    		UnitList='nA',
    		ConversionList='10',
    		samplingRate=250000,
    		Realtime=0,
    		RTaverage=100,
    		InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
    		BufferSize=1000000,
    		SamplePerChannel=1,
    		ramp_trigger_input = 0,
    		fast_seq_trigger_input = 1,
    		)

    return DAC,fs,ADC