# -*- coding: utf-8 -*-
"""
Created on Wed May 18 07:34:45 2016

@author: shintaro
"""
# Set the QT API to PyQt4
import os
os.environ['QT_API'] = 'pyqt'
import sys
sys.path.insert(0,'..')
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from PyQt5 import QtWidgets
# Import the console machinery from ipython
#from qtconsole.rich_ipython_widget import RichIPythonWidget
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from IPython.lib import guisupport


class QIPythonWidget(RichJupyterWidget):
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,customBanner=None,*args,**kwargs):
        if customBanner!=None: self.banner=customBanner
        super(QIPythonWidget, self).__init__(*args,**kwargs)
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt4'
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            guisupport.get_app_qt4().exit()            
        self.exit_requested.connect(stop)

    def pushVariables(self,variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        self.kernel_manager.kernel.shell.push(variableDict)
    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()    
    def printText(self,text):
        """ Prints some plain text to the console """
        self._append_plain_text(text)        
    def executeCommand(self,command):
        """ Execute a command in the frame of the console widget """
        self._execute(command,False)


class ExampleWidget(QtWidgets.QWidget):
    """ Main GUI Widget including a button and IPython Console widget inside vertical layout """
    def __init__(self, parent=None):
        super(ExampleWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.button = QPushButton('Another widget')
        ipyConsole = QIPythonWidget(customBanner="Welcome to the embedded ipython console\n")
        layout.addWidget(self.button)
        layout.addWidget(ipyConsole)        
        # This allows the variable foo and method print_process_id to be accessed from the ipython console
        ipyConsole.pushVariables({"foo":43,"print_process_id":print_process_id})
        ipyConsole.printText("The variable 'foo' and the method 'print_process_id()' are available. Use the 'whos' command for information.")                           

def print_process_id():
    print('Process ID is:', os.getpid())

class IpyConsoleWidget(QtWidgets.QWidget):
    """ Main GUI Widget including a button and IPython Console widget inside vertical layout """
    def __init__(self, parent=None):
        super(IpyConsoleWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.ipyConsole = QIPythonWidget(customBanner="Welcome to the embedded ipython console\n")
        layout.addWidget(self.ipyConsole)
        # This allows the variable foo and method print_process_id to be accessed from the ipython console
        self.ipyConsole.executeCommand('import numpy as np')
        self.ipyConsole.executeCommand('from measurement_classes import *')
        if parent != None:
            self.ipyConsole.pushVariables({'main':parent})
        
class AnalysisWidget(QtWidgets.QWidget):
    """ Main GUI Widget including a button and IPython Console widget inside vertical layout """
    def __init__(self, parent=None):
        super(AnalysisWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.ipyConsole = QIPythonWidget(customBanner="Welcome to the embedded ipython console\n")
        layout.addWidget(self.ipyConsole)
        # This allows the variable foo and method print_process_id to be accessed from the ipython console
        self.ipyConsole.executeCommand('from AnalysisBase.AnalysisFunctions import *')
        self.ipyConsole.executeCommand('from DataStructure.datacontainer import *')
        self.ipyConsole.executeCommand('import numpy as np')
#        self.ipyConsole.pushVariables({"box":100,"axis":0})

    def setExpdatas(self, h5path, dataNames):
        for i, dataName in enumerate(dataNames):
            data = ExpData()
            data.readHDF5data2python(h5name=h5path[:-3], grpname=dataName, folderPath='')
            self.ipyConsole.pushVariables({"data"+str(i):data})

    def setH5path(self,h5path):
        self.ipyConsole.pushVariables({"h5path":h5path})

    def setH5name(self,h5name):
        self.ipyConsole.pushVariables({"h5name":h5name})


def main():
    app  = QtWidgets.QApplication([])
    widget = IpyConsoleWidget()
    widget.show()
    app.exec_()    

if __name__ == '__main__':
    main()