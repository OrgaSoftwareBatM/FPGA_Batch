# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

#Map = AWG_map(sweep_dim=[101],waveform_duration=4000)
Map = AWG_map(sweep_dim=[1,101],waveform_duration=4000)
#Map = AWG_map(sweep_dim=[201],waveform_duration=30000)
#Map = AWG_map(sweep_dim=[100,2],waveform_duration=7000)

Map.wait_dim = 1
#Map.wait_dim = len(Map.sweep_dim)-1
Map.SAW_marker = [True]

mix1_bools = [True]
saw_bools = [True]
mix2_bools = [True]

#######################
######### SAW #########
#######################

SAW_protec = WE.Pulse(name = 'SAW_protec_RP1',\
                 channel = 'awg_RP1',\
                 Amplitude = 3.,\
                 Duration = 3000.,\
                 unit = 'ns',\
                 Delay = 200.,\
                 )
#SAW_protec.ramp_parameter('V_{protect, RP1}','Amplitude',0.05,0.05,1)
#SAW_protec.ramp_parameter('V_{protect, RP1}','Amplitude',-4.5,+3.,1)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Duration',0.,100,2)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Delay',1000+470.,1000+430.,1)
Map.add_object(SAW_protec,enable_bools=saw_bools)

#SAW_protec = WE.Pulse(name = 'SAW_protec_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 3000.,\
#                 unit = 'ns',\
#                 Delay = 200.,\
#                 )
##SAW_protec.ramp_parameter('V_{protect, RP2}','Amplitude',-4.5,+4.5,2)
##SAW_protec.ramp_parameter('t_{protect, RP2}','Duration',0.,100,2)
##SAW_protec.ramp_parameter('t_{protect, RP1}','Delay',1000+470.,1000+430.,1)
#Map.add_object(SAW_protec,enable_bools=saw_bools)

#SAW_small = WE.Pulse(name = 'SAW_small_RP1',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -2.4,\
#                 Duration = 3./1.2,\
#                 unit = 'ns',\
#                 Delay = 2005.,\
#                 )
##SAW_small.ramp_parameter('V_{sending1, RP1}','Amplitude',0,-4.5,1)
##SAW_small.ramp_parameter('t_{sending1, RP1}','Duration',42.5,2.5,2)
##SAW_small.ramp_parameter('dt_{sending1, RP1}','Delay',1440-40.,1440,2)
#Map.add_object(SAW_small,enable_bools=saw_bools)

#SAW_small = WE.Pulse(name = 'SAW_small_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 3./1.2,\
#                 unit = 'ns',\
#                 Delay = 2005.,\
#                 )
##SAW_small.ramp_parameter('V_{sending1, RP2}','Amplitude',0,-4.5,1)
##SAW_small.ramp_parameter('t_{sending1, RP2}','Duration',42.5,2.5,2)
##SAW_small.ramp_parameter('dt_{sending1, RP2}','Delay',1440-40.,1440,2)
#Map.add_object(SAW_small,enable_bools=saw_bools)

SAW_attac = WE.Pulse(name = 'SAW_attac_RP1',\
                 channel = 'awg_RP1',\
                 Amplitude = -4.5,\
                 Duration = 2.5,\
                 unit = 'ns',\
                 Delay = 2005,\
                 )
SAW_attac.ramp_parameter('V_{sending2, RP1}','Amplitude',-4.5,3.,1)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Duration',2.5,102.5,1)
#SAW_attac.ramp_parameter('dt_{sending2, RP1}','Delay',1000.,2200.,2)
Map.add_object(SAW_attac,enable_bools=saw_bools)

#SAW_attac = WE.Pulse(name = 'SAW_attac_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 2.5,\
#                 unit = 'ns',\
#                 Delay = 490+20000.,\
#                 )
##SAW_attac.ramp_parameter('V_{sending2, RP2}','Amplitude',-4.5,+4.5,3)
##SAW_attac.ramp_parameter('t_{sending2, RP2}','Duration',0.,120.,1)
##SAW_attac.ramp_parameter('dt_{sending2, RP2}','Delay',20440.,20500,2)
#Map.add_object(SAW_attac,enable_bools=saw_bools)


#pulse = WE.Pulse(name = 'V_{mixing2, LP1}',\
#                 channel = 'awg_LP1',\
##                 Amplitude = -1.2,\
#                 Amplitude = -0.5,\
#                 Duration = 300.,\
#                 unit = 'ns',\
#                 Delay = 450+5000.,\
#                 )
##pulse.ramp_parameter('V_{mixing2, LP1}','Amplitude',-1.2,-2.8,1)
#pulse.ramp_parameter('t_{mixing2, LP1}','Duration',300.,0.,1)
#Map.add_object(pulse)
#
#pulse = WE.Pulse(name = 'V_{mixing, LP2}',\
#                 channel = 'awg_LP2',\
#                 Amplitude = 0.,\
#                 Duration = 300.,\
#                 unit = 'ns',\
#                 Delay = 450+5000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, LP2}','Amplitude',-0.2,+0.2,1)
##pulse.ramp_parameter('t_{mixing, LP2}','Duration',0.,500.,1)
#Map.add_object(pulse)

#pulse = WE.Pulse(name = 'Mixing_RP1',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -1.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 20000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',3.,-4.5,2)
##pulse.ramp_parameter('t_{mixing, RP1}','Duration',120.,0.,1)
##pulse.ramp_parameter('t_{mixing, RP2}','Delay',200.,450.,2)
#Map.add_object(pulse)
###
#pulse = WE.Pulse(name = 'Mixing_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 20000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',-4.5,4.5,3)
##pulse.ramp_parameter('t_{mixing, RP2}','Duration',0.,300.,2)
##pulse.ramp_parameter('t_{mixing, RP2}','Delay',200.,450.,2)
#Map.add_object(pulse)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements,Map.SAW_elements)