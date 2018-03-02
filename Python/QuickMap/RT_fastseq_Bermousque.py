# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 19:46:45 2017

@author: manip.batm
"""

import os,sys
import numpy as np
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import ctypes 
MessageBoxW = ctypes.windll.user32.MessageBoxW
import MeasurementBase.measurement_classes as mc
import MeasurementBase.FastSequenceGenerator as fsg
from MeasurementBase.SendFileNames import sendFiles
from GUI.Experiment_GUI import arrayGenerator
from Bermousque_config_reflecto import DAC_ADC_config,RF_config
        
def find_unused_name(folder,prefix):
    findex = 0
    exists = True
    while exists:
    	findex += 1
    	config_path = folder+'\\'+prefix+'config_'+str(findex)+'.h5'
    	exp_path = folder+'\\'+prefix+ 'exp_'+str(findex)+'.h5'
    	exists = os.path.isfile(config_path) or os.path.isfile(exp_path)
    return findex,config_path,exp_path

class RT_fastseq():
    def __init__(self,folder=os.getcwd(),prefix='test'):
        self.folder = folder
        self.prefix = prefix
        self.findex,self.config_path,self.exp_path = find_unused_name(folder,prefix)
        
        self.DAC,self.fs,self.ADC = DAC_ADC_config()  
        self.RF = RF_config()  
        self.fs_slots = {}
        
        self.init_val = {}     # dict of [values]
        self.sweep_param = {}  # dict of [start,stop,dim]
        self.sequence = []
        self.sweep_list = []
        
        self.initial_wait = 100    # ms before everything
        self.ms_per_point = 1      # integration time (RT_avg/ADC_freq)
        self.step_wait = 1         # ms wait after every fastseq
        self.sweep_dim = []         
        
    def ramp_DAC(self,name,start,stop,dim,init_at=None):
         if name not in [self.DAC[key].name for key in self.DAC.keys()]:
             print ('Error adding parameter ' + name + ' - unknown parameter')
             return 0
         elif dim == 0:
             print ('Error adding parameter ' + name + ' - dim 0 not useable')
             return 0
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
    
    def build_seq(self):
         self.fast_channels = []
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
         self.fs.sequence = np.array(seq).T
         return 1
     
    def build_sweep(self):
        for key in self.sweep_param.keys():
            start,stop,axis = self.sweep_param[key]
#            if key=='t_{meta}':
#                arr = arrayGenerator(dims = self.sweep_dim[1:], axis=axis-1, initial = start, final = stop, method = 'log10')
#                sweep = mc.single_sweep(name = key,
#                                        parameter = 0,
#                                        ar = arr,
#                                        dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
#                                        creationMethod = 'log10',
#                                        sweep_dim = axis, # sweep dimension 0: array sweep, 1: sweep along 1st dim, 2: sweep along 2nd dim, ....
#                                        )
#            else:
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
        txt = '--- Init ---' + os.linesep
        for key,val in self.init_val.items():
            txt += str(key)+'\t'+str(val) + os.linesep
        txt += '--- Fast seq ---' + os.linesep
        txt += '%d points, %f ms per point' % (self.sweep_dim[0],self.ms_per_point)
        txt += os.linesep
        for i,line in enumerate(self.sequence):
            txt += '%d.\t%s\t%s'%(i,line[0],str(line[1]))+os.linesep
        txt += '--- Step dimensions ---' + os.linesep
        txt += '%s points, wait %f ms' % (self.sweep_dim[1:],self.step_wait)
        txt += os.linesep
        for key,p in self.sweep_param.items():
            if key in self.fs_slots.keys():
                slotNo = self.fs_slots[key].getParameter()
                txt += 'dim %d : %s on slot %d from %f to %f' % (p[2],key,slotNo,p[0],p[1])
            else:
                txt += 'dim %d : %s from %f to %f' % (p[2],key,p[0],p[1])
            txt += os.linesep
        return txt
        
    def reconfig_ADC(self,sampling_rate=250000):
        RT_avg = self.ms_per_point/1000.*sampling_rate/self.ADC.uint64s[1]
        if int(RT_avg) != RT_avg:   # if you want to wait 1.0067 ms, you're gonna have a bad time
            print ('Rounding integrated points to '+str(int(RT_avg)))
        RT_avg = int(RT_avg)
        self.ADC.uint64s[2] = sampling_rate
        self.ADC.uint64s[3] = 1 # Turning on real time
        self.ADC.uint64s[4] = RT_avg
        self.ADC.uint64s[7] = self.sweep_dim[0]*RT_avg
        self.fs.uint64s[2] = self.sweep_dim[0]
        if self.ADC.uint64s[6] < self.sweep_dim[0]*RT_avg:   # Buffer too small
            print ('ADC buffer size had to be increased to '+str(self.sweep_dim[0]*RT_avg))
            self.ADC.uint64s[6] = self.sweep_dim[0]*RT_avg
            
    def build_files(self):
        comment = self.txt_summary()
        print (comment)
        
        self.inst_list = [self.fs,self.ADC]+[self.DAC[key] for key in self.DAC.keys()]
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
        print(self.config_path + ' created')
        
        init_move_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})
        init_move = []
        for (name,val) in self.init_val.items():
            if name in self.fs_slots.keys():
                param = self.fs_slots[name].getParameter() # adding slot n°
            elif name in self.RF.keys():
                param = self.RF[name].getParameter()
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


###########################
####	 CHOOSE FILE NAME
###########################
##folder = os.getcwd()+'\\test'
#folder = 'C:\\Partage\\FPGA_Batch_1_7_3_1\\Test'
#prefix = 'trigger_2_test_'
##findex,config_path,exp_path = find_unused_name(folder,prefix)
#Map = RT_fastseq(folder,prefix)
#
###########################
####	 FASTSEQ + CONF FILE   			
###########################
#Map.initial_wait = 100    # ms before everything
#Map.ms_per_point = 1.      # integration time (RT_avg/ADC_freq)
#Map.step_wait = 1         # ms wait after every fastseq
#
#Map.init_val['0:0'] = -0.1
#
#Map.sequence.append(['Trigger','1111'])
#Map.sequence.append(['Timing',1])
#Map.sequence.append(['Trigger','1000'])
#Map.sequence.append(['0:0',0.])
#Map.sequence.append(['Timing',5])
#Map.sequence.append(['0:0',0.2])
#Map.sequence.append(['Timing',20])
#Map.sequence.append(['0:0',0.])
#Map.sequence.append(['Timing',10])
#Map.sequence.append(['Jump',len(Map.sequence)])
#
#Map.sweep_dim = [31,201,11]
##Map.ramp_DAC('0:0',-0.3,0.2,0)
##Map.ramp_DAC('0:1',0.2,-0.2,1)
##Map.ramp_DAC('0:2',-0.4,-0.5,2)
#Map.ramp_slot(5,'Vload',0.2,0.4,1)
#Map.ramp_slot(6,'Tload',10,20,2)
#
#
#Map.reconfig_ADC(sampling_rate=250e3)
#Map.build_seq()
#Map.build_sweep()
#Map.build_files()

