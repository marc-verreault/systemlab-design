"""
SystemLab-Design Version 19.02

SCRIPT TEMPLATE FOR FUNCTIONAL BLOCKS
Version: 1.0
Date: 5-March-2019

Ref 1:
Keysight Technologies, Application Note,
Fundamentals of RF and Microwave Noise Figure Measurements,
http://literature.cdn.keysight.com/litweb/pdf/5952-8255E.pdf (accessed 9 APr 2019)
"""

import numpy as np
import config
from scipy import signal

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'Script template'
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))    
    time = settings['time_window'] #Time window for simulation (sec)
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    f_sym = settings['symbol_rate'] #Symbol rate (default - Hz)
    t_step = settings['sampling_period'] #Sample period (Hz)
    #Iteration settings
    iteration = settings['current_iteration'] #Current iteration loop for simulation
    i_total = settings['iterations'] #Total iterations for simulation (default - 1)
    #Feedback settings
    segments = settings['feedback_segments'] #Number of integration segments
    segment = settings['feedback_current_segment'] #Current intgration segment
    segment = int(round(segment))
    feedback_mode = settings['feedback_enabled'] #Feedback mode is enabled(2)/disabled(0)
    
    # Status message (send to Simulation status panel)
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))                                     
                                          
    '''==INPUT PARAMETERS==============================================================
    '''
    gain_db = float(parameters_input[0][1])
    nf_db = float(parameters_input[1][1])
    
    '''==INPUT SIGNALS====================================================================
    '''
    # Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), 
    # amplitude_array(5), noise_array(6)
    time_array = input_signal_data[0][4]
    sig_in = input_signal_data[0][5]
    noise_in = input_signal_data[0][6]
    
    '''==CALCULATIONS=====================================================================
    '''
    carrier = 0
    sig_type_out = 'Electrical'
    
    # Apply gain to signal
    gain_linear = np.power(10, gain_db/20)
    sig_array = sig_in*np.sqrt(gain_linear)
    
    # Calculate noise (from Ref 1, Fig 2-1, page 8)
    # Noise (variance) from input (upstream source noise) = Na = total_noise_pwr_in*gain
    # Noise (variance) from amplifier (added noise) = Na_amp = (F - 1)*total_noise_pwr_in*gain
    # Total noise power out = Na + Na_amp
    noise_pwr_in = np.sum(np.abs(noise_in)*np.abs(noise_in))
    nf_linear = np.power(10, nf_db/10)
    noise_amp_var = (nf_linear - 1)*noise_pwr_in*gain_linear
    #Calculate standard deviation (sigma) & build output noise array (Gaussian noise dist)
    sigma = np.sqrt(noise_amp_var/n) #Amplifier contribution to noise 
    noise_array = np.random.normal(0, sigma, n) + noise_in*np.sqrt(gain_linear) # Add input noise
    
    #Calculate input & output SNR
    sig_pwr_in = np.sum(np.abs(sig_in)*np.abs(sig_in))
    snr_in = sig_pwr_in/noise_pwr_in
    snr_in_db = 10*np.log10(snr_in)
    
    noise_pwr_out = np.sum(np.abs(noise_array)* np.abs(noise_array))
    sig_pwr_out = np.sum(np.abs(sig_array)* np.abs(sig_array))
    snr_out = sig_pwr_out/noise_pwr_out
    snr_out_db = 10*np.log10(snr_out)
    
    noise_factor = snr_in/snr_out
    noise_figure = 10*np.log10(noise_factor)

    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS==========================================================================
    '''
    script_results = []
    result_1 = ['Gain (linear)', gain_linear, ' ', ' ', False]
    result_2 = ['Noise Figure (linear)', nf_linear, ' ', ' ', False]
    result_3 = ['SNR In (measured)', snr_in_db, 'dB', ' ', False]
    result_4 = ['SNR Out (measured)', snr_out_db, ' dB', ' ', False]
    result_5 = ['Noise Figure (measured)', noise_figure, ' dB', ' ', False]
    script_results = [result_1, result_2, result_3, result_4, result_5]
    
    '''==DATA PANEL=======================================================================
    '''
    #Send update to data panel (data_table_1)
#    data_1 = ['Name_1', value_1, 'units_1']
#    data_2 = ['Name_2', value_2, 'units_2']
#    config.data_table_1.append(data_1)
#    config.data_table_2.append(data_2)    


    '''==RETURN (Output Signals, Parameters, Results)==================================
    '''
    electrical_out = [2, sig_type_out, carrier, fs, time_array, sig_array, noise_array]
    return ([electrical_out], script_parameters, script_results)
