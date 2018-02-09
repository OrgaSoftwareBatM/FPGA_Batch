# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:38:49 2018

@author: manip.batm
"""

# from __future__ import str
import os,sys
import numpy as np
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import MeasurementBase.measurement_classes as mc
import MeasurementBase.FastSequenceGenerator as fsg
from MeasurementBase.SendFileNames import sendFiles
from GUI.Experiment_GUI import arrayGenerator
from Bermousque_config import DAC_ADC_config

def find_unused_name(folder,prefix):
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
        self.waits = {}
        
        self.init_val = {}     # dict of [values]
        self.fast_ramp = {}    # dict of [start,stop,fast_channel]
        self.sweep_param = {}  # dict of [start,stop,dim]
        self.fs_slots = {}
        self.sweep_list = []
        self.sequence = []
        self.pre_ramp_seq = []
        
        self.initial_wait = 100    # ms before everything
        self.ms_per_point = 1      # integration time (fastseq divider)
        self.step_wait = 1         # ms wait after every fastseq
        self.sweep_dim = []
        
    def ramp_DAC(self,name,start,stop,dim,init_at=None):
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
        
    def ramp_slot(self,slotNo,name,start,stop,dim,init_at=None):
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
        self.ADC.uint64s[7] = int(self.sweep_dim[0]) # set sample count
        self.fs.uint64s[2] = int(self.sweep_dim[0])	 # set sample count
        self.ADC.uint64s[4] = int(self.ADC.uint64s[2]/self.ADC.uint64s[1]*self.ms_per_point/1000.) # sampling rate per channel * time per point
        self.fs.uint64s[0] = int(2222*self.ms_per_point)	# set divider

    def build_pre_ramp_seq(self):
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
            self.sweep_list.append(sweep)
            
    def txt_summary(self):
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
        comment = self.txt_summary()
        print (comment)
        self.inst_list = [self.fs,self.ADC]+[self.DAC[key] for key in self.DAC.keys()]
        self.inst_list += [self.waits[key] for key in self.waits.keys()]
        self.inst_list += [self.fs_slots[key] for key in self.fs_slots.keys()]
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
            ans = input('SEND THIS MAP? (Y/N)    ')
            if ans in ['y','Y']:
                print ('Sending to Labview')
                sendFiles(fileList=[self.exp_path])
            else:
                print ('Sending aborted')


###########################
####	 CHOOSE FILE NAME
###########################
##folder = os.getcwd()+'\\test'
#folder = 'D:\\T23\\CD1'
#prefix = 'test_fastramp_'
#Map = StabilityDiagram(folder,prefix)
#
###########################
####	 FASTSEQ + CONF FILE   			
###########################
#Map.initial_wait = 100    # ms before everything
#Map.ms_per_point = 1.     # integration time (fastseq divider)
#Map.step_wait = 1.         # ms wait after every fastseq
#
#Map.sweep_dim = [101,21]
#Map.ramp_DAC('3:0',-0.2,0.2,0)
#Map.ramp_DAC('3:1',0.2,-0.2,1)
#Map.init_val['3:2']=0.33
##Map.ramp_DAC('2:2',-0.3,0.3,2)
##Map.ramp_DAC('0:3',0.05,0.05,3)
#
##Map.add_wait('wait_bg',0,10000,1) # (index,ms,axis) wait n ms at index for given axis
#
#Map.ADC.uint64s[7] = Map.sweep_dim[0]
#
#Map.build_fastramp()
#Map.build_sweep()
#Map.build_files()