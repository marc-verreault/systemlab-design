"""
SystemLab-Design Version 20.01.r1
Optical Filter
Version 1.0 (11 Sep 2019)

REFS:
(1) Finisar White Paper: Filter Bandwidth Definition of the WaveShaper S-series Programmable 
Optical Processor (2012) Source: https://www.finisar.com/sites/default/files/resources/
white_paper_waveshaper_filter_bandwidth_definition.pdf (accessed 15-Nov-2019)
"""
import numpy as np
import config
from scipy import constants

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Filter'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))

    '''==PARAMETERS================================================'''
    units = str(parameters_input[0][1])
    ctr_freq = float(parameters_input[1][1])
    bw =  float(parameters_input[2][1])
    profile = str(parameters_input[3][1]) 
    sigma_calc = str(parameters_input[4][1])
    sigma = float(parameters_input[5][1])
    # Constants
    pi = constants.pi
    c = constants.c
    
    '''==INPUT SIGNALS=============================================='''
    # Load optical group data from input port
    signal_type = 'Optical'
    time_array = input_signal_data[0][3] # Sampled time array
    psd_array = input_signal_data[0][4] # Noise groups
    opt_channels = input_signal_data[0][5] #Optical channel list
    
    # Load frequency, jones vector, signal & noise field envelopes for each optical channel
    channels = len(opt_channels)
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex)  
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector[ch] = opt_channels[ch][2]
        opt_field_rcv[ch] = opt_channels[ch][3]
        noise_field_rcv[ch] = opt_channels[ch][4]

    '''==CALCULATIONS=============================================='''
    # Initialize output fields
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
    else: # Polarization format: Exy
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_output = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    # Prepare freq array
    T = n/fs
    k = np.arange(n)
    frq = k/T # Positive/negative freq (double sided) 
    wave = np.empty(channels)

    for ch in range(0, channels):
        frq = frq - frq[int(round(n/2))] + wave_freq[ch]
        
        # Apply FFT (time -> freq domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_x = np.fft.fft(opt_field_rcv[ch, 0])
            Y_x = np.fft.fftshift(Y_x)
            Y_y = np.fft.fft(opt_field_rcv[ch, 1])
            Y_y = np.fft.fftshift(Y_y)
        else:
            Y = np.fft.fft(opt_field_rcv[ch, :])
            Y = np.fft.fftshift(Y)
        wave[ch] = c/wave_freq[ch]
        if units == 'GHz':
            f_c = ctr_freq*1e9 
            bw_c = bw*1e9
        else: #Convert from wavelength to freq
            f_c = c/(ctr_freq*1e-9)
            bw_c = (c/(wave[ch])**2)*bw*1e-9 #bw_freq = (c/lambda^2)*bw_lambda
        
        # Apply transfer function to field envelope of channel (REF 1, Eqs 1-3)
        if profile == 'Rectangular':
            for i in range(0, n):
                if frq[i] >= f_c - (bw_c/2) and frq[i] <= f_c + (bw_c/2):
                    tr_fcn_filter = 1
                else:
                    tr_fcn_filter = 0
                if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
                    Y_x[i] = Y_x[i] * tr_fcn_filter
                    Y_y[i] = Y_y[i] * tr_fcn_filter
                else:
                    Y[i] = Y[i] * tr_fcn_filter
        else:
            if sigma_calc == 'Direct':
                sig_filter = sigma*1e9
            else:
                sig_filter = bw_c/(2*np.sqrt(2*np.log2(2)))
            for i in range(0, n):
                tr_fcn_filter = np.exp(-((frq[i] - f_c)**2)/(2*sig_filter**2))
                if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
                    Y_x[i] = Y_x[i] * tr_fcn_filter
                    Y_y[i] = Y_y[i] * tr_fcn_filter
                else:
                    Y[i] = Y[i] * tr_fcn_filter
        
        # Apply FFT (freq -> time domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_x = np.fft.ifftshift(Y_x) # MV 20.01.r3 4-Jul-20
            opt_field_out[ch, 0] = np.fft.ifft(Y_x)
            Y_y = np.fft.ifftshift(Y_y) # MV 20.01.r3 4-Jul-20
            opt_field_out[ch, 1] = np.fft.ifft(Y_y)
        else:
            Y = np.fft.ifftshift(Y) # MV 20.01.r3 4-Jul-20
            opt_field_out[ch] = np.fft.ifft(Y)

    '''==OUTPUT PARAMETERS LIST======================================='''
    opt_filter_parameters = []
    opt_filter_parameters = parameters_input
  
    '''==RESULTS==================================================='''
    opt_filter_results = []
    # Calculate results
    if units == 'GHz':
        wave_value_m = c/(ctr_freq*1e9)
        freq_value_thz = ctr_freq*1e-3
        wave_bw_value_m = (wave_value_m**2/c)*bw*1e9
        freq_bw_value_ghz = bw
    else:
        wave_value_m = ctr_freq*1e-9
        freq_value_thz = (c/(ctr_freq*1e-9))*1e-12
        wave_bw_value_m = bw*1e-9
        freq_bw_value_ghz = (c/wave_value_m**2)*bw*1e-9
    # Prepare results list
    ctr_wave_result = ['Filter center wavelength (nm)', wave_value_m*1e9, 'nm', ' ', False]
    ctr_freq_result = ['Filter center frequency (THz)', freq_value_thz, 'THz', ' ', False]
    bw_wave_result = ['Filter bandwidth (nm)', wave_bw_value_m*1e9, 'nm', ' ', False]
    bw_freq_result = ['Filter bandwidth (GHz)', freq_bw_value_ghz, 'GHz', ' ', False]
    if profile == 'Gaussian':
        sigma_result = ['Sigma (Gaussian filter)', sig_filter*1e-9, 'GHz', ' ', False]
    else:
        sigma_result = ['Sigma (Gaussian filter)', 'NA', 'GHz', ' ', False]
    results_list = [ctr_wave_result, ctr_freq_result, bw_wave_result, bw_freq_result, sigma_result]
    opt_filter_results.extend(results_list)

    '''==RETURN (Output Signals, Parameters, Results)========================================='''   
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_output[ch, :]]
        optical_channels.append(opt_ch)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels]], 
                 opt_filter_parameters, opt_filter_results)

