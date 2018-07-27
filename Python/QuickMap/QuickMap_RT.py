# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 19:46:45 2017

@author: manip.batm
"""
import os,sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)

from _logs.logs import LOG_Manager
import logging
log = LOG_Manager()
# log.start(level_console=logging.DEBUG)
log.start(level_console=logging.INFO)
# log.start(level_console=logging.CRITICAL)

import ctypes 
MessageBoxW = ctypes.windll.user32.MessageBoxW
import numpy as np
from shutil import copy2
import MeasurementBase.measurement_classes as mc
import MeasurementBase.FastSequenceGenerator as fsg
from MeasurementBase.SendFileNames import sendFiles
from MeasurementBase.ArrayGenerator import ArrayGenerator
from QuickMap.BM13_config_CD2_2 import DAC_ADC_config, RF_config
from QuickMap.find_unused_name import find_unused_name

class RT_fastseq():
    def __init__(self,folder=os.getcwd(),prefix='test'):
        self.folder = folder
        self.prefix = prefix
        self.findex, self.config_path, self.exp_path = find_unused_name(folder, prefix, search_adjacent_folders=True)
        
        self.DAC, self.fs, self.ADC = DAC_ADC_config()  
        self.RF = RF_config()  
        self.waits = {}
        self.fs_slots = {}
        
        self.init_val = {}     # dict of [values]
        self.sweep_param = {}  # dict of [method,start,stop,dim]
        self.sweep_list = []
        self.sequence = []  # sequence (without ramp)
        
        self.initial_wait = 100    # ms before the show starts
        self.ms_per_point = 1      # integration time (RT_avg/ADC_freq)
        self.step_wait = 1         # ms wait after every fastseq
        self.sweep_dim = []  

        self.use_AWG = False
        self.AWG_status_path = '..\\AWG\\AWG_status.h5'
        self.critical_error = False
        
    def ramp_DAC(self, name, start, stop, dim, init_at=None, method='Linear'):
        """ Ramps one DAC output on dimension dim. If dim==0, the fastramp is used. """
        if name not in [self.DAC[key].name for key in self.DAC.keys()]:
            log.send(level='critical',
                        context='RT_fastseq.ramp_DAC',
                        message='unknown parameter {}'.format(name))
            self.critical_error = True
            return 0
        elif dim == 0:     # adding to the fastseq
            channel_id = self.DAC[name].uint64s[0] * 8 + self.DAC[name].uint64s[1]
            if channel_id not in self.fs.uint64s[4:20]:
                log.send(level='critical',
                            context='RT_fastseq.ramp_DAC',
                            message='channel {} is not useable for dim 0'.format(channel_id))
                self.critical_error = True
                return 0
            self.fast_ramp[name] = {}
            self.fast_ramp[name]['method'] = method
            self.fast_ramp[name]['start'] = start
            self.fast_ramp[name]['stop'] = stop
            self.fast_ramp[name]['channel'] = self.fs.uint64s[4:20].index(channel_id)
        else:      # adding to sweep_param
            self.sweep_param[name] = {}
            self.sweep_param[name]['method'] = method
            self.sweep_param[name]['start'] = start
            self.sweep_param[name]['stop'] = stop
            self.sweep_param[name]['dim'] = dim
            
        if init_at is not None:
            self.init_val[name] = init_at
        else:  # unless specified, param is initialized at starting value
            self.init_val[name] = start
        
        log.send(level='info',
                    context='RT_fastseq.ramp_DAC',
                    message='added {}'.format(name))
        return 1
    
    def ramp_RF(self, name, start, stop, dim, init_at=None, method='Linear'):
        """ Ramps RF freq/power on dimension dim>0 """
        if dim==0:
            log.send(level='critical',
                        context='RT_fastseq.ramp_RF',
                        message='dim 0 not useable for parameter {}'.format(name))
            self.critical_error = True
            return 0
        if name not in [self.RF[key].name for key in self.RF.keys()]:
            log.send(level='critical',
                        context='RT_fastseq.ramp_RF',
                        message='unknown parameter {}'.format(name))
            self.critical_error = True
            return 0
        else:      # adding to sweep_param
            self.sweep_param[name] = {}
            self.sweep_param[name]['method'] = method
            self.sweep_param[name]['start'] = start
            self.sweep_param[name]['stop'] = stop
            self.sweep_param[name]['dim'] = dim
            
        if init_at is not None:
            self.init_val[name] = init_at
        else:  # unless specified, param is initialized at starting value
            self.init_val[name] = start
        
        log.send(level='debug',
                    context='RT_fastseq.ramp_RF',
                    message='added {}'.format(name))
        return 1
        
    def ramp_slot(self, slotNo, name, start, stop, dim, init_at=None, method='Linear'):
        """ Moves a sequence slot in dimension dim. """
        if dim==0:
            log.send(level='critical',
                        context='RT_fastseq.ramp_slot',
                        message='dim 0 not useable for parameter {}'.format(name))
            self.critical_error = True
            return 0
        elif slotNo >= len(self.sequence):
            log.send(level='critical',
                        context='RT_fastseq.ramp_slot',
                        message='slot {} not in sequence (parameter {})'.format(slotNo,name))
            self.critical_error = True
            return 0
        elif self.sequence[slotNo][0] in ['Trigger', 'Jump', 'End']:
            log.send(level='critical',
                        context='RT_fastseq.ramp_slot',
                        message='slot {} is not DAC or timing (parameter {})'.format(slotNo,name))
            self.critical_error = True
            return 0
        elif self.sequence[slotNo][0] == 'Timing':
            slot = mc.FastSequenceSlot(name=name, 
                                        IPAddress=self.fs.strings[1],
                                        unit='ms',
                                        slotNo=slotNo,
                                        upperlimit=10000,
                                        lowerlimit=0)
        else: # DAC slot
            if self.sequence[slotNo][0] not in name: # avoid wrong slot selection
                log.send(level='critical',
                            context='RT_fastseq.ramp_slot',
                            message='given slot name {} does not match the one is sequence at position {} ({})'.format(self.sequence[slotNo][0],slotNo,name))
                self.critical_error = True
                return 0
            slot = mc.FastSequenceSlot(name=name,
                        IPAddress=self.fs.strings[1],
                        unit='V',
                        slotNo=slotNo,
                        upperlimit=self.fs.doubles[0],
                        lowerlimit=self.fs.doubles[1])
                                        
        self.fs_slots[name] = slot  # creating new instr
        self.sweep_param[name] = {} # and adding to the sweep dict
        self.sweep_param[name]['method'] = method
        self.sweep_param[name]['start'] = start
        self.sweep_param[name]['stop'] = stop
        self.sweep_param[name]['dim'] = dim
        
        if init_at is not None:
            self.init_val[name] = init_at
        else:  # unless specified, param is initialized at starting value
            self.init_val[name] = start
        
        log.send(level='debug',
                    context='RT_fastseq.ramp_slot',
                    message='added {}'.format(name))
        return 1
    
    def add_wait(self, name, index, ms, axis):
        """ Adds a custom wait everytime the index of the axis is at a given value """
        if axis == 0:     # adding to the fastseq
            log.send(level='critical',
                        context='RT_fastseq.add_wait',
                        message='dim 0 not useable for parameter {}'.format(name))
            self.critical_error = True
            return 0
        wait = mc.mswait(name=name,
                         unit='ms',
                         ulimit=100000,
                         llimit=0)
        self.waits[name] = wait
        
        dims = self.sweep_dim[1:]
        ax = axis-1
        arr = np.zeros(dims, dtype=np.int)
        arr = np.swapaxes(arr, 0, ax)
        arr[index, :] = ms
        arr = np.swapaxes(arr, 0, ax)
        sweep = mc.single_sweep(name = name,
                                parameter = 0,
                                ar = arr,
                                dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
                                creationMethod = '1_pos',
                                sweep_dim = axis, # sweep dimension 0: array sweep, 1: sweep along 1st dim, 2: sweep along 2nd dim, ....
                                )
        self.sweep_list.append(sweep)  
        
        log.send(level='debug',
                    context='RT_fastseq.add_wait',
                    message='added {}'.format(name))
        return 1

    def build_seq(self):
         self.fast_channels = []
         seq = []
         for name,val in self.sequence:
             if name=='Trigger':
                 seq.append([101,int(val[::-1],2)])   # convert to bitwise value
             elif name=='Timing':
                 seq.append([102,val])
             elif name=='Jump':
                 seq.append([103,val])
             elif name=='End':
                 seq.append([100,0])
             else:
                 channel_id = self.DAC[name].uint64s[0]*8+self.DAC[name].uint64s[1]
                 if channel_id not in self.fs.uint64s[4:20]:
                     print ('Error adding parameter ' + name + ' - channel '+str(channel_id)+' not useable')
                     return 0  
                 elif self.init_val[name]+val<-2 or self.init_val[name]+val>0:
                     print ('Error setting slot ' + str(len(seq)) + ' - DAC output out of boundaries')
                     return 0  
                 else:
                     pos = self.fs.uint64s[4:20].index(channel_id)
                     seq.append([pos,val])
         self.fs.sequence = np.array(seq).T
         return 1

    def build_sweep(self):
        """ Create value arrays for every instrument moved in Map (dim>0) """
        for key in self.sweep_param.keys():
            if self.sweep_param[key]['method'] in ['Linear','log10']:
                start = self.sweep_param[key]['start']
                stop = self.sweep_param[key]['stop']
                axis = self.sweep_param[key]['dim'] - 1 # dim 0 removed
                arr = ArrayGenerator(dims = self.sweep_dim[1:], 
                                        axis = axis, 
                                        initial = start, 
                                        final = stop, 
                                        method = self.sweep_param[key]['method'])
                sweep = mc.single_sweep(name = key,
                                        parameter = 0,
                                        ar = arr,
                                        dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
                                        creationMethod = self.sweep_param[key]['method'],
                                        sweep_dim = axis)
            else: 
                log.send(level='debug',
                            context='RT_fastseq.build_sweep',
                            message='Only 1D linear or log10 sweeps supported for now.')
                return 0

            if key in self.fs_slots.keys():
                sweep.param = self.fs_slots[key].getParameter() # adding slot n°
                if self.sequence[sweep.param][0] != 'Timing': # Safety for DAC (V+dV)
                    DAC_name = self.sequence[sweep.param][0]
                    [ul,ll] = self.DAC[DAC_name].getLimits()
                    V0 = self.init_val[DAC_name]
                    if any([V0+dV<ll or V0+dV>ul for dV in [start,stop]]):
                        log.send(level='debug',
                                    context='RT_fastseq.build_sweep',
                                    message='{} on slot {} would be out of limits.'.format(DAC_name,sweep.param))
                        return 0
            elif key in self.RF.keys():
                sweep.param = self.RF[key].getParameter()
            self.sweep_list.append(sweep)

        log.send(level='debug',
                    context='RT_fastseq.build_sweep',
                    message='done.')
        return 1

    def __str__(self):
        """ Prints a summary of the map content"""
        txt = '--- Fast seq ---' + os.linesep
        txt += '{} points, {} ms per point'.format(self.sweep_dim[0], self.ms_per_point) + os.linesep
        for i, line in enumerate(self.sequence):
            txt += '{}.\t{}\t{}'.format(i, line[0], line[1]) + os.linesep
            if i > 49: # don't plot more than 50 elements
                txt += '\t\t...' + os.linesep
                break
        txt += '--- Step dimensions ---' + os.linesep
        txt += '{} points, wait {} ms'.format(self.sweep_dim[1:], self.step_wait) + os.linesep
        for name in self.sweep_param.keys():
            if name in self.fs_slots.keys():
                slotNo = self.fs_slots[name].getParameter()
                txt += 'dim {} : {} on slot {} from {} to {}'.format(self.sweep_param[name]['dim'], name, slotNo, self.sweep_param[name]['start'], self.sweep_param[name]['stop'])
            else:
                txt += 'dim {} : {} from {} to {}'.format(self.sweep_param[name]['dim'], name, self.sweep_param[name]['start'], self.sweep_param[name]['stop'])
            txt += os.linesep
        return txt[:-len(os.linesep)]

    def update_timings(self):
        """ Modifies the ADC and fastseq settings for the current Map"""
        sampling_rate_per_channel = self.ADC.uint64s[2] / self.ADC.uint64s[1]
        RT_avg = self.ms_per_point / 1000. * sampling_rate_per_channel
        if int(RT_avg) != RT_avg:   # if you want to wait 1.0067 ms, you're gonna have a bad time
            log.send(level='info',
                        context='RT_fastseq.update_timings',
                        message='rounding integrated points to {}'.format(int(RT_avg)))
        RT_avg = int(RT_avg)
        self.ADC.uint64s[3] = 1 # Turning on real time
        self.ADC.uint64s[4] = RT_avg
        sample_count = self.sweep_dim[0] * RT_avg # total sample count per sweep
        self.ADC.uint64s[7] = sample_count
        if self.ADC.uint64s[6] < sample_count:   # Buffer too small
            log.send(level='info',
                        context='RT_fastseq.update_timings',
                        message='ADC buffer size had to be increased to {}'.format(sample_count))
            self.ADC.uint64s[6] = sample_count
        self.fs.uint64s[2] = int(self.sweep_dim[0])	 # set sample count
        
        log.send(level='debug',
                    context='RT_fastseq.update_timings',
                    message='done.')

    def build_files(self):
        """ Creates config and exp files """
        comment = self.__str__()
        log.send(level='info',
                    context='RT_fastseq.build_sweep',
                    message=os.linesep + comment)

        self.inst_list = [self.fs, self.ADC]
        self.inst_list += [self.DAC[key] for key in self.DAC.keys()]
        self.inst_list += [self.waits[key] for key in self.waits.keys()]
        self.inst_list += [self.fs_slots[key] for key in self.fs_slots.keys()]
        self.inst_list += [self.RF[key] for key in self.RF.keys()]
        self.conf = mc.MeasConfig(filepath=self.config_path,
                                    initial_wait = self.initial_wait,
                                    wait_before_meas = 1,	# useless
                                    integration_time = 10,	# useless
                                    wait_after_step_move = self.step_wait,
                                    fastSweep = True,
                                    ramp = False,
                                    listOfInst = self.inst_list,
                                    fastChannelNameList=[])

        self.conf.write()
        log.send(level='debug',
                    context='RT_fastseq.build_files',
                    message=os.path.basename(self.config_path) + ' created.')
        
        init_move_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})
        init_move = []
        for (name, val) in self.init_val.items():
            if name in self.fs_slots.keys():
                param = self.fs_slots[name].getParameter() # adding slot n°
            elif name in self.RF.keys():
                param = self.RF[name].getParameter()
            else:
                param = 0
            init_move.append((name, param, val))
        init_move = np.array(init_move,dtype=init_move_dt)
        return_to_init = True
        filename = os.path.basename(self.exp_path).split('.')[0]
        self.exp = mc.Experiment(fileName = filename,
                                    saveFolder = os.path.dirname(self.exp_path),
                                    configFilePath = self.config_path,
                                    sweepDim = self.sweep_dim[1:],
                                    comments = comment,
                                    sweepList = self.sweep_list,
                                    readoutlist = [],
                                    sweep_inst_bools = list(),
                                    readout_inst_bools = list(),
                                    Experimental_bool_list = [return_to_init, True],
                                    Initial_move = init_move)
        
        out = self.exp.write(fpath=self.exp_path)
        if out==0:
            log.send(level='debug',
                        context='RT_fastseq.build_files',
                        message=os.path.basename(self.exp_path) + ' created.')
            return 1
        else:
            return 0

    def build_all(self):
        if self.critical_error:
            return 0
        ans = self.build_seq()
        if ans == 0:
            return 0
        ans = self.build_sweep()
        if ans == 0:
            return 0
        ans = self.build_files()
        if ans == 0:
            return 0
        if self.use_AWG:
            self.add_AWG_infos()
        return  1
    
    def add_AWG_infos(self):
        AWG_status_path = '..\\AWG\\AWG_status.h5'
        if os.path.isfile(AWG_status_path):
            src = AWG_status_path
            dest = self.exp_path.replace('_exp_','_awg_')
            copy2(src,dest)

    def send(self, show_prompt = True):
        if show_prompt:
            ans = MessageBoxW(None, self.__str__(), 'Send Map?', 1)
            if ans != 1:    # abort
                log.send(level='critical',
                            context='RT_fastseq.send',
                            message='sending aborted.')
                return 0
        # go for launch
        log.send(level='info',
                    context='RT_fastseq.send',
                    message=os.path.basename(self.exp_path) + ' sent.')
        sendFiles(fileList=[self.exp_path])
        return 1