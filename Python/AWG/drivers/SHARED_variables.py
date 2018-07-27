# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#
#   File containing HARD-CODED variables shared for the WHOLE soft.
#   (Some should go on fridge_settings.ini)
#
# -----------------------------------------------------------------------------
import h5py, os, platform
import numpy as np

PATH_SrvInstruments_folder = "..\\AWG\\drivers\\"

PATH_AWGs_folder = PATH_SrvInstruments_folder
Tektronix5014_defaultconfigfile = "Tektronix5014_default.ini"
AWGs_configfile = "Baptiste_AWG.ini"
AWGs_h5status_file = "Baptiste_AWG_status.h5"
PATH_AWGs_configfile = PATH_AWGs_folder + AWGs_configfile

PATH_LOGS = "..\\_logs\\"
NAME_LOGS = "Main"

WITH_LABVIEW_LIBRAIRIES = False
AWG_TCPIP_ENABLED = True

if __name__=='__main__':
    pass
