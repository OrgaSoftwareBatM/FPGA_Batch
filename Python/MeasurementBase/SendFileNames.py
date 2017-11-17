import win32com.client  # Python ActiveX Client
import time
##Melusine measurement PC
#vipath = 'C:\\Documents and Settings\\Bauerle\\Mes documents\\takada\\Labview\\FPGA_Batch_1_4\\Batch_main Folder\\FileLauncher.vi'
##Melusine analysis PC
#vipath = 'E:\\Takada\\Program\\Labview\\FPGA_Batch_1_4\\Batch_main Folder\\FileLauncher.vi'
#Wodan

# vipath = """C:\\Users\\manip.batm\\Desktop\\FPGA_Batch_1_7_3\\Batch_main Folder\\FileLauncher.vi"""
vipath = """C:\\Users\\manip.batm\\Desktop\\FPGA_Batch_1_7_3\\FPGA_Batch_1_5_EVERTON\Batch_main Folder\\Filelauncher.vi"""
# vipath = """C:\\Users\\manip.batm\\Desktop\\FPGA_Batch_1_7_3\\fpga_batch_1_7.lvproj"""
#vipath = 'C:\\LabviewProgs\\FPGA_Batch_1_7_3_1\\Batch_main Folder'

def sendFiles(vipath=vipath,
              fileList = []):
    ini = time.time()
    LabVIEW = win32com.client.Dispatch("Labview.Application")
    VI = LabVIEW.getvireference(vipath)  # Path to LabVIEW VI
    VI._FlagAsMethod("Call")  # Flag "Call" as Method
    VI.setcontrolvalue('Files_temp', fileList)
    print(time.time()-ini)