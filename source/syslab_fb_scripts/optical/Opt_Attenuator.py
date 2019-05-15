"""
SystemLab-Design Version 19.02
Functional block script: Optical attenuator
Version 1.0 (19.02 23 Feb 2019)
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
    att_linear = np.power(10, -att/10)
    e_field_output = e_field_input * np.sqrt(att_linear)
    noise_array = noise_array * np.sqrt(att_linear)
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    att_parameters = []
    att_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    att_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''      
    optical_P2 = [[wave_key, wave_freq, jones_vector, e_field_output, noise_array, psd_array]]
      
    return ([[2, signal_type, fs, time_array, optical_P2]], att_parameters, att_results)

