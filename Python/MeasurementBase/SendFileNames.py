import win32com.client  # Python ActiveX Client
import time

vipath = """C:\\Partage\\FPGA_Batch\\Labview\\Batch_main Folder\\FileLauncher.vi"""
# Import parameters
# config_file = ConfigObj('..\\Fridge_settings.ini')
# vipath = config_file['Paths']['file_launcher']

def sendFiles(vipath=vipath,
              fileList = []):
    ini = time.time()
    LabVIEW = win32com.client.Dispatch("Labview.Application")
    VI = LabVIEW.getvireference(vipath)  # Path to LabVIEW VI
    VI._FlagAsMethod("Call")  # Flag "Call" as Method
    VI.setcontrolvalue('Files_temp', fileList)
#    print(time.time()-ini)