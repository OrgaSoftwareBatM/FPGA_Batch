#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 22:18:54 2016

@author: shintaro
"""

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(0,'..')
import os
import h5py
import time
import GUI.IpythonWidgetClass as IpyConsole
from GUI.UtilityGUI import *
from MeasurementBase.measurement_classes import *

pathSep = QtCore.QDir.separator()
init_param_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})

# global List of instruments
ginst_list = ['ADC','K2000','34401A','None','DAC','DAC_Lock_in','RF','AWG','None','Fast sequence']
ginst_list+= ['Fast sequence slot','command line','DSP_Lock_in','DSP_Lock_in_sweep','ms2wait','ATMDelayLine']
ginst_list+= ['RF_Attn','FPGA_ADC']

class FileNameCheck(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 ):
        super(FileNameCheck, self).__init__()
        self.okBtn = QtWidgets.QPushButton('OK')
        self.okBtn.clicked.connect(self.okProc)
        hb = QtWidgets.QHBoxLayout()
        hb.addWidget(self.okBtn)
        label = QtWidgets.QLabel('File name already exists. File creation is cancelled.')
        vb = QtWidgets.QVBoxLayout()
        vb.addWidget(label)
        vb.addLayout(hb)
        self.setLayout(vb)
            
    def okProc(self):
        self.close()
     
#"""-------------------------------------------
    #classes for setup of each instruments
    #(You have to add new class if you add a new instrument)
    #----------------------------------------------"""
    #class inst_setup_base(QtWidgets.QWidget):
    #    def __init__(self,
    #                 parent=None,
    #                 ):
    #        super(inst_setup_base, self).__init__()
    #        # inst_setup_UI will be given as parent.
    #        self.parent = parent
    #        self.w = None
    #        
    #    def setUI2LayoutAndList(self, UIList, layout, name, initparam, selections=None, dialogBtn=False, function=None):
    #        """ Setup GUI to instrument setup UI """
    #        hb = QtWidgets.QHBoxLayout()        # Layout to store the UI
    #        hb.addWidget(QtWidgets.QLabel(name))    # label
    #        if type(selections) == list:
    #            self.w = QtWidgets.QComboBox()
    #            self.w.addItems(selections)
    #            self.w.setCurrentIndex(int(initparam))
    #            hb.addWidget(self.w)
    #        else:
    #            if type(initparam) == str:
    #                self.w = QtWidgets.QLineEdit()
    #                self.w.setText(initparam)
    #                hb.addWidget(self.w)
    #                if dialogBtn:
    #                    dBtn = QtWidgets.QPushButton('...')
    #                    dBtn.clicked.connect(self.folderDialog)
    #                    hb.addWidget(dBtn)
    #            elif type(initparam)==int:
    #                self.w = QtWidgets.QSpinBox()
    #                self.w.setRange(0, 10000000)
    #                self.w.setValue(initparam)
    #                if not function == None:
    #                    self.w.valueChanged.connect(function)
    #                hb.addWidget(self.w)
    #            elif type(initparam)==float:
    #                self.w = QFloatLineEdit()
    #                self.set_value(initparam)
    #                hb.addWidget(self.w)
    #            elif type(initparam)==bool:
    #                self.w = QtWidgets.QCheckBox()
    #                if initparam:
    #                    self.w.setCheckState(2)
    #                else:
    #                    self.w.setCheckState(0)
    #                hb.addWidget(self.w)
    #            elif type(initparam)==list:
    #                self.w = []
    #                for p in initparam:
    #                    if type(p)==int:
    #                        w = QtWidgets.QSpinBox()
    #                        w.setRange(0, 10000000)
    #                        w.setValue(p)
    #                    elif type(p)==str:
    #                        w = QtWidgets.QLineEdit()
    #                        w.setText(p)
    #                    elif type(p)==float:
    #                        w = QFloatLineEdit()
    #                        w.set_value(p)
    #                    elif type(p)==bool:
    #                        w = QtWidgets.QCheckBox()
    #                        if p:
    #                            w.setCheckState(2)
    #                        else:
    #                            w.setCheckState(0)
    #                    self.w.append(w)
    #                    hb.addWidget(w)
    #                    
    #        UIList.append(self.w)
    #        layout.addLayout(hb)
    #
    #    def folderDialog(self):
    #        """ Open dialog to select folder and insert it into the given line edit """
    #        fileDialog = QtWidgets.QFileDialog(self)
    #        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
    #        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
    #        savePath = fileDialog.getExistingDirectory(self, 'Choose folder')    
    #        if not savePath == '':
    #            savePath = os.path.abspath(savePath)
    #            savePath += pathSep
    #        self.w.setText(savePath)
    #    
    #class ADC_setup(inst_setup_base):
    #    def __init__(self,
    #                 parent=None,
    #                 ):
    #        super(ADC_setup, self).__init__()
    #        # inst_setup_UI will be given as parent.
    #        self.parent = parent
    ##        self.parent = inst_setup_UI()   # temporal
    #        self.ly = QtWidgets.QVBoxLayout()
    #        self.UIs = []
    #        self.initUI()
    #        self.setLayout(self.ly)
    #        self.show()
    #        
    #    def initUI(self):
    #        if self.parent.item == 0:
    #            self.parent.item = ADC()
    ##        UIs = self.parent.UIs
    #        UIs = self.UIs
    ##        ly = self.parent.ly
    #        ly = self.ly
    #        item = self.parent.item
    #        self.setUI2LayoutAndList(UIs, ly, 'name', item.strings[0])
    #        self.setUI2LayoutAndList(UIs, ly, 'unit', item.strings[2])
    #        self.setUI2LayoutAndList(UIs, ly, 'No of ch', item.uint64s[1], function=self.adcSetup)
    ##        UIs[2].valueChanged.connect(self.adcSetup)
    #        self.setUI2LayoutAndList(UIs, ly, 'Name list', item.strings[3].split(';'))
    #        self.setUI2LayoutAndList(UIs, ly, 'Unit list', item.strings[4].split(';'))
    #        self.setUI2LayoutAndList(UIs, ly, 'Conversion factor list', [float(v) for v in item.strings[5].split(';')])
    #        self.setUI2LayoutAndList(UIs, ly, 'range', [0,1,5,10].index(item.uint64s[0]), ['+/-0.2V','+/-1V','+/-5V','+/-10V'])
    #        self.setUI2LayoutAndList(UIs, ly, 'sampling rate', item.uint64s[2])
    #        self.setUI2LayoutAndList(UIs, ly, 'real time avg on?', int(item.uint64s[3])!= 0)
    #        self.setUI2LayoutAndList(UIs, ly, 'real time average points', item.uint64s[4])
    #        self.setUI2LayoutAndList(UIs, ly, 'Inp config', [-1,10083,10078,10106,12529].index(item.uint64s[5]), ['default','RSE','NRSE','Differential','Pseudodifferential'])
    #        self.setUI2LayoutAndList(UIs, ly, 'Buffer size', item.uint64s[6])
    #        self.setUI2LayoutAndList(UIs, ly, 'ramp trigger input', item.uint64s[8])
    #        self.setUI2LayoutAndList(UIs, ly, 'fast trigger input', item.uint64s[9])
    #        
    #    def adcSetup(self, noOfchannel):
    #        print(noOfchannel)
    #        for i in range(3):
    #            ly = self.parent.ly.itemAt(i+3).layout()
    #            for j in range(ly.count()):
    #                ly.itemAt(j).widget().deleteLater()
    #        
    #        hb = QtWidgets.QHBoxLayout()
    #        label = QtWidgets.QLabel('Name list')
    #        hb.addWidget(label)
    #        wlist = []
    #        for i in range(noOfchannel):
    #            item = QtWidgets.QLineEdit()
    #            item.setText('ADC'+str(i))
    #            wlist.append(item)
    #            hb.addWidget(item)
    #        self.parent.UIs[3] = wlist
    #        self.parent.ly.insertLayout(3,hb)
    #        
    #        hb = QtWidgets.QHBoxLayout()
    #        label = QtWidgets.QLabel('Unit list')
    #        hb.addWidget(label)
    #        wlist = []
    #        for i in range(noOfchannel):
    #            item = QtWidgets.QLineEdit()
    #            item.setText('V')
    #            wlist.append(item)
    #            hb.addWidget(item)
    #        self.parent.UIs[4] = wlist
    #        self.parent.ly.insertLayout(4,hb)
    #        
    #        hb = QtWidgets.QHBoxLayout()
    #        label = QtWidgets.QLabel('Conversion factor list')
    #        hb.addWidget(label)
    #        wlist = []
    #        for i in range(noOfchannel):
    #            item = QFloatLineEdit()
    #            item.set_value(1.0)
    #            wlist.append(item)
    #            hb.addWidget(item)
    #        self.parent.UIs[5] = wlist
    #        self.parent.ly.insertLayout(5,hb)
            

"""---------------------------------
classes for fast sequence setup
------------------------------------"""
class FastSlotUI(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 selection = 0, #{'fast channel':0,'trigger':1,'timing':2,'jump':3}
                 fast_channel = 0,
                 value = 0,
                 ):
        super(FastSlotUI, self).__init__()
        singleHight = 40
        self.selection = QtWidgets.QComboBox()
        self.selection.addItems(['fast channel','trigger','timing','jump'])
        self.selection.setCurrentIndex(selection)
        self.selection.currentIndexChanged.connect(self.updateUI)
        self.selection.setFixedSize(110,singleHight)
        self.fast_channel = fast_channel
        self.fast_channelUI = QtWidgets.QSpinBox()
        self.fast_channelUI.setRange(0,15)
        self.fast_channelUI.setFixedSize(20,singleHight)
        self.value = value
        self.valueUI = QFloatLineEdit()
        self.valueUI.setFixedSize(70,singleHight)
        self.ly = QtWidgets.QHBoxLayout()
        self.ly.addWidget(self.selection)
        self.ly.setSpacing(0)
        self.Triggers = []
        self.setupUI()
        self.setLayout(self.ly)
        self.setFixedSize(400,singleHight+20)
        
    def setupUI(self):
        singleHight = 40
        selec = self.selection.currentIndex()
        if selec == 0:
            fastChannel_label = QtWidgets.QLabel('fast channel')
            fastChannel_label.setFixedSize(100,singleHight)
            self.fast_channelUI = QtWidgets.QSpinBox()
            self.fast_channelUI.setRange(0,15)
            self.fast_channelUI.setValue(self.fast_channel)
            value_label = QtWidgets.QLabel('shift value')
            value_label.setFixedSize(70,singleHight)
            self.valueUI = QFloatLineEdit()
            self.valueUI.set_value(self.value)
            self.ly.addWidget(fastChannel_label)
            self.ly.addWidget(self.fast_channelUI)
            self.ly.addWidget(value_label)
            self.ly.addWidget(self.valueUI)
        elif selec == 1:
            labels = [QtWidgets.QLabel('1'),QtWidgets.QLabel('2'),QtWidgets.QLabel('3'),QtWidgets.QLabel('4'),QtWidgets.QLabel('stop')]
            self.Triggers = []
            value = int(self.value)
            for i in range(5):
                labels[i].setFixedSize(30,singleHight)
                self.ly.addWidget(labels[i])
                checkbox = QtWidgets.QCheckBox()
                checkbox.setFixedSize(30,singleHight)
                self.Triggers.append(checkbox)
                self.ly.addWidget(self.Triggers[i])
                if not (value & 2**i) == 0:
                    self.Triggers[i].setCheckState(2)
                else:
                    self.Triggers[i].setCheckState(0)
        elif selec == 2:
            label = QtWidgets.QLabel('timing (ms)')
            label.setFixedSize(100,singleHight)
            self.valueUI = QFloatLineEdit()
            self.valueUI.set_value(self.value)
            self.ly.addWidget(label)
            self.ly.addWidget(self.valueUI)
        else:
            label = QtWidgets.QLabel('Jump to')
            label.setFixedSize(70,singleHight)
            self.valueUI = QFloatLineEdit()
            self.valueUI.set_value(int(self.value))
            self.ly.addWidget(label)
            self.ly.addWidget(self.valueUI)
            
    def updateUI(self):
        for i in reversed(range(self.ly.count()-1)):
            self.ly.itemAt(i+1).widget().deleteLater()
            self.ly.removeItem(self.ly.itemAt(i+1))
        self.ly.addWidget(self.selection)
        self.setupUI()
        
    def readValue(self):
        selec = selec = self.selection.currentIndex()
        if selec == 0:
            param = self.fast_channelUI.value()
            value = self.valueUI.get_value()
        elif selec == 1:
            param = 101
            value = 0
            for i in range(5):
                if not self.Triggers[i].checkState()==0:
                    value += 2**i
        elif selec == 2:
            param = 102
            value = self.valueUI.get_value()
        else:
            param = 103
            value = int(self.valueUI.get_value())
        return [param, value]  
        
class FastSequenceUI(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 fastSeq = np.zeros((2,10)),
                 ):
        super(FastSequenceUI, self).__init__()
        self.fastSeq = fastSeq
        self.UIs = []
        
        self.seqSize = QtWidgets.QSpinBox()
        self.seqSize.setRange(0,4095)
        self.seqSize.setValue(self.fastSeq.shape[1])
        self.seqSize.setFixedSize(60,30)
        self.Index = QtWidgets.QSpinBox()
        self.Index.setRange(0,4095)
        self.Index.setFixedSize(60,30)
        self.insertBtn = QtWidgets.QPushButton('Insert')
        self.insertBtn.clicked.connect(self.insertUI)
        self.insertBtn.setFixedSize(70,30)
        self.removeBtn = QtWidgets.QPushButton('Remove')
        self.removeBtn.clicked.connect(self.removeUI)
        self.removeBtn.setFixedSize(70,30)
        hbl = QtWidgets.QHBoxLayout()
        hbl.setSpacing(0)
        hbl.addWidget(self.Index)
        hbl.addWidget(self.insertBtn)
        hbl.addWidget(self.removeBtn)
        
        self.seqIndex = QtWidgets.QVBoxLayout()
        self.seqIndex.setSpacing(0)
        self.sequence = QtWidgets.QVBoxLayout()
        self.sequence.setSpacing(0)
        seqLayout = QtWidgets.QHBoxLayout()
        seqLayout.setSpacing(0)
        seqLayout.addLayout(self.seqIndex)
        seqLayout.addLayout(self.sequence)
        
        main = QtWidgets.QVBoxLayout()
        main.setSpacing(0)
        main.addWidget(self.seqSize)
        main.addLayout(hbl)
        main.addLayout(seqLayout)
        
        self.w = QtWidgets.QWidget()
        self.w.setLayout(main)
        self.w.setFixedSize(450,70+60*self.seqSize.value())
        container = QtWidgets.QScrollArea()
        container.setWidget(self.w)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(container)
        self.setLayout(layout)
        
        self.loadUIs()
    
    # set UIs from self.UIs
    def initUI(self):
        pass
                
    # load UIs in terms of self.fastSeq (suppose no UI before)
    def loadUIs(self):
        size = self.fastSeq.shape[1]
        self.seqSize.setValue(size)
        self.w.setFixedSize(450,100+60*self.seqSize.value())
        if not size == 0:
            self.UIs = [] # To make sure self.UIs is empty
            for i in range(size):
                parameter = self.fastSeq[0,i]
                parameter = max(0, parameter)
                value = self.fastSeq[1,i]
                if parameter<16:
                    item = FastSlotUI(selection = 0,
                                     fast_channel = parameter,
                                     value = value,
                                     )
                elif parameter == 101:
                    item = FastSlotUI(selection = 1,
                                     fast_channel = 0,
                                     value = value,
                                     )
                elif parameter == 102:
                    item = FastSlotUI(selection = 2,
                                     fast_channel = 0,
                                     value = value,
                                     )
                else:
                    item = FastSlotUI(selection = 3,
                                     fast_channel = 0,
                                     value = value,
                                     )
                self.UIs.append(item)
                counter = QtWidgets.QLabel(str(i))
                counter.setFixedSize(40,60)
                self.seqIndex.addWidget(counter)
                self.sequence.addWidget(item)
    
    # Store current configuration into self.fastSeq from self.UIs
    def readUIs(self):
        self.fastSeq = np.zeros((2,len(self.UIs)))
        for i,item in enumerate(self.UIs):
            self.fastSeq[:,i]=item.readValue()
        
    # Insert UI to indicated index
    def insertUI(self):
        index = self.Index.value()
        item = FastSlotUI()
        self.UIs.insert(index,item)
        self.sequence.insertWidget(index,item)
        size = self.seqSize.value()
        counter = QtWidgets.QLabel(str(size))
        counter.setFixedSize(40,60)
        self.seqIndex.addWidget(counter)
        self.seqSize.setValue(size+1)
        self.w.setFixedSize(450,100+60*self.seqSize.value())
        
    # Remove UI from indicated index
    def removeUI(self):
        index = self.Index.value()
        del self.UIs[index]
        self.sequence.itemAt(index).widget().deleteLater()
        self.sequence.removeItem(self.sequence.itemAt(index))
        size = self.seqSize.value()
        self.seqIndex.itemAt(size-1).widget().deleteLater()
        self.seqIndex.removeItem(self.seqIndex.itemAt(size-1))
        self.seqSize.setValue(size-1)
        self.w.setFixedSize(450,100+60*self.seqSize.value())
        
class FastSeqModUI(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 sequenceUI = 0,
                 ):
        super(FastSeqModUI, self).__init__()
        self.tab = QtWidgets.QTabWidget()
        self.sequence = np.zeros((2,10))
        
        if sequenceUI == 0:
            self.seqUI = FastSequenceUI()
        else:
            self.seqUI = sequenceUI
        self.okBtn = QtWidgets.QPushButton('OK')
        self.okBtn.clicked.connect(self.okProc)
        subly = QtWidgets.QVBoxLayout()
        subly.addWidget(self.seqUI)
        subly.addWidget(self.okBtn)
        w1 = QtWidgets.QWidget()
        w1.setLayout(subly)
        self.tab.addTab(w1, 'fast seq UI')
        
        self.console = IpyConsole.IpyConsoleWidget()
        self.console.ipyConsole.pushVariables({'fs':self})
        #import fast frequency generation file
        self.console.ipyConsole.executeCommand('from MeasurementBase.FastSequenceGenerator import *')
        self.setSeqBtn = QtWidgets.QPushButton('set')
        self.setSeqBtn.clicked.connect(self.setSeqProc)
        subly = QtWidgets.QVBoxLayout()
        subly.addWidget(self.console)
        subly.addWidget(self.setSeqBtn)
        w1 = QtWidgets.QWidget()
        w1.setLayout(subly)
        self.tab.addTab(w1, 'Edit console')
        
        
        mainly = QtWidgets.QVBoxLayout()
        mainly.addWidget(self.tab)
        
        self.setLayout(mainly)
        
        
    def okProc(self):
        self.close()
    
    def setSeqProc(self):
        # clean up all the old UIs and create new one
        for i in reversed(range(self.seqUI.seqIndex.count())):
            self.seqUI.seqIndex.itemAt(i).widget().deleteLater()
            self.seqUI.seqIndex.removeItem(self.seqUI.seqIndex.itemAt(i))
            self.seqUI.sequence.itemAt(i).widget().deleteLater()
            self.seqUI.sequence.removeItem(self.seqUI.sequence.itemAt(i))
        self.seqUI.fastSeq = self.sequence
        self.seqUI.loadUIs()
        
class inst_setup_UI(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 kind = 0,
                 ):
        super(inst_setup_UI, self).__init__()
        if parent != None:
            self.name = parent.setState
            self.item = parent.item
        else:
            self.name = ''
            self.item = 0
            
        self.kind = kind
        
        self.UIs = []
        self.okBtn = QtWidgets.QPushButton('OK')
        self.okBtn.clicked.connect(self.ok_proc)
        self.ly = QtWidgets.QVBoxLayout()
        
        self.initUI()
        
        self.ly.addWidget(self.okBtn)
        self.widget = QtWidgets.QWidget(parent=self)
        self.widget.setLayout(self.ly)
        container = QtWidgets.QScrollArea()
        container.setWidget(self.widget)
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(container)
        self.setLayout(lay)
        self.widget.setFixedSize(400,40*(len(self.UIs)+1))
        
    def __call__(self):
        if self.kind != self.item.kind:
            self.item = 0
        count = self.ly.count()
        for i in reversed(range(count-1)):
            layout = self.ly.itemAt(i).layout()
            for j in reversed(range(layout.count())):
                layout.itemAt(j).widget().deleteLater()
        self.ly.itemAt(count-1).widget().deleteLater()
        for i in reversed(range(self.ly.count())):
            self.ly.removeItem(self.ly.itemAt(i))
        self.UIs = []
        self.okBtn = QtWidgets.QPushButton('OK')
        self.okBtn.clicked.connect(self.ok_proc)
        self.initUI()
        self.ly.addWidget(self.okBtn)
        self.widget.setFixedSize(400,40*(len(self.UIs)+1))
    
    def adcSetup(self, noOfchannel):
        for i in range(3):
            ly = self.ly.itemAt(i+3).layout()
            for j in range(ly.count()):
                ly.itemAt(j).widget().deleteLater()
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Name list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QLineEdit()
            item.setText('ADC'+str(i))
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[3] = wlist
        self.ly.insertLayout(3,hb)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Unit list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QLineEdit()
            item.setText('V')
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[4] = wlist
        self.ly.insertLayout(4,hb)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Conversion factor list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QFloatLineEdit()
            item.set_value(1.0)
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[5] = wlist
        self.ly.insertLayout(5,hb)
        
    def fpga_adc_Setup(self, noOfchannel):
        for i in range(6):
            ly = self.ly.itemAt(i+2).layout()
            for j in range(ly.count()):
                ly.itemAt(j).widget().deleteLater()
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Name list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QLineEdit()
            item.setText('ADC'+str(i))
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[2] = wlist
        self.ly.insertLayout(2,hb)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Unit list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QLineEdit()
            item.setText('V')
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[3] = wlist
        self.ly.insertLayout(3,hb)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Conversion factor list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QFloatLineEdit()
            item.set_value(1.0)
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[4] = wlist
        self.ly.insertLayout(4,hb)
            
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Input channels list')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QSpinBox()
            item.setRange(0,31)
            item.setValue(i)
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[5] = wlist
        self.ly.insertLayout(5,hb)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Range List')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QComboBox()
            item.addItems(['+/-0.2V','+/-1V','+/-5V','+/-10V'])
            item.setCurrentIndex(0)
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[6] = wlist
        self.ly.insertLayout(6,hb)
        
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Term List')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QComboBox()
            item.addItems(['RSE','NRSE','DIFF'])
            item.setCurrentIndex(2)
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[7] = wlist
        self.ly.insertLayout(7,hb)

    def awgSetup(self, noOfchannel):
        for i in range(10):
            ly = self.ly.itemAt(i+10).layout()
            for j in range(ly.count()):
                ly.itemAt(j).widget().deleteLater()
            
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('ch output on?')
        hb.addWidget(label)
        wlist = []
        for i in range(noOfchannel):
            item = QtWidgets.QCheckBox()
            wlist.append(item)
            hb.addWidget(item)
        self.UIs[10] = wlist
        self.ly.insertLayout(10,hb)
        
        name_list = ['amplitude (V)','offset voltage (V)','marker1 high (V)','marker1 low (V)','marker1 delay (ps)','marker2 high (V)','marker2 low (V)']
        name_list+= ['marker2 delay(ps)','skew (ps)']
        value_list = [1.0, 0.0, 1.0, 0.0, 0, 1.0, 0.0, 0, 0]
        for i in range(9):
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(name_list[i])
            hb.addWidget(label)
            wlist = []
            for j in range(noOfchannel):
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                wlist.append(item)
                hb.addWidget(item)
            self.UIs[11+i]=wlist
            self.ly.insertLayout(11+i,hb)
            
    def awgDialog(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        savePath = fileDialog.getExistingDirectory(self, 'Choose folder')    
        if not savePath == '':
            savePath = os.path.abspath(savePath)
            savePath += pathSep
        self.UIs[3].setText(savePath)
        
    def cmdDialog(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        savePath = fileDialog.getExistingDirectory(self, 'Choose folder')    
        if not savePath == '':
            savePath = os.path.abspath(savePath)
            savePath += pathSep
        self.UIs[1].setText(savePath)
        
    def showFastseq(self):
        fastSeqWidget = FastSeqModUI(parent=self,sequenceUI=self.UIs[-1])
        fastSeqWidget.show()
        
    def initUI(self):
        kind = self.kind
        if kind == 0:
            #ADC
            if self.item == 0:
                self.item = ADC()
            namelabel = QtWidgets.QLabel('name')
            name = QtWidgets.QLineEdit()
            name.setText(self.item.strings[0])
            self.UIs.append(name)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(namelabel)
            hb.addWidget(name)
            self.ly.addLayout(hb)
            
            unitlabel = QtWidgets.QLabel('unit')
            unit = QtWidgets.QLineEdit()
            unit.setText(self.item.strings[2])
            self.UIs.append(unit)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(unitlabel)
            hb.addWidget(unit)
            self.ly.addLayout(hb)
            
            nochannellabel = QtWidgets.QLabel('No of channels')
            nochannel = QtWidgets.QSpinBox()
            nochannel.setValue(self.item.uint64s[1])
            nochannel.valueChanged.connect(self.adcSetup)
            self.UIs.append(nochannel)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(nochannellabel)
            hb.addWidget(nochannel)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Name list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[3].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QLineEdit()
                item.setText(nlist[i])
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Unit list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[4].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QLineEdit()
                wlist.append(item)
                item.setText(nlist[i])
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Conversion factor list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[5].split(';')
            for i in range(nochannel.value()):
                item = QFloatLineEdit()
                item.set_value(float(nlist[i]))
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            rangelabel = QtWidgets.QLabel('range')
            rangeUI = QtWidgets.QComboBox()
            rangeUI.addItems(['+/-0.2V','+/-1V','+/-5V','+/-10V'])
            rangeUI.setCurrentIndex([0,1,5,10].index(self.item.uint64s[0]))
            self.UIs.append(rangeUI)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(rangelabel)
            hb.addWidget(rangeUI)
            self.ly.addLayout(hb)
            
            samplinglabel = QtWidgets.QLabel('sampling rate')
            sampling = QtWidgets.QSpinBox()
            sampling.setRange(1,250000)
            sampling.setValue(self.item.uint64s[2])
            self.UIs.append(sampling)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(samplinglabel)
            hb.addWidget(sampling)
            self.ly.addLayout(hb)
            
            realtimelabel = QtWidgets.QLabel('real time averaging?')
            realtime = QtWidgets.QCheckBox()
            if self.item.uint64s[3] == 0:
                realtime.setCheckState(0)
            else:
                realtime.setCheckState(2)
            self.UIs.append(realtime)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(realtimelabel)
            hb.addWidget(realtime)
            self.ly.addLayout(hb)
            
            RTavglabel = QtWidgets.QLabel('real time average points')
            RTavg = QtWidgets.QSpinBox()
            RTavg.setRange(0,1000000)
            RTavg.setValue(self.item.uint64s[4])
            self.UIs.append(RTavg)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(RTavglabel)
            hb.addWidget(RTavg)
            self.ly.addLayout(hb)
            
            InpConfigLabel = QtWidgets.QLabel('Inp config')
            InpConfig = QtWidgets.QComboBox()
            InpConfig.addItems(['default','RSE','NRSE','Differential','Pseudodifferential'])
            InpConfig.setCurrentIndex([-1,10083,10078,10106,12529].index(self.item.uint64s[5]))
            self.UIs.append(InpConfig)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(InpConfigLabel)
            hb.addWidget(InpConfig)
            self.ly.addLayout(hb)
            
            bufferlabel = QtWidgets.QLabel('Buffer size')
            buf = QtWidgets.QSpinBox()
            buf.setRange(0,2000000)
            buf.setValue(self.item.uint64s[6])
            self.UIs.append(buf)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(bufferlabel)
            hb.addWidget(buf)
            self.ly.addLayout(hb)
            
            ramp_trig_label = QtWidgets.QLabel('ramp trigger input')
            ramp_trig = QtWidgets.QSpinBox()
            ramp_trig.setValue(self.item.uint64s[8])
            self.UIs.append(ramp_trig)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(ramp_trig_label)
            hb.addWidget(ramp_trig)
            self.ly.addLayout(hb)
            
            fast_trig_label = QtWidgets.QLabel('fast trigger input')
            fast_trig = QtWidgets.QSpinBox()
            fast_trig.setValue(self.item.uint64s[9])
            self.UIs.append(fast_trig)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(fast_trig_label)
            hb.addWidget(fast_trig)
            self.ly.addLayout(hb)
                        
        elif kind == 1:
            #K2000
            if self.item == 0:
                self.item = K2000()
            name_list = ['name','GPIB address','unit']
            value_list = [self.item.strings[0], self.item.strings[1],self.item.strings[2]]
            for i in range(3):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            name_list = ['Range', 'Digits', 'NPLC', 'NPLC fast']
            value_list = [['1000 V','100 V','10 V','1 V','0.1 V'],['4 digits','5 digits','6 digits','7 digits'],['10','1','0.1'],['10','1','0.1']]
            index_list = [self.item.uint64s[0],self.item.uint64s[1],self.item.uint64s[2],self.item.uint64s[3]]
            for i in range(4):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QComboBox()
                item.addItems(value_list[i])
                item.setCurrentIndex(index_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            label = QtWidgets.QLabel('Average')
            item = QtWidgets.QSpinBox()
            item.setRange(0,10000)
            item.setValue(self.item.uint64s[4])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('conversion factor')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
        elif kind == 2:
            # K34401A
            if self.item == 0:
                self.item = K34401A()
            name_list = ['name','GPIB address','unit']
            value_list = [self.item.strings[0], self.item.strings[1],self.item.strings[2]]
            for i in range(3):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            name_list = ['Range', 'Digits', 'NPLC', 'NPLC fast']
            value_list = [['10 V','1 V','0.1 V'],['4 digits','5 digits','6 digits','7 digits'],['100','10','1','0.2','0.02'],['100','10','1','0.2','0.02']]
            index_list = [self.item.uint64s[0],self.item.uint64s[1],self.item.uint64s[2],self.item.uint64s[3]]
            for i in range(4):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QComboBox()
                item.addItems(value_list[i])
                item.setCurrentIndex(index_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            label = QtWidgets.QLabel('Average')
            item = QtWidgets.QSpinBox()
            item.setRange(0,10000)
            item.setValue(self.item.uint64s[4])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('conversion factor')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
        elif kind == 3:
            pass
        
        elif kind == 4:
            #DAC
            if self.item == 0:
                self.item = DAC()
            label = QtWidgets.QLabel('name')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('IP address')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Unit')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[2])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('panel')
            item = QtWidgets.QSpinBox()
            item.setRange(0,7)
            item.setValue(self.item.uint64s[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('channel')
            item = QtWidgets.QSpinBox()
            item.setRange(0,7)
            item.setValue(self.item.uint64s[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Upper limit (V)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Lower limit (V)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('ms to wait')
            item = QtWidgets.QSpinBox()
            item.setRange(0,1000)
            item.setValue(self.item.doubles[2])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('conversion')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[4])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
        elif kind == 5:
            #DAC lock-in
            if self.item == 0:
                self.item = DAC_Lock_in()
            label = QtWidgets.QLabel('name')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('IP address')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Unit')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[2])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('panel')
            item = QtWidgets.QSpinBox()
            item.setRange(0,7)
            item.setValue(self.item.uint64s[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('channel')
            item = QtWidgets.QSpinBox()
            item.setRange(0,7)
            item.setValue(self.item.uint64s[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Use (On) ?')
            item = QtWidgets.QCheckBox()
            if self.item.uint64s[2] == 0:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Upper limit (V)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Lower limit (V)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('frequency (Hz)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[4])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Amplitude (V)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[5])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Control parameter')
            item = QtWidgets.QComboBox()
            itemList = ['Panel*8 + channel','Frequency (Hz)','Amplitude (Vpp)']
            item.addItems(itemList)
            item.setCurrentIndex(self.item.uint64s[3])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
        elif kind == 6:
            #RF generator
            if self.item == 0:
                self.item = RS_RF()
            label = QtWidgets.QLabel('name')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('GPIB address')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Unit')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[2])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Pulse modulation on?')
            item = QtWidgets.QCheckBox()
            if self.item.uint64s[0] == 0:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('RF output on?')
            item = QtWidgets.QCheckBox()
            if self.item.uint64s[1] == 0:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Pulse source')
            item = QtWidgets.QComboBox()
            item.addItems(['Internal','External'])
            item.setCurrentIndex(self.item.uint64s[2])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Pulse mode')
            item = QtWidgets.QComboBox()
            item.addItems(['single','double','train'])
            item.setCurrentIndex(self.item.uint64s[3])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('trigger mode')
            item = QtWidgets.QComboBox()
            item.addItems(['auto','external','external gate','single'])
            item.setCurrentIndex(self.item.uint64s[4])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('External trigger input slope')
            item = QtWidgets.QComboBox()
            item.addItems(['Negative','Positive'])
            if self.item.uint64s[5] == 0:
                item.setCurrentIndex(0)
            else:
                item.setCurrentIndex(1)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('External impedance')
            item = QtWidgets.QComboBox()
            item.addItems(['10 kOhm','50 ohm'])
            if self.item.uint64s[6] == 0:
                item.setCurrentIndex(0)
            else:
                item.setCurrentIndex(1)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Control parameter')
            item = QtWidgets.QComboBox()
            name_list = ['Frequency (GHz)','Power (dBm)','Pulse period (us)','Pulse width (us)','Pulse delay (us)']
            name_list+= ['Pulse modulation (on or off)','Output On?','Pulse source (internal or external)','Pulse mode']
            name_list+= ['External trigger input slope','External impedance']
            item.addItems(name_list)
            item.setCurrentIndex(self.item.uint64s[7])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            name_list = ['frequency (GHz)','power (dBm)','pulse period (us)','pulse width (us)','pulse delay (us)']
            name_list+= ['frequency upper limit','frequency lower limit','power upper limit','power lower limit']
            value_list = self.item.doubles
            for i in range(9):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
            
        elif kind == 7:
            #AWG
            if self.item == 0:
                self.item = AWG()
            name_list = ['name','IP address','unit','Function folder path','Initial function name']
            value_list = list(self.item.strings[0:4])+list(self.item.strings[5:6])
            for i in range(5):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                if i == 3:
                    folderBtn = QtWidgets.QPushButton('...')
                    folderBtn.clicked.connect(self.awgDialog)
                    hb.addWidget(folderBtn)
                self.ly.addLayout(hb)
            
            name_list = ['Run ?','Run mode','control parameter']
            value_list = [['OFF','ON'],['continuous','Triggered','Gated','Sequence']]
            l = ['Run','All output on?','Run mode','Sampling rate','sending trigger','sending event','ch output on?','ch amplitude','ch offset voltage']
            l+= ['ch marker1 high','ch marker1 low','ch marker1 delay','ch maker2 high','ch maker2 low','ch maker2 delay','ch skew','Initial function execution']
            for i in range(4):
                l.append('ch'+str(i+1)+' output on?')
                l.append('ch'+str(i+1)+' amplitude [V]')
                l.append('ch'+str(i+1)+' offset voltage [V]')
                l.append('ch'+str(i+1)+' marker1 high [V]')
                l.append('ch'+str(i+1)+' marker1 low [V]')
                l.append('ch'+str(i+1)+' marker 1 delay [ps]')
                l.append('ch'+str(i+1)+' marker2 high [V]')
                l.append('ch'+str(i+1)+' marker2 low [V]')
                l.append('ch'+str(i+1)+' marker 2 delay[ps]')
                l.append('ch'+str(i+1)+' channel skew [ps]')
            value_list.append(l)
            
            if self.item.uint64s[2] == 0:
                index_list = [0]
            else:
                index_list = [1]
            index_list+=[self.item.uint64s[3],self.item.uint64s[4]]
            for i in range(3):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QComboBox()
                item.addItems(value_list[i])
                item.setCurrentIndex(index_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            label = QtWidgets.QLabel('sampling frequency (GHz)')
            item = QFloatLineEdit()
            item.set_value(self.item.doubles[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('No of channels to be used')
            item = QtWidgets.QSpinBox()
            item.setRange(1,4)
            item.setValue(self.item.uint64s[0])
            item.valueChanged.connect(self.awgSetup)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('ch output on?')
            hb.addWidget(label)
            wlist = []
            for i in range(self.item.uint64s[0]):
                item = QtWidgets.QCheckBox()
                if self.item.uint64s[6+i*4]!=0:
                    item.setCheckState(2)
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            name_list = ['amplitude (V)','offset voltage (V)','marker1 high (V)','marker1 low (V)','marker1 delay (ps)','marker2 high (V)','marker2 low (V)']
            name_list+= ['marker2 delay(ps)','skew (ps)']
            value_list=[]
            type_list=['d','d','d','d','u','d','d','u','u']
            u=0
            d=0
            for i in range(9):
                valType = type_list[i]
                tempList = []
                if valType == 'd':
                    for j in range(self.item.uint64s[0]):
                        tempList.append(self.item.doubles[1+d+6*j])
                    d += 1
                else:
                    for j in range(self.item.uint64s[0]):
                        tempList.append(self.item.uint64s[7+u+4*j])
                    u += 1
                value_list.append(tempList)
                
            for i in range(9):
                hb = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(name_list[i])
                hb.addWidget(label)
                wlist = []
                for j in range(self.item.uint64s[0]):
                    item = QFloatLineEdit()
                    item.set_value(value_list[i][j])
                    wlist.append(item)
                    hb.addWidget(item)
                self.UIs.append(wlist)
                self.ly.addLayout(hb)
              
            # port number added afterwards
            label = QtWidgets.QLabel('Port number')
            item = QtWidgets.QSpinBox()
            item.setRange(0,1000000)
            try:    # temporal treatment for olf file
                item.setValue(self.item.uint64s[22])
            except:
                print('The loaded file is old version and no port number is set.')
                item.setValue(4000)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
        elif kind == 8:
            pass
        
        elif kind == 9:
            # fast sequence
            if self.item == 0:
                self.item = FastSequences()
            name_list = ['name','IP address','unit']
            value_list = self.item.strings
            for i in range(3):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            name_list = ['fast sequence divider','trigger length','Sample count','start ramp at']
            value_list = list(self.item.uint64s[0:3])+list(self.item.uint64s[20:21])
            for i in range(4):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QSpinBox()
                item.setRange(1,10000000)
                if i == 3:
                    item.setRange(0,10000000)
                item.setValue(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            label = QtWidgets.QLabel('send all points?')
            item = QtWidgets.QCheckBox()
            if self.item.uint64s[3] == 0:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            for i in range(16):
                label = QtWidgets.QLabel('fast channel %d' % (i))
                hb = QtWidgets.QHBoxLayout()
                hb.setSpacing(0)
                hb.addWidget(label)
                wlist = []
                item = QtWidgets.QSpinBox()
                item.setRange(0,7)
                item.setValue(self.item.uint64s[4+i]/8)
                wlist.append(item)
                hb.addWidget(item)
                item = QtWidgets.QSpinBox()
                item.setRange(0,7)
                item.setValue(self.item.uint64s[4+i]%8)
                wlist.append(item)
                hb.addWidget(item)
                self.UIs.append(wlist)
                self.ly.addLayout(hb)
                
            name_list = ['upper limit of shit (V)','lower limit of shift (V)']
            value_list = [self.item.doubles[0], self.item.doubles[1]]
            for i in range(2):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            label = QtWidgets.QLabel('fast sequence')
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            item = QtWidgets.QPushButton('show')
            item.clicked.connect(self.showFastseq)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            # store fast sequence as a last UI but not show
            self.UIs.append(FastSequenceUI(parent=self,fastSeq=self.item.sequence))
                
        elif kind == 10:
            # fast sequence slot
            if self.item == 0:
                self.item = FastSequenceSlot()
            name_list = ['name','IP address','unit']
            value_list = self.item.strings
            for i in range(3):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('Slot No')
            item = QtWidgets.QSpinBox()
            item.setValue(self.item.uint64s[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            name_list = ['upper limit','lower limit']
            value_list = self.item.doubles
            for i in range(2):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
            
        elif kind == 11:
            # command line
            if self.item == 0:
                self.item = CMD()
            name_list = ['name','working directory']
            value_list = self.item.strings
            for i in range(2):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                if i == 1:
                    folderBtn = QtWidgets.QPushButton('...')
                    folderBtn.clicked.connect(self.cmdDialog)
                    hb.addWidget(folderBtn)
                self.ly.addLayout(hb)
            
            label = QtWidgets.QLabel('wait for execution?')
            item = QtWidgets.QCheckBox()
            if self.item.uint64s[0] == 0:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
        
        elif kind == 12:
            #DSP lock-in
            if self.item == 0:
                self.item = DSP_lockIn()
            name_list = ['name','GPIB address','unit','name list','unit list']
            value_list = self.item.strings
            for i in range(5):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
            #    if i < 3:
                item.setText(value_list[i])
            #    else:
                #    item.setText(','.join(value_list[i]))
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
            
            name_list = ['RT average time','parameter to be read']
            value_list = [self.item.uint64s[0], self.item.uint64s[1]]
            for i in range(2):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QSpinBox()
                item.setRange(0,10000000)
                item.setValue(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
            
            name_list = ['coupling','inputMode','FET or Bipolar','line filter','auto AC gain','AC gain','sensitivity','time constant','reference channel', 'parameter to get initial value']
            value_list = [['AC and float','DC and float','AC and GND','DC and GND'],['V at port A','V at port -B','V for A-B','I for broad band','I for low noise']]
            value_list+= [['Bipolar','FET'],['off','50 Hz','100 Hz', '50/100 Hz'],['off','on'],['0 dB','10 dB','20 dB','30 dB','40 dB','50 dB','60 dB','70 dB','80 dB','90 dB']]
            value_list+= [['2 nV','5 nV','10 nV','20 nV','50 nV','100 nV','200 nV','500 nV','1 uV','2 uV','5 uV','10 uV','20 uV','50 uV','100 uV','200 uV','500 uV','1 mV','2 mV','5 mV','10 mV','20 mV','50 mV','100 mV','200 mV','500 mV','1 V']]
            value_list+= [['10 us','20 us','40 us','80 us','160 us','320 us','640 us','5 ms','10 ms','20 ms','50 ms','100 ms','200 ms','500 ms','1 s','2 s','5 s','10 s','20 s','50 s','100 s','200 s','500 s','1 ks','2 ks','5 ks','10 ks','20 ks','50 ks','100 ks']]
            value_list+= [['internal','external rear','external front'],['Oscillator amplitude','Oscillator frequency','sensitivity','time constant']]
            initial_indexes = self.item.uint64s[3:13]
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QComboBox()
                item.addItems(value_list[i])
                if i == 6:
                    item.setCurrentIndex(initial_indexes[i]-1)
                else:
                    item.setCurrentIndex(initial_indexes[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            name_list = ['conversion','oscillator amplitude','oscillator frequency','amplitude upper limit','amplitude lower limit','frequency upper limit','frequency lower limit']
            value_list = self.item.doubles
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
        
        elif kind == 13:
            #DSP lock-in sweep
            if self.item == 0:
                self.item = DSP_lockIn_sweep()
            name_list = ['name','GPIB address','unit']
            value_list = self.item.strings
            for i in range(3):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            name_list = ['parameter']
            value_list = [self.item.uint64s[0]]
            for i in range(1):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QSpinBox()
                item.setRange(0,14)
                item.setValue(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            name_list = ['upper limit','lower limit','conversion']
            value_list = self.item.doubles
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
        
        elif kind == 14:
            # ms to wait
            if self.item == 0:
                self.item = mswait()
            # GUI for strings
            name_list = ['name','unit']
            value_list = self.item.strings
            for i in range(2):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
            
            #GUI for doubles
            name_list = ['upper limit','lower limit']
            value_list = self.item.doubles
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
        
        elif kind == 15:
            # ATM delay line
            if self.item == 0:
                self.item = ATMDelayLine()
            # GUI for strings
            name_list = ['name','Com port','unit']
            value_list = self.item.strings
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QLineEdit()
                item.setText(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            # GUI for unsined 64 bit integer
            name_list = ['baud rate', 'Echo mode', 'Acceleration', 'Deceleration', 'Velocity initial', 'Velocity Maximum']
            value_list = self.item.uint64s
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QtWidgets.QSpinBox()
                item.setRange(0,1000000)
                item.setValue(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
                
            #GUI for doubles
            name_list = ['upper limit (ps)','lower limit (ps)']
            value_list = self.item.doubles
            for i in range(len(name_list)):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
        
        elif kind == 16:

             #RF attenuator 
            if self.item == 0:
                self.item = RF_Attn()
            label = QtWidgets.QLabel('name')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[0])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)

            label = QtWidgets.QLabel('USB address')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[1])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)    

            label = QtWidgets.QLabel('Unit')
            item = QtWidgets.QLineEdit()
            item.setText(self.item.strings[2])
            self.UIs.append(item)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(item)
            self.ly.addLayout(hb)
            
            name_list = ['attenuation','attenuation upper limit','attenuation lower limit','loss insertion']
            value_list = self.item.doubles
            for i in range(4):
                label = QtWidgets.QLabel(name_list[i])
                item = QFloatLineEdit()
                item.set_value(value_list[i])
                self.UIs.append(item)
                hb = QtWidgets.QHBoxLayout()
                hb.addWidget(label)
                hb.addWidget(item)
                self.ly.addLayout(hb)
        
        elif kind == 17:
            #FPGA built-in ADC
            if self.item == 0:
                self.item = FPGA_ADC()
            namelabel = QtWidgets.QLabel('Name')
            name = QtWidgets.QLineEdit()
            name.setText(self.item.strings[0])
            self.UIs.append(name)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(namelabel)
            hb.addWidget(name)
            self.ly.addLayout(hb)
            
            nochannellabel = QtWidgets.QLabel('No of channels')
            nochannel = QtWidgets.QSpinBox()
            nochannel.setValue(self.item.uint64s[0])
            nochannel.valueChanged.connect(self.fpga_adc_Setup)
            self.UIs.append(nochannel)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(nochannellabel)
            hb.addWidget(nochannel)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Name list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[2].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QLineEdit()
                item.setText(nlist[i])
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Unit list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[3].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QLineEdit()
                wlist.append(item)
                item.setText(nlist[i])
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Conversion factor list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[4].split(';')
            for i in range(nochannel.value()):
                item = QFloatLineEdit()
                item.set_value(float(nlist[i]))
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Input channels list')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[5].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QSpinBox()
                item.setRange(0,31)
                item.setValue(int(nlist[i]))
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Range List')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[6].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QComboBox()
                item.addItems(['+/-0.2V','+/-1V','+/-5V','+/-10V'])
                item.setCurrentIndex(['+/-0.2V','+/-1V','+/-5V','+/-10V'].index(nlist[i]))
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            hb = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel('Term List')
            hb.addWidget(label)
            wlist = []
            nlist = self.item.strings[7].split(';')
            for i in range(nochannel.value()):
                item = QtWidgets.QComboBox()
                item.addItems(['RSE','NRSE','DIFF'])
                item.setCurrentIndex(['RSE','NRSE','DIFF'].index(nlist[i]))
                wlist.append(item)
                hb.addWidget(item)
            self.UIs.append(wlist)
            self.ly.addLayout(hb)
            
            samplinglabel = QtWidgets.QLabel('Sampling rate')
            sampling = QtWidgets.QSpinBox()
            sampling.setRange(1,250000)
            sampling.setValue(self.item.uint64s[1])
            self.UIs.append(sampling)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(samplinglabel)
            hb.addWidget(sampling)
            self.ly.addLayout(hb)
            
            RTavglabel = QtWidgets.QLabel('RT average')
            RTavg = QtWidgets.QSpinBox()
            RTavg.setRange(1,1000000)
            RTavg.setValue(self.item.uint64s[2])
            self.UIs.append(RTavg)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(RTavglabel)
            hb.addWidget(RTavg)
            self.ly.addLayout(hb) 
            
            sampleslabel = QtWidgets.QLabel('Samples per channel')
            samples = QtWidgets.QSpinBox()
            samples.setRange(1,1000000)
            samples.setValue(self.item.uint64s[6])
            self.UIs.append(samples)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(sampleslabel)
            hb.addWidget(samples)
            self.ly.addLayout(hb)            
            
            TriggerModeLabel = QtWidgets.QLabel('Trigger mode')
            TriggerMode = QtWidgets.QComboBox()
            TriggerMode.addItems(['ramp','manual/RT'])
            TriggerMode.setCurrentIndex(self.item.uint64s[3])
            self.UIs.append(TriggerMode)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(TriggerModeLabel)
            hb.addWidget(TriggerMode)
            self.ly.addLayout(hb)
            
            TriggerSourceLabel = QtWidgets.QLabel('Trigger source')
            TriggerSource = QtWidgets.QComboBox()
            TriggerSource.addItems(['manual','1','2','3','4'])
            TriggerSource.setCurrentIndex(self.item.uint64s[4])
            self.UIs.append(TriggerSource)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(TriggerSourceLabel)
            hb.addWidget(TriggerSource)
            self.ly.addLayout(hb)
            
            TriggerEdgeLabel = QtWidgets.QLabel('Trigger edge')
            TriggerEdge = QtWidgets.QComboBox()
            TriggerEdge.addItems(['falling','rising','both'])
            TriggerEdge.setCurrentIndex(self.item.uint64s[5])
            self.UIs.append(TriggerEdge)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(TriggerEdgeLabel)
            hb.addWidget(TriggerEdge)
            self.ly.addLayout(hb)
                        
    def ok_proc(self):
        kind = self.kind
        print(kind)
        if kind == 0:
            item = ADC()
            item.strings[0] = self.UIs[0].text()
            item.strings[2] = self.UIs[1].text()
            item.uint64s[1] = self.UIs[2].value()
            item.strings[3] = ';'.join([i.text() for i in self.UIs[3]])
            item.strings[4] = ';'.join([i.text() for i in self.UIs[4]])
            item.strings[5] = ';'.join([str(i.get_value()) for i in self.UIs[5]])
            item.uint64s[0] = [0,1,5,10][self.UIs[6].currentIndex()]
            item.uint64s[2] = self.UIs[7].value()
            if self.UIs[8].checkState()==0:
                item.uint64s[3] = 0
            else:
                item.uint64s[3] = 1
            item.uint64s[4] = self.UIs[9].value()
            item.uint64s[5] = [-1,10083,10078,10106,12529][self.UIs[10].currentIndex()]
            item.uint64s[6] = self.UIs[11].value()
            item.uint64s[8] = self.UIs[12].value()
            item.uint64s[9] = self.UIs[13].value()
        elif kind == 1:
            item = K2000()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].currentIndex()
            item.uint64s[1] = self.UIs[4].currentIndex()
            item.uint64s[2] = self.UIs[5].currentIndex()
            item.uint64s[3] = self.UIs[6].currentIndex()
            item.uint64s[4] = self.UIs[7].value()
            item.doubles[0] = self.UIs[8].get_value()
            
        elif kind == 2:
            item = K34401A()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].currentIndex()
            item.uint64s[1] = self.UIs[4].currentIndex()
            item.uint64s[2] = self.UIs[5].currentIndex()
            item.uint64s[3] = self.UIs[6].currentIndex()
            item.uint64s[4] = self.UIs[7].value()
            item.doubles[0] = self.UIs[8].get_value()
            
        elif kind == 3:
            #Lecroy
            item = 0
        elif kind == 4:
            item = DAC()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].value()
            item.uint64s[1] = self.UIs[4].value()
            item.doubles[0] = self.UIs[5].get_value()
            item.doubles[1] = self.UIs[6].get_value()
            item.doubles[2] = self.UIs[7].value()
            item.doubles[4] = self.UIs[8].get_value()
        elif kind == 5:
            item = DAC_Lock_in()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].value()
            item.uint64s[1] = self.UIs[4].value()
            if self.UIs[5].checkState()==0:
                item.uint64s[2] = 0
            else:
                item.uint64s[2] = 1
            item.doubles[0] = self.UIs[6].get_value()
            item.doubles[1] = self.UIs[7].get_value()
            item.doubles[4] = self.UIs[8].get_value()
            item.doubles[5] = self.UIs[9].get_value()
            item.uint64s[3] = self.UIs[10].currentIndex()
        elif kind == 6:
            item = RS_RF()
            item.strings[0] = self.UIs[0].text()
            item.strings[2] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            if self.UIs[3].checkState()==0:
                item.uint64s[0] = 0
            else:
                item.uint64s[0] = 1
            if self.UIs[4].checkState() == 0:
                item.uint64s[1] = 0
            else:
                item.uint64s[1] = 1
            item.uint64s[2] = self.UIs[5].currentIndex()
            item.uint64s[3] = self.UIs[6].currentIndex()
            item.uint64s[4] = self.UIs[7].currentIndex()
            item.uint64s[5] = self.UIs[8].currentIndex()
            item.uint64s[6] = self.UIs[9].currentIndex()
            item.uint64s[7] = self.UIs[10].currentIndex()
            item.doubles[0] = self.UIs[11].get_value()
            item.doubles[1] = self.UIs[12].get_value()
            item.doubles[2] = self.UIs[13].get_value()
            item.doubles[3] = self.UIs[14].get_value()
            item.doubles[4] = self.UIs[15].get_value()
            item.doubles[5] = self.UIs[16].get_value()
            item.doubles[6] = self.UIs[17].get_value()
            item.doubles[7] = self.UIs[18].get_value()
            item.doubles[8] = self.UIs[19].get_value()
        elif kind == 7:
            item = AWG()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.strings[3] = self.UIs[3].text()
            item.strings[5] = self.UIs[4].text()
            item.uint64s[2] = self.UIs[5].currentIndex()
            item.uint64s[3] = self.UIs[6].currentIndex()
            item.uint64s[4] = self.UIs[7].currentIndex()
            item.doubles[0] = self.UIs[8].get_value()
            item.uint64s[0] = self.UIs[9].value()
            for i, ui in enumerate(self.UIs[10]):
                item.uint64s[6+4*i] = int(ui.checkState()//2)
            for i, ui in enumerate(self.UIs[11]):
                item.doubles[1+6*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[12]):
                item.doubles[2+6*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[13]):
                item.doubles[3+6*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[14]):
                item.doubles[4+6*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[15]):
                item.uint64s[7+4*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[16]):
                item.doubles[5+6*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[17]):
                item.doubles[6+6*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[18]):
                item.uint64s[8+4*i] = ui.get_value()
            for i, ui in enumerate(self.UIs[19]):
                item.uint64s[9+4*i] = ui.get_value()
            item.uint64s[22] = self.UIs[20].value()
            
        elif kind == 8:
            # B - field
            item = 0
        elif kind == 9:
            item = FastSequences()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].value()
            item.uint64s[1] = self.UIs[4].value()
            item.uint64s[2] = self.UIs[5].value()
            item.uint64s[20] = self.UIs[6].value()
            if self.UIs[7].checkState()==0:
                item.uint64s[3] = 0
            else:
                item.uint64s[3] = 1
            item.fast_channels = []
            for i in range(16):
                item.uint64s[4+i] = 8*self.UIs[8+i][0].value()+self.UIs[8+i][1].value()
            item.doubles[0] = self.UIs[24].get_value()
            item.doubles[1] = self.UIs[25].get_value()
            self.UIs[-1].readUIs()
            item.sequence = self.UIs[-1].fastSeq
            
        elif kind == 10:
            item = FastSequenceSlot()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].value()
            item.doubles[0] = self.UIs[4].get_value()
            item.doubles[1] = self.UIs[5].get_value()
        elif kind == 11:
            item = CMD()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.uint64s[0] = int(self.UIs[2].checkState()/2)
        elif kind == 12:
            item = DSP_lockIn()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            if not str(self.UIs[3].text()) == '':
                item.strings[3] = str(self.UIs[3].text())#.replace(';',',').split(',')
            if not str(self.UIs[4].text()) == '':
                item.strings[4] = str(self.UIs[4].text())#.replace(';',',').split(',')
            v = self.UIs[6].value()
            no_readouts = 0
            for i in range(16):
                if (v & 2**i) != 0:
                    no_readouts +=1
            item.uint64s[2] = no_readouts
            item.uint64s[0] = self.UIs[5].value()
            item.uint64s[1] = self.UIs[6].value()
            item.uint64s[3] = self.UIs[7].currentIndex()
            item.uint64s[4] = self.UIs[8].currentIndex()
            item.uint64s[5] = self.UIs[9].currentIndex()
            item.uint64s[6] = self.UIs[10].currentIndex()
            item.uint64s[7] = self.UIs[11].currentIndex()
            item.uint64s[8] = self.UIs[12].currentIndex()
            item.uint64s[9] = self.UIs[13].currentIndex()+1
            item.uint64s[10] = self.UIs[14].currentIndex()
            item.uint64s[11] = self.UIs[15].currentIndex()
            item.uint64s[12] = self.UIs[16].currentIndex()
            item.doubles[0] = self.UIs[17].get_value()
            item.doubles[1] = self.UIs[18].get_value()
            item.doubles[2] = self.UIs[19].get_value()
            item.doubles[3] = self.UIs[20].get_value()
            item.doubles[4] = self.UIs[21].get_value()
            item.doubles[5] = self.UIs[22].get_value()
            item.doubles[6] = self.UIs[23].get_value()
        elif kind == 13:
            item = DSP_lockIn_sweep()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].value()
            item.doubles[0] = self.UIs[4].get_value()
            item.doubles[1] = self.UIs[5].get_value()
            item.doubles[2] = self.UIs[6].get_value()
        elif kind == 14:
            item = mswait()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.doubles[0] = self.UIs[2].get_value()
            item.doubles[1] = self.UIs[3].get_value()
        elif kind == 15:
            item = ATMDelayLine()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.uint64s[0] = self.UIs[3].value()
            item.uint64s[1] = self.UIs[4].value()
            item.uint64s[2] = self.UIs[5].value()
            item.uint64s[3] = self.UIs[6].value()
            item.uint64s[4] = self.UIs[7].value()
            item.uint64s[5] = self.UIs[8].value()
            item.doubles[0] = self.UIs[9].get_value()
            item.doubles[1] = self.UIs[10].get_value()
        elif kind == 16:
            item = RF_Attn()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = self.UIs[2].text()
            item.doubles[0] = self.UIs[3].get_value()
            item.doubles[1] = self.UIs[4].get_value()
            item.doubles[2] = self.UIs[5].get_value()
            item.doubles[3] = self.UIs[6].get_value()
        elif kind == 17:
            item = FPGA_ADC()
            item.strings[0] = self.UIs[0].text()
            item.strings[1] = self.UIs[1].text()
            item.strings[2] = ';'.join([i.text() for i in self.UIs[2]])
            item.strings[3] = ';'.join([i.text() for i in self.UIs[3]])
            item.strings[4] = ';'.join([str(i.get_value()) for i in self.UIs[4]])
            item.strings[5] = ';'.join([str(i.value()) for i in self.UIs[5]])
            item.strings[6] = ';'.join([str(i.currentText()) for i in self.UIs[6]])
            item.strings[7] = ';'.join([str(i.currentText()) for i in self.UIs[7]])
            item.uint64s[0] = self.UIs[1].value()
            item.uint64s[1] = self.UIs[8].value()
            item.uint64s[2] = self.UIs[9].value()
            item.uint64s[6] = self.UIs[10].value()
            item.uint64s[3] = self.UIs[11].currentIndex()
            item.uint64s[4] = self.UIs[12].currentIndex()
            item.uint64s[5] = self.UIs[13].currentIndex()
        item.name = item.strings[0]
        self.item = item
        self.name.setText(item.strings[0])
        attrs = vars(self.item)
        print(', '.join("%s: %s" % item for item in attrs.items()))
        self.close()
        
class instrument(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 item = 0,
                 ):
        super(instrument, self).__init__()
        self.item = item
        self.setup = 0
        
        self.kind = QtWidgets.QComboBox(parent=self)
        self.kind.addItems(ginst_list)
        self.kind.setFixedSize(150,25)
        if self.item != 0:
            self.kind.setCurrentIndex(self.item.kind)
        self.setupBtn = QtWidgets.QPushButton('setup', parent=self)
        self.setupBtn.clicked.connect(self.setupInst)
        self.setupBtn.setFixedSize(80,25)
        setLabel = QtWidgets.QLabel('name')
        setLabel.setFixedSize(35,20)
        self.setState = QtWidgets.QLineEdit(parent=self)
        self.setState.setFixedSize(100,20)
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        hb.addWidget(setLabel)
        hb.addWidget(self.setState)
        self.ly = QtWidgets.QHBoxLayout()
        self.ly.setSpacing(1)
        self.ly.addWidget(self.kind)
        self.ly.addWidget(self.setupBtn)
        self.ly.addLayout(hb)
        self.setLayout(self.ly)
        self.setFixedSize(400,40)
        
    def setupInst(self):
        kind = self.kind.currentIndex()
        if self.setup == 0:
            self.setup = inst_setup_UI(parent=self, kind=kind)
        else:
            self.setup.kind = kind
            self.setup()
        self.setup.show()
        
class inst_list(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 noInst=5,
                 ):
        super(inst_list, self).__init__()
        self.error = QtWidgets.QErrorMessage()
        self.UIs = []
        self.inst_params=[]
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        self.noInst = QtWidgets.QSpinBox(parent=self)
        self.noInst.setFixedSize(80,25)
        self.noInst.setRange(1,1000)
        self.noInst.setValue(noInst)
        self.noInst.valueChanged.connect(self.initUI)
        hb.addWidget(self.noInst)
        label = QtWidgets.QLabel('Pos')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.targetPos = QtWidgets.QSpinBox()
        self.targetPos.setRange(0,999)
        hb.addWidget(self.targetPos)
        self.insertBtn = QtWidgets.QPushButton('Insert')
        self.insertBtn.clicked.connect(self.insert)
        hb.addWidget(self.insertBtn)
        self.removeBtn = QtWidgets.QPushButton('Remove')
        self.removeBtn.clicked.connect(self.remove)
        hb.addWidget(self.removeBtn)
        instArea = QtWidgets.QScrollArea()
        self.w = QtWidgets.QWidget()
        self.w.setFixedSize(400,40+40*self.noInst.value())
        self.vb = QtWidgets.QVBoxLayout()
        self.vb.setSpacing(0)
        self.vb.addLayout(hb)
        # self.vb.addWidget(self.noInst)
        self.initUI()
        self.w.setLayout(self.vb)
        instArea.setWidget(self.w)
        ly = QtWidgets.QVBoxLayout()
        ly.addWidget(instArea)
        self.setLayout(ly)
        
    def initUI(self):
        no = self.noInst.value()
        currentSize = len(self.UIs)
        if no <= currentSize:
            for i in reversed(range(len(self.UIs[no:]))):
                ly = self.vb.itemAt(no+1+i).layout()
                for j in reversed(range(ly.count())):
                    w = ly.itemAt(j).widget()
                    w.deleteLater()
                    ly.removeItem(ly.itemAt(j))
                # self.vb.itemAt(no+1+i).widget().deleteLater()
                self.vb.removeItem(self.vb.itemAt(no+1+i))
                del self.UIs[no+i]
        else:
            for i in range(no):
                if i >= currentSize:
                    hb = QtWidgets.QHBoxLayout()
                    label = QtWidgets.QLabel(str(i))
                    label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    hb.addWidget(label)
                    item = instrument()
                    self.UIs.append(item)
                    hb.addWidget(item)
                    self.vb.addLayout(hb)
        self.w.setFixedSize(400,40+40*self.noInst.value())
        
    def insert(self):
        target = self.targetPos.value()     # get target position
        no = self.noInst.value()            # get current number of instruments
        try:
            item = instrument()                 # prepare instrument to insert
            self.UIs.insert(target, item)       # insert it into UI list
            for i in reversed(range(no+1)):
                if i == no:
                    hb = QtWidgets.QHBoxLayout()
                    label = QtWidgets.QLabel(str(i))
                    label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    hb.addWidget(label)
                    hb.addWidget(self.UIs[i])
                    self.vb.addLayout(hb)
                else:
                    ly = self.vb.itemAt(i+1).layout()   # get layout of the position i
                    ly.itemAt(0).widget().deleteLater() # delete label at position
                    ly.removeItem(ly.itemAt(0))         # remove label from layout
                    ly.removeItem(ly.itemAt(1))         # remove instrument from layout but not delete since we will use it.
                    self.vb.removeItem(self.vb.itemAt(i+1)) # remove item from layout
                    hb = QtWidgets.QHBoxLayout()
                    label = QtWidgets.QLabel(str(i))
                    label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    hb.addWidget(label)
                    hb.addWidget(self.UIs[i])
                    self.vb.insertLayout(i+1,hb)
            
            self.noInst.valueChanged.disconnect()   # disconnect signal to change the value
            self.noInst.setValue(no+1)              # change value
            self.noInst.valueChanged.connect(self.initUI)   # connect signal again
            self.w.setFixedSize(400,40+40*self.noInst.value())  # reshape widget
        except:
            self.error.showMessage('Target index is invalid. (Probably...)')
    
    def remove(self):
        target = self.targetPos.value()     # get target position
        no = self.noInst.value()            # get current number of instruments
        try:
            # remove widget at target position
            ly = self.vb.itemAt(target+1).layout()
            for j in reversed(range(2)):
                ly.itemAt(j).widget().deleteLater()
                ly.removeItem(ly.itemAt(j))
            del self.UIs[target]                # remove list item as well
            self.vb.removeItem(self.vb.itemAt(target+1))
        
            for i in reversed(range(no-1)):
                ly = self.vb.itemAt(i+1).layout()   # get layout of the position i
                ly.itemAt(0).widget().deleteLater() # delete label at position
                ly.removeItem(ly.itemAt(0))         # remove label from layout
                ly.removeItem(ly.itemAt(1))         # remove instrument from layout but not delete since we will use it.
                self.vb.removeItem(self.vb.itemAt(i+1)) # remove item from layout
                hb = QtWidgets.QHBoxLayout()
                label = QtWidgets.QLabel(str(i))
                label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                hb.addWidget(label)
                hb.addWidget(self.UIs[i])
                self.vb.insertLayout(i+1,hb)
                
            self.noInst.valueChanged.disconnect()   # disconnect signal to change the value
            self.noInst.setValue(no-1)              # change value
            self.noInst.valueChanged.connect(self.initUI)   # connect signal again
            self.w.setFixedSize(400,40+40*self.noInst.value())  # reshape widget
        except:
            self.error.showMessage('Target index is invalid. (Probably...)')
        
"""----------------------------
Main widget
-----------------------------"""
class config_main(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 ):
        super(config_main, self).__init__()
        self.config = MeasConfig()
        self.fileCheck = 0
        
        # components for self.fpath
        dirLabel = QtWidgets.QLabel('Save directory')
        dirLabel.setFixedSize(80,25)
        dirLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dir = QtWidgets.QLineEdit()
        self.dir.setFixedSize(150,25)
        self.dirBtn = QtWidgets.QPushButton('...')
        self.dirBtn.setFixedSize(30,25)
        self.dirBtn.clicked.connect(self.dirDialog)
        nameLabel = QtWidgets.QLabel('File name')
        nameLabel.setFixedSize(60,25)
        nameLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.file = QtWidgets.QLineEdit()
        self.file.setFixedSize(150,25)
        autoLabel = QtWidgets.QLabel('auto?')
        autoLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.auto = QtWidgets.QCheckBox()
        overwriteLabel = QtWidgets.QLabel('over write?')
        overwriteLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.owrite = QtWidgets.QCheckBox()
        fi_ly = QtWidgets.QVBoxLayout()
        fi_ly.setSpacing(0)
        hb = QtWidgets.QHBoxLayout()
        hb.setSpacing(0)
        hb.addWidget(dirLabel)
        hb.addWidget(self.dir)
        hb.addWidget(self.dirBtn)
        fi_ly.addLayout(hb)
        hb = QtWidgets.QHBoxLayout()
        hb.addWidget(nameLabel)
        hb.addWidget(self.file)
        hb.addWidget(autoLabel)
        hb.addWidget(self.auto)
        hb.setSpacing(0)
        fi_ly.addLayout(hb)
        hb = QtWidgets.QHBoxLayout()
        hb.addWidget(overwriteLabel)
        hb.addWidget(self.owrite)
        hb.setSpacing(0)
        fi_ly.addLayout(hb)
        
        # components for wait
        labels = ['Initial wait (ms)','wait before measurement (ms)','integration time (ms)','wait after step move (ms)']
        values = [100,1,30,100]
        wait_ly = QtWidgets.QVBoxLayout()
        wait_ly.setSpacing(0)
        self.wait_UIs = []
        for i in range(4):
            vb = QtWidgets.QHBoxLayout()
            vb.setSpacing(0)
            label = QtWidgets.QLabel(labels[i])
            label.setFixedSize(200,25)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            vb.addWidget(label)
            item = QtWidgets.QSpinBox()
            item.setRange(0,1000000000)
            item.setValue(values[i])
            item.setFixedSize(100, 25)
            self.wait_UIs.append(item)
            vb.addWidget(item)
            wait_ly.addLayout(vb)
            
        # components for fast sweep condition
        labels = ['fast sweep ?', 'ramp mode?']
        values = [0, 0]
        fast_ly = QtWidgets.QVBoxLayout()
        fast_ly.setSpacing(0)
        self.fast_UIs = []
        for i in range(2):
            hb = QtWidgets.QHBoxLayout()
            hb.setSpacing(0)
            label = QtWidgets.QLabel(labels[i])
            label.setFixedSize(120,25)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            hb.addWidget(label)
            item = QtWidgets.QCheckBox()
            item.setFixedSize(50,25)
            if values[i]==0:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
            item.setFixedSize(50,25)
            self.fast_UIs.append(item)
            hb.addWidget(item)
            fast_ly.addLayout(hb)
        
        # Load and create button
        self.load_ly = QtWidgets.QHBoxLayout()
        self.load_ly.setSpacing(0)
        item = QtWidgets.QPushButton('Load')
        item.clicked.connect(self.load)
        item.setFixedSize(100,25)
        self.load_ly.addWidget(item)
        item = QtWidgets.QPushButton('Create')
        item.clicked.connect(self.create)
        item.setFixedSize(100,25)
        self.load_ly.addWidget(item)
        
        # instrument list
        label = QtWidgets.QLabel('Instrument list')
        inst_ly = QtWidgets.QVBoxLayout()
        inst_ly.setSpacing(0)
        inst_ly.addWidget(label)
        self.instList = inst_list(parent=self,noInst=10)
        inst_ly.addWidget(self.instList)
        
        main_ly = QtWidgets.QHBoxLayout()
        main_ly.setSpacing(0)
        sub_ly = QtWidgets.QVBoxLayout()
        sub_ly.setSpacing(0)
        sub_ly.addLayout(fi_ly)
        sub_ly.addLayout(wait_ly)
        sub_ly.addLayout(fast_ly)
        sub_ly.addLayout(self.load_ly)
        main_ly.addLayout(sub_ly)
        main_ly.addLayout(inst_ly)
        
        self.setLayout(main_ly)
        
        """ Try to load the previous files """
        try:
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5', 'r') as f:
                savePath = str(f['saveConfigFolderPath'][...])
                if savePath != '':
                    self.dir.setText(savePath)
        except:
            pass
        
    def dirDialog(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        if self.dir.text() != '':
            savePath = fileDialog.getExistingDirectory(self, 'Choose folder', directory=os.path.dirname(self.dir.text()))
        else:
            savePath = fileDialog.getExistingDirectory(self, 'Choose folder')
        if not savePath == '':
            savePath += '/'
            self.dir.setText(savePath)
            """ save folder path """
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5', 'a') as f:
                dset = f.get('saveConfigFolderPath')
                if dset == None:
                    dset = f.create_dataset('saveConfigFolderPath', data = savePath)
                else:
                    dset[...] = savePath
    
    def load(self):
        fileDialog = QtWidgets.QFileDialog()
        loadPath = fileDialog.getOpenFileName(self, 'Choose experiment file', filter='*.h5', directory=os.path.dirname(self.dir.text()))
        loadPath = loadPath[0]
        if not loadPath == '':
            self.config.fpath = loadPath
            self.config.read()
            # fill file path information
            self.dir.setText('/'.join(loadPath.split('/')[:-1])+'/')
            self.file.setText(loadPath.split('/')[-1].split('.')[0])
            # fill wait UIs
            self.wait_UIs[0].setValue(self.config.initial_wait)
            self.wait_UIs[1].setValue(self.config.wait_before_meas)
            self.wait_UIs[2].setValue(self.config.integration_time)
            self.wait_UIs[3].setValue(self.config.wait_after_step_move)
            # fill fast sweep info
            if self.config.fastSweep == False:
                self.fast_UIs[0].setCheckState(0)
            else:
                self.fast_UIs[0].setCheckState(2)
            if self.config.ramp == False:
                self.fast_UIs[1].setCheckState(0)
            else:
                self.fast_UIs[1].setCheckState(2)
            # fill instruments information
            size = len(self.config.list)
            self.instList.noInst.setValue(size)
            for i, UI in enumerate(self.instList.UIs):
                inst = self.config.list[i]
                UI.item = inst
                UI.kind.setCurrentIndex(inst.kind)
                UI.setState.setText(inst.name)
                if UI.setup == 0:
                    UI.setup = inst_setup_UI(parent=UI,kind = inst.kind)
                    UI.setup.item = inst
                else:
                    UI.setup.kind = inst.kind
                    UI.setup.item = inst
                    UI.setup()
    
    def create(self):
        if self.auto.checkState()==0:
            self.config.fpath = os.path.abspath(self.dir.text()+self.file.text()+'.h5')
        else:
            self.config.fpath = os.path.abspath(self.dir.text()+'conf_'+time.strftime('%Y%m%d%H%M')+'.h5')
        
        createFile = False
        if os.path.isfile(self.config.fpath):
            if self.owrite.checkState()==0:
                self.fileCheck = FileNameCheck()
                self.fileCheck.show()
            else:
                createFile = True
        else:
            createFile = True
            
        if createFile:
            self.config.initial_wait = self.wait_UIs[0].value()
            self.config.wait_before_meas = self.wait_UIs[1].value()
            self.config.integration_time = self.wait_UIs[2].value()
            self.config.wait_after_step_move = self.wait_UIs[3].value()
            if self.fast_UIs[0].checkState()==0:
                self.config.fastSweep = False
            else:
                self.config.fastSweep = True
            if self.fast_UIs[1].checkState() == 0:
                self.config.ramp = False
            else:
                self.config.ramp = True
            self.config.list=[]
            for i in range(self.instList.noInst.value()):
                UI = self.instList.UIs[i]
                self.config.list.append(UI.setup.item)
            #write file
            self.config.write()
        
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
#    fs = FastSQequenceUI()
#    fs.show()
#    inst = instrument()
#    inst = inst_list()
#    inst.show()
    conf = config_main()
    conf.show()
    sys.exit(app.exec_())
    pass