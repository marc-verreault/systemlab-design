"""
SystemLab-Design Version 20.01.r3 8-Jun-20
Functional block script: Optical Amplifier
Version 2.0 (26 Sep 2019)
Version 3.0 (8 Jun 2020)
- Updated calculation for input power to include all channels (max gain is calculated against
this value)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) http://www2.engr.arizona.edu/~ece487/opamp1.pdf (accessed 17 Apr 2019)
"""
import numpy as np
import config
from scipy import optimize

from scipy import constants # https://docs.scipy.org/doc/scipy/reference/constants.html

# Import project_amplifier and systemlab_viewers
import systemlab_viewers_amp as view_amp

import project_amplifier as project
import importlib
'''custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)'''

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    #module_name = 'Optical Amplifier'
    # MV 20.01.r3 13-Jun-20 Update to module name now directly reads functional block name
    module_name = settings['fb_name'] 
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))   
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    iteration = settings['current_iteration'] #Current iteration loop for simulation
    iterations = settings['iterations']
    
    # Status message - initiation of fb_script (Sim status panel & Info/Status window)
    fb_title_string = 'Running ' + str(module_name) + ' - Iteration #: ' + str(iteration)
    config.status_message(fb_title_string)

    # Data display - title of current fb_script
    config.display_data(' ', ' ', False, False)
    fb_data_string = 'Data output for ' + str(module_name) + ' - Iteration #: '
    config.display_data(fb_data_string, iteration, False, True)  # When True, string & data printed on separate lines
    
    '''Reload project config files'''
    if iteration == 1:
        importlib.reload(project)
        importlib.reload(view_amp)
    
    '''==INPUT PARAMETERS========================================================='''
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
    # Initialize output field arrays
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    # Calculate avg power + avg noise in (all channels) MV 20.01.r3 8-Jun-20------------------------------
    pwr_in = 0
    for ch in range(0, channels):
        pwr_in_ch = np.mean(np.square(np.abs(opt_field_rcv[ch])))
        noise_in_ch = np.mean(np.square(np.abs(noise_field_rcv[ch])))
        pwr_in += pwr_in_ch + noise_in_ch
    if pwr_in > 0:
        pwr_in_dbm = 10*np.log10(pwr_in*1e3)
    else:
        pwr_in_dbm = 'NA'
        
    # Calculate amplifer gain------------------------------------------------------------------------
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
        pwr_out_target = pwr_in * g - (opt_bw*(g - 1)*nf*constants.h*opt_freq/2)
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
            
    config.display_data('Adjusted gain', g, 0, 0)
    # Apply calculated (available gain) to optical channels-----------------------------------------
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
        if ( wave_freq[ch] > (opt_freq - (opt_bw/2))
            and wave_freq[ch] < (opt_freq + (opt_bw/2)) ): #Channel must be within amplifier BW
                g_channels = g/channels
                if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
                    opt_field_out[ch, 0] = opt_field_rcv[ch, 0]*np.sqrt(g_channels)*jones_vector[ch, 0]
                    opt_field_out[ch, 1] = opt_field_rcv[ch, 1]*np.sqrt(g_channels)*jones_vector[ch, 1]
                else:
                    opt_field_out[ch] = opt_field_rcv[ch]*np.sqrt(g_channels)
                noise_field_out[ch] = noise_field_rcv[ch]*np.sqrt(g_channels)
        
    # Amplifier ASE calculation------------------------------------------------------------------------
    nf = np.power(10, nf_db/10)
    psd_ase = (g/channels - 1)*nf*constants.h*opt_freq/2 # Ref 1, Eq 4.34
    psd_ase_dbm = 10*np.log10(psd_ase*1e3)
    pwr_ase_total = psd_ase*opt_bw
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
                    
    # Calculate average power exiting amplifier (all channels)
    pwr_out_amp = 0
    for ch in range(0, channels):
        pwr_out_amp_ch = np.mean(np.square(np.abs(opt_field_out[ch])))
        noise_out_amp_ch = np.mean(np.square(np.abs(noise_field_out[ch])))
        pwr_out_amp += pwr_out_amp_ch + noise_out_amp_ch
    if pwr_out_amp > 0:
        pwr_out_amp_dbm = 10*np.log10(pwr_out_amp*1e3)
    else:
        pwr_out_amp_dbm = 'NA'
                    
    '''==OUTPUT PARAMETERS LIST============================================='''
    opt_amp_parameters = []
    opt_amp_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    opt_amp_results = []
    gain_db = 10*np.log10(g)
    gain_per_ch_db = 10*np.log10(g/channels)
    gain_result =  ['Amplifier total gain (dB)', gain_db, 'dB', ' ', False, '0.3f']
    gain_result_lin =  ['Amplifier total gain (linear)', g, ' ', ' ', False]
    gain_result_per_ch =  ['Amplifier per channel gain (dB)', gain_per_ch_db, 'dB', ' ', False, '0.3f']
    gain_result_lin_per_ch =  ['Amplifier per channel gain (linear)', g/channels, ' ', ' ', False]
    pwr_out_sat_dbm_result = ['Amplifier output saturation pwr (dBm)', pwr_out_sat_dbm, ' dBm', ' ', False, '0.3f']
    psd_amplifier_result = ['Amplifier ASE (avg PSD)', psd_ase, 'A^2/Hz', ' ', False]
    psd_amplifier_dbm_result = ['Amplifier ASE (avg PSD)', psd_ase_dbm, 'dBm/Hz', ' ', False, '0.3f']
    pwr_ase_total_result = ['Amplifier ASE (total pwr)', pwr_ase_total, 'W', ' ', False]
    pwr_ase_total_dbm_result = ['Amplifier ASE (total pwr)', pwr_ase_total_dbm, 'dBm', ' ', False, '0.3f']
    in_pwr_amplifier_result = ['Avg sig/noise pwr entering amp', pwr_in, 'W', ' ', False]
    in_pwr_amplifier_result_dbm = ['Avg sig/noise pwr entering amp', pwr_in_dbm, 'dBm', ' ', False, '0.3f']
    out_pwr_amplifier_result = ['Avg sig/noise pwr exiting amp', pwr_out_amp, 'W', ' ', False]
    out_pwr_amplifier_result_dbm = ['Avg sig/noise pwr exiting amp', pwr_out_amp_dbm, 'dBm', ' ', False, '0.3f' ]
    opt_amp_results = [gain_result, gain_result_lin, gain_result_per_ch, gain_result_lin_per_ch, pwr_out_sat_dbm_result,
                                  psd_amplifier_result, psd_amplifier_dbm_result, 
                                  pwr_ase_total_result, pwr_ase_total_dbm_result, in_pwr_amplifier_result, 
                                  in_pwr_amplifier_result_dbm, out_pwr_amplifier_result, 
                                  out_pwr_amplifier_result_dbm]
                                  
    '''=DATA LIST FOR GRAPHING==========================================='''
    
    if iteration == 1: 
        # First iteration - clear the contents of the gain_db list
        project.gain_db = []
        project.pwr_out_dbm = []
    # List is updated with new gain value over each iteration
    project.gain_db.append(gain_db)
    project.pwr_out_dbm.append(pwr_out_amp_dbm)
     
    if iteration == iterations: 
        # Last iteration - instantiate the xy graph and display results
        project.amplifier_analyzer = view_amp.IterationsAnalyzer_Opt_Amp(project.amp_input_power_dbm, 
                                                                                                    project.gain_db, project.pwr_out_dbm,
                                                                                                    project.gain_db)
        project.amplifier_analyzer.show()

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
        
    return ([[2, signal_type, fs, time_array, psd_out, optical_channels]], 
                 opt_amp_parameters, opt_amp_results)


def large_signal_gain(g, g_o, pwr_out, pwr_sat):
    return g_o*np.exp(-((g-1)/g) * (pwr_out/pwr_sat))
    
def saturated_gain(g, g_o, pwr_in, pwr_sat):
    return 1 + (pwr_sat/pwr_in)*np.log(g_o/g)
