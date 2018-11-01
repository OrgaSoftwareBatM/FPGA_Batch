#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 09:51:49 2016

@author: shintaro
"""

import GUI.DataPlotter as dp
import sys, os
from PyQt5 import QtWidgets

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    pw = dp.plotWindow()
    pw.show()
    sys.exit(app.exec_())
    