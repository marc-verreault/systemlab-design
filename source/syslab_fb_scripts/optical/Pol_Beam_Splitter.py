"""
SystemLab-Design Version 20.01.r1
Functional block script: Polarization Beam Splitter
Version 1.0 (2 Dec 2019)

Refs:
1) https://spie.org/publications/fg05_p57-61_jones_matrix_calculus?SSO=1
"""
import numpy as np
import config

from scipy import constants # https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Polarization Beam Splitter'
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
    
    '''==INPUT PARAMETERS==================================================='''
    
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
    jones_matrix_x_pol = np.full([2, 2], 0 + 1j*0, dtype=complex)
    jones_matrix_x_pol[0][0] = 1 + 1j*0
    jones_matrix_y_pol = np.full([2, 2], 0 + 1j*0, dtype=complex)
    jones_matrix_y_pol[1][1] = 1 + 1j*0
    jones_vector_out_x = np.full([channels, 2], 0 + 1j*0, dtype=complex)
    jones_vector_out_y = np.full([channels, 2], 0 + 1j*0, dtype=complex)
    if opt_channels[0][3].ndim == 2:
        opt_field_out_x = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
        opt_field_out_y = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_out_x = np.full([channels, n], 0 + 1j*0, dtype=complex) 
        opt_field_out_y = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out_x = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out_y = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    for ch in range(0, channels):
        jones_vector_out_x[ch] = np.matmul(jones_matrix_x_pol, jones_vector_in[ch])
        jones_vector_out_y[ch] = np.matmul(jones_matrix_y_pol, jones_vector_in[ch])
        if opt_field_rcv[ch].ndim == 2:
            opt_field_out_x[ch, 0] = opt_field_rcv[ch, 0] 
            opt_field_out_y[ch, 1] = opt_field_rcv[ch, 1] 
        else:
            opt_field_out_x[ch] = opt_field_rcv[ch] 
            opt_field_out_y[ch] = opt_field_rcv[ch] 
        noise_field_out_x[ch] = noise_field_rcv[ch]
        noise_field_out_y[ch] = noise_field_rcv[ch]
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    pbs_parameters = []
    pbs_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    pbs_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels_x = []
    optical_channels_y = []
    for ch in range(0, channels):
        opt_ch_x = [int(wave_key[ch]), wave_freq[ch], jones_vector_out_x[ch], 
                           opt_field_out_x[ch], noise_field_out_x[ch]]
        optical_channels_x.append(opt_ch_x)
        opt_ch_y = [int(wave_key[ch]), wave_freq[ch], jones_vector_out_y[ch], 
                           opt_field_out_y[ch], noise_field_out_y[ch]]
        optical_channels_y.append(opt_ch_y)
        
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels_x],
                 [3, signal_type, fs, time_array, psd_array, optical_channels_y]], 
                pbs_parameters, pbs_results)

