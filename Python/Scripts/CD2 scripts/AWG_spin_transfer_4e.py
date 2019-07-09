# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
from AWG.AWG_map import AWG_map
from AWG.AWG_fast_send import AWG_fast_send
import AWG.Waveform_elements as WE

Map = AWG_map(sweep_dim=[1],waveform_duration=12000)
#Map = AWG_map(sweep_dim=[51],waveform_duration=12000)
#Map = AWG_map(sweep_dim=[100,2],waveform_duration=60000)

#pulse = WE.Pulse(name = 'V_{mixing, LP1}',\
#                 channel = 'awg_LP1',\
#                 Amplitude = -3.,\
#                 Duration = 500.,\
#                 unit = 'ns',\
#                 Delay = 40000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, LP1}','Amplitude',0.,-3.,2)
##pulse.ramp_parameter('t_{mixing, LP1}','Duration',0.,500.,2)
##pulse.ramp_parameter('t_{mixing, LP1}','Delay',24000,48000,1)
#Map.add_object(pulse)
#
#pulse = WE.Pulse(name = 'V_{AWG, LP2}',
#                 channel = 'awg_LP2',
#                 Amplitude = 4.5,
#                 Duration = 200.,
#                 unit = 'ns',
#                 Delay = 2000.,
#                 )
#pulse.ramp_parameter('V_{AWG, LP2}','Amplitude',-4.5,4.5,1)
##pulse.ramp_parameter('t_{pulse, LP2}','Duration',0.,50.,1)
#Map.add_object(pulse)

SAW_protec = WE.Pulse(name = 'SAW_protec',\
                 channel = 'awg_RP1',\
                 Amplitude = +3.,\
                 Duration = 8000.,\
                 unit = 'ns',\
                 Delay = -3500.+5000.,\
                 )
#SAW_protec.ramp_parameter('V_{protect, RP1}','Amplitude',-4.5,3.,1)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Duration',0.,100,2)
#SAW_protec.ramp_parameter('t_{protect, RP1}','Delay',5000+470.,5000+430.,1)
Map.add_object(SAW_protec)
#
#SAW_small = WE.Pulse(name = 'SAW_small',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -1.3-3.,\
#                 Duration = 3./1.2,\
#                 unit = 'ns',\
#                 Delay = 440+5000.,\
#                 )
##SAW_small.ramp_parameter('V_{sending1, RP1}','Amplitude',-4.,0.,2)
##SAW_small.ramp_parameter('t_{sending1, RP1}','Duration',5.,0.,2)
##SAW_small.ramp_parameter('t_{sending1, RP1}','Delay',5000+420.,5000+460.,1)
#Map.add_object(SAW_small)
#
SAW_attac = WE.Pulse(name = 'SAW_attac',\
                 channel = 'awg_RP1',\
                 Amplitude = -4.-3.,\
                 Duration = 3./1.2,\
                 unit = 'ns',\
                 Delay = 440+5000.,\
                 )
#SAW_attac.ramp_parameter('V_{sending2, RP1}','Amplitude',0,-4.5-3,2)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Duration',0.,100,2)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',5000+512.5,5000+437.5,2)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',5000+440.,5000+443.3,3)
#SAW_attac.ramp_parameter('t_{sending2, RP1}','Delay',5000+540.,5000+420,1)
Map.add_object(SAW_attac)

#
#SAW_reception = WE.Pulse(name = 'SAW_reception,1',\
#                 channel = 'awg_LP1',\
#                 Amplitude = -4.5,\
#                 Duration = 4000.,\
#                 unit = 'ns',\
#                 Delay = 0.+200.,\
#                 )
##SAW_reception.ramp_parameter('V_{catching1, LP1}','Amplitude',2.25,-4.5,1)
##SAW_reception.ramp_parameter('t_{catching1, LP1}','Duration',0.,100,2)
#SAW_reception.ramp_parameter('t_{catching1, LP1}','Delay',0000.+425.,0000+470.,1)
#Map.add_object(SAW_reception)
##
#SAW_reception = WE.Pulse(name = 'SAW_reception,2',\
#                 channel = 'awg_LP1',\
#                 Amplitude = +2.,\
#                 Duration = 4000.,\
#                 unit = 'ns',\
#                 Delay = 500.+4000.,\
#                 )
##SAW_reception.ramp_parameter('V_{catching2, LP1}','Amplitude',2.25,-4.5,1)
##SAW_reception.ramp_parameter('t_{catching2, LP1}','Duration',0.,100,2)
#SAW_reception.ramp_parameter('t_{catching2, LP1}','Delay',4000.+425,4000+470.,1)
#Map.add_object(SAW_reception)

#pulse = WE.Pulse(name = 'V_{mixing, RP1}',\
#                 channel = 'awg_RP1',\
#                 Amplitude = -2.,\
#                 Duration = 100.,\
#                 unit = 'ns',\
#                 Delay = 2000.,\
#                 )
##pulse.ramp_parameter('V_{mixing, RP1}','Amplitude',1.5,-4.5,1)
#pulse.ramp_parameter('t_{mixing, RP1}','Duration',100.,0.,1)
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
#                Vramp = -1.3,\
#                V11 = -3.,\
#                Vexch = -1.25,\
#                Delay = 2000.,\
#                Tramp = 500,\
#                T11 = 50,\
#                Texch = 8.,\
#                unit = 'ns',\
#                )
##rabi.ramp_parameter('t_{ramp, RP1}','Tramp',0,300.,1)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',120.,0.,1)
##rabi.ramp_parameter('t_{exch, RP1}','Texch',0.,23.,2)
#rabi.ramp_parameter('V_{exch, RP1}','Vexch',-4.5,2.25,1)
#Map.add_object(rabi)
#
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