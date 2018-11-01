# -*- coding: utf-8 -*-
from _logs.logs import LOG_Manager
import logging
log = LOG_Manager()
# log.start(level_console=logging.DEBUG)
log.start(level_console=logging.INFO)
# log.start(level_console=logging.CRITICAL)

import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
import h5py
import AWG.Waveform_elements as WE

AWG_status_file = '..\\AWG\\AWG_status.h5'# special data type to define array of flexible length strings in HDF5 file
flexible_str_dt = h5py.special_dtype(vlen=bytes)

class AWG_map():
    def __init__(self,sweep_dim,waveform_duration=1000):
        self.channel_names = ['awg_LP1','awg_RP1','awg_LP2','awg_RP2']
        self.sweep_dim = sweep_dim
        self.waveform_duration = waveform_duration
        self.objects = []

    def add_object(self,obj):
        if obj.channel not in self.channel_names:
            log.send(level="critical",
                        context="AWG_map.add_object",
                        message="Unknown channel")
        else:
            obj.cind = self.channel_names.index(obj.channel)
            self.objects.append(obj)
            log.send(level="debug",
                        context="AWG_map.add_object",
                        message="{} added".format(obj.name))

    def build(self,indexes):
        wfms = np.zeros((4,self.waveform_duration))
        for obj in self.objects:
            (to_add,make_output) = obj.make_wf(indexes,self.sweep_dim,self.waveform_duration)
            if make_output:
                wfms[obj.cind,:] = wfms[obj.cind,:] + to_add.T
        log.send(level="debug",
                    context="AWG_map.build",
                    message="index {}.".format(indexes))
        return wfms
    
    def build_all(self):
        if len(self.sweep_dim)==1:   # only 1 dimension
            if self.sweep_dim[0]+1>4000:
                log.send(level="critical",
                            context="AWG_map.build_all",
                            message="Sweep_dim is too big for AWG")
                return 0
            self.waveforms = np.zeros((4,self.waveform_duration,self.sweep_dim[0]+1))
            for i in range(self.sweep_dim[0]):
                self.waveforms[:,:,i] = self.build([i])
            self.wait_elements = [self.sweep_dim[0]]
        else:
            new_dim = [n+1 if i==0 else n for i,n in enumerate(self.sweep_dim)]
            if np.prod(new_dim)>4000:
                log.send(level="critical",
                            context="AWG_map.build_all",
                            message="Sweep_dim is too big for AWG")
                return 0
            is_wait = np.zeros(new_dim)
            is_wait[-1,:] = 1
            self.wait_elements = np.sort(np.ravel_multi_index(np.where(is_wait==1),new_dim,order='F'))
#            self.wait_elements = [np.prod(new_dim)]
            self.waveforms = np.zeros((4,self.waveform_duration,np.prod(new_dim)))
            for i in range(np.prod(new_dim)):
                indexes = np.unravel_index(i,new_dim,'F')
                if not is_wait[indexes]:
                    self.waveforms[:,:,i] = self.build(list(indexes))
        self.waveforms[self.waveforms<-4] = -4.
        log.send(level="info",
                    context="AWG_map.build_all",
                    message=os.linesep+self.__str__())
        return 1

    def __str__(self):
        txt = '--- AWG_map ---' + os.linesep
        txt += 'sweep_dim = {}'.format(self.sweep_dim) + os.linesep
        txt += 'waveform_duration = {}'.format(self.waveform_duration) + os.linesep
        txt += '--- Content ---'
        for obj in self.objects:
            txt += os.linesep
            txt += obj.__str__()
        return txt

    def update_h5(self):
        if not os.path.isfile(AWG_status_file):
            log.send(level="critical",
                        context="AWG_map.update_h5",
                        message="status file not found.")
            return 0
        with h5py.File(AWG_status_file, 'w') as f:
            for key in f:   # removing all content
                del f[key]

            dset = f.get('Param_list')
            if dset == None:
                dset = f.create_dataset('Param_list', (1,),data=np.array((0), dtype='f'))
            dset.attrs.create('sweep_dim', np.array(self.sweep_dim, dtype=np.uint64), dtype='uint64')
            dset.attrs.create('waveform_duration', self.waveform_duration, dtype='uint64')
            dset.attrs['comments'] = self.__str__() + os.linesep
            dset.attrs.create('obj_list', data=[obj.name for obj in self.objects], dtype=flexible_str_dt)
            sweep_list = []
            for obj in self.objects:
                obj.update_h5(f, self.sweep_dim)
                sweep_list += [obj.varied_parameters[key]['name'] for key in obj.varied_parameters.keys()]
            dset.attrs.create('sweep_list', data=sweep_list, dtype=flexible_str_dt)

        log.send(level="debug",
                    context="AWG_map.update_h5",
                    message='done.')
        return 1



if __name__ == '__main__':
    pass
#    a = AWG_map([11,3,4])
#    pulse = WE.Pulse('Pulse1_RP1','awg_RP1')
#    pulse.ramp_parameter('Pulse1_RP1_ampl','Amplitude',0.2,0.4,3)
#    a.add_object(pulse)
#    rabi = WE.Rabi('Rabi1_RP2','awg_RP2')
#    rabi.ramp_parameter('Rabi1_Texch','Texch',10,20,2)
#    rabi.ramp_parameter('Rabi1_Vexch','Vexch',0.5,1.,1)
#    a.add_object(rabi)
#    a.build_all()
    # a.txt_summary()