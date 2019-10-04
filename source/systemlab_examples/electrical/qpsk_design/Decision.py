"""
Decision module
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Decision'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(i))
        config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==INPUT PARAMETERS==================================================='''
    bit_rate_input = input_signal_data[0][3]
    carrier = 0
    
    #Parameters table
    decision_parameters = []
    
    '''==CALCULATIONS======================================================='''
    
    bit_rate = 10e9
    symbol_rate = 5e9
    order = 2
   
    samples_per_bit = int(fs/bit_rate)
    samples_per_symbol = int(fs/symbol_rate)
    n_sym = int(round(n/samples_per_symbol))
    
    integrated_sig_in = input_signal_data[0][5]
    time = input_signal_data[0][4]
    noise = input_signal_data[0][6]
    
    digital_out = np.array([], dtype = int)
    
    for sym in range(1, n_sym+1):
        decision_sample = integrated_sig_in[int(sym*samples_per_symbol) - 1]
        if decision_sample >= 0:
            digital_out = np.append(digital_out, 1)
        else:
            digital_out = np.append(digital_out, 0)

    '''==RESULTS============================================================'''
    decision_results = []

    return ([[2, 'Digital', symbol_rate, bit_rate, order, time, digital_out], 
            [3, 'Electrical', 0, fs, time, integrated_sig_in, noise],
            [4, 'Digital', symbol_rate, bit_rate, order, time, digital_out]],
            decision_parameters, decision_results)



