"""
SystemLab-Design Version 19.02
Functional block script: 90 Deg Optical Hybrid
Version 1.0 (19.02 23 Feb 2019)

Refs:
1) Integrated 90deg Hybrid Balanced Receiver Datasheet, Optoplex Corporation, Fremont, CA
Source: http://www.optoplex.com/download/Optoplex%20Integrated%2090deg%20Balanced
%20Receiver%20Brochure%20Rev3.3.pdf (Accessed 21 Feb 2019)
"""

import config

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
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    
    optical_in_sig = input_signal_data[0][4]
    wave_key = optical_in_sig[0][0]
    wave_freq = optical_in_sig[0][1]
    e_field_input_sig = optical_in_sig[0][3]
    jones_vector_sig = optical_in_sig[0][2]
    noise_array_sig = optical_in_sig[0][4]
    psd_array_sig = optical_in_sig[0][5]
    
    optical_in_ref = input_signal_data[1][4]
    wave_key = optical_in_ref[0][0]
    wave_freq = optical_in_ref[0][1]
    e_field_input_ref = optical_in_ref[0][3]
#    jones_vector_ref = optical_in_ref[0][2]
    noise_array_ref = optical_in_ref[0][4]
#    psd_array_ref = optical_in_ref[0][5]
    
    '''==CALCULATIONS======================================================='''
        
    # Calculate fields exiting ports 3-6
    # Ref 1 - Port 3: S+L, Port 4: S-L, Port 5: S+jL, Port 6: S-jL
    e_field_output_P3 = 0.5*(e_field_input_sig + e_field_input_ref)
    e_field_output_P4 = 0.5*(e_field_input_sig - e_field_input_ref)
    e_field_output_P5 = 0.5*(e_field_input_sig + 1j*e_field_input_ref)
    e_field_output_P6 = 0.5*(e_field_input_sig - 1j*e_field_input_ref)
    
    e_field_noise_P3 = 0.5*(noise_array_sig + noise_array_ref)
    e_field_noise_P4 = 0.5*(noise_array_sig - noise_array_ref)
    e_field_noise_P5 = 0.5*(noise_array_sig + 1j*noise_array_ref)
    e_field_noise_P6 = 0.5*(noise_array_sig - 1j*noise_array_ref)    
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    ninety_deg_hybrid_parameters = []
    ninety_deg_hybrid_parameters = parameters_input #If no changes were made to parameters
  
    '''==RESULTS============================================================'''
    ninety_deg_hybrid_results = [] #No results


    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    
    optical_P3 = [[wave_key, wave_freq, jones_vector_sig, e_field_output_P3, e_field_noise_P3, psd_array_sig]]
    optical_P4 = [[wave_key, wave_freq, jones_vector_sig, e_field_output_P4, e_field_noise_P4, psd_array_sig]]
    optical_P5 = [[wave_key, wave_freq, jones_vector_sig, e_field_output_P5, e_field_noise_P5, psd_array_sig]]
    optical_P6 = [[wave_key, wave_freq, jones_vector_sig, e_field_output_P6, e_field_noise_P6, psd_array_sig]]    
      
    return ([[3, signal_type, fs, time_array, optical_P3],
             [4, signal_type, fs, time_array, optical_P4],
             [5, signal_type, fs, time_array, optical_P5],
             [6, signal_type, fs, time_array, optical_P6]], 
             ninety_deg_hybrid_parameters, ninety_deg_hybrid_results)

