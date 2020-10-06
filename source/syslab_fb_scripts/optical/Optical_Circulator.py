"""
SystemLab-Design Version 20.01.r1
Optical Circulator (Bi-directional)
Version 1.0 (11 Sep 2019)

References:
1) https://www.thorlabs.de/newgrouppage9.cfm?Objectgroup_id=373
"""

import numpy as np
import config
from scipy import constants

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Circulator'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']

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
    # Load parameters from FB parameters table (format: Parameter name(0), Value(1), Units(2), Notes(3))
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    #Port 1 (ID 1 - West) - Entering signal----------------------------------------
    time_array_1 = input_signal_data[0][3]
    psd_array_1 = input_signal_data[0][4]
    opt_channels_1 = input_signal_data[0][5] #Optical channel list
    channels_1 = len(opt_channels_1)
    # Extract signal and noise field envelopes for each optical channel
    if segment == 1 or feedback_mode == 0:
        wave_key_1 = np.empty(channels_1)
        wave_freq_1 = np.empty(channels_1)
        jones_vector_1 = np.full([channels_1, 2], 0 + 1j*0, dtype=complex) 
        if opt_channels_1[0][3].ndim == 2:
            opt_field_rcv_1 = np.full([channels_1, 2, n], 0 + 1j*0, dtype=complex) 
        else: # Polarization format: Exy
            opt_field_rcv_1 = np.full([channels_1, n], 0 + 1j*0, dtype=complex) 
        noise_field_rcv_1 = np.full([channels_1, n], 0 + 1j*0, dtype=complex) 
    #Load wavelength channels
    for ch in range(0, channels_1): 
        wave_key_1[ch] = opt_channels_1[ch][0]
        wave_freq_1[ch] = opt_channels_1[ch][1]
        jones_vector_1[ch] = opt_channels_1[ch][2]
        opt_field_rcv_1[ch] = opt_channels_1[ch][3]
        noise_field_rcv_1[ch] = opt_channels_1[ch][4]

    #Port 2 (ID 4 - East) - Entering signal---------------------------------------
    time_array_4 = input_signal_data[1][3]
    psd_array_4 = input_signal_data[1][4]
    opt_channels_4 = input_signal_data[1][5] #Optical channel list
    channels_4 = len(opt_channels_4)
    # Extract signal and noise field envelopes for each optical channel
    if segment == 1 or feedback_mode == 0:
        wave_key_4 = np.empty(channels_4)
        wave_freq_4 = np.empty(channels_4)
        jones_vector_4 = np.full([channels_4, 2], 0 + 1j*0, dtype=complex) 
        if opt_channels_4[0][3].ndim == 2:
            opt_field_rcv_4 = np.full([channels_1, 2, n], 0 + 1j*0, dtype=complex) 
        else: # Polarization format: Exy
            opt_field_rcv_4 = np.full([channels_1, n], 0 + 1j*0, dtype=complex)
        noise_field_rcv_4 = np.full([channels_4, n], 0 + 1j*0, dtype=complex)  
    #Load wavelength channels
    for ch in range(0, channels_4): 
        wave_key_4[ch] = opt_channels_4[ch][0]
        wave_freq_4[ch] = opt_channels_4[ch][1]
        jones_vector_4[ch] = opt_channels_4[ch][2]
        opt_field_rcv_4[ch] = opt_channels_4[ch][3]
        noise_field_rcv_4[ch] = opt_channels_4[ch][4]
        
    #Port 3 (ID 5 - South) - Entering signal---------------------------------------
    time_array_5 = input_signal_data[2][3]
    psd_array_5 = input_signal_data[2][4]
    opt_channels_5 = input_signal_data[2][5] #Optical channel list
    channels_5 = len(opt_channels_5)
    # Extract signal and noise field envelopes for each optical channel
    if segment == 1 or feedback_mode == 0:
        wave_key_5 = np.empty(channels_5)
        wave_freq_5 = np.empty(channels_5)
        jones_vector_5 = np.full([channels_5, 2], 0 + 1j*0, dtype=complex) 
        if opt_channels_5[0][3].ndim == 2:
            opt_field_rcv_5 = np.full([channels_1, 2, n], 0 + 1j*0, dtype=complex) 
        else: # Polarization format: Exy
            opt_field_rcv_5 = np.full([channels_1, n], 0 + 1j*0, dtype=complex)
        noise_field_rcv_4 = np.full([channels_4, n], 0 + 1j*0, dtype=complex)  
        noise_field_rcv_5 = np.full([channels_5, n], 0 + 1j*0, dtype=complex)  
    #Load wavelength channels
    for ch in range(0, channels_5): 
        wave_key_5[ch] = opt_channels_5[ch][0]
        wave_freq_5[ch] = opt_channels_5[ch][1]
        jones_vector_5[ch] = opt_channels_5[ch][2]
        opt_field_rcv_5[ch] = opt_channels_5[ch][3]
        noise_field_rcv_5[ch] = opt_channels_5[ch][4]

    '''==CALCULATIONS======================================================='''

    '''==OUTPUT PARAMETERS LIST============================================='''
    opt_circ_parameters = []
    opt_circ_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    opt_circ_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''   
    optical_channels_3 = []
    optical_channels_6 = []
    optical_channels_2 = []
    
    # Port 2 (ID 3 - East) - Exiting signal (from port 1 (ID 1 West))--------------------------------------
    for ch in range(0, channels_1):
        opt_ch_3 = [int(wave_key_1[ch]), wave_freq_1[ch], jones_vector_1[ch], opt_field_rcv_1[ch], noise_field_rcv_1[ch]]
        optical_channels_3.append(opt_ch_3)
    # Port 3 (ID 6 - South) - Exiting signal (from port 2 (ID 4 East))-------------------------------------
    for ch in range(0, channels_4):
        opt_ch_6 = [int(wave_key_4[ch]), wave_freq_4[ch], jones_vector_4[ch], opt_field_rcv_4[ch], noise_field_rcv_4[ch]]
        optical_channels_6.append(opt_ch_6)
    # Port 1 (ID 2 - West) - Exiting signal (from port 3 (ID 5 - South)---------------------------------------
    for ch in range(0, channels_5):
        opt_ch_2 = [int(wave_key_5[ch]), wave_freq_5[ch], jones_vector_5[ch], opt_field_rcv_5[ch], noise_field_rcv_5[ch]]
        optical_channels_2.append(opt_ch_2)
    
    return ([ [3, signal_type, fs, time_array_1, psd_array_1, optical_channels_3],
                   [6, signal_type, fs, time_array_4, psd_array_4, optical_channels_6],
                   [2, signal_type, fs, time_array_5, psd_array_5, optical_channels_2] ], 
                   opt_circ_parameters, opt_circ_results)






