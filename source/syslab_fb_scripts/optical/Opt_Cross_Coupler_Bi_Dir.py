"""
Optical Cross Coupler (Bi-directional)
Version 1.0 (19.02 23 Feb 2019)
"""

import numpy as np
import config
import project_fabry_perot as fdk

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Cross Coupler'
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
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    cc = float(parameters_input[0][1]) #Coupling coefficient
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    optical_in = input_signal_data[0][4]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input_P1 = optical_in[0][3]
    jones_vector_P1 = optical_in[0][2]
    noise_array_P1 = optical_in[0][4]
    psd_array_P1 = optical_in[0][5]

    e_field_input_P2 = np.full(n, 0 + 1j*0, dtype=complex)   
    
    
    '''==CALCULATIONS======================================================='''    
    # 2x2 optical coupler (scattering matrix)
    # s11 = sqrt(1-cc), s12 = j*sqrt(cc), s21 = j*sqrt(cc), s22 = sqrt(1-cc)
    # Source: (Advanced Optical Communication Systems and Networks, 2013) 
    # E1_out = s11*E1_in + s12*E2_in
    
    # Calculate fields exiting ports 3/4 (based on input fields at ports 1/2)
    e_field_output_P3 = e_field_input_P1*(np.sqrt(1-cc)) + e_field_input_P2*(1j*np.sqrt(cc))
    e_field_output_P4 = e_field_input_P1*(1j*np.sqrt(cc)) + e_field_input_P2*(np.sqrt(1-cc))

    # Calculate field exiting at port 2 (based on input fields at ports 3/4)
    if segment == 1 or feedback_mode == 0:
        # Initialize input fields for ports 3/4 (set to all zeros for first iteration of 
        # feedback mode OR if feedback mode is OFF)
        fdk.e_field_output_P2 = np.full(n, 0 + 1j*0, dtype=complex)
        e_field_input_P3 = np.full(n, 0 + 1j*0, dtype=complex)
    else:
        # Retrieve signal data from In-Feedback ports (ports 3/4)
        optical_in_P3 = input_signal_data[1][4]
        e_field_input_P3 = optical_in_P3[0][3]
    
    if feedback_mode == 2:
        # If feedback mode is ON, perform calculations of output field at port 2
        # for feedback segment samples only
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        for seg in range(start_index, n):
            s21_x_E3In = e_field_input_P3[seg - int(segment_length)] * (1j*np.sqrt(cc))
            fdk.e_field_output_P2[seg] = s21_x_E3In
    else:
        # Feedback mode is OFF - calculate output field at P2 for all samples
        s21_x_E3In = e_field_input_P3 * (1j*np.sqrt(cc))
        fdk.e_field_output_P2 = s21_x_E3In
           
    '''==OUTPUT PARAMETERS LIST============================================='''
    optical_coupler_parameters = []
    optical_coupler_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    optical_coupler_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''   
    optical_P3 = [[wave_key, wave_freq, jones_vector_P1, e_field_output_P3, noise_array_P1, psd_array_P1]]
    optical_P4 = [[wave_key, wave_freq, jones_vector_P1, e_field_output_P4, noise_array_P1, psd_array_P1]] 
    optical_P2 = [[wave_key, wave_freq, jones_vector_P1, fdk.e_field_output_P2, noise_array_P1, psd_array_P1]] 
      
    return ([[5, signal_type, fs, time_array, optical_P3],
             [7, signal_type, fs, time_array, optical_P4],
             [4, signal_type, fs, time_array, optical_P2]], 
              optical_coupler_parameters, optical_coupler_results)

