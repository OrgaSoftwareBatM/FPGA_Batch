# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

#Map = AWG_map(sweep_dim=[51,51],waveform_duration=7500)
Map = AWG_map(sweep_dim=[101],waveform_duration=4000)
#Map = AWG_map(sweep_dim=[91,2],waveform_duration=60000)
Map.wait_dim = 0
#
pulse = WE.Pulse(name = 'V_{mixing, LP1}',\
                 channel = 'awg_LP1',\
                 Amplitude = -3.5,\
                 Duration = 500.,\
                 unit = 'ns',\
                 Delay = 2000.,\
                 )
pulse.ramp_parameter('V_{mixing, LP1}','Amplitude',0.5,-4.5,1)
#pulse.ramp_parameter('V_{mixing, LP1}','Amplitude',-4.,-2.,1)
#pulse.ramp_parameter('t_{pulse, LP1}','Duration',0.,50.,1)
Map.add_object(pulse)
##
pulse = WE.Pulse(name = 'V_{mixing, RP1}',\
                 channel = 'awg_RP1',\
                 Amplitude = -3.,\
                 Duration = 200.,\
                 unit = 'ns',\
                 Delay = 2000.,\
                 )
#pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.5,-4.5,2)
pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.5,-4.5,1)
#pulse.ramp_parameter('t_{mixing, RP1}','Duration',0.,500.,2)
##pulse.ramp_parameter('t_{mixing, RP2}','Delay',200.,450.,2)
Map.add_object(pulse)

#pulse = WE.Pulse(name = 'V_{mixing, LP2}',
#                 channel = 'awg_LP2',
#                 Amplitude = 4.5,
#                 Duration = 200.,
#                 unit = 'ns',
#                 Delay = 3000.,
#                 )
#pulse.ramp_parameter('V_{mixing, LP2}','Amplitude',-4.5,4.5,2)
##pulse.ramp_parameter('V_{mixing, LP2}','Amplitude',-4.5,4.5,1)
##pulse.ramp_parameter('t_{pulse, LP2}','Duration',0.,50.,1)
#Map.add_object(pulse)
#
#rabi = WE.Rabi(name = 'Rabi_RP1',\
#                channel = 'awg_RP1',\
#                Vramp = -1.,\
#                V11 = -2.,\
#                Vexch = 0.,\
#                Delay = 2000,\
#                Tramp = 500,\
#                T11 = 100.,\
#                Texch = 0.,\
#                unit = 'ns',\
#                )
#rabi.ramp_parameter('t_{ramp, RP1}','Tramp',0.,380.,2)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',0,15,2)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',0,70,1)
##rabi.ramp_parameter('V_{exch, RP1}','Vexch',-3.75,-1.75,1)
##rabi.ramp_parameter('V_{ramp, RP1}','Vramp',-1.,-2.5,2)
#rabi.ramp_parameter('V_{11, RP1}','V11',-1.,-3.,1)
#Map.add_object(rabi)
#
#rabi = WE.Rabi(name = 'Rabi_RP2',\
#                channel = 'awg_RP2',\
#                Vramp = -4.5,\
#                V11 = +4.5,\
#                Vexch = 0.,\
#                Delay = 2000,\
#                Tramp = 500,\
#                T11 = 100.,\
#                Texch = 0.,\
#                unit = 'ns',\
#                )
#rabi.ramp_parameter('t_{ramp, RP2}','Tramp',0.,380.,2)
##rabi.ramp_parameter('t_{exch, RP2}','Texch',0,15,2)
##rabi.ramp_parameter('t_{exch, RP2}','Texch',0,70,1)
##rabi.ramp_parameter('V_{exch, RP2}','Vexch',-4.5,+4.5,1)
##rabi.ramp_parameter('V_{ramp, RP2}','Vramp',-4.5,+2.25,2)
#rabi.ramp_parameter('V_{11, RP2}','V11',-4.5,+4.5,1)
#Map.add_object(rabi)
#
#pulse = WE.Pulse(name = 'V_{mixing, RP2}',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -2.5,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',-4.5,4.5,1)
##pulse.ramp_parameter('t_{mixing, RP2}','Duration',0.,300.,2)
##pulse.ramp_parameter('t_{mixing, RP2}','Delay',200.,450.,2)
#Map.add_object(pulse)

#ramp = WE.Ramp(name = 'Ramp_up_RP1',\
#                 channel = 'awg_RP1',\
#                 Vstart = -1.,\
#                 Vstop = -3.,\
#                 Tramp = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
##ramp.ramp_parameter('V0_{rampup, RP1}','Vstart',-1.,-2.5,2)
##ramp.ramp_parameter('V1_{rampup, RP1}','Vstop',-1.5,-3.,2)
#ramp.ramp_parameter('t_{rampup, RP1}','Tramp',0.,100.,1)
##ramp.ramp_parameter('dt_{rampup, RP1}','Delay',200.,450.,2)
#Map.add_object(ramp)
#
#ramp = WE.Ramp(name = 'Ramp_down_RP1',\
#                 channel = 'awg_RP1',\
#                 Vstart = -3.,\
#                 Vstop = -1.,\
#                 Tramp = 2/1.2,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
##ramp.ramp_parameter('V0_{rampdown, RP1}','Vstart',-1.5,-3.,2)
##ramp.ramp_parameter('V1_{rampdown, RP1}','Vstop',-1.,-2.5,2)
##ramp.ramp_parameter('t_{rampdown, RP1}','Tramp',0.,500.,1)
#ramp.ramp_parameter('dt_{rampdown, RP1}','Delay',2000+0.,2000+100.,1)
#Map.add_object(ramp)
#
#ramp = WE.Ramp(name = 'Ramp_up_RP2',\
#                 channel = 'awg_RP2',\
#                 Vstart = -4.5,\
#                 Vstop = +4.5,\
#                 Tramp = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
##ramp.ramp_parameter('V0_{rampup, RP1}','Vstart',-4.5,+2.25,2)
##ramp.ramp_parameter('V1_{rampup, RP1}','Vstop',-2.25,+4.5,2)
#ramp.ramp_parameter('t_{rampup, RP2}','Tramp',0.,100.,1)
##ramp.ramp_parameter('dt_{rampup, RP2}','Delay',200.,450.,2)
#Map.add_object(ramp)
#
#ramp = WE.Ramp(name = 'Ramp_down_RP2',\
#                 channel = 'awg_RP2',\
#                 Vstart = +4.5,\
#                 Vstop = -4.5,\
#                 Tramp = 2/1.2,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
##ramp.ramp_parameter('V0_{rampdown, RP2}','Vstart',-2.25,+4.5,2)
##ramp.ramp_parameter('V1_{rampdown, RP2}','Vstop',-4.5,+2.25,2)
##ramp.ramp_parameter('t_{rampdown, RP2}','Tramp',0.,500.,1)
#ramp.ramp_parameter('dt_{rampdown, RP2}','Delay',2000+0.,2000+100.,1)
#Map.add_object(ramp)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements)