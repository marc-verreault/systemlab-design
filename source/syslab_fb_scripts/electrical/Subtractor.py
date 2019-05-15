"""
Subtractor module
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Subtractor' 
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
    subtractor_parameters = []
    
    '''==CALCULATIONS======================================================='''
    time = input_signal_data[0][4]
    e_signal_p1 = input_signal_data[0][5]
    e_noise_p1 = input_signal_data[0][6]
    e_signal_p2 = input_signal_data[1][5]
    e_noise_p2 = input_signal_data[1][6]
    
    e_sig_out = np.array(n, dtype = float) 
    e_noise_out = np.array(n, dtype = float) 
    
    e_sig_out = np.subtract(e_signal_p1, e_signal_p2)
    e_noise_out = np.subtract(e_noise_p1, e_noise_p2)
  
    '''==RESULTS============================================================'''
    subtractor_results = []

    return ([[3, sig_type_out, carrier, fs, time, e_sig_out, e_noise_out]], 
            subtractor_parameters, subtractor_results)