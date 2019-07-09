# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

Map = AWG_map(sweep_dim=[126],waveform_duration=4000)

rabi = WE.Rabi(name = 'Rabi_RP1',\
                channel = 'awg_RP1',\
                Vramp = -1.25,\
                V11 = -3.,\
                Vexch = -1.36,\
                Delay = 1000,\
                Tramp = 500,\
                T11 = 50,\
                Texch = 15.,\
                unit = 'ns',\
                )
#rabi.ramp_parameter('t_{ramp, RP1}','Tramp',0.,500.,1)
#rabi.ramp_parameter('t_{exch, RP1}','Texch',70,0.,1)
#rabi.ramp_parameter('V_{exch, RP1}','Vexch',0.,-2,1)
rabi.ramp_parameter('V_{11, RP1}','V11',-2.,-4.5,1)
Map.add_object(rabi)

#rabi = WE.Rabi(name = 'Rabi_RP2',\
#                channel = 'awg_RP2',\
#                Vramp = -2.25*0.62,\
#                V11 = -2.25*2,\
#                Vexch = -2.25*0.6,\
#                Delay = 50,\
#                Tramp = 500,\
#                T11 = 50,\
#                Texch = 15.,\
#                unit = 'ns',\
#                )
##rabi.ramp_parameter('t_{ramp, RP2}','Tramp',0,300.,1)
#rabi.ramp_parameter('t_{exch, RP2}','Texch',70,0.,1)
#rabi.ramp_parameter('V_{exch, RP2}','Vexch',-4.5,4.5,2)
#Map.add_object(rabi)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements)