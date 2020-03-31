"""
SystemLab-Design Version 20.01.r1
Functional block script: Phase Shift Electrical
Phase shift is only calculated if signal is periodic and has a defined 
carrier value. Otherwise the sampled signal will not be shifted.
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Phase Shift (Electrical)'
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
    ph_shift = float(parameters_input[0][1]) #Phase shift (deg)
    
    '''==INPUT SIGNALS======================================================'''
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    fs = input_signal_data[0][3]
    time_array = input_signal_data[0][4]
    sig_in = input_signal_data[0][5]
    noise_in = input_signal_data[0][6]
    
    '''==CALCULATIONS======================================================='''       
    if carrier != 0:
        sig_period = 1/carrier
        ph_shift_time = (ph_shift/360)*sig_period
        ph_shift_samples = int(np.round(ph_shift_time*fs))
        sig_out = np.roll(sig_in, ph_shift_samples)
        noise_out = np.roll(noise_in, ph_shift_samples)
    else:
        sig_out = sig_in
        noise_out = noise_in
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    phase_shift_parameters = []
    phase_shift_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    phase_shift_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''      
    electrical_out = [2, sig_type, carrier, fs, time_array, sig_out, noise_in] 
    return ([electrical_out], phase_shift_parameters, phase_shift_results)

