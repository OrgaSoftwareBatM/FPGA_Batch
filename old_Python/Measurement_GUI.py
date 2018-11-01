#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 10:54:36 2016

@author: shintaro
"""

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import h5py
import time
import GUI.Configuration_GUI as config
import GUI.Experiment_GUI as exp
pathSep = QtCore.QDir.separator()

class mainGUI(QtWidgets.QMainWindow):
    def __init__(self,
                 parent=None,
                 ):
        super(mainGUI, self).__init__()
        self.tab = QtWidgets.QTabWidget()
        self.configGUI = config.config_main(parent=self)
        self.expGUI = exp.Main_window(parent=self)
        self.expGUI.console.ipyConsole.executeCommand('from MeasurementBase.measurement_classes import *')
        self.expGUI.console.ipyConsole.executeCommand('import h5py')
        self.expGUI.console.ipyConsole.executeCommand('import numpy as np')
        self.expGUI.console.ipyConsole.pushVariables({'dt':h5py.special_dtype(vlen=bytes)})
        self.tab.addTab(self.configGUI,'Config')
        self.tab.addTab(self.expGUI,'Experiment')
        
        self.setConfigBtn = QtWidgets.QPushButton('Set')
        self.setConfigBtn.clicked.connect(self.setConfig)
        self.setConfigBtn.setFixedSize(100,25)
        self.configGUI.load_ly.addWidget(self.setConfigBtn)
        
        self.setCentralWidget(self.tab)
        
    def setConfig(self):
        self.configGUI.create()
        self.expGUI.configFile.setText(self.configGUI.config.fpath.replace(pathSep,'/'))
        self.expGUI.config = self.configGUI.config
        self.expGUI.instInfos = self.expGUI.getInstLists()
        self.expGUI.updateUIs()
        
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = mainGUI()
    main.show()
    sys.exit(app.exec_())