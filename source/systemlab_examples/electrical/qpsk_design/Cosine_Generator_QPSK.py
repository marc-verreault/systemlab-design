"""
Cosine Generator module
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Cosine Generator'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(i))
        config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    freq = 5e9
    signal_amp = 2
    noise = False
    noise_rms = 0.1

    carrier = 0
    sig_type = 'Electrical'
    
    #Parameters table
    signal_gen_parameters = []
    #~ par_freq = ['Freq', freq, 'Hz', 'Sinusoidal']
    #~ par_amplitude = ['Amplitude', signal_amp, 'v', 'Peak to peak amplitude']
    #~ par_noise = ['Include noise', noise, '', '' ]
    #~ par_noise_amplitude = ['Amplitude noise', noise_rms , 'volts', '']

    #~ signal_gen_parameters = [par_freq, par_amplitude, par_noise, par_noise_amplitude]
    
    '''==CALCULATIONS======================================================='''
    time_array = np.linspace(0, time, n)
    signal_array = signal_amp * np.cos(2*np.pi*freq*time_array)
    noise_array = np.zeros(n)    
  
    '''==RESULTS============================================================'''
    signal_gen_results = []

    #As this is a single port transmitter, the returned signals will be allocated to the output port (portID 1)
        
    return ( [[1, sig_type, carrier, fs, time_array, signal_array, noise_array]], 
            signal_gen_parameters, signal_gen_results )



