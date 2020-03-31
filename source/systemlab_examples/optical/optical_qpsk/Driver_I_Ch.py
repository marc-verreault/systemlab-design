"""
Driver I Ch module
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    '''==PROJECT SETTINGS======================================================'''
    module_name = 'Driver I Ch'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate'] 

    config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))

    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    rf_upper = float(parameters_input[0][1])
    bias_upper = float(parameters_input[1][1])
    rf_lower = float(parameters_input[2][1])
    bias_lower = float(parameters_input[3][1])
    #Additional parameters
    symbol_rate_input = input_signal_data[0][2]
    print(symbol_rate_input)
    signal_type = 'Electrical'
    carrier_freq = 0
    
    '''==INPUT SIGNALS======================================================'''
    sym_i_input = input_signal_data[0][6]
    time_array = input_signal_data[0][5]
    
    '''==CALCULATIONS=======================================================
    '''
    symbol_seq_length = np.size(sym_i_input)
    samples_per_symbol = int(round(fs/symbol_rate_input))
    print(samples_per_symbol)
    v1_out = np.zeros(n)
    v2_out = np.zeros(n) 
    noise_v1 = np.zeros(n)
    noise_v2 = np.zeros(n)
    
    # Ref: Coherent Optical Systems, Lecture Notes, Photonics Communications Research Lab, 
    # National Technical University of Athens (NTUA)
    # http://www.photonics.ntua.gr/OptikaDiktyaEpikoinwnias/Lecture_4_CoherentOptical_DSP.pdf
    # Accessed: 24 Apr 2019
    
    for sym in range(0, symbol_seq_length):
        signal_v1 = (sym_i_input[sym] * rf_upper) + bias_upper
        signal_v2 = (sym_i_input[sym] * rf_lower) + bias_lower
        start_index = int(sym*int(samples_per_symbol))
        v1_out[start_index : start_index+samples_per_symbol] = signal_v1
        v2_out[start_index : start_index+samples_per_symbol] = signal_v2
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    driver_i_parameters = []
    driver_i_parameters = parameters_input #No changes were made to parameters
    
    '''==RESULTS============================================================'''
    driver_i_results = []

    '''==RETURN (Output Signals, Parameters, Results)======================='''
    return ([[2, signal_type, carrier_freq, fs, time_array, v1_out, noise_v1],
             [3, signal_type, carrier_freq, fs, time_array, v2_out, noise_v2]], 
            driver_i_parameters, driver_i_results)

