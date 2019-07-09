# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

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
import MeasurementBase.measurement_classes as mc
import MeasurementBase.FastSequenceGenerator as fsg
from MeasurementBase.SendFileNames import sendFiles
from MeasurementBase.ArrayGenerator import ArrayGenerator
from MeasurementBase.FPGA_timing_calculator import FPGA_timing_calculator
from QuickMap.BM13_config_CD3_1 import DAC_ADC_config, RF_config
from QuickMap.find_unused_name import find_unused_name

class StabilityDiagram():
    def __init__(self, folder=os.getcwd(), prefix='test'):
        self.folder = folder
        self.prefix = prefix
        self.findex, self.config_path, self.exp_path = find_unused_name(folder, prefix, search_adjacent_folders=True)
        
        self.DAC, self.fs, self.ADC = DAC_ADC_config()  
        self.RF = RF_config()  
        self.waits = {}
        self.fs_slots = {}
        
        self.init_val = {}     # dict of [values]
        self.fast_ramp = {}    # dict of [method,start,stop,channel]
        self.sweep_param = {}  # dict of [method,start,stop,dim]
        self.sweep_list = []
        self.sequence = []  # sequence (without ramp)
        self.pre_ramp_seq = []
        
        self.initial_wait = 100    # ms before the show starts
        self.ms_per_point = 1      # integration time (fastseq divider)
        self.step_wait = 1         # ms wait after every fastseq
        self.sweep_dim = []

        self.critical_error = False
        
    def ramp_DAC(self, name, start, stop, dim, init_at=None, method='Linear'):
        """ Ramps one DAC output on dimension dim. If dim==0, the fastramp is used. """
        if name not in [self.DAC[key].name for key in self.DAC.keys()]:
            log.send(level='critical',
                        context='StabilityDiagram.ramp_DAC',
                        message='unknown parameter {}'.format(name))
            self.critical_error = True
            return 0
        elif dim == 0:     # adding to the fastseq
            channel_id = self.DAC[name].uint64s[0] * 8 + self.DAC[name].uint64s[1]
            [ul,ll] = self.fs.getLimits()
            if (init_at is not None) and any([Vi-init_at<ll or Vi-init_at>ul for Vi in [start,stop]]):
                log.send(level='critical',
                            context='StabilityDiagram.ramp_DAC',
                            message='DAC {} is out of range on dim 0'.format(name))
                self.critical_error = True
                return 0
            self.fast_ramp[name] = {}
            self.fast_ramp[name]['method'] = method
            self.fast_ramp[name]['start'] = start
            self.fast_ramp[name]['stop'] = stop
            self.fast_ramp[name]['channel'] = channel_id
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
                    context='StabilityDiagram.ramp_DAC',
                    message='added {}'.format(name))
        return 1
    
    def ramp_RF(self, name, start, stop, dim, init_at=None, method='Linear'):
        """ Ramps RF freq/power on dimension dim>0 """
        if dim==0:
            log.send(level='critical',
                        context='StabilityDiagram.ramp_RF',
                        message='dim 0 not useable for parameter {}'.format(name))
            self.critical_error = True
            return 0
        if name not in [self.RF[key].name for key in self.RF.keys()]:
            log.send(level='critical',
                        context='StabilityDiagram.ramp_RF',
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
                    context='StabilityDiagram.ramp_RF',
                    message='added {}'.format(name))
        return 1
        
    def ramp_slot(self, slotNo, name, start, stop, dim, init_at=None, method='Linear'):
        """ Moves a sequence slot in dimension dim. """
        if dim==0:
            log.send(level='critical',
                        context='StabilityDiagram.ramp_slot',
                        message='dim 0 not useable for parameter {}'.format(name))
            self.critical_error = True
            return 0
        elif slotNo >= len(self.sequence):
            log.send(level='critical',
                        context='StabilityDiagram.ramp_slot',
                        message='slot {} not in sequence (parameter {})'.format(slotNo,name))
            self.critical_error = True
            return 0
        elif self.sequence[slotNo][0] in ['Trigger out', 'Trigger in', 'Jump', 'End']:
            log.send(level='critical',
                        context='StabilityDiagram.ramp_slot',
                        message='slot {} is not DAC or timing (parameter {})'.format(slotNo,name))
            self.critical_error = True
            return 0
        elif self.sequence[slotNo][0] == 'Timing':
            if max([start,stop])>2**16-1:
                log.send(level='critical',
                            context='StabilityDiagram.ramp_slot',
                            message='increase the range of timing slot {})'.format(slotNo))
                self.critical_error = True
                return 0
            slot = mc.FastSequenceSlot(name=name, 
                                        IPAddress=self.fs.strings[1],
                                        unit=self.sequence[slotNo][1],
                                        slotNo=slotNo,
                                        upperlimit=2^16-1,
                                        lowerlimit=0)
        else: # DAC slot
            if self.sequence[slotNo][0] not in name: # avoid wrong slot selection
                log.send(level='critical',
                            context='StabilityDiagram.ramp_slot',
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
                    context='StabilityDiagram.ramp_slot',
                    message='added {}'.format(name))
        return 1
        
    def add_wait(self, name, index, ms, axis):
        """ Adds a custom wait everytime the index of the axis is at a given value """
        if axis == 0:     # adding to the fastseq
            log.send(level='critical',
                        context='StabilityDiagram.add_wait',
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
                    context='StabilityDiagram.add_wait',
                    message='added {}'.format(name))
        return 1
    
    def update_timings(self):
        """ Modifies the ADC and fastseq settings for the current Map"""
        sampling_rate_per_channel = self.ADC.uint64s[1] / self.ADC.uint64s[0]
        RT_avg = self.ms_per_point / 1000. * sampling_rate_per_channel
        if int(RT_avg) != RT_avg:   # if you want to wait 1.0067 ms, you're gonna have a bad time
            log.send(level='info',
                        context='StabilityDiagram.update_timings',
                        message='rounding integrated points to {}'.format(int(RT_avg)))
        RT_avg = int(RT_avg)
        self.ADC.uint64s[2] = RT_avg
        # pre_ramp_time = FPGA_timing_calculator(self.sequence,ms_per_DAC=self.ms_per_point) # total time in ms
        # pre_ramp_pts = np.ceil(pre_ramp_time*sampling_rate_per_channel/1000.)+1 #+1 because the first DAC is updated after self.ms_per_point
        # tot_time = pre_ramp_time + self.sweep_dim[0]*len(self.fast_channels)*self.ms_per_point # total time in ms
        N_DAC = self.sweep_dim[0]*len(self.fast_channels)
        sample_count = (N_DAC+1)*RT_avg
        self.ADC.uint64s[3] = 1 # Turning on segment mode
        self.ADC.uint64s[4] = sample_count
        if self.ADC.uint64s[6] < sample_count:   # Buffer too small
            log.send(level='info',
                        context='StabilityDiagram.update_timings',
                        message='ADC buffer size had to be increased to {}'.format(sample_count))
            self.ADC.uint64s[6] = sample_count
            
        self.fs.uint64s[2] = N_DAC	 # set sample count for FPGA
        self.fs.uint64s[0] = np.ceil(self.ms_per_point*1000)	# us per DAC
        
        segment_param = [N_DAC,RT_avg,RT_avg,RT_avg]
        self.ADC.strings[5] = ';'.join([str(int(ai)) for ai in segment_param])
        
        log.send(level='debug',
                    context='StabilityDiagram.update_timings',
                    message='done.')

    def build_pre_ramp_seq(self):
        """ Inserts a custom sequence before the map begins """
        seq = []
        for name, val1, val2 in self.sequence:
            if name == 'Timing':
                if val1 not in ['1us','10us','100us','1ms']:
                    log.send(level='critical',
                                context='StabilityDiagram.build_pre_ramp_seq',
                                message='Range of timing slot {} not understood'.format(len(seq)))
                    return 0
                range_ = ['1us','10us','100us','1ms'].index(val1)
                if val2>2**16-1:
                    log.send(level='critical',
                                context='StabilityDiagram.build_pre_ramp_seq',
                                message='Increase range of timing slot {}'.format(len(seq)))
                    return 0
                seq.append([1, range_, val2])
            elif name == 'Trigger out':
                seq.append([2, 0, int(val2[::-1], 2)])   # convert to bitwise value
            elif name == 'Jump':
                if val1>1023:
                    val1 = 1023
                    log.send(level='critical',
                                context='StabilityDiagram.build_pre_ramp_seq',
                                message='cannot jump more than 1023 times')
                    return 0
                seq.append([3, val1, val2])
            if name == 'Trigger in':
                seq.append([4, int(val1[::-1], 2), int(val2[::-1], 2)])   # convert to bitwise value
            elif name == 'End':
                seq.append([5, 0, 0])
            else: # DAC
                if name not in self.DAC.keys():
                    log.send(level='critical',
                                context='StabilityDiagram.build_pre_ramp_seq',
                                message='Unknown DAC name {}'.format(name))
                    return 0
                [ul,ll] = self.DAC[name].getLimits()
                elif val2<ll or val2>ul:
                    log.send(level='critical',
                                context='StabilityDiagram.build_pre_ramp_seq',
                                message='DAC {} on slot {} is out of limits{}'.format(name,len(seq)))
                    return 0
                [ul,ll] = self.fs.getLimits()
                V0 = self.init_val[name]
                elif val2-V0<ll or val2-V0>ul:
                    log.send(level='critical',
                                context='StabilityDiagram.build_pre_ramp_seq',
                                message='DAC {} on slot {} is out of limits{}'.format(name,len(seq)))
                    return 0
                channel_id = self.DAC[name].uint64s[0] * 8 + self.DAC[name].uint64s[1]
                seq.append([0, channel_id, val2])
        self.pre_ramp_seq = np.array(seq).T
        
        log.send(level='debug',
                    context='StabilityDiagram.build_pre_ramp_seq',
                    message='done.')
        return 1
     
    def build_fastramp(self):
        """ Create the fastseq for the FPGA """
        self.fast_channels = []
        start = []
        stop = []
        for name in self.fast_ramp.keys():
            start.append(self.fast_ramp[name]['start'])
            stop.append(self.fast_ramp[name]['stop'])
            self.fast_channels.append(self.fast_ramp[name]['channel'])
            
        ramp = fsg.createRamp(points=self.sweep_dim[0],
                    fast_channels=self.fast_channels,
                    initial=start,
                    final=stop)
        if self.pre_ramp_seq == []:
           self.fs.sequence = ramp
           self.fs.uint64s[5] = 2 # StartAt (Trigger,Ramp,End)
        else:
            N = np.size(self.pre_ramp_seq, 1)
            self.fs.sequence = np.concatenate((self.pre_ramp_seq, ramp[:,1:]), 1) # remove first trigger from ramp
            # self.fs.sequence[1,-1] = len(self.fs.sequence[1,:]) - 1  # update jump
            self.fs.uint64s[5] = N-1
        
        if len(self.fs.sequence[1,:]) > 4096:        
            log.send(level='critical',
                    context='StabilityDiagram.build_fastramp',
                    message='fast sequence is too large.')
            return 0
        else:
            log.send(level='debug',
                        context='StabilityDiagram.build_fastramp',
                        message='done.')
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
                                        sweep_dim = axis+1)
            else: 
                log.send(level='debug',
                            context='StabilityDiagram.build_sweep',
                            message='Only 1D linear or log10 sweeps supported for now.')
                return 0

            if key in self.fs_slots.keys():
                sweep.param = self.fs_slots[key].getParameter() # adding slot n°
                if self.sequence[sweep.param][0] == 'Timing':
                    if max([start,stop])>2**16-1:
                        log.send(level='critical',
                                    context='StabilityDiagram.build_sweep',
                                    message='{} on slot {} would be out of limits.'.format(key,sweep.param))
                        return 0
                else: # Safety for DAC
                    DAC_name = self.sequence[sweep.param][0]
                    [ul,ll] = self.DAC[DAC_name].getLimits()
                    if any([Vi<ll or Vi>ul for Vi in [start,stop]]):
                        log.send(level='critical',
                                    context='StabilityDiagram.build_sweep',
                                    message='{} on slot {} would be out of limits.'.format(DAC_name,sweep.param))
                        return 0
                    [ul,ll] = self.fs.getLimits()
                    V0 = self.init_val[DAC_name]
                    elif any([Vi-V0<ll or Vi-V0>ul for Vi in [start,stop]]):
                        log.send(level='critical',
                                    context='StabilityDiagram.build_pre_ramp_seq',
                                    message='DAC {} on slot {} is out of limits{}'.format(name,len(seq)))
                        return 0
            elif key in self.RF.keys():
                sweep.param = self.RF[key].getParameter()
            self.sweep_list.append(sweep)

        log.send(level='debug',
                    context='StabilityDiagram.build_sweep',
                    message='done.')
        return 1
            
    def __str__(self):
        """ Prints a summary of the map content"""
        txt = '--- Pre-ramp seq ---' + os.linesep
        for i, line in enumerate(self.sequence):
            txt += '{}.\t{}\t{}\t{}'.format(i, line[0], line[1], line[2]) + os.linesep
        txt += '--- Fast ramp ---' + os.linesep
        txt += '{} points, {} ms per DAC'.format(self.sweep_dim[0], self.ms_per_point) + os.linesep
        for name in self.fast_ramp.keys():
            txt += '{} on channel {} : '.format(name, self.fast_ramp[name]['channel'])
            txt += 'init {}, from {} to {}'.format(self.init_val[name], self.fast_ramp[name]['start'], self.fast_ramp[name]['stop'])
            txt += os.linesep
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
        
    def build_files(self):
        """ Creates config and exp files """
        comment = self.__str__()
        log.send(level='info',
                    context='StabilityDiagram.build_sweep',
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
                                    ramp = True,
                                    listOfInst = self.inst_list,
                                    fastChannelNameList=list(self.fast_ramp.keys()))

        self.conf.write()
        log.send(level='debug',
                    context='StabilityDiagram.build_files',
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
        
        out = self.exp.write(fpath=self.exp_path, data_size=[self.sweep_dim[0]*len(self.fast_channels)]+self.sweep_dim[1:])
        if out==0:
            log.send(level='debug',
                        context='StabilityDiagram.build_files',
                        message=os.path.basename(self.exp_path) + ' created.')
            return 1
        else:
            return 0

    def build_all(self):
        if self.critical_error:
            return 0
        ans = self.build_pre_ramp_seq()
        if ans == 0:
            return 0
        ans = self.build_fastramp()
        if ans == 0:
            return 0
        self.update_timings()
        ans = self.build_sweep()
        if ans == 0:
            return 0
        ans = self.build_files()
        if ans == 0:
            return 0
        return 1

    def send(self, show_prompt = True):
        if show_prompt:
            ans = MessageBoxW(None, self.__str__(), 'Send Map?', 1)
            if ans != 1:    # abort
                log.send(level='critical',
                            context='StabilityDiagram.send',
                            message='sending aborted.')
                return 0
        # go for launch
        log.send(level='info',
                    context='StabilityDiagram.send',
                    message=os.path.basename(self.exp_path) + ' sent.')
        sendFiles(fileList=[self.exp_path])
        return 1