from Stab_diag_Cavities import StabilityDiagram


##########################
###	 CHOOSE FILE NAME
##########################
folder = 'D:\\BaptisteData\\BM13\\CD1'
prefix = 'stab_'
Map = StabilityDiagram(folder,prefix)

##########################
###	 TIMINGS 			
##########################
Map.initial_wait = 10.   # ms before everything
Map.ms_per_point = 10.     # integration time (fastseq divider)
Map.step_wait = 1.         # ms wait after every fastseq

##########################
###	 INITIAL VALUES
##########################
### SAFETY
Map.init_val['0:7'] = -0.1
Map.init_val['1:7'] = -0.1
Map.init_val['2:7'] = -0.1
Map.init_val['3:7'] = -0.1
Map.init_val['4:7'] = -0.1

### BIAS
Map.init_val['2:0'] = 0.217

### IDTs
Map.init_val['2:3'] = -0.
Map.init_val['2:4'] = -0.

### TOP GATES
Map.init_val['0:0'] = -0.
Map.init_val['0:1'] = -0.
Map.init_val['0:2'] = -0.
Map.init_val['0:3'] = -0.
Map.init_val['0:4'] = -0.
Map.init_val['0:5'] = -0.
Map.init_val['0:6'] = -0.

### BOTTOM GATES
Map.init_val['1:0'] = -0.
Map.init_val['1:1'] = -0.
Map.init_val['1:2'] = -0.
Map.init_val['1:3'] = -0.
Map.init_val['1:4'] = -0.
Map.init_val['1:5'] = -0.
Map.init_val['1:6'] = -0.

### HORZ GATES
Map.init_val['2:1'] = -1.8
Map.init_val['2:2'] = -1.8

##########################
###	 MAP
##########################
Map.sweep_dim = [201,5]
Map.ramp_DAC('0:4',-0.5,-1.5,0)
Map.ramp_DAC('2:2',-1.2,-1.2,1)
#Map.ramp_DAC('0:5',-1.,-1.6,1)
#Map.ramp_DAC('0:3',-1.5,-1.5,1)
#Map.ramp_DAC('0:0',0.,0.,1)
#Map.ramp_DAC('2:1',0.,-1.8,0)


#Map.add_wait('wait_bg',0,10000,1) # (index,ms,axis) wait n ms at index for given axis


Map.ADC.uint64s[7] = Map.sweep_dim[0]
Map.build_fastramp()
Map.build_sweep()
Map.build_files()
