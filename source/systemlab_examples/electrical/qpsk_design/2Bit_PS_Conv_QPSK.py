"""
2Bit Parallel to Serial Converter
Version 1.0 (19.02 23 Feb 2019)
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = '2 bit P-S Conv' 
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time_win = settings['time_window']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
        config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
   
    '''==INPUT PARAMETERS=================================================================
    '''
    bit_rate = 10e9
    symbol_rate = 5e9
    order = 2
    signal_type = 'Digital'
    binary_seq_length = int(round(bit_rate*time_win))
    #Parameters table
    signal_gen_parameters = []
    
    '''==CALCULATIONS=====================================================================
    '''
    binary_even = input_signal_data[0][6]
    binary_odd = input_signal_data[1][6]
    time = input_signal_data[0][5]
    
    binary_received = np.array([], dtype = int)
    
    for i in range(0, binary_seq_length):
        if i % 2 == 0:
            binary_received = np.append(binary_received, binary_even[int((i/2))])
        else:
            binary_received = np.append(binary_received, binary_odd[int((i/2))])
  
    '''==RESULTS==========================================================================
    '''
    signal_gen_results = []
        
    return ([[1, signal_type, symbol_rate, bit_rate, order, time,
              binary_received]], signal_gen_parameters, signal_gen_results)





