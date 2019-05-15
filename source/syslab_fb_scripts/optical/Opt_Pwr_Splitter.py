"""
SystemLab-Design Version 19.02
Functional block script: Optical Power Splitter
Version 1.0 (19.02 23 Feb 2019)

Refs:
1) Cvijetic, M., and , Advanced Optical Communication Systems and Networks, 
(Artech House Applied Photonics) (Kindle Locations 18576-18577). Artech House.
Kindle Edition. 
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Splitter'
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
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Parameter name(0), Value(1), Units(2), Notes(3)
    cc = float(parameters_input[0][1]) #Coupling coefficient
    loss = float(parameters_input[1][1]) #Insertion loss
    include_ph = int(parameters_input[2][1]) #Include phase shift
    
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
    
    # 2x2 optical coupler (scattering matrix)
    # s11 = sqrt(1-cc), s12 = j*sqrt(cc), s21 = j*sqrt(cc), s22 = sqrt(1-cc)
    # E1_out = s11*E1_in + s12*E2_in = s11*E1_in (E2_in = 0)
    # E2_out = s21*E1_in + s22*E2_in = s21*E1_in (E2_in = 0)
    
    if include_ph == 2:
        e_field_output_1 = e_field_input*(np.sqrt(1-cc)) 
        e_field_output_2 = e_field_input*(-1j*np.sqrt(cc))
    else:
        e_field_output_1 = e_field_input*(np.sqrt(1-cc)) 
        e_field_output_2 = e_field_input*(np.sqrt(cc))
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    optical_splitter_parameters = []
    optical_splitter_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    optical_splitter_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
      
    optical_P2 = [[wave_key, wave_freq, jones_vector, e_field_output_1, noise_array, psd_array]]
    optical_P3 = [[wave_key, wave_freq, jones_vector, e_field_output_2, noise_array, psd_array]] 
      
    return ([[2, signal_type, fs, time_array, optical_P2],
             [3, signal_type, fs, time_array, optical_P3]], 
              optical_splitter_parameters,  optical_splitter_results)

