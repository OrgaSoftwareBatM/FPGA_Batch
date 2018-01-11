# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:06:53 2016

@author: shintaro
"""
import numpy as np
import h5py
import os
from PyQt5 import QtWidgets
from configparser import ConfigParser
import sys
sys.path.insert(0,'') # import parent directory
sys.path.insert(0,'..') # import current directory

""" Fridge specific parameters """
config = ConfigParser()
ans=config.read('Fridge_settings.ini')
print(ans)
FPGA_address = config.get('Instruments','FPGA')
addressList = {}
keys = ['K2000','K34401A','DSP_lockIn','RS_RF','AWG','ATMDelayLine','RF_Attn','A3458']
for key in keys:
    addressList[key] = config.get('Instruments',key)
    

""" parameters """
compress_sweep = True
compress_data = True
compression_level = 9
save_config2ExpFile = True
# special data type for structured array in numpy
init_move_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})
init_position_dt = np.dtype({'names':['Name','kind','Value'],'formats':['S100','u8','f8']})
# special data type to define array of flexible length strings in HDF5 file
flexible_str_dt = h5py.special_dtype(vlen=bytes)

# list of kind for readout instruments and sweep instruments
readout_kind = [0,1,2,3,12]
sweep_kind = [4,5,6,7,8,9,10,11,13,14,15,16]
# list of class name ordered by 'kind' number
classList = ['ADC','K2000','K34401A','A3458','DAC','DAC_Lock_in','RS_RF','AWG','dummy','FastSequences','FastSequenceSlot']
classList+= ['CMD','DSP_lockIn','DSP_lockIn_sweep','mswait','ATMDelayLine','RF_Attn','dummy','dummy','dummy','dummy']
classList+= ['dummy','dummy']
readConfigForExpFile = [False,False,False,False,False,False,True,True,False,True,False]
readConfigForExpFile+= [False,False,False,False,False,False,False,False,False,False,False,False]

"""
--------- Place to be changed when you add a new instruments -----------------------

"""

"""--------------------------------------
--------------------------------------------
 class to generate Experiment file 
 -------------------------------------------
 ----------------------------------------"""
class Experiment():
    def __init__(self,
                 fileName = '',
                 saveFolder = '',
                 configFilePath = '',
                 sweepDim = [101],
                 comments = '',
                 sweepList = [],
                 readoutlist = [],
                 sweep_inst_bools = list(),
                 readout_inst_bools = list(),
                 Experimental_bool_list = [True, False],
                 Initial_move = np.array([('None',100,0.0)],dtype=init_move_dt),
                 Initial_positions=0,
                 ):
        self.filename = fileName
        self.saveFolder = saveFolder
        self.configFile = configFilePath
        self.dim = sweepDim
        self.comments = comments
        self.sweeplist = sweepList
        self.readoutlist = readoutlist
        self.sweep_inst_bools = sweep_inst_bools
        self.readout_inst_bools = readout_inst_bools
        self.Experimental_bool_list = Experimental_bool_list
        self.Initial_move = Initial_move
        self.Initial_positions = Initial_positions # use for read out only
        self.index = np.array(sweepDim) -1 # Initialize to expected final index            
    
    def write(self, fpath = ''):
        # Get information about instruments from config file
        measConfig = MeasConfig(filepath=self.configFile)
        measConfig.read()
        
        # safty check of the input parameters
        inst_name_list = [inst.strings[0] for inst in measConfig.list]
        initial_move_name_list = [s.decode('utf-8') for s in self.Initial_move['name']]
        sweep_name_list = []
        for sweep in self.sweeplist:
            if sweep.name in inst_name_list:
                sweep_name_list.append(sweep.name)
                inst = measConfig.list[inst_name_list.index(sweep.name)]
                safe = True
                # check upper and lower limit of the sweep array
                limits = inst.getLimits()
                if not limits == None:
                    safe = safe and (np.amax(sweep.array) <= limits[0])
                    safe = safe and (np.amin(sweep.array) >= limits[1])
                
                # check size of the array
                if not inst.kind == 9: # if it is not fast sequence
                    if not self.dim == list(sweep.array.shape):
                        print('check the dimension of the input arrays')
                        return 1
                # Escape program when the value exceeds the limit
                if not safe:
                    print('check the values of the array')
                    return 1
            else:
                # Escape when we find the instrument, which is not in the configure file.
                print('check the name of the sweep parameters')
                return 1
            
        # construct the path to save the file
        if fpath == '':
            fpath = self.saveFolder+self.filename+'.h5'
            
        # get the information about the sweep mode
        if measConfig.fastSweep == True:
            fast_sequence = measConfig.list[inst_name_list.index('fast_sequence')]
            fast_seq_data = fast_sequence.sequence
            if measConfig.ramp == True:
                # fast sequence size - 2 (trigger and jump) + start ramp at
                data_size = [fast_seq_data[1,:].shape[0]-2+fast_sequence.uint64s[20]]+self.dim
            else:
                data_size = [fast_sequence.uint64s[2]]+self.dim
        else:
            data_size = self.dim
        
        #---- creat readout (name, unit) list, set sweep and readout bools ------
        self.readoutlist = list()
        #If self.readout_inst_bools is empty, we fill up here to default values.
        if self.readout_inst_bools == list():
            fill_readout_bools = True
        else:
            fill_readout_bools = False
        #If self.sweep_inst_bools is empty, we fill up here to default values.
        if self.sweep_inst_bools == list():
            fill_sweep_bools = True
        else:
            fill_sweep_bools = False
        #unit list for the readout instruments
        unitList = []
        # counter to set sweep instrument bools
        sweep_inst_count = 0
        # update sweep parameters depending on the configure of the instrument
        sUnitList = {}
        for i, inst in enumerate(measConfig.list):
            # Treat readout instruments
            if inst.kind in readout_kind:
                # set readout inst bools if it was not given
                if fill_readout_bools:
                    #Default value is perform initialize but no post process.
                    self.readout_inst_bools.append([1, 0])
                # get readout name list and unit list
                info = inst.getNamesAndUnits()
                self.readoutlist += info[0]     # name list
                unitList += info[1]             # unit list
                
            # Treat sweep instruments
            if inst.kind in sweep_kind:
                # set sweep inst bools if it was not given
                if fill_sweep_bools:
                    bools = [0,0]
                    if inst.name in sweep_name_list:
                        # replace if it is defined as a sweep parameter.
                        bools = self.sweeplist[sweep_name_list.index(inst.name)].bools
                    self.sweep_inst_bools.append(bools)
                else:
                    if inst.name in sweep_name_list:
                        # replace if it is defined as a sweep parameter.
                        self.sweep_inst_bools[sweep_inst_count] = self.sweeplist[sweep_name_list.index(inst.name)].bools
                    sweep_inst_count += 1
                
                # set parameter and collect unit information
                parameter = inst.getParameter()
                if inst.kind == 10:
                    # special treatment for fast sequence slot
                    # convert slot number to fast channel number
                    parameter = fast_seq_data[0, parameter]
                
                if inst.name in sweep_name_list:
                    unit = inst.getUnit()
                    sUnitList.update({inst.name:unit})
                    sweep = self.sweeplist[sweep_name_list.index(inst.name)]
                    sweep.param = parameter
                    self.sweeplist[sweep_name_list.index(inst.name)] = sweep
                
                # set initial move
                if inst.name in initial_move_name_list:
                    index = initial_move_name_list.index(inst.name)
                    value = self.Initial_move[index]['value']
                    self.Initial_move[index]= np.array([(inst.name, parameter, value)],dtype=init_move_dt)
                        
        
        # Start creating the experiment file
        with h5py.File(fpath, 'w') as f:
            # Difine parameter list which store all the meta data necessary for experiment
            dset = f.get('Param_list')
            if dset==None:
                dset = f.create_dataset('Param_list', (1,),data=np.array((0), dtype='f'))
            dset.attrs['filename']=self.filename
            dset.attrs['saveFolder'] = self.saveFolder
            dset.attrs['configFilePath']=self.configFile
            dset.attrs.create('sweep_dim', np.array(self.dim, dtype=np.uint64), dtype='uint64')
            dset.attrs['comments']=self.comments
            dset.attrs.create('sweep_list', data=[i.name for i in self.sweeplist], dtype=flexible_str_dt)
            dset.attrs.create('readout_list', data=self.readoutlist, dtype=flexible_str_dt)
            dset.attrs.create('sweep_inst_bools', data=self.sweep_inst_bools, dtype='uint64')
            if self.readoutlist == list():
                self.readout_inst_bools = [[0,0]]
            dset.attrs.create('readout_inst_bools', data=self.readout_inst_bools, dtype='uint64')
            dset.attrs.create('Experimental_bool_list', data = self.Experimental_bool_list, dtype = 'bool')
            dset.attrs.create('sweep_index', np.array(self.index, dtype=np.uint64), dtype='uint64')
            # Create dataset to stor initial position information
            dset = f.get('Initial_move')
            if dset==None:
                dset = f.create_dataset('Initial_move', data=self.Initial_move, dtype=init_move_dt, chunks=True,compression='gzip',compression_opts=compression_level)
            else:
                dset[...] = self.Initial_positions
            # Create datasets to store the sweep information
            for i, item in enumerate(self.sweeplist):
                dset = f.get(item.name)
                if dset==None:
                    if compress_sweep:
                        dset = f.create_dataset(item.name, item.array.shape, data=item.array, dtype=item.dtype,chunks=True,compression='gzip',compression_opts=compression_level)
                    else:
                        dset = f.create_dataset(item.name, item.array.shape, data=item.array, dtype=item.dtype)
                dset.attrs.create('parameter', data=item.param)
                dset.attrs['unit'] = sUnitList[item.name]
                dset.attrs['creationMethod'] = item.creationMethod
                dset.attrs.create('dimension', data = item.sweep_dim)
            
            # Create the group to save the data
            grp = f.get('data')
            if grp == None:
                grp = f.create_group('data')
            for i, item in enumerate(self.readoutlist):
                dset = grp.get(item)
                if dset == None:
                    if compress_data:
                        dset = grp.create_dataset(item,shape=data_size,dtype='float',chunks = True,compression='gzip',compression_opts=compression_level)
                    else:
                        dset = grp.create_dataset(item,shape=data_size,dtype='float')
#                dset.attrs.create('unit', data=unitList[i])
                dset.attrs['unit']=unitList[i]
            
        # Save some of the config information also into the experiment file for analysis
        if save_config2ExpFile:
            measConfig = MeasConfig() # define configure class
            measConfig.fpath = self.configFile # set the file path to read
            measConfig.readForExpFile() # get the information
            measConfig.fpath = fpath # replace the path to save the information
            measConfig.write(group='configure')
            
        return 0 # safely finish excecution
            
    def read(self):
        if ((self.saveFolder=='') or (self.filename=='')):
            if not (self.saveFolder==''):
                fpath = QtWidgets.QFileDialog.getOpenFileName(caption='Choose exp file to read', filter='*.h5', directory=os.path.dirname(self.saveFolder))
            else:
                fpath = QtWidgets.QFileDialog.getOpenFileName(caption='Choose exp file to read', filter='*.h5')
            fpath = fpath[0]
        else:
            fpath = self.saveFolder+self.filename+'.h5'
#            fpath = self.saveFolder+QtCore.QDir.separator()+self.filename+'.h5'
        # for windows
        fpath = fpath.replace('\\','\\\\')
        if not fpath == '':
            with h5py.File(fpath, 'r') as f:
                dset = f['Param_list']
                self.filename = dset.attrs['filename']
                self.saveFolder = dset.attrs['saveFolder']
                self.configFile = dset.attrs['configFilePath']
                self.comments = dset.attrs['comments']
                self.dim = dset.attrs['sweep_dim']
                self.readoutlist = [str(s, 'utf-8') for s in dset.attrs['readout_list']]
                self.readout_inst_bools = dset.attrs['readout_inst_bools']
                self.sweep_inst_bools = dset.attrs['sweep_inst_bools']
                self.Experimental_bool_list = dset.attrs['Experimental_bool_list']
                self.index = dset.attrs['sweep_index']
                self.sweeplist = [single_sweep(name=str(i, 'utf-8')) for i in dset.attrs['sweep_list']]
                for i, item in enumerate(self.sweeplist):
                    dset = f[item.name]
                    try: # try to load creation method
                        creationMethod = dset.attrs['creationMethod'],    # something other than 'None' appears if the file was created by UI
                        creationMethod = creationMethod[0]
                    except: # if it is not exist, just set as linear.
                        creationMethod = 'Linear'
                        
                    try:
                        self.sweeplist[i] = single_sweep(name = item.name,
                                                         parameter = dset.attrs['parameter'],
                                                         Initialize = self.sweep_inst_bools[i][0], #0: False, else: True
                                                         PostProcess = self.sweep_inst_bools[i][0], #0: False, else: True
                                                         ar = np.array((dset),dtype=np.float64),
                                                         dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
                                                         creationMethod = creationMethod,    # something other than 'None' appears if the file was created by UI
                                                         sweep_dim = dset.attrs['dimension'],   # sweep dimension: it becomes other than 0 if it is created by square sweep UI
                                                         )
                    except:
                        self.sweeplist[i] = single_sweep(name = item.name,
                                                         parameter = dset.attrs['parameter'],
                                                         Initialize = self.sweep_inst_bools[i][0], #0: False, else: True
                                                         PostProcess = self.sweep_inst_bools[i][0], #0: False, else: True
                                                         ar = np.array((dset),dtype=h5py.special_dtype(vlen=bytes)),
                                                         dataType = h5py.special_dtype(vlen=bytes), # for CMD use dt=h5py.special_dtype(vlen=bytes)
                                                         creationMethod = creationMethod,    # something other than 'None' appears if the file was created by UI
                                                         sweep_dim = dset.attrs['dimension'],   # sweep dimension: it becomes other than 0 if it is created by square sweep UI
                                                         )
                self.Initial_move = np.array((f['Initial_move']),dtype=init_move_dt)
                try:
                    self.Initial_positions = np.array((f['Initial_positions']),dtype=init_position_dt)
                except:
                    pass
  

class single_sweep():
    """-------------------------------------------------------------------------
    ----------------------------------------------------------------------------
    class to define sweep data information for a single sweep instrument
    ----------------------------------------------------------------------------
    ----------------------------------------------------------------------------"""
    def __init__(self,
                 name = '',
                 parameter = 0,
                 Initialize = 0, #0: False, else: True
                 PostProcess = 0, #0: False, else: True
                 ar = np.zeros((100,),dtype=float),
                 dataType = 'float', # for CMD use dt=h5py.special_dtype(vlen=bytes)
                 creationMethod = 'None',
                 sweep_dim = 0, # sweep dimension 0: array sweep, 1: sweep along 1st dim, 2: sweep along 2nd dim, ....
                 ):
        self.name = name
        self.param = parameter
        self.array = ar
        self.bools = [Initialize, PostProcess]
        self.dtype = dataType
        self.creationMethod = creationMethod
        self.sweep_dim = sweep_dim

class MeasConfig():
    """-------------------------------------------------------------------------
    ----------------------------------------------------------------------------
    class to create measurement configuration file
    ----------------------------------------------------------------------------
    ----------------------------------------------------------------------------"""
    def __init__(self,
                 filepath='',
                 initial_wait = 100,
                 wait_before_meas = 1,
                 integration_time = 10,
                 wait_after_step_move = 1,
                 fastSweep = False,
                 ramp = False,
                 listOfInst = [],
                 fastChannelNameList=[],
                 ):
        self.fpath = filepath
        self.initial_wait = initial_wait
        self.wait_before_meas = wait_before_meas # not used in fast sequence
        self.integration_time = integration_time
        self.wait_after_step_move = wait_after_step_move
        self.fastSweep = fastSweep
        self.ramp = ramp
        self.list = listOfInst
        self.fastChannelNameList = fastChannelNameList
        
    def write(self, group=None):
        if group==None: 
            with h5py.File(self.fpath, 'w') as f:
                dset = f.get('Meas_config')
                if dset==None:
                    dset = f.create_dataset('Meas_config', (1,),data=np.array((0), dtype='f'))
                u = np.array((self.initial_wait, self.wait_before_meas, self.integration_time, self.wait_after_step_move), dtype=np.uint64)
                dset.attrs.create('wait_times', u, dtype='uint64')
                b = np.array((self.fastSweep, self.ramp), dtype=np.bool_)
                dset.attrs.create('fast_mode', b, dtype='bool')
                s = [i.name for i in self.list]
                dset.attrs.create('Inst_list', s, dtype=flexible_str_dt)
                if not self.fastChannelNameList == []:
                    dset.attrs.create('Fast_channel_name_list', self.fastChannelNameList, dtype=flexible_str_dt)
#                dset = f.get('Inst_list')
    
            for inst in self.list:
                if inst.kind == 9:
                    inst.writeSequence(self.fpath)
                else:
                    inst.write(self.fpath)
        else:
            with h5py.File(self.fpath, 'a') as f:
                grp = f.get(group)
                if grp == None:
                    grp = f.create_group(group)
                dset = grp.get('Meas_config')
                if dset==None:
                    dset = grp.create_dataset('Meas_config', (1,),data=np.array((0), dtype='f'))
                u = np.array((self.initial_wait, self.wait_before_meas, self.integration_time, self.wait_after_step_move), dtype=np.uint64)
                dset.attrs.create('wait_times', u, dtype='uint64')
                b = np.array((self.fastSweep, self.ramp), dtype=np.bool_)
                dset.attrs.create('fast_mode', b, dtype='bool')
                s = [i.name for i in self.list]
                dset.attrs.create('Inst_list', s, dtype=flexible_str_dt)
                if not self.fastChannelNameList == []:
                    dset.attrs.create('Fast_channel_name_list', self.fastChannelNameList, dtype=flexible_str_dt)
#                dset = f.get('Inst_list')
    
            for inst in self.list:
                if inst.kind == 9:
                    inst.writeSequence(self.fpath, group=group)
                else:
                    inst.write(self.fpath, group=group)
            
    def read(self,group=None):
        with h5py.File(self.fpath, 'r') as f:
            if group==None:
                dset = f.get('Meas_config')
            else:
                grp = f.get(group)
                dset = grp.get('Meas_config')
            u = dset.attrs['wait_times']
            self.initial_wait = u[0]
            self.wait_before_meas = u[1]
            self.integration_time = u[2]
            self.wait_after_step_move = u[3]
            b = dset.attrs['fast_mode']
            self.fastSweep = b[0]
            self.ramp = b[1]
            self.list = []
            inst_name_list = [str(s, 'utf-8') for s in dset.attrs['Inst_list']]
            fastChannelNameList = ['']*64
            for i in inst_name_list:
                if group == None:
                    dset = f.get(i)
                else:
                    grp = f.get(group)
                    dset = grp.get[i]
                kind = dset.attrs['Kind']
                u = dset.attrs['uint64s']
                d = dset.attrs['Doubles']
                if d.shape == ():
                    d = [d]
                s = [str(s, 'utf-8') for s in dset.attrs['Strings']]
                
                item = eval(classList[kind]+'()')
                item.kind = kind
                item.name = s[0]
                item.strings = s
                item.uint64s = u
                item.doubles = d
                if kind == 4:
                    # just collect information for fast sequence operation
                    fastChannelNameList[int(8*u[0]+u[1])]=s[0]
                elif kind == 9:   # readout data for fast sequence
                    item.sequence = dset[...]
                self.list.append(item)
            self.fastChannelNameList = fastChannelNameList
                
                
    def readForExpFile(self,group=None):
        """
        Read only an important information for experiment file
        also add the correspondence between fast channels and name (if defined)
        """
        with h5py.File(self.fpath, 'r') as f:
            if group==None:
                dset = f.get('Meas_config')
            else:
                grp = f.get(group)
                dset = grp.get('Meas_config')
            u = dset.attrs['wait_times']
            self.initial_wait = u[0]
            self.wait_before_meas = u[1]
            self.integration_time = u[2]
            self.wait_after_step_move = u[3]
            b = dset.attrs['fast_mode']
            self.fastSweep = b[0]
            self.ramp = b[1]
            self.list = []
            inst_name_list = [str(s, 'utf-8') for s in dset.attrs['Inst_list']]
            fastChannelNameList = ['']*64
            for i in inst_name_list:
                if group == None:
                    dset = f.get(i)
                else:
                    grp = f.get(group)
                    dset = grp.get[i]
                kind = dset.attrs['Kind']
                u = dset.attrs['uint64s']
                d = dset.attrs['Doubles']
                if d.shape == ():
                    d = [d]
                s = [str(s, 'utf-8') for s in dset.attrs['Strings']]
                
                if readConfigForExpFile[kind]:
                    item = eval(classList[kind]+'()')
                    item.kind = kind
                    item.name = s[0]
                    item.strings = s
                    item.uint64s = u
                    item.doubles = d
                    if kind == 9:   # readout data for fast sequence
                        item.sequence = dset[...]
                    self.list.append(item)
                else:
                    pass
                
                if kind == 4:
                    # just collect information for fast sequence operation
                    fastChannelNameList[int(8*u[0]+u[1])]=s[0]
            self.fastChannelNameList = fastChannelNameList

"""-------------------------------------------------------------------------
----------------------------------------------------------------------------
class to define readout instruments
----------------------------------------------------------------------------
----------------------------------------------------------------------------"""
class readout_inst(object):
    """
    base class for readout instrument
    """
    def __init__(self,
                 kind = 100,
                 name = '',
                 ):
        self.kind = kind    # type of instrument
        self.name = name    # user defined name of each instrument
        self.strings = []   # list of string to save into configuration file
        self.uint64s = []   # list of unsigned 64 bit integer to save into configuration file
        self.doubles = []   # list of doubles to save into configuration file
        
    def write(self,
              h5path,       # path to HDF5 file to save into
              group=None    # group in the HDF5 file to save into
              ):
        with h5py.File(h5path, 'r+') as f:
            if group == None:               # check whether group is given or not
                dset = f.get(self.name)     # check whether already an instrument with same name is defined or not
                if dset==None:              # If the instrument with 'name' is not defined, create it.
                    dset = f.create_dataset(self.name, (1,),data=np.array((0), dtype='f'))
            else:
                grp = f.get(group)
                dset = grp.get(self.name)
                if dset == None:
                    dset = grp.create_dataset(self.name, (1,),data=np.array((0), dtype='f'))
            # save kind
            dset.attrs.create('Kind', self.kind, dtype='uint16')
            # save strings
            s = np.array(self.strings, dtype=flexible_str_dt)
            dset.attrs.create('Strings', s, dtype=flexible_str_dt)
            # save unsined integer 64 bit
            u = np.array(self.uint64s, dtype=np.uint64)
            dset.attrs.create('uint64s', u, dtype='uint64')
            # save doubles
            d = np.array(self.doubles, dtype=np.double)
            dset.attrs.create('Doubles', d, dtype='f')
            
    def getNamesAndUnits(self):
        pass
    
# class for ADC
class ADC(readout_inst):
    def __init__(self,
                 name='ADC',
                 unit='V',
                 Range={'+/-0.2V':0, '+/-1V':1, '+/-5V':5, '+/-10V':10}['+/-10V'],
                 NameList='ADC0;ADC1',
                 UnitList='V;V',
                 ConversionList='1.0;1.0',
                 NofChannels=2,
                 samplingRate=250000,
                 Realtime=0,
                 RTaverage=100,
                 InpConfig={'default':-1,'RSE':10083,'NRSE':10078,'Differential':10106,'Pseudodifferential':12529}['Differential'],
                 BufferSize=1000000,
                 SamplePerChannel=1,
                 ramp_trigger_input = 0,
                 fast_seq_trigger_input = 1,
                 conversion=1.0):
        super(ADC, self).__init__()
        self.kind = 0
        self.name = name
        self.strings = [name, '', unit, NameList, UnitList, ConversionList]
        self.uint64s = [Range, NofChannels, samplingRate, Realtime, RTaverage, InpConfig]
        self.uint64s+= [BufferSize, SamplePerChannel, ramp_trigger_input, fast_seq_trigger_input]
        self.doubles = [conversion]
        
    def getNamesAndUnits(self):
        return [self.strings[3].split(';'), self.strings[4].split(';')] # return [list of names, list of units]
        
# class for Keythley 2000    
class K2000(readout_inst):
    def __init__(self,
                 name='I',
                 GPIB_address = addressList['K2000'],
                 unit = 'nA',
                 Range = [0,1,2,3,4][2],# 0: 1000 V, 1: 100 V, 2: 10 V, 3: 1V, 4: 0.1 V
                 Digits = [0,1,2,3][3],# 0: 4 digits, 1: 5, 2: 6, 3: 7
                 NPLC = [0,1,2][1],# 0: 10, 1: 1, 2: 0.1
                 NPLC_fast = [0,1,2][1],# 0: 10, 1: 1, 2: 0.1
                 average = 1,
                 conversion_factor = 1.0
                 ):
        super(K2000, self).__init__()
        self.kind = 1
        self.name = name
        self.strings = [name, GPIB_address, unit]
        self.uint64s = [Range, Digits, NPLC, NPLC_fast, average]
        self.doubles = [conversion_factor]
        
    def getNamesAndUnits(self):
        return [[self.strings[0]],[self.strings[2]]]
            
# class for K34401A
class K34401A(readout_inst):
    def __init__(self,
                 name='V',
                 GPIB_address = addressList['K34401A'],
                 unit = 'mV',
                 Function = [0,1,2,3,4,5,6,7,8,9,10,11,12][0],
#                0: DC Voltage 1: AC Voltage 2: 2 - Wire Resistance 3: 4 - Wire Resistance 4: DC Current 5: AC Current,...
                 average = 1,
                 conversion_factor = 1.0,
                 Range = [10.0, 1.0 , 0.1][0], #else: autoRange
                 Digits = [5.5, 6.5][1] #else: 5.5
                 ):
        super(K34401A, self).__init__()
        self.kind = 2
        self.name = name
        self.strings = [name, GPIB_address, unit]
        self.uint64s = [Function, average]
        self.doubles = [conversion_factor, Range, Digits]
        
    def getNamesAndUnits(self):
        return [[self.strings[0]], [self.strings[2]]]
		
# class for 3458
class A3458(readout_inst):
    def __init__(self,
                 name='V',
                 GPIB_address = addressList['A3458'],
                 unit = 'mV',
                 Function = [0,1,2,3,4,5,6,7,8,9,10,11,12][0],
#                0: DC Voltage 1: AC Voltage 2: 2 - Wire Resistance 3: 4 - Wire Resistance 4: DC Current 5: AC Current,...
                 average = 1,
                 AutoRange = 1,
                 FrequSource = 3,
                 TrigType = 0,
                 conversion_factor = 1.0,
                 Range = [10.0, 1.0 , 0.1][0], #else: autoRange
                 Digits = 4 #else: 8.5
                 ):
        super(A3458, self).__init__()
        self.kind = 3
        self.name = name
        self.strings = [name, GPIB_address, unit]
        self.uint64s = [Function, average, AutoRange, Digits, FrequSource, TrigType]
        self.doubles = [conversion_factor, Range]
        
    def getNamesAndUnits(self):
        return [[self.strings[0]], [self.strings[2]]]
        
# class for DSP lock-in amplifier as a readout instrument            
class DSP_lockIn(readout_inst):
    def __init__(self,
                 name = 'Lock-in',
                 GPIBAddress=addressList['DSP_lockIn'],
                 unit = 'V',
                 nameList = [], # list of names ex.) ['X','Y','Sensitivity']
                 unitList = [], # list of units ex.) ['V','V','a.u']
                 RTaverageTime = 5, # interval to take data in fast cycle mode in ms.
                 parameterToRead = 19, #bit wise parameter to be read see parameter_note in detail
                 coupling = 0, #[0: AC and float, 1: DC and float, 2: AC and GND, 3: DC and GND]
                 inputMode = 0, #[0: V and A, 1: V and -B, 2: V and A-B, 3: I and wide band, 4: I and Low noise (default 0)]
                 FETorBipolar = 0, # voltage mode input device control, see parameter_note in detail
                 lineFilter = 0, #[Line filter: 0: off, 1: 50 Hz, 2: 100 Hz, 3: both]
                 autoACgain = 0, #[0: off, 1: on]
                 acGain = 0, # [0 ~ 9 --> 0 dB ~ 90 dB in 10 dB step]
                 sensitivity = 27, # see parameter_note
                 timeConstant = 12, # see parameter_note
                 refChannel = 2, # 0: internal, 1: External logic (external rear panel TTL input) 2: External (external front panel input)
                 parameterToGetInitialValue = 2,
                 conversion = 1.0,
                 oscillatorAmp = 0.1, # [V]
                 oscillatorFreq = 37.7, # (Hz)
                 ampulimit = 1.0, # [V]
                 ampllimit = 0.0, # (V)
                 frequlimit = 1000, # (Hz)
                 freqllimit = 0.01, # (Hz)
                 ):
        super(DSP_lockIn, self).__init__()
        self.kind = 12
        self.name = name
        
        if nameList == [] or unitList== []:
            listEmpty = True
            nameList = []
            unitList = []
            nameList1 = ['X','Y','Mag','Phase','Sensitivity','ADC1','ADC2','ADC3','DAC1','DAC2','Noise','Ratio','Log ratio','EVENT variable','Ref freq bits 0 to 15','Ref freq bits 16 to 32']
            unitList1 = ['V','V','V','degree','a.u.','V','V','V','V','V','V','V','log(v)','a.u.','mHz','mHz']
            
        no_readouts = 0
        for i in range(16):
            if (parameterToRead & 2**i) != 0:
                no_readouts +=1
                if listEmpty:
                    nameList.append(nameList1[i])
                    unitList.append(unitList1[i])
                    
        self.strings = [name, GPIBAddress, unit, ';'.join(nameList), ';'.join(unitList)]
        self.uint64s = [RTaverageTime, parameterToRead, no_readouts, coupling, inputMode, FETorBipolar]
        self.uint64s+= [lineFilter, autoACgain, acGain, sensitivity, timeConstant, refChannel]
        self.uint64s+= [parameterToGetInitialValue]
        self.doubles = [conversion, oscillatorAmp, oscillatorFreq, ampulimit, ampllimit, frequlimit, freqllimit]
        
    def getNamesAndUnits(self):
        return [self.strings[3].split(';'), self.strings[4].split(';')]

"""-------------------------------------------------------------------------
----------------------------------------------------------------------------
class to define sweep instruments
----------------------------------------------------------------------------
----------------------------------------------------------------------------"""
class sweep_inst(object):
    """
    base class for sweep instrument
    """
    def __init__(self,
                 kind = 100,
                 name = '',
                 ):
        self.kind = kind    # type of instrument
        self.name = name    # user defined name of each instrument
        self.strings = []   # list of string to save into configuration file
        self.uint64s = []   # list of unsigned 64 bit integer to save into configuration file
        self.doubles = []   # list of doubles to save into configuration file
        
    def write(self,
              h5path,       # path to HDF5 file to save into
              group=None    # group in the HDF5 file to save into
              ):
        with h5py.File(h5path, 'r+') as f:
            if group == None:               # check whether group is given or not
                dset = f.get(self.name)     # check whether already an instrument with same name is defined or not
                if dset==None:              # If the instrument with 'name' is not defined, create it.
                    dset = f.create_dataset(self.name, (1,),data=np.array((0), dtype='f'))
            else:
                grp = f.get(group)
                dset = grp.get(self.name)
                if dset == None:
                    dset = grp.create_dataset(self.name, (1,),data=np.array((0), dtype='f'))
            # save kind
            dset.attrs.create('Kind', self.kind, dtype='uint16')
            # save strings
            s = np.array(self.strings, dtype=flexible_str_dt)
            dset.attrs.create('Strings', s, dtype=flexible_str_dt)
            # save unsined integer 64 bit
            u = np.array(self.uint64s, dtype=np.uint64)
            dset.attrs.create('uint64s', u, dtype='uint64')
            # save doubles
            d = np.array(self.doubles, dtype=np.double)
            dset.attrs.create('Doubles', d, dtype='f')
            
    def getLimits(self):
        return None
    
    def getParameter(self):
        pass
    
    def getUnit(self):
        pass
    
class DAC(sweep_inst):
    def __init__(self,
                 name = '0:0',
                 IPAddress = FPGA_address,
                 unit = 'V',
                 panel = 0,
                 channel = 0,
                 upper_limit = 0.3,
                 lower_limit = -2.0,
                 ms2wait = 2,# ms to wai between each bit (~ 150 uV)
                 conversion = 1.0,# only for analysis
                 ):
        super(DAC,self).__init__()
        self.kind = 4
        self.name = name
        self.strings = [name, IPAddress, unit]
        self.uint64s = [panel, channel]
        self.doubles = [upper_limit, lower_limit, ms2wait, -1, conversion]
        
    def getLimits(self):
        return [self.doubles[0],self.doubles[1]]
    
    def getParameter(self):
        return 0
    
    def getUnit(self):
        return self.strings[2]

class DAC_Lock_in(sweep_inst):
    def __init__(self,
                 name = 'DAC_Lock-in',
                 IPAddress = FPGA_address,
                 unit = 'V',
                 panel = 0,
                 channel = 1,
                 use = 1,
                 upper_limit = 1.0,
                 lower_limit = 0.0,
                 freq = 50,
                 amp = 0.1,
                 control_parameter = 0 # [0: panel*8 + channel, 1: Frequency (Hz), 2: Amplitude (Vpp)]
                 ):
        super(DAC_Lock_in, self).__init__()
        self.kind = 5
        self.name = name
        self.strings = [name, IPAddress, unit]
        self.uint64s = [panel, channel, use, control_parameter]
        self.doubles = [upper_limit, lower_limit, -1, -1, freq, amp]
        
    def getLimits(self):
        if self.uint64s[3]==0:
            return [0, 63]
        elif self.uint64s[3]==1:
            return None
        else:
            return [self.doubles[0], self.doubles[1]]
        
    def getParameter(self):
        return 0
    
    def getUnit(self):
        return self.strings[2]

class RS_RF(sweep_inst):
    def __init__(self,
                 name='RF',
                 GPIBAddress=addressList['RS_RF'],
                 Unit='GHz',
                 frequency=2, # GHz
                 power=-30, # dBm
                 pulse_period = 200, #us
                 pulse_width = 100, #us
                 pulse_delay = 0, #us
                 pulse_modulation = 1, # boolean
                 output_on = 1, # boolean
                 pulse_source = 1, # boolean, 0: internal, 1: external
                 pulse_mode = 0, # 0: single, 1: double, 2: train
                 trigger_mode = 2, # 0: auto, 1: external, 2: external gate, 3: single  
                 ex_trigger_input_slope = 0, # boolean, 0: negative, else: positive
                 external_impedance = 0, # 0: 10 kohm, else: 50 ohm
                 frequency_ul=6.001, # GHz upper limit
                 frequency_ll=9e-6, # GHz lower limit
                 power_ul=30, # dBm upper limit
                 power_ll=-145, # dBm lower limit
                 controlParam = 0, # selection of control parameter, which is used to get the initial value of the parameter
                 ):
        super(RS_RF, self).__init__()
        self.kind = 6
        self.name = name
        self.strings = [name, GPIBAddress, Unit]
        self.uint64s = [pulse_modulation, output_on, pulse_source, pulse_mode, trigger_mode]
        self.uint64s+= [ex_trigger_input_slope, external_impedance, controlParam]
        self.doubles = [frequency, power, pulse_period, pulse_width, pulse_delay]
        self.doubles+= [frequency_ul, frequency_ll, power_ul, power_ll]
        
    def getLimits(self):
        if self.uint64s[7]==0:
            return [self.doubles[5], self.doubles[6]]
        elif self.uint64s[7]==1:
            return [self.doubles[7], self.doubles[8]]
        else:
            return None
        
    def getParameter(self):
        return self.uint64s[7]
    
    def getUnit(self):
        return self.strings[2]
  
class AWG(sweep_inst):
    def __init__(self,
                 name = 'AWG',
                 IPAddress = addressList['AWG'],
                 port = 4000,
                 Unit = '',
                 functionFolderPath = 'C:\Documents and Settings\Bauerle\Mes documents\Bautze\FPGA-clean_works_1.13.6_batchtest\Python\AWG', #Path to the folder containing your fuction
                 InitialFunctionFileName='SAWnstrig_v4.py', # In case you would like to perform one function at the begging, please use it.
                 noCh = 4, # Number of channels to be used
                 run = 0, # Run? 0: off, else: run
                 run_mode = 3, # [0: continuous, 1: Triggered, 2: Gated, 3: Sequence]
                 sampling_freq = 1.2, # GHz
                 control_parameter = 0,
                 chOutput = [0,0,0,0],
                 chAmplitude = [1.0,1.0,1.0,1.0],
                 chOffset = [0.0,0.0,0.0,0.0],
                 Mk1High = [1.0,1.0,1.0,1.0],
                 Mk1Low = [0.0,0.0,0.0,0.0],
                 Mk1Delay = [0,0,0,0],
                 Mk2High = [1.0,1.0,1.0,1.0],
                 Mk2Low = [0.0,0.0,0.0,0.0],
                 Mk2Delay = [0,0,0,0],
                 chSkew = [0,0,0,0],
                 ):
       super(AWG, self).__init__()
       self.kind = 7
       self.name = name
       self.strings = [name, IPAddress, Unit, functionFolderPath, 'dummy', InitialFunctionFileName]
       self.uint64s = [noCh, 0, run, run_mode, control_parameter, 0]
       for i in range(noCh):
           self.uint64s += [chOutput[i], Mk1Delay[i], Mk2Delay[i], chSkew[i]]
       if len(self.uint64s) < 22: # in case channel number is less than 4, fill up with 0 to implement port number.
           self.uint64s += [0]*(22-len(self.uint64s))
       self.uint64s += [port]
       self.doubles = [sampling_freq]
       for i in range(noCh):
           self.doubles += [chAmplitude[i], chOffset[i], Mk1High[i], Mk1Low[i], Mk2High[i], Mk2Low[i]]
       
    def getLimits(self):
        return None
    
    def getParameter(self):
        return self.uint64s[4]
    
    def getUnit(self):
        return self.strings[2]

class FastSequences(sweep_inst):
    def __init__(self,
                 IPAddress = FPGA_address,
                 Unit = 'V',
                 fastSequenceDivider = 44439, #averaging time for ramp mode
                 triggerLength = 300, # Trigger length for ramp mode
                 SampleCount = 200, # Number of points for fast sequence mode
                 send_all_points = 0,
                 fast_channels = [0,1,2,3,4,5,6,7,16,17,18,19,20,21,22,23],
                 start_ramp_at = 0,
                 upper_limit = 0.5,
                 lower_limit = -0.5,
                 sequence = np.zeros((2,10))
                 ):
        super(FastSequences, self).__init__()
        self.kind = 9
        self.name = 'fast_sequence'
        self.strings = ['fast_sequence', IPAddress, Unit]
        self.uint64s = [fastSequenceDivider, triggerLength, SampleCount, send_all_points]
        for i in fast_channels:
            self.uint64s.append(i)
        self.uint64s.append(start_ramp_at)
        self.doubles = [upper_limit, lower_limit, -1, -1]
        
        self.sequence = sequence
        
    def writeSequence(self, h5path, group=None):
        with h5py.File(h5path, 'r+') as f:
            #check the limitation of the sequence
            dacRange = np.logical_and(self.sequence[0,:]>-1, self.sequence[0,:]<16)
            if np.any(dacRange):
                if (self.doubles[0] < np.amax(self.sequence[1,dacRange]) or self.doubles[1] > np.amin(self.sequence[1,dacRange])):
                    print('check the values of fast sequence')
                    return 1
                    
            if self.sequence[1,:].shape[0]>4096:
                print('check the size of fast sequence')
                return 1
            # create dataset and attach all the meta information
            if group == None:
                dset = f.get(self.name)
                if dset==None:
                    if compress_data:
                        dset = f.create_dataset(self.name, shape=self.sequence.shape, data=self.sequence, dtype='float',chunks = True,compression='gzip',compression_opts=compression_level)
                    else:
                        dset = f.create_dataset(self.name, shape=self.sequence.shape, data=self.sequence, dtype='float')
            else:
                grp = f.get(group)
                dset = grp.get(self.name)
                if dset == None:
                    if compress_data:
                        dset = grp.create_dataset(self.name, shape=self.sequence.shape, data=self.sequence, dtype='float',chunks = True,compression='gzip',compression_opts=compression_level)
                    else:
                        dset = grp.create_dataset(self.name, shape=self.sequence.shape, data=self.sequence, dtype='float')
            # standard writing function below
            if group == None:               # check whether group is given or not
                dset = f.get(self.name)     # check whether already an instrument with same name is defined or not
                if dset==None:              # If the instrument with 'name' is not defined, create it.
                    dset = f.create_dataset(self.name, (1,),data=np.array((0), dtype='f'))
            else:
                grp = f.get(group)
                dset = grp.get(self.name)
                if dset == None:
                    dset = grp.create_dataset(self.name, (1,),data=np.array((0), dtype='f'))
            # save kind
            dset.attrs.create('Kind', self.kind, dtype='uint16')
            # save strings
            s = np.array(self.strings, dtype=flexible_str_dt)
            dset.attrs.create('Strings', s, dtype=flexible_str_dt)
            # save unsined integer 64 bit
            u = np.array(self.uint64s, dtype=np.uint64)
            dset.attrs.create('uint64s', u, dtype='uint64')
            # save doubles
            d = np.array(self.doubles, dtype=np.double)
            dset.attrs.create('Doubles', d, dtype='f')

class FastSequenceSlot(sweep_inst):
    def __init__(self,
                 name='slot',
                 IPAddress=FPGA_address,
                 unit='V',
                 slotNo=0,
                 upperlimit=0.5,
                 lowerlimit=-0.5
                 ):
        super(FastSequenceSlot, self).__init__()
        self.kind = 10
        self.name = name
        self.strings = [name, IPAddress, unit]
        self.uint64s = [slotNo, 0]
        self.doubles = [upperlimit, lowerlimit]
        
    def getLimits(self):
        return [self.doubles[0], self.doubles[1]]
    
    def getParameter(self):
        return self.uint64s[0]
    
    def getUnit(self):
        return self.strings[2]

class CMD(sweep_inst):# Used for sending command line arguments, data should be string rather than double precision floating point.
    def __init__(self,
                 name = 'cmd',
                 workDir = '',
                 wait_execution = 1, # 0: not wait, else: wait
                 ):
        super(CMD, self).__init__()
        self.kind = 11
        self.name = name
        self.strings = [name, workDir]
        self.uint64s = [wait_execution, 0]
        self.doubles = [0.0,0.0]
        
    def getLimits(self):
        return None
    
    def getParameter(self):
        return 0
    
    def getUnit(self):
        return 'a.u.'
            
class DSP_lockIn_sweep(sweep_inst):
    def __init__(self,
                 name='DSP7265',
                 address = '0:12',
                 unit = 'V',
                 parameter = 12,
                 ulimit = 1.0,
                 llimit = 0.0,
                 conversion = 1.0,
                 ):
        """
        [List of parameters to control]
        0:	Singnal channel coupling
        1:	Signal channel input mode
        2:	Signal channel FET or Bipolar
        3:	Signal channel line filter
        4:	Auto ac gain
        5:	AC gain
        6:	Sensitivity
        7:	Auto sensitivity
        8:	Auto phase
        9:	Auto sensitivity & phase
        10:	Time constant
        11:	Reference channel source
        12:	Oscillator amplitude
        13:	Oscillator frequency
        14:	Parameter to be read
        """
        super(DSP_lockIn_sweep, self).__init__()
        self.kind = 13
        self.name = name
        self.strings = [name, address, unit]
        self.uint64s = [parameter, 0]
        self.doubles = [ulimit, llimit, conversion]
        
    def getLimits(self):
        return [self.doubles[0], self.doubles[1]]
    
    def getParameter(self):
        return self.uint64s[0]
    
    def getUnit(self):
        return self.strings[2]
            
class mswait(sweep_inst):   # kind = 14
    def __init__(self,
                 name='wait',
                 unit = 'ms',
                 ulimit = 100000,
                 llimit = 0,
                 ):
        super(mswait, self).__init__()
        self.kind = 14
        self.name = name
        self.strings = [name, unit]
        self.uint64s = [0,0]
        self.doubles = [ulimit, llimit]
        
    def getLimits(self):
        return [self.doubles[0], self.doubles[1]]
    
    def getParameter(self):
        return 0
    
    def getUnit(self):
        return self.strings[1]
    
class ATMDelayLine(sweep_inst):   # kind = 15
    def __init__(self,
                 name='Delay',
                 address = addressList['ATMDelayLine'],
                 unit = 'ps',
                 baudRate = 9600,
                 EchoMode = 2,
                 Acceleration = 10000,
                 Deceleration = 10000,
                 VelocityInit = 100000,
                 VelocityMax = 100000,
                 ulimit = 259.3,
                 llimit = 0,
                 ):
        super(ATMDelayLine, self).__init__()
        self.kind = 15
        self.name = name
        self.strings = [name, address, unit]
        self.uint64s = [baudRate, EchoMode, Acceleration, Deceleration, VelocityInit, VelocityMax]
        self.doubles = [ulimit, llimit]
        
    def getLimits(self):
        return [self.doubles[0], self.doubles[1]]
    
    def getParameter(self):
        return 0
    
    def getUnit(self):
        return self.strings[2]


class RF_Attn(sweep_inst):
    def __init__(self,
                 name='RF_Attn',
                 USBAddress=addressList['RF_Attn'],
                 Unit='dB',
                 attn = 10,
                 attn_ul=63, # dB upper limit
                 attn_ll=5.5, # dB lower limit
                 insertion_loss=5.5, # dB insertion loss
                 ):
        super(RF_Attn, self).__init__()
        self.kind = 16
        self.name = name
        self.strings = [name, USBAddress, Unit]
        self.uint64s = []
        self.doubles = [attn, attn_ul, attn_ll, insertion_loss]
        
    def getLimits(self):
        return [self.doubles[1], self.doubles[2]]
    
    def getUnit(self):
        return self.strings[2]

    def getParameter(self):
        return 0


if __name__=='__main__':
    pass