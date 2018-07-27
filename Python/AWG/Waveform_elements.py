from _logs.logs import LOG_Manager
import logging
log = LOG_Manager()
# log.start(level_console=logging.DEBUG)
log.start(level_console=logging.CRITICAL)

import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
import matplotlib.pyplot as plt

sampling_rate = 1.2 # GHz

class Pulse():
    def __init__(self, name, channel, Amplitude=0.8, Duration=100, Delay=25, unit='pts'):
        self.name = name
        self.channel = channel
        self.Amplitude = Amplitude
        self.Duration = Duration
        self.Delay = Delay
        self.unit = unit
        self.varied_parameters = {}

    def ramp_parameter(self, name, parameter, start, stop, dim):
        if parameter not in ['Amplitude','Duration','Delay']:
            log.send(level="critical",
                        context="Waveform_elements.ramp_parameter",
                        message="Unknown parameter : {}".format(parameter))
            return 0
        
        sweep_infos = {}
        sweep_infos['name'] = name
        sweep_infos['type'] = 'linear'
        sweep_infos['start'] = start
        sweep_infos['stop'] = stop
        sweep_infos['dim'] = dim
        self.varied_parameters[parameter] = sweep_infos
        return 1

    def calc_value(self, start, stop, dim, indexes, sweep_dim):
        val_list = np.linspace(start,stop,sweep_dim[dim-1])
        # print (val_list[indexes[dim-1]])
        return val_list[indexes[dim-1]]

    def make_wf(self, indexes, sweep_dim, waveform_duration=1000):
        if (len(indexes) != len(sweep_dim)) or any([indexes[i]>=sweep_dim[i] for i in range(len(sweep_dim))]):
            self.wf = np.zeros((1,waveform_duration))
            log.send(level="critical",
                        context="Waveform_elements.make_wf",
                        message="Sweeep indexes are incorrect")
            return (self.wf,0)

        if 'Amplitude' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Amplitude']
            amplitude = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            amplitude = self.Amplitude

        if 'Duration' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Duration']
            amplitude = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            duration = self.Duration
            
        if 'Delay' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Delay']
            delay = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            delay = self.Delay

        if self.unit == 'ns':
            wf_length = int(waveform_duration)
            pos_start = int(delay * sampling_rate)
            pos_stop = int((delay + duration) * sampling_rate)
        else:
            wf_length = int(waveform_duration)
            pos_start = int(delay)
            pos_stop = int(delay + duration)

        if delay + duration + 1 > waveform_duration:
            self.wf = np.zeros((1,waveform_duration))
            log.send(level="critical",
                        context="Waveform_elements.make_wf",
                        message="Pulse is too large for WaveformDuration")
            return (self.wf,0)

        self.wf = np.zeros((wf_length,1))
        self.wf[pos_start:pos_stop] = amplitude   
        return (self.wf,1)

    def __str__(self):
        txt = 'Pulse object {} on channel {}'.format(self.name,self.channel) + os.linesep
        for param in ['Amplitude','Duration','Delay']:
            unit = self.unit if param in ['Duration','Delay'] else 'V'
            if param in self.varied_parameters:
                sweep_infos = self.varied_parameters[param]
                txt += '\t {} ramped from {} {} to {} {} on dim {}'.format(param,sweep_infos['start'],unit,sweep_infos['stop'],unit,sweep_infos['dim']) + os.linesep
            else:
                txt += '\t {} fixed at {} {}'.format(param,getattr(self,param),unit) + os.linesep
        return txt[:-len(os.linesep)]

    def update_h5(self, h5file, sweep_dim):
        if h5file.get(self.name) != None:
            log.send(level="critical",
                        context="Pulse.update_h5",
                        message="group {} already exists in h5 file".format(self.name))
            return 0
        
        grp = h5file.create_group(self.name)
        for key in ['name','channel','unit','Amplitude','Duration','Delay']:
            grp.attrs[key] = getattr(self, key)
            if key in self.varied_parameters:
                sweep_infos = self.varied_parameters[key]
                val_list = np.linspace(sweep_infos['start'], sweep_infos['stop'], sweep_dim[sweep_infos['dim']-1])
                val_list = val_list.reshape((len(val_list),1))
                dset = grp.create_dataset(key, data=val_list)
                dset.attrs['parameter'] = key 
                for key2 in ['name','type','start','stop','dim']:
                    dset.attrs[key2] = sweep_infos[key2] 
        return 1

class Rabi():
    def __init__(self, name, channel, Vramp=0.8, V11=1.5, Vexch=1., Delay=25, Tramp=250, T11=50, Texch=10, unit='pts'):
        self.name = name
        self.channel = channel
        self.Vramp = Vramp
        self.V11 = V11
        self.Vexch = Vexch
        self.Tramp = Tramp
        self.T11 = T11
        self.Texch = Texch
        self.Delay = Delay
        self.unit = unit
        self.varied_parameters = {}

    def ramp_parameter(self, name, parameter, start, stop, dim):
        if parameter not in ['Vramp','V11','Vexch','Delay','Tramp','T11','Texch']:
            log.send(level="critical",
                        context="Waveform_elements.ramp_parameter",
                        message="Unknown parameter : {}".format(parameter))
            return 0
        
        sweep_infos = {}
        sweep_infos['name'] = name
        sweep_infos['type'] = 'linear'
        sweep_infos['start'] = start
        sweep_infos['stop'] = stop
        sweep_infos['dim'] = dim
        self.varied_parameters[parameter] = sweep_infos
        return 1

    def calc_value(self, start, stop, dim, indexes, sweep_dim):
        val_list = np.linspace(start,stop,sweep_dim[dim-1])
        # print (val_list[indexes[dim-1]])
        return val_list[indexes[dim-1]]

    def make_wf(self, indexes, sweep_dim, waveform_duration=1000):
        if (len(indexes) != len(sweep_dim)) or any([indexes[i]>=sweep_dim[i] for i in range(len(sweep_dim))]):
            self.wf = np.zeros((1,waveform_duration))
            log.send(level="critical",
                        context="Waveform_elements.make_wf",
                        message="Sweeep indexes are incorrect")
            return (self.wf,0)

        if 'Vramp' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Vramp']
            Vramp = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            Vramp = self.Vramp

        if 'V11' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['V11']
            V11 = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            V11 = self.V11

        if 'Vexch' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Vexch']
            Vexch = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            Vexch = self.Vexch
            
        if 'Delay' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Delay']
            Delay = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            Delay = self.Delay

        if 'Tramp' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Tramp']
            Tramp = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            Tramp = self.Tramp

        if 'T11' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['T11']
            T11 = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            T11 = self.T11

        if 'Texch' in self.varied_parameters.keys():
            sweep_infos = self.varied_parameters['Texch']
            Texch = self.calc_value(sweep_infos['start'],sweep_infos['stop'],sweep_infos['dim'],indexes,sweep_dim)
        else:
            Texch = self.Texch

        if self.unit == 'ns':
            dur = int(waveform_duration)
            Delay = int(Delay * sampling_rate)
            Tramp = int(Tramp * sampling_rate)
            T11 = int(T11 * sampling_rate)
            Texch = int(Texch * sampling_rate)
        else:
            dur = int(waveform_duration)
            Delay = int(Delay)
            Tramp = int(Tramp)
            T11 = int(T11)
            Texch = int(Texch)

        if Delay + 2*(Tramp+T11) + Texch +  2 > waveform_duration:
            self.wf = np.zeros((1,waveform_duration))
            log.send(level="debug",
                        context="Waveform_elements.make_wf",
                        message="Rabi is too large for WaveformDuration")
            return (self.wf,0)

        self.wf = np.zeros((dur,1))
        rabi_pulse = np.hstack((np.linspace(Vramp,V11,Tramp),np.linspace(V11,V11,T11)))
        rabi_pulse = np.hstack((rabi_pulse,np.linspace(Vexch,Vexch,Texch),rabi_pulse[::-1]))
        self.wf[Delay:Delay+len(rabi_pulse),0] = rabi_pulse
        return (self.wf,1)
        
    def __str__(self):
        txt = 'Rabi object {} on channel {}'.format(self.name,self.channel) + os.linesep
        for param in ['Vramp','V11','Vexch','Delay','Tramp','T11','Texch']:
            unit = self.unit if param in ['Delay','Tramp','T11','Texch'] else 'V'
            if param in self.varied_parameters:
                sweep_infos = self.varied_parameters[param]
                txt += '\t {} ramped from {} {} to {} {} on dim {}'.format(param,sweep_infos['start'],unit,sweep_infos['stop'],unit,sweep_infos['dim']) + os.linesep
            else:
                txt += '\t {} fixed at {} {}'.format(param,getattr(self,param),unit) + os.linesep
        return txt[:-len(os.linesep)]

    def update_h5(self, h5file, sweep_dim):
        if h5file.get(self.name) != None:
            log.send(level="critical",
                        context="Pulse.update_h5",
                        message="group {} already exists in h5 file".format(self.name))
            return 0
        
        grp = h5file.create_group(self.name)
        for key in ['name','channel','unit','Vramp','V11','Vexch','Delay','Tramp','T11','Texch']:
            grp.attrs[key] = getattr(self, key)
            if key in self.varied_parameters:
                sweep_infos = self.varied_parameters[key]
                val_list = np.linspace(sweep_infos['start'], sweep_infos['stop'], sweep_dim[sweep_infos['dim']-1])
                val_list = val_list.reshape((len(val_list),1))
                dset = grp.create_dataset(key, data=val_list)
                dset.attrs['parameter'] = key 
                for key2 in ['name','type','start','stop','dim']:
                    dset.attrs[key2] = sweep_infos[key2] 
        return 1