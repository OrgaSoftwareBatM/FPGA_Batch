# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:45:32 2015

@author: shintaro
"""


import os
import time
import copy
import numpy as np
import platform
import h5py
import matplotlib as plt
import matplotlib.gridspec as gridspec
from DataStructure.datacontainer import *
from AnalysisBase.AnalysisFunctions import *
from MeasurementBase.measurement_classes import *
# set up the defalut figure style
plt.rc('lines', linewidth=1.5)
plt.rc('font', size=18)
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"
plt.rc('text', usetex=False)
plt.rcParams['text.latex.unicode']=False
plt.rc('axes', facecolor='white', edgecolor='black', grid=False, titlesize=18, labelsize=18)
ticklabelsize = 12
colorBarSize = 10
plt.rc('grid', color='black',linewidth=0.5,linestyle=':',alpha=0.5)
plt.rc('figure', titlesize=18)
plt.rc('savefig', format='pdf')
plt.rcParams['mathtext.fontset']='stix'
plt.rcParams['legend.fontsize']=12
# some default data type for numpy
init_param_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})

def analysis_20161218():
    h5path = 'E:/Takada/DATA/HBT6/data/'
    dataname = '201612181913'
    stddata = ExpData()
    stddata.readHDF5data2python(h5name=dataname, folderPath=h5path)
    avgdata = copy.deepcopy(stddata)
    stddata.data = np.mean(np.std(stddata.data, axis=1, keepdims=True), axis=2, keepdims=True)
    avgdata.data = np.mean(np.mean(avgdata.data, axis=1, keepdims=True),axis=2, keepdims=True)
    fig = plt.figure(figsize=(20,30))
    fig.patch.set_facecolor('#ffffff')  # figure background color
    gs = gridspec.GridSpec(7,2)
    axes = [fig.add_subplot(gs[:2,:]), fig.add_subplot(gs[2,:])]
    stddata.getGateConfig(axes=axes)
    readouts = ['sud','rud','rld','sld']
    for i in range(4):
        ax0 = fig.add_subplot(gs[3+i,0])
        stddata.plot2D(fig=fig, ax = ax0, plotDims = [[2,4+i],[3,8+i]],readout = readouts[i],
                       pranges=[0,0,Ellipsis,Ellipsis])
        ax1 = fig.add_subplot(gs[3+i,1])
        avgdata.plot2D(fig=fig, ax = ax1, plotDims = [[2,4+i],[3,8+i]],readout = readouts[i],
                       pranges=[0,0,Ellipsis,Ellipsis])
    fig.savefig('test')
    
def Analysis20161220batch():
    h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161220/'
    basename = '20161220batch_'
    
    readouts = ['sud','rud','rld','sld']
    var1_no = 5
    var1list = [['suu',-0.8,-1.2],['ruu',-0.8,-1.2],['rll',-0.8,-1.2],['sll',-0.8,-1.2]]
    var2_no = 6
    var2list = [['sul',-1.05,-1.55],['rul',-1.05,-1.55],['rlu',-1.05,-1.55],['slu',-1.05,-1.55]]
    
    counter = 0
    for i in range(len(readouts)):
#    for i in range(1):
        fig = plt.figure(figsize=(5*var1_no*len(var1list),15*var2_no), dpi=100)
        gs = gridspec.GridSpec(var2_no,var1_no)
        var1 = var1list[i]
        var2 = var2list[i]
        for j in range(var1_no):
            v1 = var1[1] + (var1[2]-var1[1])/float(var1_no-1)*j
            s1 = var1[0]+'='+str(v1)+' (V)'
            for k in range(var2_no):
                v2 = var2[1] + (var2[2]-var2[1])/float(var2_no-1)*k
                s2 = var2[0]+'='+str(v2)+' (V)'
                expdata = ExpData()
                expdata.readHDF5data2python(h5name = basename + str(counter), folderPath = h5path)
                diffdata = derivative(expdata, 5, 1)
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(basename + str(counter)+' : '+s2+','+s1)
                diffdata.plot2D(fig=fig, ax=ax, plotDims=[[0,0],[1,0]],
                                colormap='viridis',readout=readouts[i],pranges=[Ellipsis,Ellipsis]
                                )
                counter += 1
        fig.savefig(h5path+basename+str(i)+'.png')
        
def Analysis20161221batch():
    h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161221/'
    basename = '20161221batch_'
    
    readouts = ['sud','rud','rld','sld']
    var1_no = 3
    var1list = [['suu',-0.8,-0.9],['ruu',-0.8,-0.9],['rll',-0.8,-0.9],['sll',-0.8,-0.9]]
    var2_no = 4
    var2list = [['sul',-1.25,-1.35],['rul',-1.35,-1.45],['rlu',-1.35,-1.45],['slu',-1.35,-1.45]]
    
    counter = 0
    for i in range(len(readouts)):
#    for i in range(1):
        fig = plt.figure(figsize=(5*var1_no*len(var1list),15*var2_no), dpi=100)
        gs = gridspec.GridSpec(var2_no,var1_no)
        var1 = var1list[i]
        var2 = var2list[i]
        for j in range(var1_no):
            v1 = var1[1] + (var1[2]-var1[1])/float(var1_no-1)*j
            s1 = var1[0]+'='+str(v1)+' (V)'
            for k in range(var2_no):
                v2 = var2[1] + (var2[2]-var2[1])/float(var2_no-1)*k
                s2 = var2[0]+'='+str(v2)+' (V)'
                expdata = ExpData()
                expdata.readHDF5data2python(h5name = basename + str(counter), folderPath = h5path)
                diffdata = derivative(expdata, 5, 1)
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(basename + str(counter)+' : '+s2+','+s1)
                diffdata.plot2D(fig=fig, ax=ax, plotDims=[[0,0],[1,0]],
                                colormap='viridis',readout=readouts[i],pranges=[Ellipsis,Ellipsis]
                                )
                counter += 1
        fig.savefig(h5path+basename+str(i)+'.png')
        
def Analysis20161221():
    h5path = 'E:/Takada/DATA/HBT6/data/'
    fileList = ['201612211803','201612211808','201612211817','201612211820']
    
    readouts = ['sud','rud','rld','sld']
    vlist = [['sur',-1.3,-1.4,-1.5,-1.6],['rur',-1.3,-1.4,-1.5,-1.6],['rlr',-1.4,-1.5,-1.6,-1.7],['slr',-1.3,-1.4,-1.5,-1.6]]
        
    for i in range(len(readouts)):
        fig = plt.figure(figsize=(20*4,15*9), dpi=100)
        gs = gridspec.GridSpec(9,4)
        for j, name in enumerate(fileList):
            expdata = ExpData()
            expdata.readHDF5data2python(h5name=name, folderPath=h5path)
            for k in range(3):
                for l, pos in enumerate([[10,99],[17,99],[22,99]][k]):
                    ax = fig.add_subplot(gs[3*k+l, j])
                    title_str = '%s: %s=%f, position=%d, wait time=%d' % (name, vlist[i][0],vlist[i][1+j], pos, 10*(1+k))
                    ax.set_title(title_str)
                    expdata.plot2D(fig=fig,ax=ax,plotDims=[[1,i],[2,2*i+4]],colormap='viridis',
                                   readout=readouts[i],pranges=[pos,Ellipsis,Ellipsis,k],flipX = True, flipY = True)
            for k in range(3):
                positions = [[10,99],[17,99],[22,99]][k]
                expdata.data[i,0,Ellipsis,k] = expdata.data[i,positions[0],Ellipsis,k] - expdata.data[i,positions[1],Ellipsis,k]
                ax = fig.add_subplot(gs[3*k+2, j])
                title_str = '%s: %s=%f, position=%d - %d, wait time=%d' % (name, vlist[i][0],vlist[i][1+j], positions[0],positions[1], 10*(1+k))
                ax.set_title(title_str)
                expdata.plot2D(fig=fig,ax=ax,plotDims=[[1,i],[2,2*i+4]],colormap='bwr',
                               readout=readouts[i],pranges=[0,Ellipsis,Ellipsis,k],flipX = True, flipY = True, z_ax_range=[-0.8,0.8])

        fig.savefig(h5path+'20161221overnight_'+readouts[i]+'.png')
        
def Analysis20161222():
    h5path = 'E:/Takada/DATA/HBT6/data/'
    fileList = ['201612221353','201612221359','201612221400','201612221401','201612221402','201612221403','201612221403_0']
    
    readouts = ['rud','rld']
    vlist = [['rur',-1.4,-1.45,-1.5,-1.55,-1.6,-1.65,-1.7],['rlr',-1.25,-1.3,-1.35,-1.4,-1.45,-1.5,-1.55]]
        
    for i in range(len(readouts)):
        fig = plt.figure(figsize=(20*len(vlist[i][1:]),15*3), dpi=100)
        gs = gridspec.GridSpec(3,len(vlist[i][1:]))
        for j, name in enumerate(fileList):
            expdata = ExpData()
            expdata.readHDF5data2python(h5name=name, folderPath=h5path)
            for l, pos in enumerate([10,99]):
                ax = fig.add_subplot(gs[l, j])
                title_str = '%s: %s=%f, position=%d, wait time=%d' % (name, vlist[i][0],vlist[i][1+j], pos, 10)
                ax.set_title(title_str)
                expdata.plot2D(fig=fig,ax=ax,plotDims=[[1,i],[2,2*i+2]],colormap='viridis',
                               readout=readouts[i],pranges=[pos,Ellipsis,Ellipsis],flipX = True, flipY = True)
                
            positions = [10,99]
            expdata.data[i+1,0,Ellipsis] = expdata.data[i+1,positions[0],Ellipsis] - expdata.data[i+1,positions[1],Ellipsis]
            ax = fig.add_subplot(gs[2, j])
            title_str = '%s: %s=%f, position=%d - %d, wait time=%d' % (name, vlist[i][0],vlist[i][1+j], positions[0],positions[1], 10)
            ax.set_title(title_str)
            expdata.plot2D(fig=fig,ax=ax,plotDims=[[1,i],[2,2*i+2]],colormap='bwr',
                           readout=readouts[i],pranges=[0,Ellipsis,Ellipsis],flipX = True, flipY = True, z_ax_range=[-0.5,0.5])
        fig.savefig(h5path+'20161222afternoon_'+readouts[i]+'.png')
        
def Analysis20161223(): # ANALYSIS OF FAST CYCLE WITH EMPTY AND LOADING SEQUENCE -- LOADING MAP
    h5path = 'E:/Takada/DATA/HBT6/data/'
    fileList = ['201612231501','201612231303','201612231307','201612231308','201612231310','201612231311','201612231456','201612231458']
    
    readouts = ['sud','rud','rld','sld']
    vlist = [['rur',-1.40,-1.45,-1.50,-1.55,-1.60,-1.65,-1.70,-1.75,-1.80], \
             ['rur',-1.40,-1.45,-1.50,-1.55,-1.60,-1.65,-1.70,-1.75,-1.80], \
             ['rlr',-1.20,-1.25,-1.30,-1.35,-1.40,-1.45,-1.50,-1.55,-1.60], \
             ['rlr',-1.20,-1.25,-1.30,-1.35,-1.40,-1.45,-1.50,-1.55,-1.60]]
        
    for i in range(len(readouts)):
        fig = plt.figure(figsize=(20*len(vlist[i][1:]),15*3), dpi=100)
        gs = gridspec.GridSpec(3,len(vlist[i][1:]))
        for j, name in enumerate(fileList):
            expdata = ExpData()
            expdata.readHDF5data2python(h5name=name, folderPath=h5path)
            for l, pos in enumerate([10,99]):
                ax = fig.add_subplot(gs[l, j])
                title_str = '%s: %s=%f, position=%d, wait time=%d' % (name, vlist[i][0],vlist[i][1+j], pos, 10)
                ax.set_title(title_str)
                expdata.plot2D(fig=fig,ax=ax,plotDims=[[1,i],[2,2*i+2]],colormap='viridis',
                               readout=readouts[i],pranges=[pos,Ellipsis,Ellipsis],flipX = True, flipY = True)
                
            positions = [10,99]
            expdata.data[i+1,0,Ellipsis] = expdata.data[i+1,positions[0],Ellipsis] - expdata.data[i+1,positions[1],Ellipsis]
            ax = fig.add_subplot(gs[2, j])
            title_str = '%s: %s=%f, position=%d - %d, wait time=%d' % (name, vlist[i][0],vlist[i][1+j], positions[0],positions[1], 10)
            ax.set_title(title_str)
            expdata.plot2D(fig=fig,ax=ax,plotDims=[[1,i],[2,2*i+2]],colormap='bwr',
                           readout=readouts[i],pranges=[0,Ellipsis,Ellipsis],flipX = True, flipY = True, z_ax_range=[-0.5,0.5])
        fig.savefig(h5path+'20161222afternoon_'+readouts[i]+'.png')
        
def Analysis20161222batch():
    h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161222/'
    basename = '20161222batch_'
    
    readouts = ['sud','rud','rld','sld']
    var1_no = 5
    var1list = [['suu',-0.8,-0.9],['ruu',-0.8,-0.9],['rll',-0.85,-0.95],['sll',-0.8,-0.9]]
    var2_no = 9
    var2list = [['sul',-1.23,-1.33],['rul',-1.4,-1.5],['rlu',-1.33,-1.43],['slu',-1.3,-1.4]]
    
    counter = 0
    for i in range(len(readouts)):
#    for i in range(3):
        fig = plt.figure(figsize=(5*var1_no*len(var1list),15*var2_no), dpi=100)
        gs = gridspec.GridSpec(var2_no,var1_no)
        var1 = var1list[i]
        var2 = var2list[i]
        for j in range(var1_no):
            v1 = var1[1] + (var1[2]-var1[1])/float(var1_no-1)*j
            s1 = var1[0]+'='+str(v1)+' (V)'
            for k in range(var2_no):
                v2 = var2[1] + (var2[2]-var2[1])/float(var2_no-1)*k
                s2 = var2[0]+'='+str(v2)+' (V)'
                expdata = ExpData()
                counterstr = '%05d' % counter
                expdata.readHDF5data2python(h5name = basename + counterstr, folderPath = h5path)
                diffdata = derivative(expdata, 5, 1)
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(basename + str(counter)+' : '+s2+','+s1)
                diffdata.plot2D(fig=fig, ax=ax, plotDims=[[0,0],[1,0]],
                                colormap='viridis',readout=readouts[i],pranges=[Ellipsis,Ellipsis]
                                )
                counter += 1
        fig.savefig(h5path+basename+str(i)+'.png')
        
def Analysis20161228batch():
    h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161228/'
    basename = '20161228batch_'
    
    readouts = ['sud','rud','rld','sld']
    var1_no = 6
    var1list = [['suu',-0.75,-1.0],['ruu',-0.75,-1.0],['rll',-0.75,-1.0],['sll',-0.75,-1.0]]
    var2_no = 9
    var2list = [['sul',-0.75,-1.0],['rul',-0.75,-1.0],['rlu',-0.75,-1.0],['slu',-0.75,-1.0]]

    counter = 0
    for i in range(len(readouts)):
#    for i in range(3):
        fig = plt.figure(figsize=(6*var1_no*len(var1list),15*var2_no), dpi=100)
        gs = gridspec.GridSpec(var2_no,var1_no)
        var1 = var1list[i]
        var2 = var2list[i]
        for j in range(var1_no):
            v1 = var1[1] + (var1[2]-var1[1])/float(var1_no-1)*j
            s1 = var1[0]+'='+str(v1)+' (V)'
            for k in range(var2_no):
                v2 = var2[1] + (var2[2]-var2[1])/float(var2_no-1)*k
                s2 = var2[0]+'='+str(v2)+' (V)'
                expdata = ExpData()
                counterstr = '%05d' % counter
                expdata.readHDF5data2python(h5name = basename + counterstr, folderPath = h5path)
                diffdata = derivative(expdata, 5, 1)
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(basename + str(counter)+' : '+s2+','+s1)
                diffdata.plot2D(fig=fig, ax=ax, plotDims=[[0,0],[1,0]],
                                colormap='viridis',readout=readouts[i],pranges=[Ellipsis,Ellipsis]
                                )
                counter += 1
        fig.savefig(h5path+basename+str(i)+'.png')

def Analysis20161230batch():
    h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161230/'
    basename = '20161230batch_'
    
    readouts = ['sud','rud','rld','sld']
    var1_no = 16
    var1list = [['suu',-0.6,-0.75],['ruu',-0.6,-0.75],['rll',-0.6,-0.75],['sll',-0.6,-0.75]]
    var2_no = 11
    var2list = [['sul',-0.6,-0.75],['rul',-0.6,-0.75],['rlu',-0.6,-0.75],['slu',-0.6,-0.75]]

    counter = 0
    for i in range(len(readouts)):
#    for i in range(3):
        fig = plt.figure(figsize=(5*var1_no*len(var1list),15*var2_no), dpi=100)
        gs = gridspec.GridSpec(var2_no,var1_no)
        var1 = var1list[i]
        var2 = var2list[i]
        for j in range(var1_no):
            v1 = var1[1] + (var1[2]-var1[1])/float(var1_no-1)*j
            s1 = var1[0]+'='+str(v1)+' (V)'
            for k in range(var2_no):
                v2 = var2[1] + (var2[2]-var2[1])/float(var2_no-1)*k
                s2 = var2[0]+'='+str(v2)+' (V)'
                expdata = ExpData()
                counterstr = '%05d' % counter
                expdata.readHDF5data2python(h5name = basename + counterstr, folderPath = h5path)
                diffdata = derivative(expdata, 5, 1)
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(basename + str(counter)+' : '+s2+','+s1)
                diffdata.plot2D(fig=fig, ax=ax, plotDims=[[0,0],[1,0]],
                                colormap='viridis',readout=readouts[i],pranges=[Ellipsis,Ellipsis]
                                )
                counter += 1
        fig.savefig(h5path+basename+str(i)+'.png')
    
def Analysis20161225():
    h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161223/'
    basename = '20161223batch_'
    positions = [[9,12],[22,25],[46,49]]
    readouts = ['sud','rud','rld','sld']
    cvars = [['suc',-0.1,-0.3],['ruc',-0.05,-0.25],['rlc',-0.15,-0.35],['slc',-0.07,-0.27]]
    cNo = 101
    rvars = [['sur',-1.4,-1.9],['rur',-1.4,-1.9],['rlr',-1.2,-1.7],['slr',-1.2,-1.7]]
    rNo = 51
    datamap = np.empty((4,rNo,cNo,3),dtype=float)
    loadpositions = [[195,199],[195,199],[195,199],[195,199]]
        
    fig = plt.figure(figsize=(20*3,15*4), dpi=100)
    gs = gridspec.GridSpec(4, 3)
    for i in range(rNo):
        fname = basename
        fname += '%05d' % (i)
        data = AnalysisLoadMap(h5path=h5path,
                               filename = fname,
                               positions = positions,
                               plot = False,
                               saveFig = False)
        for j in range(4):
            for k in range(3):
                datamap[j,i,:,k] = np.mean(data.data[j,k,loadpositions[j][0]:loadpositions[j][1],:], axis=0)
                
    for i in range(4):
        for j in range(3):
            zmin = np.min(datamap[i,0,:,j].flatten())-0.5
            zmax = np.max(datamap[i,0,:,j].flatten())+0.5
            ax = fig.add_subplot(gs[i,j])
            xmin = cvars[i][1]
            xmax = cvars[i][2]
            ymin = rvars[i][1]
            ymax = rvars[i][1] + (rvars[i][2]-rvars[i][1])/50*rNo
            cax = ax.imshow(np.flipud(np.fliplr(datamap[i,:,:,j])),extent=(xmax,xmin,ymax,ymin),origin='lower',
                            interpolation='nearest',aspect='auto',cmap=plt.get_cmap('viridis'),
                            vmin=zmin, vmax=zmax)
            ax.set_xlabel(cvars[i][0], fontsize=24)
            ax.set_ylabel(rvars[i][0], fontsize=24)
            cbar = fig.colorbar(cax)
            cbar.set_label(readouts[i], rotation=270, labelpad=20, fontsize=24)
            cbar.ax.tick_params(labelsize=24)
            ax.tick_params(axis='both', which='major', labelsize=24)
    fig.savefig(h5path+basename+'full.png')
    
def Analysis20170102():
    h5path = 'E:/Takada/DATA/HBT6/data/20170102/'
#    basename = '201701022000'
    basename = '201701032037'
    positions = [[9,12],[22,25],[46,49]]
    readouts = ['sud','rud','rld','sld']
#    cvars = [['suc',-0.65,-0.85],['ruc',-0.7,-0.9],['rlc',-0.9,-1.1],['slc',-0.6,-0.8]]
#    cNo = 41
    rvars = [['sur',-1.5,-1.9],['rur',-1.55,-1.95],['rlr',-1.58,-1.98],['slr',-1.3,-1.7]]
    rNo = 9
    strlist = ["after init.", "after load.", "load. stability"]
#    datamap = np.empty((4,rNo,cNo,3),dtype=float)
#    loadpositions = [[56,60],[56,60],[56,60],[56,60]]
    
    expdata = ExpData()
    expdata.readHDF5data2python(h5name = basename, folderPath = h5path)
    sdata = copy.deepcopy(expdata)
    dshape = list(expdata.data.shape)
    dshape[1] = 3 # check initialization, chack loading (load - init), check stability of loading
    data = np.empty(dshape, dtype=float)
    data[:,0,Ellipsis] = np.mean(expdata.data[:,positions[0][0]:positions[0][1],Ellipsis],axis=1)
    data[:,1,Ellipsis] = np.mean(expdata.data[:,positions[1][0]:positions[1][1],Ellipsis],axis=1) - data[:,0,Ellipsis]
    data[:,2,Ellipsis] = np.mean(expdata.data[:,positions[2][0]:positions[2][1],Ellipsis],axis=1) - np.mean(expdata.data[:,positions[1][0]:positions[1][1],Ellipsis],axis=1)
    sdata.data = data
    
    for i in range(4):
        for l in range(3):
            fig = plt.figure(figsize=(20*3,15*rNo), dpi=100)
            gs = gridspec.GridSpec(rNo, 3)
            for j in range(3):
                for k in range(rNo):
                    ax = fig.add_subplot(gs[k,j])
                    ax.set_title(basename + rvars[i][0]+'='+str(rvars[i][1]+(rvars[i][2]-rvars[i][1])/float(rNo-1)*k)+', '+strlist[j])
                    sdata.plot2D(figNo=0,
                                   fig=fig,                                                        # plot data to given fig
                                   ax = ax,                                                        # plot data into given ax
                                   plotDims = [[1,i*6],[3,4+i*6]],                                 # plot axis [[x, choice], [y, choice]]
                                   readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                                   pranges= [j,Ellipsis,k,Ellipsis,l],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
    #                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                                   factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                                   clear = True,                                                   # clear previous plot or not
                                   showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = False,
                                   xlabel = '',   ylabel = '',   zlabel = '',
                                   x_ax_range=[], y_ax_range=[], z_ax_range=[],
                                   x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                                   xticks=[],     yticks=[],     zticks=[], 
                                   colormap = "viridis",
                                )
            fig.savefig(h5path+basename+readouts[i]+str(l)+'.png')
        
def Analysis20170104():
    h5path = 'E:/Takada/DATA/HBT6/data/20170102/'
#    basename = '201701022000'
    basename = '201701041947'
    positions = [[9,12],[22,25],[46,49]]
    readouts = ['sud','rud','rld','sld']
#    cvars = [['suc',-0.65,-0.85],['ruc',-0.7,-0.9],['rlc',-0.9,-1.1],['slc',-0.6,-0.8]]
#    cNo = 41
    rvars = [['sur',-1.35,-1.75],['rur',-1.45,-1.85],['rlr',-1.45,-1.85],['slr',-1.4,-1.8]]
    rNo = 9
    strlist = ["after init.", "after load.", "load. stability"]
#    datamap = np.empty((4,rNo,cNo,3),dtype=float)
#    loadpositions = [[56,60],[56,60],[56,60],[56,60]]
    
    expdata = ExpData()
    expdata.readHDF5data2python(h5name = basename, folderPath = h5path)
    sdata = copy.deepcopy(expdata)
    dshape = list(expdata.data.shape)
    dshape[1] = 3 # check initialization, chack loading (load - init), check stability of loading
    data = np.empty(dshape, dtype=float)
    data[:,0,Ellipsis] = np.mean(expdata.data[:,positions[0][0]:positions[0][1],Ellipsis],axis=1)
    data[:,1,Ellipsis] = np.mean(expdata.data[:,positions[1][0]:positions[1][1],Ellipsis],axis=1) - data[:,0,Ellipsis]
    data[:,2,Ellipsis] = np.mean(expdata.data[:,positions[2][0]:positions[2][1],Ellipsis],axis=1) - np.mean(expdata.data[:,positions[1][0]:positions[1][1],Ellipsis],axis=1)
    sdata.data = data
    
    for i in range(4):
        for l in range(3):
            fig = plt.figure(figsize=(20*3,15*rNo), dpi=100)
            gs = gridspec.GridSpec(rNo, 3)
            for j in range(3):
                for k in range(rNo):
                    ax = fig.add_subplot(gs[k,j])
                    ax.set_title(basename + rvars[i][0]+'='+str(rvars[i][1]+(rvars[i][2]-rvars[i][1])/float(rNo-1)*k)+', '+strlist[j])
                    sdata.plot2D(figNo=0,
                                   fig=fig,                                                        # plot data to given fig
                                   ax = ax,                                                        # plot data into given ax
                                   plotDims = [[1,i*6],[3,4+i*6]],                                 # plot axis [[x, choice], [y, choice]]
                                   readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                                   pranges= [j,Ellipsis,k,Ellipsis,l],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
    #                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                                   factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                                   clear = True,                                                   # clear previous plot or not
                                   showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = False,
                                   xlabel = '',   ylabel = '',   zlabel = '',
                                   x_ax_range=[], y_ax_range=[], z_ax_range=[],
                                   x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                                   xticks=[],     yticks=[],     zticks=[], 
                                   colormap = "viridis",
                                )
            fig.savefig(h5path+basename+readouts[i]+str(l)+'.png')
            
def Analysis20170105():
    h5path = 'E:/Takada/DATA/HBT6/data/20170102/'
    basenames = ['201701052058','201701052101']
    readouts = ['sud','rud','rld','sld']
    positions = [[7,7],[16,16],[20,21]]
    position_label = ['init', 'load', 'send map']
    load = ['load','no load']
    saw = ['without send','with send']
    
    load2 = ['load for send dots','no load']
    power = [22,25,28]
    
    # read all data
    sdata = []
    for i in range(len(basenames)):
        rawdata = ExpData()
        rawdata.readHDF5data2python(h5name=basenames[i],folderPath=h5path)
        dshape = list(rawdata.data.shape)
        dshape[1] = 3
        data = np.empty(dshape, dtype=float)
        data[:,0,Ellipsis] = np.mean(rawdata.data[:,positions[0][0]:positions[0][1]+1,Ellipsis],axis=1)
        data[:,1,Ellipsis] = np.mean(rawdata.data[:,positions[1][0]:positions[1][1]+1,Ellipsis],axis=1) - np.mean(rawdata.data[:,positions[0][0]:positions[0][1]+1,Ellipsis],axis=1)
        data[:,2,Ellipsis] = np.mean(rawdata.data[:,positions[2][0]:positions[2][1]+1,Ellipsis],axis=1) - np.mean(rawdata.data[:,positions[1][0]:positions[1][1]+1,Ellipsis],axis=1)
        rawdata.data = data
        sdata.append(rawdata)
        
    # Analyze "201701052058"
    fig = plt.figure(figsize=(20*len(positions)*len(load)*len(saw),15*len(readouts)), dpi=100)
    gs = gridspec.GridSpec(len(readouts),len(positions)*len(load)*len(saw))
    for i in range(len(readouts)):
        for j in range(len(positions)):
            for k in range(len(load)):
                for l in range(len(saw)):
                    ax = fig.add_subplot(gs[i, l+len(saw)*k+len(saw)*len(load)*j])
                    ax.set_title(basenames[0]+','+readouts[i]+','+position_label[j]+','+load[k]+','+saw[l])
                    sdata[0].plot2D(figNo=0,
                                   fig=fig,                                                        # plot data to given fig
                                   ax = ax,                                                        # plot data into given ax
                                   plotDims = [[1,i],[2,i+4]],                                 # plot axis [[x, choice], [y, choice]]
                                   readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                                   pranges= [j,Ellipsis,Ellipsis,k,l],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
    #                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                                   factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                                   clear = True,                                                   # clear previous plot or not
                                   showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                                   xlabel = '',   ylabel = '',   zlabel = '',
                                   x_ax_range=[], y_ax_range=[], z_ax_range=[],
                                   x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                                   xticks=[],     yticks=[],     zticks=[], 
                                   colormap = "viridis",
                                   )
    fig.savefig(h5path+basenames[0]+'.png')
    
    # Analyze "201701052101"
    fig = plt.figure(figsize=(20*len(positions)*len(load2)*len(power),15*len(readouts)), dpi=100)
    gs = gridspec.GridSpec(len(readouts),len(positions)*len(load2)*len(power))
    for i in range(len(readouts)):
        for j in range(len(positions)):
            for l in range(len(power)):
                for k in range(len(load2)):
                    ax = fig.add_subplot(gs[i, l+len(power)*k+len(power)*len(load2)*j])
                    ax.set_title(basenames[1]+','+readouts[i]+','+position_label[j]+','+load2[k]+','+str(power[l])+' dBm')
                    sdata[1].plot2D(figNo=0,
                                   fig=fig,                                                        # plot data to given fig
                                   ax = ax,                                                        # plot data into given ax
                                   plotDims = [[1,i],[2,i+4]],                                 # plot axis [[x, choice], [y, choice]]
                                   readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                                   pranges= [j,Ellipsis,Ellipsis,k,l],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
    #                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                                   factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                                   clear = True,                                                   # clear previous plot or not
                                   showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                                   xlabel = '',   ylabel = '',   zlabel = '',
                                   x_ax_range=[], y_ax_range=[], z_ax_range=[],
                                   x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                                   xticks=[],     yticks=[],     zticks=[], 
                                   colormap = "viridis",
                                   )
    fig.savefig(h5path+basenames[1]+'.png')
    
    # subtract background QPC fluctuations with sending movements
    sdata[0].data[:,2,:,:,0,:] = sdata[0].data[:,2,:,:,0,:]-sdata[0].data[:,2,:,:,1,:]
    fig = plt.figure(figsize=(20*len(saw),15*len(readouts)), dpi=100)
    gs = gridspec.GridSpec(len(readouts),len(saw))
    for i in range(len(readouts)):
        for l in range(len(saw)):
            ax = fig.add_subplot(gs[i,l])
            ax.set_title(basenames[0]+','+readouts[i]+',send map with no load subtraction,'+saw[l])
            sdata[0].plot2D(figNo=0,
                           fig=fig,                                                        # plot data to given fig
                           ax = ax,                                                        # plot data into given ax
                           plotDims = [[1,i],[2,i+4]],                                 # plot axis [[x, choice], [y, choice]]
                           readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                           pranges= [2,Ellipsis,Ellipsis,0,l],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
#                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                           factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                           clear = True,                                                   # clear previous plot or not
                           showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                           xlabel = '',   ylabel = '',   zlabel = '',
                           x_ax_range=[], y_ax_range=[], z_ax_range=[],
                           x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                           xticks=[],     yticks=[],     zticks=[], 
                           colormap = "viridis",
                           )
    fig.savefig(h5path+basenames[0]+'_subtraction.png')
    
    sdata[1].data[:,2,:,:,0,:] = sdata[1].data[:,2,:,:,0,:]-sdata[1].data[:,2,:,:,1,:]
    fig = plt.figure(figsize=(20*len(power),15*len(readouts)), dpi=100)
    gs = gridspec.GridSpec(len(readouts),len(power))
    for i in range(len(readouts)):
        for l in range(len(power)):
            ax = fig.add_subplot(gs[i,l])
            ax.set_title(basenames[1]+','+readouts[i]+',send map with no load subtraction,'+str(power[l])+' dBm')
            sdata[1].plot2D(figNo=0,
                           fig=fig,                                                        # plot data to given fig
                           ax = ax,                                                        # plot data into given ax
                           plotDims = [[1,i],[2,i+4]],                                 # plot axis [[x, choice], [y, choice]]
                           readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                           pranges= [2,Ellipsis,Ellipsis,0,l],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
#                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                           factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                           clear = True,                                                   # clear previous plot or not
                           showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                           xlabel = '',   ylabel = '',   zlabel = '',
                           x_ax_range=[], y_ax_range=[], z_ax_range=[],
                           x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                           xticks=[],     yticks=[],     zticks=[], 
                           colormap = "viridis",
                           )
    fig.savefig(h5path+basenames[1]+'_subtraction.png')
    
def Analysis20170106():
    h5path = 'E:/Takada/DATA/HBT6/data/20170106/'
    basename = '201701061554_0'
    readouts = ['sud','rud','rld','sld']
    positions = [[10,12],[23,26]]
    position_label = ['init', 'load', 'load - init']
    rgates = [-1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=basename,folderPath=h5path)
    dshape = list(rawdata.data.shape)
    dshape[1] = 3
    data = np.empty(dshape, dtype=float)
    data[:,0,Ellipsis] = np.mean(rawdata.data[:,positions[0][0]:positions[0][1]+1,Ellipsis],axis=1)
    data[:,1,Ellipsis] = np.mean(rawdata.data[:,positions[1][0]:positions[1][1]+1,Ellipsis],axis=1)
    data[:,2,Ellipsis] = data[:,1,Ellipsis] - data[:,0,Ellipsis]
    rawdata.data = data
    
    for i, readout in enumerate(readouts):
        fig = plt.figure(figsize=(20*len(position_label), 15*len(rgates)), dpi=100)
        gs = gridspec.GridSpec(len(rgates),len(position_label))
        for j in range(len(rgates)):
            for k in range(len(position_label)):
                ax = fig.add_subplot(gs[j,k])
                ax.set_title(basename + ': '+readout+', '+ position_label[k]+', '+readout[:-1]+'r = '+str(rgates[j])+' V')
                rawdata.plot2D(figNo=0,
                           fig=fig,                                                        # plot data to given fig
                           ax = ax,                                                        # plot data into given ax
                           plotDims = [[1,5*i],[2,1+5*i]],                                 # plot axis [[x, choice], [y, choice]]
                           readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                           pranges= [k,Ellipsis,Ellipsis,j],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
#                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                           factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                           clear = True,                                                   # clear previous plot or not
                           showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = True,
                           xlabel = '',   ylabel = '',   zlabel = '',
                           x_ax_range=[], y_ax_range=[], z_ax_range=[],
                           x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                           xticks=[],     yticks=[],     zticks=[], 
                           colormap = "viridis",
                           )
        fig.savefig(h5path+basename+'_'+readout+'.png')
        
def Analysis20170106B():
    h5path = 'E:/Takada/DATA/HBT6/data/20170106/'
    basename = '201701062057'
    readouts = ['sud','rud','rld','sld']
    variance_range = [12,19]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=basename,folderPath=h5path)
    rawdata = derivative(rawdata, 0, 0)
    rawdata = varianceData(rawdata, 0, initial = variance_range[0], final = variance_range[1])
    rawdata = averagingData(rawdata, 1, initial=0, final=0)
    
    dshape = list(rawdata.data.shape)
    cgate_range = [np.linspace(-0.6,-0.4,dshape[5]),np.linspace(-0.6,-0.4,dshape[5]),np.linspace(-0.77,-0.57,dshape[5]),np.linspace(-0.65,-0.45,dshape[5])]
    dshape[5] = 11
    
    fig = plt.figure(figsize=(20*len(readouts), 15*dshape[5]), dpi=100)
    gs = gridspec.GridSpec(dshape[5], len(readouts))
    for i, readout in enumerate(readouts):
        for j in range(dshape[5]):
            ax = fig.add_subplot(gs[j,i])
            cstr = 'c = %2.4f V' % (cgate_range[i][j]) 
            ax.set_title(basename + ': '+readout+', '+readout[:-1]+cstr)
            rawdata.plot2D(figNo=0,
                           fig=fig,                                                        # plot data to given fig
                           ax = ax,                                                        # plot data into given ax
                           plotDims = [[1,6*i],[2,1+6*i]],                                 # plot axis [[x, choice], [y, choice]]
                           readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                           pranges= [0,0,Ellipsis,Ellipsis,j],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
#                               pranges= [j,Ellipsis,k,Ellipsis],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                           factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                           clear = True,                                                   # clear previous plot or not
                           showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = True,
                           xlabel = '',   ylabel = '',   zlabel = '',
                           x_ax_range=[], y_ax_range=[], z_ax_range=[],
                           x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                           xticks=[],     yticks=[],     zticks=[], 
                           colormap = "viridis",
                           )
    fig.savefig(h5path+basename+'.png')
    
def Analysis20170107():
    h5path = 'E:/Takada/DATA/HBT6/data/20170106/'
    basename = '201701072134B'
    readouts = ['sud','rud','rld','sld']
    analysis_range = [10,13,25,30]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=basename,folderPath=h5path)
    rawdata = sendingMap(rawdata, analysis_range[0], analysis_range[1], analysis_range[2], analysis_range[3])
    
    dshape = list(rawdata.data.shape)
    rgate_range = [np.linspace(-1.35,-1.85,dshape[4]),np.linspace(-1.45,-1.95,dshape[4]),np.linspace(-1.4,-1.9,dshape[4]),np.linspace(-1.3,-1.8,dshape[4])]
    cgate_range = [np.linspace(-0.45,-0.3,dshape[5]),np.linspace(-0.45,-0.3,dshape[5]),np.linspace(-0.6,-0.45,dshape[5]),np.linspace(-0.5,-0.35,dshape[5])]
    
    for i, readout in enumerate(readouts):
        fig = plt.figure(figsize=(20*dshape[5], 15*dshape[4]), dpi=100)
        gs = gridspec.GridSpec(dshape[4], dshape[5])
        for j in range(dshape[4]):
            for k in range(dshape[5]):
                ax = fig.add_subplot(gs[j,k])
                rstr = 'r = %2.4f V' % (rgate_range[i][j])
                cstr = 'c = %2.4f V' % (cgate_range[i][k])
                ax.set_title(basename + ': '+readout+', '+readout[:-1]+rstr+', '+readout[:-1]+cstr)
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,7*i],[2,1+7*i]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [0,Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = True,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
        fig.savefig(h5path+basename+'_'+readout+'.png')
        
def Analysis20170108():
    h5path = 'E:/Takada/DATA/HBT6/data/20170106/'
    basename = '201701081211'
    readouts = ['sud','rud','rld','sld']
    analysis_range = [10,13,25,30]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=basename,folderPath=h5path)
    rawdata = sendingMap(rawdata, analysis_range[0], analysis_range[1], analysis_range[2], analysis_range[3])
    
    dshape = list(rawdata.data.shape)
    rgate_range = [np.linspace(-1.5,-1.6,dshape[4]),np.linspace(-1.6,-1.7,dshape[4]),np.linspace(-1.55,-1.65,dshape[4]),np.linspace(-1.47,-1.57,dshape[4])]
    cgate_range = [np.linspace(-0.45,-0.3,dshape[5]),np.linspace(-0.45,-0.3,dshape[5]),np.linspace(-0.57,-0.42,dshape[5]),np.linspace(-0.5,-0.35,dshape[5])]
    
    for i, readout in enumerate(readouts):
        fig = plt.figure(figsize=(20*dshape[5], 15*dshape[4]), dpi=100)
        gs = gridspec.GridSpec(dshape[4], dshape[5])
        for j in range(dshape[4]):
            for k in range(dshape[5]):
                ax = fig.add_subplot(gs[j,k])
                rstr = 'r = %2.4f V' % (rgate_range[i][j])
                cstr = 'c = %2.4f V' % (cgate_range[i][k])
                ax.set_title(basename + ': '+readout+', '+readout[:-1]+rstr+', '+readout[:-1]+cstr)
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,7*i],[2,1+7*i]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [0,Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = True,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
        fig.savefig(h5path+basename+'_'+readout+'.png')
        
def Analysis20170108B():
    h5path = 'E:/Takada/DATA/HBT6/data/20170106/'
    basename = '201701082047'
    readouts = ['sud','rud','rld','sld']
    analysis_range = [25,26,32,34]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=basename,folderPath=h5path)
    rawdata = sendingMap(rawdata, analysis_range[0], analysis_range[1], analysis_range[2], analysis_range[3])
    
    dshape = list(rawdata.data.shape)
    fig = plt.figure(figsize=(20*dshape[4]*len(readouts), 15*dshape[5]), dpi=100)
    gs = gridspec.GridSpec(dshape[5], dshape[4]*len(readouts))
    
    for i, readout in enumerate(readouts):
        for j in range(dshape[4]):
            for k in range(dshape[5]):
                ax = fig.add_subplot(gs[k,j+i*dshape[4]])
                ax.set_title(basename + ': '+readout+', '+['no load, ', 'load, '][j]+str(np.linspace(0,30,11)[k])+' dBm')
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,i],[2,4+i]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [0,Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
    fig.savefig(h5path+basename+'.pdf')
    
def Analysis20170109():
    h5path = 'E:/Takada/DATA/HBT6/data/20170106/'
    basename = '201701091942'
    readouts = ['sud','rud','rld','sld']
    analysis_range = [25,26,32,34]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=basename,folderPath=h5path)
    rawdata = sendingMap(rawdata, analysis_range[0], analysis_range[1], analysis_range[2], analysis_range[3])
    
    dshape = list(rawdata.data.shape)
    row = dshape[4]
    col = dshape[5]
    
    rgate_range = [np.linspace(-1.7,-1.4,row),np.linspace(-1.7,-1.4,row),np.linspace(-1.7,-1.4,row),np.linspace(-1.7,-1.4,row)]
    cgate_range = [np.linspace(-0.4,-0.1,col),np.linspace(-0.4,-0.1,col),np.linspace(-0.55,-0.25,col),np.linspace(-0.45,-0.15,col)]
    
    for i, readout in enumerate(readouts):
        fig = plt.figure(figsize=(20*col, 15*row), dpi=100)
        gs = gridspec.GridSpec(row, col)
        for j in range(row):
            for k in range(col):
                ax = fig.add_subplot(gs[j,k])
                rstr = 'r = %2.4f V' % (rgate_range[i][j])
                cstr = 'c = %2.4f V' % (cgate_range[i][k])
                ax.set_title(basename + ': '+readout+', '+readout[:-1]+rstr+', '+readout[:-1]+cstr)
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,i*9],[2,1+i*9]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readouts[i],                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [0,Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
        fig.savefig(h5path+basename+'_'+readout+'.png')
 
def Analysis20170119():       
#def Analysis20170116():
#def Analysis20170115():
    h5path = 'E:/Takada/DATA/HBT6/data2/20170113/'
    filenames = ['201701191842','201701191844','201701191846','201701191847']
#    filenames = ['201701162029','201701162032','201701162035','201701162039']
#    filenames = ['201701151930','201701151934']
    
    readouts = ['sud','rud','rld','sld']
    var2_no = 11
#    var2list = [['sul',-1.1,-1.3],['rul',-1.1,-1.3],['rlu',-1.1,-1.3],['slu',-1.1,-1.3]]
    var2list = [['suu',-0.7,-1.1],['ruu',-0.7,-1.1],['rll',-0.7,-1.1],['sll',-0.7,-1.1]]
    
    fig = plt.figure(figsize=(20*len(readouts),15*var2_no), dpi=100)
    gs = gridspec.GridSpec(var2_no,len(readouts))
    for i, fname in enumerate(filenames):
        data = ExpData()
        data.readHDF5data2python(h5name=fname,folderPath=h5path)
        data = derivative(data, 5, 1)
        for j in range(var2_no):
            ax = fig.add_subplot(gs[j,i])
            ax.set_title(fname+' pulse gate = -0.3 V, '+var2list[i][0]+'='+str(var2list[i][1]+(var2list[i][2]-var2list[i][1])*j/float(var2_no-1))+' V')
#            ax.set_title(fname+' pulse gate = -0.2 V, '+var2list[i][0]+'='+str(var2list[i][1]+(var2list[i][2]-var2list[i][1])*j/float(var2_no-1))+' V')
            data.plot2D(fig=fig, ax=ax, plotDims=[[0,0],[1,0]],
                                colormap='viridis',readout=readouts[i],pranges=[Ellipsis,Ellipsis,j]
                                )
    fig.savefig(h5path+'20170119_overnight'+'.png')
    
def Analysis20170124():       
    h5path = 'E:/Takada/DATA/HBT6/data2/20170120/'
    filename = '201701242247'
    
    readouts = ['rld','sld']
    
    analysis_range = [25,26,32,34]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=filename,folderPath=h5path)
    rawdata = sendingMap(rawdata, analysis_range[0], analysis_range[1], analysis_range[2], analysis_range[3])
    
    dshape = list(rawdata.data.shape)
    
    for i, readout in enumerate(readouts):
#        print(readout)
        fig = plt.figure(figsize=(20*dshape[4], 15*dshape[5]), dpi=100)
        gs = gridspec.GridSpec(dshape[5], dshape[4])
        for j in range(dshape[4]):
            for k in range(dshape[5]):
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(filename + ': '+readout+', '+'lrfSend = '+str(-0.05*j)+' V, rluSend = '+str(-0.2+0.05*k)+' V')
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,0],[2,1]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readout,                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [0,Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
        fig.savefig(h5path+filename+'_'+readout+'.png')
        
def Analysis20170125():       
    h5path = 'E:/Takada/DATA/HBT6/data2/20170120/'
    filename = '201701251955_0'
    
    readouts = ['rld','sld']
    
    analysis_range = [25,26,32,34]
    
    rawdata = ExpData()
    rawdata.readHDF5data2python(h5name=filename,folderPath=h5path)
    rawdata = sendingMap(rawdata, analysis_range[0], analysis_range[1], analysis_range[2], analysis_range[3])
    
    dshape = list(rawdata.data.shape)
    
    for i, readout in enumerate(readouts):
#        print(readout)
        fig = plt.figure(figsize=(20*dshape[2], 15*dshape[3]), dpi=100)
        gs = gridspec.GridSpec(dshape[3], dshape[2])
        for j in range(dshape[2]):
            for k in range(dshape[3]):
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(filename + ': '+readout+', '+'rluSend = '+str(0.5-0.05*j)+' V, tSend = '+str(0.45-0.05*k)+' V')
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,2],[2,3]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readout,                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [0,j,k,Ellipsis,slice(0,47)],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
                print j,k
        fig.savefig(h5path+filename+'_'+readout+'.png')
    
def Analysis20170126():       
    h5path = 'E:/Takada/DATA/HBT6/data2/20170120/'
    filenames = ['201701261959','201701262000']
    
    readouts = ['sld','rld']
    
    
    for i, readout in enumerate(readouts):
        rawdata = ExpData()
        rawdata.readHDF5data2python(h5name=filenames[i],folderPath=h5path)
        rawdata = derivative(rawdata, 5, 1)
        # get average and variance to get nice plotting range
        avgdata = averagingData(rawdata, 0, initial=100, final=300)
        avgdata = averagingData(avgdata, 1, initial=50, final=90)
        vardata = varianceData(rawdata, 0, initial=100, final=300)
        vardata = averagingData(vardata, 1, initial=50, final=90)
#        print(rawdata.data.shape, avgdata.data.shape, vardata.data.shape)
        
        dshape = list(rawdata.data.shape)
#        print(readout)
#        dshape[3]=1;dshape[4]=1
        fig = plt.figure(figsize=(20*dshape[3], 15*dshape[4]), dpi=100)
        gs = gridspec.GridSpec(dshape[4], dshape[3])
        for j in range(dshape[3]):
            for k in range(dshape[4]):
                zmin = avgdata.data[3-i,0,0,j,k] - 150 * vardata.data[3-i,0,0,j,k]
                zmax = avgdata.data[3-i,0,0,j,k] + 150 * vardata.data[3-i,0,0,j,k]
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(filenames[i] + ': '+readout+', '+['s','r'][i]+'ll = '+str(-0.85-0.05*j)+' V,' +['s','r'][i]+ 'lu = '+str(-1.0-0.05*k)+' V')
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[0,0],[1,1]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readout,                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[zmin, zmax],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
        fig.savefig(h5path+filenames[i]+'_'+readout+'.png')
        
def Analysis20170127():       
    h5path = 'E:/Takada/DATA/HBT6/data2/20170127/'
    filenames = ['201701271950','201701271955']
    
    readouts = ['rld','sld']
    
    
    for i, readout in enumerate(readouts):
        rawdata = ExpData()
        rawdata.readHDF5data2python(h5name=filenames[i],folderPath=h5path)
        rawdata = derivative(rawdata, 5, 1)
        # get average and variance to get nice plotting range
        avgdata = averagingData(rawdata, 0, initial=100, final=300)
        avgdata = averagingData(avgdata, 1, initial=50, final=90)
        vardata = varianceData(rawdata, 0, initial=100, final=300)
        vardata = averagingData(vardata, 1, initial=50, final=90)
#        print(rawdata.data.shape, avgdata.data.shape, vardata.data.shape)
        
        dshape = list(rawdata.data.shape)
#        print(readout)
#        dshape[3]=1;dshape[4]=1
        fig = plt.figure(figsize=(20*dshape[3], 15*dshape[4]), dpi=100)
        gs = gridspec.GridSpec(dshape[4], dshape[3])
        for j in range(dshape[3]):
            for k in range(dshape[4]):
                zmin = avgdata.data[3-i,0,0,j,k] - 150 * vardata.data[3-i,0,0,j,k]
                zmax = avgdata.data[3-i,0,0,j,k] + 150 * vardata.data[3-i,0,0,j,k]
                ax = fig.add_subplot(gs[k,j])
                ax.set_title(filenames[i] + ': '+readout+', '+'lrf = '+str(-0.0-0.05*j)+' V,' +' t = '+str(-1.0-0.05*k)+' V')
                rawdata.plot2D(figNo=0,
                               fig=fig,                                                        # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[0,0],[1,1]],                                 # plot axis [[x, choice], [y, choice]]
                               readout=readout,                                            # name of readout instrument that should be plotted on z-axis
                               pranges= [Ellipsis,Ellipsis,j,k],                             # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = False, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[zmin, zmax],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                               )
        fig.savefig(h5path+filenames[i]+'_'+readout+'.png')
    
def AnalysisLoadMap(h5path = 'E:/Takada/DATA/HBT6/data/Batch/20161223/',
                    filename = '201701021256',
                    positions = [[9,12],[22,25],[46,49]],
                    plot = True,
                    saveFig = True,
                    ):
    readouts = ['sud','rud','rld','sld']
    
    expdata = ExpData()
    expdata.readHDF5data2python(h5name = filename, folderPath = h5path)
    sdata = copy.deepcopy(expdata)
    dshape = list(expdata.data.shape)
    dshape[1] = 3 # check initialization, chack loading (load - init), check stability of loading
    smapdata = np.empty(dshape, dtype=float)
    smapdata[:,0,Ellipsis] = np.mean(expdata.data[:,positions[0][0]:positions[0][1],Ellipsis],axis=1)
    smapdata[:,1,Ellipsis] = np.mean(expdata.data[:,positions[1][0]:positions[1][1],Ellipsis],axis=1) - smapdata[:,0,Ellipsis]
    smapdata[:,2,Ellipsis] = np.mean(expdata.data[:,positions[2][0]:positions[2][1],Ellipsis],axis=1) - np.mean(expdata.data[:,positions[1][0]:positions[1][1],Ellipsis],axis=1)
    sdata.data = smapdata
    note = 'Load position analysis: check initialization, chack loading (load - init), check stability of loading. '
    note += 'analyzed range: '
    for item in positions:
        note += '%d ~ %d, ' % (item[0], item[1])
    sdata.comments += note
    if plot:
        fig = plt.figure(figsize=(20*3,15*4), dpi=100)
        gs = gridspec.GridSpec(4, 3)
        for i in range(4):
            for j in range(3):
                ax = fig.add_subplot(gs[i,j])
                sdata.plot2D(figNo=0,
                               fig=fig,                                                         # plot data to given fig
                               ax = ax,                                                        # plot data into given ax
                               plotDims = [[1,i*5],[2,1+i*5]],                                        # plot axis [[x, choice], [y, choice]]
                               readout=readouts[i],                                                     # name of readout instrument that should be plotted on z-axis
                               pranges= [j,Ellipsis,Ellipsis],                                                    # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factor = [1.0,1.0,1.0],                                         # scaling factor for x, y and z
                               clear = True,                                                   # clear previous plot or not
                               showColorbar = True, showTitle = True, showGrid = True, flipX = True, flipY = False,
                               xlabel = '',   ylabel = '',   zlabel = '',
                               x_ax_range=[], y_ax_range=[], z_ax_range=[],
                               x_tick_freq=0, y_tick_freq=0, z_tick_freq=0,
                               xticks=[],     yticks=[],     zticks=[], 
                               colormap = "viridis",
                            )
        if saveFig:
            fig.savefig(h5path+filename+'.png')
    return sdata
    
def qpcAnalysisForStabilityDiagram(dataname = '201612302024',
                h5path = 'E:/Takada/DATA/HBT6/data/',
                saveFolder = 'E:/Takada/DATA/HBT6/data/Batch/20161230/',
                outputBaseName = '20161230batch_',
                saveFolderFile = '\\\\10.0.0.7\\takada2\\DATA\\HBT6\\data\\Batch\\20161230\\',
                configBasePath = '\\\\10.0.0.7\\takada2\\DATA\\HBT6\\data\\Configs\\',
                configFiles = ['conf_20161230_ramp_sur_-400.h5','conf_20161230_ramp_rur_-400.h5','conf_20161230_ramp_rlr_-400.h5','conf_20161230_ramp_slr_-400.h5'],
                comments = 'sus:50 ohm / 50 kohm, rus: 50 ohm / 50 kohm, rls: 10 ohm / 10 kohm, rls: 50 ohm / 10 kohm, suo,lo,slo,ro,rlo,ruo: GND',
                dim = 201,
                qpcTargets = [['suq',9.5], ['ruq',10.0], ['rlq',12.0], ['slq',9.0]], # [name, target qpc current value]
                sweepVars = [['sur',-1.25],['rur',-1.30],['rlr',-1.4],['slr',-1.45]], # [name, base position]
                stepVars = [['suc',-0.6,-1.0],['ruc',-0.65,-1.05],['rlc',-0.85,-1.25],['slc',-0.5,-0.9]], # [name, initial, final]
                var1_no = 16,
                var1 = [['suu',-0.60,-0.75,-0.888,-0.5],['ruu',-0.60,-0.75,-0.666,-0.666],['rll',-0.60,-0.75,-1.111,-0.8333],['sll',-0.60,-0.75,-1.777,-0.0]], # [name, initial, final, rate for sweep, rate for step]
                var2_no = 11,
                var2 = [['sul',-0.60,-0.75,-0.444,-0.5],['rul',-0.60,-0.75,-0.333,-0.666],['rlu',-0.60,-0.75,-0.555,-0.8333],['slu',-0.60,-0.75,-0.888,-0.0]], # [name, initial, final, rate for sweep, rate for step]
                ):
#    h5path = '/Users/shintaro/Documents/1_Research/3_SAW/4_Data/4_Postdoc/HBT6/'
#    configBasePath = '/Users/shintaro/Documents/1_Research/3_SAW/4_Data/4_Postdoc/HBT6/Config/'

    expdata = ExpData()
    expdata.readHDF5data2python(h5name=dataname, folderPath=h5path)
    
    X = []
    xpoints = expdata.dim[0]
    with h5py.File(expdata.saveFolder+expdata.filename+'.h5', 'r') as f:
        for item in qpcTargets:
            name = item[0]
            X.append([np.array(f[name][...]).flatten()[0], (np.array(f[name][...]).flatten()[-1]-np.array(f[name][...]).flatten()[0])/(xpoints-1)])
    
    pdatas = []
    for i, item in enumerate(qpcTargets):
        var = item[1]
        pdata = np.argmin(np.flipud(np.absolute(expdata.data[i,Ellipsis]-var)), axis=0)
        pdata = X[i][0]+X[i][1]*(xpoints-pdata)
        pdatas.append(pdata)
    
    # get conefficient to calculate the qpc current
    coefs = []
    basePos = []
    with h5py.File(h5path+dataname+'.h5', 'r') as f:
        l = []
        bp = []
        for i, var in enumerate(sweepVars):
            dset = f[var[0]]
            sdim = dset.attrs['dimension']
            pdata = np.moveaxis(pdatas[i], sdim-2, 0).reshape((2,-1), order='F')
            xdata = np.array(dset[...])
            xi = xdata.flatten()[0]
            xl = xdata.flatten()[-1]
            a = np.mean((pdata[0,Ellipsis]-pdata[1,Ellipsis])/(xi-xl))
            l.append(a)
            bp.append(xi)
        coefs.append(l)
        basePos.append(bp)
            
        l = []
        bp = []
        for i, var in enumerate(stepVars):
            dset = f[var[0]]
            sdim = dset.attrs['dimension']
            pdata = np.moveaxis(pdatas[i], sdim-2, 0).reshape((2,-1), order='F')
            xdata = np.array(dset[...])
            xi = xdata.flatten()[0]
            xl = xdata.flatten()[-1]
            a = np.mean((pdata[0,Ellipsis]-pdata[1,Ellipsis])/(xi-xl))
            l.append(a)
            bp.append(xi)
        coefs.append(l)
        basePos.append(bp)
            
        l = []
        bp = []
        for i, var in enumerate(var1):
            dset = f[var[0]]
            sdim = dset.attrs['dimension']
            pdata = np.moveaxis(pdatas[i], sdim-2, 0).reshape((2,-1), order='F')
            xdata = np.array(dset[...])
            xi = xdata.flatten()[0]
            xl = xdata.flatten()[-1]
            a = np.mean((pdata[0,Ellipsis]-pdata[1,Ellipsis])/(xi-xl))
            l.append(a)
            bp.append(xi)
        coefs.append(l)
        basePos.append(bp)
            
        l = []
        bp = []
        for i, var in enumerate(var2):
            dset = f[var[0]]
            sdim = dset.attrs['dimension']
            pdata = np.moveaxis(pdatas[i], sdim-2, 0).reshape((2,-1), order='F')
            xdata = np.array(dset[...])
            xi = xdata.flatten()[0]
            xl = xdata.flatten()[-1]
            a = np.mean((pdata[0,Ellipsis]-pdata[1,Ellipsis])/(xi-xl))
            l.append(a)
            bp.append(xi)
        coefs.append(l)
        basePos.append(bp)
        
        
    base = [i[0,0,0,0] for i in pdatas]
                
    counter = 0
    for i in range(len(qpcTargets)):
        qpc = qpcTargets[i]
        sweep = sweepVars[i]
        step = stepVars[i]
        v1 = var1[i]
        v2 = var2[i]
        for j in range(var1_no):
            for k in range(var2_no):
                ex = Experiment()
                ex.sweeplist = []
                ex.comments = comments
                ex.dim = [dim]
                counterstr = '%05d' % counter
                ex.filename = outputBaseName + counterstr
                ex.configFile = configBasePath + configFiles[i]
                ex.saveFolder = saveFolderFile
                # make initial move
                init_move = []
                # var1
                if var1_no > 1:
                    name = v1[0]
                    parameter = 0
                    value1 = v1[1] + (v1[2]-v1[1])/(var1_no - 1)*j
                    init_move.append((name, parameter, value1))
                    delta1 = (v1[2]-v1[1])/(var1_no - 1)*j
                else:
                    delta1 = 0
                # var2
                if var2_no > 1:
                    name = v2[0]
                    parameter = 0
                    value2 = v2[1] + (v2[2]-v2[1])/(var2_no - 1)*k
                    init_move.append((name, parameter, value2))
                    delta2 = (v2[2]-v2[1])/(var2_no - 1)*k
                else:
                    delta2 = 0
                # sweep
                name = sweep[0]
                parameter = 0
                value = sweep[1]+delta1*v1[3]+delta2*v2[3]
                init_move.append((name, parameter, value))
                
                ex.Initial_move = np.array(init_move, dtype=init_param_dt)
                # step
                ss = single_sweep(name = step[0], sweep_dim = 1)
                y0 = step[1]+delta1*v1[4]+delta2*v2[4]
                y1 = step[2]+delta1*v1[4]+delta2*v2[4]
                ss.array = np.linspace(y0,y1,num=dim)
                ex.sweeplist.append(ss)
                # qpc step
                ss = single_sweep(name = qpc[0], sweep_dim = 1)
#                z0 = base[i]+coefs[0][i][2]*value+coefs[1][i][2]*y0+coefs[2][i][2]*value1+coefs[3][i][2]*value2
                z0 = base[i]+coefs[0][i]*(value-basePos[0][i])+coefs[1][i]*(y0-basePos[1][i])+coefs[2][i]*(value1-basePos[2][i])+coefs[3][i]*(value2-basePos[3][i])
                z0 = min(z0, -0.4)
                z0 = max(z0, -2.5)
#                z1 = base[i]+coefs[0][i][2]*value+coefs[1][i][2]*y1+coefs[2][i][2]*value1+coefs[3][i][2]*value2
                z1 = base[i]+coefs[0][i]*(value-basePos[0][i])+coefs[1][i]*(y1-basePos[1][i])+coefs[2][i]*(value1-basePos[2][i])+coefs[3][i]*(value2-basePos[3][i])
                z1 = min(z1, -0.4)
                z1 = max(z1, -2.5)
                ss.array = np.linspace(z0,z1,num=dim)
                ex.sweeplist.append(ss)
                ex.write(fpath=saveFolder+ex.filename+'.h5')
                counter +=1
                
def qpcAnalysisForLoading(dataname = '201612231648',
                h5path = 'E:/Takada/DATA/HBT6/data/',
                saveFolder = 'E:/Takada/DATA/HBT6/data/Batch/20161223/',
                outputBaseName = '20161223batch_',
                saveFolderFile = '\\\\10.0.0.7\\takada2\\DATA\\HBT6\\data\\Batch\\20161223\\',
                configBasePath = '\\\\10.0.0.7\\takada2\\DATA\\HBT6\\data\\Configs\\',
                configFiles = 'conf_20161223_fc_sendmap.h5',
                comments = 'sus:50 ohm / 50 kohm, rus: 50 ohm / 50 kohm, rls: 10 ohm / 10 kohm, rls: 50 ohm / 10 kohm, suo,lo,slo,ro,rlo,ruo: GND',
                qpcTargets = [['suq',10.0], ['ruq',10.0], ['rlq',7.0], ['slq',8.0]], # [name, target qpc current value]
                load_count = 201,
                load = [['su_load',0.2, 0.4],['ru_load',0.1, 0.3],['rl_load',0.0, 0.2],['sl_load',0.1, 0.3]], # [name, initial, final]
                rStep = 51,
                rVars = [['sur',-1.4,-1.9],['rur',-1.4,-1.9],['rlr',-1.2,-1.7],['slr',-1.2,-1.7]], # [name, initial, final]
                cStep = 101,
                cVars = [['suc',-0.1,-0.3],['ruc',-0.05,-0.25],['rlc',-0.15,-0.35],['slc',-0.07,-0.27]], # [name, initial, final]
                cinit = [['suc_init',-0.2,-0.0],['ruc_init',-0.25,-0.05],['rlc_init',-0.25,-0.05],['slc_init',-0.25,-0.05]], # [name, initial, final]
                rinit = [['sur_init',0.45,0.451],['rur_init',0.28,0.281],['rlr_init',0.20,0.201],['slr_init',0.30,0.301]], # [name, initial, final, rate for sweep, rate for step]
                ):
#    h5path = '/Users/shintaro/Documents/1_Research/3_SAW/4_Data/4_Postdoc/HBT6/'
#    configBasePath = '/Users/shintaro/Documents/1_Research/3_SAW/4_Data/4_Postdoc/HBT6/Config/'

    expdata = ExpData()
    expdata.readHDF5data2python(h5name=dataname, folderPath=h5path)
    
    X = []
    xpoints = expdata.dim[0]
    with h5py.File(expdata.saveFolder+expdata.filename+'.h5', 'r') as f:
        for item in qpcTargets:
            name = item[0]
            X.append([np.array(f[name][...]).flatten()[0], (np.array(f[name][...]).flatten()[-1]-np.array(f[name][...]).flatten()[0])/(xpoints-1)])
    
    pdatas = []
    for i, item in enumerate(qpcTargets):
        var = item[1]
        pdata = np.argmin(np.flipud(np.absolute(expdata.data[i,Ellipsis]-var)), axis=0)
        pdata = X[i][0]+X[i][1]*(xpoints-pdata)
        pdatas.append(pdata)
                
    for j in range(rStep):
        ex = Experiment()
        ex.sweeplist = []
        ex.comments = comments
        ex.dim = [load_count, cStep]
        counterstr = '%05d' % (j)
        ex.filename = outputBaseName+counterstr
        ex.configFile = configBasePath + configFiles
        ex.saveFolder = saveFolderFile
        
        init_move = []
        for i in range(len(qpcTargets)):
            # initial move for r gates
            name = rVars[i][0]
            parameter = 0
            rdelta = (rVars[i][2]-rVars[i][1])/float(rStep-1)*j
            value = rVars[i][1]+rdelta
            init_move.append((name, parameter, value))
            
            # load position sweep
            ss = single_sweep(name = load[i][0], sweep_dim = 1)
            ss.array = np.moveaxis(np.ones(ex.dim,dtype=float), 0, -1)
            pos0 = load[i][1] - rdelta
            pos1 = load[i][2] - rdelta
            ss.array = ss.array * np.linspace(pos0, pos1, num=ex.dim[0])
            ss.array = np.moveaxis(ss.array, -1, 0)
            ex.sweeplist.append(ss)
            
            # c steps
            ss = single_sweep(name = cVars[i][0], sweep_dim = 2)
            pos0 = cVars[i][1]
            pos1 = cVars[i][2]
            ss.array = np.ones(ex.dim, dtype=float) * np.linspace(pos0, pos1, num=ex.dim[1])
            ex.sweeplist.append(ss)
            
            # c_init steps
            ss = single_sweep(name = cinit[i][0], sweep_dim = 2)
            pos0 = cinit[i][1]
            pos1 = cinit[i][2]
            ss.array = np.ones(ex.dim, dtype=float) * np.linspace(pos0, pos1, num=ex.dim[1])
            ex.sweeplist.append(ss)
            
            # r_init steps
            ss = single_sweep(name = rinit[i][0], sweep_dim = 2)
            pos0 = rinit[i][1] - rdelta
            pos1 = rinit[i][2] - rdelta
            ss.array = np.ones(ex.dim, dtype=float) * np.linspace(pos0, pos1, num=ex.dim[1])
            ex.sweeplist.append(ss)
            
            # qpc step
            ss = single_sweep(name = qpcTargets[i][0], sweep_dim = 2)
            z0 = pdatas[i][0,0] + (pdatas[i][0,1] - pdatas[i][0,0])/(rStep-1)*j
            z0 = min(z0, -0.4)
            z0 = max(z0, -2.0)

            z1 = pdatas[i][1,0] + (pdatas[i][1,1] - pdatas[i][1,0])/(rStep-1)*j
            z1 = min(z1, -0.4)
            z1 = max(z1, -2.0)
            ss.array = np.ones(ex.dim, dtype=float)*np.linspace(z0,z1,num=ex.dim[1])
            ex.sweeplist.append(ss)
        ex.Initial_move = np.array(init_move, dtype=init_param_dt)
        ex.write(fpath=saveFolder+ex.filename+'.h5')
    
    
    
if __name__ == '__main__':
    start = time.time()
    if platform.system()=='Windows':
        h5path = 'E:/Takada/DATA/HBT6/data/'
    elif platform.system()=='Darwin':
#        path = '/Users/shintaro/Documents/1_Research/10_UniversalPhase/Data/Sample33/'+folder+'/'
        h5path = '/Users/shintaro/Documents/1_Research/10_UniversalPhase/Data/Sample14/HDF5/'
    dataname = '201612181352'
#    qpcAnalysisForStabilityDiagram()
#    Analysis20161221batch()
#    Analysis20161228batch()
#    Analysis20161221()
#    Analysis20161222()
#    Analysis20161222batch()
#    qpcAnalysisForLoading()
#    AnalysisLoadMap()
#    Analysis20161225()
#    Analysis20161230batch()
#    Analysis20170102()
#    Analysis20170104()
#    Analysis20170105()
#    Analysis20170106()
#    Analysis20170106B()
#    Analysis20170107()
#    Analysis20170108()
#    Analysis20170108B()
#    Analysis20170109()
#    Analysis20170115()
#    Analysis20170119()
#    Analysis20170124()
#    Analysis20170125()
#    Analysis20170126()
    Analysis20170127()
    print 'Time for loading data:%f' % (time.time()-start)
#    plt.show()