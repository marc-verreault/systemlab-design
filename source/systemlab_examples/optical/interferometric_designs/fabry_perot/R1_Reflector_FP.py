"""
Optical reflector
"""

import numpy as np
import config
import project_fabry_perot as fdk

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
    r = float(parameters_input[0][1]) #Reflectivity Mirror 1
    signal_type = 'Optical'
    time_array = input_signal_data[0][3] 
    #Input signal Port ID 1 - from 2x2 coupler
    optical_in = input_signal_data[0][4]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input_port_1 = optical_in[0][3]
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    psd_array = optical_in[0][5]
    #Input signal Port ID 3 - from mirror r2
#    e_field_input_port_3 = np.full(n, 0 + 1j*0, dtype=complex)

    '''==CALCULATIONS=======================================================
    '''
    # Calculate field exiting at port 4 (returning to 2x2 coupler)
    
    reflection_factor = r
    
    if segment == 1 or feedback_mode == 0:
        # Initialize input field for port ID 3 (set to all zeros for first iteration of 
        # feedback mode OR if feedback mode is OFF)
        fdk.e_field_output_port_4 = np.full(n, 0 + 1j*0, dtype=complex)
        fdk.e_field_output_port_2 = np.full(n, 0 + 1j*0, dtype=complex)
        e_field_input_port_3 = np.full(n, 0 + 1j*0, dtype=complex)
    else:
        # Retrieve signal data from port ID 3
        optical_input_port_3 = input_signal_data[1][4]
        e_field_input_port_3 = optical_input_port_3[0][3]
    
    if feedback_mode == 2:
        # If feedback mode is ON, perform calculations of output field at port 4
        # for feedback segment samples only
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        for seg in range(start_index, n):
            reflected_field_port_1 = e_field_input_port_1[seg - int(segment_length)]*np.sqrt(r)
            trans_field_port_1 = e_field_input_port_1[seg - int(segment_length)]*np.sqrt(1-r)
            reflected_field_port_3 = e_field_input_port_3[seg - int(segment_length)]*np.sqrt(r)
            trans_field_port_3 = e_field_input_port_3[seg - int(segment_length)]*np.sqrt(1-r)
            fdk.e_field_output_port_4[seg] = reflected_field_port_1 + trans_field_port_3
            fdk.e_field_output_port_2[seg] = reflected_field_port_3 + trans_field_port_1
    else:
        # Feedback mode is OFF
        reflected_field_port_1 = e_field_input_port_1*np.sqrt(r)
        trans_field_port_1 = e_field_input_port_1*np.sqrt(1-r)
        reflected_field_port_3 = e_field_input_port_3*np.sqrt(r)
        trans_field_port_3 = e_field_input_port_3*np.sqrt(1-r)
        fdk.e_field_output_port_4 = reflected_field_port_1 + trans_field_port_3
        fdk.e_field_output_port_2 = reflected_field_port_3 + trans_field_port_1
            
    '''==OUTPUT PARAMETERS LIST============================================='''
    reflector1_parameters = []
    reflector1_parameters = parameters_input
    
    '''==RESULTS============================================================'''
    reflector1_results = []
    
    optical_port_2 = [[wave_key, wave_freq, jones_vector, fdk.e_field_output_port_2, noise_array, psd_array]]
    optical_port_4 = [[wave_key, wave_freq, jones_vector, fdk.e_field_output_port_4, noise_array, psd_array]] 
      
    return ([[2, signal_type, fs, time_array, optical_port_2],
             [4, signal_type, fs, time_array, optical_port_4]], 
              reflector1_parameters, reflector1_results)

