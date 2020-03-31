"""
SystemLab-Design Version 20.01.r1
Functional block script: Optical Power Splitter (4 Port)
Version 1.0 (23 Feb 2019)

Refs:
1) Cvijetic, M., and , Advanced Optical Communication Systems and Networks, 
(Artech House Applied Photonics) (Kindle Locations 18576-18577). Artech House.
Kindle Edition. 
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Splitter (4 Port)'
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
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Parameter name(0), Value(1), Units(2), Notes(3)
    loss_db = float(parameters_input[0][1]) #Insertion loss
    
    '''==INPUT SIGNALS======================================================'''
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
    if opt_channels[0][3].ndim == 2:
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex)  
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector[ch] = opt_channels[ch][2]
        opt_field_rcv[ch] = opt_channels[ch][3]
        noise_field_rcv[ch] = opt_channels[ch][4]
    
    '''==CALCULATIONS======================================================='''
    if opt_channels[0][3].ndim == 2:
        opt_field_output = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_output = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_output = np.full([channels, n], 0 + 1j*0, dtype=complex)
    loss_linear = np.power(10, -loss_db/10)
    for ch in range(0, channels):
        opt_field_output[ch] = (np.sqrt(0.25))*opt_field_rcv[ch, :]*np.sqrt(loss_linear)
        noise_field_output[ch] = (np.sqrt(0.25))*noise_field_rcv[ch, :]*np.sqrt(loss_linear)
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    opt_splitter_parameters = []
    opt_splitter_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    opt_splitter_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_output[ch], noise_field_output[ch]]
        optical_channels.append(opt_ch)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels],
                  [3, signal_type, fs, time_array, psd_array, optical_channels],
                  [4, signal_type, fs, time_array, psd_array, optical_channels],
                  [5, signal_type, fs, time_array, psd_array, optical_channels]],
                  opt_splitter_parameters, opt_splitter_results)

