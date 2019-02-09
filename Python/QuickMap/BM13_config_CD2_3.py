# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:38:49 2018

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from configobj import ConfigObj
import MeasurementBase.measurement_classes as mc

# Import parameters
config_file = ConfigObj('..\\Fridge_settings.ini')
addr_dict = config_file['Instruments']
    
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
    DAC_id['LP2'] = [2,2]
    DAC_id['RP2'] = [2,3]
    DAC_id['Lbias'] = [3,0]
    DAC_id['Rbias'] = [3,1]
    DAC = {}
    for key in DAC_id.keys():
        if key in ['Lbias','Rbias']:
            limits = [-0.5,0.5]
        else:
            limits = [-2.2,0.]
        panel = DAC_id[key][0]
        channel = DAC_id[key][1]
        DAC[key] = mc.DAC(name = key,
    					 IPAddress = addr_dict['FPGA'],
    					 unit = 'V',
    					 panel = panel,
    					 channel = channel,
    					 lower_limit = limits[0],
    					 upper_limit = limits[1],
    					 ms2wait = 1,# ms to wait between each bit (~ 150 uV)
    					 conversion = 1.0,# only for analysis
    					 )
    
    ##########################
    ###		 FastSeq
    ##########################
    fs = mc.FastSequences(IPAddress = addr_dict['FPGA'],
    		Unit = 'V',
    		fastSequenceDivider = 44444, #averaging time for ramp mode
    		triggerLength = 300, # Trigger length for ramp mode
    		SampleCount = 200, # Number of points for fast sequence mode
    		send_all_points = 0,
    		fast_channels = [1,2,3,4,5,6,9,10,11,12,13,14,16,17,18,19],
    		start_ramp_at = 2,
    		upper_limit = 2,
    		lower_limit = -2,
    		sequence = np.zeros((2,10)),
    		)
    
    ##########################
    ###		 ADC 2 Channels
    ##########################
    ADC = mc.ADC(name='ADC',
                 SourceList='0;1',
                 NameList='V_{RF,L};V_{RF,R}',
                 UnitList='mV;mV',
                 ConversionList='1000;1000',
                 NofChannels=2,
                 samplingRate=200000,
                 downsampling=100,
                 Analysis_type=0,
                 sample_count=100,
                 InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
                 BufferSize=1000000,
                 SamplePerChannel=1,
                 trigger_input = 0,
                 minimum_value = -0.2,
                 maximum_value = 0.2)
    
#    ##########################
#    ###		 ADC 1 Channel
#    ##########################
#    ADC = mc.ADC(name='ADC',
#                 SourceList='1',
#                 NameList='V_{RF,R}',
#                 UnitList='mV',
#                 ConversionList='1000',
#                 NofChannels=1,
#                 samplingRate=200000,
#                 downsampling=100,
#                 Analysis_type=0,
#                 sample_count=100,
#                 InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
#                 BufferSize=1000000,
#                 SamplePerChannel=1,
#                 trigger_input = 0,
#                 minimum_value = 0.,
#                 maximum_value = 0.1)
    
#    ##########################
#    ###		 ADC Trigger
#    ##########################
#    ADC = mc.ADC(name='ADC',
#                 SourceList='2',
#                 NameList='RF_Trigger',
#                 UnitList='V',
#                 ConversionList='1.0',
#                 NofChannels=1,
#                 samplingRate=200000,
#                 downsampling=100,
#                 Analysis_type=0,
#                 sample_count=100,
#                 InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
#                 BufferSize=1000000,
#                 SamplePerChannel=1,
#                 trigger_input = 0,
#                 minimum_value = -0.1,
#                 maximum_value = 0.1)
    
    return DAC, fs, ADC

def RF_config():
    ##########################
    ### RF SYNTH FOR REFLECTO
    ##########################
    RF = {}
    RF['RF0_{freq}'] = mc.RF_Synth(name='RF0_{freq}',
                GPIBAddress=addr_dict['RF_Synth'],
                Unit='GHz',
                channel = 0, # 0: channel A, else: channel B (for dual output synth)
                controlParam = 0, # selection of control parameter, which is used to get the initial value of the parameter
                frequency=0.2, # GHz
                power=-30, # dBm
                phase=0., # deg
                output_on = 1, # boolean
                trig_mode = 0, # 0: none, 1: ON/OFF on trigger
                freq_ul=13.6, # frequency upper limit
                freq_ll=0.054, # frequency lower limit
                power_ul=20., # power upper limit
                power_ll=-60, # power lower limit
                )

    RF['RF0_{power}'] = mc.RF_Synth(name='RF0_{power}',
                GPIBAddress=addr_dict['RF_Synth'],
                Unit='dB',
                channel = 0, # 0: channel A, else: channel B (for dual output synth)
                controlParam = 1, # selection of control parameter, which is used to get the initial value of the parameter
                frequency=0.2, # GHz
                power=-30, # dBm
                phase=0., # deg
                output_on = 1, # boolean
                trig_mode = 0, # 0: none, 1: ON/OFF on trigger
                freq_ul=13.6, # frequency upper limit
                freq_ll=0.054, # frequency lower limit
                power_ul=20., # power upper limit
                power_ll=-60, # power lower limit
                )

    RF['RF1_{freq}'] = mc.RF_Synth(name='RF1_{freq}',
                GPIBAddress=addr_dict['RF_Synth'],
                Unit='GHz',
                channel = 1, # 0: channel A, else: channel B (for dual output synth)
                controlParam = 0, # selection of control parameter, which is used to get the initial value of the parameter
                frequency=0.2, # GHz
                power=-30, # dBm
                phase=0., # deg
                output_on = 1, # boolean
                trig_mode = 0, # 0: none, 1: ON/OFF on trigger
                freq_ul=13.6, # frequency upper limit
                freq_ll=0.054, # frequency lower limit
                power_ul=20., # power upper limit
                power_ll=-60, # power lower limit
                )

    RF['RF1_{power}'] = mc.RF_Synth(name='RF1_{power}',
                GPIBAddress=addr_dict['RF_Synth'],
                Unit='dB',
                channel = 1, # 0: channel A, else: channel B (for dual output synth)
                controlParam = 1, # selection of control parameter, which is used to get the initial value of the parameter
                frequency=0.2, # GHz
                power=-30, # dBm
                phase=0., # deg
                output_on = 1, # boolean
                trig_mode = 0, # 0: none, 1: ON/OFF on trigger
                freq_ul=13.6, # frequency upper limit
                freq_ll=0.054, # frequency lower limit
                power_ul=20., # power upper limit
                power_ll=-60, # power lower limit
                )

    RF['SAW_{freq}'] = mc.RS_RF(name='SAW_{freq}',
                 GPIBAddress=addr_dict['RS_RF'],
                 Unit='GHz',
                 frequency=2.644, # GHz
                 power=25, # dBm
                 pulse_period = 200, #us
                 pulse_width = 0.1, #us
                 pulse_delay = 200., #us
                 pulse_modulation = 1, # boolean
                 output_on = 1, # boolean
                 pulse_source = 0, # boolean, 0: internal, 1: external
                 pulse_mode = 0, # 0: single, 1: double, 2: train
                 trigger_mode = 1, # 0: auto, 1: external, 2: external gate, 3: single  
                 ex_trigger_input_slope = 1, # boolean, 0: negative, else: positive
                 external_impedance = 0, # 0: 10 kohm, else: 50 ohm
                 frequency_ul=6.001, # GHz upper limit
                 frequency_ll=9e-6, # GHz lower limit
                 power_ul=30, # dBm upper limit
                 power_ll=-145, # dBm lower limit
                 controlParam = 0, # selection of control parameter, which is used to get the initial value of the parameter
                 )

    RF['SAW_{power}'] = mc.RS_RF(name='SAW_{power}',
                 GPIBAddress=addr_dict['RS_RF'],
                 Unit='dBm',
                 frequency=2.644, # GHz
                 power=25, # dBm
                 pulse_period = 200, #us
                 pulse_width = 0.1, #us
                 pulse_delay = 200., #us
                 pulse_modulation = 1, # boolean
                 output_on = 1, # boolean
                 pulse_source = 0, # boolean, 0: internal, 1: external
                 pulse_mode = 0, # 0: single, 1: double, 2: train
                 trigger_mode = 1, # 0: auto, 1: external, 2: external gate, 3: single  
                 ex_trigger_input_slope = 1, # boolean, 0: negative, else: positive
                 external_impedance = 0, # 0: 10 kohm, else: 50 ohm
                 frequency_ul=6.001, # GHz upper limit
                 frequency_ll=9e-6, # GHz lower limit
                 power_ul=30, # dBm upper limit
                 power_ll=-145, # dBm lower limit
                 controlParam = 1, # selection of control parameter, which is used to get the initial value of the parameter
                 )

    RF['SAW_{width}'] = mc.RS_RF(name='SAW_{width}',
                 GPIBAddress=addr_dict['RS_RF'],
                 Unit='us',
                 frequency=2.644, # GHz
                 power=25, # dBm
                 pulse_period = 200, #us
                 pulse_width = 0.1, #us
                 pulse_delay = 200., #us
                 pulse_modulation = 1, # boolean
                 output_on = 1, # boolean
                 pulse_source = 0, # boolean, 0: internal, 1: external
                 pulse_mode = 0, # 0: single, 1: double, 2: train
                 trigger_mode = 1, # 0: auto, 1: external, 2: external gate, 3: single  
                 ex_trigger_input_slope = 1, # boolean, 0: negative, else: positive
                 external_impedance = 0, # 0: 10 kohm, else: 50 ohm
                 frequency_ul=6.001, # GHz upper limit
                 frequency_ll=9e-6, # GHz lower limit
                 power_ul=30, # dBm upper limit
                 power_ll=-145, # dBm lower limit
                 controlParam = 3, # selection of control parameter, which is used to get the initial value of the parameter
                 )

    RF['SAW_{delay}'] = mc.RS_RF(name='SAW_{delay}',
                 GPIBAddress=addr_dict['RS_RF'],
                 Unit='us',
                 frequency=2.644, # GHz
                 power=25, # dBm
                 pulse_period = 200, #us
                 pulse_width = 0.1, #us
                 pulse_delay = 200., #us
                 pulse_modulation = 1, # boolean
                 output_on = 1, # boolean
                 pulse_source = 0, # boolean, 0: internal, 1: external
                 pulse_mode = 0, # 0: single, 1: double, 2: train
                 trigger_mode = 1, # 0: auto, 1: external, 2: external gate, 3: single  
                 ex_trigger_input_slope = 1, # boolean, 0: negative, else: positive
                 external_impedance = 0, # 0: 10 kohm, else: 50 ohm
                 frequency_ul=6.001, # GHz upper limit
                 frequency_ll=9e-6, # GHz lower limit
                 power_ul=30, # dBm upper limit
                 power_ll=-145, # dBm lower limit
                 controlParam = 4, # selection of control parameter, which is used to get the initial value of the parameter
                 )
    return RF

def Bfield_config():
    ##########################
    ### MERCURY IPS
    ##########################
    MercuryIPS = mc.MercuryIPS(name='MercuryIPS',
                               IP_address=addr_dict['MercuryIPS'],
                               unit='T',
                               axis = 'GRPZ', # only Z axis implemented for now
                               permanent_mode = 0, # not implemented yet
                               wait_after_move = 10, # s
                               upper_limit = 0.5, # T
                               lower_limit = -0.5, # T
                               rate = 0.1) # T/min
    return MercuryIPS