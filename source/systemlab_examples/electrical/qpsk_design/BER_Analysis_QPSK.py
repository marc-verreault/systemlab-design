"""
BER Analysis module
"""

import numpy as np
import matplotlib.pyplot as plt
import config
import project_qpsk as project

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'BER Analysis'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    iterations = settings['iterations']
    time_win = settings['time_window']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
        config.app.processEvents()
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
    bit_rate = 10e9
    symbol_rate = 5e9
    order = 2
    signal_type = 'Digital'
    
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
    
    #Send update to data box (data_table_1)
    config.data_tables['qpsk_1'] = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['Binary sequence length', binary_seq_length, '0.2E', ' ']
    data_3 = ['Errored bits', err_count, '0.2E', ' ']
    data_4 = ['Bit error rate', ber, '0.2E', ' ']
    data_list = [data_1, data_2, data_3, data_4]
    config.data_tables['qpsk_1'].extend(data_list)
    
    # Add BER data to graph
    if iteration == 1:
        project.ber = []
    project.ber.append(ber)

    return ([], ber_parameters, ber_results)



