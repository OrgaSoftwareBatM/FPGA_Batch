from configparser import ConfigParser
import sys, os
sys.path.insert(0,'..') # import parent directory

import Utility.SHARED_variables as sv 



def get_InstrumentDict() :
    """
    Get the "Instruments" section dictionnary from the "fridge_settings.ini" file.

    INPUT :
        - None 

    OUTPUT :
        - [dict] addressList : contains all instruments and their address (IP/GPIB)
    """

    config = ConfigParser()
    config.read(sv.fridge_settings_path)
    addressList = {}
    for key in list(config['Instruments'].keys()):
        addressList[key] = config.get('Instruments',key)
    
    return addressList



def find_unused_name(folder,prefix):
    findex = 0
    exists = True
    while exists:
    	findex += 1
    	config_path = folder+'\\'+prefix+'config_'+str(findex)+'.h5'
    	exp_path = folder+'\\'+prefix+ 'exp_'+str(findex)+'.h5'
    	exists = os.path.isfile(config_path) or os.path.isfile(exp_path)
    return findex,config_path,exp_path