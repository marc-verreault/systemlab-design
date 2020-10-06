"""
SystemLab-Design Version 20.01.r3 8-Jun-20
Functional block script: Optical Amplifier
Version 2.0 (26 Sep 2019)
Version 3 (8 Jun 2020)
- Updated calculation for input power to include all channels (max gain is calculated against
this value)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) http://www2.engr.arizona.edu/~ece487/opamp1.pdf (accessed 17 Apr 2019)
"""
version = 3 #New versioning system for functional block scripts (8-Jun-20)
import numpy as np
import config
from scipy import optimize

from scipy import constants # https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Amplifier'
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
    # Load parameters from FB parameters table
    # Main amplifier parameters (header)
    g_o_db = float(parameters_input[1][1]) #Small signal gain
    pwr_sat_dbm = float(parameters_input[2][1]) #Saturated output power (dBm)
    nf_db = float(parameters_input[3][1]) #Noise figure (optical)
    # Operating parameters (header)
    mode = str(parameters_input[5][1])
    gain_setting_db = float(parameters_input[6][1]) 
    pwr_setting_dbm = float(parameters_input[7][1])
    # Noise analysis (header)
    add_ase = int(float(parameters_input[9][1]))
    
    '''==INPUT SIGNALS======================================================'''
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
    
    '''==CALCULATIONS=======================================================''' 
    # Channel gain calculations
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    # Calculate total power in (all channels) MV 20.01.r3 8-Jun-20
    pwr_in = 0
    for ch in range(0, channels):
        pwr_in = np.mean(np.square(np.abs(opt_field_rcv[ch])))
        pwr_in += pwr_in
        
    # Calculate amplifer gain
    g_o = np.power(10, g_o_db/10)  # Linear gain
    p_out = pwr_in * g_o
    pwr_sat = 1e-3*np.power(10, pwr_sat_dbm/10)

    # Solve large signal gain implicit equation (G = Go*exp(-((G-1)*Pout)/G*(Psat))
    # where Psat is the output saturation power (output power where gain (G) drops by 3 dB)
    # Ref 1, Eq. 2.92 & Ref 2
    g = g_o
    counter = 0
    resolution = 0.005 #Convergence criterium
    while True:
        if counter > 30: #Stop after 30 iterations
            break
        p_out_target = pwr_in * g
        g_target = g_o*np.exp(-((g-1)/g) * (p_out_target/pwr_sat))
        if g_target/g < 1 - resolution: #g is too high
            g = 0.5 * (g - g_target)
            counter += 1
        elif g_target/g > 1 + resolution: #g is too low
            g = 0.5 * (g_target + g)
            counter += 1
        else:
            break
    
    res = optimize.fixed_point(large_signal_gain, [g_o] , args=(g_o, pwr_in, pwr_sat))
    print(res)
    print(g)
    
    # Apply calculated (available gain) to optical channels
    for ch in range(0, channels):
        p_out = pwr_in * g
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
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            opt_field_out[ch, 0] = opt_field_rcv[ch, 0] * np.sqrt(g/2)
            opt_field_out[ch, 1] = opt_field_rcv[ch, 1] * np.sqrt(g/2)
        else:
            opt_field_out[ch] = opt_field_rcv[ch] * np.sqrt(g)
        noise_field_out[ch] = noise_field_rcv[ch] * np.sqrt(g)
        
        # Integrate ase noise with time-domain noise?
        pwr_ase = 0
        if add_ase == 2:
            # Build time-domain freq points
            T = n/fs
            k = np.arange(n)
            frq = (k/T)
            frq = frq - frq[int(round(n/2))] + wave_freq[ch]
            ng_w = psd_array[0, 1] - psd_array[0, 0]
            for i in range(0, ng):
                if psd_array[0, i] > frq[0] and psd_array[0, i] < frq[n-1]:
                    pwr_ase += psd_out[1, i]*ng_w
            # Convert to time-domain noise
            sigma_ase = np.sqrt(pwr_ase)
            noise_ase = np.random.normal(0, sigma_ase , n)
            noise_field_out[ch] += noise_ase
            
    # Amplifier ASE calculation
    nf = np.power(10, nf_db/10)
    psd_ase = (g - 1)*nf*constants.h*wave_freq[ch]/2 # Ref 1, Eq 4.34
    
    # Add noise to psd array
    ng = len(psd_array[0, :])
    psd_out = np.array([psd_array[0, :], np.zeros(ng)])
    for i in range(0, ng): # psd_out = psd_ase + psd_in*g 
        psd_out[1, i] = psd_ase + (psd_array[1, i]*g)
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    opt_amp_parameters = []
    opt_amp_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    opt_amp_results = []
    gain_db = 10*np.log10(g)
    gain_result =  ['Amplifier gain (dB)', gain_db, 'dB', ' ', False]
    gain_result_lin =  ['Amplifier gain (linear)', g, ' ', ' ', False]
    psd_amplifier_result = ['Amplifier ASE (avg PSD)', psd_ase, 'A^2/Hz', ' ', False]
    psd_ase_out_result = ['Output ASE (avg PSD)', pwr_ase/fs, 'A^2/Hz', ' ', False]
    opt_amp_results = [gain_result, gain_result_lin, psd_amplifier_result, psd_ase_out_result]

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
        
    return ([[2, signal_type, fs, time_array, psd_out, optical_channels]], 
                 opt_amp_parameters, opt_amp_results)


def large_signal_gain(g, g_o, pwr_in, pwr_sat):
    return g_o*np.exp(-((g-1)/g) * ((pwr_in*g)/pwr_sat))
