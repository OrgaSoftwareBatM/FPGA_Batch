# -*- coding: utf-8 -*-


from _logs.logs import LOG_Manager
import logging
log = LOG_Manager()
# log.start(level_console=logging.DEBUG)
# log.start(level_console=logging.CRITICAL)
log.start(level_console=logging.INFO)

import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)
import numpy as np
import time
from configobj import ConfigObj
from AWG.drivers.DRIVER_AWG5014 import DRIVER_AWG5014

config_file = '..\\AWG\\drivers\\Baptiste_AWG.ini'

def AWG_fast_send(waveforms,channel_names,wait_elements):
    if not os.path.isfile(config_file):
        log.send(level="critical",
                    context="AWG_fast_send",
                    message="AWG configuration file {} not found".format(config_file))
        return 0
    ini_file = ConfigObj(config_file)

    if check_wfm(waveforms,channel_names,ini_file):
        t0 = time.time()
        awg = DRIVER_AWG5014(settings=ini_file['0'])
        awg.load_instructions(waveforms, channel_names)
        awg.SendToInstrument(wait_elements)
        awg.OutputRunON()
#        awg._wait_OPC()
        log.send(level="debug",
                    context="AWG_fast_send",
                    message="done in {} s.".format(time.time()-t0))
        return 1
    else:
        return 0

def check_wfm(waveforms,channel_names,ini_file):
    names = [ini_file['0']['channel_settings'][i]['logical_name'] for i in ['1','2','3','4']]
    lower_limits = [float(ini_file['0']['channel_settings'][i]['lower_limit']) for i in ['1','2','3','4']]
    upper_limits = [float(ini_file['0']['channel_settings'][i]['upper_limit']) for i in ['1','2','3','4']]
    
    if np.shape(waveforms)[0] != 4 or len(channel_names) !=4:
        log.send(level="critical",
                    context="AWG_fast_send.check_wfm",
                    message="Incorrect number of channels supplied")
        return 0
    for i in range(4):
        if channel_names[i] not in names:
            log.send(level="critical",
                        context="AWG_fast_send.check_wfm",
                        message="Unknown channel name : {}".format(channel_names[i]))
            return 0
        ind = names.index(channel_names[i])
        ll = lower_limits[ind]
        ul = upper_limits[ind]

        if np.any(waveforms[i,:]>ul) or np.any(waveforms[i,:]<ll):
            log.send(level="critical",
                        context="AWG_fast_send.check_wfm",
                        message="Channel {} is out of voltage limits".format(channel_names[i]))
            return 0

    log.send(level="debug",
                context="AWG_fast_send.check_wfm",
                message="done.")
    return 1