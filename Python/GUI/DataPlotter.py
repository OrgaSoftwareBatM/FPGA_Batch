#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 22:07:20 2016

@author: shintaro
"""
import os, sys
#sys.path.insert(0,'../..') # include parent parent directory
sys.path.insert(0,'..')
from DataStructure.datacontainer import *
import copy
import h5py
import natsort
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.gridspec as gridspec

import GUI.Analysis_widget as aw
import GUI.IpythonWidgetClass as ipy

pathSep = QtCore.QDir.separator()
""" -------------------------------------------
Utility classes 
----------------------------------------------"""
class BasePEWidget(object):
    def get_value(self):
        pass
    def set_value(self):
        pass
        
class QFloatLineEdit(QtWidgets.QLineEdit, BasePEWidget):
    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        validator = QtGui.QDoubleValidator(self)
        self.setValidator(validator)
    def get_value(self):
        return float(str(self.text()))
    def set_value(self, str_value):
        self.setText(str(str_value))
        
class oneDCombo(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 label = 'test',
                 initial_size = 3,
                 widget=QtWidgets.QComboBox,
                 hight = 25,
                 width = 100,
                 items = [],
                 vertical = False,
                 showSizeControl = True,
                 ):
        super(oneDCombo, self).__init__()
        self.parent = parent
        self.w = widget
        self.c = initial_size
        self.items = items
        self.label = label
        self.hight = hight
        self.width = width
        self.vertical = vertical
        self.showSizeControl = showSizeControl
        if self.vertical:
            self.main = QtWidgets.QVBoxLayout()
            self.main.setSpacing(0)
            self.sub1 = QtWidgets.QVBoxLayout()
            self.sub1.setSpacing(0)
            self.sub2 = QtWidgets.QGridLayout()
            self.sub2.setSpacing(0) 
        else:
            self.main = QtWidgets.QHBoxLayout()
            self.main.setSpacing(0)
            self.sub1 = QtWidgets.QHBoxLayout()
            self.sub1.setSpacing(0)
            self.sub2 = QtWidgets.QGridLayout()
            self.sub2.setSpacing(0)
        item = QtWidgets.QLabel(self.label)
        item.setFixedSize(len(label)*7,self.hight)
        self.sub1.addWidget(item)
        item = QtWidgets.QSpinBox()
        item.setRange(1,10000)
        item.setValue(self.c)
        item.setFixedSize(40,hight)
        item.valueChanged.connect(self.update)
        self.sub1.addWidget(item)
        
        for i in range(self.c):
            w = self.w()
            w.addItems(self.items)
            w.setFixedSize(self.width, self.hight)
            if self.vertical:
                self.sub2.addWidget(w,i,0,1,1)
            else:
                self.sub2.addWidget(w,0,i,1,1)
            
        if self.showSizeControl:
            self.main.addLayout(self.sub1)
            additional_size = 2
        else:
            additional_size = 0
        self.main.addLayout(self.sub2)
        self.setLayout(self.main)
        
        if not self.parent == None:
            extra = 0
        else:
            extra = 40
        if self.vertical:
            self.setFixedSize(extra+max(self.width, len(self.label)*7), extra+(self.c+additional_size)*self.hight)
        else:
            self.setFixedSize(extra+max(40, len(self.label)*7)+(self.c+additional_size)*self.width, extra+self.hight)
        
    def update(self):
        col = self.sub1.itemAt(1).widget()
        for i in range(col.value()):
            if self.vertical:
                item = self.sub2.itemAtPosition(i,0)
            else:
                item = self.sub2.itemAtPosition(0,i)
            if item == None:
                w = self.w()
                w.addItems(self.items)
                w.setFixedSize(self.width, self.hight)
            else:
                if item.widget() == None:
                    w = self.w()
                    w.addItems(self.items)
                    w.setFixedSize(self.width, self.hight)
                else:
                    w = item.widget()
            if self.vertical:
                self.sub2.addWidget(w,i,0,1,1)
            else:
                self.sub2.addWidget(w,0,i,1,1)
                    
         #delete extra widgets
        if self.c > col.value():
            for i in reversed(range(self.c - col.value())):
                if self.vertical:
                    item = self.sub2.itemAtPosition(i+col.value(), 0)
                else:
                    item = self.sub2.itemAtPosition(0,i+col.value())
                if not item == None:
                    w = item.widget()
                    if not w == None:
                        w.deleteLater()
        self.c = col.value()
        
        if self.showSizeControl:
            self.main.addLayout(self.sub1)
            additional_size = 2
        else:
            additional_size = 0
            
        if not self.parent == None:
            extra = 0
        else:
            extra = 40
            
        if self.vertical:
            self.setFixedSize(extra+max(self.width, len(self.label)*7), extra+(self.c+additional_size)*self.hight)
        else:
            self.setFixedSize(extra+max(40, len(self.label)*7)+(self.c+additional_size)*self.width, extra+self.hight)
        
class oneDgui(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 label = 'test',
                 initial_size = 3,
                 widget=QFloatLineEdit,
                 hight = 25,
                 width = 100,
                 vertical = False,
                 showSizeControl = True,
                 ):
        super(oneDgui, self).__init__()
        self.w = widget
        self.c = initial_size
        self.label = label
        self.hi = hight
        self.wi = width
        self.vertical = vertical
        self.showSizeControl = showSizeControl
        if self.vertical:
            self.main = QtWidgets.QVBoxLayout()
            self.main.setSpacing(0)
            self.sub1 = QtWidgets.QVBoxLayout()
            self.sub1.setSpacing(0)
            self.sub2 = QtWidgets.QGridLayout()
            self.sub2.setSpacing(0) 
        else:
            self.main = QtWidgets.QHBoxLayout()
            self.main.setSpacing(0)
            self.sub1 = QtWidgets.QHBoxLayout()
            self.sub1.setSpacing(0)
            self.sub2 = QtWidgets.QGridLayout()
            self.sub2.setSpacing(0)
        item = QtWidgets.QLabel(self.label)
        item.setFixedSize(len(label)*7,self.hi)
        self.sub1.addWidget(item)
        item = QtWidgets.QSpinBox()
        item.setRange(1,10000)
        item.setValue(self.c)
        item.setFixedSize(40,hight)
        item.valueChanged.connect(self.update)
        self.sub1.addWidget(item)
        
        for i in range(self.c):
            w = self.w()
            w.setFixedSize(self.wi, self.hi)
            if self.vertical:
                self.sub2.addWidget(w,i,0,1,1)
            else:
                self.sub2.addWidget(w,0,i,1,1)
            
        if self.showSizeControl:
            self.main.addLayout(self.sub1)
            additional_size = 2
        else:
            additional_size = 0
        self.main.addLayout(self.sub2)
        self.setLayout(self.main)
        
        if not self.parent == None:
            extra = 0
        else:
            extra = 40
            
        if self.vertical:
            self.setFixedSize(extra+max(self.wi, len(self.label)*7), extra+(self.c+additional_size)*self.hi)
        else:
            self.setFixedSize(extra+max(40, len(self.label)*7)+(self.c+additional_size)*self.wi, extra+self.hi)
        
    def update(self):
        col = self.sub1.itemAt(1).widget()
        for i in range(col.value()):
            if self.vertical:
                item = self.sub2.itemAtPosition(i,0)
            else:
                item = self.sub2.itemAtPosition(0,i)
            if item == None:
                w = self.w()
                w.setFixedSize(self.wi, self.hi)
            else:
                if item.widget() == None:
                    w = self.w()
                    w.setFixedSize(self.wi, self.hi)
                else:
                    w = item.widget()
            if self.vertical:
                self.sub2.addWidget(w,i,0,1,1)
            else:
                self.sub2.addWidget(w,0,i,1,1)
                    
         #delete extra widgets
        if self.c > col.value():
            for i in reversed(range(self.c - col.value())):
                if self.vertical:
                    item = self.sub2.itemAtPosition(i+col.value(), 0)
                else:
                    item = self.sub2.itemAtPosition(0,i+col.value())
                if not item == None:
                    w = item.widget()
                    if not w == None:
                        w.deleteLater()
        self.c = col.value()
        
        if self.showSizeControl:
#            self.main.addLayout(self.sub1)
            additional_size = 2
        else:
            additional_size = 0
            
        if not self.parent == None:
            extra = 0
        else:
            extra = 40
            
        if self.vertical:
            self.setFixedSize(extra+max(self.wi, len(self.label)*7), extra+20+(self.c+additional_size)*self.hi)
        else:
            self.setFixedSize(extra+max(40, len(self.label)*7)+(self.c+additional_size)*self.wi, extra+20+self.hi)
        
class twoDgui(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 label = 'test',
                 initial_size = [3,3],
                 widget=QFloatLineEdit,
                 hight = 25,
                 width = 100,
                 showSizeControl = True,
                 ):
        super(twoDgui, self).__init__()
        self.w = widget
        self.r = initial_size[0]
        self.c = initial_size[1]
        self.label = label
        self.hi = hight
        self.wi = width
        self.showSizeControl = showSizeControl
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.size = QtWidgets.QVBoxLayout()
        self.size.setSpacing(0)
        if self.showSizeControl:
            self.additionalWidth = 1
        else:
            self.additionalWidth = 0
            
        item = QtWidgets.QLabel(label)
        item.setFixedSize(len(label)*7,hight)
        self.size.addWidget(item)
        for i, no in enumerate(initial_size):
            item = QtWidgets.QSpinBox()
            item.setRange(1, 10000)
            item.setValue(no)
            item.setFixedSize(40,hight)
            item.valueChanged.connect(self.update)
            self.size.addWidget(item)
        
        for i in range(self.r):
            for j in range(self.c):
                w = self.w()
                w.setFixedSize(self.wi, self.hi)
                self.grid.addWidget(w,i,j,1,1)
                
        if not self.parent == None:
            extra = 0
        else:
            extra = 40
            
        ly = QtWidgets.QHBoxLayout()
        ly.setSpacing(0)
        if self.showSizeControl:
            ly.addLayout(self.size)
        ly.addLayout(self.grid)
        self.setLayout(ly)
        self.setFixedSize(max(40,len(self.label)*5)*self.additionalWidth+self.wi*self.c+extra,max(self.r*self.hi, self.hi*3)+extra)
        
    def update(self):
        row = self.size.itemAt(1).widget()
        col = self.size.itemAt(2).widget()
        for i in range(row.value()):
            for j in range(col.value()):
                item = self.grid.itemAtPosition(i,j)
                if item == None:
                    w = self.w()
                    w.setFixedSize(self.wi, self.hi)
                else:
                    if item.widget() == None:
                        w = self.w()
                        w.setFixedSize(self.wi, self.hi)
                    else:
                        w = item.widget()
                self.grid.addWidget(w,i,j,1,1)
                    
         #delete extra widgets
        if self.r > row.value():
            csize = self.grid.columnCount()
            for i in reversed(range(self.r-row.value())):
                for j in reversed(range(csize)):
                    item = self.grid.itemAtPosition(row.value()+i, j)
                    if not item == None:
                        w = item.widget()
                        if not w == None:
                            w.deleteLater()
        if self.c > col.value():
            rsize = self.grid.rowCount()
            for i in reversed(range(rsize)):
                for j in reversed(range(self.c - col.value())):
                    item = self.grid.itemAtPosition(i, col.value()+j)
                    if not item == None:
                        w = item.widget()
                        if not w == None:
                            w.deleteLater()
        self.r = row.value()
        self.c = col.value()
        self.setFixedSize(max(40,len(self.label)*5)*self.additionalWidth+self.wi*self.c+40,max(self.r*self.hi, self.hi*3)+40)
        
""" Widget to make figure window """                
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor('#ffffff')
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
#        self.axes.hold(False)

        self.compute_initial_figure()
        #
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
    
class fileList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(fileList, self).__init__()
        vb = QtWidgets.QVBoxLayout()
        vb.setSpacing(0)
        folderBtn = QtWidgets.QPushButton('Folder')
        folderBtn.clicked.connect(self.folderDialog)
        folderBtn.setFixedSize(70,25)
        self.folderPath = QtWidgets.QLineEdit()
        self.folderPath.setFixedSize(180,25)
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        hb.addWidget(folderBtn)
        hb.addWidget(self.folderPath)
        vb.addLayout(hb)
        label = QtWidgets.QLabel('Filter')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(70,25)
        self.filterStr = QtWidgets.QLineEdit()
        self.filterStr.editingFinished.connect(self.updateFileList)
        self.filterStr.setFixedSize(180,25)
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        hb.addWidget(label)
        hb.addWidget(self.filterStr)
        vb.addLayout(hb)
        self.fileList = QtWidgets.QListWidget()
        self.fileList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.fileList.setFixedWidth(250)
        self.fileWatcher = QtCore.QFileSystemWatcher()
        self.fileWatcher.directoryChanged.connect(self.updateFileList)
        vb.addWidget(self.fileList)
        self.setLayout(vb)
        try:
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5','r') as f:
                dset = f.get('log')
                self.folderPath.setText(dset.attrs['PlotFolderPath'])
                self.updateFileList()
        except:
            pass
        
    def folderDialog(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        if not self.folderPath.text() == '':
            savePath = fileDialog.getExistingDirectory(self, 'Choose folder', directory=os.path.dirname(self.folderPath.text()))
        else:
            savePath = fileDialog.getExistingDirectory(self, 'Choose folder')
        if not savePath == '':
            self.fileWatcher.addPath(savePath)
            self.folderPath.setText(savePath)
            """ save folder path """
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5', 'a') as f:
                dset = f.get('log')
                if dset == None:
                    dset = f.create_dataset('log', data = 0)
                dset.attrs['PlotFolderPath'] = self.folderPath.text()
        self.updateFileList()
                
    def updateFileList(self):
        dirName = self.folderPath.text()
        current_dir = QtCore.QDir(dirName)
        self.fileList.clear()
        filterStr = self.filterStr.text()+'*.h5'
        fileNames = natsort.natsorted(current_dir.entryList([filterStr], QtCore.QDir.Files, QtCore.QDir.Name))
        self.fileList.addItems(fileNames)
        
class plotInfo1D(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 pDim = 0,
                 sweeps = [],
                 readouts=[],
                 readout_selections=[0],
                 prange=[],
                 offsets=[],
                 factor=[1.0,1.0],
                 showlegend = True, showTitle = True,   showGrid = True, useCounter=False,
                 xlabel = '',   ylabel = '',
                 x_ax_range=[], y_ax_range=[],
                 x_tick_freq=0, y_tick_freq=0,
                 xticks=[],     yticks=[],
                 ):
        super(plotInfo1D, self).__init__()
        self.ly = QtWidgets.QVBoxLayout()
        self.ly.setSpacing(0)
        
        # GUI for plot dim
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('Plot dim')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.pDim = QtWidgets.QSpinBox()
        self.pDim.setRange(0,20)
        self.pDim.setFixedSize(40,30)
        self.pDim.setValue(pDim)
        hb.addWidget(self.pDim)
        self.ly.addLayout(hb)
        # GUI for sweeps
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('sweeps')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.sweeps = QtWidgets.QComboBox()
        if sweeps == []:
            self.sweeps.addItem('none')
        else:
            self.sweeps.addItems(sweeps)
        hb.addWidget(self.sweeps)
        self.ly.addLayout(hb)
        
        # GUI for readouts
        if readouts == []:
            readouts = ['none']
        self.readouts = oneDCombo(label = 'readouts',
                                initial_size = len(readout_selections),
                                items = readouts,
                                widget = QtWidgets.QComboBox,
                                hight=40,
                                width=100
                                )
        if readouts == []:
            for i in range(self.readouts.c):
                w = self.readouts.sub2.itemAt(i).widget()
                w.setCurrentIndex(readout_selections[i])
        else:
            for i in range(self.readouts.c):
                w = self.readouts.sub2.itemAt(i).widget()
                w.setCurrentIndex(readout_selections[i])
        sc = QtWidgets.QScrollArea()
        sc.setWidget(self.readouts)
        sc.setFixedHeight(80)
        self.ly.addWidget(sc)
        
        # GUI for plot ranges
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('plot range')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(100,30)
        hb.addWidget(label)
        self.pranges = QtWidgets.QLineEdit()
        self.pranges.setText(','.join([str(i) for i in prange]))
        hb.addWidget(self.pranges)
        self.ly.addLayout(hb)
        
        # GUI for offsets
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('y offset')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(70,30)
        hb.addWidget(label)
        self.offsets = QtWidgets.QLineEdit()
        self.offsets.setText(','.join(offsets))
        hb.addWidget(self.offsets)
        self.ly.addLayout(hb)
        
        # GUI for factor
        self.factor = QtWidgets.QHBoxLayout()
        self.factor.setSpacing(0)
        label = QtWidgets.QLabel('xscale')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.factor.addWidget(label)
        item = QFloatLineEdit()
        item.set_value(factor[0])
        item.setFixedSize(60,30)
        self.factor.addWidget(item)
        label = QtWidgets.QLabel('yscale')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.factor.addWidget(label)
        item = QFloatLineEdit()
        item.set_value(factor[1])
        item.setFixedSize(60,30)
        self.factor.addWidget(item)
        self.ly.addLayout(self.factor)
        
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)

        label = QtWidgets.QLabel('Legend')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.showlegend = QtWidgets.QCheckBox()
        if showlegend:
            self.showlegend.setCheckState(2)
        else:
            self.showlegend.setCheckState(0)
        hb.addWidget(self.showlegend)

        label = QtWidgets.QLabel('Title')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.showTitle = QtWidgets.QCheckBox()
        if showTitle:
            self.showTitle.setCheckState(2)
        else:
            self.showTitle.setCheckState(0)
        hb.addWidget(self.showTitle)
        self.ly.addLayout(hb)
            
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('Grid')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.showGrid = QtWidgets.QCheckBox()
        if showGrid:
            self.showGrid.setCheckState(2)
        else:
            self.showGrid.setCheckState(0)
        hb.addWidget(self.showGrid)
        label = QtWidgets.QLabel('Use counter')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.useCounter = QtWidgets.QCheckBox()
        if useCounter:
            self.useCounter.setCheckState(2)
        else:
            self.useCounter.setCheckState(0)
        hb.addWidget(self.useCounter)

        self.ly.addLayout(hb)
            
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('xlabel')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.xlabel = QtWidgets.QLineEdit()
        self.xlabel.setText(xlabel)
        self.xlabel.setFixedSize(130,30)
        hb.addWidget(self.xlabel)
        self.ly.addLayout(hb)

        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('ylabel')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.ylabel = QtWidgets.QLineEdit()
        self.ylabel.setText(ylabel)
        self.ylabel.setFixedSize(130,30)
        hb.addWidget(self.ylabel)
        self.ly.addLayout(hb)
        
        self.x_ax_range = QtWidgets.QHBoxLayout()
        self.x_ax_range.setSpacing(0)
        label = QtWidgets.QLabel('x min')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.x_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(x_ax_range[0])
        except:
            pass
        item.setFixedSize(60,30)
        self.x_ax_range.addWidget(item)
        label = QtWidgets.QLabel('x max')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.x_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(x_ax_range[1])
        except:
            pass
        item.setFixedSize(60,30)
        self.x_ax_range.addWidget(item)
        self.ly.addLayout(self.x_ax_range)
        
        self.y_ax_range = QtWidgets.QHBoxLayout()
        self.y_ax_range.setSpacing(0)
        label = QtWidgets.QLabel('y min')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.y_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(y_ax_range[0])
        except:
            pass
        item.setFixedSize(60,30)
        self.y_ax_range.addWidget(item)
        label = QtWidgets.QLabel('y max')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.y_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(y_ax_range[1])
        except:
            pass
        item.setFixedSize(60,30)
        self.y_ax_range.addWidget(item)
        self.ly.addLayout(self.y_ax_range)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('x tick freq')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(90,30)
        hb.addWidget(label)
        self.x_tick_freq = QtWidgets.QSpinBox()
        self.x_tick_freq.setFixedSize(50,30)
        try:
            self.x_tick_freq.setValue(x_tick_freq)
        except:
            pass
        hb.addWidget(self.x_tick_freq)
        label = QtWidgets.QLabel('y tick freq')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(90,30)
        hb.addWidget(label)
        self.y_tick_freq = QtWidgets.QSpinBox()
        self.y_tick_freq.setFixedSize(50,30)
        try:
            self.y_tick_freq.setValue(y_tick_freq)
        except:
            pass
        hb.addWidget(self.y_tick_freq)
        self.ly.addLayout(hb)
                
#        self.setFixedSize(500,600)
        self.setLayout(self.ly)
        
    def dimSelec2Slice(self, string):
        if string == '':
            return [Ellipsis]
        else:
            selection=list()
            for item in string.split(','):
                if item == ':':
                    selection.append(slice(None))
                elif item.find(':') != -1:
                    l = item.split(':')
                    if len(l)==2:
                        selection.append(slice(int(l[0]),int(l[1])))
                    elif len(l)==3:
                        selection.append(slice(int(l[0]),int(l[1]),int(l[2])))
                    else:
                        selection.append(slice(None))
                else:
                    selection.append(slice(int(item),int(item)+1))
            return selection
        
    def getValues(self):
        args = {}
        args['pDim'] = self.pDim.value()
        if self.sweeps.currentText() == 'none':
            args['sweep']=''
        else:
            args['sweep'] = self.sweeps.currentText()#.encode('ascii')
        args['readouts'] = [self.readouts.sub2.itemAt(i).widget().currentText() for i in range(self.readouts.c)]
        args['pranges'] = self.dimSelec2Slice(self.pranges.text())
        if self.offsets.text()=='':
            args['y offsets'] = []
        else:
            args['y offsets'] = [float(n) for n in self.offsets.text().split(',')]
        args['factor'] = [self.factor.itemAt(1).widget().get_value(),self.factor.itemAt(3).widget().get_value()]
        if self.showlegend.checkState() == 0:
            args['showlegend'] = False
        else:
            args['showlegend'] = True
        if self.showTitle.checkState() == 0:
            args['showTitle'] = False
        else:
            args['showTitle'] = True
        if self.showGrid.checkState() == 0:
            args['showGrid'] = False
        else:
            args['showGrid'] = True
        if self.useCounter.checkState() == 0:
            args['useCounter'] = False
        else:
            args['useCounter'] = True
        args['xlabel'] = self.xlabel.text()
        args['ylabel'] = self.ylabel.text()
        try:
            xmin = self.x_ax_range.itemAt(1).widget().get_value()
            xmax = self.x_ax_range.itemAt(3).widget().get_value()
            args['x_ax_range'] = [xmin, xmax]
        except:
            args['x_ax_range'] = []
        try:
            ymin = self.y_ax_range.itemAt(1).widget().get_value()
            ymax = self.y_ax_range.itemAt(3).widget().get_value()
            args['y_ax_range'] = [ymin, ymax]
        except:
            args['y_ax_range'] = []
        args['x_tick_freq'] = self.x_tick_freq.value()
        args['y_tick_freq'] = self.y_tick_freq.value()
        return args
        
class plotInfo2D(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 plotDims = [[0,0],[1,0]],
                 sweeps = [],
                 readouts=[],
                 pranges=[],
                 factor=[1.0,1.0,1.0],
                 showColorbar = True, showTitle = True,   showGrid = False,
                 flipX = False, flipY = False, transpose = True,
                 xlabel = '',   ylabel = '', zlabel = '',
                 x_ax_range=[], y_ax_range=[], z_ax_range = [],
                 x_tick_freq=0, y_tick_freq=0, z_tick_freq = 0,
                 lineSlice=False,
                 ):
        super(plotInfo2D, self).__init__()
        self.ly = QtWidgets.QVBoxLayout()
        self.ly.setSpacing(0)
        

        # GUI for plot dimenstions
        self.plotDims = QtWidgets.QHBoxLayout()
        self.plotDims.setSpacing(0)
        label = QtWidgets.QLabel('x')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.plotDims.addWidget(label)
        item = QtWidgets.QSpinBox()
        item.setValue(plotDims[0][0])
        self.plotDims.addWidget(item)
        item = QtWidgets.QComboBox()
        if sweeps == []:
            item.addItem('none')
        else:
            item.addItems(sweeps)
        item.setCurrentIndex(plotDims[0][1])
        self.plotDims.addWidget(item)
        label = QtWidgets.QLabel('y')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.plotDims.addWidget(label)
        item = QtWidgets.QSpinBox()
        item.setValue(plotDims[1][0])
        self.plotDims.addWidget(item)
        item = QtWidgets.QComboBox()
        if sweeps == []:
            item.addItem('none')
        else:
            item.addItems(sweeps)
        item.setCurrentIndex(plotDims[1][1])
        self.plotDims.addWidget(item)
        self.ly.addLayout(self.plotDims)
        
        # GUI for readouts
        if readouts == []:
            readouts = ['none']
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('readout')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.readouts = QtWidgets.QComboBox()
        self.readouts.addItems(readouts)
        hb.addWidget(self.readouts)
        self.ly.addLayout(hb)
        
        # GUI for plot ranges
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('plot range')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(100,30)
        hb.addWidget(label)
        self.pranges = QtWidgets.QLineEdit()
        self.pranges.setText(','.join([str(i) for i in pranges]))
        hb.addWidget(self.pranges)
        self.ly.addLayout(hb)
        
        # GUI for factor
        self.factor = QtWidgets.QHBoxLayout()
        self.factor.setSpacing(0)
        label = QtWidgets.QLabel('xscale')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.factor.addWidget(label)
        item = QFloatLineEdit()
        item.set_value(factor[0])
        item.setFixedSize(60,30)
        self.factor.addWidget(item)
        label = QtWidgets.QLabel('yscale')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.factor.addWidget(label)
        item = QFloatLineEdit()
        item.set_value(factor[1])
        item.setFixedSize(60,30)
        self.factor.addWidget(item)
        label = QtWidgets.QLabel('zscale')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.factor.addWidget(label)
        item = QFloatLineEdit()
        item.set_value(factor[1])
        item.setFixedSize(60,30)
        self.factor.addWidget(item)
        self.ly.addLayout(self.factor)
        
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)

        label = QtWidgets.QLabel('Color bar')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.showcolorBar = QtWidgets.QCheckBox()
        if showColorbar:
            self.showcolorBar.setCheckState(2)
        else:
            self.showcolorBar.setCheckState(0)
        hb.addWidget(self.showcolorBar)

        label = QtWidgets.QLabel('Title')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.showTitle = QtWidgets.QCheckBox()
        if showTitle:
            self.showTitle.setCheckState(2)
        else:
            self.showTitle.setCheckState(0)
        hb.addWidget(self.showTitle)
        
        label = QtWidgets.QLabel('Grid')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.showGrid = QtWidgets.QCheckBox()
        if showGrid:
            self.showGrid.setCheckState(2)
        else:
            self.showGrid.setCheckState(0)
        hb.addWidget(self.showGrid)
        self.ly.addLayout(hb)
            
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('frip x')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.flipX = QtWidgets.QCheckBox()
        if flipX:
            self.flipX.setCheckState(2)
        else:
            self.flipX.setCheckState(0)
        hb.addWidget(self.flipX)
        label = QtWidgets.QLabel('frip y')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.flipY = QtWidgets.QCheckBox()
        if flipX:
            self.flipY.setCheckState(2)
        else:
            self.flipY.setCheckState(0)
        hb.addWidget(self.flipY)
        label = QtWidgets.QLabel('transpose')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.transpose = QtWidgets.QCheckBox()
        if transpose:
            self.transpose.setCheckState(2)
        else:
            self.transpose.setCheckState(0)
        hb.addWidget(self.transpose)
        self.ly.addLayout(hb)
            
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('xlabel')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.xlabel = QtWidgets.QLineEdit()
        self.xlabel.setText(xlabel)
        self.xlabel.setFixedSize(130,30)
        hb.addWidget(self.xlabel)
        self.ly.addLayout(hb)

        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('ylabel')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.ylabel = QtWidgets.QLineEdit()
        self.ylabel.setText(ylabel)
        self.ylabel.setFixedSize(130,30)
        hb.addWidget(self.ylabel)
        self.ly.addLayout(hb)
        
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('zlabel')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(60,30)
        hb.addWidget(label)
        self.zlabel = QtWidgets.QLineEdit()
        self.zlabel.setText(ylabel)
        self.zlabel.setFixedSize(130,30)
        hb.addWidget(self.zlabel)
        self.ly.addLayout(hb)
        
        self.x_ax_range = QtWidgets.QHBoxLayout()
        self.x_ax_range.setSpacing(0)
        label = QtWidgets.QLabel('x ini')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.x_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(x_ax_range[0])
        except:
            pass
        item.setFixedSize(60,30)
        self.x_ax_range.addWidget(item)
        label = QtWidgets.QLabel('x fin')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.x_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(x_ax_range[1])
        except:
            pass
        item.setFixedSize(60,30)
        self.x_ax_range.addWidget(item)
        self.ly.addLayout(self.x_ax_range)
        
        self.y_ax_range = QtWidgets.QHBoxLayout()
        self.y_ax_range.setSpacing(0)
        label = QtWidgets.QLabel('y ini')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.y_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(y_ax_range[0])
        except:
            pass
        item.setFixedSize(60,30)
        self.y_ax_range.addWidget(item)
        label = QtWidgets.QLabel('y fin')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.y_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(y_ax_range[1])
        except:
            pass
        item.setFixedSize(60,30)
        self.y_ax_range.addWidget(item)
        self.ly.addLayout(self.y_ax_range)
        
        self.z_ax_range = QtWidgets.QHBoxLayout()
        self.z_ax_range.setSpacing(0)
        label = QtWidgets.QLabel('z min')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.z_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(z_ax_range[0])
        except:
            pass
        item.setFixedSize(60,30)
        self.z_ax_range.addWidget(item)
        label = QtWidgets.QLabel('z max')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(50,30)
        self.z_ax_range.addWidget(label)
        item = QFloatLineEdit()
        try:
            item.set_value(z_ax_range[1])
        except:
            pass
        item.setFixedSize(60,30)
        self.z_ax_range.addWidget(item)
        self.ly.addLayout(self.z_ax_range)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('x tick freq')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(90,30)
        hb.addWidget(label)
        self.x_tick_freq = QtWidgets.QSpinBox()
        self.x_tick_freq.setFixedSize(50,30)
        try:
            self.x_tick_freq.setValue(x_tick_freq)
        except:
            pass
        hb.addWidget(self.x_tick_freq)
        label = QtWidgets.QLabel('y tick freq')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(90,30)
        hb.addWidget(label)
        self.y_tick_freq = QtWidgets.QSpinBox()
        self.y_tick_freq.setFixedSize(50,30)
        try:
            self.y_tick_freq.setValue(y_tick_freq)
        except:
            pass
        hb.addWidget(self.y_tick_freq)
        label = QtWidgets.QLabel('z tick freq')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label.setFixedSize(90,30)
        hb.addWidget(label)
        self.z_tick_freq = QtWidgets.QSpinBox()
        self.z_tick_freq.setFixedSize(50,30)
        try:
            self.z_tick_freq.setValue(z_tick_freq)
        except:
            pass
        hb.addWidget(self.z_tick_freq)
        self.ly.addLayout(hb)
        
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        label = QtWidgets.QLabel('Image Slice')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.slice = QtWidgets.QCheckBox()
        if lineSlice:
            self.slice.setCheckState(2)
        else:
            self.slice.setCheckState(0)
        hb.addWidget(self.slice)
        label = QtWidgets.QLabel('color map')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.colormap = QtWidgets.QComboBox()
        colormap = ['viridis', 'inferno', 'plasma', 'magma','Blues', 'BuGn', 'BuPu',
                 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd','PuBu', 'PuBuGn',
                 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu', 'YlOrBr',
                 'YlOrRd','afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat',
                 'gray', 'hot','pink', 'spring', 'summer', 'winter','BrBG', 'bwr',
                 'coolwarm', 'PiYG', 'PRGn', 'PuOr','RdBu', 'RdGy', 'RdYlBu',
                 'RdYlGn', 'Spectral','seismic','Accent', 'Dark2', 'Paired',
                 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3','Miscellaneous',
                 'gist_earth', 'terrain', 'ocean', 'gist_stern','brg', 'CMRmap',
                 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar','nipy_spectral',
                 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']
        self.colormap.addItems(colormap)
        self.colormap.setCurrentIndex(0)
        hb.addWidget(self.colormap)
        self.ly.addLayout(hb)
        
#        self.setFixedSize(500,600)
        self.setLayout(self.ly)
        
    def dimSelec2Slice(self, string):
        if string == '':
            return [slice(None),slice(None)]
        else:
            selection = list()
            for item in string.split(','):
                if item == ':':
                    selection.append(slice(None))
                elif item.find(':') != -1:
                    l = item.split(':')
                    if len(l)==2:
                        selection.append(slice(int(l[0]),int(l[1])))
                    elif len(l)== 3:
                        selection.append(slice(int(l[0]),int(l[1]),int(l[2])))
                    else:
                        selection.apend(slice(None))
                else:
                    try:
                        v = int(item)
                    except:
                        print('Given value for plot range is not interger. Set to 0.')
                        v = 0
                    selection.append(v)
            return selection
        
    def getValues(self):
        args = {}
        w = self.plotDims.itemAt(1).widget()
        dim0 = w.value()
        w = self.plotDims.itemAt(2).widget()
        if w.currentText() == 'none':
            selec0 = 0
        else:
            selec0 = w.currentIndex()
        w = self.plotDims.itemAt(4).widget()
        dim1 = w.value()
        w = self.plotDims.itemAt(5).widget()
        if w.currentText() == 'none':
            selec1 = 1
        else:
            selec1 = w.currentIndex()
        args['plotDims']=[[dim0, selec0], [dim1, selec1]]
        args['readout'] = self.readouts.currentText()
        args['pranges'] = self.dimSelec2Slice(self.pranges.text())
        args['factor'] = [self.factor.itemAt(i).widget().get_value() for i in range(1,6,2)]
        if self.showcolorBar.checkState() == 0:
            args['showColorbar'] = False
        else:
            args['showColorbar'] = True
        if self.showTitle.checkState() == 0:
            args['showTitle'] = False
        else:
            args['showTitle'] = True
        if self.showGrid.checkState() == 0:
            args['showGrid'] = False
        else:
            args['showGrid'] = True
        if self.flipX.checkState() == 0:
            args['flipX'] = False
        else:
            args['flipX'] = True
        if self.flipY.checkState() == 0:
            args['flipY'] = False
        else:
            args['flipY'] = True
        if self.transpose.checkState() == 0:
            args['transpose'] = False
        else:
            args['transpose'] = True
        args['xlabel'] = self.xlabel.text()
        args['ylabel'] = self.ylabel.text()
        args['zlabel'] = self.zlabel.text()
        try:
            xmin = self.x_ax_range.itemAt(1).widget().get_value()
            xmax = self.x_ax_range.itemAt(3).widget().get_value()
            args['x_ax_range'] = [xmin, xmax]
        except:
            args['x_ax_range'] = []
        try:
            ymin = self.y_ax_range.itemAt(1).widget().get_value()
            ymax = self.y_ax_range.itemAt(3).widget().get_value()
            args['y_ax_range'] = [ymin, ymax]
        except:
            args['y_ax_range'] = []
        try:
            ymin = self.z_ax_range.itemAt(1).widget().get_value()
            ymax = self.z_ax_range.itemAt(3).widget().get_value()
            args['z_ax_range'] = [ymin, ymax]
        except:
            args['z_ax_range'] = []
        args['x_tick_freq'] = self.x_tick_freq.value()
        args['y_tick_freq'] = self.y_tick_freq.value()
        args['z_tick_freq'] = self.z_tick_freq.value()
        args['colormap'] = self.colormap.currentText()#.encode('ascii')
        if self.slice.checkState() == 0:
            args['lineSlice'] = False
        else:
            args['lineSlice'] = True
        return args
        
class figureWindow(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 title='',
                 toolbar=True,
                 width=7,
                 height=5,
                 dpi=100,
                 ):
        super(figureWindow, self).__init__()
        self.ly = QtWidgets.QVBoxLayout()
        self.winTitle = title
        self.setWindowTitle(self.winTitle)
        self.fig = MyMplCanvas(parent=self,width=width,height=height,dpi=dpi)
        if toolbar:
            self.toolbar = NavigationToolbar(self.fig, self)
        self.clip = QtWidgets.QPushButton('clip')
        self.clip.clicked.connect(self.clipFigure)
        hb = QtWidgets.QHBoxLayout()
        if toolbar:
            hb.addWidget(self.toolbar)
        hb.addWidget(self.clip)
        self.ly.addWidget(self.fig)
        self.ly.addLayout(hb)
        self.setLayout(self.ly)
        
    def clipFigure(self):
        pixmap = self.fig.grab()
        QtWidgets.QApplication.clipboard().setPixmap(pixmap)
        
class plotWindow(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 ):
        super(plotWindow, self).__init__()
        # window list
        self.wlist = []
        # data list
        self.data = []
        # define main layout
        self.ly = QtWidgets.QVBoxLayout()
        # target window widgets
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('target window number')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.targetWin = QtWidgets.QSpinBox()
        self.targetWin.setRange(1,1000)
        self.targetWin.valueChanged.connect(self.newWindow)
        hb.addWidget(self.targetWin)
        self.ly.addLayout(hb)
        # create first target window
        w = figureWindow(title='Fig'+str(1))
        self.wlist.append(w)
        w.show()
        # file list
        self.flist = fileList(parent=self)
        self.flist.filterStr.setText('20*')
        self.flist.fileList.itemSelectionChanged.connect(self.updateUIs)
        self.ly.addWidget(self.flist)
        # reload and analyze button
        hb = QtWidgets.QHBoxLayout()
        self.reload = QtWidgets.QPushButton('reload')
        self.reload.clicked.connect(self.updateUIs)
        hb.addWidget(self.reload)
        self.analysisBtn = QtWidgets.QPushButton('analyze')
        self.analysisBtn.clicked.connect(self.analysis)
        hb.addWidget(self.analysisBtn)
        self.ly.addLayout(hb)
        # plot and add button
        hb = QtWidgets.QHBoxLayout()
        self.plotBtn = QtWidgets.QPushButton('plot')
        self.plotBtn.clicked.connect(self.plot)
        hb.addWidget(self.plotBtn)
        self.addBtn = QtWidgets.QPushButton('add')
        self.addBtn.clicked.connect(self.add)
        hb.addWidget(self.addBtn)
        self.ly.addLayout(hb)
        # analysis widget
        self.analysis = aw.AnalysisPanelWidget()
        self.ly.addWidget(self.analysis)
        # some check boxes
        # plot and add button
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Back to raw after analysis.')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.returnAnalysis = QtWidgets.QCheckBox()
        hb.addWidget(self.returnAnalysis)
        self.ly.addLayout(hb)
        
        #tab for plot information
        self.tab = QtWidgets.QTabWidget()
        # information for 1D plot
        sc = QtWidgets.QScrollArea()
        self.plotInfo1D = plotInfo1D()
        sc.setWidget(self.plotInfo1D)
        self.tab.addTab(sc, '1d plot')
        # information for 2D plot
        sc = QtWidgets.QScrollArea()
        self.plotInfo2D = plotInfo2D()
        sc.setWidget(self.plotInfo2D)
        self.tab.addTab(sc, '2d plot')
        # ipython console to perform analysis
        self.console = ipy.AnalysisWidget()
        self.console.ipyConsole.pushVariables({'aw':self})
        self.tab.addTab(self.console, 'console')
        
        self.ly.addWidget(self.tab)
        
        self.setLayout(self.ly)
        
        # configure window
        self.config = figureWindow(title='config',toolbar=False,width=6,height=5,dpi=100)
        self.config.show()
        
        #test
        
        
    def newWindow(self):
        value = self.targetWin.value()
        try:
            ind = [i.winTitle for i in self.wlist].index('Fig'+str(value))
            self.wlist[ind].show()
        except:
            w = figureWindow(title='Fig'+str(value))
            self.wlist.append(w)
            w.show()
        
    def updateUIs(self):
        # get data list
        self.data = []
        if not self.flist.fileList.selectedItems()==[]:
            for data in self.flist.fileList.selectedItems():
                expdata = ExpData(filename = data.text().split('.')[0],
                                  path = self.flist.folderPath.text()+'/'
                                  )
                expdata.readData()
                self.data.append(expdata)
            # update config to the 1st selected data
            self.config.fig.fig.clf()
            axes = []
            gs = gridspec.GridSpec(3,1)
            axes.append(self.config.fig.fig.add_subplot(gs[:2,0]))
            axes.append(self.config.fig.fig.add_subplot(gs[2:,0]))
            self.config.fig.axes = axes
            self.data[0].getGateConfig(axes=self.config.fig.axes)
            self.config.fig.draw()
            # update 1D plot info
            self.plotInfo1D.sweeps.clear()
            self.plotInfo1D.sweeps.addItems(self.data[0].sweepnamelist)
            self.plotInfo1D.readouts.items = list(self.data[0].readoutnamelist)
            for i in range(self.plotInfo1D.readouts.c):
                self.plotInfo1D.readouts.sub2.itemAt(i).widget().clear()
                self.plotInfo1D.readouts.sub2.itemAt(i).widget().addItems(self.data[0].readoutnamelist)
                self.plotInfo1D.readouts.sub2.itemAt(i).widget().setCurrentIndex(i)
            # update 2D plot info
#            self.plotInfo2D.plotDims.itemAt(1).widget().setRange(0,len(self.data[0].data.shape)-2)
#            self.plotInfo2D.plotDims.itemAt(4).widget().setRange(0,len(self.data[0].data.shape)-2)
            self.plotInfo2D.plotDims.itemAt(2).widget().clear()
            self.plotInfo2D.plotDims.itemAt(2).widget().addItems(self.data[0].sweepnamelist)
            self.plotInfo2D.plotDims.itemAt(5).widget().clear()
            self.plotInfo2D.plotDims.itemAt(5).widget().addItems(self.data[0].sweepnamelist)
            self.plotInfo2D.readouts.clear()
            self.plotInfo2D.readouts.addItems(self.data[0].readoutnamelist)
            
    def updateListUIs(self, expdata=ExpData()):
        self.plotInfo1D.sweeps.clear()
        self.plotInfo1D.sweeps.addItems(expdata.sweepnamelist)
        self.plotInfo1D.readouts.items = list(expdata.readoutnamelist)
        for i in range(self.plotInfo1D.readouts.c):
            self.plotInfo1D.readouts.sub2.itemAt(i).widget().clear()
            self.plotInfo1D.readouts.sub2.itemAt(i).widget().addItems(expdata.readoutnamelist)
            self.plotInfo1D.readouts.sub2.itemAt(i).widget().setCurrentIndex(i)
        
        self.plotInfo2D.plotDims.itemAt(2).widget().clear()
        self.plotInfo2D.plotDims.itemAt(2).widget().addItems(expdata.sweepnamelist)
        self.plotInfo2D.plotDims.itemAt(5).widget().clear()
        self.plotInfo2D.plotDims.itemAt(5).widget().addItems(expdata.sweepnamelist)
        self.plotInfo2D.readouts.clear()
        self.plotInfo2D.readouts.addItems(expdata.readoutnamelist)
    
    def plot(self):
        wNo = self.targetWin.value()
        ind = [i.winTitle for i in self.wlist].index('Fig'+str(wNo))
        w = self.wlist[ind]
        w.fig.fig.clf()
        w.fig.fig.set_facecolor('#ffffff')
        w.fig.axes = w.fig.fig.add_subplot(111)
        ax = w.fig.axes
            
        try:
            for i, d in enumerate(self.data):
                sweeplist = d.sweepnamelist
                readoutlist = d.readoutnamelist
                d = self.analysis.executeAnalysis(d)
                if (sweeplist != d.sweepnamelist) or (readoutlist != d.readoutnamelist): # update list in UI if there is some change in the analysis.
                    self.updateListUIs(d)
                self.data[i] = d
                if self.tab.currentIndex() == 0:
                    args = self.plotInfo1D.getValues()
                    d.plot1D(ax=ax, # ax to be plotted data
                           clear = False, # clear the existing plot in the 'ax'
                           useCounter = args['useCounter'],
                           showlegend = args['showlegend'], showTitle = args['showTitle'], showGrid = args['showGrid'],
                           title = d.filename, # set title
                           plotaxis = args['pDim'], # plot along 
                           plotrange=args['pranges'], # plot range ex.) [slice(0,100), slice(None), Ellipsis, 0]
                           readouts = args['readouts'], # select plot readout by name or number
                           xaxis = args['sweep'], #0, 1, 2 or 'name' of axis
                           xoffsets=[], yoffsets=args['y offsets'], # offset for x and y
                           xfactor=args['factor'][0], yfactor=args['factor'][1], # factor to multiply
                           xlabel = args['xlabel'],   ylabel = args['ylabel'],
                           x_axis_range=args['x_ax_range'], y_axis_range=args['y_ax_range'],
                           x_tick_freq=args['x_tick_freq'], y_tick_freq=args['y_tick_freq'],
                           xticks=[], yticks=[],
                           ticklabelsize = 12, labelsize = 14, linewidth = 1.0,
                           )
                elif self.tab.currentIndex() == 1:
                    args = self.plotInfo2D.getValues()
                    d.plot2D(fig = w.fig.fig,
                           ax = ax,                                                        # plot data into given ax
                           plotDims = args['plotDims'],                                        # plot axis [[x, choice], [y, choice]]
                           readout=args['readout'],                                                     # name of readout instrument that should be plotted on z-axis
                           plotrange= args['pranges'],                                                    # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                           factors = args['factor'],                                         # scaling factor for x, y and z
                           clear = False,                                                   # clear previous plot or not
                           showColorbar = args['showColorbar'], showTitle = args['showTitle'], showGrid = args['showGrid'],
                           flipX = args['flipX'], flipY = args['flipY'], transpose = args['transpose'],
                           xlabel = args['xlabel'],   ylabel = args['ylabel'],   zlabel = args['zlabel'],
                           x_ax_range=args['x_ax_range'], y_ax_range=args['y_ax_range'], z_ax_range=args['z_ax_range'],
                           x_tick_freq=args['x_tick_freq'], y_tick_freq=args['y_tick_freq'], z_tick_freq=args['z_tick_freq'],
                           xticks=[],     yticks=[],     zticks=[],
                           ticklabelsize = 12, labelsize = 14,
                           colormap = args['colormap'], lineSlice = args['lineSlice'], pyqt = True,
                           )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        w.fig.fig.tight_layout()
        w.fig.draw()
        w.activateWindow()
        # update config
        self.config.fig.fig.clf()
        axes = []
        gs = gridspec.GridSpec(3,1)
        axes.append(self.config.fig.fig.add_subplot(gs[:2,0]))
        axes.append(self.config.fig.fig.add_subplot(gs[2:,0]))
        self.config.fig.axes = axes
        try:
            self.data[0].getGateConfig(axes=self.config.fig.axes)
            self.config.fig.draw()
        except:
            'This file has not been measured yet.'
        # return analysis selection to raw
        if self.returnAnalysis.checkState() != 0:
            self.analysis.method_selection.setCurrentIndex(0)
    
    def add(self):
        wNo = self.targetWin.value()
        ind = [i.winTitle for i in self.wlist].index('Fig'+str(wNo))
        w = self.wlist[ind]
        ax = w.fig.axes
        xlim = ax.get_xlim() # store x axis limits
        ylim = ax.get_ylim() # store y axis limits
        try:
            for i, d in enumerate(self.data):
                sweeplist = d.sweepnamelist
                readoutlist = d.readoutnamelist
                d = self.analysis.executeAnalysis(d)
                if (sweeplist != d.sweepnamelist) or (readoutlist != d.readoutnamelist):  # update list in UI if there is some change in the analysis.
                    self.updateListUIs(d)
                self.data[i] = d
                if self.tab.currentIndex() == 0:
                    args = self.plotInfo1D.getValues()
                    d.plot1D(ax=ax, # ax to be plotted data
                               clear = False, # clear the existing plot in the 'ax'
                               useCounter = args['useCounter'],
                               showlegend = args['showlegend'], showTitle = args['showTitle'], showGrid = args['showGrid'],
                               title = d.filename, # set title
                               plotaxis = args['pDim'], # plot along 
                               plotrange=args['pranges'], # plot range ex.) [slice(0,100), slice(None), Ellipsis, 0]
                               readouts = args['readouts'], # select plot readout by name or number
                               xaxis = args['sweep'], #0, 1, 2 or 'name' of axis
                               xoffsets=[], yoffsets=args['y offsets'], # offset for x and y
                               xfactor=args['factor'][0], yfactor=args['factor'][1], # factor to multiply
                               xlabel = args['xlabel'],   ylabel = args['ylabel'],
                               x_axis_range=args['x_ax_range'], y_axis_range=args['y_ax_range'],
                               x_tick_freq=args['x_tick_freq'], y_tick_freq=args['y_tick_freq'],
                               xticks=[], yticks=[],
                               ticklabelsize = 12, labelsize = 14, linewidth = 1.0,
                               )
                elif self.tab.currentIndex() == 1:
                    w.fig.fig.clf()
                    w.fig.fig.set_facecolor('#ffffff')
                    w.fig.axes = w.fig.fig.add_subplot(111)
                    args = self.plotInfo2D.getValues()
                    d.plot2D(fig = w.fig.fig,
                               ax = ax,                                                        # plot data into given ax
                               plotDims = args['plotDims'],                                        # plot axis [[x, choice], [y, choice]]
                               readout=args['readout'],                                                     # name of readout instrument that should be plotted on z-axis
                               plotrange= args['pranges'],                                                    # plotting ranges [ range for sweep, step 1, etc.]; should give a matrix!!
                               factors = args['factor'],                                         # scaling factor for x, y and z
                               clear = False,                                                   # clear previous plot or not
                               showColorbar = args['showColorbar'], showTitle = args['showTitle'], showGrid = args['showGrid'],
                               flipX = args['flipX'], flipY = args['flipY'], transpose = args['transpose'],
                               xlabel = args['xlabel'],   ylabel = args['ylabel'],   zlabel = args['zlabel'],
                               x_ax_range=args['x_ax_range'], y_ax_range=args['y_ax_range'], z_ax_range=args['z_ax_range'],
                               x_tick_freq=args['x_tick_freq'], y_tick_freq=args['y_tick_freq'], z_tick_freq=args['z_tick_freq'],
                               xticks=[],     yticks=[],     zticks=[],
                               ticklabelsize = 12, labelsize = 14,
                               colormap = args['colormap'], lineSlice = args['lineSlice'], pyqt = True
                               )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        xlim2 = ax.get_xlim() # get new x axis limits
        ylim2 = ax.get_ylim() # get new y axis limit
        ax.set_xlim(min(xlim[0],xlim2[0]), max(xlim[1],xlim2[1])) # set x axis limits from the 2 configurations
        ax.set_ylim(min(ylim[0],ylim2[0]), max(ylim[1],ylim2[1])) # set y axis limits from the 2 configurations
        w.fig.fig.tight_layout()
        w.fig.draw()
        w.activateWindow()
        # update config
        self.config.fig.fig.clf()
        axes = []
        gs = gridspec.GridSpec(3,1)
        axes.append(self.config.fig.fig.add_subplot(gs[:2,0]))
        axes.append(self.config.fig.fig.add_subplot(gs[2:,0]))
        self.config.fig.axes = axes
        if self.data[0].InitialPositions != []:
            self.data[0].getGateConfig(axes=self.config.fig.axes)
            self.config.fig.draw()
        # return analysis selection to raw
        if self.returnAnalysis.checkState() != 0:
            self.analysis.method_selection.setCurrentIndex(0)
    
    def analysis(self):
        for i, d in enumerate(self.data):
            sweeplist = d.sweepnamelist
            readoutlist = d.readoutnamelist
            d = self.analysis.executeAnalysis(d)
            if (sweeplist != d.sweepnamelist) or (readoutlist != d.readoutnamelist):  # update list in UI if there is some change in the analysis.
                self.updateListUIs(d)
            self.data[i] = d
        # update config
        self.config.fig.fig.clf()
        axes = []
        gs = gridspec.GridSpec(3,1)
        axes.append(self.config.fig.fig.add_subplot(gs[:2,0]))
        axes.append(self.config.fig.fig.add_subplot(gs[2:,0]))
        self.config.fig.axes = axes
        if self.data[0].InitialPositions != []:
            self.data[0].getGateConfig(axes=self.config.fig.axes)
            self.config.fig.draw()
        # return analysis selection to raw
        if self.returnAnalysis.checkState() != 0:
            self.analysis.method_selection.setCurrentIndex(0)
        
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
#    fl = fileList()
#    fl.show()
    pi = plotWindow()
    pi.show()
#    td = twoDgui()
#    td.show()
#    od = oneDgui()
#    od.show()
    sys.exit(app.exec_())
    