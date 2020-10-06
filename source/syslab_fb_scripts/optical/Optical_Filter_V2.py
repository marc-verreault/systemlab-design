"""
SystemLab-Design Version 20.01.r3
Optical Demux 4-Ch
Version 1.0 (4 June 2020)
"""
import numpy as np
import config
from scipy import constants
import os
import importlib

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==========================================='''
    module_name = 'Channel Filter'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    iterations = settings['iterations']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']
    
    # Status message - initiation of fb_script (Sim status panel & Info/Status window)
    fb_title_string = 'Running ' + str(module_name) + ' - Iteration #: ' + str(iteration)
    config.status_message(fb_title_string)

    # Data display - title of current fb_script
    # display_data(text, data, print data to second line?, apply bold font?)
    config.display_data(' ', ' ', False, False)
    fb_data_string = 'Data output for ' + str(module_name) + ' - Iteration #: '
    config.display_data(fb_data_string, iteration, False, True) 
    
    '''==PARAMETERS================================================'''
    ctr_freq_1 = float(parameters_input[1][1])*1e12
    bw =  float(parameters_input[3][1])*1e9
    profile = str(parameters_input[4][1]) 
    sigma_calc = str(parameters_input[5][1])
    sigma = float(parameters_input[6][1])*1e9
    pwr_gauss = float(parameters_input[7][1])
    display_filter_profile = int(parameters_input[9][1])
    passband = float(parameters_input[10][1])*1e9 # GHz -> Hz
    graph_units = str(parameters_input[11][1])
    freq_start =  float(parameters_input[12][1])*1e12 # THz -> Hz
    freq_end = float(parameters_input[13][1])*1e12 # THz -> Hz
    ref_key = int(parameters_input[14][1])
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
    # Initialize output fields (for 4 ports)
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out_1 = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
    else: # Polarization format: Exy
        opt_field_out_1 = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    # Prepare freq array (sampled signals)
    T = n/fs
    k = np.arange(n)
    frq = k/T # Positive/negative freq (double sided) 
    wave = np.empty(channels)
    
    bw_3_db = 'NA'
    bw_1_db = 'NA'
    bw_half_db = 'NA'
    bw_isolation = 'NA'
    adj_isolation_ratio = 'NA'
    
    """Apply port filtering to all input channels-----------------------------------------"""
    for ch in range(0, channels):
        config.status_message('Applying port filtering to channel: ' + str(ch) + ' (' +
                                           str(wave_freq[ch]*1e-12) + ' THz)')
        # Frequency array adjusted to center frequency of optical channel
        frq = frq - frq[int(round(n/2))] + wave_freq[ch]
        # Apply FFT (time -> freq domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_x_1 = np.fft.fft(opt_field_rcv[ch, 0])
            Y_x_1 = np.fft.fftshift(Y_x_1)
            Y_y_1 = np.fft.fft(opt_field_rcv[ch, 1])
            Y_y_1 = np.fft.fftshift(Y_y_1)
        else:
            Y_1 = np.fft.fft(opt_field_rcv[ch])
            Y_1 = np.fft.fftshift(Y_1)
        N = np.fft.fftshift(np.fft.fft(noise_field_rcv[ch]))
        """Apply transfer function to field envelope of channel---------------"""
        if profile == 'Rectangular':
            tr_fcn_filt_1 = rect_profile(frq, ctr_freq_1, bw)
        elif profile == 'Gaussian':
            if sigma_calc == 'Direct':
                sig_filter = sigma
            else:
                sig_filter = bw/(2*np.sqrt(2*np.log2(2)))
            tr_fcn_filt_1 = gaussian_profile(frq, ctr_freq_1, sig_filter)
        elif profile == 'Super-Gaussian':
            if sigma_calc == 'Direct':
                sig_filter = sigma
            else:
                sig_filter = bw/(2*np.sqrt(2*np.log2(2)))
            tr_fcn_filt_1 = super_gaussian_profile(frq, ctr_freq_1, sig_filter, pwr_gauss)
            
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_x_1 = Y_x_1*tr_fcn_filt_1
            Y_y_1 = Y_y_1*tr_fcn_filt_1
        else:
            Y_1 = Y_1*tr_fcn_filt_1
        N = N*tr_fcn_filt_1
        
        # Apply IFFT (freq -> time domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            opt_field_out_1[ch, 0] = np.fft.ifft(np.fft.ifftshift(Y_x_1))
            opt_field_out_1[ch, 1] = np.fft.ifft(np.fft.ifftshift(Y_y_1))
        else:
            opt_field_out_1[ch] = np.fft.ifft(np.fft.ifftshift(Y_1))
        noise_field_out[ch] = np.fft.ifft(np.fft.ifftshift(N))
            
    """Perform filter analysis (passband, transfer function graph, isolation)--------------------"""
    # Build pass band profile for all channels 
    freq_array = np.arange(freq_start, freq_end, 0.5e9)
    if profile == 'Rectangular':
        tr_fcn_filt_1 = rect_profile(freq_array, ctr_freq_1, bw)
    elif profile == 'Gaussian':
        if sigma_calc == 'Direct':
            sig_filter = sigma
        else:
            sig_filter = bw/(2*np.sqrt(2*np.log2(2)))
        tr_fcn_filt_1 = gaussian_profile(freq_array, ctr_freq_1, sig_filter)
    elif profile == 'Super-Gaussian':
        if sigma_calc == 'Direct':
            sig_filter = sigma
        else:
            sig_filter = bw/(2*np.sqrt(2*np.log2(2)))
        tr_fcn_filt_1 = super_gaussian_profile(freq_array, ctr_freq_1, sig_filter, pwr_gauss)
        
    total_profile = [np.square(np.abs(tr_fcn_filt_1))]
    ctr_freqs = [ctr_freq_1]
        
    # BW calculations------------------------------------------------------------
    power_profile_p1 = total_profile[0]
    i_max = np.argmax(power_profile_p1)
    power_profile_p1 = power_profile_p1[0:i_max+1]
    frq_3_db = np.interp(0.5, power_profile_p1, freq_array[:i_max+1])
    frq_1_db = np.interp(0.79432, power_profile_p1, freq_array[:i_max+1])
    frq_half_db = np.interp(0.89125, power_profile_p1, freq_array[:i_max+1])
    bw_3_db = 2*1e-9*np.abs(ctr_freq_1 - frq_3_db)
    bw_1_db = 2*1e-9*np.abs(ctr_freq_1 - frq_1_db)
    bw_half_db = 2*1e-9*np.abs(ctr_freq_1 - frq_half_db)
    # Create plot instance
    if display_filter_profile == 2:
        config.demux_filter_graph =  config.view.Demux_Analyzer('Filter transfer (all ports)', freq_array, 'Frequency (Hz)', 
                                                                         total_profile, 'Transmission - power', wave_freq, wave_key, freq_start,
                                                                         freq_end, ctr_freqs, passband/2, graph_units, ref_key)
        config.demux_filter_graph.show()
        
    '''==OUTPUT PARAMETERS LIST======================================='''
    opt_filter_parameters = []
    opt_filter_parameters = parameters_input
  
    '''==RESULTS==================================================='''
    results = []
    '''bw_result_3_dB = ['3 dB passband', bw_3_db, 'GHz', ' ', False, '0.2f']
    bw_result_1_dB = ['1 dB passband', bw_1_db, 'GHz', ' ', False, '0.2f']
    bw_result_half_dB = ['0.5 dB passband', bw_half_db, 'GHz', ' ', False, '0.2f']
    results.extend([bw_result_3_dB, bw_result_1_dB, bw_result_half_dB, adj_isolation_result ])'''
    
    '''==RETURN (Output Signals, Parameters, Results)========================================='''   
    optical_channels_1 = []
    for ch in range(0, channels):
        opt_ch_1 = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out_1[ch], noise_field_out[ch, :]]
        optical_channels_1.append(opt_ch_1)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels_1]], 
                 opt_filter_parameters, results)
                 
def rect_profile(frq, ctr_freq, bw):
    tr_fcn_filter = np.full(np.size(frq), 0 + 1j*0, dtype=complex)
    for i in range(0, np.size(frq)):
        if frq[i] >= ctr_freq - (bw/2) and frq[i] <= ctr_freq + (bw/2):
            tr_fcn_filter[i] = 1 + 1j*0
    return tr_fcn_filter
    
def gaussian_profile(frq, ctr_freq, sigma):
    tr_fcn_filter = np.full(np.size(frq), 0 + 1j*0, dtype=complex)
    for i in range(0, np.size(frq)):
        tr_fcn_filter[i] = np.exp(-((frq[i] - ctr_freq)**2)/(2*sigma**2))
    return tr_fcn_filter
    
def super_gaussian_profile(frq, ctr_freq, sigma, pwr_gauss):
    tr_fcn_filter = np.full(np.size(frq), 0 + 1j*0, dtype=complex)
    for i in range(0, np.size(frq)):
        tr_fcn_filter[i] = np.exp(-np.power(((frq[i] - ctr_freq)**2)/(2*sigma**2), pwr_gauss))
    return tr_fcn_filter
