"""
SystemLab-Design Version 20.01.r1
Functional block script: Gaussian Pulse Gen (Optical)
Version 1.0 (17 Dec 2019)

Refs:
1) Wikipedia contributors, "Gaussian function," Wikipedia, The Free Encyclopedia, 
https://en.wikipedia.org/w/index.php?title=Gaussian_function&oldid=910923914
(accessed September 15, 2019). 
2) "Gaussian Pulses and Different Width Definitions", 
https://lr.ttu.ee/irm0120/2016kevad/width_table.pdf (accessed 17-Sep-2019)
3) Optical Communication Systems (OPT428) Govind P. Agrawal, Institute of Optics,
University of Rochester, Rochester, NY (2006)
Slide 195/196, Chirped Gaussian Pulses
http://www2.optics.rochester.edu/users/gpa/opt428b.pdf
"""
import numpy as np
import systemlab_utilities as util
import config
from scipy import constants #https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Gaussian Pulse Gen (Optical)'
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
    #Optical settings-------------------------------------------
    wave_freq = float(parameters_input[1][1])*1e12
    phase_deg = float(parameters_input[2][1])
    pol_azimuth = float(parameters_input[3][1])
    pol_ellipticity = float(parameters_input[4][1])
    e_field_format = str(parameters_input[5][1])
    #Pulse settings---------------------------------------------
    signal_pwr = float(parameters_input[7][1])
    width_model = str(parameters_input[8][1])
    time_units = str(parameters_input[9][1])
    unit_factor = util.adjust_units_time(time_units)
    t0 = float(parameters_input[10][1])*unit_factor
    offset = float(parameters_input[11][1])*unit_factor 
    rep = float(parameters_input[12][1])*unit_factor

    # Additional parameters
    signal_type = 'Optical'
    wave_key = 1
    #wave_freq = constants.c/(wavelength*1e-9) #Hz
    
    '''==CALCULATIONS======================================================='''
    # Polarization settings
    pol_azimuth_rad = (pol_azimuth/180)*np.pi
    pol_ellipticity_rad = (pol_ellipticity/180)*np.pi
    jones_vector = ([np.cos(pol_azimuth_rad)*np.cos(pol_ellipticity_rad) - 
                     1j*np.sin(pol_azimuth_rad)*np.sin(pol_ellipticity_rad),  
                     np.sin(pol_azimuth_rad)*np.cos(pol_ellipticity_rad) + 
                     1j*np.cos(pol_azimuth_rad)*np.sin(pol_ellipticity_rad)])

    # Prepare initial electrical field definition for optical signal
    time_array = np.linspace(0, time, n)
    e_field_array = e_field_array = np.full(n, np.sqrt(signal_pwr*1e-3))
    noise_array = np.zeros(n)
    
    # Build electrial field
    # Slowly varying envelope approximation ( E(z,t) = Eo(z, t)*exp(i(kz - wt)) )
    phase_rad = (phase_deg/180)*np.pi
    e_field_array_real = np.zeros(n)
    e_field_array_imag = np.zeros(n)
    e_field_env = np.full(n, 0 + 1j*0, dtype=complex) 
    if e_field_format == 'Exy':
        e_field_env = np.full(n, 0 + 1j*0, dtype=complex)
        e_field_env_total = np.full(n, 0 + 1j*0, dtype=complex)
    else:
        e_field_env = np.full([2, n], 0 + 1j*0, dtype=complex)
        e_field_env_total = np.full([2, n], 0 + 1j*0, dtype=complex)
    
    for i in range(0,n): #Add intial phase setting to complex envelope
        e_field_array_real[i] = e_field_array[i]*np.cos(phase_rad)
        e_field_array_imag[i] = e_field_array[i]*np.sin(phase_rad)
        if e_field_format == 'Exy':
            e_field_env[i] = e_field_array_real[i] + 1j*e_field_array_imag[i]  
        else:
            e_field_env[0][i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
            e_field_env[1][i] = e_field_array_real[i] + 1j*e_field_array_imag[i]
    
    # Width definitions (wrt to t_zero)
    # 1/e width : Amplitude: sqrt(2)*t_zero, Power: t_zero (1/e = 1/2.718282 = 0.367879)
    # FWHM: Amplitude: sqrt(8*log(2))*t_zero, Power: sqrt(4*log(2))*t_zero
    # RMS: Amplitude: t_zero, Power: (1/sqrt(2))*t_zero
    if width_model == 'FWHM (pwr)':
        t0 = t0/(2*np.sqrt(np.log(2)))
    
    for i in range(0, n):
        if e_field_format == 'Exy':
            e_field_env[i] = e_field_array[i] * np.exp(-(np.square(time_array[i] - offset))/(2*np.square(t0))) 
        else:
            e_field_env[0][i] = e_field_array[i] * np.exp(-(np.square(time_array[i] - offset))/(2*np.square(t0))) 
            e_field_env[1][i] = e_field_array[i] * np.exp(-(np.square(time_array[i] - offset))/(2*np.square(t0))) 
            
    # Apply Jones vector to Ex and Ey complex arrays
    if e_field_format == 'Ex-Ey':
        e_field_env[0] = jones_vector[0]*e_field_env[0]
        e_field_env[1] = jones_vector[1]*e_field_env[1]
        
    # Setup pulses
    total_pulses = 0
    if rep > 0:
        total_pulses = int(np.round(time/rep))
        pulse_spacing = int(np.round(rep*fs))
        for p in range(0, total_pulses):
            e_field_env_total =  np.roll(e_field_env, int(pulse_spacing*p)) + e_field_env_total
    else:
        e_field_env_total = e_field_env
    
    # Noise groups (freq domain) - set to zero
    freq_start = 192e14
    freq_end = 194e14
    ng = 20
    freq_delta = freq_end - freq_start
    ng_w = freq_delta/ng
    freq_points = np.linspace(freq_start + (ng_w/2), freq_end - (ng_w/2), ng)
    psd_points = np.full(ng, 0)
    psd_array = np.array([freq_points, psd_points])
        
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    opt_gaussian_parameters = []
    opt_gaussian_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    opt_gaussian_results = []
    
    spectral_width = 1/t0
    spectral_width_result = ['Pulse spectral width (GHz)', spectral_width*1e-9, 'GHz', ' ', False]
    opt_gaussian_results = [spectral_width_result]
    
    '''==RETURN (Output Signals, Parameters, Results)=================================='''
    optical_1 = [wave_key, wave_freq, jones_vector, e_field_env_total, noise_array]
    optical = [optical_1]
    
    return ([[1, signal_type, fs, time_array, psd_array, optical]], opt_gaussian_parameters, opt_gaussian_results)

