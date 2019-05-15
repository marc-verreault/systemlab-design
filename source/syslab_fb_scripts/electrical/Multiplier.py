"""
Multiplier module
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Multiplier' 
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']
    sig_type_out = 'Electrical'
    carrier = 0

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    multiplier_parameters = []
    
    '''==CALCULATIONS======================================================='''
    time = input_signal_data[0][4]
    signal = input_signal_data[0][5]
    noise = input_signal_data[0][6]
    
    lo_signal = input_signal_data[1][5]
    lo_noise = input_signal_data[1][6]
    
    PSK_sig_out = np.array(n, dtype = float)
    PSK_noise_out = np.array(n, dtype = float)
    
    PSK_sig_out = np.multiply(signal, lo_signal)
    PSK_noise_out = np.multiply(noise, lo_signal)
  
    '''==RESULTS============================================================'''
    multiplier_results = []

    return ([[3, sig_type_out, carrier, fs, time, PSK_sig_out, PSK_noise_out]], 
            multiplier_parameters, multiplier_results)