"""
Phase Shift
"""

import numpy as np
import config
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
        config.sim_status_win.progressBarFunctionalBlock.setValue(0)
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    ph_shift = float(parameters_input[0][1]) #Phase shift (deg)
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    optical_in = input_signal_data[0][4]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input = optical_in[0][3]
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    psd_array = optical_in[0][5]
    
    '''==CALCULATIONS======================================================='''
    config.sim_status_win.progressBarFunctionalBlock.setValue(10)
    ph_shift_rad = (ph_shift/180)*np.pi
    e_field_output = e_field_input * np.exp(1j*(ph_shift_rad))
    
    # Calculate field exiting at port 2 (based on input fields at ports 3/4)
    if segment == 1 or feedback_mode == 0:
        fdk.e_field_output_ph_shifter = np.full(n, 0 + 1j*0, dtype=complex)
        e_field_input_reflector = np.full(n, 0 + 1j*0, dtype=complex)
    else:
        # Retrieve signal data from In-Feedback ports (ports 3/4)
        optical_reflector_in = input_signal_data[0][4]
        e_field_input_reflector = optical_reflector_in[0][3]
    
    if feedback_mode == 2:
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        for seg in range(start_index, n): 
            fdk.e_field_output_ph_shifter[seg] = ( e_field_input_reflector[seg-int(segment_length)]
                                                * np.exp(1j*(ph_shift_rad)) )
    else:
        # Feedback mode is OFF
        fdk.e_field_output_ph_shifter = e_field_input_reflector * np.exp(1j*(ph_shift_rad))
           
    '''==OUTPUT PARAMETERS LIST============================================='''
    phase_shift_parameters = []
    phase_shift_parameters = parameters_input
    
    if config.sim_status_win_enabled == True:
        config.sim_status_win.progressBarFunctionalBlock.setValue(90)
  
    '''==RESULTS============================================================'''
    phase_shift_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    if config.sim_status_win_enabled == True:
        config.sim_status_win.progressBarFunctionalBlock.setValue(100)
    
    optical_out_2 = [[wave_key, wave_freq, jones_vector, e_field_output, noise_array, psd_array]]
    optical_out_4 = [[wave_key, wave_freq, jones_vector, fdk.e_field_output_ph_shifter, noise_array, psd_array]] 
      
    return ([[2, signal_type, fs, time_array, optical_out_2],
             [4, signal_type, fs, time_array, optical_out_4]], 
              phase_shift_parameters, phase_shift_results)

