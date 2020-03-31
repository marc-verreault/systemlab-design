"""
SystemLab-Design Version 20.01.r1
PRBS (Binary source)
Version 1.0 (19.02 23 Feb 2019)
Version 2.0 (8-Nov-19)
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'PRBS Gen'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time_win = settings['time_window']
    #symbol_rate = settings['symbol_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    bit_rate = float(parameters_input[0][1]) #Bit rate (b/s)
    seq_type = str(parameters_input[1][1])
    seq_defined = parameters_input[2][1]    
    #Additional parameters
    signal_type = 'Digital'
    order = 1
    symbol_rate = bit_rate/order
    
    '''==CALCULATIONS======================================================='''
    binary_seq_length = int(round(bit_rate*time_win))
    time_array = np.linspace(0, time_win, n)
    
    if seq_type == 'PRBS':
        seq_binary = np.random.randint(2, size=binary_seq_length)
    else:        
        seq = np.fromstring(seq_defined, dtype=int, sep=',')
        seq_binary = np.tile(seq, round(binary_seq_length/np.size(seq)))
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    prbs_parameters = []
    prbs_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    prbs_results = []
    res_seq = ['Bit sequence length', binary_seq_length, 'bits', ' ']    
    prbs_results = [res_seq]
    
    return ([[1, signal_type, symbol_rate, bit_rate, order, time_array, seq_binary],
                [2, signal_type, symbol_rate, bit_rate, order, time_array, seq_binary]],
                prbs_parameters, prbs_results)




