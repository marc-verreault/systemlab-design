"""
SystemLab-Design Version 20.01.r1
Functional block script: Optical attenuator
Version 2.0 (26 Sep 2019)
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Attenuator'
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
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    att = float(parameters_input[0][1]) #Attenuation (dB)
    
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
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector[ch] = opt_channels[ch][2]
        opt_field_rcv[ch, :] = opt_channels[ch][3]
        noise_field_rcv[ch, :] = opt_channels[ch][4]
    
    '''==CALCULATIONS======================================================='''       
    att_linear = np.power(10, -att/10)
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
    else: # Polarization format: Exy
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels):
        opt_field_out[ch] = opt_field_rcv[ch]*np.sqrt(att_linear)
        noise_field_out[ch] = noise_field_rcv[ch]*np.sqrt(att_linear)
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    att_parameters = []
    att_parameters = parameters_input
    
    '''==RESULTS============================================================'''
    att_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''      
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels]], 
                 att_parameters, att_results)

