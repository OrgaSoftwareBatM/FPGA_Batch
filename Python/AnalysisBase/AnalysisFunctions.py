
# -*- coding: utf-8 -*-
"""
Created on San Oct 25 12:19:39 2015

@author: Shintaro
"""

#from __future__ import division

#import locale
#locale.setlocale(locale.LC_ALL,"de_DE.utf8") 

import sys
sys.path.insert(0,'..') # import parent directory
import copy
import numpy as np
import scipy.constants as const
import scipy.fftpack
from scipy.signal import hanning
import math
import inspect
import matplotlib.pyplot as plt
from matplotlib import rc
from DataStructure.datacontainer import ExpData

nameofpc='Shintaro Professional'#This much be changed in different PC

params = {'legend.fontsize': 12}
plt.rcParams.update(params)

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('xtick', labelsize=7)
rc('ytick', labelsize=7)
#rc('figure', figsize=(14/2.58,10.5/2.58))

plt.rcParams['xtick.major.pad']='14'
plt.rcParams['ytick.major.pad']='14'

"""---------------------------"""
""" Basic analyses """
"""---------------------------"""
def dataCalculation(expdatas=[], coefficients=[]):
    """ calculate A + B*data1 + C*data2 + ...
    at least 2 datasets and 3 coefficients are required."""
    calcdata = copy.deepcopy(expdatas[0])
    calcdata.readouts['data'][Ellipsis] = float(coefficients[0])
    s = 'calculate %f ' % (coefficients[0])# create a comment            
    for j, coef in enumerate(coefficients[1:]):
        calcdata.readouts['data'][Ellipsis] += coef * expdatas[j].readouts['data'][Ellipsis]
        s += '+ %f * %s ' % (coef, expdatas[j].filename)
    calcdata.comments += s + '.\r'
    return calcdata
    
def raw(expdata):
    return expdata

def movingAverage(expdata=ExpData(), box_size=10, axis=0):
    """1st points up to box_size is smoothed by using the data up to that number."""
    axis += 1 # shift axis to compensate readouts
    smoothdata = copy.deepcopy(expdata)
    smoothdata.readouts['data'] = np.moveaxis(smoothdata.readouts['data'], axis, 0)
    smoothdata.readouts['data'] = np.cumsum(smoothdata.readouts['data'], axis=0, dtype=float)
    smoothdata.readouts['data'][box_size:,Ellipsis] = (smoothdata.readouts['data'][box_size:,Ellipsis] - smoothdata.readouts['data'][:-1*box_size,Ellipsis])
    smoothdata.readouts['data'][box_size-1:,Ellipsis] = smoothdata.readouts['data'][box_size-1:,Ellipsis]/box_size
    if (box_size-1)>0:
        for i in range(box_size-1):
            smoothdata.readouts['data'][i,Ellipsis] = smoothdata.readouts['data'][i,Ellipsis]/(i+1)
    smoothdata.readouts['data'] = np.moveaxis(smoothdata.readouts['data'], 0, axis)
    s = 'movein average is performed along axis: '+str(axis-1)+' using box size: '+str(box_size)+' .\r'
    smoothdata.comments += s
    return smoothdata
    
def subtractSmoothedBackground(expdata=ExpData(), box_size=10, axis=0):
    smoothdata = movingAverage(expdata, box_size, axis)
    smbgdata = dataCalculation(expdatas=[expdata, smoothdata], coefficients=[0, 1, -1])
    return smbgdata

def convertV2G(expdata=ExpData(), axis=0, bias=3e-6, unit=1e-6, R_contact=0, R_measure=10000):
    axis += 1 # shift axis to compensate readouts
    """Convert measured voltage to conductance"""
    norm = 2*const.e*const.e/const.h
    gdata = copy.deepcopy(expdata)
    gdata.readouts['data'] = np.moveaxis(gdata.readouts['data'], axis, 0)
    gdata.readouts['data'][Ellipsis] = 1/((bias/(gdata.readouts['data'][Ellipsis]*unit)-1)*R_measure-R_contact) / norm
    gdata.readouts['data'] = np.moveaxis(gdata.readouts['data'], 0, axis)
    # create comments
    s = 'converted measured voltage ('+str(unit)+' V) to conductance along axis: '
    s+=str(axis-1)+' using bias = '+str(bias)+'uV, contact resistance = '+str(R_contact)
    s+=' ohm, measurement registance = '+str(R_measure)+' ohm.\r'
    gdata.comments += s
    return gdata
    
def derivative(expdata=ExpData(), box_smooth_size=5, axis=0):
    axis += 1 # shift axis to compensate readouts
    """1st order derivative a[n]=a[n+1]-a[n-1]
    Edge: a[0]=a[1]-a[0], a[N-1]=a[N-1]-a[N-2]"""
    if box_smooth_size == 0:
        smoothdata = expdata
    else:
        smoothdata = movingAverage(expdata, box_smooth_size, axis-1)
    smoothdata.readouts['data'] = np.moveaxis(smoothdata.readouts['data'], axis, 0)
    diffdata = copy.deepcopy(smoothdata)
    diffdata.readouts['data'][1:-1,Ellipsis] = np.diff(smoothdata.readouts['data'][:-1,Ellipsis],n=1,axis=0)+np.diff(smoothdata.readouts['data'][1:,Ellipsis],n=1,axis=0)
    diffdata.readouts['data'][0,Ellipsis]=np.subtract(smoothdata.readouts['data'][1,Ellipsis],smoothdata.readouts['data'][0,Ellipsis])
    diffdata.readouts['data'][-1:,Ellipsis]=np.subtract(smoothdata.readouts['data'][-1:,Ellipsis], smoothdata.readouts['data'][-2:-1,Ellipsis])
    diffdata.readouts['data'] = np.moveaxis(diffdata.readouts['data'], 0, axis)
    smoothdata.readouts['data'] = np.moveaxis(smoothdata.readouts['data'], 0, axis)
    s = '1st order derivative after smoothing with box size %d along the axis %d\r' % (box_smooth_size, axis-1)
    diffdata.comments += s
    return diffdata
    
def averagingData(expdata=ExpData(), axis=0, initial=0, final=0):
    axis += 1 # shift axis to compensate readouts
    avgdata = copy.deepcopy(expdata)
    if final == 0:
        final = avgdata.readouts['data'].shape[axis]
    avgdata.readouts['data'] = np.moveaxis(avgdata.readouts['data'], axis, 0)
    avgdata.readouts['data'] = np.mean(avgdata.readouts['data'][initial:final,Ellipsis], axis=0, dtype=float, keepdims=True)
    avgdata.readouts['data'] = np.moveaxis(avgdata.readouts['data'], 0, axis)
    s = 'Average is performed along the axis %d\r' % (axis-1)
    avgdata.comments += s
    return avgdata
    
def varianceData(expdata=ExpData(), axis=0, initial=0, final=0):
    axis += 1 # shift axis to compensate readouts
    vardata = copy.deepcopy(expdata)
    if final == 0:
        final = vardata.readouts['data'].shape[axis]
    vardata.readouts['data'] = np.moveaxis(vardata.readouts['data'], axis, 0)
    vardata.readouts['data'] = np.var(vardata.readouts['data'][initial:final,Ellipsis], axis=0, dtype=float, keepdims=True)
    vardata.readouts['data'] = np.moveaxis(vardata.readouts['data'], 0, axis)
    s = 'Average is performed along the axis %d\r' % (axis-1)
    vardata.comments += s
    return vardata
    
#def fftAmplitude(expdata=ExpData(), axis=0, window='Hanning'):
#    axis += 1 # shift axis to compensate readouts
#    fftdata = copy.deepcopy(expdata)
#    # Perform FFT with or without a window function
#    if window == 'Hanning':
#        fftdata.readouts['data'] = np.moveaxis(fftdata.readouts['data'], axis, -1)
#        dshape = fftdata.readouts['data'].shape
#        fftdata.readouts['data'] = np.absolute(scipy.fftpack.fft(fftdata.readouts['data']*hanning(dshape[-1]), axis=-1))
#        fftdata.readouts['data'] = np.moveaxis(fftdata.readouts['data'], -1, axis)
#    else:
#        fftdata.readouts['data'] = np.absolute(scipy.fftpack.fft(fftdata.readouts['data'], axis=axis))
#    # Make x axis
#    if axis == 0:
#        pass
#    s = 'Fast fourier transform is performed along the axis %d\r' % (axis-1)
#    fftdata.comments += s
#    return fftdata
    
#def fftPhase(data, axis):
#    fftdata = copy.deepcopy(data)
#    #phase is output in unit of pi [radian]
#    fftdata = np.angle(np.fft.fft(fftdata,axis=axis))/math.pi
#    s = 'Fast fourier transform is performed along the axis %d\r' % (axis)
#    return fftdata, s
#    
#def fftFilter(data, axis=0, delta=1.0, frange=[0,-1]):
#    filtdata = copy.deepcopy(data)
#    fftdata = scipy.fftpack.rfft(filtdata,axis=axis)
#    bins = scipy.fftpack.rfftfreq(data.shape[axis], d=delta)
#    if frange[1]==-1:
#        frange[1]=bins[-1]
#    fftdata[(bins<frange[0])]=0
#    fftdata[(bins>frange[1])]=0
#    filtdata = scipy.fftpack.irfft(fftdata, axis=axis)
#    s = 'FFT filter between %f and %f.' % (frange[0], frange[1])
#    return filtdata, s
    
"""------------------------------------------"""
""" special analyses for each measurement"""
"""-----------------------------------------"""
""" Pulse experiment (Everton) """
def pulseAnalysis(expdata=ExpData(), skip=50, normalize=True, correctjump=True ):
    orderStr = 'F'
    pulse=copy.deepcopy(expdata)
    # analyze data and make new data to return
    data=pulse.readouts['data']
    dshape = list(data.shape)
    dshape = tuple(dshape[0:2]+[-1]+dshape[4:]) # Get data size of (dshape[0], dshape[1], dshape[2]*dshape[3], dshape[4], ...)
    data = data.reshape(dshape, order=orderStr)
    newshape = list(data.shape) # Get data size of (dshape[0], 1, dshape[2]*dshape[3], dshape[4], ...)
    newshape[1]=1
    dstdata = np.empty(tuple(newshape), dtype=float)
    dstdata = np.mean(data[:,skip:,Ellipsis], axis=1, dtype=float, keepdims=True)
    pulse.readouts['data']=dstdata
    # create x axis to plot
    skew = expdata.sweeps['data'][expdata.sweepnamelist.index('ch2Skew'),Ellipsis]
    partial = [0]*len(skew.shape)
    partial[0] = slice(None)
    skew = skew[tuple(partial)] # channel skew
    skew = np.around(skew, 0) # round skew to integer
    dshape = list(expdata.sweeps['data'].shape)[1:]
    xarray = np.ones(tuple(dshape),dtype=float)
    # treat 83.33 ps along step2
    xarray = np.moveaxis(xarray, 1, -1)
    xarray = np.multiply(xarray, np.linspace(0, 1000/12*(dshape[1]-1), num=dshape[1]))
    xarray = np.moveaxis(xarray, -1, 1)
    # treat skew
    xarray = np.moveaxis(xarray, 0, -1)
    xarray = np.add(xarray, skew)
    xarray = np.moveaxis(xarray, -1, 0)
    # reshape data
    xarray = xarray.reshape(tuple([1]+newshape[2:]), order=orderStr)
    
    pulse.sweeps['data'] = pulse.sweeps['data'].reshape(tuple([-1]+newshape[2:]), order=orderStr)
    pulse.sweeps['data'] = np.vstack((pulse.sweeps['data'], xarray))
    
    pulse.sweeps['dims'].append(1)
    pulse.sweeps['units'].append('ps')
    pulse.sweeps['params'].append(0)
    
    pulse.sweepnamelist.append('delay')
    
    return pulse
    

#""" ----------   HBT experiment   -----------------------"""
#def shrinkSAWData(expdata, shrinkrange, bg_stage=0, bg_subtraction=[1,1,0,1]):
#    dshape = list(expdata.data.shape)
#    shData = copy.deepcopy(expdata)
#    no = len(shrinkrange)
#    dshape[1]=no
##    shData.dim[0] = no
#    shrinkedData=np.empty(dshape, dtype=np.float)
#    newnote='\rshrink data: '
#    for i in xrange(no):
#        newnote += '%d ~ %d, ' % (shrinkrange[i][0],shrinkrange[i][1])
#        """Subtract reference current value as a background"""
#        shrinkedData[:,i,Ellipsis]= (-1)*np.mean(expdata.data[:,shrinkrange[i][0]:shrinkrange[i][1]+1,Ellipsis], axis=1)
#    for i in xrange(no):
#        if i!= bg_stage:
#            for j in xrange(dshape[0]):
#                shrinkedData[j,i,Ellipsis]+= np.mean(expdata.data[j,shrinkrange[bg_stage][0]:shrinkrange[bg_stage][1]+1,Ellipsis], axis=0)*bg_subtraction[j]
#        else:
#            shrinkedData[:,i,Ellipsis] *= (-1)
#    # continue to make note
#    newnote += 'back ground = %d, background subtraction for [' % (bg_stage)
#    for item in bg_subtraction:
#        newnote += ' %d' % (item)
#    newnote += ']'
#    shData.comments += newnote
#    shData.data = shrinkedData
#    shData.filename = expdata.filename+'_sh'
#    return shData
#    
def sendingMap(expdata=ExpData(), bi=10, bf=13, ai=30, af=33):
    """
    bi: before send or receive initial position
    bf: before send or receive final position
    ai: after send or receive initial position
    af: after send or receive final position
    """
    smapdata = copy.deepcopy(expdata)
    dshape = list(smapdata.readouts['data'].shape)
    dshape[1] = 1
    sdata = np.empty(dshape, dtype=np.float)
    sdata[:,0,Ellipsis] = np.mean(expdata.readouts['data'][:,ai:af+1,Ellipsis],axis=1) - np.mean(expdata.readouts['data'][:,bi:bf+1,Ellipsis],axis=1)
    smapdata.readouts['data'] = sdata
    smapdata.comments += 'sending map: mean(%d ~ %d) - mean(%d ~ %d)' % (ai, af, bi, bf)
    return smapdata
#    
## SAW STATISTICS NOT UPDATED FOR NEW HBT5 FILE FORMAT!!!
#def sawStatistics(expdata, boundaries, repstep=2, error_correct=True, shrinkData=True, shrinkrange=[], bg_stage=0, bg_subtraction=[1,1,0,1]):
#    """ Shrink data """
#    if shrinkData:
#        statsdata = shrinkSAWData(expdata, shrinkrange, bg_stage=0, bg_subtraction=[1,1,0,1])
#    else:
#        statsdata = copy.deepcopy(expdata)
#    """ change the shape to digitize """
#    dshape = list(statsdata.data.shape)
#    statsdata.data = statsdata.data.reshape(dshape[0],dshape[1],-1)
#    sumstats = np.empty(dshape[2:],dtype=np.str)
#    sumstats = sumstats.reshape((-1))
#    sumstats[:]=''
#    """ digitize data using given boundaries"""
#    for i in range(dshape[0]):
#        for j in range(dshape[1]):
#            sumstats = np.core.defchararray.add(sumstats,np.digitize(statsdata.data[i,j,:], np.array(boundaries[i][j])).astype(np.str))
#        sumstats = np.core.defchararray.add(sumstats,'|')
#    u, inverse = np.unique(sumstats, return_inverse=True, return_counts=False)
#    inverse = inverse.reshape(dshape[2:])
#    """ return the shape back """
#    statsdata.data = statsdata.data.reshape(dshape)
#    """ Calculate statistics """
#    inverse = np.moveaxis(inverse, repstep-1, 0) # -1 to remove the readouts
#    tempshape = inverse.shape
#    inverse = inverse.reshape((tempshape[0],-1))
#    tempshape = inverse.shape
#    dstShape=dshape[:]
#    dstShape[1]=1       # set fast cycle dimension size to 1
#    dstShape[repstep]=1 # set repetition step size to 1
#    dstShape[0]=len(u)+1    # set readouts dimension to len(u)+1
#    dstdata = np.zeros(dstShape, dtype=float)
#    dstdata = dstdata.reshape((dstShape[0],-1))
#    for i in range(tempshape[0]):
#        u_temp, count = np.unique(inverse[i,:], return_counts=True)
#        """ calculate total number of error detection event to be subtracted """
#        no_error=0
#        if error_correct:
#            for k in range(len(u_temp)):
#                temp = u[u_temp[k]]
#                for l in range(len(temp)):
#                    if temp[l]!='|':
#                        if (int(temp[l])%2)==1:
#                            no_error += count[k]
#                            break
#        dstdata[len(u)][i]= dshape[repstep]-no_error
#        for k in range(len(u_temp)):
#            dstdata[u_temp[k]][i] = float(count[k])/float(dshape[repstep]-no_error)
#    dstdata = dstdata.reshape(dstShape)
#    """ Summarise the required probabilities """
#    manual = ['020|0..|0..|000|','020|002|000|000|','020|000|002|000|','020|001|001|000|']
#    if error_correct:
#        """ convert 'manual' for post selection """
#        manual_conv = []
#        for i in range(len(manual)):
#            temp = manual[i]
#            for j in range(len(temp)):
#                char = temp[j]
#                if char != '.' and char != '|':
#                    temp=temp[0:j]+str(2*int(char))+temp[j+1:]
#            manual_conv.append(temp)
#    else:
#        manual_conv = manual
#    statsShape = dstShape[:]
#    statsShape[0]=len(manual)+1
#    statsdata.data = np.zeros(statsShape, dtype=float)
#    statsdata.readoutlist = [s.replace('.','x') for s in manual]
#    statsdata.readoutunits = ['prob']*len(manual)
#    statsdata.readoutlist.append('Sampling')
#    statsdata.readoutunits.append('pts')
#    statsdata.data[Ellipsis,len(manual)]=dstdata[Ellipsis,len(u)]
#    for i in range(len(u)):
#        for j in range(len(manual)):
#            if error_correct == True:
#                manual_conv[j] = manual_conv[j].replace('.','[02468]').replace('|','')
#            else:
#                manual_conv[j] = manual_conv[j].replace('.','[0-9]').replace('|','')
#            if re.match(manual_conv[j],u[i].replace('|','')):
#                statsdata.data[j,Ellipsis] = np.add(statsdata.data[j,Ellipsis],dstdata[i,Ellipsis])
#    return statsdata

if __name__ == '__main__':
    test = inspect.signature(derivative)
    print(test.parameters)