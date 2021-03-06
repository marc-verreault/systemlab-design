"""
Sine Generator module
Version 1.0 (19.02 23 Feb 2019)
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Sine Generator'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    freq = float(parameters_input[0][1]) #Hz
    signal_amp = float(parameters_input[1][1]) #Peak amplitude (crest-to-crest = 2*Peak amplitude)
    bias = float(parameters_input[2][1]) #
    
    carrier = freq
    sig_type = 'Electrical'
    
    #Parameters table
    signal_gen_parameters = []
    signal_gen_parameters = parameters_input
    
    '''==CALCULATIONS======================================================='''
    time_array = np.linspace(0, time, n)
    signal_array = signal_amp * np.sin(2*np.pi*freq*time_array) + bias
    noise_array = np.zeros(n)    
  
    '''==RESULTS============================================================'''
    signal_gen_results = []
    
    return ( [[1, sig_type, carrier, fs, time_array, signal_array, noise_array]], 
            signal_gen_parameters, signal_gen_results )



