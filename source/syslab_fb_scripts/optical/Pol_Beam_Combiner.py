"""
SystemLab-Design Version 20.01.r1
Functional block script: Polarization Beam Combiner
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
    # Load optical group data from input X port (upper)
    signal_type = 'Optical'
    time_array = input_signal_data[0][3] # Sampled time array
    psd_array_p1 = input_signal_data[0][4] # Noise groups
    opt_channels_p1 = input_signal_data[0][5] #Optical channel list
    
    # Load frequency, jones vector, signal & noise field envelopes for each optical channel of X port
    channels_p1 = len(opt_channels_p1)
    wave_key_p1 = np.empty(channels_p1)
    wave_freq_p1 = np.empty(channels_p1)
    jones_vector_p1 = np.full([channels_p1, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels_p1[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv_p1 = np.full([channels_p1, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv_p1 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex)
    noise_field_rcv_p1 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels_p1): #Load wavelength channels
        wave_key_p1[ch] = opt_channels_p1[ch][0]
        wave_freq_p1[ch] = opt_channels_p1[ch][1]
        jones_vector_p1[ch] = opt_channels_p1[ch][2]
        opt_field_rcv_p1[ch] = opt_channels_p1[ch][3]
        noise_field_rcv_p1[ch] = opt_channels_p1[ch][4]
    
    # Load optical group data from Y port (lower)
    signal_type = 'Optical'
    time_array = input_signal_data[1][3] # Sampled time array
    psd_array_p2 = input_signal_data[1][4] # Noise groups
    opt_channels_p2 = input_signal_data[1][5] #Optical channel list

    # Load frequency, jones vector, signal & noise field envelopes for Y port (lower)
    channels_p2 = len(opt_channels_p2)
    wave_key_p2 = np.empty(channels_p2)
    wave_freq_p2 = np.empty(channels_p2)
    jones_vector_p2 = np.full([channels_p2, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels_p2[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv_p2 = np.full([channels_p2, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv_p2 = np.full([channels_p2, n], 0 + 1j*0, dtype=complex)
    noise_field_rcv_p2 = np.full([channels_p2, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels_p2): #Load wavelength channels
        wave_key_p2[ch] = opt_channels_p2[ch][0]
        wave_freq_p2[ch] = opt_channels_p2[ch][1]
        jones_vector_p2[ch] = opt_channels_p2[ch][2]
        opt_field_rcv_p2[ch] = opt_channels_p2[ch][3]
        noise_field_rcv_p2[ch] = opt_channels_p2[ch][4]
    
    '''==CALCULATIONS=======================================================''' 
    jones_vector_out_xy = np.full([channels_p1, 2], 0 + 1j*0, dtype=complex)
    if opt_channels_p1[0][3].ndim == 2:
        opt_field_out_xy = np.full([channels_p1, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_out_xy = np.full([channels_p1, n], 0 + 1j*0, dtype=complex) 
    noise_field_out_xy = np.full([channels_p1, n], 0 + 1j*0, dtype=complex)
    for ch in range(0, channels_p1):
        jones_vector_out_xy[ch] = [jones_vector_p1[ch, 0], jones_vector_p2[ch, 1]]
        #Normalization
        norm_factor = np.sqrt(np.abs(jones_vector_p1[ch, 0])**2 + np.abs(jones_vector_p2[ch, 1])**2)
        jones_vector_out_xy[ch] /= norm_factor
        
        if opt_field_rcv_p1[ch].ndim == 2:
            opt_field_out_xy[ch, 0] = opt_field_rcv_p1[ch, 0] 
            opt_field_out_xy[ch, 1] = opt_field_rcv_p2[ch, 1] 
        else:
            opt_field_out_xy[ch] = (jones_vector_p1[ch, 0]*opt_field_rcv_p1[ch] 
                                                + jones_vector_p2[ch, 1]*opt_field_rcv_p2[ch])
        noise_field_out_xy[ch] = jones_vector_out_xy[ch, 0]*noise_field_rcv_p1[ch]
        noise_field_out_xy[ch] +=jones_vector_out_xy[ch, 1]*noise_field_rcv_p2[ch]
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    pbc_parameters = []
    pbc_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    pbc_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels_xy = []
    for ch in range(0, channels_p1):
        opt_ch_xy = [int(wave_key_p1[ch]), wave_freq_p1[ch], jones_vector_out_xy[ch], 
                             opt_field_out_xy[ch], noise_field_out_xy[ch]]
        optical_channels_xy.append(opt_ch_xy)
        
    return ([[3, signal_type, fs, time_array, psd_array_p1, optical_channels_xy]], 
                pbc_parameters, pbc_results)

