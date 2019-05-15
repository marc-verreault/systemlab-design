"""
SystemLab-Design Version 19.02
Functional block script: Optical Cross Coupler (Uni-directional)
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
    module_name = 'Optical Cross Coupler'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate']
        
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
    #Load parameters from FB parameters table [row][column]
    #Parameter name(0), Value(1), Units(2), Notes(3)
    cc = float(parameters_input[0][1]) #Coupling ratio (power)
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    optical_in_P1 = input_signal_data[0][4]
    wave_key = optical_in_P1[0][0]
    wave_freq = optical_in_P1[0][1]
    e_field_input_P1 = optical_in_P1[0][3]
    jones_vector_P1 = optical_in_P1[0][2]
    noise_array_P1 = optical_in_P1[0][4]
    psd_array_P1 = optical_in_P1[0][5]
    
    optical_in_P2 = input_signal_data[1][4]
    wave_key = optical_in_P2[0][0]
    wave_freq = optical_in_P2[0][1]
    e_field_input_P2 = optical_in_P2[0][3]
    jones_vector_P2 = optical_in_P2[0][2]
    noise_array_P2 = optical_in_P2[0][4]
    psd_array_P2 = optical_in_P2[0][5]
    
    '''==CALCULATIONS======================================================='''   
    # 2x2 symmetric optical coupler (scattering matrix) (Ref 1 - Eq 2.119)
    # t = s11/s22 = cos(kL) = , r = s12/s21 = j*sin(kL) where k is coupling coefficient & L is coupling length
    # s11/s22 = sqrt(1-cc), s12/s21 = j*sqrt(cc)
    # E1_out = s11*E1_in + s12*E2_in, E2_out = s21*E1_in + s22*E2_in
    
    # Calculate fields exiting ports 3/4 (based on input fields at ports 1/2)
    e_field_output_P3 = e_field_input_P1*(np.sqrt(1-cc)) + e_field_input_P2*(1j*np.sqrt(cc))
    e_field_output_P4 = e_field_input_P1*(1j*np.sqrt(cc)) + e_field_input_P2*(np.sqrt(1-cc)) 
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    optical_coupler_parameters = []
    optical_coupler_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    optical_coupler_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''    
    optical_P3 = [[wave_key, wave_freq, jones_vector_P1, e_field_output_P3, noise_array_P1, psd_array_P1]]
    optical_P4 = [[wave_key, wave_freq, jones_vector_P2, e_field_output_P4, noise_array_P2, psd_array_P2]] 
      
    return ([[3, signal_type, fs, time_array, optical_P3],
             [4, signal_type, fs, time_array, optical_P4]], 
              optical_coupler_parameters, optical_coupler_results)

