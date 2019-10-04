"""
Driver I Ch module
"""

import numpy as np
import config
import importlib

def run(input_signal_data, parameters_input, settings):
    '''==PROJECT SETTINGS======================================================'''
    module_name = 'Driver I Ch'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate'] 

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))

    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    pp_amplitude = float(parameters_input[0][1])
    bias = float(parameters_input[1][1])
    #Additional parameters
    symbol_rate_input = input_signal_data[0][2]
    signal_type = 'Electrical'
    carrier_freq = 0
    
    '''==INPUT SIGNALS======================================================'''
    sym_i_input = input_signal_data[0][6]
    time_array = input_signal_data[0][5]
    
    '''==CALCULATIONS======================================================='''
    symbol_seq_length = np.size(sym_i_input)
    samples_per_symbol = int(round(fs/symbol_rate_input))
    
    v1_out = np.zeros(n, )
    v2_out = np.zeros(n, )    
            
    for sig in range(0, symbol_seq_length):
        signal_v1 =  pp_amplitude + bias
        signal_v2 =  -(pp_amplitude + bias)
        if sym_i_input[sig] == 0:
            signal_v1 =  bias
            signal_v2 =  -bias
        start_index = int(sig*int(samples_per_symbol))
        v1_out[start_index : start_index+samples_per_symbol] = signal_v1
        v2_out[start_index : start_index+samples_per_symbol] = signal_v2

    noise_v1 = np.zeros(n)
    noise_v2 = np.zeros(n)
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    driver_i_parameters = []
    driver_i_parameters = parameters_input #No changes were made to parameters
    
    '''==RESULTS============================================================'''
    driver_i_results = []

    '''==RETURN (Output Signals, Parameters, Results)======================='''
    return ([[2, signal_type, carrier_freq, fs, time_array, v1_out, noise_v1],
                [3, signal_type, carrier_freq, fs, time_array, v2_out, noise_v2]], 
                driver_i_parameters, driver_i_results)


