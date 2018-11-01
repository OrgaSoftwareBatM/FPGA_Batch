# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

Map = AWG_map(sweep_dim=[1,2,61],waveform_duration=2000)

pulse = WE.Pulse(name = 'V_{AWG, RP1}',\
                 channel = 'awg_RP1',\
                 Amplitude = -4.5,\
                 Duration = 2.5,\
                 unit = 'ns',\
                 Delay = 335,\
                 )
#pulse.ramp_parameter('V_{AWG, RP1}','Amplitude',0.,-4.5,3)
#pulse.ramp_parameter('t_{pulse, RP1}','Duration',0.,10.,4)
#pulse.ramp_parameter('t_{pulse, RP1}','Delay',310.,360.,4)
Map.add_object(pulse)

pulse = WE.Pulse(name = 'V_{AWG, LP1}',\
                 channel = 'awg_LP1',\
                 Amplitude = -4.5,\
                 Duration = 5.,\
                 unit = 'ns',\
                 Delay = 310.,\
                 )
#pulse.ramp_parameter('V_{AWG, LP1}','Amplitude',0.,-4.5,3)
#pulse.ramp_parameter('t_{pulse, LP1}','Duration',0.,100.,3)
pulse.ramp_parameter('t_{pulse, LP1}','Delay',300.,400.,3)
Map.add_object(pulse)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements)