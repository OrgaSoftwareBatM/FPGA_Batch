# -*- coding: utf-8 -*-

import AWG.drivers.SHARED_variables as sv

## Error definitions
class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    pass

class UnrecognizedPropertyError(Error):
    """
    Error raised when the method calls a non defined property
    """
    def __init__(self, property_name):
        self.property_name = property_name

    def __str__(self):
        return "The property {} is not recognized".format(self.property_name)


class RunType:
    """
    RunType
    """

    def __init__(self, **kwargs):

        # Initialize the dictionary value
        self.values = {}

        # Authorize Labview libraries flag
        # run on a the experiment computer
        self.values["with_Labview_Libraries"] = sv.WITH_LABVIEW_LIBRAIRIES
        if "with_Labview_Libraries" in kwargs.keys():
            self.values["with_Labview_Libraries"] = kwargs["with_Labview_Libraries"]

        self.values["with_Remote_connection"] = True
        if "with_Remote_connection" in kwargs.keys():
            self.values["with_Remote_connection"] = kwargs["with_Remote_connection"]

        # Select RampMode
        self.values["isFastRampMode"] = False
        if "isFastRampMode" in kwargs.keys():
            self.values["isFastRampMode"] = kwargs["isFastRampMode"]


        # Select RealTimeMode
        self.values["isRealTimeMode"] = False
        if "isRealTimeMode" in kwargs.keys():
            self.values["isRealTimeMode"] = kwargs["isRealTimeMode"]

        # Is the sequence Master, or slave
        self.values["isMasterSequence"] = True
        if "isMasterSequence" in kwargs.keys():
            self.values["isMasterSequence"] = kwargs["isMasterSequence"]

        # Define returnToInit
        self.values["returnToInit"] = True
        if "returnToInit" in kwargs.keys():
            self.values["returnToInit"] = kwargs["returnToInit"]
        else:
            self.values["returnToInit"] = True


        ## AWG related

        # Terminal print of the messages
        self.values["awg_tprint_enabled"] = False
        if "awg_tprint_enabled" in kwargs.keys():
            self.values["awg_tprint_enabled"] = kwargs["awg_tprint_enabled"]

        # awg_tcpip_enabled
        self.values["awg_tcpip_enabled"] = sv.AWG_TCPIP_ENABLED
        if "awg_tcpip_enabled" in kwargs.keys():
            self.values["awg_tcpip_enabled"] = kwargs["awg_tcpip_enabled"]

        # awg_opc_check_enabled
        self.values["awg_opc_conf_enabled"] = False
        if "awg_opc_conf_enabled" in kwargs.keys():
            self.values["awg_opc_conf_enabled"] = kwargs["awg_opc_conf_enabled"]

        self.values["awg_opc_wf_enabled"] = True
        if "awg_opc_wf_enabled" in kwargs.keys():
            self.values["awg_opc_wf_enabled"] = kwargs["awg_opc_wf_enabled"]

        self.values["awg_import_ini_only"] = False
        if "awg_import_ini_only" in kwargs.keys():
            self.values["awg_import_ini_only"] = kwargs["awg_import_ini_only"]

        self.values["awg_use_reduced_wfs"] = True
        if "awg_use_reduced_wfs" in kwargs.keys():
            self.values["awg_use_reduced_wfs"] = kwargs["awg_use_reduced_wfs"]


        self.values["awg_non_authorized_ip"] = []
        if "awg_non_authorized_ip" in kwargs.keys():
            self.values["awg_non_authorized_ip"] = kwargs["awg_non_authorized_ip"]


    def isproperty(self, prop):
        """
        Return True (False) if the asked property exists (doesnt)
        """
        if prop in self.values.keys():
            return True
        else:
            return False

    def get(self, prop):
        if prop in self.values.keys():
            return self.values[prop]
        else:
            raise UnrecognizedPropertyError(prop)

    def set(self, prop, val):
        if self.isproperty(prop):
            self.values[prop] = val
        else:
            raise ValueError("Unknown property "+ prop)

__all__ = ["RunType"]
