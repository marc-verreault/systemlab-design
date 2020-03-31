"""
SystemLab-Design Version 20.01.r1
Functional block script: 90 Deg Optical Hybrid
Version 1.0 (19.02 23 Feb 2019)
Version 2.0 (12 Nov 2019)
Note: This component will only process the first channel of an optical group (other
channels will be ignored)

Refs:
1) Integrated 90deg Hybrid Balanced Receiver Datasheet, Optoplex Corporation, Fremont, CA
Source: http://www.optoplex.com/download/Optoplex%20Integrated%2090deg%20Balanced
%20Receiver%20Brochure%20Rev3.3.pdf (Accessed 21 Feb 2019)
"""

import config
import numpy as np
import copy
from scipy import constants, special #https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = '90 deg optical hybrid'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate']
    
    # Status message
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
    pol_mode = str(parameters_input[0][1])
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    # Input port (transmitted channel)
    time_array = input_signal_data[0][3]  
    psd_array_sig = input_signal_data[0][4]
    optical_in_sig = input_signal_data[0][5]
    if optical_in_sig[0][3].ndim == 2:
        e_field_input_sig = np.full([2, n], 0 + 1j*0, dtype=complex) 
    else:
        e_field_input_sig = np.full(n, 0 + 1j*0, dtype=complex)
    # Access first channel of optical group
    wave_key_sig = optical_in_sig[0][0]
    wave_freq_sig = optical_in_sig[0][1]
    jones_vector_sig = optical_in_sig[0][2]
    e_field_input_sig = copy.deepcopy(optical_in_sig[0][3])
    noise_array_sig = optical_in_sig[0][4]
    # Input port (local oscillator)
    psd_array_lo = input_signal_data[1][4]
    optical_in_lo = input_signal_data[1][5]
    if optical_in_lo[0][3].ndim == 2:
        e_field_input_lo = np.full([2, n], 0 + 1j*0, dtype=complex) 
    else:
        e_field_input_lo = np.full(n, 0 + 1j*0, dtype=complex)
    # Access first channel of optical group
    wave_key_lo = optical_in_lo[0][0]
    wave_freq_lo = optical_in_lo[0][1]
    jones_vector_lo = optical_in_lo[0][2]
    e_field_input_lo = copy.deepcopy(optical_in_lo[0][3])
    noise_array_lo = optical_in_lo[0][4]
    
    '''==CALCULATIONS======================================================='''
    pi = constants.pi
    #Add optical carrier to fields
    for i in range (0, n):
        if optical_in_sig[0][3].ndim == 2:
            e_field_input_sig[0, i] = e_field_input_sig[0, i]*np.exp(1j*2*pi*wave_freq_sig*time_array[i])
            e_field_input_sig[1, i] = e_field_input_sig[1, i]*np.exp(1j*2*pi*wave_freq_sig*time_array[i])
            e_field_input_lo[0, i] = e_field_input_lo[0, i]*np.exp(1j*2*pi*wave_freq_lo*time_array[i])
            e_field_input_lo[1, i] = e_field_input_lo[1, i]*np.exp(1j*2*pi*wave_freq_lo*time_array[i])
        else:
            e_field_input_sig[i] = e_field_input_sig[i]*np.exp(1j*2*pi*wave_freq_sig*time_array[i])
            e_field_input_lo[i] = e_field_input_lo[i]*np.exp(1j*2*pi*wave_freq_lo*time_array[i])
    # Calculate fields exiting ports 3-6
    # Ref 1 - Port 3: S+L, Port 4: S-L, Port 5: S+jL, Port 6: S-jL
    if optical_in_sig[0][3].ndim == 2:
        if pol_mode == 'X':
            e_field_output_P3 = 0.5*(e_field_input_sig[0] + e_field_input_lo[0])
            e_field_output_P4 = 0.5*(e_field_input_sig[0] - e_field_input_lo[0])
            e_field_output_P5 = 0.5*(e_field_input_sig[0] + 1j*e_field_input_lo[0])
            e_field_output_P6 = 0.5*(e_field_input_sig[0] - 1j*e_field_input_lo[0])
        else:
            e_field_output_P3 = 0.5*(e_field_input_sig[1] + e_field_input_lo[1])
            e_field_output_P4 = 0.5*(e_field_input_sig[1] - e_field_input_lo[1])
            e_field_output_P5 = 0.5*(e_field_input_sig[1] + 1j*e_field_input_lo[1])
            e_field_output_P6 = 0.5*(e_field_input_sig[1] - 1j*e_field_input_lo[1])
    else:
        e_field_output_P3 = 0.5*(e_field_input_sig + e_field_input_lo)
        e_field_output_P4 = 0.5*(e_field_input_sig - e_field_input_lo)
        e_field_output_P5 = 0.5*(e_field_input_sig + 1j*e_field_input_lo)
        e_field_output_P6 = 0.5*(e_field_input_sig - 1j*e_field_input_lo)
    
    e_field_noise_P3 = 0.5*(noise_array_sig + noise_array_lo)
    e_field_noise_P4 = 0.5*(noise_array_sig - noise_array_lo)
    e_field_noise_P5 = 0.5*(noise_array_sig + 1j*noise_array_lo)
    e_field_noise_P6 = 0.5*(noise_array_sig - 1j*noise_array_lo)    
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    ninety_deg_hybrid_parameters = []
    ninety_deg_hybrid_parameters = parameters_input #If no changes were made to parameters
    
    '''==RESULTS============================================================'''
    ninety_deg_hybrid_results = [] #No results
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_P3 = [[wave_key_lo, wave_freq_lo, jones_vector_sig, e_field_output_P3, e_field_noise_P3]]
    optical_P4 = [[wave_key_lo, wave_freq_lo, jones_vector_sig, e_field_output_P4, e_field_noise_P4]]
    optical_P5 = [[wave_key_lo, wave_freq_lo, jones_vector_sig, e_field_output_P5, e_field_noise_P5]]
    optical_P6 = [[wave_key_lo, wave_freq_lo, jones_vector_sig, e_field_output_P6, e_field_noise_P6]]    
      
    return ([[3, signal_type, fs, time_array, psd_array_sig, optical_P3],
             [4, signal_type, fs, time_array, psd_array_sig, optical_P4],
             [5, signal_type, fs, time_array, psd_array_sig, optical_P5],
             [6, signal_type, fs, time_array, psd_array_sig, optical_P6]], 
             ninety_deg_hybrid_parameters, ninety_deg_hybrid_results)

