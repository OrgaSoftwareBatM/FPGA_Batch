#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:16:32 2017

@author: shintaro
"""

import sys, os
sys.path.insert(0,'..') # import parent directory
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.gridspec as gridspec
from DataStructure.LoadGDS import structurefromGDS
import textwrap
from cycler import cycler
from DataStructure.ImageSlice import LineSlice
from PyQt5 import QtCore
rc('axes', prop_cycle=(cycler('color',
                            ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                              '#bcbd22', '#17becf'])))
rc('lines', linewidth=1.0)
rc('font',**{'family':'sans-serif', 'sans-serif':'Helvetica'})
rc('text',**{'usetex':False, 'latex.unicode':False})
rc('axes',**{'facecolor':'white', 'edgecolor':'black', 'grid':False, 'linewidth': 1.0,
             'titlesize':18, 'labelsize':16})
rc('xtick',**{'top':True, 'bottom':True, 'direction':'in'})
rc('ytick',**{'left':True, 'right':True, 'direction':'in'})
rc('grid',**{'color':'grey','linewidth':0.5,'linestyle':':','alpha':0.5})
rc('figure',**{'titlesize':18, 'facecolor':'white', 'edgecolor':'white'})
rc('savefig',**{'format':'pdf'})
rc('mathtext',**{'fontset':'stix'})
rc('legend',**{'fontsize':12})
rc('image',cmap='viridis')

init_pos_dt = np.dtype({'names':['Name','kind','Value'],'formats':['S100','u8','f8']})
pathSeparator = QtCore.QDir.separator()
gdsname = 'HBT6'

class ExpData():
    def __init__(self,
                 filename = '',
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
        self.filename = filename
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
        
    def readData(self):
        with h5py.File(self.path+self.filename+'.h5', 'r') as f:
            # read parameter list
            dset = f['Param_list']
            self.comments = str(dset.attrs['comments'])
            self.sweepDims = list(dset.attrs['sweep_dim'])
            self.sweepIndex = list(dset.attrs['sweep_index'])
            self.readoutnamelist = [str(s, 'utf-8') for s in dset.attrs['readout_list']]
            self.sweepnamelist = [str(s, 'utf-8') for s in dset.attrs['sweep_list']]
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
                
    def slist(self, selection=[]):
        if len(self.sweepnamelist)==0: # Return empty dictionary if there is no sweep parameter
            self.sweeps = {}
        else:
            slist = {'dims':[],'params':[],'units':[]}
            if selection == []:
                selection = [Ellipsis]
            elif len(selection) > len(self.sweepDims):
                selection = selection[0:len(self.sweepDims)]
                print('Selected range is larger than sweep dimensions.')
            elif len(selection) < len(self.sweepDims):
                if not Ellipsis in selection:
                    selection.append(Ellipsis)
            selection = tuple(selection)
            
            with h5py.File(self.path+self.filename+'.h5', 'r') as f:
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
            
            with h5py.File(self.path+self.filename+'.h5', 'r') as f:
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
            if not self.mode == 0: # In case of fast sequence, paxis = plotaxis -1
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
            print('Selected axis is not swept along the plot axis. The fixed value is %f.' % (x[0]))
            x = np.linspace(0,x.size-1,num=x.size,dtype=float)
            labelX = 'counter (points)'
        return x, labelX
    
    def getSweepArray(self,
                      selectRange=[],   # range to return the sweep array
                      selectFastSequenceDim = False,    # get axis for fast sequence or not
                      choice = 0,       # choice of the sweep array (number or name)
                      ):
        """ Get array for the 3D plot or pcolormesh plot """
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
    
    def getGateConfig(self,
                      axes=[],
                      gdsFile=os.path.dirname(os.path.abspath(__file__))+pathSeparator+'GDS'+pathSeparator+gdsname+'.GDS',
                      figNo='Config',
                      commentsize=8,
                      labelsize = 8,
                      titlesize = 10,
                      ):
        try:
            getStuff = structurefromGDS(gdsFile)
        except:
            print('GDS file has not been found.')
            return
        
        """ read initial positions """
        if type(self.InitialPositions) == type([]):
            print('This file has not been measured yet.')
            return
            
        """ plot into given ax."""
        if axes ==[]:
            tight = True
            if figNo == 0:
                fig = plt.figure(figsize=(2*3.375,1.8*3.375))
            else:
                fig = plt.figure(figNo,figsize=(2*3.375,1.8*3.375))
                fig.clf()
            fig.patch.set_facecolor('#ffffff')
            fig.subplots_adjust(left=0.01, top=0.94, right=0.99, bottom=0.1, hspace=0.1, wspace=0.1)
            plt.suptitle(self.filename,y=0.99,fontsize=titlesize)
            axes.append(plt.subplot2grid((4,1),(0,0),rowspan=3))
            axes.append(plt.subplot2grid((4,1),(3,0)))
        else:
            tight = False
            axes[0].set_title(self.filename)
        
        """
        Plot the gate geometry with all the gate voltages
        """
        axes[0].get_xaxis().set_visible(False)
        axes[0].get_yaxis().set_visible(False)
        axes[0].set_frame_on(False)
        clist = np.array(['green','blue','orange','purple','cyan','yellow'])
        xmin = 0; xmax=0; ymin = 0; ymax=0;
        for i, array in enumerate(getStuff()):
                xpos = array[:,0]
                ypos = array[:,1]
                if max(xpos)>xmax: xmax=max(xpos)
                if min(xpos)<xmin: xmin=min(xpos)
                if max(ypos)>ymax: ymax=max(ypos)
                if min(ypos)<ymin: ymin=min(ypos)
                """Show gates with enumeration if wanted"""
                if not i in getStuff.string_infos.keys():                                  # If polygone ...
                    axes[0].fill(xpos, ypos, facecolor='grey',alpha=0.2,edgecolor='white') # draw it.
                else:                                                                      # If label ...
                    col='black'; style='normal'
                    label = str(getStuff.string_infos[i], 'utf-8')
                    if np.any(label.encode('utf-8')==self.InitialPositions['Name']):
                        gValue = "%s=%4.3f V" % (label, self.InitialPositions['Value'][label.encode('utf-8')==self.InitialPositions['Name']])
                        if label in self.sweepnamelist:
                            gValue = label
                            j = int(self.sweeps['dims'][self.sweepnamelist.index(label)])
                            col = clist[j]; style='bold'
                        if self.mode == 1: # for ramp mode
                            fast_channel_index = list(set(self.fastSeq['seq'][0,1:-1]))
                            for index in fast_channel_index:
                                if label == self.fastSeq['channels'][int(index)]:
                                    gValue = label
                                    col = "red"; style='bold'
                    elif label in self.readoutnamelist:
                            gValue = "read %s" % label
                            style='bold'
                    else:
                            gValue = label
                    axes[0].text(xpos[0], ypos[0], gValue, color=col, weight=style, size=labelsize)
        axes[0].set_xlim([xmin, xmax]); axes[0].set_ylim([ymin, ymax])
        axes[0].margins(0)
        # comments            
        axes[1].axis('off')
        axes[1].margins(0)
        axes[1].annotate(textwrap.fill(self.comments, width=70),(0.01,0.999),xycoords='axes fraction',
                         horizontalalignment='left',verticalalignment='top', size=commentsize)
        if tight:   plt.tight_layout()
    
    def plot1D(self,
               figNo=0, # Number of the figure in case ax is not given
               ax='', # ax to be plotted data
               clear = True, # clear the existing plot in the 'ax'
               useCounter = False,
               showlegend=True, showTitle=True, showGrid=True,
               title = '', # set title
               plotaxis = 0, # plot along 
               plotrange=[], # plot range ex.) [slice(0,100), slice(None), Ellipsis, 0]
               readouts = [], # select plot readout by name or number
               xaxis = 0, #0, 1, 2 or 'name' of axis
               xoffsets=[], yoffsets=[], # offset for x and y
               xfactor=1, yfactor=1, # factor to multiply
               xlabel='', ylabel='',
               x_axis_range = [], y_axis_range = [],
               x_tick_freq = 0, y_tick_freq = 0,
               xticks=[], yticks=[],
               ticklabelsize = 12, labelsize = 14,
               linestyles=[], linewidth = 1.0,
               markers=[None], markersize=3,
               colors=[],
               mode = ['standard', 'vector'][0],          # (under construction) please use pcolor mesh when you plot vector sweep data.
               ):
        if len(self.readoutnamelist)==0: # escape plot if there is no readout
            return
        """ Define figure and ax if ax is not given."""
        if ax == '':
            tight = True
            """ Either plot for specific figure or make new figure"""
            if figNo == 0:
                fig = plt.figure()
            else:
                fig = plt.figure(figNo)
                if clear:
                    fig.clf()
            ax = fig.add_subplot(111)
            """ Set background white """
            fig.patch.set_facecolor('#ffffff')
        else:
            tight = False
            
        """ set title """
        if showTitle:
            if title == '':
                title = self.filename
            ax.set_title(title, fontdict={'fontsize':labelsize})
                
        # Get dimensions
        dims = list(self.readouts['data'].shape)[1:]
        
        # correct plotaxis into the available range
        plotaxis = max(0, plotaxis)
        plotaxis = min(len(dims)-1, plotaxis)
        
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
                X = np.arange(dims[plotaxis])[plotrange[plotaxis]]
                labelX = 'Counter (points)'
            else:
                X, labelX = self.getAxis(dim = plotaxis,
                                 axisSelec = xaxis,
                                 selection = plotrange[plotaxis])
                X = np.multiply(X, xfactor) # Apply factor for x
        elif mode == 'vector':
            if useCounter:
                X = np.moveaxis(np.moveaxis(np.ones(tuple(dims),dtype=float),plotaxis,-1)*np.arange(dims[plotaxis]),-1,plotaxis)[tuple(plotrange)]
                labelX = 'Counter (points)'
            else:
                if (self.mode != 0) and (plotaxis == 0):    # fast sequence and plot axis = 0
                    selectFastSequenceDim = True
                else:
                    selectFastSequenceDim = False
                    
                X, labelX = self.getSweepArray(selectRange=plotrange,
                                               selectFastSequenceDim=selectFastSequenceDim,
                                               choice=xaxis)
                X = np.moveaxis(X, plotaxis, 0) # move plot axis to axis 0
                dshape = X.shape                # Get the dim size
                X = X.reshape(dshape[0], -1)    # reshape X for plot
                
        # start ploting
        if linestyles == []:
            linestyles = ['-','--',':','-.']
        
        if colors == []:
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                      '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                      '#bcbd22', '#17becf']
        if markers == []:
            markers = [None]
        labelY = ''
        xoffset = np.moveaxis(xoffset, plotaxis, 0) # move plot axis to axis0
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
            d = np.add(d, yoffset) # Apply offset to data
            d = np.moveaxis(d, plotaxis, 0) # move plot axis to axis0
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
                    ax.plot(x, y, linewidth = linewidth,
                            linestyle=linestyles[np.mod(i, len(linestyles))],
                            color = colors[np.mod(j+i,len(colors))],
                            marker=markers[np.mod(i, len(markers))], markersize=markersize,
                            label=self.readoutnamelist[read]+'('+self.readouts['units'][read]+')'
                            )
                else:
                    ax.plot(x, y, linewidth = linewidth,
                        linestyle=linestyles[np.mod(i, len(linestyles))],
                        color = colors[np.mod(j+i,len(colors))],
                        )
            labelY += self.readoutnamelist[read]+' ('+self.readouts['units'][read]+')'
            
        """ set various plotting settings """       
        if xlabel=='':     ax.set_xlabel(labelX, fontsize=labelsize)  
        else:              ax.set_xlabel(xlabel, fontsize=labelsize)
        if ylabel=='':     ax.set_ylabel(labelY, fontsize=labelsize)
        else:              ax.set_ylabel(ylabel, fontsize=labelsize)
        if showlegend:     
            ax.legend(loc='best')
        """ set tick  and their label size """
        if xticks==[]:
            if x_tick_freq > 0:
                ax.set_xticks(np.linspace(xmin,xmax,x_tick_freq))
        else:
            ax.set_xticks(xticks)
        if yticks==[]:
            if y_tick_freq > 0:
                ax.set_yticks(np.linspace(ymin,ymax,y_tick_freq))
        else:
            ax.set_yticks(yticks)
        ax.tick_params(axis='both', which='major', labelsize=ticklabelsize)
        """ set axis range """    
        if x_axis_range == []:
            ax.set_xlim([xmin,xmax])
        else:
            ax.set_xlim(x_axis_range)
        if y_axis_range == []:
            ax.set_ylim([ymin-(ymax-ymin)*0.05,ymax+(ymax-ymin)*0.05])
        else:
            ax.set_ylim(y_axis_range)
        if showGrid == True:     ax.grid()
        if tight:   plt.tight_layout()
        
    def plot2D(self,
               figNo=0,
               title='',
               fig='',                                                         # plot data to given fig
               ax = '',                                                        # plot data into given ax
               plotDims = [[0,0],[1,0]],                                        # plot axis [[x, choice], [y, choice]] (choice is number of 'name')
               readout=0,                                                     # name or number of readout instrument that should be plotted on z-axis
               plotrange= [],                                                    # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
               factors = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
               clear = True,                                                   # clear previous plot or not
               showColorbar = True, showTitle = True, showGrid = True,
               flipX = False, flipY = False, transpose = True,
               xlabel = '',   ylabel = '',   zlabel = '',
               x_ax_range=[], y_ax_range=[], z_ax_range=[],
               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
               xticks=[],     yticks=[],     zticks=[],
               ticklabelsize = 12, labelsize = 14,
               colormap = "viridis", lineSlice = False, pyqt = False,
               mode = ['imshow', 'pcolormesh'][0],          # (under construction) please use pcolor mesh when you plot vector sweep data.
               ):
        if len(self.readoutnamelist)==0: # Escape if there is no readout.
            return
        """ Define figure and ax if ax is not given."""
        if ax == '' or (lineSlice and pyqt): # create ax if ax is not given. Or line slice is True and ax is given by pyqt.
            tight = True
            """Either plot for specific figure or make new figure"""
            if figNo == 0:
                fig = plt.figure()
            else:
                fig = plt.figure(figNo)
                if clear == True:
                    fig.clf()
            ax = fig.add_subplot(111)
            """ Set background white """
            fig.patch.set_facecolor('#ffffff')
        else:
            tight = False
            
        """ set title """
        if showTitle:
            if title == '':
                title = self.filename
            ax.set_title(title, fontdict={'fontsize':labelsize})
                
        # Get dimensions
        dims = list(self.readouts['data'].shape)[1:]
            
        # Treat plot range
        if plotrange == []:
            plotrange = [0]*len(dims)
            plotrange[plotDims[0][0]]=slice(None)
            plotrange[plotDims[1][0]]=slice(None)
        else:
            if len(plotrange)>len(dims):
                plotrange = plotrange[:len(dims)]
            elif len(plotrange)<len(dims):
                dif = len(dims)-len(plotrange)
                length = len(plotrange)
                for i in range(dif):
                    if (length+i == plotDims[0][0]) or (length+i == plotDims[1][0]):
                        plotrange.append(slice(None))
                    else:
                        plotrange.append(0)            
            for i in range(len(dims)):
                if (i==plotDims[0][0]) or (i==plotDims[1][0]):
                    if type(plotrange[i]) == int:   # plot axis should slice and else should be int.
                        plotrange[i] = slice(None)
                else:
                    if not type(plotrange[i]) == int: # if non integer is given, correct it to 0.
                        plotrange[i] = 0
                    else: 
                        n = plotrange[i] # if the given range is not within the available range, correct it.
                        plotrange[i] = int(max(0, plotrange[i]))
                        plotrange[i] = int(min(dims[i]-1, plotrange[i]))
                        if n != plotrange[i]:
                            print('Selected plotrange[%d]=%d is corrected to %d.' % (i, n, plotrange[i]))
            
        # Get data
        selectRange = tuple(plotrange)
        if not type(readout) == type(0): # check whether readout is name or number, then get data
            if readout in self.readoutnamelist:
                readout = self.readoutnamelist.index(readout)
                data = self.readouts['data'][readout,Ellipsis]
            else:
                readout = 0
                data = self.readouts['data'][0,Ellipsis]
        else:
            if readout < len(self.readoutnamelist):
                data = self.readouts['data'][readout,Ellipsis]
            else:
                readout = 0
                data = self.readouts['data'][0,Ellipsis]
        Z = data[selectRange]
        if plotDims[0][0]>plotDims[1][0]: # set x axis to first dimension
            Z = np.moveaxis(Z, 1, 0)
        labelZ = self.readoutnamelist[readout]+' ('+self.readouts['units'][readout]+')'
        
        # Get plot axis
        if mode == 'imshow':
            # Get xaxis
            X, labelX = self.getAxis(dim = plotDims[0][0],
                             axisSelec = plotDims[0][1],
                             selection = plotrange[plotDims[0][0]])
            # Get yaxis
            Y, labelY = self.getAxis(dim = plotDims[1][0],
                             axisSelec = plotDims[1][1],
                             selection = plotrange[plotDims[1][0]])
        elif mode == 'pcolormesh':
            if plotDims[0][0]==0:
                selectFastSequenceDim = True
            else:
                selectFastSequenceDim = False
            X, labelX = self.getSweepArray(selectRange=plotrange,   # range to return the sweep array
                                          selectFastSequenceDim = selectFastSequenceDim,    # get axis for fast sequence or not
                                          choice = plotDims[0][1],       # choice of the sweep array (number or name)
                                          )
            if plotDims[1][0]==0:
                selectFastSequenceDim = True
            else:
                selectFastSequenceDim = False
            Y, labelY = self.getSweepArray(selectRange=plotrange,   # range to return the sweep array
                                          selectFastSequenceDim = selectFastSequenceDim,    # get axis for fast sequence or not
                                          choice = plotDims[1][1],       # choice of the sweep array (number or name)
                                          )
        # Apply factor
        X = np.multiply(X, factors[0]) # Apply factor for x
        Y = np.multiply(Y, factors[1]) # Apply factor for y        

        if transpose:
            Z = Z.T
            T = X
            X = Y
            Y = T
            t = labelX; labelX = labelY; labelY = t
            if mode == 'pcolormesh':
                X = X.T
                Y = Y.T
            
        # Get plot limits for X, Y and Z
        if mode == 'imshow':
            xini = X[0]; xfin = X[-1];
            yini = Y[0]; yfin = Y[-1];
        elif mode == 'pcolormesh':
            xini = X[0,0]; xfin = X[-1,-1];
            yini = Y[0,0]; yfin = Y[-1,-1];
        
        if z_ax_range == []:                                                   # Obtain limits of z.
            zmin = np.min(Z.flatten()); zmax = np.max(Z.flatten())
        else:
            zmin = z_ax_range[0]; zmax = z_ax_range[1];
            
        # plot
        if mode == 'imshow':
            # imshow
            cax = ax.imshow(np.fliplr(np.flipud(Z)).T, extent=(xfin,xini,yfin,yini),origin='lower',
                      interpolation='nearest', aspect='auto', cmap=plt.get_cmap(colormap),
                      vmin=zmin, vmax=zmax)
        elif mode == 'pcolormesh':
            #pcolormesh used for plotting the vector sweep data
            cax = ax.pcolormesh(X, Y, Z, cmap=plt.get_cmap(colormap),
                      vmin=zmin, vmax=zmax)
        
        """ Add colorbar, set label and ticks """
        if showColorbar:
            cbar = fig.colorbar(cax)
            if zlabel == '':  cbar.set_label(labelZ, rotation=270, labelpad=20, fontsize = labelsize)
            else:             cbar.set_label(zlabel, rotation=270, labelpad=20, fontsize = labelsize)
            if zticks==[]:
                if z_tick_freq > 0:
                    cbar.ax.set_ticks(np.linspace(zmin,zmax,z_tick_freq))
            else:
                cbar.ax.set_ticks(zticks)
            cbar.ax.tick_params(labelsize=ticklabelsize) 
        
        """ set various plotting settings """       
        if xlabel=='':     ax.set_xlabel(labelX, fontsize=labelsize)  
        else:              ax.set_xlabel(xlabel, fontsize=labelsize)
        if ylabel=='':     ax.set_ylabel(labelY, fontsize=labelsize)
        else:              ax.set_ylabel(ylabel, fontsize=labelsize)
            
        """ set tick  and their label size """
        if xticks==[]:
            if x_tick_freq > 0:
                ax.set_xticks(np.linspace(xini,xfin,x_tick_freq))
        else:
            ax.set_xticks(xticks)
        if yticks==[]:
            if y_tick_freq > 0:
                ax.set_yticks(np.linspace(yini,yfin,y_tick_freq))
        else:
            ax.set_yticks(yticks)
        ax.tick_params(axis='both', which='major', labelsize=ticklabelsize)
        """ set axis ranges """
        if not x_ax_range == []:
            ax.set_xlim(x_ax_range[0], x_ax_range[1])
        if not y_ax_range == []:
            ax.set_ylim(y_ax_range[0], y_ax_range[1])
            
        """ Flip axes """
        if flipX:
            ax.invert_xaxis()
        
        if flipY:
            ax.invert_yaxis()
        
        if showGrid == True:     ax.grid()                                     # If chosen, show grid.
        if tight:   plt.tight_layout()
        # Image line slice
        if lineSlice:
            fig2 = plt.figure('Image slice')
            fig2.clf()
            axS = fig2.add_subplot(111)
            LnTr = LineSlice(cax, axS, Z, X, Y)
            
            
#    def save2DTiledData(self,
#                        plotaxis = [[0,0],[1,1]],
#                        readouts = [0], # number or name
#                        plotrange = [], # silce the data
#                        xdim = -1, # -1 is default and choose lowest dim except plot dimensions
#                        width = 20, # widh of each figure
#                        height = 15, # height of each figure
#                       ):
#        dshape = self.readouts['data'].shape
#        # Treat plot range
#        if plotrange == []:
#            plotrange = [slice(None)]*len(dshape[1:])
#        elif len(plotrange) > len(dshape[1:]):
#            plotrange = plotrange[0:len(dshape[1:])]
#            print('Selected range is larger than sweep dimensions.')
#        elif len(plotrange) < len(dshape[1:]):
#            dif = len(dshape[1:])-len(plotrange)
#            if not Ellipsis in plotrange:
#                plotrange += [slice(None)]*(dif)
#            else:
#                plotrange = plotrange[0:plotrange.index(Ellipsis)]+[slice(None)]*(dif)+plotrange[plotrange.index(Ellipsis)+1:]
#        for i, p in enumerate(plotrange):
#            if type(p) == int:
#                plotrange[i] = slice(p,p+1) # By replacing number to slice of 1 value, keep the data dimensions
#        # Get x dim for plotting
#        axisList = list(range(len(dshape[1:])))
#        del axisList[plotaxis[0][0]]
#        del axisList[plotaxis[1][0]]
#        if xdim == -1:
#            xdim = axisList[0]
#        else:
#            if not xdim in axisList:
#                xdim = axisList[0]
#        data = self.readouts['data'][tuple([slice(None)]+plotrange)]
#        # make tiles
#        for i, read in enumerate(readouts):
#            # convert name to number here
#            if read in self.readoutnamelist:
#                read = self.readoutnamelist.index(read)
#            else:
#                if not type(read) == int:
#                    read = i
#            data = self.readouts['data'][tuple([read]+plotrange)]
            
if __name__=='__main__':
    fname = '201612141401'
#    fname = '201702031747'
    path = '/Users/shintaro/Documents/1_Research/3_SAW/4_Data/4_Postdoc/HBT6/'
#    path = r'E:/Takada/DATA/HBT6/data2/20170202/'
    data = ExpData(filename = fname,
                   path = path,
                   )
    data.readData()
    data.plot1D(figNo=1, # Number of the figure in case ax is not given
               ax='', # ax to be plotted data
               clear = True, # clear the existing plot in the 'ax'
               useCounter=False,
               showlegend=True, showTitle=True, showGrid=True,
               title = '', # set title
               plotaxis = 0, # plot along 
               plotrange=[], # plot range ex.) [slice(0,100), slice(None), Ellipsis, 0]
               readouts = [], # select plot readout by name or number
               xaxis = 4, #0, 1, 2 or 'name' of axis
               xoffsets=[], yoffsets=[],
               xfactor=1, yfactor=1,
               xlabel='', ylabel='',
               x_axis_range = [], y_axis_range = [],
               x_tick_freq = 0, y_tick_freq = 0,
               xticks=[], yticks=[],
               ticklabelsize = 12, labelsize = 14,
               linestyles=[], linewidth = 1.0,
               markers=['P'], markersize=3,
               colors=[],
               mode = ['standard', 'vector'][1],
               )
#    data.plot2D(figNo=4,
#               fig='',                                                         # plot data to given fig
#               ax = '',                                                        # plot data into given ax
#               plotDims = [[0,0],[1,0]],                                        # plot axis [[x, choice], [y, choice]] (choice is number of 'name')
#               readout=0,                                                     # name or number of readout instrument that should be plotted on z-axis
#               plotrange= [slice(None),slice(None)],                                                    # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
#               factors = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
#               clear = True,                                                   # clear previous plot or not
#               showColorbar = True, showTitle = True, showGrid = True,
#               flipX = False, flipY = False, transpose = False,
#               xlabel = '',   ylabel = '',   zlabel = '',
#               x_ax_range=[], y_ax_range=[], z_ax_range=[],
#               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
#               xticks=[],     yticks=[],     zticks=[],
#               ticklabelsize = 12, labelsize = 14,
#               colormap = "viridis", lineSlice=False,
#               mode = ['imshow', 'pcolormesh'][1],
#               )
#    data.getGateConfig()
    pass
