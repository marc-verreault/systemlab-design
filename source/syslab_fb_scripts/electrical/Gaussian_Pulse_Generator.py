"""
Gaussian Pulse Generator module
Version 1.0 (19.02.r2 15 Sep 2019)

Refs:
1) Wikipedia contributors, "Gaussian function," Wikipedia, The Free Encyclopedia, 
https://en.wikipedia.org/w/index.php?title=Gaussian_function&oldid=910923914
(accessed September 15, 2019). 
2) "Gaussian Pulses and Different Width Definitions", 
https://lr.ttu.ee/irm0120/2016kevad/width_table.pdf (accessed 17-Sep-2019)
"""
import numpy as np
import systemlab_utilities as util
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Gaussian Pulse Generator'
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
    signal_mag = float(parameters_input[0][1])
    width_model = str(parameters_input[1][1])
    time_units = str(parameters_input[2][1])
    unit_factor = util.adjust_units_time(time_units)
    t0 = float(parameters_input[3][1])*unit_factor
    offset = float(parameters_input[4][1])*unit_factor
    rep = float(parameters_input[5][1])*unit_factor
    carrier = 0
    sig_type = 'Electrical'
    
    #Parameters table
    signal_gen_parameters = []
    signal_gen_parameters = parameters_input
    
    '''==CALCULATIONS======================================================='''
    time_array = np.linspace(0, time, n)
    signal_array_start = np.zeros(n) 
    signal_array_total = np.zeros(n) 
    # Width definitions (wrt to t_zero) 
    # Width (1/e) : Amplitude: sqrt(2)*t_zero, Power: t_zero (1/e = 1/2.718282 = 0.367879)
    # FWHM: Amplitude: sqrt(8*log(2))*t_zero, Power: sqrt(4*log(2))*t_zero
    # RMS: Amplitude: t_zero, Power: (1/sqrt(2))*t_zero

    if width_model == 'FWHM (mag)':
        t0 = t0/(2*np.sqrt(2*np.log(2)))
    elif width_model == 'FWHM (pwr)':
        t0 = t0/(2*np.sqrt(np.log(2)))
    elif width_model == '1/e width (mag)': 
        t0 = t0/np.sqrt(2)
        
    for i in range(0, n):
        signal_array_start[i] = signal_mag * np.exp(-(np.square(time_array[i] - offset))/(2*np.square(t0)))
    
    total_pulses = 0
    if rep > 0:
        total_pulses = int(np.round(time/rep))
        pulse_spacing = int(np.round(rep*fs))
        for p in range(0, total_pulses):
            signal_array_total =  np.roll(signal_array_start, int(pulse_spacing*p)) + signal_array_total
    else:
        signal_array_total = signal_array_start
        
    noise_array = np.zeros(n)    
  
    '''==RESULTS============================================================'''
    signal_gen_results = []
    
    return ( [[1, sig_type, carrier, fs, time_array, signal_array_total, noise_array]], 
            signal_gen_parameters, signal_gen_results )



