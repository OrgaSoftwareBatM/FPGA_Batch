# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

Map = AWG_map(sweep_dim=[41,41],waveform_duration=2000)

#pulse = WE.Pulse(name = 'V_{AWG, LP1}',\
#                 channel = 'awg_LP1',\
#                 Amplitude = -1.,\
#                 Duration = 100.,\
#                 unit = 'ns',\
#                 Delay = 50.,\
#                 )
##pulse.ramp_parameter('V_{AWG, LP1}','Amplitude',0.,2.,1)
##pulse.ramp_parameter('t_{pulse, LP1}','Duration',0.,100,2)
#Map.add_object(pulse)
#
#pulse = WE.Pulse(name = 'V_{AWG, LP2}',
#                 channel = 'awg_LP2',
#                 Amplitude = -4.5,
#                 Duration = 100.,
#                 unit = 'ns',
#                 Delay = 50.,
#                 )
##pulse.ramp_parameter('V_{AWG, LP2}','Amplitude',0,-4.5,1)
##pulse.ramp_parameter('t_{pulse, LP2}','Duration',0.,50.,1)
#Map.add_object(pulse)

pulse = WE.Pulse(name = 'V_{AWG, RP1}',\
                 channel = 'awg_RP1',\
                 Amplitude = -2.,\
                 Duration = 10.,\
                 unit = 'ns',\
                 Delay = 435.,\
                 )
pulse.ramp_parameter('V_{AWG, RP1}','Amplitude',-2.,+2.,1)
#pulse.ramp_parameter('t_{pulse, RP1}','Duration',0.,100,2)
#pulse.ramp_parameter('t_{pulse, RP1}','Delay',200.,450.,1)
Map.add_object(pulse)

pulse = WE.Pulse(name = 'V_{AWG, RP2}',\
                 channel = 'awg_RP2',\
                 Amplitude = +4.5,\
                 Duration = 10.,\
                 unit = 'ns',\
                 Delay = 435.,\
                 )
pulse.ramp_parameter('V_{AWG, RP2}','Amplitude',+4.5,-4.5,2)
#pulse.ramp_parameter('t_{pulse, RP2}','Duration',0.,50.,1)
#pulse.ramp_parameter('t_{pulse, RP2}','Delay',200.,450.,1)
Map.add_object(pulse)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements)