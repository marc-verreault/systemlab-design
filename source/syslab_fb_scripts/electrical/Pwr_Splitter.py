"""
1x2 Pwr Splitter module
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = '1x2 Pwr Splitter' 
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
    pwr_splitter_parameters = []
    
    '''==CALCULATIONS======================================================='''
    time = input_signal_data[0][4]
    qpsk_signal = input_signal_data[0][5]
    qpsk_noise = input_signal_data[0][6]
    
    qpsk_sig_out = np.array(n, dtype = float) 
    qpsk_noise_out = np.array(n, dtype = float)
    
    qpsk_sig_out = np.multiply(qpsk_signal, 1/np.sqrt(2))
    qpsk_noise_out = np.multiply(qpsk_noise, 1/np.sqrt(2))
  
    '''==RESULTS============================================================'''
    pwr_splitter_results = []

    return ([[2, sig_type_out, carrier, fs, time, qpsk_sig_out,  qpsk_noise_out],
            [3, sig_type_out, carrier, fs, time, qpsk_sig_out,  qpsk_noise_out]], 
            pwr_splitter_parameters, pwr_splitter_results)