# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE


#Map = AWG_map(sweep_dim=[101],waveform_duration=4000)
Map = AWG_map(sweep_dim=[3,49,2],waveform_duration=4000)
#Map = AWG_map(sweep_dim=[201],waveform_duration=30000)
#Map = AWG_map(sweep_dim=[100,2],waveform_duration=7000)

Map.wait_dim = 1
#Map.wait_dim = len(Map.sweep_dim)-1
Map.SAW_marker = [False,True,False]

mix1_bools = [True,False,False]
saw_bools = [False,True,False]
mix2_bools = [False,False,True]

#########################################
################## SAW ##################
#########################################

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

SAW_small = WE.Pulse(name = 'SAW_small_RP1',\
                 channel = 'awg_RP1',\
                 Amplitude = -1.,\
                 Duration = 3./1.2,\
                 unit = 'ns',\
                 Delay = 2005.,\
                 )
#SAW_small.ramp_parameter('V_{sending1, RP1}','Amplitude',0,-4.5,1)
#SAW_small.ramp_parameter('t_{sending1, RP1}','Duration',42.5,2.5,2)
#SAW_small.ramp_parameter('dt_{sending1, RP1}','Delay',1440-40.,1440,2)
Map.add_object(SAW_small,enable_bools=saw_bools)

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
                 Delay = 2005+6.666,\
                 )
#SAW_attac.ramp_parameter('V_{sending2, RP1}','Amplitude',-4.5,3.,1)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Duration',2.5,102.5,1)
#SAW_attac.ramp_parameter('dt_{sending2, RP1}','Delay',2002.5,2077.5,1)
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

#########################################
############## MIXING LEFT ##############
#########################################

pulse = WE.Pulse(name = 'Mixing_LP1',\
                 channel = 'awg_LP1',\
                 Amplitude = -2.6,\
                 Duration = 600.,\
                 unit = 'ns',\
                 Delay = 2000.,\
                 )
pulse.ramp_parameter('V_{mixing, LP1}','Amplitude',0.,-2.6,2)
#pulse.ramp_parameter('t_{mixing, LP1}','Duration',300.,0.,1)
Map.add_object(pulse,enable_bools=mix2_bools)
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

#pulse = WE.Pulse(name = 'Mixing_RP1',\
#                 channel = 'awg_RP1',\
#                 Amplitude = 0.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0,-4.5,2)
##pulse.ramp_parameter('t_{mixing, RP1}','Duration',120.,0.,1)
#Map.add_object(pulse,enable_bools=mix1_bools)

#pulse = WE.Pulse(name = 'Mixing_RP2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',-4.5,4.5,2)
##pulse.ramp_parameter('t_{mixing, RP2}','Duration',0.,300.,2)
#Map.add_object(pulse,enable_bools=mix1_bools)

rabi = WE.Rabi(name = 'Rabi_RP1',\
                channel = 'awg_RP1',\
                Vramp = -0.8,\
                V11 = -2.5,\
                Vexch = -0.785,\
                Delay = 2000,\
                Tramp = 500,\
                T11 = 50.,\
                Texch = 5.,\
                unit = 'ns',\
                )
#rabi.ramp_parameter('t_{ramp, RP1}','Tramp',10.,510.,1)
rabi.ramp_parameter('t_{exch, RP1}','Texch',0,40,1)
#rabi.ramp_parameter('t_{exch, RP1}','Texch',3.33,18.33,2)
#rabi.ramp_parameter('V_{exch, RP1}','Vexch',-0.65,-0.95,2)
#rabi.ramp_parameter('V_{ramp, RP1}','Vramp',-0.5,-1.5,1)
#rabi.ramp_parameter('V_{11, RP1}','V11',-1.,-3.,1)
Map.add_object(rabi,enable_bools=mix1_bools)

rabi = WE.Rabi(name = 'Rabi_RP2',\
                channel = 'awg_RP2',\
                Vramp = +4.5,\
                V11 = +4.5,\
                Vexch = +3.525,\
                Delay = 2000,\
                Tramp = 500,\
                T11 = 50.,\
                Texch = 5.,\
                unit = 'ns',\
                )
#rabi.ramp_parameter('t_{ramp, RP2}','Tramp',10.,510.,1)
rabi.ramp_parameter('t_{exch, RP2}','Texch',0,40,1)
#rabi.ramp_parameter('t_{exch, RP2}','Texch',3.33,18.33,2)
#rabi.ramp_parameter('V_{exch, RP2}','Vexch',2.925,4.275,2)
#rabi.ramp_parameter('V_{ramp, RP2}','Vramp',-4.5,+4.5,1)
#rabi.ramp_parameter('V_{11, RP2}','V11',-1.,-3.,1)
Map.add_object(rabi,enable_bools=mix1_bools)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements,Map.SAW_elements)