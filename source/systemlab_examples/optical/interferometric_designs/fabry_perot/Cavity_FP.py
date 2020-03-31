"""
Cavity FP
"""

import numpy as np
import config
from scipy import constants
# REF: https://docs.scipy.org/doc/scipy/reference/constants.html
import project_fabry_perot as fdk

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Phase shift'
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
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    d = float(parameters_input[0][1]) # Cavity length (m)
    index = float(parameters_input[1][1]) #Refractive index within cavity
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    psd_array = input_signal_data[0][4]
    optical_in = input_signal_data[0][5]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input_port_1 = optical_in[0][3]
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    
    '''==CALCULATIONS======================================================='''
    
    ph_shift = 2*np.pi*index*d/(constants.c/wave_freq)
    time_delay = 2*index*d/constants.c
    
    if segment == 1 or feedback_mode == 0:
        fdk.e_field_output_cavity_port_4 = np.full(n, 0 + 1j*0, dtype=complex)
        fdk.e_field_output_cavity_port_2 = np.full(n, 0 + 1j*0, dtype=complex)
        e_field_input_port_1 = np.full(n, 0 + 1j*0, dtype=complex)
        e_field_input_port_3 = np.full(n, 0 + 1j*0, dtype=complex)
    else:
        # Retrieve signal data from In-Feedback port (3)
        optical_in = input_signal_data[0][5]
        e_field_input_port_1 = optical_in[0][3]
        optical_r2_in = input_signal_data[1][5]
        e_field_input_port_3 = optical_r2_in[0][3]
    
    if feedback_mode == 2:
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        for seg in range(start_index, n): 
            fdk.e_field_output_cavity_port_2[seg] = ( e_field_input_port_1[seg-int(segment_length)]
                                                * np.exp(-1j*ph_shift) )
            fdk.e_field_output_cavity_port_4[seg] = ( e_field_input_port_3[seg-int(segment_length)]
                                                * np.exp(-1j*ph_shift) )
    else:
        # Feedback mode is OFF
        fdk.e_field_output_cavity_port_4 = e_field_input_port_3 * np.exp(-1j*ph_shift)
        fdk.e_field_output_cavity_port_2 = e_field_input_port_1 * np.exp(-1j*ph_shift)
       
    '''==OUTPUT PARAMETERS LIST============================================='''
    cavity_parameters = []
    cavity_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    cavity_results = []
    ph_shift_result = ['Phase shift (one-way)', ph_shift, 'rad', ' ', False]
    time_delay_result = ['Optical time delay (one-way)', time_delay, 's', ' ', False]
    cavity_results = [ph_shift_result, time_delay_result]

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_out_2 = [[wave_key, wave_freq, jones_vector, fdk.e_field_output_cavity_port_2, noise_array]]
    optical_out_4 = [[wave_key, wave_freq, jones_vector, fdk.e_field_output_cavity_port_4, noise_array]] 
      
    return ([[2, signal_type, fs, time_array, psd_array, optical_out_2],
             [4, signal_type, fs, time_array, psd_array, optical_out_4]], 
              cavity_parameters, cavity_results)

