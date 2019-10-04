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
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
   
    '''==INPUT PARAMETERS=================================================================
    '''
    bit_rate = float(parameters_input[0][1])
    order = 2
    symbol_rate = bit_rate/2
    signal_type = 'Digital'
    
    samples_per_symbol = int(fs/symbol_rate)
    n_sym = int(round(n/samples_per_symbol))
    binary_seq_length = int(round(bit_rate*time_win))
    
    #Parameters table
    signal_gen_parameters = []
    signal_gen_parameters = parameters_input
    
    '''==CALCULATIONS=====================================================================
    '''
    i_sym = input_signal_data[0][6]
    q_sym = input_signal_data[1][6]
    time = input_signal_data[0][5]
    binary_received = np.zeros(binary_seq_length)
    
    for i in range(0, n_sym):
        if [i_sym[i], q_sym[i]] == [1, 1]:
            binary_received[int(2*i)] = 1
            binary_received[int(2*i+1)] = 1
        elif [i_sym[i], q_sym[i]] == [-1, 1]:
            binary_received[int(2*i)] = 0
            binary_received[int(2*i+1)] = 1
        elif [i_sym[i], q_sym[i]] == [1, -1]:
            binary_received[int(2*i)] = 1
            binary_received[int(2*i+1)] = 0
        else:
            binary_received[int(2*i)] = 0
            binary_received[int(2*i+1)] = 0
  
    '''==RESULTS==========================================================================
    '''
    signal_gen_results = []
        
    return ([[3, signal_type, symbol_rate, bit_rate, order, time,
              binary_received]], signal_gen_parameters, signal_gen_results)





