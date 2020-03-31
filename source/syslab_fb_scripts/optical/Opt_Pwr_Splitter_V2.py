"""
SystemLab-Design Version 20.01.r1
Functional block script: Optical Power Splitter
Version 1.0 (19.02 23 Feb 2019)
Version 2.0 (12 Nov 2019)

Notes:
1) All channels are processed with same coupling coefficient and phase shift (wavelength-independent)
2) The psd array (for the input optical group) is not currently split (to be updated in future)

Refs:
1) Cvijetic, M., and , Advanced Optical Communication Systems and Networks, 
(Artech House Applied Photonics) (Kindle Locations 18576-18577). Artech House.
Kindle Edition. 
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Splitter'
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
    cc = float(parameters_input[0][1]) #Coupling coefficient
    loss_db = float(parameters_input[1][1]) #Insertion loss
    include_ph = int(parameters_input[2][1]) #Include phase shift
    
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
    # 2x2 optical coupler (scattering matrix)
    # s11 = sqrt(1-cc), s12 = j*sqrt(cc), s21 = j*sqrt(cc), s22 = sqrt(1-cc)
    # E1_out = s11*E1_in + s12*E2_in = s11*E1_in (E2_in = 0)
    # E2_out = s21*E1_in + s22*E2_in = s21*E1_in (E2_in = 0)
    if opt_channels[0][3].ndim == 2:
        opt_field_output_p1 = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
        opt_field_output_p2 = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_output_p1 = np.full([channels, n], 0 + 1j*0, dtype=complex) 
        opt_field_output_p2 = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_output_p1 = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_output_p2 = np.full([channels, n], 0 + 1j*0, dtype=complex)
    # Convert loss (dB) to linear
    loss_linear = np.power(10, -loss_db/10)
    for ch in range(0, channels):
        if include_ph == 2:
            opt_field_output_p1[ch, :] = opt_field_rcv[ch, :]*(np.sqrt(1-cc))*np.sqrt(loss_linear)
            opt_field_output_p2[ch, :] = opt_field_rcv[ch, :]*(-1j*np.sqrt(cc))*np.sqrt(loss_linear)
            noise_field_output_p1[ch, :] = noise_field_rcv[ch, :]*(np.sqrt(1-cc))*np.sqrt(loss_linear)
            noise_field_output_p2[ch, :] = noise_field_rcv[ch, :]*(-1j*np.sqrt(cc))*np.sqrt(loss_linear)
        else:
            opt_field_output_p1[ch, :] = opt_field_rcv[ch, :]*(np.sqrt(1-cc))*np.sqrt(loss_linear)
            noise_field_output_p1[ch, :] = noise_field_rcv[ch, :]*(np.sqrt(1-cc))*np.sqrt(loss_linear)
            opt_field_output_p2[ch, :] = opt_field_rcv[ch, :]*(np.sqrt(cc))*np.sqrt(loss_linear)
            noise_field_output_p2[ch, :] = noise_field_rcv[ch, :]*(np.sqrt(cc))*np.sqrt(loss_linear)
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    optical_splitter_parameters = []
    optical_splitter_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    optical_splitter_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels_p1 = []
    optical_channels_p2 = []
    for ch in range(0, channels):
        opt_ch_1 = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_output_p1[ch, :], noise_field_output_p1[ch, :]]
        optical_channels_p1.append(opt_ch_1)
        opt_ch_2 = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_output_p2[ch, :], noise_field_output_p2[ch, :]]
        optical_channels_p2.append(opt_ch_2)
      
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels_p1],
             [3, signal_type, fs, time_array, psd_array, optical_channels_p2]], 
              optical_splitter_parameters,  optical_splitter_results)

