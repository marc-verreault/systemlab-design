"""
I_Q_Generator
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS======================================================'''
    module_name = 'I-Q Gen'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate'] 

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
    signal_type = 'Digital'
    N = float(parameters_input[0][1])
    
    '''==CALCULATIONS=========================================================='''
    bit_rate = input_signal_data[0][3]
    binary_input = input_signal_data[0][6]
    time_array = input_signal_data[0][5]  
    binary_seq_length = np.size(binary_input)
    samples_per_bit = int(round(fs/bit_rate))
    
    #Create I and Q symbol arrays
    symbol_rate = bit_rate/N
    I = [-1, 1]
    Q = [-1, 1]
    num_symbols = int(round(binary_seq_length/int(N)))
    bit_groups = np.reshape(binary_input, (num_symbols, int(N)))
    print(bit_groups)
    i_symbols = np.zeros(num_symbols)
    q_symbols = np.zeros(num_symbols)  
    
    for g in range(0, num_symbols):
        bit_groups[g].tolist()
        if np.all(bit_groups[g] == [0, 0]):
            # -135 deg (5/4*pi)
            i_symbols[g]= I[0]
            q_symbols[g]= Q[0]
        elif np.all(bit_groups[g] == [0, 1]):
            # +135 deg (3/4*pi)
            i_symbols[g]= I[0]
            q_symbols[g]= Q[1]
        elif np.all(bit_groups[g] == [1, 0]):
            # -45 deg (7/4*pi)
            i_symbols[g]= I[1]
            q_symbols[g]= Q[0]
        else:
            # +45 deg (1/4*pi)
            i_symbols[g]= I[1]
            q_symbols[g]= Q[1]

    '''==OUTPUT PARAMETERS LIST============================================='''
    IQ_parameters = []
    IQ_parameters = parameters_input 
  
    '''==RESULTS==============================================================='''
    IQ_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
        
    return ([[2, signal_type, symbol_rate, bit_rate, N, time_array, i_symbols],
             [3, signal_type, symbol_rate, bit_rate, N, time_array, q_symbols]], 
            IQ_parameters, IQ_results)

