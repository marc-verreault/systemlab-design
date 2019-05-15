"""
Function Generator module
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config
from scipy import signal

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Function Generator'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    waveform_type = str(parameters_input[0][1])
    freq = float(parameters_input[1][1])
    duty_cycle = float(parameters_input[2][1])
    gain = float(parameters_input[3][1])
    bias = float(parameters_input[4][1])
    # Other parameters
    carrier = 0
    sig_type = 'Electrical'
    
    #Parameters table
    signal_gen_parameters = []
    signal_gen_parameters = parameters_input
    
    '''==CALCULATIONS======================================================='''
    time_array = np.linspace(0, time, n)
    noise_array = np.zeros(n) 
    
    if waveform_type == 'Square':
        signal_array = gain*signal.square(2*np.pi*freq*time_array, duty = duty_cycle) + bias
    elif waveform_type == 'Sawtooth':
        signal_array = gain*signal.sawtooth(2*np.pi*freq*time_array, width = duty_cycle) + bias 
  
    '''==RESULTS============================================================'''
    signal_gen_results = []

    #As this is a single port transmitter, the returned signals will be allocated to the output port (portID 1)
        
    return ( [[1, sig_type, carrier, fs, time_array, signal_array, noise_array]], 
            signal_gen_parameters, signal_gen_results )



