#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:16:32 2017

@author: shintaro
"""

import sys, os, glob
sys.path.insert(0,'..') # import parent directory
import h5py
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore

init_pos_dt = np.dtype({'names':['Name','kind','Value'],'formats':['S100','u8','f8']})
pathSeparator = QtCore.QDir.separator()
gdsname = 'HBT6'

class spec():
    """
    Class for data import 
    reads txt files with only 2 columns: x position and height

    Parameters
    ----------
    input: 
        filename and path,... parameters see __init__
        
    output : 
        Class to view the config, plot, work with Data
    """

    def __init__(self,
                 fname = '',
                  path = '',
                 comments = '',
                 sweepDims = [],
                 sweepIndex = [],
                 readoutnamelist = [],
                 sweepnamelist = [],
                 InitialPositions = [],
                 mode = 0, # 0: Normal, 1: fast ramp, 2: fast cycle
                 fastSeq = {'seq': np.zeros((1,1)), 'name': 'fast sequences',
                 'start ramp at':0, 'channels':[i for i in np.arange(16)],
                 'divider': 6661, 'count': 0},
                 ):
        
        if not (fname.endswith('.h5') or fname.endswith('.txt') or fname.endswith('.dat') or fname.endswith('.csv') or fname.endswith('.sp2')):
            raise ValueError( 'Can only create a spec class object from hdf5, txt,csv, dat or s2p file; fname=%s' % fname )
        self.fname = fname
        self.path = path
        self.comments = comments
        self.sweepDims = sweepDims
        self.sweepIndex = sweepIndex
        self.readoutnamelist = readoutnamelist
        self.sweepnamelist = sweepnamelist
        self.InitialPositions = InitialPositions
        self.mode = mode
        self.fastSeq = fastSeq
        self.readouts = {}
        self.sweeps = {}
        self.reads = readoutnamelist
        self.sweeps = sweepnamelist
        if fname.endswith('.h5'):
            self.read()
        if fname.endswith('.txt'):
            self.read_txt()
        if fname.endswith('.dat'):
            self.read_dat()
        if fname.endswith('.csv'):
            self.read_csv()
        if fname.endswith('.s2p'):
            self.read_s2p()
        import matplotlib.pyplot as plt
        from IPython.display import set_matplotlib_formats
        set_matplotlib_formats('png', 'pdf')
    def read(self):
        """
        read spec data from hdf5 file

        Parameters
        ----------
        input: 
            filename and path
        
        output : 
            sweeplist, readoutlist
        """
        with h5py.File(os.path.join(self.path, self.fname), 'r') as f:
            # read parameter list
            dset = f['Param_list']
            self.comments = str(dset.attrs['comments'])
            self.sweepDims = list(dset.attrs['sweep_dim'])
            self.sweepIndex = list(dset.attrs['sweep_index'])
            self.readoutnamelist = [str(s, 'utf-8') for s in dset.attrs['readout_list']]
            self.reads = [str(s, 'utf-8') for s in dset.attrs['readout_list']]
            self.sweepnamelist = [str(s, 'utf-8') for s in dset.attrs['sweep_list']]
            self.sweeps = [str(s, 'utf-8') for s in dset.attrs['readout_list']]
            # read initial positions
            try:
                self.InitialPositions = np.array(f['Initial_positions'], dtype=init_pos_dt)
            except Exception as e:
                print('This file is not measured yet.')
            # read measurement config information
            dset = f['configure/Meas_config']
            if dset.attrs['fast_mode'][0] == False:
                self.mode = 0
            else:
                if dset.attrs['fast_mode'][1] == True:
                    self.mode = 1
                else:
                    self.mode = 2
            # Get read out data
            self.rlist()
            # Get sweep data
            self.slist()
            
            # Get information about fast sequence
            if not self.mode == 0:
                dac_names = [str(s, 'utf-8') for s in dset.attrs['Fast_channel_name_list']]
                dset = f['configure/fast_sequence']
                self.fastSeq['name'] = str(dset.attrs['Strings'][0], 'utf-8')
                self.fastSeq['seq'] = np.array(dset[...], dtype=float)
                self.fastSeq['start ramp at'] = int(dset.attrs['uint64s'][20])
                
                self.fastSeq['channels'] = [str(dac_names[i]) for i in dset.attrs['uint64s'][4:20]]
                self.fastSeq['divider'] = int(dset.attrs['uint64s'][0])
                if self.mode == 1: # number of points in the data of the first sequence dimension
                    self.fastSeq['count'] = int(self.fastSeq['seq'].shape[1])-2
                else:
                    self.fastSeq['count'] = int(dset.attrs['uint64s'][2])
                    
############################## under construction other file extensions ########################
    def read_txt( self ):
        """
        
        Wrapper function for *.txt import as np.loadtext()
        reads txt files with only 2 columns: x position and height

        Parameters
        ----------
        input: 
            as np.loadtxt(args, kwargs)
        
        output : 
            rlist, slist
        """
        skips = 5
        try:
            data = np.loadtxt(self.fname, delimiter=',', skiprows=skips)
            self.rlist()
            self.slist()
            self.time = data[:,0]
            self.amp = data[:,1]
        except:
            #print(Could not load %s)
            pass

    def read_dat( self ):
        """
        Wrapper function for dat import as np.loadtext()
        reads dat files with only 2 columns: x position and height

        Parameters
        ----------
        input: 
            as np.loadtxt(args, kwargs)
        output : 
            rlist, slist
        """
        try:
            data = np.loadtxt(self.fname)
            self.rlist()
            self.slist()
#            pprint(data)
        except:
            pass
    def read_csv( self ):
        """
        Wrapper function for csv import as np.genfromtext()
        reads simple csv files with only 2 columns: x position and height

        Parameters
        ----------
        input: 
            as np.genfromtxt(args, kwargs)
        output : 
            rlist, slist
        """
        try:
            data = np.genfromtxt(self.fname,skip_header=40,delimiter=',', skip_footer=5)
            self.rlist()
            self.slist()
#            pprint(data)
        except:
            pass
#        self.X = data[0:,0]
#        self.H = data[0:,1]

############################## under construction other file extensions ########################

                
    def slist(self, selection=[]):
        """
        Creating sweep list dictionary

        Parameters
        ----------
        input: 
            sweepnamelist, fname
        output : 
            dictionary of sweeps
        """
        if len(self.sweepnamelist)==0: # Return empty dictionary if there is no sweep parameter
            self.sweeps = {}
        else:
            slist = {'names':[],'dims':[],'params':[],'units':[]}
            if selection == []:
                selection = [Ellipsis]
            elif len(selection) > len(self.sweepDims):
                selection = selection[0:len(self.sweepDims)]
                print('Selected range is larger than sweep dimensions.')
            elif len(selection) < len(self.sweepDims):
                if not Ellipsis in selection:
                    selection.append(Ellipsis)
            selection = tuple(selection)
            
            with h5py.File(os.path.join(self.path, self.fname), 'r') as f:
                for i, name in enumerate(self.sweepnamelist):
                    dset = f[name]
                    slist['dims'].append(int(dset.attrs['dimension']))
                    slist['params'].append(int(dset.attrs['parameter']))
                    if type(dset.attrs['unit'])==str:
                        slist['units'].append(dset.attrs['unit'])
                    else:
                        slist['units'].append(str(dset.attrs['unit'], 'utf-8')) # convert to str if the type is 'bytes'
                        
                    if i == 0:
                        slist['data'] = np.array(dset[selection], dtype=float)
                        dshape = list(slist['data'].shape)
                    else:
                        slist['data'] = np.vstack((slist['data'], np.array(dset[selection], dtype=float)))
            dshape = [i+1]+dshape
            slist['data'] = slist['data'].reshape(tuple(dshape))
            self.sweeps = slist
    
    def rlist(self,selection=[]):
        """
        Creating readout list dictionary

        Parameters
        ----------
        input: 
            as np.genfromtxt(args, kwargs)
        output : 
            rlist, slist
        """
        if len(self.readoutnamelist)==0:
            self.readouts = {}
        else:
            rlist = {'units':[]}
            if not self.mode == 0:
                dimSize = len(self.sweepDims)+1 # Add dim size for fast sequence
            else:
                dimSize = len(self.sweepDims)
                
            if selection == []:
                selection = [Ellipsis]
            elif len(selection) > dimSize:
                selection = selection[0:dimSize]
                print('Selected range is larger than sweep dimensions.')
            elif len(selection) < dimSize:
                if not Ellipsis in selection:
                    selection.append(Ellipsis)
            selection = tuple(selection)
            
            with h5py.File(os.path.join(self.path, self.fname), 'r') as f:
                for i, name in enumerate(self.readoutnamelist):
                    dset = f['data/'+name]
                    if type(dset.attrs['unit'])==str:
                        rlist['units'].append(dset.attrs['unit'])
                    else:
                        rlist['units'].append(str(dset.attrs['unit'], 'utf-8')) # convert to str if the type is 'bytes'
                        
                    if i == 0:
                        rlist['data'] = np.array(dset[selection], dtype=float)
                        dshape = list(rlist['data'].shape)
                    else:
                        rlist['data'] = np.vstack((rlist['data'], np.array(dset[selection], dtype=float)))
            dshape = [i+1]+dshape
            rlist['data'] = rlist['data'].reshape(tuple(dshape))
            self.readouts = rlist
    
    def getAxis(self,
                dim = 0, # dimension number
                axisSelec = 0, # name or number
                selection = slice(None), # partial selection
                ):
        """
        ToDo Update description

        Parameters
        ----------
        input: 
            as np.genfromtxt(args, kwargs)
        output : 
            rlist, slist
        """
        dims = list(self.readouts['data'].shape)[1:] # shape of data for each readout
        """ Get sweep axis for plot """
        if dim == 0:
            # Treat fast sequence
            if self.mode == 1:
                # ramp mode
                fseq = self.fastSeq['seq']
                length = fseq.shape[1]
                # check whether ramp more than 1 variable or not
                count = 0           # count how many fast channels are rampled at the same time
                ramps=[]            # store the fast channels rampled
                while fseq[0, count+self.fastSeq['start ramp at']] != fseq[0, count+self.fastSeq['start ramp at']+1]:
                    ramps.append(int(fseq[0, count+1]))
                    count += 1
                # Get x axis
                if not type(axisSelec) == type(0): # Convert xaxis name to fast channel number
                    if axisSelec in self.fastSeq['channels']: # check given xaxis exists in the fast channel list
                        if int(self.fastSeq['channels'].index(axisSelec)) in ramps: # check obtained fast channel number is valid or not
                            no = ramps.index(int(self.fastSeq['channels'].index(axisSelec)))
                        else:
                            no = 0
                    else:
                        no = 0
                else:
                    if axisSelec in ramps:
                        no = ramps.index(axisSelec)
                    else:
                        no = 0
                try:
                    x0 = float(self.InitialPositions['Value'][self.InitialPositions['Name']==self.fastSeq['channels'][int(ramps[no])].encode('utf-8')])
                except Exception as e:
                    print('Fast channel used in the ramp is not used for your measurement.')
                    x0 = 0
                x = np.linspace(fseq[1, no+self.fastSeq['start ramp at']+1]+x0, fseq[1, length-1-count+no]+x0, num=length-2)[selection]
                labelX = self.fastSeq['channels'][ramps[no]]+' (V)'
            elif self.mode == 2:
                # fast cycle mode
                x = np.arange(int(self.fastSeq['count']))[selection]
                labelX = 'counter (points)'
            else:
                # normal sweep mode
                if self.sweeps == {}:
                    x = np.arange(dims[0],dtype=float)[selection]
                    labelX = 'counter (points)'
                    print('There is no sweep variables.')
                else:
                    partial = [0]*len(dims)
                    partial[dim] = slice(None)
                    partial = tuple(partial)
                    if not type(axisSelec) == type(0):
                        if axisSelec in self.sweepnamelist:
                            axisSelec = self.sweepnamelist.index(axisSelec)
                            x = self.sweeps['data'][axisSelec,Ellipsis][partial][selection]
                            labelX = self.sweepnamelist[axisSelec] + ' ('+self.sweeps['units'][axisSelec]+')'
                        else:
                            x = self.sweeps['data'][0,Ellipsis][partial][selection]
                            labelX = self.sweepnamelist[0] + ' ('+self.sweeps['units'][0]+')'
                    else:
                        if axisSelec < len(self.sweepnamelist):
                            x = self.sweeps['data'][axisSelec,Ellipsis][partial][selection]
                            labelX = self.sweepnamelist[axisSelec] + ' ('+self.sweeps['units'][axisSelec]+')'
                        else:
                            x = self.sweeps['data'][0,Ellipsis][partial][selection]
                            labelX = self.sweepnamelist[0] + ' ('+self.sweeps['units'][0]+')'
                            print('plot range selection is out of range.')
        else:
            if not self.mode == 0: # In case of fast sequence, paxis = plotAxis -1
                paxis = dim - 1
            else:
                paxis = dim
            if self.sweeps == {}:
                x = np.arange(dims[dim],dtype=float)[selection]
                labelX = 'counter (points)'
                print('There is no sweep variables.')
            else:
                partial = [0]*len(self.sweeps['data'].shape[1:])
                partial[paxis] = slice(None)
                partial = tuple(partial)
                if not type(axisSelec) == type(0):
                    if axisSelec in self.sweepnamelist:
                        axisSelec = self.sweepnamelist.index(axisSelec)
                        x = self.sweeps['data'][axisSelec,Ellipsis][partial][selection]
                        labelX = self.sweepnamelist[axisSelec] + ' ('+self.sweeps['units'][axisSelec]+')'
                    else:
                        x = self.sweeps['data'][0,Ellipsis][partial][selection]
                        labelX = self.sweepnamelist[0] + ' ('+self.sweeps['units'][0]+')'
                else:
                    if axisSelec < len(self.sweepnamelist):
                        x = self.sweeps['data'][axisSelec,Ellipsis][partial][selection]
                        labelX = self.sweepnamelist[axisSelec] + ' ('+self.sweeps['units'][axisSelec]+')'
                    else:
                        x = self.sweeps['data'][0,Ellipsis][partial][selection]
                        labelX = self.sweepnamelist[0] + ' ('+self.sweeps['units'][0]+')'
                        print('plot range selection is out of range.')
        # if x[0] == x [-1], convert x to counter
        if x[0] == x[-1]:
            print('Selected axis is not swept: Xmin = Xmax = %f --> useCounter' % (x[0]))
            x = np.linspace(0,x.size-1,num=x.size,dtype=float)
            labelX = 'counter (points)'
        return x, labelX
    
    def getSweepArray(self,
                      selectRange=[],   # range to return the sweep array
                      selectFastSequenceDim = False,    # get axis for fast sequence or not
                      choice = 0,       # choice of the sweep array (number or name)
                      ):
        """
        ToDo Update description

        Parameters
        ----------
        input: 
            selectRange=[],   # range to return the sweep array
            selectFastSequenceDim = False,    # get axis for fast sequence or not
            choice = 0
        output : 
            ar, label
        """
        if self.mode == 0:      # normal sweep mode
            # convert choice to number
            if type(choice) == str:
                if choice in self.sweepnamelist:
                    choice = self.sweepnamelist.index(choice)
                else:
                    choice = 0
            choice = min(choice, len(self.sweepnamelist)-1)
                    
            ar = self.sweeps['data'][choice, Ellipsis][tuple(selectRange)]
            label = self.sweepnamelist[choice]+' ('+self.sweeps['units'][choice]+')'
        elif self.mode == 2:    # fast cycle mode
            dims = [self.fastSeq['count']]+list(self.sweepDims)
            if selectFastSequenceDim:
                ar = np.moveaxis(np.moveaxis(np.ones(tuple(dims), dtype=float), 0, -1)*np.arange(self.fastSeq['count']), -1, 0)[tuple(selectRange)]
                label = 'counter (points)'
            else:
                # convert choice to number
                if type(choice) == str:
                    if choice in self.sweepnamelist:
                        choice = self.sweepnamelist.index(choice)
                    else:
                        choice = 0
                    choice = min(choice, len(self.sweepnamelist)-1)
                    
                ar = self.sweeps['data'][choice,Ellipsis][tuple(list(selectRange[1:]))]
                if not type(selectRange[0]) == int: # when fast cycle axis is chosen to plot, treat array here.
                    ar = np.ones(tuple(dims), dtype=float)[tuple(selectRange)]*ar
                label = self.sweepnamelist[choice]+' ('+self.sweeps['units'][choice]+')'
        elif self.mode == 1:    # fast ramp mode
            dims = [self.fastSeq['count']]+list(self.sweepDims)
            fseq = self.fastSeq['seq']
            length = fseq.shape[1]
            # check whether ramp more than 1 variable or not
            count = 0           # count how many fast channels are rampled at the same time
            ramps=[]            # store the fast channels rampled
            while fseq[0, count+self.fastSeq['start ramp at']] != fseq[0, count+self.fastSeq['start ramp at']+1]:
                ramps.append(int(fseq[0, count+1]))
                count += 1
                
            if selectFastSequenceDim:   # in case fast ramp axis is selected
                # convert choice to number
                if type(choice)==str:
                    if choice in [self.fastSeq['channels'][i] for i in ramps]:
                        choice = self.fastSeq['channels'].index(choice)
                        choice = ramps.index(choice)
                    else:
                        choice = 0
                choice = min(choice, len(ramps)-1)
                # Get offset value
                try:
                    x0 = float(self.InitialPositions['Value'][self.InitialPositions['Name']==self.fastSeq['channels'][int(ramps[choice])].encode('utf-8')])
                except Exception as e:
                    print('Fast channel used in the ramp is not used for your measurement.')
                    x0 = 0
                        
                if self.fastSeq['channels'][ramps[choice]] in self.sweepnamelist: # in case ramped variables is also swept
                    no = self.sweepnamelist.index(self.fastSeq['channels'][ramps[choice]])
                    ar = np.moveaxis(np.moveaxis(np.ones(tuple(dims),dtype=float),0,-1)*np.linspace(x0+fseq[1,choice+self.fastSeq['start ramp at']+1], x0+fseq[1,length-1-count+choice], num=length-2),-1,0)
                    ar = ar + np.ones(tuple(dims),dtype=float)*self.sweeps['data'][no,Ellipsis]
                    ar = ar[tuple(selectRange)]
                else:
                    ar = np.moveaxis(np.moveaxis(np.ones(tuple(dims),dtype=float),0,-1)*np.linspace(x0+fseq[1,choice+self.fastSeq['start ramp at']+1], x0+fseq[1,length-1-count+choice], num=length-2),-1,0)
                    ar = ar[tuple(selectRange)]
                label = self.fastSeq['channels'][ramps[choice]]+' (V)'
            else:
                # convert choice to number
                if type(choice) == str:
                    if choice in self.sweepnamelist:
                        choice = self.sweepnamelist.index(choice)
                    else:
                        choice = 0
                    choice = min(choice, len(self.sweepnamelist)-1)
                        
                if self.sweepnamelist[choice] in [self.fastSeq['channels'][i] for i in ramps]:  # check the selected variable is ramped or not
                    no = self.fastSeq['channels'].index(self.sweepnamelist[choice])
                    no = ramps.index(no)
                    try:
                        x0 = float(self.InitialPositions['Value'][self.InitialPositions['Name']==self.fastSeq['channels'][int(ramps[no])].encode('utf-8')])
                    except Exception as e:
                        print('Fast channel used in the ramp is not used for your measurement.')
                        x0 = 0
                    ar = np.moveaxis(np.moveaxis(np.ones(tuple(dims),dtype=float),0,-1)*np.linspace(x0+fseq[1,no+self.fastSeq['start ramp at']+1], x0+fseq[1,length-1-count+no], num=length-2),-1,0)
                    ar = ar + np.ones(tuple(dims),dtype=float)*self.sweeps['data'][choice,Ellipsis]
                    ar = ar[tuple(selectRange)]
                else:
                    ar = np.ones(tuple(dims),dtype=float)*self.sweeps['data'][choice,Ellipsis]
                    ar = ar[tuple(selectRange)]
                label = self.sweepnamelist[choice]+' ('+self.sweeps['units'][choice]+')'
            
        return ar, label
    
    def plot1D(self,*args, **kwargs):
        """
        Wrapper function for 1D plotting with mpl.plt.plot()

        Prameters
        ----------
        input: 
            arguments as matplotlib.pyplot.plot(*args, **kwargs)
        aditional inputs: 
            to be completed
        output: 
            mpl line
        """
        if len(self.readoutnamelist)==0: # escape plot if there is no readout
            return
        
        """
        define all additional inputs to variables set defaults and delete args kwargs
        """
        if 'figNo' in kwargs:
            figNo = kwargs['figNo']
            del kwargs['figNo']
        else:
            figNo = 0
        if 'ax' in kwargs:
            ax = kwargs['ax']
            del kwargs['ax']
        else:
            ax = ''
        if 'clear' in kwargs:
            clear = kwargs['clear']
            del kwargs['clear']
        else:
            clear = False
        if 'counter' in kwargs:
           useCounter = kwargs['counter']
           del kwargs['counter']
        else:
            useCounter = False
        if 'showTitle' in kwargs:
            showTitle = kwargs['showTitle']
            del kwargs['showTitle']
        else:
            showTitle = True
        if 'showLegend' in kwargs:
            showLegend = kwargs['showLegend']
            del kwargs['showLegend']
        else:
            showLegend = True
        if 'showGrid' in kwargs:
            showGrid = kwargs['showGrid']
            del kwargs['showGrid']
        else:
            showGrid = False
        if 'title' in kwargs:
            titlein = kwargs['title']
            del kwargs['title']
        else:
            titlein = ''  
        if 'plotAxis' in kwargs:
            plotAxis = kwargs['plotAxis']
            del kwargs['plotAxis']
        else:
            plotAxis = 0
        if 'plotRange' in kwargs:
            plotrange = kwargs['plotRange']
            del kwargs['plotRange']
        else:
            plotrange = []
        if 'readouts' in kwargs:
            readouts = kwargs['readouts']
            del kwargs['readouts']
        else:
            readouts = []
        if 'xaxis' in kwargs:
            xaxis = kwargs['xaxis']
            del kwargs['xaxis']
        else:
            xaxis = 0
        if 'xoffsets' in kwargs:
            xoffsets = kwargs['xoffsets']
            del kwargs['xoffsets']
        else:
            xoffsets = []
        if 'yoffsets' in kwargs:
            yoffsets = kwargs['yoffsets']
            del kwargs['yoffsets']
        else:
            yoffsets = []
        if 'xfactor' in kwargs:
            xfactor = kwargs['xfactor']
            del kwargs['xfactor']
        else:
            xfactor = 1
        if 'yfactor' in kwargs:
            yfactor = kwargs['yfactor']
            del kwargs['yfactor']
        else:
            yfactor = 1
        if 'ylaw' in kwargs:
            ylaw = True
            del kwargs['ylaw']
        if 'xlabel' in kwargs:
            xlabel = kwargs['xlabel']
            del kwargs['xlabel']
        else:
            xlabel = ''
        if 'ylabel' in kwargs:
            ylabel = kwargs['ylabel']
            del kwargs['ylabel']
        else:
            ylabel = ''
        if 'xaxisRange' in kwargs:
            xaxisRange = kwargs['xaxisRange']
            del kwargs['xaxisRange']
        else:
            xaxisRange = []
        if 'yaxisRange' in kwargs:
            yaxisRange = kwargs['yaxisRange']
            del kwargs['yaxisRange']
        else:
            yaxisRange = []
        if 'xtickFreq' in kwargs:
            xtickFreq = kwargs['xtickFreq']
            del kwargs['xtickFreq']
        else:
            xtickFreq = 0
        if 'ytickFreq' in kwargs:
            ytickFreq = kwargs['ytickFreq']
            del kwargs['ytickFreq']
        else:
            ytickFreq = 0
        if 'xticks' in kwargs:
            xticks = kwargs['xticks']
            del kwargs['xticks']
        else:
            xticks= []
        if 'yticks' in kwargs:
            yticks= kwargs['yticks']
            del kwargs['yticks']
        else:
            yticks = []
        
        if 'mode' in kwargs:
            mode = kwargs['mode']
            del kwargs['mode']
        else:
            mode = 'standard'
        
        """ Define figure and ax if ax is not given."""
        if ax == '':
            tight = True
            """ Either plot for specific figure or make new figure"""
            if figNo == 0:
                if plt.fignum_exists(figNo):
                    plt.figure(0)
                else:
                    fig = plt.figure()
            else:
                if plt.fignum_exists(figNo):
                    fig = plt.figure(figNo)
                else:
                    fig = plt.figure()
                if clear:
                    fig.clf()
            ax = plt.gca()
            """ Set background white """
            fig.patch.set_facecolor('#ffffff')
        else:
            tight = False
            
        """ set title """
        if showTitle:
            if titlein == '':
                titlein = self.fname
            ax.set_title(titlein)
            
                
        # Get dimensions
        dims = list(self.readouts['data'].shape)[1:]
        
        # correct plotAxis into the available range
        plotAxis = max(0, plotAxis)
        plotAxis = min(len(dims)-1, plotAxis)
        
        # correct readouts
        if readouts == []:
            readouts = [0]
                
        # Treat plot range
        if plotrange == []:
            plotrange = [slice(None)]*len(dims)
        elif len(plotrange) > len(dims):
            plotrange = plotrange[0:len(dims)]
            print('Selected range is larger than sweep dimensions.')
        elif len(plotrange) < len(dims):
            dif = len(dims)-len(plotrange)
            if not Ellipsis in plotrange:
                plotrange += [slice(None)]*(dif)
            else:
                plotrange = plotrange[0:plotrange.index(Ellipsis)]+[slice(None)]*(dif)+plotrange[plotrange.index(Ellipsis)+1:]
        for i, p in enumerate(plotrange):
            if type(p) == int:
                plotrange[i] = slice(p,p+1) # By replacing number to slice of 1 value, keep the data dimensions
            
        # make offset array
        xoffset = np.zeros(dims, dtype=float)
        yoffset = np.zeros(dims, dtype=float)
        for i, dim in enumerate(dims):
            if i < len(xoffsets):
                xoffset = np.moveaxis(xoffset, i, -1)
                xoffset = np.add(xoffset, np.linspace(0, xoffsets[i]*(dim-1), num=dim))
                xoffset = np.moveaxis(xoffset, -1, i)
            if i < len(yoffsets):
                yoffset = np.moveaxis(yoffset, i, -1)
                yoffset = np.add(yoffset, np.linspace(0, yoffsets[i]*(dim-1), num=dim))
                yoffset = np.moveaxis(yoffset, -1, i)
        xoffset = xoffset[tuple(plotrange)]
        yoffset = yoffset[tuple(plotrange)]
        
        # Get xaxis
        if mode == 'standard':
            if useCounter:
                X = np.arange(dims[plotAxis])[plotrange[plotAxis]]
                X = np.multiply(X, xfactor) # Apply factor for x
                #print('apply X factor')
                labelX = 'Counter (points)'
            else:
                X, labelX = self.getAxis(dim = plotAxis,
                                 axisSelec = xaxis,
                                 selection = plotrange[plotAxis])
                X = np.multiply(X, xfactor) # Apply factor for x
        elif mode == 'vector':
            if useCounter:
                X = np.moveaxis(np.moveaxis(np.ones(tuple(dims),dtype=float),plotAxis,-1)*np.arange(dims[plotAxis]),-1,plotAxis)[tuple(plotrange)]
                labelX = 'Counter (points)'
            else:
                if (self.mode != 0) and (plotAxis == 0):    # fast sequence and plot axis = 0
                    selectFastSequenceDim = True
                else:
                    selectFastSequenceDim = False
                    
                X, labelX = self.getSweepArray(selectRange=plotrange,
                                               selectFastSequenceDim=selectFastSequenceDim,
                                               choice=xaxis)
                X = np.moveaxis(X, plotAxis, 0) # move plot axis to axis 0
                dshape = X.shape                # Get the dim size
                X = X.reshape(dshape[0], -1)    # reshape X for plot

        labelY = ''
        xoffset = np.moveaxis(xoffset, plotAxis, 0) # move plot axis to axis0
        dshape = xoffset.shape # Get the dim size
        xoffset = xoffset.reshape(dshape[0], -1) # reshape xoffset for plot
        
        for i, read in enumerate(readouts):
            if not type(read)==type(0): #if read is name, convert to number.
                if read in self.readoutnamelist:
                    read = self.readoutnamelist.index(read)
                else:
                    read = i
            d = self.readouts['data'][read,Ellipsis][tuple(plotrange)]      # Get data
            d = np.multiply(d, yfactor) # Apply factor for data
            try:
                if ylaw:
                    try:
                        #print('apply Y scaling Law')
                        from ptcalib import PTspline
                        spline = PTspline()
                        d = spline(d)
                        ylabel = r'$T$'+'(°C)'
                        #print(d)
                    except:
                        print('No import found for the Y Scaling Law')
            except:
                pass
            d = np.add(d, yoffset) # Apply offset to data
            d = np.moveaxis(d, plotAxis, 0) # move plot axis to axis0
            d = d.reshape(dshape[0], -1) # reshape data for plot
            NoPlot = d.shape[1] # keep dimension
            if i == 0:
                xmin = np.min(X)+np.min(xoffset); xmax = np.max(X)+np.max(xoffset)
                ymin = np.min(d); ymax = np.max(d)
            else:
                xmin = min(xmin, np.min(X)+np.min(xoffset)); xmax = max(xmax, np.max(X)+np.max(xoffset))
                ymin = min(ymin, np.min(d)); ymax = max(ymax, np.max(d))
                labelY += ', '
            for j in range(NoPlot):
                if mode == 'standard':
                    x = X + xoffset[:,j]; y = d[:,j]
                elif mode == 'vector':
                    x = X[:,j] + xoffset[:,j]; y = d[:,j]
                if j == 0: # put legend only for the first one
                    ax.plot(x, y, label=self.readoutnamelist[read]+\
                            '('+self.readouts['units'][read]+')', *args, **kwargs)
                else:
                    ax.plot(x, y, *args, **kwargs)
            labelY += self.readoutnamelist[read]+' ('+self.readouts['units'][read]+')'
            
        """ set various plotting settings """       
        if xlabel=='':     ax.set_xlabel(labelX)  
        else:              ax.set_xlabel(xlabel)
        if ylabel=='':     ax.set_ylabel(labelY)
        else:              ax.set_ylabel(ylabel)
        if showLegend:     
            ax.legend(loc='best')
        """ set tick  and their label size """
        if xticks==[]:
            if xtickFreq > 0:
                ax.set_xticks(np.linspace(xmin,xmax,xtickFreq))
        else:
            ax.set_xticks(xticks)
        if yticks==[]:
            if ytickFreq > 0:
                ax.set_yticks(np.linspace(ymin,ymax,ytickFreq))
        else:
            ax.set_yticks(yticks)
        ax.tick_params(axis='both', which='major')
        """ set axis range """    
        if xaxisRange == []:
            ax.set_xlim([xmin,xmax])
        else:
            ax.set_xlim(xaxisRange)
        if yaxisRange == []:
            ax.set_ylim([ymin-(ymax-ymin)*0.05,ymax+(ymax-ymin)*0.05])
        else:
            ax.set_ylim(yaxisRange)
        if showGrid == True:     ax.grid()
        if tight:   plt.tight_layout()
#        
#    def plot2D(self,
#               figNo=0,
#               title='',
#               fig='',                                                         # plot data to given fig
#               ax = '',                                                        # plot data into given ax
#               plotDims = [[0,0],[1,0]],                                        # plot axis [[x, choice], [y, choice]] (choice is number of 'name')
#               readout=0,                                                     # name or number of readout instrument that should be plotted on z-axis
#               plotrange= [],                                                    # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
#               factors = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
#               clear = True,                                                   # clear previous plot or not
#               showColorbar = True, showTitle = True, showGrid = True,
#               flipX = False, flipY = False, transpose = True,
#               xlabel = '',   ylabel = '',   zlabel = '',
#               x_ax_range=[], y_ax_range=[], z_ax_range=[],
#               xtickFreq=0, ytickFreq=0, z_tick_freq=0,
#               xticks=[],     yticks=[],     zticks=[],
#               colormap = "viridis", lineSlice = False, pyqt = False,
#               mode = ['imshow', 'pcolormesh'][0],          # (under construction) please use pcolor mesh when you plot vector sweep data.
#               ):
#        if len(self.readoutnamelist)==0: # Escape if there is no readout.
#            return
#        """ Define figure and ax if ax is not given."""
#        if ax == '' or (lineSlice and pyqt): # create ax if ax is not given. Or line slice is True and ax is given by pyqt.
#            tight = True
#            """Either plot for specific figure or make new figure"""
#            if figNo == 0:
#                fig = plt.figure()
#            else:
#                fig = plt.figure(figNo)
#                if clear == True:
#                    fig.clf()
#            ax = fig.add_subplot(111)
#            """ Set background white """
#            fig.patch.set_facecolor('#ffffff')
#        else:
#            tight = False
#            
#        """ set title """
#        if showTitle:
#            if title == '':
#                title = self.plotrange
#            ax.set_title(title)
#                
#        # Get dimensions
#        dims = list(self.readouts['data'].shape)[1:]
#            
#        # Treat plot range
#        if plotrange == []:
#            plotrange = [0]*len(dims)
#            plotrange[plotDims[0][0]]=slice(None)
#            plotrange[plotDims[1][0]]=slice(None)
#        else:
#            if len(plotrange)>len(dims):
#                plotrange = plotrange[:len(dims)]
#            elif len(plotrange)<len(dims):
#                dif = len(dims)-len(plotrange)
#                length = len(plotrange)
#                for i in range(dif):
#                    if (length+i == plotDims[0][0]) or (length+i == plotDims[1][0]):
#                        plotrange.append(slice(None))
#                    else:
#                        plotrange.append(0)            
#            for i in range(len(dims)):
#                if (i==plotDims[0][0]) or (i==plotDims[1][0]):
#                    if type(plotrange[i]) == int:   # plot axis should slice and else should be int.
#                        plotrange[i] = slice(None)
#                else:
#                    if not type(plotrange[i]) == int: # if non integer is given, correct it to 0.
#                        plotrange[i] = 0
#                    else: 
#                        n = plotrange[i] # if the given range is not within the available range, correct it.
#                        plotrange[i] = int(max(0, plotrange[i]))
#                        plotrange[i] = int(min(dims[i]-1, plotrange[i]))
#                        if n != plotrange[i]:
#                            print('Selected plotrange[%d]=%d is corrected to %d.' % (i, n, plotrange[i]))
#            
#        # Get data
#        selectRange = tuple(plotrange)
#        if not type(readout) == type(0): # check whether readout is name or number, then get data
#            if readout in self.readoutnamelist:
#                readout = self.readoutnamelist.index(readout)
#                data = self.readouts['data'][readout,Ellipsis]
#            else:
#                readout = 0
#                data = self.readouts['data'][0,Ellipsis]
#        else:
#            if readout < len(self.readoutnamelist):
#                data = self.readouts['data'][readout,Ellipsis]
#            else:
#                readout = 0
#                data = self.readouts['data'][0,Ellipsis]
#        Z = data[selectRange]
#        if plotDims[0][0]>plotDims[1][0]: # set x axis to first dimension
#            Z = np.moveaxis(Z, 1, 0)
#        labelZ = self.readoutnamelist[readout]+' ('+self.readouts['units'][readout]+')'
#        
#        # Get plot axis
#        if mode == 'imshow':
#            # Get xaxis
#            X, labelX = self.getAxis(dim = plotDims[0][0],
#                             axisSelec = plotDims[0][1],
#                             selection = plotrange[plotDims[0][0]])
#            # Get yaxis
#            Y, labelY = self.getAxis(dim = plotDims[1][0],
#                             axisSelec = plotDims[1][1],
#                             selection = plotrange[plotDims[1][0]])
#        elif mode == 'pcolormesh':
#            if plotDims[0][0]==0:
#                selectFastSequenceDim = True
#            else:
#                selectFastSequenceDim = False
#            X, labelX = self.getSweepArray(selectRange=plotrange,   # range to return the sweep array
#                                          selectFastSequenceDim = selectFastSequenceDim,    # get axis for fast sequence or not
#                                          choice = plotDims[0][1],       # choice of the sweep array (number or name)
#                                          )
#            if plotDims[1][0]==0:
#                selectFastSequenceDim = True
#            else:
#                selectFastSequenceDim = False
#            Y, labelY = self.getSweepArray(selectRange=plotrange,   # range to return the sweep array
#                                          selectFastSequenceDim = selectFastSequenceDim,    # get axis for fast sequence or not
#                                          choice = plotDims[1][1],       # choice of the sweep array (number or name)
#                                          )
#        # Apply factor
#        X = np.multiply(X, factors[0]) # Apply factor for x
#        Y = np.multiply(Y, factors[1]) # Apply factor for y        
#
#        if transpose:
#            Z = Z.T
#            T = X
#            X = Y
#            Y = T
#            t = labelX; labelX = labelY; labelY = t
#            if mode == 'pcolormesh':
#                X = X.T
#                Y = Y.T
#            
#        # Get plot limits for X, Y and Z
#        if mode == 'imshow':
#            xini = X[0]; xfin = X[-1];
#            yini = Y[0]; yfin = Y[-1];
#        elif mode == 'pcolormesh':
#            xini = X[0,0]; xfin = X[-1,-1];
#            yini = Y[0,0]; yfin = Y[-1,-1];
#        
#        if z_ax_range == []:                                                   # Obtain limits of z.
#            zmin = np.min(Z.flatten()); zmax = np.max(Z.flatten())
#        else:
#            zmin = z_ax_range[0]; zmax = z_ax_range[1];
#            
#        # plot
#        if mode == 'imshow':
#            # imshow
#            cax = ax.imshow(np.fliplr(np.flipud(Z)).T, extent=(xfin,xini,yfin,yini),origin='lower',
#                      interpolation='nearest', aspect='auto', cmap=plt.get_cmap(colormap),
#                      vmin=zmin, vmax=zmax)
#        elif mode == 'pcolormesh':
#            #pcolormesh used for plotting the vector sweep data
#            cax = ax.pcolormesh(X, Y, Z, cmap=plt.get_cmap(colormap),
#                      vmin=zmin, vmax=zmax)
#        
#        """ Add colorbar, set label and ticks """
#        if showColorbar:
#            cbar = fig.colorbar(cax)
#            if zlabel == '':  cbar.set_label(labelZ, rotation=270, labelpad=20)
#            else:             cbar.set_label(zlabel, rotation=270, labelpad=20)
#            if zticks==[]:
#                if z_tick_freq > 0:
#                    cbar.ax.set_ticks(np.linspace(zmin,zmax,z_tick_freq))
#            else:
#                cbar.ax.set_ticks(zticks)
#            #cbar.ax.tick_params(labelsize=ticklabelsize) 
#        
#        """ set various plotting settings """       
#        if xlabel=='':     ax.set_xlabel(labelX)  
#        else:              ax.set_xlabel(xlabel)
#        if ylabel=='':     ax.set_ylabel(labelY)
#        else:              ax.set_ylabel(ylabel)
#            
#        """ set tick  and their label size """
#        if xticks==[]:
#            if xtickFreq > 0:
#                ax.set_xticks(np.linspace(xini,xfin,xtickFreq))
#        else:
#            ax.set_xticks(xticks)
#        if yticks==[]:
#            if ytickFreq > 0:
#                ax.set_yticks(np.linspace(yini,yfin,ytickFreq))
#        else:
#            ax.set_yticks(yticks)
#        ax.tick_params(axis='both', which='major')
#        """ set axis ranges """
#        if not x_ax_range == []:
#            ax.set_xlim(x_ax_range[0], x_ax_range[1])
#        if not y_ax_range == []:
#            ax.set_ylim(y_ax_range[0], y_ax_range[1])
#            
#        """ Flip axes """
#        if flipX:
#            ax.invert_xaxis()
#        
#        if flipY:
#            ax.invert_yaxis()
#        
#        if showGrid == True:     ax.grid()                                     # If chosen, show grid.
#        if tight:   plt.tight_layout()
#        # Image line slice
#        if lineSlice:
#            fig2 = plt.figure('Image slice')
#            fig2.clf()
#            axS = fig2.add_subplot(111)
#            LnTr = LineSlice(cax, axS, Z, X, Y)
        
if __name__=='__main__':

    flist = []
    plist = []
    for f in sorted(glob.glob('*.h5')):
        fname = f
        path = os.getcwd()
        print('Current Directory: '+str(path))
        print('File: ' + str(f))
        flist.append(f)
        
    """ for test only select first file in cwd flist[0]"""
    data = spec(fname = flist[0],path = path)
    data.read()
#    print('Sweeps:')
#    print(data.sweepnamelist)
#    print('Readouts:')
#    print(data.readoutnamelist)
        
    """
    Test 1D plotting on hdf5 files
    """
    for i,unit in enumerate(data.readouts['units']):
        #readoutlist to be completed
        name = data.reads[i]
        print('Readout %i: %s in (%s)' %(i, data.reads[i], unit))
        data.plot1D(figNo=i, # Number of the figure in case ax is not given
               #ax='', # ax to be plotted data
               #clear = True, # clear the existing plot in the 'ax'
               counter=True,
               #showLegend=True, showTitle=True, showGrid=False,
               #title = '', # set title
               #plotAxis = 0, # plot along 
               #plotrange=[], # plot range ex.) [slice(0,100), slice(None), Ellipsis, 0]
               readouts = [i], # select plot readout by name or number
               #xaxis = 4, #0, 1, 2 or 'name' of axis
               #xoffsets=[], yoffsets=[],
               #xfactor=1, yfactor=1,
               xlabel='time (minutes)', ylabel='',
               #xaxisRange = [], yaxisRange = [],
               #xtickFreq = 0, ytickFreq = 0,
               #xticks=[], yticks=[],
               #markers=['P'], markersize=3,
               #mode = ['standard', 'vector'][0],
               )
    pass
