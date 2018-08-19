# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

Map = AWG_map(sweep_dim=[11,6],waveform_duration=2000)

pulse = WE.Pulse(name = 'Pulse1_RP1',\
                 channel = 'awg_RP1',\
                 Amplitude = -2.,\
                 Duration = 100.,\
                 unit = 'ns',\
                 Delay = 10.,\
                 )
pulse.ramp_parameter('Pulse1_RP1_ampl','Amplitude',0.,-2.,1)
Map.add_object(pulse)

rabi = WE.Rabi(name = 'Rabi1_RP2',\
                channel = 'awg_RP2',\
                Vramp = 0.8,\
                V11 = 1.5,\
                Vexch = 1.,\
                Delay = 25,\
                Tramp = 250,\
                T11 = 50,\
                Texch = 10,\
                unit = 'ns',\
                )
rabi.ramp_parameter('Rabi1_Texch','Texch',10,20,1)
rabi.ramp_parameter('Rabi1_Vexch','Vexch',0.5,1.,2)
Map.add_object(rabi)

Map.build_all()
Map.update_h5()
AWG_fast_send(Map.waveforms,Map.channel_names)