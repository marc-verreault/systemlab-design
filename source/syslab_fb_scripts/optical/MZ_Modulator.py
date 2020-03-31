"""
SystemLab-Design Version 19.02
Functional block script: Mach Zhender Modulator
Version 1.0 (19.02 23 Feb 2019)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'MZM'
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
    
    '''==INPUT PARAMETERS=================================================================
    '''
    # Load parameters from FB parameters table
    # Parameter name(0), Value(1), Units(2), Notes(3)
    v_pi = float(parameters_input[0][1]) #Differential drive voltage (V)
    loss =  float(parameters_input[1][1]) #Insertion loss (dB)
    e_ratio = float(parameters_input[2][1]) #Extinction ratio (dB)

    #Additional parameters
    signal_type = 'Optical'
    
    '''==INPUT SIGNALS====================================================================
    '''
    time_array = input_signal_data[0][3] 
    psd_array =  input_signal_data[0][4]
    optical_in = input_signal_data[0][5]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input = optical_in[0][3]
    v1 = input_signal_data[1][5] #Upper arm (input port ID = 3)
    v2 = input_signal_data[2][5] #Lower arm (input port ID = 4)
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    
    '''==CALCULATIONS=====================================================================
    '''   
    # MZ modulator transfer function (Ref 1, Eq 5.56)
    # Eout = 0.5*[exp(j*(pi/v_pi)*V1) + exp(j*(pi/v_pi)*V2)]*Ein, where V1/V2 are 
    # upper/lower arm driver voltages
    e_ratio_linear = np.power(10, -e_ratio/10)
    loss_linear = np.power(10, -loss/10)
    e_field_output = np.sqrt(loss_linear) * e_field_input*0.5*( (1+np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*v1)
                             + (1- np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*v2) )
        
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    MZM_parameters = []
    MZM_parameters = parameters_input 
  
    '''==RESULTS==========================================================================
    '''
    MZM_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_out = [[wave_key, wave_freq, jones_vector, e_field_output, noise_array, psd_array]]
    
    return ([[2, signal_type, fs, time_array, optical_out]], MZM_parameters, MZM_results)

