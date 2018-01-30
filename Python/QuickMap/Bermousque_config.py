# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:38:49 2018

@author: manip.batm
"""
import os,sys
sys.path.append('..')
import numpy as np
import MeasurementBase.measurement_classes as mc

# Merlin parameters
FPGA_address = '192.168.137.11'
addressList = {'K2000':'0:17','K34401A':'0:17','DSP_lockIn':'0:12','RS_RF':'0:19','AWG':'192.168.0.4', 'ATMDelayLine':'COM3'}
    
def DAC_ADC_config():
    ##########################
    ###		 DAC
    ##########################
    DAC_id = {}
    DAC_id['LD1'] = [0,0]
    DAC_id['LD2'] = [0,1]
    DAC_id['LV1'] = [0,2]
    DAC_id['LV2'] = [0,3]
    DAC_id['LH1'] = [0,4]
    DAC_id['LH2'] = [0,5]
    DAC_id['LH3'] = [0,6]
    DAC_id['RD1'] = [1,0]
    DAC_id['RD2'] = [1,1]
    DAC_id['RV1'] = [1,2]
    DAC_id['RV2'] = [1,3]
    DAC_id['RH1'] = [1,4]
    DAC_id['RH2'] = [1,5]
    DAC_id['RH3'] = [1,6]
    DAC_id['TC'] = [2,0]
    DAC_id['BC'] = [2,1]
    DAC_id['Lbias'] = [3,0]
    DAC_id['Rbias'] = [3,1]
    DAC = {}
    for key in DAC_id.keys():
        if key in ['Lbias','Rbias']:
            limits = [-0.5,0.5]
        else:
            limits = [-2.,0.]
        panel = DAC_id[key][0]
        channel = DAC_id[key][1]
        DAC[key] = mc.DAC(name = key,
    					 IPAddress = FPGA_address,
    					 unit = 'V',
    					 panel = panel,
    					 channel = channel,
    					 upper_limit = limits[1],
    					 lower_limit = limits[0],
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
    		fast_channels = [0,1,2,3,4,5,6,8,9,10,11,12,13,14,16,17],
    		start_ramp_at = 2,
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
    		RTaverage=250,
    		InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
    		BufferSize=1000000,
    		SamplePerChannel=1,
    		ramp_trigger_input = 0,
    		fast_seq_trigger_input = 1,
    		)
    
    return DAC,fs,ADC