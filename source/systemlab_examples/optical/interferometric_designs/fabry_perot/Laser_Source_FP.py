"""
Laser Source (Fabry_Perot interferometer project)
"""

import numpy as np
import config
import project_fabry_perot as project
from scipy import constants
# REF: https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Laser Source'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    iterations = settings['iterations']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']
    
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
        config.app.processEvents()
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    #General parameters (header)
#    wavelength = float(parameters_input[1][1]) #Optical wavelength (nm)
    optical_pwr = float(parameters_input[2][1]) #Optical power (mW)
    line_width = float(parameters_input[3][1]) #Laser linewidth (MHz)
    phase_deg = float(parameters_input[4][1]) #Optical phase (deg)
    #Relative intensity noise (header)
    ref_bw = float(parameters_input[6][1]) #Reference bandwidth (Hz)
    rin = float(parameters_input[7][1]) #RIN (dB/Hz)
    add_rin_to_signal = int(parameters_input[8][1]) #Add RIN to signal
    #Polarization settings (header)
    pol_azimuth = float(parameters_input[10][1])
    pol_ellipticity = float(parameters_input[11][1])

    #Additional parameters
    signal_type = 'Optical'
    wave_key_1 = 'Ch1'
    
    '''==CALCULATIONS======================================================='''        
    freq_start = 100e12 #Hz
    freq_end = 200e12 #nm
    delta = freq_end - freq_start
    wave_freq = freq_start
    if iterations > 1:
        wave_freq = freq_start + ((iteration-1)/(iterations-1))*delta
    
    #Polarization settings
    pol_azimuth_rad = (pol_azimuth/180)*np.pi
    pol_ellipticity_rad = (pol_ellipticity/180)*np.pi
    jones_vector = ([np.cos(pol_azimuth_rad)*np.cos(pol_ellipticity_rad) - 
                     1j*np.sin(pol_azimuth_rad)*np.sin(pol_ellipticity_rad),  
                     np.sin(pol_azimuth_rad)*np.cos(pol_ellipticity_rad) + 
                     1j*np.cos(pol_azimuth_rad)*np.sin(pol_ellipticity_rad)])

    #Prepare initial electrical field definition for optical signal
    time_array = np.linspace(0, time, n)
    e_field_array = np.full(n, np.sqrt(optical_pwr*1e-3))
    
    #Add RIN to field values (if selected)
    if add_rin_to_signal == 1:
        rin_linear = np.power(10, rin/10)
        noise_pwr = rin_linear * ref_bw * optical_pwr*1e-3
        sigma_field = np.sqrt(np.sqrt(noise_pwr))
        rin_noise_array = np.random.normal(0, sigma_field , n)
        e_field_array = e_field_array + rin_noise_array
    
    #Build electrial field
    # Slowly varying envelope approximation - optical phase and 
    # amplitude are assumed to be constant over simulation time window
    phase_rad = (phase_deg/180)*np.pi
    e_field_array_real = np.zeros(n)
    e_field_array_imag = np.zeros(n)
    e_field_env = np.full(n, 0 + 1j*0, dtype=complex) 
    
    for i in range(0,n):
        e_field_array_real[i] = e_field_array[i]*np.cos(phase_rad)
        e_field_array_imag[i] = e_field_array[i]*np.sin(phase_rad)
        e_field_env[i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
        
    #Optical noise settings
    #Time domain noise array
    noise_array = np.zeros(n)
    #Noise groups
    ng = 20
    freq_start = 193e12
    freq_end = 194e12
    freq_delta = freq_end - freq_start
    ng_w = freq_delta/ng
    freq_points = np.linspace(freq_start + (ng_w/2), freq_end - (ng_w/2), ng)
    psd_points = np.full(ng, 1e-11)
    psd_array = np.array([freq_points, psd_points])
    
    #Add phase noise to field envelope (Brownian randon walk)
    phase_sigma = np.sqrt(np.pi*2*line_width*1e6)
    phase = phase_rad
    phase_array = np.full(n, phase)
    
    for i in range(1,n):
        phase_walk = np.random.normal(0, phase_sigma)*np.sqrt(t_step)
        phase_array[i] = phase_array[i-1] + phase_walk
        e_field_array_real[i] = e_field_array[i]*np.cos(phase_array[i])
        e_field_array_imag[i] = e_field_array[i]*np.sin(phase_array[i])
        e_field_env[i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
        
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    laser_parameters = []
    laser_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    laser_results = []
    
    if iteration == 1:
        project.wave = []
        project.wave.append(wave_freq)
    else:
        project.wave.append(wave_freq)
    
    optical_1 = [wave_key_1, wave_freq, jones_vector, e_field_env, noise_array, psd_array]
    optical = [optical_1]
    
    return ([[1, signal_type, fs, time_array, optical]], laser_parameters, laser_results)

