"""
Adder module
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Adder' 
    n = settings['num_samples']
    n = int(round(n))
    iteration= settings['current_iteration']
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
    
    if config.sim_data_activate == True:    
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    adder_parameters = []
    
    '''==CALCULATIONS======================================================='''
    time = input_signal_data[0][4]
    port_1_signal = input_signal_data[0][5]
    port_1_noise = input_signal_data[0][6]
    port_2_signal = input_signal_data[1][5]
    port_2_noise = input_signal_data[1][6]
    
    sig_out = np.array(n, dtype = float) 
    noise_out = np.array(n, dtype = float) 
    
    sig_out = np.add(port_1_signal, port_2_signal)
    noise_out = np.add(port_1_noise, port_2_noise)
    
  
    '''==RESULTS============================================================'''
    adder_results = []

    #the returned signals will be allocated to the output port (portID 1)
    return ([[3, sig_type_out, carrier, fs, time, sig_out, noise_out]],
            adder_parameters, adder_results)