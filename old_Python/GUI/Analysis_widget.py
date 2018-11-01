# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:46:20 2016

@author: shintaro
"""

#import time
#import natsort
import sys
#import os
import numpy as np
#import matplotlib.pyplot as plt

sys.path.insert(0,'..')
import AnalysisBase.AnalysisFunctions as analysis

from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

""" Utility GUI """
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
""" ------------------ """

pathSeparator = QtCore.QDir.separator()

""" To add new function you have to create another function in the file 'AnalyaisBase/AnalysisFunctions.py
    and update 'methodList', 'functionDict', 'paramList' in the following """
# method list and param list has to have same order about methods.    
methodList = ['raw','Box smooth','subtract smoothed background', 'ConvV2G', 'derivative',
              'Average','Variance','send map','pulse analysis']
# dictionary of the name of the function in AnalysisFunctions.py for each method
functionDict={methodList[0]:'raw',methodList[1]:'movingAverage',methodList[2]:'subtractSmoothedBackground',
              methodList[3]:'convertV2G', methodList[4]:'derivative',methodList[5]:'averagingData',
              methodList[6]:'varianceData',methodList[7]:'sendingMap',methodList[8]:'pulseAnalysis'}
# name of the parameter and default value of arguments in each function
paramList = {methodList[0]:[]}
paramList[methodList[1]] = ['box size',10,'axis',0] # [argument0 name, value0, argument1 name, value1, ...]
paramList[methodList[2]] = ['box size',10,'axis',0]
paramList[methodList[3]] = ['axis',0,'bias',3e-6,'unit',1e-6,'R_contact',0.0,'R_measure',1e4]
paramList[methodList[4]] = ['box size',5,'axis',0]
paramList[methodList[5]] = ['axis',0,'initial',0,'final',0]
paramList[methodList[6]] = ['axis',0,'initial',0,'final',0]
paramList[methodList[7]] = ['Initial before',10,'Final before',13,'Initial after',30,'Final after',33]
paramList[methodList[8]] = ['skip',50,'normalize',True,'correct jump',True]

class AnalysisPanelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AnalysisPanelWidget, self).__init__()
        self.method_list = methodList
        self.funcList = functionDict
        self.paramList = paramList
        self.method_selection = QtWidgets.QComboBox()
        self.method_selection.addItems(self.method_list)
        self.method_selection.currentIndexChanged.connect(self.updateWidgets)
        self.grid_analysis = QtWidgets.QGridLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.method_selection)
        self.vbox.addLayout(self.grid_analysis)
        self.setLayout(self.vbox)
        
    def updateWidgets(self, index):
        for i in reversed(range(self.grid_analysis.count())): 
                self.grid_analysis.itemAt(i).widget().deleteLater()
        method = self.method_list[index]
        params = self.paramList[method]
        for i in range(len(params)//2):
            label = QtWidgets.QLabel(params[2*i])
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.grid_analysis.addWidget(label,i,0,1,1)
            v = params[2*i+1]
            if type(v) == int:
                item = QtWidgets.QSpinBox()
                item.setRange(0,1000000)
                item.setValue(v)
            elif type(v) == float:
                item = QFloatLineEdit()
                item.set_value(v)
            elif type(v) == str:
                # suppose it is list of string (separated by either ',' or ';')
                v = v.replace(';',',').split(',')
                item = QtWidgets.QComboBox()
                item.addItems(v)
            elif type(v) == bool:
                item = QtWidgets.QCheckBox()
                if v == False:
                    item.setCheckState(0)
                else:
                    item.setCheckState(2)
            self.grid_analysis.addWidget(item,i,1,1,1)
          
    def executeAnalysis(self, expdata):
        index = self.method_selection.currentIndex()
        method = self.method_list[index]
        params = self.paramList[method]
        function = self.funcList[method]
        # collect arguments from widgets
        args=[]
        for i in range(len(params)//2):
            v = params[2*i+1]
            if type(v) == int:
               args.append(self.grid_analysis.itemAtPosition(i,1).widget().value()) 
            elif type(v) == float:
                args.append(self.grid_analysis.itemAtPosition(i,1).widget().get_value())
            elif type(v) == str:
                # suppose it is list of string (separated by either ',' or ';')
                args.append(self.grid_analysis.itemAtPosition(i,1).widget().currentText())
            elif type(v) == bool:
                if self.grid_analysis.itemAtPosition(i,1).widget().checkState()==0:
                    args.append(False)
                else:
                    args.append(True)
        # create command from function name and arguments
        if len(args)>0:
            cmd = 'analysis.'+function+'(expdata,'+','.join(str(s) for s in args)+')'
        else:
            cmd = 'analysis.'+function+'(expdata)'
        adata = eval(cmd)
        return adata
            
def main():
    app = QtWidgets.QApplication(sys.argv)
#    aw = AnalysisWidget()
#    aw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()