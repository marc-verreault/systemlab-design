"""
Decision module
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Decision Circuit'
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
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS===================================================
    '''
    decision_th = float(parameters_input[0][1])
    decision_pt = float(parameters_input[1][1])
    dc_block = int(parameters_input[2][1])

    '''==CALCULATIONS=======================================================
    '''
    order = 1
    bit_rate = f_sym*order
    samples_per_sym = int(fs/f_sym)
    n_sym = int(round(n/samples_per_sym))
    time = input_signal_data[0][4]
    sampled_sig_in = input_signal_data[0][5]
    noise = input_signal_data[0][6]
    
    digital_out = np.zeros(n_sym, dtype = int)
    
    #DC block (if enabled)
    if dc_block == 2:
        sig_avg = np.mean(np.real(sampled_sig_in))
        sampled_sig_in = sampled_sig_in - sig_avg
    
    for sym in range(0, n_sym):
        sampling_index = int(sym*samples_per_sym + round(samples_per_sym*decision_pt))
        decision_sample = sampled_sig_in[sampling_index]
        if decision_sample >= decision_th:
            digital_out[sym] = 1
            
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    decision_parameters = []
    decision_parameters = parameters_input

    '''==RESULTS============================================================'''
    decision_results = []

    return ([[2, 'Digital', f_sym, bit_rate, order, time, digital_out]],
                decision_parameters, decision_results)



