# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

#Map = AWG_map(sweep_dim=[101],waveform_duration=4000)
Map = AWG_map(sweep_dim=[76,5],waveform_duration=41000)
#Map = AWG_map(sweep_dim=[201],waveform_duration=30000)
#Map = AWG_map(sweep_dim=[100,2],waveform_duration=7000)

Map.wait_dim = 0
#Map.wait_dim = len(Map.sweep_dim)-1
#
#ramp = WE.Ramp(name = 'Ramp_up_RP1',\
#                 channel = 'awg_RP1',\
#                 Vstart = -2.-3.,\
#                 Vstop = -3.-3.,\
#                 Tramp = 2.5,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
##ramp.ramp_parameter('V0_{rampup, RP1}','Vstart',-1.,-2.5,2)
##ramp.ramp_parameter('V1_{rampup, RP1}','Vstop',0.,-7.5,1)
#ramp.ramp_parameter('t_{rampup, RP1}','Tramp',0.,400.,1)
#ramp.ramp_parameter('dt_{rampup, RP1}','Delay',2000+400.,2000.+0.,1)
#Map.add_object(ramp)

pulse = WE.Pulse(name = 'V_{mixing, RP1}',\
                 channel = 'awg_RP1',\
                 Amplitude = -3.,\
                 Duration = 200.,\
                 unit = 'ns',\
                 Delay = 20000.,\
                 )
pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',0.,-7.5,1)
#pulse.ramp_parameter('t_{mixing, RP1}','Duration',0.,500.,2)
#pulse.ramp_parameter('t_{mixing, RP1}','Delay',24000,48000,1)
Map.add_object(pulse)

pulse = WE.Pulse(name = 'V_{mixing, RP2}',\
                 channel = 'awg_RP2',\
                 Amplitude = 4.5+4.5,\
                 Duration = 200.,\
                 unit = 'ns',\
                 Delay = 20000.,\
                 )
pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',0.,+9.,2)
#pulse.ramp_parameter('t_{mixing, RP2}','Duration',0.,500.,2)
#pulse.ramp_parameter('t_{mixing, RP2}','Delay',24000,48000,1)
Map.add_object(pulse)

SAW_protec = WE.Pulse(name = 'SAW_protec',\
                 channel = 'awg_RP1',\
                 Amplitude = +3.,\
                 Duration = 20000.,\
                 unit = 'ns',\
                 Delay = 14000.,\
                 )
#SAW_protec.ramp_parameter('V_{protect, RP1}','Amplitude',0,+3.,1)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Duration',0.,100,2)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Delay',1000+470.,1000+430.,1)
Map.add_object(SAW_protec)

SAW_protec = WE.Pulse(name = 'SAW_protec2',\
                 channel = 'awg_RP2',\
                 Amplitude = -4.5,\
                 Duration = 20000.,\
                 unit = 'ns',\
                 Delay = 14000.,\
                 )
#SAW_protec.ramp_parameter('V_{protect, RP2}','Amplitude',-4.5,+4.5,2)
#SAW_protec.ramp_parameter('t_{protect, RP2}','Duration',0.,100,2)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Delay',1000+470.,1000+430.,1)
Map.add_object(SAW_protec)

#SAW_small = WE.Pulse(name = 'SAW_small',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -1.8-3.,\
#                 Duration = 3./1.2,\
#                 unit = 'ns',\
#                 Delay = 440+2000.,\
#                 )
##SAW_small.ramp_parameter('V_{sending1, RP1}','Amplitude',0,-4.5,1)
##SAW_small.ramp_parameter('t_{sending1, RP1}','Duration',42.5,2.5,2)
##SAW_small.ramp_parameter('dt_{sending1, RP1}','Delay',1440-40.,1440,2)
#Map.add_object(SAW_small)

#SAW_small = WE.Pulse(name = 'SAW_small2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = 4.5+4.5,\
#                 Duration = 3./1.2,\
#                 unit = 'ns',\
#                 Delay = 440+1000.,\
#                 )
##SAW_small.ramp_parameter('V_{sending1, RP2}','Amplitude',0,-4.5,1)
##SAW_small.ramp_parameter('t_{sending1, RP2}','Duration',42.5,2.5,2)
##SAW_small.ramp_parameter('dt_{sending1, RP2}','Delay',1440-40.,1440,2)
#Map.add_object(SAW_small)
#
#SAW_attac = WE.Pulse(name = 'SAW_attac',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -3.-3.,\
#                 Duration = 2.5,\
#                 unit = 'ns',\
#                 Delay = 460.+2000.,\
#                 )
#SAW_attac.ramp_parameter('V_{sending2, RP1}','Amplitude',-7.5,-0.,1)
##SAW_attac.ramp_parameter('t_{sending2, RP1}','Duration',2.5,102.5,1)
##SAW_attac.ramp_parameter('dt_{sending2, RP1}','Delay',20440.,20340.,1)
##SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',1000+540.,1000+420,1)
#Map.add_object(SAW_attac)

#SAW_attac2 = WE.Pulse(name = 'SAW_attac2',\
#                 channel = 'awg_RP2',\
#                 Amplitude = 4.5+4.5,\
#                 Duration = 2.5,\
#                 unit = 'ns',\
#                 Delay = 440+2000.,\
#                 )
#SAW_attac2.ramp_parameter('V_{sending2, RP2}','Amplitude',0.,+9.,2)
##SAW_attac2.ramp_parameter('V_{sending2, RP2}','Amplitude',-4.5,+4.5,2)
##SAW_attac2.ramp_parameter('t_{sending2, RP2}','Duration',0.,120.,1)
##SAW_attac2.ramp_parameter('t_{sending2, RP2}','Delay',1000+490.,1000+440.,1)
##SAW_attac2.ramp_parameter('t_{sending2, RP2}','Delay',1000+440.,1000+443.3,3)
##SAW_attac2.ramp_parameter('t_{sending2, RP2}','Delay',1000+540.,1000+420,1)
#Map.add_object(SAW_attac2)

#SAW_reception = WE.Pulse(name = 'SAW_reception,1',\
#                 channel = 'awg_LP1',\
#                 Amplitude = -4.5,\
#                 Duration = 1000.,\
#                 unit = 'ns',\
#                 Delay = 0.+452.5,\
#                 )
##SAW_reception.ramp_parameter('V_{catching1, LP1}','Amplitude',3.,-4.5,1)
##SAW_reception.ramp_parameter('t_{catching1, LP1}','Duration',0.,100,2)
#SAW_reception.ramp_parameter('t_{catching1, LP1}','Delay',0000.+430.,0000+490.,1)
#Map.add_object(SAW_reception)
#
#SAW_reception = WE.Pulse(name = 'SAW_reception,2',\
#                 channel = 'awg_LP1',\
#                 Amplitude = +3.,\
#                 Duration = 1000.,\
#                 unit = 'ns',\
#                 Delay = 1000.+452.5,\
#                 )
##SAW_reception.ramp_parameter('V_{catching2, LP1}','Amplitude',2.25,-4.5,1)
##SAW_reception.ramp_parameter('t_{catching2, LP1}','Duration',0.,100,2)
#SAW_reception.ramp_parameter('t_{catching2, LP1}','Delay',1000.+430,1000+490.,1)
#Map.add_object(SAW_reception)
#
#pulse = WE.Pulse(name = 'V_{mixing, RP1}',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -3.-3.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 5000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',3.,-4.5,2)
#pulse.ramp_parameter('t_{mixing, RP1}','Duration',50.,0.,2)
#pulse.ramp_parameter('dt_{mixing, RP1}','Delay',1440.-52.5,1440.-2.5,2)
#Map.add_object(pulse)
#
#pulse = WE.Pulse(name = 'V_{mixing, RP2}',\
#                 channel = 'awg_RP2',\
#                 Amplitude = +4.5+4.5,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 5000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',0.5,-4.5,2)
#pulse.ramp_parameter('t_{mixing, RP2}','Duration',50.,0.,2)
#pulse.ramp_parameter('dt_{mixing, RP2}','Delay',1440.-52.5,1440.-2.5,2)
#Map.add_object(pulse)

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

#pulse = WE.Pulse(name = 'V_{mixing, RP1}',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -4.5-3.,\
#                 Duration = 100.,\
#                 unit = 'ns',\
#                 Delay = 450+5000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',-3.,-5.,1)
##pulse.ramp_parameter('t_{mixing, RP1}','Duration',120.,0.,1)
##pulse.ramp_parameter('t_{mixing, RP2}','Delay',200.,450.,2)
#Map.add_object(pulse)
#
#pulse = WE.Pulse(name = 'V_{mixing, RP2}',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -2.5,\
#                 Duration = 200.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
#pulse.ramp_parameter('V_{mixing, RP2}','Amplitude',-4.5,4.5,2)
##pulse.ramp_parameter('t_{mixing, RP2}','Duration',0.,300.,2)
##pulse.ramp_parameter('t_{mixing, RP2}','Delay',200.,450.,2)
#Map.add_object(pulse)

#rabi = WE.Rabi(name = 'Rabi_RP1',\
#                channel = 'awg_RP1',\
#                Vramp = -2.-3.,\
#                V11 = -3.-3.,\
##                Vexch = -1.36,\
#                Vexch = -3.-3.,\
#                Delay = 2000,\
#                Tramp = 200,\
#                T11 = 50.,\
#                Texch = 0.,\
#                unit = 'ns',\
#                )
#rabi.ramp_parameter('t_{ramp, RP1}','Tramp',0.,400.,1)
#rabi.ramp_parameter('dt_{ramp, RP1}','Delay',2000.+400,2000.,1)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',0,15,2)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',0,70,1)
##rabi.ramp_parameter('V_{exch, RP1}','Vexch',-0.5,-1.5,1)
##rabi.ramp_parameter('V_{ramp, RP1}','Vramp',-1.25,-2.25,2)
##rabi.ramp_parameter('V_{11, RP1}','V11',-2.,-4.5,1)
#Map.add_object(rabi)

#rabi = WE.Rabi(name = 'Rabi_RP2',\
#                channel = 'awg_RP2',\
#                Vramp = -0.,\
#                V11 = -0.,\
#                Vexch = -0.,\
#                Delay = 2000.,\
#                Tramp = 500,\
#                T11 = 50,\
#                Texch = 8.,\
#                unit = 'ns',\
#                )
##rabi.ramp_parameter('t_{ramp, RP2}','Tramp',0,300.,1)
##rabi.ramp_parameter('t_{exch, RP2}','Texch',120.,0.,1)
##rabi.ramp_parameter('t_{exch, RP2}','Texch',0.,23.,2)
#rabi.ramp_parameter('V_{exch, RP2}','Vexch',-4.5,+4.5,2)
#Map.add_object(rabi)

#pulse = WE.Pulse(name = 'V_{AWG, RP2}',\
#                 channel = 'awg_RP2',\
#                 Amplitude = -4.5,\
#                 Duration = 10.,\
#                 unit = 'ns',\
#                 Delay = 235.+25000.,\
#                 )
##pulse.ramp_parameter('V_{AWG, RP2}','Amplitude',0,-4.5,2)
##pulse.ramp_parameter('t_{pulse, RP2}','Duration',0.,50.,1)
##pulse.ramp_parameter('t_{pulse, RP2}','Delay',200.,450.,2)
#Map.add_object(pulse)

outp = Map.build_all()
Map.update_h5()
if outp==1:
    AWG_fast_send(Map.waveforms,Map.channel_names,Map.wait_elements)