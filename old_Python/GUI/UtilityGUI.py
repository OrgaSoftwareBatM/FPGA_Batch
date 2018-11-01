# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 18:28:07 2017

@author: Bauerle
"""
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class BasePEWidget(object):
    def get_value(self):
        pass
    def set_value(self):
        pass
        
class QFloatLineEdit(QtWidgets.QLineEdit, BasePEWidget):
    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        validator = QtGui.QDoubleValidator(self)
        validator.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setValidator(validator)
    def get_value(self):
        return float(str(self.text()))
    def set_value(self, str_value):
        self.setText(str(str_value))
        
        
class oneDgui(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 label = 'test',
                 size = 3,
                 widget=QFloatLineEdit,
                 height = 25,
                 width = 100,
                 vertical = False,
                 showSizeControl = True,
                 extraSize = 40,    # used in case it is stand alone GUI (no parent)
                 ):
        super(oneDgui, self).__init__()
        self.label = label
        self.size = size
        self.parent = parent
        self.widget = widget
        self.h = height
        self.w = width
        self.vertical = vertical
        self.showSizeControl = showSizeControl
        self.extraSize = extraSize
        
        self.counter = QtWidgets.QSpinBox()
        self.counter.setRange(1, 10000)
        self.counter.setValue(self.size)
        self.counter.setFixedSize(40, self.h)
        self.counter.valueChanged.connect(self.update)
        
        self.grid = QtWidgets.QGridLayout()
        
        # create a label if given
        infoLine = 0
        if not self.label == '':
            infoLine = 1
            self.grid.addWidget(QtWidgets.QLabel(label),0,0,1,1)
        # create a counter to show the size of the GUI
        if self.showSizeControl:
            if infoLine == 1:
                if self.vertical:
                    self.grid.addWidget(self.counter,infoLine,0,1,1)
                else:
                    self.grid.addWidget(self.counter,0,infoLine,1,1)
            else:
                self.grid.addWidget(self.counter,0,0,1,1)
                infoLine = 1
        
        for i in range(self.counter.value()):
            w = self.widget()
            w.setFixedSize(self.w, self.h)
            if self.vertical:
                self.grid.addWidget(w,i,infoLine,1,1)
            else:
                self.grid.addWidget(w,infoLine,i,1,1)
        
        self.setLayout(self.grid)
        
        if not self.parent == None:
            extra = 0
        else:
            extra = self.extraSize
            
        if self.showSizeControl:
            counter_width = 40
        else:
            counter_width = 0
            
        if self.vertical:
            w = extra+self.w+max(len(self.label)*7, counter_width)*infoLine
            h = extra+self.counter.value()*self.h
        else:
            w = extra+max(self.counter.value()*self.w, (counter_width+len(self.label))*infoLine)
            h = extra+self.h*(1+infoLine)
        self.setFixedSize(w, h)
        
    def update(self):
        newsize = self.counter.value()
        if (self.label != '') or (self.showSizeControl):
            infoLine = 1
        else:
            infoLine = 0
            
        for i in range(newsize):
            if self.vertical:
                item = self.grid.itemAtPosition(i, infoLine)
            else:
                item = self.grid.itemAtPosition(infoLine, i)
            if item == None:
                w = self.widget()
                w.setFixedSize(self.w, self.h)
            else:
                if item.widget() == None:
                    w = self.widget()
                    w.setFixedSize(self.w, self.h)
                else:
                    w = item.widget()
            if self.vertical:
                self.grid.addWidget(w,i,infoLine,1,1)
            else:
                self.grid.addWidget(w,infoLine,i,1,1)
                    
         #delete extra widgets
        if self.size > newsize:
            for i in reversed(range(self.size - newsize)):
                if self.vertical:
                    item = self.grid.itemAtPosition(i+newsize, infoLine)
                else:
                    item = self.grid.itemAtPosition(infoLine, i+newsize)
                if not item == None:
                    w = item.widget()
                    if not w == None:
                        w.deleteLater()
        self.size = newsize
        
        # set widget size
        if not self.parent == None:
            extra = 0
        else:
            extra = self.extraSize
            
        if self.showSizeControl:
            counter_width = 40
        else:
            counter_width = 0
            
        if self.vertical:
            w = extra+self.w+max(len(self.label)*7, counter_width)*infoLine
            h = extra+self.counter.value()*self.h
        else:
            w = extra+max(self.counter.value()*self.w, (counter_width+len(self.label))*infoLine)
            h = extra+self.h*(1+infoLine)
        self.setFixedSize(w, h)
        
class twoDgui(QtWidgets.QWidget):
    def __init__(self,
                 parent=None,
                 label = 'test',
                 initial_size = [3,3],
                 widget=QFloatLineEdit,
                 hight = 25,
                 width = 100,
                 showSizeControl = True,
                 extraSize = 40,
                 ):
        super(twoDgui, self).__init__()
        self.parent = parent
        self.label = label
        self.w = widget
        self.r = initial_size[0]
        self.c = initial_size[1]
        self.hi = hight
        self.wi = width
        self.showSizeControl = showSizeControl
        self.extraSize = extraSize
        
        self.rcounter = QtWidgets.QSpinBox()
        self.rcounter.setRange(1, 10000)
        self.rcounter.setValue(self.r)
        self.rcounter.setFixedSize(40, 30)
        self.rcounter.valueChanged.connect(self.update)
        self.ccounter = QtWidgets.QSpinBox()
        self.ccounter.setRange(1, 10000)
        self.ccounter.setValue(self.c)
        self.ccounter.setFixedSize(40, 30)
        self.ccounter.valueChanged.connect(self.update)
        
        self.grid = QtWidgets.QGridLayout()
        
        self.additionalWidth = 0
        if (self.label != ''):
            self.grid.addWidget(QtWidgets.QLabel(self.label),0,0,1,1)
            self.additionalWidth = 1
            
        if self.showSizeControl:
            self.grid.addWidget(self.rcounter,0,self.additionalWidth,1,1)
            self.grid.addWidget(self.ccounter,0,self.additionalWidth+1,1,1)
            self.additionalWidth = 1
        
        for i in range(self.r):
            for j in range(self.c):
                w = self.w()
                w.setFixedSize(self.wi, self.hi)
                self.grid.addWidget(w,self.additionalWidth+i,j,1,1)
                
        # set layout
        self.setLayout(self.grid)
        
        # set widget size
        if not self.parent == None:
            extra = 0
        else:
            extra = self.extraSize
        
        if self.showSizeControl:
            counter_width = 40
        else:
            counter_width = 0
            
        w = (counter_width*2+len(self.label)*5)*self.additionalWidth+self.wi*self.c+extra
        h = 30*self.additionalWidth+self.r*self.hi+extra
        self.setFixedSize(w, h)
        
    def update(self):
        row = self.rcounter.value()
        col = self.ccounter.value()
        for i in range(row):
            for j in range(col):
                item = self.grid.itemAtPosition(i+self.additionalWidth,j)
                if item == None:
                    w = self.w()
                    w.setFixedSize(self.wi, self.hi)
                else:
                    if item.widget() == None:
                        w = self.w()
                        w.setFixedSize(self.wi, self.hi)
                    else:
                        w = item.widget()
                self.grid.addWidget(w,i+self.additionalWidth,j,1,1)
                    
         #delete extra widgets
        if self.r > row:
            csize = self.grid.columnCount()
            for i in reversed(range(self.r-row)):
                for j in reversed(range(csize)):
                    item = self.grid.itemAtPosition(row+i+self.additionalWidth, j)
                    if not item == None:
                        w = item.widget()
                        if not w == None:
                            w.deleteLater()
        if self.c > col:
            rsize = self.grid.rowCount()-self.additionalWidth
            for i in reversed(range(rsize)):
                for j in reversed(range(self.c - col)):
                    item = self.grid.itemAtPosition(i+self.additionalWidth, col+j)
                    if not item == None:
                        w = item.widget()
                        if not w == None:
                            w.deleteLater()
        self.r = row
        self.c = col
        # set widget size
        if not self.parent == None:
            extra = 0
        else:
            extra = self.extraSize
        
        if self.showSizeControl:
            counter_width = 40
        else:
            counter_width = 0
            
        w = (counter_width*2+len(self.label)*5)*self.additionalWidth+self.wi*self.c+extra
        h = 30*self.additionalWidth+self.r*self.hi+extra
        self.setFixedSize(w, h)
            
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)

    td = twoDgui()
    td.show()
#    od = oneDgui()
#    od.show()
    sys.exit(app.exec_())