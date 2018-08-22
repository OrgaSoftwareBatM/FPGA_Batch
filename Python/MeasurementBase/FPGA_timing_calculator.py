# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 09:44:12 2018

@author: manip.batm
"""
def timing_correction(t):
    return 1.05*t+0.00155
    
def FPGA_timing_calculator(sequence,ms_per_DAC=0.016):
    total = 0
    for s in sequence:
        if s[0] in ['Trigger','Jump']:
            continue
        elif s[0] == 'Timing':
            total += timing_correction(s[1])
        else:
            total += ms_per_DAC
    return total