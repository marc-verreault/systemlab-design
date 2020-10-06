"""
SystemLab-Design Version 20.01.r3
Functional block script: Time Shift Electrical
Version 1.0 (20.01.r3 25-Jun-20)
"""
import numpy as np
import config
import copy

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Time Shift (Electrical)'
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))   
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    iteration = settings['current_iteration'] #Current iteration loop for simulation    
    
    """Status messages-----------------------------------------------------------------------"""
    # Status message - initiation of fb_script (Sim status panel & Info/Status window)
    fb_title_string = 'Running ' + str(module_name) + ' - Iteration #: ' + str(iteration)
    config.status_message(fb_title_string)
    # Data display - title of current fb_script
    config.display_data(' ', ' ', False, False)
    fb_data_string = 'Data output for ' + str(module_name) + ' - Iteration #: '
    # Display data settings: Data title (str), Data (scalar, array, etc), 
    # Set to Bold?, Title & Data on separate lines?
    config.display_data(fb_data_string, iteration, False, True) 
    
    '''==INPUT PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    t_shift = float(parameters_input[0][1]) # Time shift (sec)
    
    '''==INPUT SIGNALS======================================================'''
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    time_array = input_signal_data[0][4]
    sig_t_shift = copy.deepcopy(input_signal_data[0][5])
    noise_t_shift = copy.deepcopy(input_signal_data[0][6])
    
    '''==CALCULATIONS======================================================='''       
    time_samples_shift = int(np.round(t_shift*fs))
    t_residual = float(t_shift) - float(time_samples_shift*(1/fs))
    if t_shift != 0:
        sig_t_shift = np.roll(sig_t_shift, time_samples_shift)
        noise_t_shift = np.roll(noise_t_shift, time_samples_shift)
        #sig_t_shift = np.interp(time_array + t_residual, time_array, sig_t_shift)
        #noise_t_shift = np.interp(time_array + t_residual, time_array, noise_t_shift)
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    parameters_output = []
    parameters_output = parameters_input
  
    '''==RESULTS============================================================'''
    results = []
    results.append(['Time shift',  t_shift, 's', ' ', False])
    
    if np.sign(time_samples_shift) == -1:
        results.append(['Shifted sample periods (left)',  np.abs(time_samples_shift), 'samples', ' ', False, 'n'])
    elif np.sign(time_samples_shift) == 1:
        results.append(['Shifted sample periods (right)',  np.abs(time_samples_shift), 'samples', ' ', False, 'n'])
    else:
        results.append(['Shifted sample periods',  np.abs(time_samples_shift), 'samples', ' ', False, 'n'])
    #results.append(['Time residual (interpolated)',  t_residual, 's', ' ', False])
    results.append(['Time residual (interpolated)',  'NA', ' ', ' ', False])

    '''==RETURN (Output Signals, Parameters, Results)=========================='''      
    electrical_out = [2, sig_type, carrier, fs, time_array, sig_t_shift, noise_t_shift] 
    return ([electrical_out], parameters_output, results)

