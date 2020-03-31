"""
Noise source module
"""
import numpy as np
import config
from scipy import constants
# REF: https://docs.scipy.org/doc/scipy/reference/constants.html

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Noise Source - Electrical'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    noise_model = str(parameters_input[0][1]) #Noise model (Power, PSD)
    noise_pwr_dbm = float(parameters_input[1][1]) #Noise power (W)
    psd_dbm = float(parameters_input[2][1]) #Power spectral density of noise (dBm/Hz)
    noise_temp = float(parameters_input[3][1]) #Temp for calculating source thermal noise (K)
    add_noise_to_sig = int(parameters_input[4][1]) #Add noise to signal

    carrier = 0
    sig_type = 'Electrical'
    
    '''==CALCULATIONS======================================================='''
    time_array = np.linspace(0, time, n)
    signal_array = np.zeros(n)
    noise_pwr_linear = 0
    psd_linear_w = 0
    
    if noise_model == 'Power':
        noise_pwr_linear = np.power(10, (noise_pwr_dbm-30)/10) #Convert from dBm to W
        sigma = np.sqrt(noise_pwr_linear/n)
    elif noise_model == 'PSD':
        psd_linear_w = np.power(10, (psd_dbm-30)/10)
        sigma = np.sqrt(psd_linear_w*fs/n)
    else:
        psd_linear_thermal = constants.k*noise_temp
        sigma = np.sqrt(psd_linear_thermal*fs/n)

    noise_array = np.random.normal(0, sigma, n)
    if add_noise_to_sig == 2:
        signal_array = noise_array
    
    #Re-calculate total power of output signal
    total_noise_pwr = np.sum(np.square(noise_array))
    total_noise_dbm = 10*np.log10(total_noise_pwr) + 30
    psd = total_noise_dbm - 10*np.log10(fs)
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    noise_parameters = []
    noise_parameters = parameters_input #No changes were made to parameters
  
    '''==RESULTS============================================================'''
    noise_results = []
    noise_pwr_measured = ['Noise power measured (W)',  total_noise_pwr, 'W', ' ', False]
    noise_pwr_measured_dbm = ['Noise power measured (dBm)',  total_noise_dbm, 'dBm', ' ', False]
    psd_result = ['PSD measured (dBm/Hz)', psd, 'dBm/Hz', ' ', False]
    noise_results = [noise_pwr_measured, noise_pwr_measured_dbm, psd_result]

    return ( [[1, sig_type, carrier, fs, time_array, signal_array, noise_array]], 
                noise_parameters, noise_results )



