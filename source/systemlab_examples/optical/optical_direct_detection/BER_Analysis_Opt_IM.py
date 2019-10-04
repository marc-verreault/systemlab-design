"""
BER Analysis module
Version 1.0 (19.02 23 Feb 2019)
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'BER Analysis'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    ber_parameters = []
    
    '''==CALCULATIONS======================================================='''
    binary_reference = input_signal_data[0][6]
    binary_recovered = input_signal_data[1][6]
    binary_seq_length = np.size(binary_reference)
    
    # Calculate BER
    err_count = 0
    for i in range(0, binary_seq_length):
        if binary_reference[i] != binary_recovered[i]:
            err_count += 1
    ber = err_count/binary_seq_length   
  
    '''==RESULTS============================================================'''
    ber_results = []
    res_ber = ['Bit error rate', ber, ' ', ' ', False]
    num_errors = ['Bit errors', err_count, ' ', ' ', False]
    ber_results = [res_ber, num_errors]

    return ([], ber_parameters, ber_results)