# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:52:59 2016

@author: shintaro
"""

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(0,'..')
import os, platform
import h5py
import time
import GUI.IpythonWidgetClass as IpyConsole
from GUI.UtilityGUI import *
from MeasurementBase.measurement_classes import *

if platform.system()=='Windows':
    import MeasurementBase.SendFileNames as sfn
    pass
elif platform.system()=='Darwin':
    pass

pathSep = QtCore.QDir.separator()
init_move_dt = np.dtype({'names':['name','parameter','value'],'formats':['S100','u8','f8']})
inst_combo_width = 80
numberOfDigitsTobeReadForInitialPosition = 5

# list of kind for readout instruments and sweep instruments
readout_kind = [0,1,2,3,12,17]
sweep_kind = [4,5,6,7,8,9,10,11,13,14,15,16]

#-------create parameter list for bool setup-------------
listOfCustomBools = [None, None, None, None, None, None, 'RF', 'AWG', None, None, None, None, 'DSP', None, None,'ATMDelayLine',None,None]
# parameter for RF
param_list = {'RF':['Frequency','Power','Pulse period','Pulse width','Pulse delay','Pulse mod on?','output on?','Pulse source (int or ext)','Pulse mode','Ext trig input src','Ext impedance']}
# parameter for AWG
params = ['Run','All output on?','Run mode','Sampling frequency','Sending trigger','Sending event','ch output on?']
params+= ['ch amplitude [V]','ch offset voltage [V]','ch marker1 high [V]','ch marker1 low [V]','ch marker1 delay [ps]','ch marker2 high [V]','ch marker2 low[V]']
params+= ['ch marker2 delay [ps]','ch skew [ps]','Initial function execution']
s = [' output on?',' amplitude [V]',' offset voltage',' marker1 high',' marker1 low',' marker1 delay',' marker2 high',' marker2 low',' marker2 delay',' skew']
for i in range(4):
    for j in s:
        item = 'ch'+str(i+1)+j
        params +=[item]
param_list.update({'AWG':params})
# parameter for DSP lock-in readout
params = ['Singnal channel coupling','Signal channel input mode','Signal channel FET or Bipolar','Signal channel line filter','Auto ac gain','AC gain','Sensitivity']
params+= ['Auto sensitivity','Auto phase','Auto sensitivity & phase','Time constant','Reference channel source','Oscillator amplitude','Oscillator frequency','Parameter to be read']
param_list.update({'DSP':params})
# parameter for ATM delay line
params = ['Echo Mode', 'Acceleration', 'Deceleration', 'Velocity Initial', 'Velocity Maximum', 'Initialize to 0 position']
param_list.update({'ATMDelayLine':params})


"""------------------------------
Define different sweep mode
---------------------------------"""
# sweep type
sweeptype = ['Linear','1/x','log10','1_pos']
# Linear: equal space in linear between initial and final, Standard sweep
# 1/x: equal space in 1/x between initial and final, This is useful for Schubnikov de haas measurement.
# log10: equal space in log10 between initial and final , Just implemented but not sure it is useful or not.
# 1_pos: Insert single value to 1 point of certain dimension, This is useful to insert AWG event, trigger or custom wait time during the measurement

def arrayGenerator(dims = [101], axis=0, initial = -0.1, final = -0.2, method = 'Linear'):
    if not method in sweeptype:
        method = 'Linear'
        
    if method == 'Linear':
        array = np.moveaxis(np.ones(tuple(dims), dtype=np.float), axis, -1)
        array *= np.linspace(initial, final, num=dims[axis], dtype=np.float)
        array = np.moveaxis(array, -1, axis)
    elif method == '1/x':
        array = np.moveaxis(np.ones(tuple(dims), dtype=np.float), axis, -1)
        array *= np.reciprocal(np.linspace(1/initial,1/final,num=dims[axis],dtype=np.float))
        array = np.moveaxis(array, -1, axis)
    elif method == 'log10':
        array = np.moveaxis(np.ones(tuple(dims), dtype=np.float), axis, -1)
        array *= np.power(10, np.linspace(np.log10(initial),np.log10(final),num=dims[axis],dtype=np.float))
        array = np.moveaxis(array, -1, axis)
    elif method == '1_pos':
        """ initial specify the position in the product up to axis, final specifies the value to be inserted """
        array = np.zeros(tuple(dims), dtype=np.float)
        repetition = np.prod(np.array(dims[0:axis+1]))
        if initial == -1:
            initial = repetition -1
        sl = np.array(range(0, array.size, repetition), dtype=np.int) + initial
        array = array.reshape(-1, order='F')
        array[sl.astype(np.int)]=final
        array = array.reshape(tuple(dims), order='F')
    return array

def getInitialFinal(data, sweepDim, method):
    """ Get parameters for londing to square sweep tab """
    if not method in sweeptype:
        method = 'Linear'
    
    if method == 'Linear' or method == '1/x' or method == 'log10':
        data = data.reshape(-1)
        initial = data[0]
        final = data[-1]
    elif method == '1_pos':
        repetition = np.prod(np.array(list(data.shape)[0:sweepDim+1]))
        data = data.reshape(-1, order='F')[0:repetition+1]
        initial = np.nonzero(data)[0][0]
        final = data[initial]
    
    return initial, final
    
def getBaseAndVectors(data, method):
    """ Get parameters for londing to vector sweep tab """
    if not method in sweeptype:
        method = 'Linear'
    
    if method == 'Linear' or method == '1/x' or method == 'log10':
        dimsize = len(data.shape)
        vectors = [0]*dimsize
        base = data[tuple(vectors)]
        for i in range(dimsize):
            delta = [0]*dimsize
            delta[i]=-1
            vec = data[tuple(delta)] - base
            vectors[i]=vec
        
    elif method == '1_pos': # suppose this method is used only along 1 vector
        dshape = data.shape
        vectors = [0]*len(dshape)
        data = data.reshape(-1, order='F')
        nonzero = np.nonzero(data)[0]
        base = nonzero[0]
        value = data[base]
        if len(nonzero)==1:
            vectors[-1] = value
        else:
            dif = nonzero[1]-base
            repetition = dshape[0]
            i=0
            while dif > repetition:
                i += 1
                dif = dif // repetition
                repetition = dshape[i]
            else:
                vectors[i] = value
    
    return base, vectors

"""-----------------------------
class for basic components
----------------------"""
class inst_list():
    """use this class to get the instrument list"""
    def __init__(self,
                 configFilePath=''):
        self.configFilePath = configFilePath
        self.list = self.getInstList()
        
    def getInstList(self):
        if not self.configFilePath == '':
            with h5py.File(self.configFilePath, 'r') as f:
                dset=f['Meas_config']
                inst_list = list(dset.attrs['Inst_list'])
        else:
            inst_list = list()
        print('inst_list')
        print(inst_list)
        return inst_list

"""------------------------------------
Classes for vector sweep tab
---------------------------------------"""
class vectorSweepBase(QtWidgets.QWidget):
    """ Widget for the base position of the vector sweep """
    def __init__(self,
                 parent=None,
                 ):
        super(vectorSweepBase, self).__init__()
        self.updateCount = 0
        self.gl = QtWidgets.QGridLayout()
        self.gl.setSpacing(0)
        selecLabel = QtWidgets.QLabel('inst')
        selecLabel.setFixedSize(50,15)
        self.selec = QtWidgets.QComboBox()
        self.selec.setFixedSize(inst_combo_width,25)
        self.selec.currentIndexChanged.connect(self.checkUse)
        stypeLabel = QtWidgets.QLabel('type')
        stypeLabel.setFixedSize(50,15)
        self.stype = QtWidgets.QComboBox()
        self.stype.addItems(sweeptype)
        self.stype.setFixedSize(inst_combo_width,25)
        self.stype.currentIndexChanged.connect(self.checkUse)
        baseLabel = QtWidgets.QLabel('base')
        baseLabel.setFixedSize(50,15)
        self.base = QFloatLineEdit()
        self.base.setFixedSize(80,25)
        useLabel = QtWidgets.QLabel('use?')
        useLabel.setFixedSize(40,15)
        self.use = QtWidgets.QCheckBox()
        self.use.setFixedSize(40,25)
        
        self.gl.addWidget(selecLabel,0,0,1,1)
        self.gl.addWidget(self.selec,1,0,1,1)
        self.gl.addWidget(stypeLabel,0,1,1,1)
        self.gl.addWidget(self.stype,1,1,1,1)
        self.gl.addWidget(baseLabel,0,2,1,1)
        self.gl.addWidget(self.base,1,2,1,1)
        self.gl.addWidget(useLabel,0,3,1,1)
        self.gl.addWidget(self.use,1,3,1,1)
        self.setLayout(self.gl)
        self.setFixedSize(120+inst_combo_width*2,40)
        
    def getInst(self):
        use = self.gl.itemAtPosition(1,3).widget().checkState()
        if use != 0:
            inst = str(self.gl.itemAtPosition(1,0).widget().currentText())
        else:
            inst = None
        return inst
        
    def getValue(self):
        use = self.gl.itemAtPosition(1,3).widget().checkState()
        if use != 0:
            value = float(self.gl.itemAtPosition(1,2).widget().get_value())
        else:
            value = None
        return value
        
    def updateList(self, instList):
        w = self.gl.itemAtPosition(1,0).widget()
        name = w.currentText()
        w.clear()
        self.updateCount = 0
        w.addItems(instList)
        self.updateCount = 1
        n = w.findText(name, QtCore.Qt.MatchFixedString)
        if n >=0:
            self.updateCount = 0
            w.setCurrentIndex(n)
            self.updateCount = 1
            
    def checkUse(self):
        if self.updateCount > 0:
            self.use.setCheckState(2)
        else:
            self.updateCount += 1
        
class vectorSweepVec(QtWidgets.QWidget):
    """ Widget for the vector position of the vector sweep """
    def __init__(self,
                 parent=None,
                 ):
        super(vectorSweepVec, self).__init__()
        self.gl = QtWidgets.QGridLayout()
        self.gl.setSpacing(0)
        label = QtWidgets.QLabel('vector')
        self.vec = QFloatLineEdit()
        self.vec.setFixedSize(80,25)
        
        self.gl.addWidget(label,0,0,1,1)
        self.gl.addWidget(self.vec,1,0,1,1)
        self.setLayout(self.gl)
        self.setFixedSize(80, 40)
        
    def getValue(self):
        value = self.vec.get_value()
        return value
        
class vectorSweep(QtWidgets.QWidget):
    """ Main widget for the vector sweep """
    def __init__(self,
                 parent=None,
                 rNo = 3,
                 cNo = 2,
                 instList = ['counter']
                 ):
        super(vectorSweep, self).__init__()
        self.instList = instList
        # define components
        grid = QtWidgets.QGridLayout()
        rlabel = QtWidgets.QLabel('No of inst.')
        rlabel.setFixedSize(70,25)
        grid.addWidget(rlabel,0,0,1,1)
        self.rNo = QtWidgets.QSpinBox()
        self.rNo.setFixedSize(70,25)
        self.rNo.setRange(1,100)
        self.rNo.setValue(rNo)
        self.rNo.valueChanged.connect(self.rowUpdate)
        grid.addWidget(self.rNo,1,0,1,1)
        clabel = QtWidgets.QLabel('No of vec.')
        clabel.setFixedSize(70,25)
        grid.addWidget(clabel,2,0,1,1)
        self.cNo = QtWidgets.QSpinBox()
        self.cNo.setFixedSize(70,25)
        self.cNo.setRange(1,100)
        self.cNo.setValue(cNo)
        self.cNo.valueChanged.connect(self.colUpdate)
        grid.addWidget(self.cNo,3,0,1,1)
        
        self.base = oneDgui(label='',
                            size = rNo,
                            widget=vectorSweepBase,
                            height = 50,
                            width = 150+inst_combo_width*2,
                            vertical = True,
                            showSizeControl = False)
        for i in range(self.base.size):
            self.base.grid.itemAtPosition(i,0).widget().updateList(self.instList)
        
        self.vectos = twoDgui(label = '',
                              initial_size=[rNo,cNo],
                              widget=vectorSweepVec,
                              hight=50,
                              width=100,
                              showSizeControl = False)
        
        grid.addWidget(self.base,0,1,10,4)
        grid.addWidget(self.vectos,0,5,10,10)
        
        self.setLayout(grid)
        w1 = self.base.width()
        h1 = self.base.height()
        w2 = self.vectos.width()
        h2 = self.vectos.height()
        self.setFixedSize(80+w1+w2, max(h1+40, h2+40, 140))
        
    def rowUpdate(self):
        row = self.rNo.value()
        self.base.counter.setValue(row)
        self.vectos.rcounter.setValue(row)
        w1 = self.base.width()
        h1 = self.base.height()
        w2 = self.vectos.width()
        h2 = self.vectos.height()
        self.setFixedSize(80+w1+w2, max(h1+40, h2+40, 140))
        self.updateInstList()
        
    def colUpdate(self):
        col = self.cNo.value()
        self.vectos.ccounter.setValue(col)
        w1 = self.base.width()
        h1 = self.base.height()
        w2 = self.vectos.width()
        h2 = self.vectos.height()
        self.setFixedSize(80+w1+w2, max(h1+40, h2+40, 140))
        
    def updateInstList(self):
        for i in range(self.base.size):
            try:
                self.base.grid.itemAtPosition(i,0).widget().updateCount = 0
                self.base.grid.itemAtPosition(i,0).widget().updateList(self.instList)
            except:
                pass

"""--------------------------
classes for square sweep tab
-----------------------------"""
class SquareSweep(QtWidgets.QWidget):
    """ base widget of the square sweep """
    def __init__(self,
                 parent=None,
                 ItemList = ['counter'],):
        super(SquareSweep, self).__init__()
        self.updateCount = 0
        # Instrument selection 
        selection_label = QtWidgets.QLabel('Inst')
        selection_label.setFixedSize(50,15)
        self.selection = QtWidgets.QComboBox()
        self.selection.setFixedSize(inst_combo_width,20)
        self.selection.addItems(ItemList)
        self.selection.currentIndexChanged.connect(self.checkUse)
        # sweep method
        stype_label = QtWidgets.QLabel('type')
        stype_label.setFixedSize(50,15)
        self.stype = QtWidgets.QComboBox()
        self.stype.setFixedSize(60,20)
        self.stype.addItems(sweeptype)
        # use ?
        use_label = QtWidgets.QLabel('use?')
        self.use = QtWidgets.QCheckBox()
        # sweep from
        init_label = QtWidgets.QLabel('from')
        init_label.setFixedSize(50,15)
        self.init = QFloatLineEdit()
        self.init.setFixedSize(inst_combo_width,20)
        self.init.set_value(0.0)
        # sweep to
        final_label = QtWidgets.QLabel('to')
        final_label.setFixedSize(50,15)
        self.final = QFloatLineEdit()
        self.final.setFixedSize(60,20)
        self.final.set_value(0.0)
        
        # Difine layout
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.grid.addWidget(selection_label,0,0,1,1)
        self.grid.addWidget(self.selection,1,0,1,1)
        self.grid.addWidget(stype_label,0,1,1,1)
        self.grid.addWidget(self.stype,1,1,1,1)
        self.grid.addWidget(init_label,2,0,1,1)
        self.grid.addWidget(self.init,3,0,1,1)
        self.grid.addWidget(final_label,2,1,1,1)
        self.grid.addWidget(self.final,3,1,1,1)
        self.grid.addWidget(use_label,0,2,1,1)
        self.grid.addWidget(self.use,1,2,1,1)
        
        self.setFixedSize(110+inst_combo_width,100)
        self.setLayout(self.grid)
        
    def updateList(self, instList):
        w = self.selection
        name = w.currentText()
        w.clear()
        self.updateCount = 0
        w.addItems(instList)
        self.updateCount = 1
        n = w.findText(name, QtCore.Qt.MatchFixedString)
        if n >=0:
            self.updateCount = 0
            w.setCurrentIndex(n)
            self.updateCount = 1
        
    def checkUse(self):
        if self.updateCount > 0:
            self.use.setCheckState(2)
        else:
            self.updateCount += 1

class SweepParameters(QtWidgets.QWidget):
    """ Main widget for the square sweep """
    def __init__(self,
                 parent=None,
                 row_size=4,
                 col_size=3,
                 ItemList = ['counter'],
                 ):
        super(SweepParameters, self).__init__()
        # Sweep setup
        self.ItemList = ItemList
        self.rowSize = QtWidgets.QSpinBox() # Number of row
        self.rowSize.setRange(1,100)
        self.rowSize.setValue(row_size)
        self.rowSize.valueChanged.connect(self.setSweepArray)
        self.colSize = QtWidgets.QSpinBox() # Number of column
        self.colSize.setRange(1,20)
        self.colSize.setValue(col_size)
        self.colSize.valueChanged.connect(self.setSweepArray)
        self.sweepArray = twoDgui(label = '', # List of single sweep infor widgets
                              initial_size=[row_size,col_size],
                              widget=SquareSweep,
                              hight=100,
                              width=20+110+inst_combo_width,
                              showSizeControl = False)
        self.setSweepArray()
        
        self.ly = QtWidgets.QGridLayout()
        self.ly.setSpacing(0)
        self.ly.addWidget(self.rowSize,0,0,1,1)
        self.ly.addWidget(self.colSize,1,0,1,1)
        self.ly.addWidget(self.sweepArray,0,1,5,5)
        
        self.setLayout(self.ly)
        
    def setSweepArray(self):
        row = self.rowSize.value()
        col = self.colSize.value()
        self.sweepArray.rcounter.setValue(row)
        self.sweepArray.ccounter.setValue(col)
        for i in range(row):
            for j in range(col):
                w = self.sweepArray.grid.itemAtPosition(i,j).widget()
                w.updateCount = 0
                w.updateList(self.ItemList)
        
        self.adjustSize()
        
"""------------------------------
Base widget for the sweep dimension
---------------------------------"""
class Sweep_dim_gui(QtWidgets.QSpinBox):
    def __init__(self,
                 parent=None,
                 maxVar = 100000000):
        super(Sweep_dim_gui, self).__init__()
        self.setRange(0,maxVar)
        
"""------------------------------
Classes for initial move
---------------------------------"""
class initialMove(QtWidgets.QWidget):
    """ Base element of the initial move """
    def __init__(self,
                 parent=None,
                 name = 'counter'
                 ):
        super(initialMove, self).__init__()
        self.inst = QtWidgets.QLineEdit()
        self.inst.setText(name)
        self.inst.setReadOnly(True)
        self.inst.setFixedSize(60,20)
        self.value = QFloatLineEdit()
        self.value.set_value(0.0)
        self.value.setFixedSize(60,20)
        self.value.textChanged.connect(self.checkMove)
        move_label = QtWidgets.QLabel('move?')
        move_label.setFixedSize(40,15)
        self.move = QtWidgets.QCheckBox()
        self.move.setFixedSize(20,15)
        
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.grid.addWidget(self.inst,0,0,1,2)
        self.grid.addWidget(move_label,1,0,1,1)
        self.grid.addWidget(self.move,1,1,1,1)
        self.grid.addWidget(self.value,2,0,1,2)
        
        self.setLayout(self.grid)
        self.setFixedSize(100,80)
        
    def checkMove(self):
        self.move.setCheckState(2)
        
class initialMoves(QtWidgets.QWidget):
    """ Main widget for the initial move """
    def __init__(self,
                 parent=None,
                 inst_name_list=['counter'],
                 no_of_col = 8,
                 ):
        super(initialMoves, self).__init__()
        self.inst_name_list = inst_name_list
        self.UI_list = []
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.no_of_col = no_of_col
        self.initUI()
        self.setLayout(self.grid)
        
    def initUI(self):
        size = len(self.inst_name_list)
        for i, name in enumerate(self.inst_name_list):
            item = initialMove(name=name)
            self.UI_list.append(item)
            row = i / self.no_of_col
            col = i % self.no_of_col
            self.grid.addWidget(item,row,col,1,1)
        if size/self.no_of_col > 0:
            self.setFixedSize(60+self.no_of_col*70, 20+(size/self.no_of_col+1)*70)
        else:
            self.setFixedSize(60+size*70,80)
        
    def exportInitMoves(self):
        l = []
        for i in self.UI_list:
            if not i.move.checkState()==0:
                l.append((i.inst.text(),0,i.value.get_value()))
        initmove = np.array(l,dtype=init_move_dt)
        return initmove

"""---------------------------------------
classes for instruments bools
------------------------------------------"""
class Inst_bool_setup_UI(QtWidgets.QWidget):
    """ Widget for bool number setup """
    def __init__(self,
                 parent=None,
                 kind=100,
                 valueUI=[],
                 ):
        super(Inst_bool_setup_UI, self).__init__()
        self.kind = kind
        self.valueUI = valueUI
        self.value = int(valueUI.text())
        self.okBtn = QtWidgets.QPushButton('OK')
        self.okBtn.clicked.connect(self.ok_proc)
        self.uiList = []
        self.ly = QtWidgets.QVBoxLayout()
        self.initUI()
        self.ly.addWidget(self.okBtn)
        widget = QtWidgets.QWidget(parent=self)
        widget.setLayout(self.ly)
        container = QtWidgets.QScrollArea()
        container.setWidget(widget)
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(container)
        self.setLayout(lay)
        
        
    def initUI(self):
        # initialize UI list depending on the kind of the instruments
        name = listOfCustomBools[self.kind]
        if name != None:
            uiList = param_list[name]
        else:
            uiList = ['initialize?']
                    
        for i, item in enumerate(uiList):
            label = QtWidgets.QLabel(item)
            check = QtWidgets.QCheckBox()
            if not ((self.value & 2**i) == 0):
                check.setCheckState(2)
            self.uiList.append(check)
            hb = QtWidgets.QHBoxLayout()
            hb.addWidget(label)
            hb.addWidget(check)
            self.ly.addLayout(hb)
            
    def ok_proc(self):
        value = 0
        for i, item in enumerate(self.uiList):
             if not item.checkState()==0:
                 value += 2**i
        self.valueUI.setText(str(value))
        self.close()
        
        
class Inst_bool(QtWidgets.QWidget):
    """ Base widget for bool list """
    def __init__(self,
                 parent=None,
                 inst_name='counter',
                 kind=100,
                 ):
        super(Inst_bool, self).__init__()
        self.kind = kind
        self.bool_ui = 0
        self.inst = QtWidgets.QLineEdit()
        self.inst.setText(inst_name)
        self.inst.setReadOnly(True)
        self.inst.setFixedSize(60,20)
        self.value = QtWidgets.QLineEdit()
        self.value.setFixedSize(60,20)
        initLabel = QtWidgets.QLabel('Initialize')
        initLabel.setFixedSize(60,20)
        self.value.setText(str(0))
        self.setupBtn = QtWidgets.QPushButton('setup')
        self.setupBtn.setFixedSize(60,30)
        self.setupBtn.clicked.connect(self.setupBool)
        postLabel = QtWidgets.QLabel('Post proc')
        postLabel.setFixedSize(60,30)
        self.value2 = QtWidgets.QLineEdit()
        self.value2.setFixedSize(60,20)
        self.value2.setText(str(0))
        self.setupBtn2 = QtWidgets.QPushButton('setup')
        self.setupBtn2.setFixedSize(60,30)
        self.setupBtn2.clicked.connect(self.setupBool2)
        
        self.ly = QtWidgets.QVBoxLayout()
        self.ly.setSpacing(0)
        self.ly.addWidget(self.inst)
        self.ly.addWidget(initLabel)
        self.ly.addWidget(self.value)
        self.ly.addWidget(self.setupBtn)
        self.ly.addWidget(postLabel)
        self.ly.addWidget(self.value2)
        self.ly.addWidget(self.setupBtn2)
        
        self.setLayout(self.ly)
        
    def setupBool(self):
        """ setup initilization """
        self.bool_ui = Inst_bool_setup_UI(kind=self.kind, valueUI=self.value)
        self.bool_ui.show()
                           
    def setupBool2(self):
        """ setup finalization """
        self.bool_ui = Inst_bool_setup_UI(kind=self.kind, valueUI=self.value2)
        self.bool_ui.show()
   
class Inst_bools(QtWidgets.QWidget):
    """ list of bool setup widget """
    def __init__(self,
                 parent=None,
                 inst_name_list=['counter'],
                 kind_list = [6],
                 ):
        super(Inst_bools, self).__init__()
        self.inst_name_list = inst_name_list
        self.UI_list = []
        self.kind_list = kind_list
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.initUI()
        self.setLayout(self.grid)
        
    def initUI(self):
        size = len(self.inst_name_list)
        for i, name in enumerate(self.inst_name_list):
            item = Inst_bool(inst_name=name, kind=self.kind_list[i])
            self.UI_list.append(item)
            self.grid.addWidget(item, 0, i, 1, 1)
        self.setFixedSize(60+size*70, 200)
        
    def exportInstBools(self, writeInstList):
        size = len(writeInstList)
        blist = []
        for i in range(size):
            name = writeInstList[i]
            for k in self.UI_list:
                if name == k.inst.text():
                    blist.append([int(k.value.text()),int(k.value2.text())])
        print('blist')
        print(blist)
        return blist
        
"""---------------------------
------------------------------
main window
------------------------------
---------------------------"""
class Main_window(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 numOfParameters=4,
                 numOfDims=3,
                 ):
        super(Main_window, self).__init__()
        self.exp = Experiment()
        self.config = MeasConfig()
        self.instInfos = [['a'],[0],['b'],[0]]
        self.error = QtWidgets.QErrorMessage()
        
        #------ save file path and configu file path ------------------
        # widget to choose the path to save the created experiment file
        savePath_label = QtWidgets.QLabel('save folder')
        self.savePathBtn = QtWidgets.QPushButton('Load')
        self.savePathBtn.clicked.connect(self.savePathDialog)
        self.savePath = QtWidgets.QLineEdit()

        # widget to choose the file name 
        saveFile_label = QtWidgets.QLabel('save name')
        self.saveFile = QtWidgets.QLineEdit()        
        # saveFile_label_comment = QtWidgets.QLabel('without .h5 extension')
        yyyymmddhhmm_label = QtWidgets.QLabel('yymmhh format')
        self.yyyymmddhhmm = QtWidgets.QCheckBox()
        
        # widget to choose the configuration file to be used for experiment file creation
        config_label = QtWidgets.QLabel('config file')
        self.configBtn = QtWidgets.QPushButton('Load')
        self.configBtn.clicked.connect(self.configFileDialog)
        self.configFile = QtWidgets.QLineEdit()
        
        # Div - file load/save
        pathLine = QtWidgets.QGridLayout()
        pathLine.setSpacing(1)

        # First Line
        pathLine.addWidget(savePath_label, 1, 1)
        pathLine.addWidget(self.savePathBtn, 1, 2)
        pathLine.addWidget(self.savePath, 1, 3)

        pathLine.addWidget(saveFile_label, 1, 4)
        pathLine.addWidget(self.saveFile, 1, 5)

        # Second Line
        pathLine.addWidget(config_label, 2, 1)
        pathLine.addWidget(self.configBtn, 2, 2)
        pathLine.addWidget(self.configFile, 2, 3)
        # pathLine.addWidget(saveFile_label_comment, 2, 5)
        pathLine.addWidget(yyyymmddhhmm_label,2,4)
        pathLine.addWidget(self.yyyymmddhhmm,2,5)

        # # BACKUP
        # pathLine = QtWidgets.QHBoxLayout()
        # pathLine.setSpacing(1)
        # pathLine.addWidget(savePath_label)
        # pathLine.addWidget(self.savePathBtn)
        # pathLine.addWidget(self.savePath)

        # pathLine.addWidget(saveFile_label)
        # pathLine.addWidget(self.saveFile)

        # pathLine.addWidget(config_label)
        # pathLine.addWidget(self.configBtn)
        # pathLine.addWidget(self.configFile)


        #---------- sweep dimensions --------------------
        # widget to set the sweep dimension
        sweepDim_container = QtWidgets.QScrollArea()
        self.sweepDim = oneDgui(label = 'sweep dims',
                             size = numOfDims,
                             widget=Sweep_dim_gui,
                             height = 20,
                             width = 70,
                             vertical = False,
                             showSizeControl = True,
                             )
        sweepDim_container.setWidget(self.sweepDim)
        
        #------- return to initial position ?, read initial positions to initial move ?, comments -------
        # widget to store the comments
        commentLabel = QtWidgets.QLabel('Comments')
        self.comments = QtWidgets.QTextEdit()
        self.comments.setFixedSize(300,80)
        # widget to set return to initial position after sweep
        return_label = QtWidgets.QLabel('return to init pos?')
        self.return2initial = QtWidgets.QCheckBox()
        # widget to choose whether you read the initial positions when you load the exp file
        readInitialPosLabel = QtWidgets.QLabel('Read init pos?')
        self.readInitialPos = QtWidgets.QCheckBox()
        
        commentLine = QtWidgets.QHBoxLayout()
        commentLine.setSpacing(1)
        commentLine.addWidget(return_label)
        commentLine.addWidget(self.return2initial)
        commentLine.addWidget(readInitialPosLabel)
        commentLine.addWidget(self.readInitialPos)
        commentLine.addWidget(commentLabel)
        commentLine.addWidget(self.comments)
        
        #------ Initial move & sweep + readout instrument bools --------------
        # Widgets for initial moves
        leftTab = QtWidgets.QTabWidget()
        
        initMoveWidget = QtWidgets.QWidget()
        initMoveLayout = QtWidgets.QVBoxLayout()
        hb = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('Keep init moves')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.initMoveKeep = QtWidgets.QCheckBox()
        hb.addWidget(self.initMoveKeep)
        initMoveLayout.addLayout(hb)
        self.initial_move_container = QtWidgets.QScrollArea()
        self.initial_move = initialMoves(inst_name_list=self.instInfos[2])
        self.initial_move_container.setWidget(self.initial_move)
        initMoveLayout.addWidget(self.initial_move_container)
        initMoveWidget.setLayout(initMoveLayout)
        
        leftTab.addTab(initMoveWidget, 'Init move')
        
        # sweep & readout bools
        boolWidget = QtWidgets.QWidget()
        boolLayout = QtWidgets.QVBoxLayout()
        # widgets for sweep instruments bools
        hb = QtWidgets.QHBoxLayout()
        hb.addWidget(QtWidgets.QLabel('Initialize and post process for sweep instruments'))
        label = QtWidgets.QLabel('Keep bools')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.sbool_keep = QtWidgets.QCheckBox()
        hb.addWidget(self.sbool_keep)
        boolLayout.addLayout(hb)
        self.sweep_bool_container = QtWidgets.QScrollArea()
        self.sweep_bool_container.setFixedHeight(200)
        self.sweep_inst_bools = Inst_bools(inst_name_list=self.instInfos[2], kind_list=self.instInfos[3])
        self.sweep_bool_container.setWidget(self.sweep_inst_bools)
        boolLayout.addWidget(self.sweep_bool_container)
        
        # widgets for readout instruments bools
        hb = QtWidgets.QHBoxLayout()
        hb.addWidget(QtWidgets.QLabel('Initialize and post process for readout instruments'))
        label = QtWidgets.QLabel('Keep bools')
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hb.addWidget(label)
        self.rbool_keep = QtWidgets.QCheckBox()
        hb.addWidget(self.rbool_keep)
        boolLayout.addLayout(hb)
        self.readout_bool_container = QtWidgets.QScrollArea()
        self.readout_bool_container.setFixedHeight(200)
        self.readout_inst_bools = Inst_bools(inst_name_list=self.instInfos[0], kind_list=self.instInfos[1])
        self.readout_bool_container.setWidget(self.readout_inst_bools)
        boolLayout.addWidget(self.readout_bool_container)
        
        boolWidget.setLayout(boolLayout)
        
        leftTab.addTab(boolWidget, 'Instruments init')
        
        # Add the widget into the layout for the left part
        self.ly = QtWidgets.QVBoxLayout()
        self.ly.setSpacing(1)
        self.ly.addLayout(pathLine)
        self.ly.addWidget(sweepDim_container)
        self.ly.addLayout(commentLine)
        self.ly.addWidget(leftTab)
        
        # --------- right area ---------------------
        self.tab = QtWidgets.QTabWidget()
        self.sweep_container = QtWidgets.QScrollArea()
        self.sweep_params = SweepParameters(row_size=numOfParameters,
                                            col_size=numOfDims,
                                            ItemList=self.instInfos[2])
        self.sweep_container.setWidget(self.sweep_params)
        self.tab.addTab(self.sweep_container, 'square sweep')
        
        vector_container = QtWidgets.QScrollArea()
        self.vector_params = vectorSweep(rNo=numOfParameters,
                                         cNo=numOfDims,
                                         instList=self.instInfos[2])
        vector_container.setWidget(self.vector_params)
        self.tab.addTab(vector_container, 'vector sweep')
        
        self.console = IpyConsole.IpyConsoleWidget()
        self.console.ipyConsole.executeCommand('from AnalysisBase.AnalysisFunctions import *')
        self.console.ipyConsole.pushVariables({'main':self})
        self.tab.addTab(self.console, 'console')
        
        
        self.loadBtn = QtWidgets.QPushButton('Load')
        self.loadBtn.clicked.connect(self.loadExp)
        self.createBtn = QtWidgets.QPushButton('Create')
        self.createBtn.clicked.connect(self.createExp)
        self.sendBtn = QtWidgets.QPushButton('Send')
        self.sendBtn.clicked.connect(self.sendExp)
        expBtns = QtWidgets.QHBoxLayout()
        expBtns.addWidget(self.loadBtn)
        expBtns.addWidget(self.createBtn)
        expBtns.addWidget(self.sendBtn)
        
        # add widget into the right tab
        self.ly2 = QtWidgets.QVBoxLayout()
        self.ly2.addWidget(self.tab)
        self.ly2.addLayout(expBtns)
        
        # combine all the layouts
        self.ly3 = QtWidgets.QHBoxLayout()
        self.ly3.setSpacing(1)
        self.ly3.addLayout(self.ly)
        self.ly3.addLayout(self.ly2)
        
        self.setLayout(self.ly3)
        
        """ Try to load the previous files """
        try:
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5', 'r') as f:
                savePath = str(f['saveFolderPath'][...])
                if savePath != '':
                    self.savePath.setText(savePath)
                savePath = str(f['configFilePath'][...])
                if savePath != '':
                    self.configFile.setText(savePath)
                    self.config.fpath = savePath.replace('\\','\\\\')
                    self.config.read()
                    self.instInfos = self.getInstLists()
                    # Init inst list
                    self.updateUIs()
        except:
            pass
    
    """------------------
    Member functions
    ---------------------"""
    def fillDimensions(self, dims):
        """ Function to fill up the sweep dimension widget """
        if self.sweepDim.size < len(dims):
            self.sweepDim.counter.setValue(len(dims))
        for i in range(self.sweepDim.size):
            if i < len(dims):
                no = dims[i]
            else:
                no = 0
            if self.sweepDim.vertical:
                self.sweepDim.grid.itemAtPosition(i,1).widget().setValue(no)
            else:
                self.sweepDim.grid.itemAtPosition(1,i).widget().setValue(no)
                
    def savePathDialog(self):
        """ open dialog to choose the save file path """
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        if self.savePath.text() != '':
            savePath = fileDialog.getExistingDirectory(self, 'Choose folder', directory=os.path.dirname(self.savePath.text()))
        else:
            savePath = fileDialog.getExistingDirectory(self, 'Choose folder')
        if not savePath == '':
            savePath += '/'
            self.savePath.setText(savePath)
            """ save folder path """
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5', 'a') as f:
                dset = f.get('saveFolderPath')
                if dset == None:
                    dset = f.create_dataset('saveFolderPath', data = savePath)
                else:
                    dset[...] = savePath
    
    def configFileDialog(self):
        """ open dialog to choose the configuration file """
        fileDialog = QtWidgets.QFileDialog()
        if self.configFile.text() != '':
            savePath = fileDialog.getOpenFileName(self, 'Choose config file', filter='*.h5', directory=os.path.dirname(self.savePath.text()))
        else:
            savePath = fileDialog.getOpenFileName(self, 'Choose config file', filter='*.h5')
        savePath = savePath[0]
        if not savePath == '':
            self.configFile.setText(savePath)
            """ save file path """
            with h5py.File(os.path.dirname(os.path.abspath(__file__))+'/log.h5', 'a') as f:
                dset = f.get('configFilePath')
                if dset == None:
                    dset = f.create_dataset('configFilePath', data = savePath)
                else:
                    dset[...] = savePath
            """ Load information """
            self.config.fpath = os.path.abspath(savePath)
            self.config.read()
            self.instInfos = self.getInstLists()
            # Init inst list
            self.updateUIs()
        
    
    def loadExp(self):
        """ Function to values from existing experimental file and set up widgets """
        fileDialog = QtWidgets.QFileDialog()
        loadPath = fileDialog.getOpenFileName(self, 'Choose experiment file', filter='*.h5', directory=os.path.dirname(self.savePath.text()))
        loadPath = loadPath[0]
        if not loadPath == '':
            self.exp.filename = loadPath.split('/')[-1].split('.')[0] # remove file extention (.h5)
            self.exp.saveFolder = '/'.join(loadPath.split('/')[:-1])+'/'
            self.exp.read()
            #if configration file sored in the experiment file is found, load it.s
            if os.path.isfile(self.exp.configFile):
                self.configFile.setText(self.exp.configFile.replace(pathSep,'/'))
                self.config.fpath = self.exp.configFile
                self.config.read()
                self.instInfos = self.getInstLists()
                print('load')
                print(self.instInfos)
                self.updateUIs()
            
            # Fill information into UIs
            self.savePath.setText(self.exp.saveFolder)
            # remove sweep information from comments
            pos = str(self.exp.comments).find('----- sweep parameters -----')
            if not pos == -1:
                comments = self.exp.comments[:pos-1]
            else:
                comments = self.exp.comments
            comments = comments[:-1]    # remove line feed in the end
            self.comments.setPlainText(comments)
            
            # set check state of return to initial position after sweep
            if self.exp.Experimental_bool_list[0]:
                self.return2initial.setCheckState(2)
            else:
                self.return2initial.setCheckState(0)
                
            # setup initial move
                # initialize all the init move to uncheck
            for i, name in enumerate(self.initial_move.inst_name_list):
                self.initial_move.UI_list[i].move.setCheckState(0)
                
            for j in self.exp.Initial_move:
                found = 0
                for i, name in enumerate(self.initial_move.inst_name_list):
                    if j['name'].decode('utf-8') == name:
                        self.initial_move.UI_list[i].value.set_value(j['value'])
                        self.initial_move.UI_list[i].move.setCheckState(2)
                        found = 1
                    elif j['name'].decode('utf-8')=='None':
                        found = 1
                        
                if found == 0:
                    print('Proper configuration file is not loaded.')
                    
            # Read and set the initial positions if exists
            if self.readInitialPos.checkState() == 2:
                if not self.exp.Initial_positions == []:
                    for i, inst in enumerate(self.exp.Initial_positions):
                        found = 0
                        for j, name in enumerate(self.initial_move.inst_name_list):
                            if inst['Name'].decode('utf-8')== name:
                                self.initial_move.UI_list[j].value.set_value(round(inst['Value'], numberOfDigitsTobeReadForInitialPosition))
                                self.initial_move.UI_list[j].move.setCheckState(2)
                                found = 1
                            elif inst['Name'].decode('utf-8')=='None':
                                found = 1
                        if found == 0:
                            print('Proper configuration file is not loaded.')
                            
            # setup dim sizes
            self.fillDimensions(list(self.exp.dim))
            
            # setup sweep inst bools
            sindex = 0
            rindex = 0
            for i, item in enumerate(self.config.list):
                if item.kind in sweep_kind:
                #    sweep_inst = True
                    # setup sweep instruments bools
                    if item.name in self.sweep_inst_bools.inst_name_list:
                        n = self.sweep_inst_bools.inst_name_list.index(item.name)
                        self.sweep_inst_bools.UI_list[n].value.setText(str(self.exp.sweep_inst_bools[sindex][0]))
                        self.sweep_inst_bools.UI_list[n].value2.setText(str(self.exp.sweep_inst_bools[sindex][1]))
                        sindex += 1
                    else:
                        print('cannot find %s in sweep bool GUIs. Please check the configuration file.')
                elif item.kind in readout_kind:
                #    sweep_inst = False
                    # setup readout instruments bools
                    if item.name in self.readout_inst_bools.inst_name_list:
                        n = self.readout_inst_bools.inst_name_list.index(item.name)
                        self.readout_inst_bools.UI_list[n].value.setText(str(self.exp.readout_inst_bools[rindex][0]))
                        self.readout_inst_bools.UI_list[n].value2.setText(str(self.exp.readout_inst_bools[rindex][1]))
                        rindex += 1
                    else:
                        print('cannot find %s in readout bool GUIs. Please check the configuration file.')

        #        if sweep_inst:
        #            found = 0
        #            for j, name2 in enumerate(self.sweep_inst_bools.inst_name_list):
        #                if item.name == name2:
        #                    self.sweep_inst_bools.UI_list[j].value.setText(str(self.exp.sweep_inst_bools[index][0]))
        #                    self.sweep_inst_bools.UI_list[j].value2.setText(str(self.exp.sweep_inst_bools[index][1]))
        #                    found = 1
        #            index += 1
        #            if found == 0:# In case the instrument is not found in the current list add an instrument to the list (under construction)
        #                print('Proper configuration file is not loaded.')
                        
        #     setup readout inst bools (Known problem: It does not work for ADC.)
        #    for i, name in enumerate(self.exp.readoutlist):
        #        for j, name2 in enumerate(self.readout_inst_bools.inst_name_list):
        #            if name == name2:
        #                self.readout_inst_bools.UI_list[j].value.setText(str(self.exp.readout_inst_bools[i][0]))
        #                self.readout_inst_bools.UI_list[j].value2.setText(str(self.exp.readout_inst_bools[i][1]))
                        
            # Read data and set data
            if self.tab.currentIndex()==0:
                # check the current dimension of UIs and measurement dimension
                no_var = len(self.exp.sweeplist)
                sweep_dim = len(self.exp.dim)
                if sweep_dim > self.sweep_params.colSize.value():
                    self.sweep_params.colSize.setValue(sweep_dim)
                if no_var > self.sweep_params.rowSize.value():
                    self.sweep_params.rowSize.setValue(no_var)
                    
                #Initialize use check to none
                for i in range(self.sweep_params.rowSize.value()):
                    for j in range(self.sweep_params.colSize.value()):
                        self.sweep_params.sweepArray.grid.itemAtPosition(i,j).widget().use.setCheckState(0)
                    
                indexes = [0]*len(self.exp.dim)
                for i in self.exp.sweeplist:
                    name = i.name
                    data = i.array
                    try:
                        method = i.creationMethod
                    except:
                        method = 'Linear'
                    sweepDim = i.sweep_dim
                    if sweepDim != 0:   # if sweepDim is not 0 (meaning file was created by square sweep UI), -1 to be able to use as axis.
                        sweepDim -= 1
                    else:
                        print('This file was not created by square sweep GUI.')
                        
                    item = self.sweep_params.sweepArray.grid.itemAtPosition(indexes[sweepDim], sweepDim).widget()
                    indexes[sweepDim] = indexes[sweepDim]+1
                    n = item.selection.findText(name, QtCore.Qt.MatchFixedString)
                    m = item.stype.findText(method, QtCore.Qt.MatchFixedString)
                    if n >= 0:
                        item.selection.setCurrentIndex(n)
                        item.stype.setCurrentIndex(m)
                        initial, final = getInitialFinal(data, sweepDim, method)
                        item.init.set_value(initial)
                        item.final.set_value(final)
                        item.use.setCheckState(2)
                    else:
                        print('Proper configuration is not loaded.')
                        
            elif self.tab.currentIndex()==1:
                no_var = len(self.exp.sweeplist)
                sweep_dim = len(self.exp.dim)
                self.vector_params.cNo.setValue(sweep_dim)
                self.vector_params.rNo.setValue(no_var)
                    
                index = 0
                for i in range(no_var):
                    setup = False
                    name = self.exp.sweeplist[i].name
                    data = self.exp.sweeplist[i].array
                    try:
                        method = self.exp.sweeplist[i].creationMethod
                    except:
                        method = 'Linear'
                    base, vectors = getBaseAndVectors(data, method)
                    if self.vector_params.base.vertical:
                        w = self.vector_params.base.grid.itemAtPosition(index, 0).widget()
                    else:
                        w = self.vector_params.base.grid.itemAtPosition(0, index).widget()
                    n = w.selec.findText(name, QtCore.Qt.MatchFixedString)
                    m = w.stype.findText(method, QtCore.Qt.MatchFixedString)
                    if n >= 0:
                        index += 1
                        setup = True
                        w.use.setCheckState(2)
                        w.base.set_value(base)
                        w.selec.setCurrentIndex(n)
                        w.stype.setCurrentIndex(m)
                    else:
                        print('Proper configuration file is not loaded.')
                        
                    for j in range(sweep_dim):
                        if setup:
                            self.vector_params.vectos.grid.itemAtPosition(i,j).widget().vec.set_value(vectors[j])
                
            # initialize exp.sweeplist for next use if the selected tab is not console.
            if not self.tab.currentIndex()==2:
                self.exp.sweeplist = []
        
    def createExp(self):
        result_error = 0
        # File name = time
        # self.exp.filename = time.strftime('%Y%m%d%H%M')
        # File name = user choice

        if not self.yyyymmddhhmm.checkState()== 0:
            self.exp.filename = time.strftime('%Y%m%d%H%M')
        else:
            self.exp.filename = self.saveFile.text()
        
        self.exp.saveFolder = os.path.abspath(self.savePath.text())+pathSep#.replace('\\','\\\\')
        self.exp.configFile = os.path.abspath(self.configFile.text())#.replace('\\','\\\\')
   
        self.exp.dim = []
        for i in range(self.sweepDim.size):
            if self.sweepDim.vertical:
                value = self.sweepDim.grid.itemAtPosition(i,1).widget().value()
            else:
                value = self.sweepDim.grid.itemAtPosition(1,i).widget().value()
                
            if value>0:
                self.exp.dim.append(value)
            else:
                break
                
        self.exp.comments = self.comments.toPlainText()
        if self.return2initial.checkState() == 0:
            self.exp.Experimental_bool_list = [False, False]
        else:
            self.exp.Experimental_bool_list = [True, False]
        self.exp.Initial_move = self.initial_move.exportInitMoves()
        if self.exp.Initial_move.size==0:
            self.exp.Initial_move = np.array([('None',100,0.0)],dtype=init_move_dt)
        self.exp.index = np.array(self.exp.dim)-1
        self.exp.readoutlist = self.instInfos[0]
        print('readout_list export')
        print(self.instInfos[0])
        self.exp.readout_inst_bools = self.readout_inst_bools.exportInstBools(self.instInfos[0])
        print('readout_bools export')
        print(self.exp.readout_inst_bools)
        
        if self.tab.currentIndex()==0:
            # square sweep
            self.setSweepListandBools()
        elif self.tab.currentIndex()==1:
            # vector sweep
            ret = self.setSweepListandBoolsForVector()
            if ret[0] == 1:
                # escape if the dimension of the parameter is not correct.
                print(ret[1])
                return 1
        elif self.tab.currentIndex()==2:
            # console
            self.setSweepBoolsandDims()
        
        # quit the program if all the dimension size is 0.
        if not len(self.exp.dim)==0:
            if os.path.isfile(self.exp.saveFolder+self.exp.filename+'.h5'):
                i=0
                while os.path.isfile(self.exp.saveFolder+self.exp.filename+'_'+str(i)+'.h5'):
                    i+=1
                else:
                    self.exp.filename += '_'+str(i)
            result_error = self.exp.write()
            # initialize exp.sweeplist for next use
            self.exp.sweeplist = []
            
        if result_error == 0:
            print("\n\n self.exp.saveFolder : \t"+self.exp.saveFolder+self.exp.filename+'.h5'+"\n")
            return self.exp.saveFolder+self.exp.filename+'.h5'
        else:
            self.error.showMessage('File creation has failed. Please check the input parameters.')
            return 1
         
    def sendExp(self):
        filePath = [self.createExp()]
        if not filePath == [1]:
            if platform.system()=='Windows':
                sfn.sendFiles(fileList = filePath)
                pass
            elif platform.system()=='Darwin':
                pass        
        
    def getInstLists(self):
        readoutList = []
        readoutKindList = []
        sweep_inst_list = []
        sweep_inst_kind_list = []
        for i in self.config.list:
            if i.kind in readout_kind:
                readoutList.append(i.name)
                readoutKindList.append(i.kind)
                
            if i.kind in sweep_kind:
                sweep_inst_list.append(i.name)
                sweep_inst_kind_list.append(i.kind)
            
        print('inst_list')
        print([readoutList,readoutKindList,sweep_inst_list,sweep_inst_kind_list])
        return [readoutList,readoutKindList,sweep_inst_list,sweep_inst_kind_list]
        
    def setSweepListandBools(self):
        """ this function is used in square sweep mode. """
        self.exp.sweep_inst_bools=[]
        for k in self.sweep_inst_bools.UI_list:
            self.exp.sweep_inst_bools.append([int(k.value.text()),int(k.value2.text())])
        sweepList=[]
        dims = self.exp.dim
        self.exp.comments += os.linesep # make comment to indicate the sweep dimension
        self.exp.comments += '----- sweep parameters -----'+ os.linesep
        for i, dim in enumerate(dims):
            self.exp.comments += 'step%d, %d points, ' % (i+1, dim)
            for j in range(self.sweep_params.sweepArray.r):
                item = self.sweep_params.sweepArray.grid.itemAtPosition(j,i).widget()
                if not item.use.checkState() == 0:
                    selec = item.selection.currentText()
                    if not (selec in sweepList):
                        sweepList.append(selec)
                        ini = item.init.get_value()
                        fin = item.final.get_value()
                        method = str(item.stype.currentText())
                        ar = arrayGenerator(dims, i, ini, fin, method)
                        ss = single_sweep(name=selec,
                                          ar = ar,
                                          parameter = 0,
                                          sweep_dim = i+1,
                                          creationMethod = method
                                          )
                        self.exp.comments += '%s: from %f to %f, ' % (selec, ini, fin)
                        for k in self.sweep_inst_bools.UI_list:
                            if selec == k.inst.text():
                                ss.bools=[int(k.value.text()),int(k.value2.text())]
                    #    self.exp.sweep_inst_bools.append(ss.bools)
                        self.exp.sweeplist.append(ss)
            self.exp.comments += os.linesep
            
    def setSweepListandBoolsForVector(self):
        """ this function is used in vector sweep mode. """
        self.exp.sweep_inst_bools=[]
        for k in self.sweep_inst_bools.UI_list:
            self.exp.sweep_inst_bools.append([int(k.value.text()),int(k.value2.text())])
        sweepList=[]
        dims = self.exp.dim
        
        # if sweep dimension is bigger than the number of vector defined, return error message.
        if len(list(dims))>self.vector_params.vectos.c:
            return (1, 'check the number of vector and sweep dimensions')
            
        self.exp.comments += os.linesep # make comment to indicate the sweep dimension
        self.exp.comments += '----- sweep parameters -----'+ os.linesep
        for i in range(self.vector_params.base.size):
            w = self.vector_params.base.grid.itemAtPosition(i,0).widget()
            name = w.getInst()
            method = str(w.stype.currentText())
            if not name == None:
                if not (name in sweepList):
                    sweepList.append(name)
                    base_value = w.getValue()
                    self.exp.comments += '%s: base position = %f, ' % (name, base_value)
                    ss = single_sweep(name=name,
                                      creationMethod=method)
                    ss.array = np.ones(dims, dtype=np.float64)*base_value
                    for j, dim in enumerate(dims):
                        vec_value = self.vector_params.vectos.grid.itemAtPosition(i,j).widget().getValue()
                        self.exp.comments += 'vec%d = %f, ' % (j, vec_value)
                        ss.array += arrayGenerator(dims, j, base_value, vec_value, method)
                    #    ss.array += np.moveaxis(np.moveaxis(np.ones(dims,dtype=np.float64),j,-1)*np.linspace(0,vec_value,dim),-1,j)
                    self.exp.comments += os.linesep
                    self.exp.sweeplist.append(ss)
        return (0, 'OK')
                        
    def setSweepBoolsandDims(self):
        """ This function is used with console. """
        self.exp.sweep_inst_bools = []
        for j in self.sweep_inst_bools.UI_list:
            self.exp.sweep_inst_bools.append([int(j.value.text()),int(j.value2.text())])
        for i, item in enumerate(self.exp.sweeplist):
            if i == 0:
                self.exp.dim = list(item.array.shape)
            self.exp.sweeplist[i]=item
                        
    def updateUIs(self):
        # update inst list of square sweep
        self.sweep_params.ItemList = self.instInfos[2]
        self.sweep_params.setSweepArray()
        # update inst list of vector sweep
        self.vector_params.instList = self.instInfos[2]
        self.vector_params.updateInstList()
        # update sweep inst bools while keeping the previous values
        if self.sbool_keep.checkState()==2:
            sbool_list = list()
            for item in self.sweep_inst_bools.UI_list:
                dic = {'kind':item.kind,'inst':item.inst.text(),'value':item.value.text(),'value2':item.value2.text()}
                sbool_list.append(dic)
        self.sweep_inst_bools = Inst_bools(inst_name_list=self.instInfos[2], kind_list=self.instInfos[3]) # reinitialize UIs
        if self.sbool_keep.checkState()==2:
            for item in sbool_list: # recall the old values
                try:
                    n = self.sweep_inst_bools.inst_name_list.index(item['inst'])
                    ui = self.sweep_inst_bools.UI_list[n]
                    ui.kind = item['kind']
                    ui.inst.setText(item['inst'])
                    ui.value.setText(item['value'])
                    ui.value2.setText(item['value2'])
                except:
                    pass
        self.sweep_bool_container.setWidget(self.sweep_inst_bools)
        # update readout inst bools while keeping the previous values
        if self.rbool_keep.checkState()==2:
            rbool_list = list()
            for item in self.readout_inst_bools.UI_list:
                dic = {'kind':item.kind,'inst':item.inst.text(),'value':item.value.text(),'value2':item.value2.text()}
                rbool_list.append(dic)
        self.readout_inst_bools = Inst_bools(inst_name_list=self.instInfos[0], kind_list=self.instInfos[1]) # reinitialize UIs
        for item in self.readout_inst_bools.UI_list: # initialize all the readout instruments bools to 1
            item.value.setText('1')
        if self.rbool_keep.checkState()==2:
            for item in rbool_list: # recall the old values
                try:
                    n = self.readout_inst_bools.inst_name_list.index(item['inst'])
                    ui = self.readout_inst_bools.UI_list[n]
                    ui.kind = item['kind']
                    ui.inst.setText(item['inst'])
                    ui.value.setText(item['value'])
                    ui.value2.setText(item['value2'])
                except:
                    pass
        self.readout_bool_container.setWidget(self.readout_inst_bools)
        # update initial move while keeping the previous values
        if self.initMoveKeep.checkState()==2:
            initMove = list() # store old information
            for item in self.initial_move.UI_list:
                dic = {'inst':item.inst.text(),'value':item.value.get_value(),'move':item.move.checkState()}
                initMove.append(dic)
        self.initial_move = initialMoves(inst_name_list=self.instInfos[2]) # reinitialize UIs
        if self.initMoveKeep.checkState()==2:
            for item in initMove: # recall the old values
                try:
                    n = self.initial_move.inst_name_list.index(item['inst'])
                    ui = self.initial_move.UI_list[n]
                    ui.inst.setText(item['inst'])
                    ui.value.set_value(item['value'])
                    ui.move.setCheckState(item['move'])
                except:
                    pass
        self.initial_move_container.setWidget(self.initial_move)
    
        
if __name__=='__main__':
    qApp = QtWidgets.QApplication(sys.argv)
    
#    v = vectorSweep()
#    v.show()
#    ss = SquareSweep()
#    ss.show()
#    ew = SweepParameters()
#    ew.show()
#    sd = Sweep_dim_gui()
#    sd.show()
#    im = Inst_bool()
#    im.show()
    
#    value2 = QtWidgets.QLineEdit()
#    value2.setFixedSize(60,20)
#    value2.setText(str(3))
#    ib = Inst_bool_setup_UI(kind=7,valueUI=value2)
#    ib.show()
    
    mw = Main_window()
    mw.show()
    
    sys.exit(qApp.exec_())