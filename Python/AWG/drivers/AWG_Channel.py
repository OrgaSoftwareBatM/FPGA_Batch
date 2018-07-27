# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------
#  LIBRARY import
#--------------------------------------------------------------------------------

import os
import numpy as np

import AWG.drivers.SHARED_variables as sv
from AWG.drivers.RunType import RunType
#--------------------------------------------------------------------------------
#  Channel
#--------------------------------------------------------------------------------

class Channel:
    def __init__(self, physical_channel, channel_conf, belongs_to_awg, **kwargs):
        #physical_channel, logical_name, RFline):

        # -- Kwargs
        # Runtype
        if "runtype" in kwargs.keys():
            self.runtype = kwargs["runtype"]
        else:
            self.runtype = RunType()

        # -- Channel description
        # self.physical_channel = channel_conf["physical_channel"]
        self.physical_channel = physical_channel
        self.logical_name = channel_conf["logical_name"]
        self.RFline = int(channel_conf["RFline"])
        self.triggering_delay = float(channel_conf["triggering_delay"])

        # -- Markers
        self.markers = {}
        for mind, mval in channel_conf["marker_settings"].items():
            self.markers[mind] = {}
            for pind, pval in mval.items():
                self.markers[mind][pind] = pval

        # -- Line attenuation
        self.applied_over_command_voltage_ratio = 1.
        if channel_conf["terminal_impedance"] == "high":
            self.applied_over_command_voltage_ratio = self.applied_over_command_voltage_ratio / 2.
        self.applied_over_command_voltage_ratio *= 10**(float(channel_conf["line_insertion_loss"])/20.)

        # -- Parent AWG index
        self.belongs_to_awg = belongs_to_awg


        # -- Channel waveforms
        self.reset()

    def reset(self):
        """
        Reset channel waveforms and their information
        """
        self.waveform_names = []
        self.waveforms = []
        self.skew_trigdelay = 0.
        self._amplitude = 0.02
        self._offset = 0.

    #---------------------------------------------------------------------------
    #   set methods
    #---------------------------------------------------------------------------
    def set_waveforms(self, wf, **kwargs):
        """
        Set waveforms, waveform_names and waveform_counts
        (n_lines, n_sequence_elements)
        TODO: set markers
        """
        #### Handle kwargs first
        if "wf_names" in kwargs.keys():
            self._set_waveform_names(kwargs["wf_names"])
        else:
            # Construct local names
            n_sequence_elements = wf.shape[1]
            wf_names = ["C"+str(self.physical_channel)+"W"+str(i) for i in range(n_sequence_elements)]
            self._set_waveform_names(wf_names)

        if "wf_counts" in kwargs.keys():
            self._set_waveform_counts(kwargs["wf_counts"])
        else:
            # Construct local counts
            n_sequence_elements = wf.shape[1]
            wf_counts = [1] * n_sequence_elements
            self._set_waveform_counts(wf_counts)

        self._set_waveforms(wf)

    def set_amplitude(self, amplitude):
        """
        """
        self._amplitude = amplitude

    def set_offset(self, offset):
        """
        """
        self._offset = offset

    def _set_waveforms(self, wf):
        """
        Set waveforms
        """
        self.waveforms = wf

    def _set_waveform_names(self, wf_names):
        """
        Set waveform_names
        """
        self.waveform_names = wf_names

    def _set_waveform_counts(self, wf_counts):
        """
        Set waveform_counts
        """
        self.waveform_counts = wf_counts

    #---------------------------------------------------------------------------
    #   append/extend methods
    #---------------------------------------------------------------------------
    def append_waveforms(self, wf, wf_names, wf_counts):
        """
        Set waveform_names and waveforms
        TODO: set markers
        """
        self._append_waveforms(wf)
        self._append_waveform_names(wf_names)
        self._append_waveform_counts(wf_counts)

    def _append_waveforms(self, wf):
        """
        Append waveforms
        """
        if isinstance(wf, list):
            self.waveforms.extend(wf)
        else:
            self.waveforms.append(wf)

    def _append_waveform_names(self, wf_names):
        """
        Append waveform_names
        """
        if isinstance(wf_names, list):
            self.waveform_names.extend(wf_names)
        else:
            self.waveform_names.append(wf_names)

    def _append_waveform_counts(self, wf_counts):
        """
        Append waveform_names
        """
        if isinstance(wf_counts, list):
            self.waveform_names.extend(wf_counts)
        else:
            self.waveform_names.append(wf_counts)

    #---------------------------------------------------------------------------
    #   reduce methods
    #---------------------------------------------------------------------------
    def _reduce_waveforms(self):
        """
        If authorized, compare consecutive waveforms. If equal, delete the
        second one and increment the count number of the first.
        """

        if self.runtype.isproperty("awg_use_reduced_wfs"):
            if self.runtype.get("awg_use_reduced_wfs"):
                if len(self.waveforms)>1:
                    reduced_wfs = []
                    reduced_wf_names = []
                    reduced_wf_counts = []

                    # current_wf = self.waveforms[0]
                    # for i, current_wf in enumerate(self.waveforms[1:]):
                    #     while

    #---------------------------------------------------------------------------
    #   get methods
    #---------------------------------------------------------------------------
    def get_waveforms(self):
        """
        Get waveform_names and waveforms
        """
        return self.waveforms, self.waveform_names
        # if not self.are_waveforms_reduced:
        #     self._reduce_waveforms()
        # return self.waveforms, self.waveform_names, self.waveform_counts


    def get_amplitude(self):
        """
        """
        return self._amplitude

    def get_offset(self):
        """
        """
        return self._offset

    def get_physical_channel(self):
        return self.physical_channel

    def get_logical_name(Self):
        return self.logical_name

    def get_RFline(self):
        return self.RFline

    def get_triggering_delay(self):
        return self.triggering_delay

    def get_marker1_Vlow(self):
        return self.marker1_Vlow

    def get_marker1_Vhigh(self):
        return self.marker1_Vhigh

    def get_marker1_delay(self):
        return self.marker1_delay

    def get_marker2_Vlow(self):
        return self.marker2_Vlow

    def get_marker2_Vhigh(self):
        return self.marker2_Vhigh

    def get_marker2_delay(self):
        return self.marker2_delay

    #---------------------------------------------------------------------------
    #   Config files
    #---------------------------------------------------------------------------
    def Export_Channel_config_file(self):
        channel = { "physical_channel": self.physical_channel,
                    "logical_name": self.logical_name,
                    "RFline":self.RFline}
        return channel


if __name__ == '__main__':
    # sion = SionAWG('192.168.1.117', 4000)
    # sion.test()
    sion = DRIVER_AWGs()

    awg1 = DRIVER_AWG5014('192.168.1.10', 4000, rank = "Master", awg_index = 0)
    awg1.add_channel(1, "awg_L-TL", RFline = 1)
    awg1.add_channel(2, "awg_B-BL", RFline = 2)
    awg1.add_channel(3, "awg_R-BR", RFline = 3)
    awg1.add_channel(4, "awg_T-TR", RFline = 4)
    sion.add_AWG(awg1)

    awg2 = DRIVER_AWG5014('192.168.1.11', 4000, rank = "Slave", awg_index = 1)
    awg2.add_channel(1, "awg_L-BL", RFline = 5)
    awg2.add_channel(2, "awg_B-BR", RFline = 6)
    awg2.add_channel(3, "awg_R-TR", RFline = 7)
    awg2.add_channel(4, "awg_T-TL", RFline = 8)
    sion.add_AWG(awg2)

    awg3 = DRIVER_AWG5014('192.168.1.12', 4040, rank = "Slave", awg_index = 2)
    awg3.add_channel(1, "awg_L", RFline = 9)
    awg3.add_channel(2, "awg_B", RFline = 10)
    awg3.add_channel(3, "awg_R", RFline = 11)
    awg3.add_channel(4, "awg_T", RFline = 12)
    sion.add_AWG(awg3)

    # sion.Export_AWGs_config_file(sv.PATH_SrvInstruments_folder + "SionAWGs_1.ini")
    # sion.Import_AWGs_config_file(sv.PATH_SrvInstruments_folder + "SionAWGs_1.ini")
    # sion.Export_AWGs_config_file(os.getcwd() + os.sep + "SionAWGs_2.ini")

    # sion.Import_AWGs_config_file(os.getcwd() + os.sep + "SionAWGs_1.ini")
