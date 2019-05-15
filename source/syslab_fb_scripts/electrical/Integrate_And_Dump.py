"""
Integrate & Dump module
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'I&D'
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
    bit_rate = input_signal_data[0][3]
    carrier = 0    
    sig_type_out = 'Electrical'
    
    #Parameters table
    int_dump_parameters = []
    
    '''==CALCULATIONS======================================================='''    
    psk_sig_in = input_signal_data[0][5]
    psk_noise_in = input_signal_data[0][6]
    time = input_signal_data[0][4]
    
    bit_rate = 10e9
    symbol_rate = 5e9
   
    samples_per_bit = int(fs/bit_rate)
    samples_per_symbol = int(fs/symbol_rate)
    n_sym = int(round(n/samples_per_symbol))
    
    integrated_sig_out = np.zeros(n, )
    integrated_noise_out = np.zeros(n, )
    
    for s in range(0, n_sym):
        i = 0
        start_value = psk_sig_in[int(s*samples_per_symbol)]
        start_value_noise = psk_noise_in[int(s*samples_per_symbol)]
        while i < int(samples_per_symbol):
            integrated_sig_out[int(s*samples_per_symbol)+i] = (start_value 
                               + psk_sig_in[int(s*samples_per_symbol)+i])
            start_value = integrated_sig_out[int(s*samples_per_symbol)+i]
            
            integrated_noise_out[int(s*samples_per_symbol)+i] = (start_value_noise
                                 + psk_noise_in[int(s*samples_per_symbol)+i])
            start_value_noise = integrated_noise_out[int(s*samples_per_symbol)+i]
            i += 1
     
    '''==RESULTS============================================================'''
    int_dump_results = []
        
    return ([[2, sig_type_out, carrier, fs, time, integrated_sig_out, integrated_noise_out]],
                int_dump_parameters, int_dump_results)



