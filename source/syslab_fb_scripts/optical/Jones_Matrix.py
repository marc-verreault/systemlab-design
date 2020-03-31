"""
SystemLab-Design Version 20.01.r1
Functional block script: Jones Matrix
Version 1.0 (2 Dec 2019)

Refs:
1) https://spie.org/publications/fg05_p57-61_jones_matrix_calculus?SSO=1
"""
import numpy as np
import config

from scipy import constants # https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Jones Matrix'
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))   
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    iteration = settings['current_iteration'] #Current iteration loop for simulation    
    
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS========================================================='''
    # Load parameters from FB parameters table
    # Main amplifier parameters (header)
    j_xx = complex(parameters_input[0][1])
    j_xy = complex(parameters_input[1][1])
    j_yx = complex(parameters_input[2][1])
    j_yy = complex(parameters_input[3][1])
    
    '''==INPUT SIGNALS======================================================'''
    # Load optical group data from input port
    signal_type = input_signal_data[0][1]
    time_array = input_signal_data[0][3] # Sampled time array
    psd_array = input_signal_data[0][4] # Noise groups
    opt_channels = input_signal_data[0][5] #Optical channel list
    
    # Load frequency, jones vector, signal & noise field envelopes for each optical channel
    channels = len(opt_channels)
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    jones_vector_in = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2:
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector_in[ch] = opt_channels[ch][2]
        opt_field_rcv[ch] = opt_channels[ch][3]
        noise_field_rcv[ch] = opt_channels[ch][4]
    
    '''==CALCULATIONS=======================================================''' 
    jones_matrix = np.full([2, 2], 0 + 1j*0, dtype=complex)
    jones_matrix[0][0] = j_xx
    jones_matrix[0][1] = j_xy
    jones_matrix[1][0] = j_yx
    jones_matrix[1][1] = j_yy
    jones_vector_out = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2:
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    for ch in range(0, channels):
        jones_vector_out[ch] = np.matmul(jones_matrix, jones_vector_in[ch])
        if opt_field_rcv[ch].ndim == 2:
            if np.abs(jones_vector_in[ch, 0]) > 0:
                opt_field_out[ch, 0] = opt_field_rcv[ch, 0]*jones_vector_out[ch, 0]/jones_vector_in[ch, 0]
            else:
                opt_field_out[ch, 0] = opt_field_rcv[ch, 0] 
            if np.abs(jones_vector_in[ch, 1]) > 0:
                opt_field_out[ch, 1] = opt_field_rcv[ch, 1]*jones_vector_out[ch, 1]/jones_vector_in[ch, 1]
            else:
                opt_field_out[ch, 1] = opt_field_rcv[ch, 1] 
        else:
            opt_field_out[ch] = opt_field_rcv[ch] 
        noise_field_out[ch] = noise_field_rcv[ch]
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    jones_matrix_parameters = []
    jones_matrix_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    jones_matrix_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector_out[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
        
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels]], 
                 jones_matrix_parameters, jones_matrix_results)

