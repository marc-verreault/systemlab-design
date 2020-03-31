"""
SystemLab-Design Version 20.01.r1
Comparator module

Refs/Background:
1) Wikipedia contributors. (2019, September 7). Comparator. In Wikipedia, The Free Encyclopedia.
Retrieved 16:49, October 2, 2019, from https://en.wikipedia.org/w/index.php?title=Comparator&oldid=914467902
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Comparator' 
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']
    f_sym = settings['symbol_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    
    '''==INPUT SIGNALS=======================================================
    '''
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    fs = input_signal_data[0][3]
    time_array = input_signal_data[0][4]
    sig_in_v_pos = input_signal_data[0][5]
    noise_in_v_pos = input_signal_data[0][6]
    sig_in_v_neg = input_signal_data[1][5]
    noise_in_v_neg = input_signal_data[1][6]
    
    '''==CALCULATIONS======================================================='''
    sig_in_v_pos += noise_in_v_pos
    sig_in_v_neg += noise_in_v_neg
    noise_out = np.zeros(n)
    sig_out = np.zeros(n)  
    
    for i in range(0, n):
        if sig_in_v_pos[i] > sig_in_v_neg[i]:
            sig_out[i] = 1.0
    
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    comparator_parameters = []
    comparator_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS============================================================'''
    comparator_results = []

    return ([[3, sig_type, carrier, fs, time_array, sig_out, noise_out]], 
            comparator_parameters, comparator_results)