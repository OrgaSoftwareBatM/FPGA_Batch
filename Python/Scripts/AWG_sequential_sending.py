# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

#Map = AWG_map(sweep_dim=[121],waveform_duration=4000)
Map = AWG_map(sweep_dim=[2,1],waveform_duration=12000)
#Map = AWG_map(sweep_dim=[201],waveform_duration=30000)
#Map = AWG_map(sweep_dim=[1],waveform_duration=7000)

Map.wait_dim = 0
#Map.wait_dim = len(Map.sweep_dim)-1

SAW_protec = WE.Pulse(name = 'SAW_protec',\
                 channel = 'awg_RP1',\
                 Amplitude = +3.,\
                 Duration = 8000.,\
                 unit = 'ns',\
                 Delay = -3500.+5000.,\
                 )
#SAW_protec.ramp_parameter('V_{protect, RP1}','Amplitude',0,+3.,1)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Duration',0.,100,2)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Delay',1000+470.,1000+430.,1)
Map.add_object(SAW_protec)

SAW_small = WE.Pulse(name = 'SAW_small',\
                 channel = 'awg_RP1',\
                 Amplitude = -2.-3.,\
                 Duration = 3./1.2,\
                 unit = 'ns',\
                 Delay = 440+5000.,\
                 )
#SAW_small.ramp_parameter('V_{sending1, RP1}','Amplitude',0,-7.5,2)
SAW_small.ramp_parameter('t_{sending1, RP1}','Duration',2.5,0.,1)
#SAW_small.ramp_parameter('t_{sending1, RP1}','Delay',5000+420.,5000+460.,1)
Map.add_object(SAW_small)
#
SAW_attac = WE.Pulse(name = 'SAW_attac',\
                 channel = 'awg_RP1',\
                 Amplitude = -0.75-3.,\
                 Duration = 3./1.2,\
                 unit = 'ns',\
                 Delay = 340+5000.,\
                 )
#SAW_attac.ramp_parameter('V_{sending2, RP1}','Amplitude',0.,-7.5,2)
SAW_attac.ramp_parameter('t_{sending2, RP1}','Duration',0,102.5,1)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',5000+512.5,5000+437.5,2)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',1000+440.,1000+443.3,3)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',1000+540.,1000+420,1)
Map.add_object(SAW_attac)
#
#SAW_attac = WE.Pulse(name = 'SAW_attac_2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 3./1.2,\
#                 unit = 'ns',\
#                 Delay = 440+5000.,\
#                 )
##SAW_attac.ramp_parameter('V_{sending2, RP2}','Amplitude',4.5,-4.5,3)
##SAW_attac.ramp_parameter('t_{sending2, RP2}','Duration',0,2.5,1)
#SAW_attac.ramp_parameter('t_{sending2, RP2}','Delay',5000+512.5,5000+437.5,2)
##SAW_attac.ramp_parameter('t_{sending2, RP2}','Delay',1000+440.,1000+443.3,3)
##SAW_attac.ramp_parameter('t_{sending2, RP2}','Delay',1000+540.,1000+420,1)
#Map.add_object(SAW_attac)


#pulse = WE.Pulse(name = 'V_{mixing, RP1}',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -4.5,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 5000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.,-4.5,2)
##pulse.ramp_parameter('t_{mixing, RP1}','Duration',0.,500.,1)
#Map.add_object(pulse)


#pulse = WE.Pulse(name = 'V_{mixing, RP2}',\
#                 channel = 'awg_RP2',\
#                 Amplitude = +1.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 5000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.,-2,1)
#pulse.ramp_parameter('t_{mixing, RP1}','Duration',0.,500.,1)
#Map.add_object(pulse)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements)