"""
2Bit Serial to Parallel Converter
Version 1.0 (19.02 23 Feb 2019)
"""

import numpy as np
import config
import project_qpsk as project

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = '2 bit S-P Conv' 
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
    
    '''==INPUT PARAMETERS==================================================='''
    bit_rate_input = 10e9
    bit_rate_output = 5e9
    symbol_rate = 5e9
    order = 2
    signal_type = 'Digital'
    binary_seq_length = int(round(bit_rate_input*time_win))
    #Parameters table
    signal_gen_parameters = []
    
    '''==CALCULATIONS======================================================='''
    
    binary = input_signal_data[0][6]
    time = input_signal_data[0][5]    
    
    binary_even = np.array([], dtype = int)
    binary_odd = np.array([], dtype = int)
    
    for i in range(0, binary_seq_length):  
        if i % 2 == 0:
            binary_even = np.append(binary_even, binary[i])
        else:
            binary_odd = np.append(binary_odd, binary[i])
  
    '''==RESULTS============================================================'''
    signal_gen_results = []
    bin_even = ['Bit sequence length - Even', binary_seq_length/2, 'bits', ' ']
    bin_odd = ['Bit sequence length - Odd', binary_seq_length/2, 'bits', ' ']    
    signal_gen_results = [bin_even, bin_odd]
    
    '''==DATA BOX UPDATES==================================================='''
    project.symbol_seq_odd = binary_odd
    project.symbol_seq_even = binary_even
        
    return  [[2, signal_type, symbol_rate, bit_rate_output, order, time,
              binary_even], [3, signal_type, symbol_rate, bit_rate_output, order, 
              time, binary_odd]], signal_gen_parameters, signal_gen_results









