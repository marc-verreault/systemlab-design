"""
PRBS BinarySource
"""

import numpy as np
import config

'''
Signal formats:
Electrical: portID, signal_type, carrier, sample_rate, time_array, 
amplitude_array, noise_array
Optical: portID, signal_type, wave_channel, jones_matrix, sample_rate, 
time_array, envelope_array, psd_array
Digital: portID, signal_type, symbol_rate, bit_rate, order, time_array, 
discrete_array
'''

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Binary Source'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    time_win = settings['time_window']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(i))
        config.app.processEvents()
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==INPUT PARAMETERS==================================================='''
    bit_rate = 10e9
    symbol_rate = 10e9
    order = 1
    signal_type = 'Digital'
    sequence_type = 'random' #other choice is 'defined'
    defined_sequence = '001001'
    binary_seq_length = int(round(bit_rate*time_win))

    '''==CALCULATIONS======================================================='''
    time_array = np.linspace(0, time_win, n)
    seq_binary = np.random.randint(2, size=binary_seq_length)
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    #Parameters table
    signal_gen_parameters = []
  
    '''==RESULTS============================================================'''
    signal_gen_results = []
    res_seq = ['Bit sequence length', binary_seq_length, 'bits', ' ']
    signal_gen_results = [res_seq]

    return ([[1, signal_type, bit_rate, symbol_rate, order, time_array, seq_binary], 
            [2, signal_type, bit_rate, symbol_rate, order, time_array, seq_binary]],
            signal_gen_parameters, signal_gen_results)




