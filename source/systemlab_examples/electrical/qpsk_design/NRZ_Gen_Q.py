"""
NRZ Generator module
"""

import numpy as np
import config
import project_qpsk as project

#import imp
#project = imp.load_source('project', 'C:/SystemLab_Dev/Project/QPSK Design/project.py')

'''
Signal formats:
Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), amplitude_array(5), noise_array(6)
Optical: portID, signal_type, wave_channel, jones_matrix, sample_rate, time_array, envelope_array, psd_array
Digital: portID(0), signal_type(1), symbol_rate(2), bit_rate(3), order(4), 
time_array(5), discrete_array(6)
'''

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'NRZ Gen'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate'] 

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
        config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    bit_rate_input = input_signal_data[0][3]
    carrier_freq = project.carrier_freq
    

    
    #Parameters table
    signal_gen_parameters = []
#    par_freq = ['Freq', freq, 'Hz', 'Sinusoidal']
#    par_amplitude = ['Amplitude', signal_amp, 'v', 'Peak to peak amplitude']
#    par_noise = ['Include noise', noise, '', '' ]
#    par_noise_amplitude = ['Amplitude noise', noise_rms , 'volts', '']

#    signal_gen_parameters = [par_freq, par_amplitude, par_noise, par_noise_amplitude]
    
    '''==CALCULATIONS======================================================='''
    binary_input = input_signal_data[0][6]
    time = input_signal_data[0][5]
    
    binary_seq_length = np.size(binary_input)
    samples_per_bit = int(round(fs/bit_rate_input))
    
    #Create electrical NRZ from binary stream  
    
    
    
    
    
    elec_sig_out = np.zeros(n, )    
    
    for sig in range(0, binary_seq_length):
        signal = 1
        if binary_input[sig] == 0:
            signal = -1
        start_index = int(sig*int(samples_per_bit))
        elec_sig_out[start_index : start_index+samples_per_bit] = float(signal)
    
    
    
    
    
    
    
    #~ elec_sig_out = np.array([], dtype = float)          
    #~ for sig in range(0, binary_seq_length):
        #~ i = 0
        #~ while i < int(samples_per_bit):
            #~ if binary_input[sig] == 0:
                #~ signal = -1
            #~ else:
                #~ signal = 1
            #~ elec_sig_out = np.append(elec_sig_out, signal)
            #~ i += 1
    
    #  Setup noise variance/standard deviation based on EsNo setting
    voltage = 1
    T = project.symbol_rate
    sym_period = 1/T
    Es = np.square(voltage)*sym_period #for matched filter (V^2 * 1/Sym rate)
    SNR_per_sym_dB = iteration
    SNR_per_sym_linear = np.power(10, SNR_per_sym_dB/10)
    psd = Es/(2*SNR_per_sym_linear)
    std_dev = np.sqrt(psd*fs)
    
    # Build noise array (AWGN)
    config.sim_status_win.textEdit.append('Building noise array...')
    #noise_sig_out = np.random.normal(0,std_dev,n)
    noise_sig_out = np.zeros(n, )
    for i in range(0, n):
       noise_sig_out[i] = np.random.normal(0,std_dev)
    config.sim_status_win.textEdit.append('Noise array complete...')
    
    #Add noise to signal
    elec_sig_out = np.add(elec_sig_out, noise_sig_out)
    
    '''==RESULTS============================================================'''
    signal_gen_results = []


    #As this is a single port transmitter, the returned signals will be allocated to the output port (portID 1)
    return ([[2, 'Electrical', carrier_freq, fs, time, elec_sig_out, noise_sig_out]], 
            signal_gen_parameters, signal_gen_results)


