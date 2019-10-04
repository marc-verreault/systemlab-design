"""
Optical reflector
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'R1'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(i))
        config.app.processEvents()
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==PARAMETERS========================================================='''
    r = float(parameters_input[0][1]) #Reflectivity Mirror 2
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    optical_in = input_signal_data[0][4]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input = optical_in[0][3]
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    psd_array = optical_in[0][5]
    
    '''==CALCULATIONS=======================================================
    '''
    #Prepare reflected signal data
    e_field_reflected = np.full(n, 0 + 1j*0, dtype=complex) 
    e_noise_reflected = np.full(n, 0 + 1j*0, dtype=complex)
    
    if feedback_mode == 2:
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        for seg in range(start_index, n):
            e_field_reflected[seg] = e_field_input[seg]*np.sqrt(r)
            e_noise_reflected[seg] = noise_array[seg]*np.sqrt(r)
    else:
        e_field_reflected = e_field_input*np.sqrt(r)
            
    '''==OUTPUT PARAMETERS LIST============================================='''
    reflector_parameters = []
    reflector_parameters = parameters_input
    
    '''==RESULTS============================================================'''
    reflector_results = []
    
    optical_out = [[wave_key, wave_freq, jones_vector, e_field_reflected, e_noise_reflected, psd_array]]
      
    return ([[3, signal_type, fs, time_array, optical_out]], 
              reflector_parameters, reflector_results)

