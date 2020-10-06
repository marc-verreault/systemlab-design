"""
2Bit Serial to Parallel Converter
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config

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
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
    bit_rate = float(parameters_input[0][1])
    order = 1
    symbol_rate = bit_rate/order
    signal_type = 'Digital'
    binary_seq_length = int(round(bit_rate*time_win))
    #Parameters table
    signal_gen_parameters = []
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    sp_parameters = []
    sp_parameters = parameters_input
    
    '''==CALCULATIONS======================================================='''   
    binary = input_signal_data[0][6]
    time = input_signal_data[0][5]    
    binary_seq_odd_even = int(round(binary_seq_length/2))
    binary_even = np.zeros(binary_seq_odd_even)
    binary_odd = np.zeros(binary_seq_odd_even)
    
    for i in range(0, binary_seq_length):  
        if i % 2 == 0:
            binary_even[int(round(i/2))] = binary[i]
        else:
            binary_odd[int(round((i-1)/2))] = binary[i]
  
    '''==RESULTS============================================================'''
    sp_results = []
    bin_even = ['Bit sequence length - Even', binary_seq_length/2, 'bits', ' ']
    bin_odd = ['Bit sequence length - Odd', binary_seq_length/2, 'bits', ' ']    
    sp_results = [bin_even, bin_odd]
        
    return  ([[2, signal_type, symbol_rate, bit_rate, order, time,
              binary_even], [3, signal_type, symbol_rate, bit_rate, order, 
              time, binary_odd]], sp_parameters, sp_results)








