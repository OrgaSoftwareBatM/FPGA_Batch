# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 09:44:12 2018

@author: manip.batm
"""
def timing_correction(t):
    return 1.054*t+0.00155
    
def FPGA_timing_calculator(sequence,ms_per_DAC=0.01617):
    total = 0
    for s in sequence:
        if s[0] in ['Trigger','Jump']:
            continue
        elif s[0] == 'Timing':
            total += timing_correction(s[1])
        else:
            total += ms_per_DAC
    return total
    
def total_seq_time(sequence,Njumps=0,ms_per_DAC=0.01617):
    i = 0
    jumped = 0
    total = 0
    while i<len(sequence) and jumped<=Njumps:
        s = sequence[i]
        if s[0] == 'Trigger':
            pass
        elif s[0] == 'Jump':
            i = s[1]
            jumped += 1
            continue
        elif s[0] == 'Timing':
            total += timing_correction(s[1])
        else:
            total += ms_per_DAC
        i += 1
    return total
    
def segment_timing(sequence,ms_per_DAC=0.01617):
    ADC_trigger = min([i for i,seq in enumerate(sequence) if seq[0]=='Trigger' and seq[1][1]=='0'])
    jump_index = [s[0] for s in sequence].index('Jump')
    jump_to = sequence[jump_index][1]
    last_timing_index = max([i for i,seq in enumerate(sequence[:jump_index]) if seq[0]=='Timing'])
    
    t_init = FPGA_timing_calculator(sequence[ADC_trigger:last_timing_index],ms_per_DAC)
    t_segment = FPGA_timing_calculator(sequence[jump_to:jump_index],ms_per_DAC)
    t_read = timing_correction(sequence[last_timing_index][1])
#    print (t_init,t_segment,t_read)
    return t_init,t_segment,t_read

#sequence = []
#sequence.append(['Trigger','1111'])
#sequence.append(['Timing',0.1])
#sequence.append(['Trigger','1010'])
#sequence.append(['LH3',0.27])
#sequence.append(['LH2',0.08])
#sequence.append(['Timing',0.1])  # load 2 electrons
#sequence.append(['LH3',0.15])
#sequence.append(['LH2',0.1])
#sequence.append(['Trigger','1011'])
#sequence.append(['Timing',10.]) # Meas 1
#sequence.append(['Trigger','1010'])
#sequence.append(['LH2',-0.05])    # Metastable
#sequence.append(['LH1',0.])
#sequence.append(['LH3',0.3])
#sequence.append(['Timing',0.1])
#sequence.append(['LH3',0.])
#sequence.append(['LH1',0.])
#sequence.append(['LH2',0.1])
#sequence.append(['Trigger','1011'])
#sequence.append(['Timing',10.]) # Meas 2
#sequence.append(['Trigger','1010'])
#sequence.append(['Jump',2])
#
#total_seq_time(sequence,Njumps=0,ms_per_DAC=0.01617)