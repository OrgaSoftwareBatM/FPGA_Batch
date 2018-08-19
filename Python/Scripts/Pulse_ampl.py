# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

Map = AWG_map(sweep_dim=[101],waveform_duration=2000)

#pulse = WE.Pulse(name = 'V_{AWG, LP1}',\
#                 channel = 'awg_LP1',\
#                 Amplitude = -3.,\
#                 Duration = 100.,\
#                 unit = 'ns',\
#                 Delay = 10.,\
#                 )
#pulse.ramp_parameter('V_{AWG, LP1}','Amplitude',0.,-2.,1)
##pulse.ramp_parameter('t_{pulse, LP1}','Duration',0.,40.,1)
#Map.add_object(pulse)
#
#pulse = WE.Pulse(name = 'V_{AWG, LP2}',\
#                 channel = 'awg_LP2',\
#                 Amplitude = -2.,\
#                 Duration = 100.,\
#                 unit = 'ns',\
#                 Delay = 10.,\
#                 )
#pulse.ramp_parameter('V_{AWG, LP2}','Amplitude',0.,4.5,1)
#Map.add_object(pulse)

rabi = WE.Rabi(name = 'Rabi_LP1',\
                channel = 'awg_LP1',\
                Vramp = -0.7,\
                V11 = -2.,\
                Vexch = -0.72,\
                Delay = 25,\
                Tramp = 250,\
                T11 = 50,\
                Texch = 5,\
                unit = 'ns',\
                )
rabi.ramp_parameter('t_{exch, LP1}','Texch',0,100.,1)
#rabi.ramp_parameter('V_{exch, LP1}','Vexch',-0.5,-1.,2)
Map.add_object(rabi)

rabi = WE.Rabi(name = 'Rabi_LP2',\
                channel = 'awg_LP2',\
                Vramp = +1.575,\
                V11 = +4.5,\
                Vexch = +1.62,\
                Delay = 25,\
                Tramp = 250,\
                T11 = 50,\
                Texch = 5,\
                unit = 'ns',\
                )
rabi.ramp_parameter('t_{exch, LP2}','Texch',0,100.,1)
#rabi.ramp_parameter('V_{exch, LP2}','Vexch',+1.125,+2.25,2)
Map.add_object(rabi)

Map.build_all()
Map.update_h5()
AWG_fast_send(Map.waveforms,Map.channel_names)