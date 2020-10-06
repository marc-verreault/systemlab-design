"""
OPTICAL AMPLIFIER
Version 3.0 (20.01.r3 20-Aug-20)
Associated functional block: syslab_fb_library/Optical Amplifier

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication 
Systems and Networks (Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) Section 5: Optical Amplifiers, Course Notes (authors unknown)
Source: http://www2.engr.arizona.edu/~ece487/opamp1.pdf (accessed 17 Apr 2019)
3) Introduction to Optical Amplifiers (authors unknown)
Source: http://opti500.cian-erc.org/opti500/pdf/sm/Introduction%
20to%20Optical%20Ampflifers%20Module.pdf
(accessed 14 June 2020)
4) Calculation of Q-Factor from OSNR, T. Antony, A. Gumaste; 
WDM Network Design (Cisco Press, Feb 7, 2003)
Source: https://www.ciscopress.com/articles/article.asp?p=30886&seqNum=5
(accessed 20-Aug-20)
"""
import numpy as np
import config
from scipy import optimize

from scipy import constants # https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS===================================================
    '''
    module_name = settings['fb_name'] 
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
    
    '''==INPUT PARAMETERS===================================================
    '''
    # Load parameters from FB parameters table
    # Main amplifier parameters (header)
    g_o_db = float(parameters_input[1][1]) #Small signal gain
    pwr_sat_dbm = float(parameters_input[2][1]) #Saturated output power (dBm)
    nf_db = float(parameters_input[3][1]) #Noise figure (optical)
    opt_bw =  float(parameters_input[4][1])*1e12 #Optical amplifier bandwidth (THz->Hz)
    opt_freq =  float(parameters_input[5][1])*1e12 #Center frequency of amplifier BW (THz->Hz)
    # Operating parameters (header)
    mode = str(parameters_input[7][1])
    gain_setting_db = float(parameters_input[8][1]) 
    pwr_setting_dbm = float(parameters_input[9][1])
    # Noise analysis (header)
    add_ase = int(float(parameters_input[11][1]))
    add_ase_to_signal = int(float(parameters_input[12][1]))
    bw_osnr_measurment = float(parameters_input[13][1])*1e9 # GHz -> Hz
    
    '''==INPUT SIGNALS======================================================
    '''
    # Load optical group data from input port
    signal_type = input_signal_data[0][1]
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
    
    '''==CALCULATIONS=======================================================
    ''' 
    # Initialize output field arrays
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    # Calculate avg power + avg noise in (all channels) MV 20.01.r3 8-Jun-20------------------------------
    pwr_in = 0
    avg_ch_pwr_in = 0
    for ch in range(0, channels):
        pwr_in_ch = np.mean(np.square(np.abs(opt_field_rcv[ch])))
        noise_in_ch = np.mean(np.square(np.abs(noise_field_rcv[ch])))
        avg_ch_pwr_in += pwr_in_ch
        pwr_in += pwr_in_ch + noise_in_ch
    avg_ch_pwr_in = avg_ch_pwr_in/channels
    
    if pwr_in > 0:
        pwr_in_dbm = 10*np.log10(pwr_in*1e3)
    else:
        pwr_in_dbm = 'NA'
    if avg_ch_pwr_in > 0:
        avg_ch_pwr_in_dbm = 10*np.log10(avg_ch_pwr_in*1e3)
    else:
        avg_ch_pwr_in_dbm = 'NA'
        
    """Calculate amplifer gain------------------------------------------------------------------------"""
    g_o = np.power(10, g_o_db/10) # Linear gain
    pwr_sat = 1e-3*np.power(10, pwr_sat_dbm/10)
    
    # Calculate output saturation power (maximum output power of amplifier)
    pwr_out_sat = pwr_sat*np.log(2) # Ref 1, Eq. 2.93
    pwr_out_sat_dbm = 10*np.log10(pwr_out_sat*1e3)
    
    # Solve large signal gain implicit equation (G = Go*exp(-((G-1)*Pout)/G*(Psat))
    # where Psat is the output saturation power (output power where gain (G) drops by 3 dB)
    # Ref 1, Eq. 2.92 & Ref 2
    g = g_o
    counter = 0
    resolution = 0.001 #Convergence criterium
    pwr_out_target = pwr_in * g
    nf = np.power(10, nf_db/10)
    
    while True:
        if counter > 250: #Stop after 250 iterations
            break
        # Calculate predicted output power based on updated g
        #pwr_out_target = pwr_in * g
        #config.display_data('Output pwr target', pwr_out_target, 0, 0)
        #config.display_data('Output pwr target (dBm)', 10*np.log10(pwr_out_target*1e3), 0, 0)
        pwr_out_target = pwr_in * g + (opt_bw*(g - 1)*nf*constants.h*opt_freq/2)
        g_target = large_signal_gain(g, g_o, pwr_out_target, pwr_sat)
        #g_target = saturated_gain(g, g_o, pwr_in, pwr_sat)
        if g_target/g < 1 - resolution: #g is too high
            g = 0.5 * (g - g_target)
            counter += 1
        elif g_target/g > 1 + resolution: #g is too low
            g = 0.5 * (g_target + g)
            counter += 1
        else:
            break
            
    """Apply calculated (available gain) to optical channels-----------------------------------------"""
    for ch in range(0, channels):
        p_out = pwr_in * g #Total power calculation
        if mode == 'None':
            pass
        elif mode == 'Gain control':
            gain_setting = np.power(10, gain_setting_db/10)
            if gain_setting < g:
                g = gain_setting
        else: 
            pwr_setting = 1e-3*np.power(10, pwr_setting_dbm/10) 
            if pwr_setting < p_out:
                g = pwr_setting/pwr_in
        # Apply gain (g) to optical field and noise arrays
        g_channels = 1.0
        if (wave_freq[ch] > (opt_freq - (opt_bw/2))
             and wave_freq[ch] < (opt_freq + (opt_bw/2))): #Channel is within amplifier BW
                g_channels = g/channels
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            opt_field_out[ch, 0] = opt_field_rcv[ch, 0]*np.sqrt(g_channels)*jones_vector[ch, 0]
            opt_field_out[ch, 1] = opt_field_rcv[ch, 1]*np.sqrt(g_channels)*jones_vector[ch, 1]
        else:
            opt_field_out[ch] = opt_field_rcv[ch]*np.sqrt(g_channels)
        noise_field_out[ch] = noise_field_rcv[ch]*np.sqrt(g_channels)
        
    """Amplifier ASE calculation------------------------------------------------------------------------"""
    # Calculate noise spectral density (Ref 1, Eq 4.34)
    psd_ase = ((g/channels) - 1)*nf*constants.h*opt_freq/2 
    psd_ase_dbm = 10*np.log10(psd_ase*1e3)
    # Calculate total power of ASE
    # Ref 1, Eq 4.37 (factor of 2 accounts for both polarization states)
    pwr_ase_total = psd_ase*opt_bw*2
    pwr_ase_total_dbm = 10*np.log10(pwr_ase_total*1e3)
    
    # Add noise to psd array (only added to noise bins/slices that are within
    # defined amplifier BW)
    ng = len(psd_array[0, :])
    psd_out = np.array([psd_array[0, :], np.zeros(ng)])
    for i in range(0, ng): # psd_out = psd_ase + psd_in*g
        if ( psd_array[0, i] > (opt_freq - (opt_bw/2)) 
            and psd_array[0, i] < (opt_freq + (opt_bw/2)) ):
            psd_out[1, i] = psd_ase + (psd_array[1, i]*g/channels)
        else:
            psd_out[1, i] = psd_array[1, i]
            
    # Integrate ase noise with time-domain noise?
    # Note: The noise bins used to calculate the time-domain
    # noise will not be removed. However, if time-domain noise
    # is integrated into the signal array, the noise bins will be set
    # to near-zero (1e-30 A^2/Hz)
    if add_ase == 2:
        ng_w = psd_array[0, 1] - psd_array[0, 0]
        for ch in range(0, channels):
            pwr_ase = 0
            # Build time-domain freq points
            T = n/fs
            k = np.arange(n)
            frq = (k/T)
            frq = frq - frq[int(round(n/2))] + wave_freq[ch]
            for i in range(0, ng):
                if psd_array[0, i] > frq[0] and psd_array[0, i] < frq[n-1]:
                    pwr_ase += 2*psd_out[1, i]*ng_w # Ref 1, Eq 4.37 (Pwr = 2*psd_ase*bw)
            # Convert to time-domain noise
            sigma_ase = np.sqrt(pwr_ase/2)
            noise_ase_real = np.random.normal(0, sigma_ase , n)
            noise_ase_imag = np.random.normal(0, sigma_ase , n)
            noise_array_ase = noise_ase_real + 1j*noise_ase_imag
            noise_field_out[ch] += noise_array_ase
            
        # Add noise to time domain signal and remove from noise array?
        if add_ase_to_signal == 2:
            for ch in range(0, channels):
                if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
                    opt_field_out[ch, 0] += noise_array_ase * jones_vector[ch, 0]
                    opt_field_out[ch, 1] += noise_array_ase * jones_vector[ch, 1]
                else:
                    opt_field_out[ch] += noise_array_ase
                noise_field_out[ch] += -noise_array_ase
                
        # Set psd_array points to zero (very low value)
        for ch in range(0, channels):
            T = n/fs
            k = np.arange(n)
            frq = k/T
            frq = frq - frq[int(round(n/2))] + wave_freq[ch]
            for i in range(0, ng):
                if psd_out[0, i] > frq[0] and psd_out[0, i] < frq[n-1]:
                    psd_out[1, i] = 1e-30
                    
    """Calculate average power exiting amplifier (all channels)----------------------------------------"""
    pwr_out_amp = 0
    for ch in range(0, channels):
        pwr_out_amp_ch = np.mean(np.square(np.abs(opt_field_out[ch])))
        noise_out_amp_ch = np.mean(np.square(np.abs(noise_field_out[ch])))
        pwr_out_amp += pwr_out_amp_ch + noise_out_amp_ch
    if pwr_out_amp > 0:
        pwr_out_amp_dbm = 10*np.log10(pwr_out_amp*1e3)
    else:
        pwr_out_amp_dbm = 'NA'
                    
    '''==OUTPUT PARAMETERS LIST===========================================
    '''
    opt_amp_parameters = []
    opt_amp_parameters = parameters_input
  
    '''==RESULTS======================================================
    '''
    # Estimation of output OSNR (Ref 4, Eq 4-20)
    osnr_predicted = 158.93 + avg_ch_pwr_in_dbm - nf_db - (10*np.log10(bw_osnr_measurment))
    results = []
    gain_db = 10*np.log10(g)
    gain_per_ch_db = 10*np.log10(g/channels)
    results.append(['Amplifier total gain (dB)', gain_db, 'dB', ' ', False, '0.3f'])
    results.append(['Amplifier total gain (linear)', g, ' ', ' ', False])
    results.append(['Amplifier per channel gain (dB)', gain_per_ch_db, 'dB', ' ', False, '0.3f'])
    results.append(['Amplifier per channel gain (linear)', g/channels, ' ', ' ', False])
    results.append(['Amplifier output saturation pwr (dBm)', pwr_out_sat_dbm, ' dBm', ' ', False, '0.3f'])
    results.append(['Amplifier ASE (avg PSD)', psd_ase, 'A^2/Hz', ' ', False])
    results.append(['Amplifier ASE (avg PSD)', psd_ase_dbm, 'dBm/Hz', ' ', False, '0.3f'])
    results.append(['Amplifier ASE (total pwr)', pwr_ase_total, 'W', ' ', False])
    results.append(['Amplifier ASE (total pwr)', pwr_ase_total_dbm, 'dBm', ' ', False, '0.3f'])
    results.append(['Avg sig/noise pwr entering amp', pwr_in, 'W', ' ', False])
    results.append(['Avg sig/noise pwr entering amp', pwr_in_dbm, 'dBm', ' ', False, '0.3f'])
    results.append(['Avg sig/noise pwr exiting amp', pwr_out_amp, 'W', ' ', False])
    results.append(['Avg sig/noise pwr exiting amp', pwr_out_amp_dbm, 'dBm', ' ', False, '0.3f' ])
    results.append(['Estimated OSNR at output', osnr_predicted , 'dB', ' ', False, '0.2f' ])
    
    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
        
    return ([[2, signal_type, fs, time_array, psd_out, optical_channels]], 
                 opt_amp_parameters, results)


def large_signal_gain(g, g_o, pwr_out, pwr_sat):
    return g_o*np.exp(-((g-1)/g) * (pwr_out/pwr_sat))
    
def saturated_gain(g, g_o, pwr_in, pwr_sat):
    return 1 + (pwr_sat/pwr_in)*np.log(g_o/g)
