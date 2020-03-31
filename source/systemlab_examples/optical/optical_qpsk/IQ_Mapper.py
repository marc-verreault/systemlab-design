"""
I_Q_Generator
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config
import project_optical_qpsk as project

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
    N = 2
    diff_encoding = int(parameters_input[1][1]) # Enable differential encoding
    
    '''==CALCULATIONS=========================================================='''
    bit_rate = input_signal_data[0][3]
    binary_input = input_signal_data[0][6]
    time_array = input_signal_data[0][5]  
    binary_seq_length = np.size(binary_input)
    samples_per_bit = int(round(fs/bit_rate))
    
    #Create I and Q symbol arrays
    symbol_rate = 25e9
    n_symbols = int(round(binary_seq_length/int(N)))
    bit_groups = np.reshape(binary_input, (n_symbols, int(N)))
    iq_symbols = np.full(n_symbols, 0 + 0j)

    # Symbol map (QPSK)
    # Gray mapping (CCW motion)
    sym_map = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    # IQ map (QPSK)
    # pi/4 (45 deg), 3*pi/4 (135 deg), 5*pi/4 (225 deg), 7*pi/4 (315 deg)
    iq_map = np.array([1.0+1.0j, -1.0+1.0j, -1.0-1.0j, 1.0-1.0j]) 
    hyp = np.abs(iq_map[0])
    # Map symbol groups to IQ constellation
    for g in range(0, n_symbols):
        bit_groups[g].tolist()
        if np.all(bit_groups[g] == sym_map[0]):
            iq_symbols[g]= iq_map[0]
        elif np.all(bit_groups[g] == sym_map[1]):
            iq_symbols[g]= iq_map[1]
        elif np.all(bit_groups[g] == sym_map[2]):
            iq_symbols[g]= iq_map[2]
        else:
            iq_symbols[g]= iq_map[3]
        
    # Apply differential encoding
    # REF 1: https://en.wikipedia.org/wiki/Differential_coding
    # REF 2: http://staff.ustc.edu.cn/~jingxi/Lecture%209_10.pdf
    if diff_encoding == 2:
        for g in range(1, n_symbols):
            ph_abs_previous = np.angle(iq_symbols[g-1])
            if ph_abs_previous < 0:
                 ph_abs_previous += 2*np.pi
            ph_abs_current = np.angle(iq_symbols[g])
            if ph_abs_current < 0:
                 ph_abs_current += 2*np.pi
            # Modulo 2 addition + rotation of pi/4 (to set to original constellation layout)
            ph_encoded = np.mod((ph_abs_previous + ph_abs_current + np.pi/4), 2*np.pi) 
            x = hyp*np.cos(ph_encoded)
            y = hyp*np.sin(ph_encoded)
            iq_symbols[g] = x + 1j*y

    '''==OUTPUT PARAMETERS LIST============================================='''
    IQ_parameters = []
    IQ_parameters = parameters_input 
    
    # Add bit group data to project file
    project.sym_ref_i = np.real(iq_symbols)
    project.sym_ref_q = np.imag(iq_symbols)
    
    '''==RESULTS==============================================================='''
    IQ_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
        
    return ([[2, signal_type, symbol_rate, bit_rate, N, time_array, np.real(iq_symbols)],
             [3, signal_type, symbol_rate, bit_rate, N, time_array, np.imag(iq_symbols)]], 
            IQ_parameters, IQ_results)

