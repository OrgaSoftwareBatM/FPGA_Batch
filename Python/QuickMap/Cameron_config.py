# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 20:25:39 2017

@author: manip.batm
"""

import os,sys
import numpy as np
import MeasurementBase.measurement_classes as mc

# Numerobis parameters
FPGA_address = '192.168.1.21'
addressList = {'K2000':'0:17','K34401A':'0:17','DSP_lockIn':'0:12','RS_RF':'0:28','AWG':'192.168.0.4', 'ATMDelayLine':'COM3'}
    
def DAC_ADC_config():
    ##########################
    ###		 DAC
    ##########################
    DAC_id = {}
    DAC_id['Vg'] = [0,0,1.]
    DAC_id['Vsd'] = [0,1,0.01]
    DAC_id['Vbg'] = [0,2,10.]
    DAC = {}
    for key in DAC_id.keys():
    	panel = DAC_id[key][0]
    	channel = DAC_id[key][1]
    	conv = DAC_id[key][2]
    	DAC[key] = mc.DAC(name = key,
    					 IPAddress = FPGA_address,
    					 unit = 'V',
    					 panel = panel,
    					 channel = channel,
    					 upper_limit = 2.5,
    					 lower_limit = -2.5,
    					 ms2wait = 1,# ms to wait between each bit (~ 150 uV)
    					 conversion = conv,# only for analysis
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
    		fast_channels = [0,1,2,3,4,5,6,7,16,17,18,19,20,21,22,23],
    		start_ramp_at = 0,
    		upper_limit = 5.,
    		lower_limit = -5.,
    		sequence = np.zeros((2,10)),
    		)
    
    ##########################
    ###		 ADC
    ##########################
    ADC = mc.ADC(name='ADC',
    		unit='V',
    		Range={'+/-0.2V':0, '+/-1V':1, '+/-5V':5, '+/-10V':10}['+/-10V'],
    		NofChannels=2,
    		NameList='ADC0;ADC1',
    		UnitList='V;V',
    		ConversionList='1.0;1.0',
    		samplingRate=1000000,
    		Realtime=0,
    		RTaverage=100,
    		InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
    		BufferSize=1000000,
    		SamplePerChannel=1,
    		ramp_trigger_input = 0,
    		fast_seq_trigger_input = 1,
    		)
    
    return DAC,fs,ADC