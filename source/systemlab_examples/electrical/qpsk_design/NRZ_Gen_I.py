"""
NRZ Generator module
"""
import os, sys
import time as t
import numpy as np
from scipy import special
import config
import project_qpsk as project
import importlib

data_panels_path = str('syslab_config_files.config_data_panels')
config_data_panel = importlib.import_module(data_panels_path)

custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

# Instantiate status dialog for function block 
status_NRZ = view.FunctionalBlockStatusGUI()

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=================================================================
    '''
    module_name = 'NRZ Gen'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    feedback_mode = settings['feedback_enabled']
    if feedback_mode == 2:
        segments = settings['feedback_segments']
        segment = settings['feedback_current_segment']
        segment = int(round(segment))
    time = settings['time_window']
    fs = settings['sampling_rate'] 

    config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
                                          
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration)) 

    '''==INPUT PARAMETERS=================================================================
    '''
    bit_rate_input = input_signal_data[0][3]
    carrier_freq = project.carrier_freq

    #Parameters table
    signal_gen_parameters = []
#    par_freq = ['Freq', freq, 'Hz', 'Sinusoidal']
#    par_amplitude = ['Amplitude', signal_amp, 'v', 'Peak to peak amplitude']
#    par_noise = ['Include noise', noise, '', '' ]
#    par_noise_amplitude = ['Amplitude noise', noise_rms , 'volts', '']

#    signal_gen_parameters = [par_freq, par_amplitude, par_noise, par_noise_amplitude]
    
    '''==CALCULATIONS=====================================================================
    '''
    #~ status_NRZ.setWindowTitle('Simulation status/data: ' + module_name 
                                            #~ + ' (Iter #: ' + str(iteration) + ')')
    #~ status_NRZ.show()

    binary_input = input_signal_data[0][6]
    time = input_signal_data[0][5]
    
    binary_seq_length = np.size(binary_input)
    samples_per_bit = int(round(fs/bit_rate_input))
    
    # Create electrical NRZ from binary stream 
    elec_sig_out = np.zeros(n, )
    
    for sig in range(0, binary_seq_length):
        #~ status_NRZ.update_progress_bar(100*(sig/(binary_seq_length-1)))
        signal = 1
        if binary_input[sig] == 0:
            signal = -1
        start_index = int(sig*int(samples_per_bit))
        elec_sig_out[start_index : start_index+samples_per_bit] = float(signal)
            
    #  Setup noise variance/standard deviation based on EsNo setting
    voltage = 1
    T = project.symbol_rate
    sym_period = 1/T
    Es = np.square(voltage)*sym_period #for matched filter (V^2 * 1/Sym rate)
    SNR_per_sym_dB = iteration
    SNR_per_sym_linear = np.power(10, SNR_per_sym_dB/10)
    psd = Es/(2*SNR_per_sym_linear)
    psd_dB = 10 * np.log10(psd)
    std_dev = np.sqrt(psd*fs)
    
    # Build noise array (AWGN)
    #~ status_NRZ.text_update('Building noise array...')
    #~ config.app.processEvents()
    #noise_sig_out = np.random.normal(0,std_dev,n)
    noise_sig_out = np.zeros(n, )
    for i in range(0, n):
        noise_sig_out[i] = np.random.normal(0,std_dev)
        #~ status_NRZ.update_progress_bar(100*(i/(n-1)))
    #~ status_NRZ.text_update('Noise array complete...')
    #~ config.app.processEvents()
    
    #Re-calculate variance of sample to verify
    var_sample = np.var(noise_sig_out) 
    noise_pwr = np.average(np.square(noise_sig_out))
    PSD_measured = noise_pwr/fs
    
    #Add noise to signal
    elec_sig_out = np.add(elec_sig_out, noise_sig_out)
     
    '''==RESULTS==========================================================================
    '''
    signal_gen_results = []
    
    '''==UPDATES FOR DATA BOXES===========================================================
    '''
    #Send update to data box (data_table_2)
    config_data_panel.data_table_qpsk_2 = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['SNR per sym', SNR_per_sym_linear , '0.4E', 'a.u.']
    data_3 = ['SNR per sym (dB)', SNR_per_sym_dB, '0.4E', 'a.u.']                
    data_4 = ['PSD', psd, '0.4E', 'W/Hz']
    data_5 = ['PSD(dBW)', psd_dB, '0.4E', 'dBW/Hz']
    data_6 = ['Noise variance', var_sample, '0.4E', 'W'] 
    data_7 = ['Noise power', noise_pwr, '0.4E', 'W']
    data_8 = ['PSD measured', PSD_measured, '0.4E', 'W/Hz']
    data_list = [data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8]
    config_data_panel.data_table_qpsk_2.extend(data_list)

    '''==UPDATES FOR SIM DATA WINDOW======================================================
    '''
    #Update project graph list
    if iteration == 1:
        project.snr_per_sym = []
        project.ser_th = []
        
    project.snr_per_sym.append(SNR_per_sym_dB)
    
    # Probability of symbol error rate calculation = erfc[sqrt(Es/(2*No))] where SNR_per_sym_linear = Es/No
    # REF: Link Budget Analysis: Digital Modulation, Part 3 (slide 21), Atlanta RF (Bob Garvey, Chief Engineer), July. 
    # Retrieved (28-March-2019) from http://www.atlantarf.com/Downloads.php  
    
    ser_th = special.erfc(np.sqrt(SNR_per_sym_linear*0.5))  
    project.ser_th.append(ser_th)

    '''==RETURN (Output Signals, Parameters, Results)=====================================
    '''
    return ([[2, 'Electrical', carrier_freq, fs, time, elec_sig_out, noise_sig_out]], 
            signal_gen_parameters, signal_gen_results)


