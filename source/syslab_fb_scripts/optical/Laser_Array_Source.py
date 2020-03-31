"""
SystemLab-Design Version 20.01.r1
Functional block script: Laser Source
Version 1.0 (23-Dec-2019)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
"""
import numpy as np
import config

from scipy import constants #https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Laser Array Source'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
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
    
    '''==INPUT PARAMETERS========================================================='''
    # Load parameters from FB parameters table
    # Parameter name(0), Value(1), Units(2), Notes(3)   
    #Channel parameters (header)
    channels = int(parameters_input[1][1]) #Number of optical channels
    wave_units = str(parameters_input[2][1])
    start_freq =  float(parameters_input[3][1]) #First channel frequency
    if wave_units == 'Wavelength (nm)':
        start_freq = 1e-3*constants.c/start_freq
    delta_freq = float(parameters_input[4][1]) #Channel spacing (GHz)
    #Main settings (all channels)
    optical_pwr = float(parameters_input[6][1]) #Optical power (mW)
    line_width = float(parameters_input[7][1]) #Laser linewidth (MHz)
    phase_deg = float(parameters_input[8][1]) #Optical phase (deg)
    # Relative intensity noise (header)
    ref_bw = float(parameters_input[10][1]) #Reference bandwidth (Hz)
    rin = float(parameters_input[11][1]) #RIN (dB/Hz)
    add_rin_to_signal = int(parameters_input[12][1]) #Add RIN to signal
    # Polarization settings (header)
    pol_azimuth = float(parameters_input[14][1])
    pol_ellipticity = float(parameters_input[15][1])
    e_field_format = str(parameters_input[16][1])
    # Frequency domain noise groups (header)
    psd_freq = float(parameters_input[18][1])
    ng = int(parameters_input[19][1])
    freq_start = float(parameters_input[20][1])
    freq_end = float(parameters_input[21][1])
    add_ase = int(float(parameters_input[22][1]))

    # Additional parameters
    signal_type = 'Optical'
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    
    '''==CALCULATIONS======================================================='''

    # Polarization settings
    pol_azimuth_rad = (pol_azimuth/180)*np.pi
    pol_ellipticity_rad = (pol_ellipticity/180)*np.pi
    jones_vector = ([np.cos(pol_azimuth_rad)*np.cos(pol_ellipticity_rad) - 
                     1j*np.sin(pol_azimuth_rad)*np.sin(pol_ellipticity_rad),  
                     np.sin(pol_azimuth_rad)*np.cos(pol_ellipticity_rad) + 
                     1j*np.cos(pol_azimuth_rad)*np.sin(pol_ellipticity_rad)])

    # Prepare initial electrical field definitions for optical signals
    time_array = np.linspace(0, time, n)
    e_field_array = np.full([channels, n], np.sqrt(optical_pwr*1e-3))
    if e_field_format == 'Exy':
        e_field_env = np.full([channels, n], 0 + 1j*0, dtype=complex)
    else:
        e_field_env = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
    noise_array = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    
    for ch in range(0,channels): #Loop through all optical channels
        wave = start_freq*1e12 + ch*delta_freq*1e9
        wave_key[ch] = ch+1
        wave_freq[ch] = wave #Hz
    
        #Add RIN to field values (if selected) - Ref 1, Eq 4.127
        if add_rin_to_signal == 2:
            rin_linear = np.power(10, rin/10)
            noise_pwr = rin_linear * ref_bw * (optical_pwr*1e-3)**2
            #Penalty (noise var) at receiver is: 2*(RP1)^2*RIN*BW
            sigma_field = np.sqrt(np.sqrt(noise_pwr))
            noise_array[ch, :] = np.random.normal(0, sigma_field , n)
            e_field_array[ch, :] = e_field_array[ch, :] + noise_array[ch, :]
    
        # Build electrial field
        # Slowly varying envelope approximation ( E(z,t) = Eo(z, t)*exp(i(kz - wt)) )
        # e_field_env = E(z,t); w is carried separately as wave_freq 
        phase_rad = (phase_deg/180)*np.pi
        e_field_array_real = np.zeros(n)
        e_field_array_imag = np.zeros(n)
    
        for i in range(0,n): #Add intial phase setting to complex envelope
            e_field_array_real[i] = e_field_array[ch, i]*np.cos(phase_rad)
            e_field_array_imag[i] = e_field_array[ch, i]*np.sin(phase_rad)
            if e_field_format == 'Exy':
                e_field_env[ch, i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
            else:
                e_field_env[ch, 0, i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
                e_field_env[ch, 1, i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
            
        #Noise groups (freq domain)
        freq_delta = freq_end - freq_start
        ng_w = freq_delta/ng
        freq_points = np.linspace(freq_start + (ng_w/2), freq_end - (ng_w/2), ng)
        psd_points = np.full(ng, psd_freq)
        psd_array = np.array([freq_points, psd_points])
    
        # Integrate ase noise with time-domain noise?
        if add_ase == 2:
            # Build time-domain freq points
            T = n/fs
            k = np.arange(n)
            frq = (k/T)
            frq = frq - frq[int(round(n/2))] + wave_freq[ch]
            ng_w = psd_array[0, 1] - psd_array[0, 0]
            pwr_ase = 0
            for i in range(0, ng):
                if psd_array[0, i] > frq[0] and psd_array[0, i] < frq[n-1]:
                    pwr_ase += psd_array[1, i]*ng_w
            
            #Convert to time-domain noise
            sigma_ase = np.sqrt(pwr_ase)
            noise_ase = np.random.normal(0, sigma_ase , n)
            noise_array[ch, :] += noise_ase
            
        #Add phase noise to field envelope (Brownian randon walk) - Ref 1, Eq. 4.7
        phase_sigma = np.sqrt(np.pi*2*line_width*1e6)
        phase = phase_rad
        phase_array = np.full(n, phase)
    
        for i in range(1,n):
            phase_walk = np.random.normal(0, phase_sigma)*np.sqrt(t_step)
            phase_array[i] = phase_array[i-1] + phase_walk
            e_field_array_real[i] = e_field_array[ch, i]*np.cos(phase_array[i])
            e_field_array_imag[i] = e_field_array[ch, i]*np.sin(phase_array[i])
            if e_field_format == 'Exy':
                e_field_env[ch, i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
            else:
                e_field_env[ch, 0, i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
                e_field_env[ch, 1, i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
                
        # Apply Jones vector to Ex and Ey complex arrays
        if e_field_format == 'Ex-Ey':
            e_field_env[ch, 0] = jones_vector[0]*e_field_env[ch, 0]
            e_field_env[ch, 1] = jones_vector[1]*e_field_env[ch, 1]
            
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    laser_parameters = []
    laser_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    laser_results = []
    laser_pwr = np.sum(np.abs(e_field_env)*np.abs(e_field_env))/n
    laser_pwr_dbm = 10*np.log10(laser_pwr*1e3)
    laser_pwr_dbm_result = ['Laser per channel power (dBm)', laser_pwr_dbm, 'dBm', ' ', False]
    laser_results.append(laser_pwr_dbm_result)
    wavelength = np.empty(channels)
    
    for ch in range(0,channels): #Loop through all optical channels
        wavelength[ch] = constants.c/wave_freq[ch] #m
        frequency_result =  ['Laser frequency (THz) - Ch '+ str(ch+1), wave_freq[ch]*1e-12, 'THz', ' ', False, '3.3f']
        wavelength_result = ['Laser wavelength (nm) - Ch ' + str(ch+1), wavelength[ch]*1e9, 'nm', ' ', False, '4.2f']
        laser_results.append(frequency_result)
        laser_results.append(wavelength_result)
        
    header_pol_results = ['Polarization data', '', '', '', True]
    azimuth_result = ['Polarization (azimuth)', pol_azimuth, 'deg', ' ', False]
    ellipticity_result = ['Polarization (ellipticity)', pol_ellipticity, 'deg', ' ', False]
    pol_list = [header_pol_results, azimuth_result, ellipticity_result]
    laser_results.extend(pol_list)
    
    '''#Send update to data box (laser_array_1)
    config.data_tables['laser_array_1'] = []
    for ch in range(0, channels):
        data_1 = ['Laser wavelength (nm) - Ch '+ str(ch+1), wavelength[ch]*1e9, '4.2f', ' ']
        data_list = [data_1]
        config.data_tables['laser_array_1'] .extend(data_list)'''

    '''==RETURN (Output Signals, Parameters, Results)=================================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector, e_field_env[ch], noise_array[ch]]
        optical_channels.append(opt_ch)
    
    return ([[1, signal_type, fs, time_array, psd_array, optical_channels]], laser_parameters, laser_results)

