"""
SystemLab-Design Version 20.01.r1
Functional block script: Optical Noise Source
Version 2.0 (26 Sep 2019)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
"""
import numpy as np
import config
from scipy import constants #https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Noise Source'
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
    wavelength = float(parameters_input[0][1]) #Optical wavelength (nm)
    # Frequency domain noise groups (header)
    psd_freq = float(parameters_input[2][1])
    ng = int(parameters_input[3][1])
    freq_start = float(parameters_input[4][1])
    freq_end = float(parameters_input[5][1])
    add_ase = int(parameters_input[6][1])

    # Additional parameters
    signal_type = 'Optical'
    wave_key = 1
    wave_freq = constants.c/(wavelength*1e-9) #Hz
    
    '''==CALCULATIONS======================================================='''
    jones_vector = ([1/np.sqrt(2)+ 1j*0, 1/np.sqrt(2) + 1j*0]) # 50% in X, 50% in Y

    # Prepare initial electrical field definition for optical signal
    time_array = np.linspace(0, time, n)
    e_field_array = np.full(n, 0)
    noise_array = np.zeros(n)
    
    # Build electrial field
    # Slowly varying envelope approximation ( E(z,t) = Eo(z, t)*exp(i(kz - wt)) )
    # e_field_env = E(z,t); w is carried separately as wave_freq = c/optical wavelength
    e_field_array_real = np.zeros(n)
    e_field_array_imag = np.zeros(n)
    e_field_env = np.full(n, 0 + 1j*0, dtype=complex) 
    
    #Noise groups (freq domain)
    freq_delta = freq_end - freq_start
    ng_w = freq_delta/ng
    freq_points = np.linspace(freq_start + (ng_w/2), freq_end - (ng_w/2), ng)
    psd_points = np.full(ng, psd_freq)
    psd_array = np.array([freq_points, psd_points])
    
    if add_ase == 2:
        # Build time-domain freq points
        T = n/fs
        k = np.arange(n)
        frq = (k/T)
        frq = frq - frq[int(round(n/2))] + wave_freq
        ng_w = psd_array[0, 1] - psd_array[0, 0]
        pwr_opt_noise = 0
        for i in range(0, ng):
            if psd_array[0, i] > frq[0] and psd_array[0, i] < frq[n-1]:
                pwr_opt_noise += psd_array[1, i]*ng_w
                
        #Convert to time-domain noise
        sigma = np.sqrt(pwr_opt_noise)
        noise_opt = np.random.normal(0, sigma , n)
        noise_array += noise_opt
        
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    opt_noise_parameters = []
    opt_noise_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    opt_noise_results = []

    psd_freq_dbm = 10*np.log10(psd_freq*1e3)
    psd_freq_dbm_result = ['Noise PSD', psd_freq_dbm, 'dBm/Hz', ' ', False]
    opt_noise_results = [psd_freq_dbm_result]

    '''==RETURN (Output Signals, Parameters, Results)=================================='''
    optical_1 = [wave_key, wave_freq, jones_vector, e_field_env, noise_array]
    optical = [optical_1]
    
    return ([[1, signal_type, fs, time_array, psd_array, optical]], opt_noise_parameters, opt_noise_results)

