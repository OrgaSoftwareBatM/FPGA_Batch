# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:41:04 2018

@author: manip.batm
"""
# from __future__ import str
import os,sys
import ctypes 
MessageBoxW = ctypes.windll.user32.MessageBoxW
import numpy as np
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import MeasurementBase.measurement_classes as mc
import MeasurementBase.FastSequenceGenerator as fsg
from MeasurementBase.SendFileNames import sendFiles
from GUI.Experiment_GUI import arrayGenerator
from Bermousque_config_reflecto import DAC_ADC_config,RF_config


def find_unused_name(folder,prefix):
    """ Finds a config and exp file names that don't exist """
    findex = 0
    exists = True
    while exists:
    	findex += 1
    	config_path = folder+'\\'+prefix+'config_'+str(findex)+'.h5'
    	exp_path = folder+'\\'+prefix+ 'exp_'+str(findex)+'.h5'
    	exists = os.path.isfile(config_path) or os.path.isfile(exp_path)
    return findex,config_path,exp_path

class StabilityDiagram():
    def __init__(self,folder=os.getcwd(),prefix='test'):
        self.folder = folder
        self.prefix = prefix
        self.findex,self.config_path,self.exp_path = find_unused_name(folder,prefix)
        
        self.DAC,self.fs,self.ADC = DAC_ADC_config()  
        self.RF = RF_config()  
        self.waits = {}
        self.fs_slots = {}
        
        self.init_val = {}     # dict of [values]
        self.fast_ramp = {}    # dict of [start,stop,fast_channel]
        self.sweep_param = {}  # dict of [start,stop,dim]
        self.sweep_list = []
        self.sequence = []  # full sequence (with ramp)
        self.pre_ramp_seq = []
        
        self.initial_wait = 100    # ms before everything
        self.ms_per_point = 1      # integration time (fastseq divider)
        self.step_wait = 1         # ms wait after every fastseq
        self.sweep_dim = []
        
    def ramp_DAC(self,name,start,stop,dim,init_at=None):
        """ Ramps one DAC output on dimension dim. If dim==0, the fastramp is used. """
        if name not in [self.DAC[key].name for key in self.DAC.keys()]:
            print ('Error adding parameter ' + name + ' - unknown parameter')
            return 0
        elif dim == 0:     # adding to the fastseq
            channel_id = self.DAC[name].uint64s[0]*8+self.DAC[name].uint64s[1]
            if channel_id not in self.fs.uint64s[4:20]:
                print ('Error adding parameter ' + name + ' - channel '+str(channel_id)+' not useable')
                return 0
            self.fast_ramp[name] = [start,stop,self.fs.uint64s[4:20].index(channel_id)]
        else:      # adding to sweep_param
            self.sweep_param[name] = [start,stop,dim]
            
        if init_at is not None:
            self.init_val[name] = init_at
        else:  # unless specified, param is initialized at starting value
            self.init_val[name] = start
        return 1
    
    def ramp_RF(self,name,start,stop,dim,init_at=None):
        """ Ramps RF freq/power on dimension dim>0 """
        if dim==0:
             print ('Error adding parameter ' + name + ' - dim 0 not useable')
             return 0
        if name not in [self.RF[key].name for key in self.RF.keys()]:
            print ('Error adding parameter ' + name + ' - unknown parameter')
            return 0
        else:      # adding to sweep_param
            self.sweep_param[name] = [start,stop,dim]
            
        if init_at is not None:
            self.init_val[name] = init_at
        else:  # unless specified, param is initialized at starting value
            self.init_val[name] = start
        return 1
        
    def ramp_slot(self,slotNo,name,start,stop,dim,init_at=None):
        """ Moves a sequence slot in dimension dim. """
        if dim==0:
             print ('Error adding parameter ' + name + ' - dim 0 not useable')
             return 0
        elif slotNo >= len(self.sequence):
             print ('Error adding parameter ' + name + ' - slot is not in sequence')
             return 0
        elif self.sequence[slotNo][0] in ['Trigger','Jump','End']:
             print ('Error adding parameter ' + name + ' - slot is not DAC or timing')
             return 0
        elif self.sequence[slotNo][0] == 'Timing':
            slot = mc.FastSequenceSlot(name=name,
                     IPAddress=self.fs.strings[1],
                     unit='ms',
                     slotNo=slotNo,
                     upperlimit=10000,
                     lowerlimit=0)
        else:
            slot = mc.FastSequenceSlot(name=name,
                     IPAddress=self.fs.strings[1],
                     unit='V',
                     slotNo=slotNo,
                     upperlimit=self.fs.doubles[0],
                     lowerlimit=self.fs.doubles[1])
        self.fs_slots[name] = slot  # creating new instr
        self.sweep_param[name] = [start,stop,dim] # and adding to the sweep dict
        
        if init_at is not None:
            self.init_val[name] = init_at
        else:  # unless specified, param is initialized at starting value
            self.init_val[name] = start
        return 1
        
    def add_wait(self,name,index,ms,axis):
        """ Adds a custom wait everytime the index of the axis is at a given value """
        if axis == 0:     # adding to the fastseq
            print ('Error adding wait to the fastseq dim')
            return 0
        wait = mc.mswait(name=name,
                         unit = 'ms',
                         ulimit = 100000,
                         llimit = 0)
        self.waits[name] = wait
        
        dims = self.sweep_dim[1:]
        ax = axis-1
        arr = np.zeros(dims,dtype=np.int)
        arr = np.swapaxes(arr, 0, ax)
        arr[index,:] = ms
        arr = np.swapaxes(arr, 0, ax)
        sweep = mc.single_sweep(name = name,
                                    parameter = 0,
                                    ar = arr,
                                    dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
                                    creationMethod = '1_pos',
                                    sweep_dim = axis, # sweep dimension 0: array sweep, 1: sweep along 1st dim, 2: sweep along 2nd dim, ....
                                    )
        self.sweep_list.append(sweep)  
        return 1
    
    def update_timings(self):
        """ Modifies the ADC and fastseq settings for the current Map"""
        self.ADC.uint64s[7] = int(self.sweep_dim[0]) # set sample count
        self.fs.uint64s[2] = int(self.sweep_dim[0])	 # set sample count
        self.ADC.uint64s[4] = int(self.ADC.uint64s[2]/self.ADC.uint64s[1]*self.ms_per_point/1000.) # sampling rate per channel * time per point
        self.fs.uint64s[0] = int(2222*self.ms_per_point)	# set divider

    def build_pre_ramp_seq(self):
        """ Inserts a custom sequence before the map begins """
        seq = []
        for name,val in self.sequence:
            if name=='Trigger':
                seq.append([101,int(val,2)])   # convert to bitwise value
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
                else:
                    pos = self.fs.uint64s[4:20].index(channel_id)
                    seq.append([pos,val])
        self.pre_ramp_seq = np.array(seq).T
        return 1
     
    def build_fastramp(self):
        """ Create the fastseq for the FPGA """
        self.fast_channels = []
        start = []
        stop = []
        for name in self.fast_ramp.keys():
            start.append(self.fast_ramp[name][0]-self.init_val[name])
            stop.append(self.fast_ramp[name][1]-self.init_val[name])
            self.fast_channels.append(self.fast_ramp[name][2])
        if self.pre_ramp_seq == []:
           self.fs.sequence = fsg.createRamp(points=self.sweep_dim[0],
                                      fast_channels=self.fast_channels,
                                      initial=start,
                                      final=stop)
           self.fs.uint64s[20] = 4
        else:
            N = np.size(self.pre_ramp_seq,1)
            ramp = fsg.createRamp(points=self.sweep_dim[0],
                          fast_channels=self.fast_channels,
                          initial=start,
                          final=stop)
            self.fs.sequence = np.concatenate((self.pre_ramp_seq,ramp[:,1:]),1)
            self.fs.sequence[1,-1] = len(self.fs.sequence[1,:])-1  # update jump
            self.fs.uint64s[20] = N-1
            
    def build_sweep(self):
        """ Create value arrays for every instrument moved in Map (dim>0) """
        for key in self.sweep_param.keys():
            start,stop,axis = self.sweep_param[key]
            arr = arrayGenerator(dims = self.sweep_dim[1:], axis=axis-1, initial = start, final = stop, method = 'Linear')
            sweep = mc.single_sweep(name = key,
                                    parameter = 0,
                                    ar = arr,
                                    dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
                                    creationMethod = 'Linear',
                                    sweep_dim = axis, # sweep dimension 0: array sweep, 1: sweep along 1st dim, 2: sweep along 2nd dim, ....
                                    )
            if key in self.fs_slots.keys():
                sweep.param = self.fs_slots[key].getParameter() # adding slot n°
            elif key in self.RF.keys():
                sweep.param = self.RF[key].getParameter()
            self.sweep_list.append(sweep)
            
    def txt_summary(self):
        """ Prints a summary for approval before starting the map """
        txt = '--- Fast ramp ---' + os.linesep
        txt += '%d points, %f ms per point' % (self.sweep_dim[0],self.ms_per_point)
        txt += os.linesep
        for name in self.fast_ramp.keys():
            txt += name + ' on channel %d : ' % (self.fast_ramp[name][2])
            txt += 'offset %f, from %f to %f' % (self.init_val[name],self.fast_ramp[name][0],self.fast_ramp[name][1])
            txt += os.linesep
        txt += '--- Step dimensions ---' + os.linesep
        txt += '%s points, wait %f ms' % (self.sweep_dim[1:],self.step_wait)
        txt += os.linesep
        for name in self.sweep_param.keys():
            txt += 'dim %d : %s from %f to %f' % (self.sweep_param[name][2],name,self.sweep_param[name][0],self.sweep_param[name][1])
            txt += os.linesep
        return txt
        
    def build_files(self):
        """ Creates config and exp files """
        comment = self.txt_summary()
        print (comment)
        self.inst_list = [self.fs,self.ADC]+[self.DAC[key] for key in self.DAC.keys()]
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
        print(self.config_path + ' created')
        
        init_move_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})
        init_move = []
        for (name,val) in self.init_val.items():
            if name in self.fs_slots.keys():
                param = self.fs_slots[name].getParameter() # adding slot n°
            elif name in self.RF.keys():
                param = self.RF[name].uint64s[1]
            else:
                param = 0
            init_move.append((name,param,val))
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
            print(self.exp_path + ' created') 
            ans = MessageBoxW(None, comment, 'Send Map?', 1)
            # ans = input('SEND THIS MAP? (Y/N)    ')
            # if ans in ['y','Y']:
            if ans == 1:
                print ('Sending to Labview')
                sendFiles(fileList=[self.exp_path])
            else:
                print ('Sending aborted')
