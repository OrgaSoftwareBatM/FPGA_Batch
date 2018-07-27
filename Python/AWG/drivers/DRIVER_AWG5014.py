# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# LIBRARY import
# -----------------------------------------------------------------------------
from time import localtime
from io import BytesIO
import re
import math
import struct
import itertools
from configobj import ConfigObj
import numpy as np

import AWG.drivers.SHARED_variables as sv
from AWG.drivers.RunType import RunType

from AWG.drivers.SocketCom import SocketCom
from AWG.drivers.AWG_Channel import Channel

from _logs.logs import LOG_Manager
log = LOG_Manager()

class ADDRESSES_AWG5014(dict):

    def __init__(self):
        # super(ADDRESSES_AWG5014, self).__init__(**kwargs)
        self.__dict__["general_settings"] = {
                "SAMPLING_RATE": self._SAMPLING_RATE,
                "CLOCK_SOURCE": self._CLOCK_SOURCE,
                "REFERENCE_SOURCE": self._REFERENCE_SOURCE,
                "EXTERNAL_REFERENCE_TYPE": self._EXTERNAL_REFERENCE_TYPE,
                "REFERENCE_CLOCK_FREQUENCY_SELECTION": self._REFERENCE_CLOCK_FREQUENCY_SELECTION,
                "REFERENCE_MULTIPLIER_RATE": self._REFERENCE_MULTIPLIER_RATE,
                "TRIGGER_SOURCE": self._TRIGGER_SOURCE,
                "TRIGGER_INPUT_IMPEDANCE": self._TRIGGER_INPUT_IMPEDANCE,
                "TRIGGER_INPUT_SLOPE": self._TRIGGER_INPUT_SLOPE,
                "TRIGGER_INPUT_POLARITY": self._TRIGGER_INPUT_POLARITY,
                "TRIGGER_INPUT_THRESHOLD": self._TRIGGER_INPUT_THRESHOLD,
                "EVENT_INPUT_IMPEDANCE": self._EVENT_INPUT_IMPEDANCE,
                "EVENT_INPUT_POLARITY": self._EVENT_INPUT_POLARITY,
                "EVENT_INPUT_THRESHOLD": self._EVENT_INPUT_THRESHOLD,
                "JUMP_TIMING": self._JUMP_TIMING,
                "RUN_MODE": self._RUN_MODE}
        self.__dict__["channel_settings"] = {
                "marker_settings":{
                    "DELAY":self._MARKER_DELAY,
                    "HIGH":self._MARKER_VOLTAGE_HIGH,
                    "LOW":self._MARKER_VOLTAGE_LOW},
                "OUTPUT":self._OUTPUT,
                "ANALOG_FILTER":self._ANALOG_FILTER,
                "DIRECT_OUTPUT":self._DIRECT_OUTPUT,
                "ADD_INPUT":self._ADD_INPUT,
                "DC_OUTPUT_LEVEL":self._DC_OUTPUT_LEVEL,
                "DELAY":self._DELAY,
                "AMPLITUDE":self._AMPLITUDE,
                "OFFSET":self._OFFSET,
                "PHASE":self._PHASE,
                "SKEW":self._SKEW}


    # -------------------------- Dictionary --------------------------
    def __getitem__(self, key):
        return self.addresses[key]

    def keys(self):
        return self.addresses.keys()

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))



    # -------------------------- General settings --------------------------
    @staticmethod
    def _RUN_MODE(mode, *args):
        if mode == "set":
            return "AWGControl:RMODe {}".format(args[0])
        elif mode == "query":
            return "AWGControl:RMODe?"

    # @staticmethod
    # def _TRIGGER_SEQUENCE_MODE(mode, *args):
    #     if mode == "set":
    #         return "TRIGger:SEQuence:MODE {}".format(args[0])
    #     elif mode == "query":
    #         return "TRIGger:SEQuence:MODE?"

    # ----- TRIGGER
    @staticmethod
    def _TRIGGER_SOURCE(mode, *args):
        if mode == "set":
            return "TRIGger:SEQuence:SOURCe {}".format(args[0])
        elif mode == "query":
            return "TRIGger:SEQuence:SOURCe?"

    @staticmethod
    def _TRIGGER_INPUT_THRESHOLD(mode, *args):
        if mode == "set":
            return "TRIGger:SEQuence:LEVel {}".format(args[0])
        elif mode == "query":
            return "TRIGger:SEQuence:LEVel?"

    @staticmethod
    def _TRIGGER_INPUT_SLOPE(mode, *args):
        if mode == "set":
            return "TRIGger:SEQuence:SLOPe {}".format(args[0])
        elif mode == "query":
            return "TRIGger:SEQuence:SLOPe?"

    @staticmethod
    def _TRIGGER_INPUT_IMPEDANCE(mode, *args):
        if mode == "set":
            return "TRIGger:SEQuence:IMPedance {}".format(args[0])
        elif mode == "query":
            return "TRIGger:SEQuence:IMPedance?"

    @staticmethod
    def _TRIGGER_INPUT_POLARITY(mode, *args):
        if mode == "set":
            return "TRIGger:SEQuence:POLarity {}".format(args[0])
        elif mode == "query":
            return "TRIGger:SEQuence:POLarity?"

    # ----- EVENT
    @staticmethod
    def _EVENT_INPUT_THRESHOLD(mode, *args):
        if mode == "set":
            return "EVENt:LEVel {}".format(args[0])
        elif mode == "query":
            return "EVENt:LEVel?"

    @staticmethod
    def _EVENT_INPUT_POLARITY(mode, *args):
        if mode == "set":
            return "EVENt:POLarity {}".format(args[0])
        elif mode == "query":
            return "EVENt:POLarity?"

    @staticmethod
    def _JUMP_TIMING(mode, *args):
        if mode == "set":
            return "EVENt:JTIMing {}".format(args[0])
        elif mode == "query":
            return "EVENt:JTIMing?"

    @staticmethod
    def _EVENT_INPUT_IMPEDANCE(mode, *args):
        if mode == "set":
            return "EVENt:IMPedance {}".format(args[0])
        elif mode == "query":
            return "EVENt:IMPedance?"

    # ----- TIMING
    @staticmethod
    def _CLOCK_SOURCE(mode, *args):
        if mode == "set":
            return "AWGControl:CLOCk:SOURCe {}".format(args[0])
        elif mode == "query":
            return "AWGControl:CLOCk:SOURCe?"

    @staticmethod
    def _REFERENCE_SOURCE(mode, *args):
        if mode == "set":
            return "ROSCillator:SOURCe {}".format(args[0])
        elif mode == "query":
            return "ROSCillator:SOURCe?"

    @staticmethod
    def _EXTERNAL_REFERENCE_TYPE(mode, *args):
        if mode == "set":
            return "ROSCillator:TYPE {}".format(args[0])
        elif mode == "query":
            return "ROSCillator:TYPE?"

    @staticmethod
    def _REFERENCE_MULTIPLIER_RATE(mode, *args):
        if mode == "set":
            return "ROSCillator:MULTiplier {}".format(args[0])
        elif mode == "query":
            return "ROSCillator:MULTiplier?"

    @staticmethod
    def _REFERENCE_CLOCK_FREQUENCY_SELECTION(mode, *args):
        if mode == "set":
            return "ROSCillator:FREQuency {}".format(args[0])
        elif mode == "query":
            return "SOURce1:FREQuency?"

    @staticmethod
    def _CLOCK_SOURCE(mode, *args):
        if mode == "set":
            return "ROSCillator:FREQuency {}".format(args[0])
        elif mode == "query":
            return "ROSCillator:FREQuency?"

    @staticmethod
    def _SAMPLING_RATE(mode, *args):
        if mode == "set":
            return "SOURce1:FREQuency {}".format(args[0])
        elif mode == "query":
            return "SOURce1:FREQuency?"

    # -------------------------- Channel settings --------------------------

    @staticmethod
    def _OUTPUT(mode, *args):
        if mode == "set":
            return "OUTPut{}:STATe {}".format(args[0], args[1])
        elif mode == "query":
            return "OUTPut{}:STATe?".format(args[0])

    @staticmethod
    def _ANALOG_FILTER(mode, *args):
        if mode == "set":
            return "OUTPut{}:FILTer:LPASs:FREQuency {}".format(
                                                            args[0], args[1])
        elif mode == "query":
            return "OUTPut{}:FILTer:LPASs:FREQuency?".format(args[0])

    @staticmethod
    def _DIRECT_OUTPUT(mode, *args):
        if mode == "set":
            return "AWGControl:DOUTput{}:STATe {}".format(args[0], args[1])
        elif mode == "query":
            return "AWGControl:DOUTput{}:STATe?".format(args[0])

    @staticmethod
    def _ADD_INPUT(mode, *args):
        if mode == "set":
            if args[1]:
                return 'SOURce{}:COMBine:FEED "ESIGnal"'.format(args[0])
            else:
                return 'SOURce{}:COMBine:FEED ""'.format(args[0])
        elif mode == "query":
            return "SOURce{}:COMBine:FEED?".format(args[0])

    @staticmethod
    def _DC_OUTPUT_LEVEL(mode, *args):
        if mode == "set":
            return "AWGControl:DC{}:VOLTage:OFFSet {}".format(args[0], args[1])
        elif mode == "query":
            return "AWGControl:DC{}:VOLTage:OFFSet?".format(args[0])

    @staticmethod
    def _DELAY(mode, *args):
        if mode == "set":
            return "SOURce{}:DELAY:ADJUST {}".format(args[0], args[1])
        elif mode == "query":
            return "SOURce{}:DELAY?".format(args[0])

    @staticmethod
    def _AMPLITUDE(mode, *args):
        if mode == "set":
            return "SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}".format(
                                                            args[0], args[1])
        elif mode == "query":
            return "SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?".format(
                                                            args[0])

    @staticmethod
    def _OFFSET(mode, *args):
        if mode == "set":
            return "SOURce{}:VOLTage:LEVel:IMMediate:OFFSet {}".format(
                                                            args[0], args[1])
        elif mode == "query":
            return "SOURce{}:VOLTage:LEVel:IMMediate:OFFSet?".format(args[0])

    @staticmethod
    def _PHASE(mode, *args):
        if mode == "set":
            return "SOURce{}:PHASE:ADJUST {}".format(args[0], args[1])
        elif mode == "query":
            return "SOURce{}:PHASE:ADJUST?".format(args[0])

    @staticmethod
    def _SKEW(mode, *args):
        if mode == "set":
            return "SOURce{}:SKEW {}".format(args[0], args[1])
        elif mode == "query":
            return "SOURce{}:SKEW?".format(args[0])

    # -------------------------- Marker settings --------------------------

    @staticmethod
    def _MARKER_DELAY(mode, *args):
        if mode == "set":
            return "SOURce{}:MARKer{}:DELay {}".format(
                                                    args[0], args[1], args[2])
        elif mode == "query":
            return "SOURce{}:MARKer{}:DELay?".format(args[0], args[1])

    @staticmethod
    def _MARKER_VOLTAGE_HIGH(mode, *args):
        if mode == "set":
            return "SOURce{}:MARKer{}:VOLTage:HIGH {}".format(
                                                    args[0], args[1], args[2])
        elif mode == "query":
            return "SOURce{}:MARKer{}:VOLTage:HIGH?".format(args[0], args[1])

    @staticmethod
    def _MARKER_VOLTAGE_LOW(mode, *args):
        if mode == "set":
            return "SOURce{}:MARKer{}:VOLTage:LOW {}".format(
                                                    args[0], args[1], args[2])
        elif mode == "query":
            return "SOURce{}:MARKer{}:VOLTage:LOW?".format(args[0], args[1])


class LowLevelCom_AWG5014(SocketCom):

    """
    The AWGCom object is a tcpip Socket which faciliates communication to a
    Tektronix AWG. After creation of the Instance a Connection has to be opened
    with the function openCom() to establish a TCPIp connection which
    afterwards should be closed with the function closeCom. To concatenate
    different commands use the optional parameter stringOnly and pass the
    commands as a list of the created strings to sendMessage(). If this
    parameter is not defined or 0, the command will be passed to the AWG when
    the function is called.
    """

    def __init__(self, **kwargs):

        # - take Ip and Port
        new_kwargs = kwargs
        new_kwargs["Ip"] = self.settings["general_settings"]["ip"]
        new_kwargs["Port"] = self.settings["general_settings"]["port"]
        super(LowLevelCom_AWG5014, self).__init__(**new_kwargs)

        # --- General settings
        # -- Runtype
        if "runtype" in kwargs.keys():
            self.runtype = kwargs["runtype"]
        else:
            self.runtype = RunType()


        # --- Local command addresses
        self.addresses = ADDRESSES_AWG5014()


    def _wait_OPC(self):
        self.send_message('*OPC?', self.runtype)
        self.read_message(self.runtype)

    def sendMessage(self, msg, msg_type="configuration"):
        """
        Convenience function that simply pass some arguments
        """
        self.send_message(msg, self.runtype)

        if msg_type == "configuration":
            # if self.opc_conf_enabled:
            if self.runtype.isproperty("awg_opc_conf_enabled"):
                if self.runtype.get("awg_opc_conf_enabled"):
                    self._wait_OPC()
        if msg_type == "waveform":
            # if self.opc_wf_enabled:
            if self.runtype.isproperty("awg_opc_wf_enabled"):
                if self.runtype.get("awg_opc_wf_enabled"):
                    self._wait_OPC()

    def queryMessage(self, msg):
        """
        Convenience function that simply pass some arguments
        """
        self.send_message(msg, self.runtype)
        return self.read_message(self.runtype)

    # --------------------------------- Public --------------------------------

    def openCom(self):
        """
        Convenience function that simply pass some arguments
        """
        self.open_communication(self.runtype)

    def closeCom(self):
        """
        Convenience function that simply pass some arguments
        """
        self.close_communication(self.runtype)

    def clearSystem(self, wait_opc=False):
        """
        Convenience function that simply pass some arguments
        """
        msg = "*RST"
        self.sendMessage(msg)
        msg = "*CLS"
        self.sendMessage(msg)

        if wait_opc:
            self._wait_OPC()

    def get(self, prop):
        if prop in self.addresses.keys():
            return self.queryMessage(self.addresses[prop]()+"?")
        else:
            raise ValueError(prop + " is unknown.")

    # --------------------------------- Private -------------------------------
    def newWaveform(self, name, size):
        """
        Creates a new Waveform slot without data in it
        """
        msg = 'WLIST:WAVeform:NEW "' + name + '", ' + str(size) + ', REAL'
        self.sendMessage(msg)

    def transmitWaveformData(self, name, data, marker1=[], marker2=[]):
        """
        Writes the Data given into the Waveformslot 'name' created by the
        function newWaveform
        """
        MARKER1 = 0b01000000
        MARKER2 = 0b10000000
        if (marker1 == []):
            marker1 = np.zeros(len(data), dtype=int)
        else:
            marker1 = marker1 * MARKER1

        if (marker2 == []):
            marker2 = np.zeros(len(data), dtype=int)
        else:
            marker2 = marker2 * MARKER2
        # self.newWaveform(name,len(data))
        block_data = ''
        msg = 'WLISt:WAVeform:DATA "' + name + '",0,'
        msg += str(len(data)) + ',#' + str(len(str(5 * len(data))))
        msg += str(5 * len(data))
        for val, m1, m2 in itertools.izip(data, marker1, marker2):
            converted_data = struct.pack('<fB',
                                         float(val),
                                         m1 + m2)
            block_data = block_data + converted_data
        msg += block_data

        self.sendMessage(msg, msg_type="waveform")

    def readWaveformNames(self):
        """
        Returns a List of all the Waveformnames (strings without enclosing "s)
        """
        msg = 'WLIST:SIZE?'
        ansr = self.queryMessage(msg)
        if ansr != "nothing to listen to":
            wnames = []
            for i in range(1, int(ansr)):
                msg = 'WLIST:NAME? '+str(i)
                wname = self.queryMessage(msg)
                wnames.append(wname)
            names = [re.findall('".*?"', wname)[0] for wname in wnames]
        else:
            names = []
        strippednames = []
        for name in names:
            strippednames.append(name.rstrip('"').lstrip('"'))
        return strippednames

        # return wnames

    def deleteWaveforms(self, Names=[]):
        """
        Deletes a list of Waveforms given to the function as strings
        The names are without the enclosing "s and is compliant with the format
        returned by the function readWaveformNames.
        Passing a single string will try to delete only this Waveform.
        """
        if isinstance(Names, basestring):
            msg = 'WLISt:WAVeform:DELete "' + Names + '"'
            self.sendMessage(msg)
        else:
            try:
                dlmsg = []
                for name in Names:
                    msg = 'WLISt:WAVeform:DELete "'+name+'"'
                    self.sendMessage(msg)
            except TypeError:
                raise TypeError('Waveform Names in function deleteWaveforms, \
                                please ensure that message is a string or a \
                                list of strings')

    def changeChannelDelay(self, Channel, Delay):
        """
        Changes the delay of the Channel to 'Delay' picoseconds
        """
        msg = 'SOURCE' + str(Channel) + ':DELAY:ADJUST ' + str(Delay)
        self.sendMessage(msg)

    def changeChannelPhase(self, Channel, Phase):
        """
        Changes the phase of the Channel to Phase in Degrees
        """
        msg = 'SOURCE' + str(Channel) + ':PHASE:ADJUST ' + str(Phase)
        self.sendMessage(msg)

    def changeChannelAmplitude(self, Channel, Amplitude):
        msg = 'SOURCE' + str(Channel) + ':VOLTage:LEVel:IMMediate:AMPLitude '
        msg += str(Amplitude)
        self.sendMessage(msg)

    def changeChannelOffset(self, Channel, Offset):
        msg = 'SOURCE' + str(Channel) + ':VOLTage:LEVel:IMMediate:OFFSet '
        msg += str(Offset)
        self.sendMessage(msg)

    def setChannelSkew(self, Channel, Skew):
        msg = 'SOURCE' + str(Channel) + ':SKEW ' + str(Skew) + "E-9"
        self.sendMessage(msg)

    def setChannelWaveformSequence(self,
                                   Channel,
                                   WaveformName,
                                   SequenceIndex=1):
        """
        Puts Waveform 'WaveformName' into Channel 'Channel'.
        If the RunMode is SEQuence, it will use the optional Argument
        'SequenceIndex' to determine the element in the sequence.
        """
        msg = 'SEQuence:ELEMent' + str(SequenceIndex) + ':WAVeform'
        msg += str(Channel) + ' "' + WaveformName + '"'
        self.sendMessage(msg, msg_type="waveform")

    def setChannelWaveform(self, Channel, WaveformName):
        """
        Puts Waveform 'WaveformName' into Channel 'Channel'.
        If the RunMode is SEQuence, it will use the optional Argument
        'SequenceIndex' to determine the element in the sequence.
        """
        msg = 'SOUR' + str(Channel) + ':WAVeform "' + WaveformName + '"'
        self.sendMessage(msg)

    def setRun(self, state):
        """
        Sets the run
        True = RUN
        False = STOP
        """
        if state:
            msg = "AWGControl:RUN"
        else:
            msg = "AWGControl:STOP"
        self.sendMessage(msg)

    def queryRunMode(self):
        msg = "AWGControl:RMODe?"
        return self.queryMessage(msg)

    def setRunMode(self, RunMode):
        """
        Sets the runmode of the machine
        RunModes are : CONTinuous, TRIGgered, GATed, SEQuence, ENHanced
        use CONT for normal operation and SEQuence for sequence operation
        """
        msg = "AWGControl:RMODe " + RunMode
        self.sendMessage(msg)

    def setChannelOutput(self, Channel, Output):
        """
        Sets the output of the channel
        """
        if Output:
            msg = "OUTPut"+str(Channel)+":STATe ON"
        else:
            msg = "OUTPut"+str(Channel)+":STATe OFF"
        self.sendMessage(msg)

    def setOutput(self, Output):
        """
        Sets all the outputs
        """
        self.setChannelOutput(1, Output)
        self.setChannelOutput(2, Output)
        self.setChannelOutput(3, Output)
        self.setChannelOutput(4, Output)

    def setOutputFilterChannel(self, Channel, filt):
        """
        Sets the filter of the channel output
        """
        msg = ''
        if filt == 'Through' or filt == 'INF':
            msg = "OUTPut"+str(Channel)+":FILTer:LPASs:FREQuency INF"
        self.sendMessage(msg)

    def setSourceMarkerDelay(self, Channel, Marker, Delay):
        """
        Sets the Delay of the Marker
        """
        msg = "SOURce" + str(Channel) + ":MARKer" + str(Marker)
        msg += ":DELay " + str(Delay)
        self.sendMessage(msg)

    def setDirectOutput(self, Channel, State):
        """
        This command enables the raw DAC waveform outputs for the specified
        channel.
        """
        if State:
            msg = "AWGControl:DOUTput"+str(Channel)+":STATe ON"
        else:
            msg = "AWGControl:DOUTput"+str(Channel)+":STATe OFF"
        self.sendMessage(msg)

    def setAddInput(self, Channel, State):
        """
        This command adds the signal from an external input to the output of
        the channel.
        """
        if State:
            msg = "SOURce"+str(Channel)+':COMBine:FEED "ESIGnal"'
        else:
            msg = "SOURce"+str(Channel)+':COMBine:FEED ""'
        self.sendMessage(msg)

    def setSourceMarkerVoltageHigh(self, Channel, Marker, VoltageHigh):
        """
        Sets the VoltageHigh of the Marker
        """
        msg = "SOURce" + str(Channel) + ":MARKer" + str(Marker)
        msg += ":VOLTage:HIGH " + str(VoltageHigh)
        self.sendMessage(msg)

    def setSourceMarkerVoltageLow(self, Channel, Marker, VoltageLow):
        """
        Sets the VoltageLow of the Marker
        """
        msg = "SOURce" + str(Channel) + ":MARKer" + str(Marker)
        msg += ":VOLTage:LOW " + str(VoltageLow)
        self.sendMessage(msg)

    def setSamplingRate(self, Rate):
        """
        This command and query sets or returns the sampling frequency of the
        arbitrary waveform generator. Sampling frequency can be set when the
        internal clock source is selected and one of the following conditions
        is met:
        """
        msg = "SOURce1:FREQuency "+str(Rate)
        self.sendMessage(msg)

    def setClockSource(self, Source):
        """
        This command and query sets or returns the clock source. When the clock
        source is internal, the arbitrary waveform generator's internal clock
        is used to generate the clock signal. If the clock source is external,
        the clock signal from an external oscillator is used.
        """
        if Source == 'Internal':
            msg = "AWGControl:CLOCk:SOURCe INTernal"
        else:
            msg = "AWGControl:CLOCk:SOURCe EXTernal"
        self.sendMessage(msg)

    def setReferenceOscillatorSource(self, Source):
        """
        This command selects the reference oscillator source. INTernal means
        that the reference frequency is derived from the internal precision
        oscillator. EXTernal means the reference frequency is derived from an
        external signal supplied through the Reference Clock Input connector.
        """
        if Source == 'Internal':
            msg = "ROSCillator:SOURCe INTernal"
        else:
            msg = "ROSCillator:SOURCe EXTernal"
        self.sendMessage(msg)

    def setReferenceOscillatorType(self, Type):
        """
        This command selects the type of the reference oscillator. This
        parameter is valid only when ClockSource is Internal and
        Reference Source is External.
        """
        if Type == 'FIXed' or Type == 'Fixed':
            msg = "ROSCillator:TYPE FIXed"
        else:
            msg = "ROSCillator:TYPE VARiable"
        self.sendMessage(msg)

    def setReferenceOscillatorFreq(self, Freq):
        """
        This command selects the reference oscillator frequency. Valid values
        are 10 MHz, 20 MHzand 100 MHz. This command is used when the Clock
        Source is Internal and Reference Input is External and External
        Reference Type is Fixed.
        """
        msg = "ROSCillator:FREQuency " + str(Freq)

        self.sendMessage(msg)

    def setReferenceOscillatorMult(self, Mult):
        """
        This command and query sets or returns the ROSCillator multiplier rate.
        This parameter is valid only when Clock Source is Internal and
        Reference Source is External and External Reference Type is Variable.
        """
        msg = "ROSCillator:MULTiplier " + str(int(Mult))
        self.sendMessage(msg)

    def setTriggerSequenceModeSynchronous(self, state=False):
        """
        This command and query sets or returns the trigger source
        """
        if state:
            msg = "TRIGger:SEQuence:MODE SYNChronous"
        else:
            msg = "TRIGger:SEQuence:MODE ASYNchronous"
        self.sendMessage(msg)

    def setTriggerSource(self, Source):
        """
        This command and query sets or returns the trigger source
        """
        if Source == 'Internal':
            msg = "TRIGger:SEQuence:SOURCe INTernal"
        else:
            msg = "TRIGger:SEQuence:SOURCe EXernal"

        self.sendMessage(msg)

    def setTriggerLevel(self, Level):
        """
        This command and query sets or returns the trigger input level
        (threshold).
        """
        msg = "TRIGger:SEQuence:LEVel " + str(Level)
        self.sendMessage(msg)

    def setTriggerSlope(self, Slope):
        """
        This command and query sets or returns the trigger slope. It is used
        to set polarity in modes other than gated mode.
        """
        if Slope == 'Positive':
            msg = "TRIGger:SEQuence:SLOPe POSitive"
        else:
            msg = "TRIGger:SEQuence:SLOPe NEGative"
        self.sendMessage(msg)

    def setTriggerImpedance(self, Impedance):
        """
        This command and query sets or returns the trigger impedance.
        It applies only to the external trigger.
        """
        if Impedance == '1k':
            msg = "TRIGger:SEQuence:IMPedance 1000"
        else:
            msg = "TRIGger:SEQuence:IMPedance 50"
        self.sendMessage(msg)

    def setEventLevel(self, Level):
        """
        This command and query sets or returns the event level.
        """
        msg = "EVENt:LEVel " + str(Level)
        self.sendMessage(msg)

    def setEventImpedance(self, Impedance):
        """
        This command and query sets or returns the impedance of the external
        event input. Valid values are 50 ohm or 1 kohm.
        """
        if Impedance == '1k':
            msg = "EVENt:IMPedance 1000"
        else:
            msg = "EVENt:IMPedance 50"
        self.sendMessage(msg)

    def setEventJumpTiming(self, JTiming):
        """
        This command and query sets or returns the jump timing. Refer to the
        User Online Help for more information on jump timing.
        """
        if JTiming == 'Async':
            msg = "EVENt:JTIMing ASYNchronous"
        else:
            msg = "EVENt:JTIMing SYNChronous"

        self.sendMessage(msg)

    def setEventPolarity(self, Polarity):
        """
        This command and query sets or returns the polarity of event signal.
        The Event Jump is the function to change the sequencing of the
        waveform by an event signal.
        """
        if Polarity == 'Positive':
            msg = "EVENt:POLarity POSitive"
        else:
            msg = "EVENt:POLarity NEGative"
        self.sendMessage(msg)

    def setDCOutputLevel(self, Channel, Level):
        """
        This command and query sets or returns the DC output level.
        The value of n = 1|2|3|4.
        At *RST, this returns 0 V.
        """
        msg = "AWGControl:DC" + str(Channel) + ":VOLTage:OFFSet " + str(Level)
        self.sendMessage(msg)

    def createSequence(self, SequenceLength):
        """
        This has to be called to initialize a sequence
        """
        msg = 'SEQuence:LENGth ' + str(SequenceLength)
        self.sendMessage(msg)

    def setSeqElementGoto(self, SequenceIndex=1, State=1, Index=1):
        """
        Used to set JumpMode for a sequence Element
        States are : 0(OFF) , 1(ON)
        """
        msg1 = "SEQuence:ELEMent" + str(SequenceIndex) + ":GOTO:STATe "
        msg1 += str(State)
        msg2 = "SEQuence:ELEMent" + str(SequenceIndex) + ":GOTO:INDex "
        msg2 += str(Index)

        self.sendMessage(msg1)
        if (State == 1):
            self.sendMessage(msg2)

    def setSeqElementJump(self, SequenceIndex=1, Type='INDex', Index=1):
        """
        Used to set JumpMode for a sequence Element
        Types are : INDex , NEXT, OFF
        """
        msg = "SEQuence:ELEMent"+str(SequenceIndex)+":JTARget:TYPE "+str(Type)
        self.sendMessage(msg)
        if (Type == 'INDex'):
            msg = "SEQuence:ELEMent"+str(SequenceIndex)+":JTARget:INDex "
            msg += str(Index)
            self.sendMessage(msg)

    def setSeqElementLooping(self, SequenceIndex=1, Repeat=1, InfiniteLoop=0):
        """
        Used to set JumpMode for a sequence Element
        States are : 0(OFF) , 1(ON)
        """
        if (InfiniteLoop == 1):
            msg = "SEQuence:ELEMent"+str(SequenceIndex)+":LOOP:INFinite 1"
            self.sendMessage(msg)
        else:
            msg = "SEQuence:ELEMent"+str(SequenceIndex)+":LOOP:INFinite 0"
            self.sendMessage(msg)
            msg = "SEQuence:ELEMent"+str(SequenceIndex)+":LOOP:COUNt "
            msg += +str(Repeat)
            self.sendMessage(msg)

    def setSeqElementTWait(self, SequenceIndex=1, TWait=False):
        """
        This command and query sets or returns the wait trigger state for an
        element. Send a trigger signal in one of the following ways:
        - By using an external trigger signal.
        - By pressing the "ForceTrigger" button on the front panel.
        - By sending the *TRG remote command
        """

        if TWait:
            msg = "SEQuence:ELEMent"+str(SequenceIndex)+":TWAit 1"
        else:
            msg = "SEQuence:ELEMent"+str(SequenceIndex)+":TWAit 0"
        self.sendMessage(msg)


class DRIVER_AWG5014(LowLevelCom_AWG5014):
    AWG_FILE_FORMAT_HEAD = {
        'SAMPLING_RATE': 'd',    # d
        'REPETITION_RATE': 'd',    # # NAME?
        'HOLD_REPETITION_RATE': 'h',    # True | False
        'CLOCK_SOURCE': 'h',    # Internal | External
        'REFERENCE_SOURCE': 'h',    # Internal | External
        'EXTERNAL_REFERENCE_TYPE': 'h',    # Fixed | Variable
        'REFERENCE_CLOCK_FREQUENCY_SELECTION': 'h',
        'REFERENCE_MULTIPLIER_RATE': 'h',    #
        'DIVIDER_RATE': 'h',   # 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256
        'TRIGGER_SOURCE': 'h',    # Internal | External
        'INTERNAL_TRIGGER_RATE': 'd',    #
        'TRIGGER_INPUT_IMPEDANCE': 'h',    # 50 ohm | 1 kohm
        'TRIGGER_INPUT_SLOPE': 'h',    # Positive | Negative
        'TRIGGER_INPUT_POLARITY': 'h',    # Positive | Negative
        'TRIGGER_INPUT_THRESHOLD': 'd',    #
        'EVENT_INPUT_IMPEDANCE': 'h',    # 50 ohm | 1 kohm
        'EVENT_INPUT_POLARITY': 'h',    # Positive | Negative
        'EVENT_INPUT_THRESHOLD': 'd',
        'JUMP_TIMING': 'h',    # Sync | Async
        'INTERLEAVE': 'h',    # On |  This setting is stronger than .
        'ZEROING': 'h',    # On | Off
        'COUPLING': 'h',    # The Off | Pair | All setting is weaker than .
        'RUN_MODE': 'h',    # Continuous | Triggered | Gated | Sequence
        'WAIT_VALUE': 'h',    # First | Last
        'RUN_STATE': 'h',    # On | Off
        'INTERLEAVE_ADJ_PHASE': 'd',
        'INTERLEAVE_ADJ_AMPLITUDE': 'd',
    }
    AWG_FILE_FORMAT_CHANNEL = {
        # Include NULL.(Output Waveform Name for Non-Sequence mode)
        'OUTPUT_WAVEFORM_NAME_N': 's',
        'CHANNEL_STATE_N': 'h',  # On | Off
        'ANALOG_DIRECT_OUTPUT_N': 'h',  # On | Off
        'ANALOG_FILTER_N': 'h',  # Enum type.
        'ANALOG_METHOD_N': 'h',  # Amplitude/Offset, High/Low
        # When the Input Method is High/Low, it is skipped.
        'ANALOG_AMPLITUDE_N': 'd',
        # When the Input Method is High/Low, it is skipped.
        'ANALOG_OFFSET_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'ANALOG_HIGH_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'ANALOG_LOW_N': 'd',
        'MARKER1_SKEW_N': 'd',
        'MARKER1_METHOD_N': 'h',  # Amplitude/Offset, High/Low
        # When the Input Method is High/Low, it is skipped.
        'MARKER1_AMPLITUDE_N': 'd',
        # When the Input Method is High/Low, it is skipped.
        'MARKER1_OFFSET_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'MARKER1_HIGH_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'MARKER1_LOW_N': 'd',
        'MARKER2_SKEW_N': 'd',
        'MARKER2_METHOD_N': 'h',  # Amplitude/Offset, High/Low
        # When the Input Method is High/Low, it is skipped.
        'MARKER2_AMPLITUDE_N': 'd',
        # When the Input Method is High/Low, it is skipped.
        'MARKER2_OFFSET_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'MARKER2_HIGH_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'MARKER2_LOW_N': 'd',
        'DIGITAL_METHOD_N': 'h',  # Amplitude/Offset, High/Low
        # When the Input Method is High/Low, it is skipped.
        'DIGITAL_AMPLITUDE_N': 'd',
        # When the Input Method is High/Low, it is skipped.
        'DIGITAL_OFFSET_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'DIGITAL_HIGH_N': 'd',
        # When the Input Method is Amplitude/Offset, it is skipped.
        'DIGITAL_LOW_N': 'd',
        'EXTERNAL_ADD_N': 'h',  # AWG5000 only
        'PHASE_DELAY_INPUT_METHOD_N':   'h',  # Phase/DelayInme/DelayInints
        'PHASE_N': 'd',  # When the Input Method is not Phase, it is skipped.
        # When the Input Method is not DelayInTime, it is skipped.
        'DELAY_IN_TIME_N': 'd',
        # When the Input Method is not DelayInPoint, it is skipped.
        'DELAY_IN_POINTS_N': 'd',
        'CHANNEL_SKEW_N': 'd',
        'DC_OUTPUT_LEVEL_N': 'd',  # V
    }
    # -------------------------- CONSTRUCTORS --------------------------
    def __init__(self, **kwargs):
        self.reset()

        # -- Runtype
        if "runtype" in kwargs.keys():
            self.runtype = kwargs["runtype"]
        else:
            self.runtype = RunType()

        if "conf_file" in kwargs.keys():
            self.conf_file = kwargs["conf_file"]
        else:
            self.conf_file = sv.Tektronix5014_defaultconfigfile

        # -- AWG config: Use kwarg or import default
        # Load default
        self._import_settings(conf_file=self.conf_file,
                              folder=sv.PATH_SrvInstruments_folder,
                              reset_status=True)

        # Look for settigns in kwargs
        if "settings" in kwargs.keys():
            self._overwrite_settings(kwargs["settings"])

        # - AWG ID settings: ip, port, awg_index, rank
        self._setAWG_ID()

        # - Channel settings
        self._setChannels()

        # -- Instanciating the LowLevelCom_AWG5014
        # Has to be after the runtype definition
        super(DRIVER_AWG5014, self).__init__(**kwargs)

    # -------------------------- PRIVATE METHODS ------------------------------
    # --------------------------     GENERAL    -------------------------------
    def reset(self):
        self.general_settings = {}
        self.channel_settings = {}
        self.channels = {}
        self.channel_range = range(1, 5)
        self.marker_range = range(1, 3)
        # self.settings = {}
        # self.nclock_trigdelay = 0

        # -- Load the default file for types
        file_default_types = sv.PATH_SrvInstruments_folder
        file_default_types += sv.Tektronix5014_defaultconfigfile
        ini_file = ConfigObj(file_default_types)

        # -- Create general and channel type dictionaries
        self.setting_types = ini_file["default_types"]

    # -------------------------- Sequence related -----------------------------
    def _verify_sequence(self, sequence, channel_names):
        """
        Verify the consistency of the data
        TODO!
        """
        pass

    # --------------------------     Settings    --------------------------
    def _import_settings(self, conf_file, folder, reset_status = False):
        """
        Import the
        """
        ini_file = ConfigObj("{}{}".format(folder, conf_file))
        ini_file = ini_file["default"]
        
        # -- Initialize the status dic
        if reset_status:
            self.settings = {"general_settings": {},
                           "channel_settings":
                           {i: {"marker_settings":{j:{} for j in self.marker_range}} for i in self.channel_range},
                           "sequence": {}}


        for skey, sval  in ini_file.items():
            # skey = ["general_settings", "channel_settings"]

            # - General settings
            if skey == "general_settings":
                for gkey, gval in sval.items():
                    self.settings[skey][gkey] = gval

            # - Channel settings
            elif skey == "channel_settings":
                for ckey, cval in sval.items():
                    cind = int(ckey)
                    # ckey = ["1", "2", "3", "4"]
                    for pkey, pval in cval.items():
                        #  pkey = ["RFline", "logical_name", ...]
                        if pkey != "marker_settings":
                            self.settings["channel_settings"][cind][pkey] = pval
                        else:
                            for mkey, mval in pval.items():
                                mind = int(mkey)
                                for mmkey, mmval in mval.items():
                                    self.settings["channel_settings"][cind]["marker_settings"][mind][mmkey] = mmval

        # Log
        log.send(level="debug",
                 context="DRIVER_AWG5014._import_settings",
                 message="done: {}.".format(conf_file))

        # Convert the imported dictionary to a typed dict.
        self._convert_setting_types()

    def _overwrite_settings(self, settings):
        """
        Overwrites the setting dictionary keys.
        """
        for skey, sval  in settings.items():
            # skey = ["general_settings", "channel_settings"]

            # - General settings
            if skey == "general_settings":
                for gkey, gval in sval.items():
                    self.settings[skey][gkey] = gval

            # - Channel settings
            elif skey == "channel_settings":
                for ckey, cval in sval.items():
                    cind = int(ckey)
                    # ckey = ["1", "2", "3", "4"]
                    for pkey, pval in cval.items():
                        if ckey != "marker_settings":
                            self.settings["channel_settings"][cind][pkey] = pval
                        else:
                            for mkey, mval in pval.items():
                                mind = int(mkey)
                                for mmkey, mmval in mval.items():
                                    self.settings["channel_settings"][cind]["marker_settings"][mind][mmkey] = mmval
        # Log
        log.send(level="debug",
                 context="DRIVER_AWG5014._overwrite_settings",
                 message="done.")

        # - Convert types
        self._convert_setting_types()

    def _convert_setting_types(self):
        """
        The imported dictionary has properties in a string format. This method
        runs over all propeties and convert them to the proper type.
        """

        type_cases = ["int", "integer", "str", "string", "float"]
        # All keys in settings
        for skey, sval in self.settings.items():
            if skey == "general_settings":
                for pkey, pval in sval.items():
                    t = self.setting_types[skey][pkey]
                    self.settings[skey][pkey] = self._convert_type(self.settings[skey][pkey], t)
            elif skey == "channel_settings":
                for ckey, cval in sval.items():
                    for pkey, pval in cval.items():
                        if pkey == "marker_settings":
                            for mkey, mval in pval.items():
                                for mmkey, mmval in mval.items():
                                    t = self.setting_types[skey][pkey][mmkey]
                                    self.settings[skey][ckey][pkey][mkey][mmkey] = self._convert_type(self.settings[skey][ckey][pkey][mkey][mmkey], t)
                        else:
                            t = self.setting_types[skey][pkey]
                            self.settings[skey][ckey][pkey] = self._convert_type(self.settings[skey][ckey][pkey], t)
        # Log
        log.send(level="debug",
                 context="DRIVER_AWG5014._convert_setting_types",
                 message="done.")

    @staticmethod
    def _convert_type(myval, mytyp):
        # case the types
        if (mytyp == "str") or (mytyp == "string"):
            ans = str(myval)
        elif (mytyp == "int") or (mytyp == "integer"):
            ans = int(myval)
        elif (mytyp == "float"):
            ans = float(myval)
        return ans

    def _setAWG_ID(self):
        """
        Import from the setting dictionary the properties given in inheritance:
        - ip
        - port
        - awg_index
        - rank
        """
        self.set_Ip(self.get_general_setting("ip"))
        self.set_Port(self.get_general_setting("port"))
        self.awg_index = self.get_general_setting("awg_index")
        self.awg_rank = self.get_general_setting("rank")

        # Log
        log.send(level="debug",
                 context="DRIVER_AWGs._setChannels",
                 message="done.")

    def _setChannels(self):
        """
        Using the channel properties in settings, instanciate all channels
        """
        for cind, cval in self.settings["channel_settings"].items():
            belongs_to_awg = self.settings["general_settings"]["awg_index"]
            # RFline = int(c["RFline"])
            # logical_name = c["logical_name"]
            # physical_channel = c["physical_channel"]
            self.add_channel(cind, cval, belongs_to_awg)

        # Log
        log.send(level="debug",
                 context="DRIVER_AWGs._setChannels",
                 message="done.")

    # -------------------------- Global commands --------------------------
    def _reduce_wfs(self):
        """
        Check if all sequences for each channel is constant.
        If so, reduce to 1 sequence.
        """
        if self.runtype.isproperty("awg_use_reduced_wfs"):
            if self.runtype.get("awg_use_reduced_wfs"):
                constant_wfs = []
                for c in self.channels.values():
                    wfs, wf_names = c.get_waveforms()
                    t = True
                    for i in np.arange(1, wfs.shape[1]):
                        if any(wfs[:, i] != wfs[:, 0]):
                            t = False
                    constant_wfs.append(t)

                if all(t for t in constant_wfs):
                    for c in self.channels.values():
                        wfs, wf_names = c.get_waveforms()
                        new_wfs = np.zeros((wfs.shape[0], 1))
                        new_wfs[:, 0] = wfs[:, 0]
                        new_wf_names = [wf_names[0]]
                        c.set_waveforms(new_wfs, wf_names=new_wf_names)

                # Log
                log.send(level="debug",
                         context="DRIVER_AWGs._reduce_wfs",
                         message="done.")

    def _send_sequence(self):
        """
        Send a sequence, with the proper Wait/Goto configuration
        """
        # - Open Communication
        self.openCom()

        self._normalize_sequence_to_m0_a1()
        self._configure_amplitude_offset()

        # - Check for repetitions

        # - Create the sequence
        sequence_length = self.getSequenceLength()
        self.createSequence(SequenceLength=sequence_length)

        # - Set sequence elements
        for n_c, c in enumerate(self.channels.values()):
            # wfs, wf_names, wf_counts = c.get_waveforms()
            wfs, wf_names = c.get_waveforms()
            sequence_index = 1
            physical_channel = c.get_physical_channel()
            awg_rank = self.awg_rank

            for i in range(wfs.shape[1]):
                # Hardcode triggers ...
                if int(physical_channel) == 1 and awg_rank == "Master":
                    marker = np.ones(wfs[:, i].size)
                    marker[0] = 1
                    marker[1:100] = 0
                else:
                    marker = []

                # Send waveform
                self._send_wf(channel=physical_channel,
                              SequenceIndex=sequence_index,
                              wf=wfs[:, i],
                              marker1=marker,
                              marker2=marker)

                if sequence_index == sequence_length:
                    self.setSeqElementGoto(SequenceIndex=sequence_index,
                                           Index=1)

                sequence_index += 1

        # - Set sequence behavior
        sequence_index = 1
        for i in range(sequence_length):
            self.setSeqElementTWait(SequenceIndex=sequence_index,
                                    TWait=True)
            sequence_index += 1

        # - Close Communication
        self.closeCom()

    def _send_wf(self,
                 channel,
                 SequenceIndex,
                 wf_name,
                 wf,
                 marker1=[],
                 marker2=[]):
        self.newWaveform(name=wf_name, size=wf.size)
        self.transmitWaveformData(name=wf_name,
                                  data=wf,
                                  marker1=marker1,
                                  marker2=marker2)
        self.setChannelWaveformSequence(Channel=channel,
                                        WaveformName=wf_name,
                                        SequenceIndex=int(SequenceIndex))
        self._wait_OPC()

    def _normalize_sequence_to_m0_a1(self):
        """
        """
        for n_c, c in enumerate(self.channels.values()):
            wfs, wf_names = c.get_waveforms()
            amplitude = 2.*np.max(np.abs(wfs))
            c.set_offset(0.)
            c.set_amplitude(amplitude * c.applied_over_command_voltage_ratio)
            if np.max(np.abs(wfs)) > 0:
                c._set_waveforms(wfs/np.max(np.abs(wfs)))

    def _configure_amplitude_offset(self):
        """Set each channel amplitude and offset in channel_settings"""
        for ckey, cval in self.channels.items():
            cind = cval.get_physical_channel()
            amplitude = cval.get_amplitude()
            if amplitude > 0:
                pass
            else:
                amplitude = 0.02

            #  Do something
            self.settings["channel_settings"][cind]["AMPLITUDE"] = amplitude
            self.settings["channel_settings"][cind]["OFFSET"] = 0.

        # Log
        log.send(level="debug",
                 context="DRIVER_AWGs._configure_amplitude_offset",
                 message="Amplitude set to {}, {}, {}, {} V".format(\
                    self.settings["channel_settings"][1]["AMPLITUDE"],
                    self.settings["channel_settings"][2]["AMPLITUDE"],
                    self.settings["channel_settings"][3]["AMPLITUDE"],
                    self.settings["channel_settings"][4]["AMPLITUDE"],))

    def make_awg_file(self, waveforms, m1s, m2s,
                      nreps, trig_waits,
                      goto_states, jump_tos,
                      channels=None, preservechannelsettings=True):
        """
        Args:
            waveforms (list): A list of the waveforms to be packed. The list
                should be filled like so:
                [[wfm1ch1, wfm2ch1, ...], [wfm1ch2, wfm2ch2], ...]
                Each waveform should be a numpy array with values in the range
                -1 to 1 (inclusive). If you do not wish to send waveforms to
                channels 1 and 2, use the channels parameter.

            m1s (list): A list of marker 1's. The list should be filled
                like so:
                [[elem1m1ch1, elem2m1ch1, ...], [elem1m1ch2, elem2m1ch2], ...]
                Each marker should be a numpy array containing only 0's and 1's

            m2s (list): A list of marker 2's. The list should be filled
                like so:
                [[elem1m2ch1, elem2m2ch1, ...], [elem1m2ch2, elem2m2ch2], ...]
                Each marker should be a numpy array containing only 0's and 1's

            nreps (list): List of integers specifying the no. of
                repetions per sequence element.  Allowed values: 0 to
                65536. O corresponds to Infinite repetions.

            trig_waits (list): List of len(segments) of integers specifying the
                trigger wait state of each sequence element.
                Allowed values: 0 (OFF) or 1 (ON).

            goto_states (list): List of len(segments) of integers
                specifying the goto state of each sequence
                element. Allowed values: 0 to 65536 (0 means next)

            jump_tos (list): List of len(segments) of integers specifying
                the logic jump state for each sequence element. Allowed values:
                0 (OFF) or 1 (ON).

            channels (list): List of channels to send the waveforms to.
                Example: [1, 3, 2]

            preservechannelsettings (bool): If True, the current channel
                settings are found from the parameter history and added to
                the .awg file. Else, channel settings are not written in the
                file and will be reset to factory default when the file is
                loaded. Default: True.
            """
        packed_wfs = {}
        waveform_names = []
        if not isinstance(waveforms[0], list):
            waveforms = [waveforms]
            m1s = [m1s]
            m2s = [m2s]
        for ii in range(len(waveforms)):
            namelist = []
            for jj in range(len(waveforms[ii])):
                if channels is None:
                    thisname = 'wfm{:03d}ch{}'.format(jj + 1, ii + 1)
                else:
                    thisname = 'wfm{:03d}ch{}'.format(jj + 1, channels[ii])
                namelist.append(thisname)

                package = self._pack_waveform(waveforms[ii][jj],
                                              m1s[ii][jj],
                                              m2s[ii][jj])

                packed_wfs[thisname] = package
            waveform_names.append(namelist)

        wavenamearray = np.array(waveform_names, dtype='str')

        channel_cfg = {}

        return self._generate_awg_file(
            packed_wfs, wavenamearray, nreps, trig_waits, goto_states,
            jump_tos, channel_cfg,
            preservechannelsettings=preservechannelsettings)

    def _pack_record(self, name, value, dtype):
        """
        packs awg_file record into a struct in the folowing way:
            struct.pack(fmtstring, namesize, datasize, name, data)
        where fmtstring = '<IIs"dtype"'

        The file record format is as follows:
        Record Name Size:        (32-bit unsigned integer)
        Record Data Size:        (32-bit unsigned integer)
        Record Name:             (ASCII) (Include NULL.)
        Record Data
        For details see "File and Record Format" in the AWG help

        < denotes little-endian encoding, I and other dtypes are format
        characters denoted in the documentation of the struct package

        Args:
            name (str): Name of the record (Example: 'MAGIC' or
            'SAMPLING_RATE')
            value (Union[int, str]): The value of that record.
            dtype (str): String specifying the data type of the record.
                Allowed values: 'h', 'd', 's'.
        """
        if len(dtype) == 1:
            record_data = struct.pack('<' + dtype, value)
        else:
            if dtype[-1] == 's':
                record_data = value.encode('ASCII')
            else:
                record_data = struct.pack('<' + dtype, *value)

        # the zero byte at the end the record name is the "(Include NULL.)"
        record_name = name.encode('ASCII') + b'\x00'
        record_name_size = len(record_name)
        record_data_size = len(record_data)
        size_struct = struct.pack('<II', record_name_size, record_data_size)
        packed_record = size_struct + record_name + record_data
        
        return packed_record

    def _pack_waveform(self, wf, m1, m2):
        """
        Converts/packs a waveform and two markers into a 16-bit format
        according to the AWG Integer format specification.
        The waveform occupies 14 bits and the markers one bit each.
        See Table 2-25 in the Programmer's manual for more information

        Since markers can only be in one of two states, the marker input
        arrays should consist only of 0's and 1's.

        Args:
            wf (numpy.ndarray): A numpy array containing the waveform. The
                data type of wf is unimportant.
            m1 (numpy.ndarray): A numpy array containing the first marker.
            m2 (numpy.ndarray): A numpy array containing the second marker.

        Returns:
            numpy.ndarray: An array of unsigned 16 bit integers.

        Raises:
            Exception: if the lengths of w, m1, and m2 don't match
            TypeError: if the waveform contains values outside (-1, 1)
            TypeError: if the markers contain values that are not 0 or 1
        """

        # Input validation
        if (not((len(wf) == len(m1)) and ((len(m1) == len(m2))))):
            raise Exception('error: sizes of the waveforms do not match')
        if np.min(wf) < -1 or np.max(wf) > 1:
            raise TypeError('Waveform values out of bonds.' +
                            ' Allowed values: -1 to 1 (inclusive)')
        if not np.all(np.in1d(m1, np.array([0, 1]))):
            raise TypeError('Marker 1 contains invalid values.' +
                            ' Only 0 and 1 are allowed')
        if not np.all(np.in1d(m2, np.array([0, 1]))):
            raise TypeError('Marker 2 contains invalid values.' +
                            ' Only 0 and 1 are allowed')

        wflen = len(wf)
        packed_wf = np.zeros(wflen, dtype=np.uint16)
        packed_wf += np.uint16(np.round(wf * 8191) + 8191 +
                               np.round(16384 * m1) +
                               np.round(32768 * m2))
        if len(np.where(packed_wf == -1)[0]) > 0:
            print(np.where(packed_wf == -1))
        return packed_wf

    def generate_sequence_cfg(self):
        """
        This function is used to generate a config file, that is used when
        generating sequence files, from existing settings in the awg.
        Querying the AWG for these settings takes ~0.7 seconds
        """
        # log.info('Generating sequence_cfg')

        AWG_sequence_cfg = {
            # 'SAMPLING_RATE': self.get('clock_freq'),
            'SAMPLING_RATE': self.get_general_setting('SAMPLING_RATE'),
            # 'CLOCK_SOURCE': (1 if self.clock_source().startswith('INT')
            #                  else 2),  # Internal | External
            'CLOCK_SOURCE': (1 if self.get_general_setting('CLOCK_SOURCE').startswith('INT') else 2),
            # 'REFERENCE_SOURCE': (1 if self.ref_source().startswith('INT') else 2),  # Internal | External
            'REFERENCE_SOURCE': (1 if self.get_general_setting('REFERENCE_SOURCE').startswith('INT') else 2),
            # 'EXTERNAL_REFERENCE_TYPE':   1,  # Fixed | Variable
            'EXTERNAL_REFERENCE_TYPE': (1 if self.get_general_setting('REFERENCE_SOURCE').startswith('FIX') else 2),
            # 'REFERENCE_CLOCK_FREQUENCY_SELECTION': 1, # 10 MHz | 20 MHz | 100 MHz
            'REFERENCE_CLOCK_FREQUENCY_SELECTION': self.get_general_setting('REFERENCE_CLOCK_FREQUENCY_SELECTION'),
            'REFERENCE_MULTIPLIER_RATE': self.get_general_setting('REFERENCE_MULTIPLIER_RATE'),
            # 'TRIGGER_SOURCE':   1 if
            # self.get('trigger_source').startswith('EXT') else 2,
            # # External | Internal
            'TRIGGER_SOURCE': (1 if self.get_general_setting('TRIGGER_SOURCE').startswith('EXT') else 2),
            # 'TRIGGER_INPUT_IMPEDANCE': (1 if self.get('trigger_impedance') ==
            #                             50. else 2),  # 50 ohm | 1 kohm
            'TRIGGER_INPUT_IMPEDANCE': (1 if self.get_general_setting('TRIGGER_INPUT_IMPEDANCE').startswith('50') else 2),
            # 'TRIGGER_INPUT_SLOPE': (1 if self.get('trigger_slope').startswith(
            #                         'POS') else 2),  # Positive | Negative
            'TRIGGER_INPUT_SLOPE': (1 if self.get_general_setting('TRIGGER_INPUT_SLOPE').startswith('POS') else 2),
            # 'TRIGGER_INPUT_POLARITY': (1 if self.ask('TRIGger:' +
            #                                          'POLarity?').startswith(
            #                            'POS') else 2),  # Positive | Negative
            'TRIGGER_INPUT_POLARITY': (1 if self.get_general_setting('TRIGGER_INPUT_POLARITY').startswith('POS') else 2),
            # 'TRIGGER_INPUT_THRESHOLD':  self.get('trigger_level'),  # V
            'TRIGGER_INPUT_THRESHOLD': self.get_general_setting('TRIGGER_INPUT_THRESHOLD'),
            # 'EVENT_INPUT_IMPEDANCE':   (1 if self.get('event_impedance') ==
            #                             50. else 2),  # 50 ohm | 1 kohm
            'EVENT_INPUT_IMPEDANCE': (1 if self.get_general_setting('EVENT_INPUT_IMPEDANCE').startswith('50') else 2),
            # 'EVENT_INPUT_POLARITY':  (1 if self.get('event_polarity').startswith(
            #                           'POS') else 2),  # Positive | Negative
            'EVENT_INPUT_POLARITY': (1 if self.get_general_setting('EVENT_INPUT_POLARITY').startswith('POS') else 2),
            # 'EVENT_INPUT_THRESHOLD':   self.get('event_level'),  # V
            'EVENT_INPUT_THRESHOLD': self.get_general_setting('EVENT_INPUT_THRESHOLD'),
            # 'JUMP_TIMING':   (1 if
            #                   self.get('event_jump_timing').startswith('SYNC')
            #                   else 2),  # Sync | Async
            'JUMP_TIMING': (1 if self.get_general_setting('JUMP_TIMING').startswith('SYNC') else 2),
            # 'RUN_MODE':   4,  # Continuous | Triggered | Gated | Sequence
            'RUN_MODE': (4 if self.get_general_setting('RUN_MODE').startswith('SEQ') else 1),
            # 'RUN_STATE':  0,  # On | Off
            'RUN_STATE': self.get_general_setting('RUN_STATE'),
        }

        # Log
        log.send(level="debug",
                 context="DRIVER_AWGs.generate_sequence_cfg",
                 message="done.")

        return AWG_sequence_cfg

    def generate_channel_cfg(self):
        """
        Function to generate a channel config
        Returns:
            dict: A dict with the current setting for each entry in
            AWG_FILE_FORMAT_HEAD iff this entry applies to the
            AWG5014 AND has been changed from its default value.
        """
        # log.info('Getting channel configurations.')

        AWG_channel_cfg = {}

        # for chan in range(1, self.num_channels+1):
        # for ckey, cval in self.channels.items():
        for cind, cval in self.settings["channel_settings"].items():
            AWG_channel_cfg['ANALOG_DIRECT_OUTPUT_{}'.format(cind)] =\
                self.settings["channel_settings"][cind]["ANALOG_DIRECT_OUTPUT"]
            AWG_channel_cfg['ANALOG_FILTER_{}'.format(cind)] =\
                self.settings["channel_settings"][cind]["ANALOG_FILTER"]
            AWG_channel_cfg['ANALOG_AMPLITUDE_{}'.format(cind)] =\
                self.settings["channel_settings"][cind]["AMPLITUDE"]
            AWG_channel_cfg['ANALOG_OFFSET_{}'.format(cind)] =\
                self.settings["channel_settings"][cind]["OFFSET"]
            AWG_channel_cfg['EXTERNAL_ADD_{}'.format(cind)] =\
                self.settings["channel_settings"][cind]["EXTERNAL_ADD"]

            for mind, mval in cval["marker_settings"].items():
                # mind = int(mkey)
                AWG_channel_cfg['MARKER{}_HIGH_{}'.format(mind, cind)] =\
                                                            mval["HIGH"]
                AWG_channel_cfg['MARKER{}_LOW_{}'.format(mind, cind)] =\
                                                            mval["LOW"]
                AWG_channel_cfg['MARKER{}_SKEW_{}'.format(mind, cind)] =\
                                                            mval["SKEW"]
        # Log
        log.send(level="debug",
                 context="DRIVER_AWGs.generate_channel_cfg",
                 message="done.")

        return AWG_channel_cfg

    def _generate_awg_file(self,
                           packed_waveforms, wfname_l, nrep, trig_wait,
                           goto_state, jump_to, channel_cfg,
                           sequence_cfg=None,
                           preservechannelsettings=False):
        """
        This function generates an .awg-file for uploading to the AWG.
        The .awg-file contains a waveform list, full sequencing information
        and instrument configuration settings.

        Args:
            packed_waveforms (dict): dictionary containing packed waveforms
            with keys wfname_l

            wfname_l (numpy.ndarray): array of waveform names, e.g.
                array([[segm1_ch1,segm2_ch1..], [segm1_ch2,segm2_ch2..],...])

            nrep (list): list of len(segments) of integers specifying the
                no. of repetions per sequence element.
                Allowed values: 1 to 65536.

            trig_wait (list): list of len(segments) of integers specifying the
                trigger wait state of each sequence element.
                Allowed values: 0 (OFF) or 1 (ON).

            goto_state (list): list of len(segments) of integers specifying the
                goto state of each sequence element. Allowed values: 0 to 65536
                (0 means next)

            jump_to (list): list of len(segments) of integers specifying
                the logic jump state for each sequence element. Allowed values:
                0 (OFF) or 1 (ON).

            channel_cfg (dict): dictionary of valid channel configuration
                records. See self.AWG_FILE_FORMAT_CHANNEL for a complete
                overview of valid configuration parameters.

            preservechannelsettings (bool): If True, the current channel
                settings are queried from the instrument and added to
                channel_cfg (does not overwrite). Default: False.

            sequence_cfg (dict): dictionary of valid head configuration records
                     (see self.AWG_FILE_FORMAT_HEAD)
                     When an awg file is uploaded these settings will be set
                     onto the AWG, any parameter not specified will be set to
                     its default value (even overwriting current settings)

        for info on filestructure and valid record names, see AWG Help,
        File and Record Format (Under 'Record Name List' in Help)
        """
        #if preservechannelsettings:
        # channel_settings = self.generate_channel_cfg()
        channel_cfg = self.generate_channel_cfg() 
        # for setting in channel_settings:
        #     if setting not in channel_cfg:
        #         channel_cfg.update({setting: channel_settings[setting]})

        timetuple = tuple(np.array(localtime())[[0, 1, 8, 2, 3, 4, 5, 6, 7]])

        # general settings
        head_str = BytesIO()
        bytes_to_write = (self._pack_record('MAGIC', 5000, 'h') +
                          self._pack_record('VERSION', 1, 'h'))
        head_str.write(bytes_to_write)
        # head_str.write(string(bytes_to_write))

        if sequence_cfg is None:
            sequence_cfg = self.generate_sequence_cfg()

        for k in list(sequence_cfg.keys()):
            if k in self.AWG_FILE_FORMAT_HEAD:
                head_str.write(self._pack_record(k, sequence_cfg[k],
                                                 self.AWG_FILE_FORMAT_HEAD[k]))
            else:
                pass
                # log.warning('AWG: ' + k +
                #             ' not recognized as valid AWG setting')
        # channel settings
        ch_record_str = BytesIO()
        for k in list(channel_cfg.keys()):
            ch_k = k[:-1] + 'N'
            if ch_k in self.AWG_FILE_FORMAT_CHANNEL:
                pack = self._pack_record(k, channel_cfg[k],
                                         self.AWG_FILE_FORMAT_CHANNEL[ch_k])
                ch_record_str.write(pack)

            else:
                pass
                # log.warning('AWG: ' + k +
                #             ' not recognized as valid AWG channel setting')

        # waveforms
        ii = 21

        wf_record_str = BytesIO()
        wlist = list(packed_waveforms.keys())
        wlist.sort()
        for wf in wlist:
            wfdat = packed_waveforms[wf]
            lenwfdat = len(wfdat)

            wf_record_str.write(
                self._pack_record('WAVEFORM_NAME_{}'.format(ii), wf + '\x00',
                                  '{}s'.format(len(wf + '\x00'))) +
                self._pack_record('WAVEFORM_TYPE_{}'.format(ii), 1, 'h') +
                self._pack_record('WAVEFORM_LENGTH_{}'.format(ii),
                                  lenwfdat, 'l') +
                self._pack_record('WAVEFORM_TIMESTAMP_{}'.format(ii),
                                  timetuple[:-1], '8H') +
                self._pack_record('WAVEFORM_DATA_{}'.format(ii), wfdat,
                                  '{}H'.format(lenwfdat)))
            ii += 1

        # sequence
        kk = 1
        seq_record_str = BytesIO()
     
        for segment in wfname_l.transpose():

            seq_record_str.write(
                self._pack_record('SEQUENCE_WAIT_{}'.format(kk),
                                  trig_wait[kk - 1], 'h') +
                self._pack_record('SEQUENCE_LOOP_{}'.format(kk),
                                  int(nrep[kk - 1]), 'l') +
                self._pack_record('SEQUENCE_JUMP_{}'.format(kk),
                                  jump_to[kk - 1], 'h') +
                self._pack_record('SEQUENCE_GOTO_{}'.format(kk),
                                  goto_state[kk - 1], 'h'))
            for wfname in segment:
                if wfname is not None:
                    # TODO (WilliamHPNielsen): maybe infer ch automatically
                    # from the data size?
                    ch = wfname[-1]
                    seq_record_str.write(
                        self._pack_record('SEQUENCE_WAVEFORM_NAME_CH_' + ch
                                          + '_{}'.format(kk), wfname + '\x00',
                                          '{}s'.format(len(wfname + '\x00')))
                    )
            kk += 1

        awg_file = (head_str.getvalue() + ch_record_str.getvalue() +
                    wf_record_str.getvalue() + seq_record_str.getvalue())
        
        # Log
        log.send(level="debug",
                 context="DRIVER_AWGs._generate_awg_file",
                 message="done.")

        return awg_file

    def send_awg_file(self, filename, awg_file):
        """
        Writes an .awg-file onto the disk of the AWG.
        Overwrites existing files.

        Args:
            filename (str): The name that the file will get on
                the AWG.
            awg_file (bytes): A byte sequence containing the awg_file.
                Usually the output of self.make_awg_file.
            verbose (bool): A boolean to allow/suppress printing of messages
                about the status of the filw writing. Default: False.
        """
        # Log
        msg = "Writing to: {}{}".format(
                self.queryMessage('MMEMory:CDIRectory?').replace('\n', '\ '),
                filename)
        log.send(level="debug",
                 context="DRIVER_AWG5014.send_awg_file",
                 message=msg)

        # Header indicating the name and size of the file being send
        name_str = 'MMEMory:DATA "{}",'.format(filename).encode('ASCII')
        size_str = ('#' + str(len(str(len(awg_file)))) +
                    str(len(awg_file))).encode('ASCII')
        msg = name_str + size_str + awg_file

        self.sendMessage(msg, msg_type="waveform")

    def load_awg_file(self, filename):
        """
        Loads an .awg-file from the disc of the AWG into the AWG memory.
        This may overwrite all instrument settings, the waveform list, and the
        sequence in the sequencer.

        Args:
            filename (str): The filename of the .awg-file to load.
        """
        # Log
        msg = "Loading awg file using {}".format(filename)
        log.send(level="debug",
                 context="DRIVER_AWG5014.send_awg_file",
                 message=msg)

        # Send the instruction
        msg = 'AWGControl:SREStore "{}"'.format(filename)
        self.sendMessage(msg, msg_type="waveform")

    # -------------------------- PUBLIC METHODS -------------------------------
    # -------------------------- Global commands ------------------------------
    def Retrieve_status(self):
        """
        Retrieve the state of all properties that exists in:
            general_settings
            channel_settings
            sequence
        """

        # -- Open a communication if necessary
        self.openCom()

        # -- Initialize the status dic
        self.status = {"general_settings": {},
                       "channel_settings":
                       {i: {"marker_settings":{j:{} for j in self.marker_range}} for i in self.channel_range},
                       "sequence": {}}

        # - General settings
        for prop, func in self.addresses["general_settings"].items():
            msg = func("query")
            ans = self.queryMessage(msg)
            self.status["general_settings"][prop] = ans

        # - Channel settings
        for prop, func in self.addresses["channel_settings"].items():
            for channel in self.channel_range:
                # All but markers
                if prop != "marker_settings":
                    msg = func("query", channel)
                    ans = self.queryMessage(msg)
                    self.status["channel_settings"][channel][prop] = ans
                # Markers
                elif prop == "marker_settings":
                    for marker_prop, marker_func in func.items():
                        for marker in self.marker_range:
                            msg = marker_func("query", channel, marker)
                            ans = self.queryMessage(msg)
                            self.status["channel_settings"][channel]["marker_settings"][marker][marker_prop] = ans

        # -- Close a communication if necessary
        self.closeCom()

    def add_channel(self, physical_channel, channel_conf, belongs_to_awg):
        # physical_channel, logical_name, RFline):
        logical_name = channel_conf["logical_name"]
        self.channels[logical_name] = Channel(physical_channel,
                                              channel_conf,
                                              belongs_to_awg)

    def OutputRunOFF(self):
        # Open Communication
        self.openCom()

        # Outputs off
        self.setOutput(False)
        # Run stop
        self.setRun(False)

        # Close Communication
        self.closeCom()

    def OutputRunON(self):
        # Open Communication
        self.openCom()

        # Run True
        self.setRun(True)
        # Outputs on
        self.setOutput(True)

        # Close Communication
        self.closeCom()

    def load_settings(self,
                      overwritting_settings={},
                      default_conf_file="Tektronix5014_default.ini",
                      default_folder=sv.PATH_SrvInstruments_folder):
        """
        Load the settings given by the main AWG driver as a dictionary.
        If this dictionary is uncomplete, will load default values for this
        awg.
        """

        # - Reset settings
        self.reset()

        # - Import default settings for a 5014
        self._import_settings(conf_file=default_conf_file,
                              folder=default_folder)

        # - Overwrite settings
        self._overwrite_settings(overwritting_settings)

        # - update isConfigured
        self.set_isConfigured(False)

        # - AWG ID settings: ip, port, awg_index, rank
        self._setAWG_ID()

        # - Channel settings
        self._setChannels()

    def SendToInstrument(self):
        """
        QCoDeS version
        """
        # -- Reduce  the waveforms
        self._reduce_wfs()

        # -- Normalize the waveforms
        self._normalize_sequence_to_m0_a1()

        # -- Set the AMPLITUDE and OFFSET of the channel_settings
        self._configure_amplitude_offset()

        # -- Make the awg file
        waveforms = []
        for c in self.channels.values():
            wfs, wf_names = c.get_waveforms()
            waveforms.append([wfs[:,i] for i in np.arange(wfs.shape[1])])

        # Hardcode triggers ...
        m1s = []
        channels = []
        for ckey, cval in self.channels.items():
            cind = cval.physical_channel
            channels.append(cind)
            cm = []
            for i in np.arange(wfs.shape[1]):
                s = wfs[:, i].size
                if (cind == 1) and (self.get_general_setting("rank") == "Master"):
                    marker = np.ones(s)
                    marker[0] = 1
                    marker[1:100] = 0
                else:
                    marker = np.zeros(s)
                cm.append(marker)
            m1s.append(cm)
        m2s = m1s

        nreps = [1] * len(waveforms[0])
        trig_waits = [1] * len(waveforms[0])
        goto_states = list(range(2, 2 + len(waveforms[0])))
        goto_states[-1] = 1
        jump_tos = [0] * len(waveforms[0])
        awg_file = self.make_awg_file(waveforms, m1s, m2s,
                                      nreps, trig_waits,
                                      goto_states, jump_tos,
                                      channels=channels, preservechannelsettings=False)
        filename = "test.AWG"
        self.openCom()
        self.send_awg_file(filename=filename, awg_file=awg_file)
        self.load_awg_file(filename)
        self.closeCom()

    # -------------------------- Sequence related --------------------------
    def load_instructions(self, sequence, channel_names):
        """
        Import selectively instructions form the full sequence
        """
        # -- Verify the data availability
        self._verify_sequence(sequence, channel_names)

        # -- Load
        for c in self.channels.keys():
            # - Get channel index
            index = 0
            for cn in channel_names:
                if cn == c:
                    c_index = index
                else:
                    index += 1

            # - Get subarray
            channel_array = sequence[c_index, :, :]

            # - Generate waveform_names

            self.channels[c].set_waveforms(channel_array)

    # --------------------------       Get      --------------------------

    def get_general_setting(self, prop):
        """
        Return, if exists, the value of a property in self.general_settings
        """
        if prop in self.settings["general_settings"].keys():
            return self.settings["general_settings"][prop]
        else:
            raise ValueError(prop + " doesn't exist in settings.")

    def get_channel_setting(self, channel, prop):
        """
        Return, if exists, the value of a property in self.general_settings
        """
        if prop in self.settings["channel_settings"][channel].keys():
            return self.settings["channel_settings"][channel][prop]
        else:
            raise ValueError(prop + " doesn't exist in settings.")

    def getSequenceLength(self):
        """
        Get the length of the sequence.
        Also verify that all channels have the same sequence length.
        """
        seq_lengths = []
        for n_c, c in enumerate(self.channels.values()):
            wfs, wf_names = c.get_waveforms()
            seq_lengths.append(wfs.shape[1])

        for i in range(1, len(seq_lengths)):
            if seq_lengths[0] != seq_lengths[i]:
                raise ValueError("Not all channels have the same sequence \
                                  length.")

        return seq_lengths[0]

    def get_settings(self):
        """
        Returns self.status
        """
        return self.status

    def get_synchro_wait(self):
        return self.wait_wf, self.wait_name

    # --------------------------     Settings    --------------------------
    def Export_Channels_config_file(self):
        channels = {}
        for c in self.channels.keys():
            channels[c] = self.channels[c].Export_Channel_config_file()
        return channels

    # --------------------------     deprecated    --------------------------
    def _define_synchro_wait(self):
        self.wait_name = "wait"+str(self.min_length)
        self.wait_wf = np.zeros(self.min_length)


if __name__ == '__main__':
    pass
