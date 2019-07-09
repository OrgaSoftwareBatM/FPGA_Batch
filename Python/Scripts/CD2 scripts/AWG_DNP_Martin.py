# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

#Map = AWG_map(sweep_dim=[101],waveform_duration=4000)
Map = AWG_map(sweep_dim=[1,121],waveform_duration=4100)
#Map = AWG_map(sweep_dim=[1,61],waveform_duration=41000)
#Map = AWG_map(sweep_dim=[1,100],waveform_duration=4000)


Map.wait_dim = 1
#Map.wait_dim = len(Map.sweep_dim)-1
Map.SAW_marker = [False]

mix1_bools = [True]
#mix2_bools = [True]
#saw_bools = [False]


#########################################
############## MIXING LEFT ##############
#########################################

#pulse = WE.Pulse(name = 'Mixing_LP1',\
#                 channel = 'awg_LP1',\
#                 Amplitude = -2.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, LP1}','Amplitude',0.5,-4.5,1)
##pulse.ramp_parameter('t_{mixing, LP1}','Duration',300.,0.,1)
#Map.add_object(pulse,enable_bools=mix2_bools)
#
#pulse = WE.Pulse(name = 'Mixing_LP2',\
#                 channel = 'awg_LP2',\
#                 Amplitude = 0.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, LP2}','Amplitude',-0.2,+0.2,1)
##pulse.ramp_parameter('t_{mixing, LP2}','Duration',0.,500.,1)
#Map.add_object(pulse,enable_bools=mix2_bools)

#########################################
############## MIXING RIGHT #############
#########################################
#
#pulse = WE.Pulse(name = 'Protect_RP1',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -4.5,\
#                 Duration = 20000.,\
#                 unit = 'ns',\
#                 Delay = 14000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0,-2,1)
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.,-3.,2)
##pulse.ramp_parameter('t_{mixing, RP1}','Duration',0.,100.,1)
#Map.add_object(pulse,enable_bools=mix1_bools)
#
pulse = WE.Pulse(name = 'Mixing_RP1',\
                 channel = 'awg_RP1',\
                 Amplitude = 2.5,\
                 Duration = 20000.,\
                 unit = 'ns',\
                 Delay = 8000.,\
                 )
pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',-0.8,-4.5,1)
#pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0,2.5,2)
#pulse.ramp_parameter('t_{mixing, RP1}','Duration',100.,0.,1)
Map.add_object(pulse,enable_bools=mix1_bools)


#pulse = WE.Pulse(name = 'Positive_pulse_RP1',\
#                 channel = 'awg_RP1',\
#                 Amplitude = 3,\
#                 Duration = 5000.,\
#                 unit = 'ns',\
#                 Delay = 20000.,\
#                 )
##pulse.ramp_parameter('V_{positive pulse, RP1}','Amplitude',0,0.865,2)
##pulse.ramp_parameter('V_{positive pulse, RP1}','Amplitude',0,3.,1)
##pulse.ramp_parameter('t_{positive pulse, RP1}','Duration',1000.,11000.,1)
#Map.add_object(pulse,enable_bools=mix1_bools)
#
ramp = WE.Ramp(name = 'Ramp_up_RP1',\
                 channel = 'awg_RP1',\
                 Vstart = -1,\
                 Vstop = -2.5,\
                 Tramp = 5000.,\
                 unit = 'ns',\
                 Delay = 2000.,\
                 )
#ramp.ramp_parameter('V0_{rampup, RP1}','Vstart',-1.,-2.5,2)
#ramp.ramp_parameter('V1_{rampup, RP1}','Vstop',1,0,2)
#ramp.ramp_parameter('t_{rampup, RP1}','Tramp',0.,1000.,1)
#ramp.ramp_parameter('dt_{rampup, RP1}','Delay',200.,450.,2)
Map.add_object(ramp)

#ramp = WE.Ramp(name = 'Ramp_down_RP1',\
#                 channel = 'awg_RP1',\
#                 Vstart = 3,\
#                 Vstop = 2,\
#                 Tramp = 800.,\
#                 unit = 'ns',\
#                 Delay = 25000.,\
#                 )
##ramp.ramp_parameter('V0_{rampdown, RP1}','Vstart',3,1,1)
##ramp.ramp_parameter('V1_{rampdown, RP1}','Vstop',3,0,1)
##ramp.ramp_parameter('t_{rampdown, RP1}','Tramp',0.,1000.,1)
##ramp.ramp_parameter('dt_{rampdown, RP1}','Delay',21000.,31000.,1)
#Map.add_object(ramp)

#pulse = WE.Pulse(name = 'Protect_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 20000.,\
#                 unit = 'ns',\
#                 Delay = 14000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0,-2,1)
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.,-3.,2)
##pulse.ramp_parameter('t_{mixing, RP1}','Duration',0.,100.,1)
#Map.add_object(pulse,enable_bools=mix1_bools)
##
#pulse = WE.Pulse(name = 'Mixing_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = 2.34,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 20000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',-4.5,4.5,1)
##pulse.ramp_parameter('t_{mixing, RP2}','Duration',0.,1000.,1)
#Map.add_object(pulse,enable_bools=mix1_bools)

#rabi = WE.Rabi(name = 'Rabi_RP1',\
#                channel = 'awg_RP1',\
#                Vramp = -2,\
#                V11 = -4.5,\
#                Vexch = -1.36,\
#                Delay = 2000,\
#                Tramp = 250,\
#                T11 = 50.,\
#                Texch = 20.,\
#                unit = 'ns',\
#                )
##rabi.ramp_parameter('t_{ramp, RP1}','Tramp',10.,510.,1)
#rabi.ramp_parameter('t_{exch, RP1}','Texch',100,0,1)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',150,0,1)
##rabi.ramp_parameter('V_{exch, RP1}','Vexch',0.,-2.,1)
##rabi.ramp_parameter('V_{ramp, RP1}','Vramp',-1.,-2.,1)
##rabi.ramp_parameter('V_{11, RP1}','V11',-1.,-3.,1)
#Map.add_object(rabi,enable_bools=mix1_bools)

#rabi = WE.Rabi(name = 'Rabi_RP2',\
#                channel = 'awg_RP2',\
#                Vramp = 0.,\
#                V11 = -4.5,\
#                Vexch = +4.5,\
#                Delay = 20000,\
#                Tramp = 500,\
#                T11 = 50.,\
#                Texch = 30.,\
#                unit = 'ns',\
#                )
##rabi.ramp_parameter('t_{ramp, RP2}','Tramp',10.,510.,1)
#rabi.ramp_parameter('t_{exch, RP2}','Texch',0,100,1)
##rabi.ramp_parameter('t_{exch, RP2}','Texch',100,0,1)
##rabi.ramp_parameter('V_{exch, RP2}','Vexch',2.925,4.275,2)
##rabi.ramp_parameter('V_{ramp, RP2}','Vramp',-4.5,+4.5,1)
##rabi.ramp_parameter('V_{11, RP2}','V11',-1.,-3.,1)
#Map.add_object(rabi,enable_bools=mix1_bools)


outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements,Map.SAW_elements)
