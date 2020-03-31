"""
SystemLab-Design Version 20.01.r1
Functional block script: Optical Cross Coupler (Uni-directional)
Version 1.0 (19.02 23 Feb 2019)
Version 2.0 (9-Sep-2019)
Note: This model currently supports one optical channel per input port (additional 
channels will not be processed)
Refs:
1) Cvijetic, M., and , Advanced Optical Communication Systems and Networks, 
(Artech House Applied Photonics) (Kindle Locations 18576-18577). Artech House.
Kindle Edition. 
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Cross Coupler'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate']
        
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
    #Load parameters from FB parameters table [row][column]
    #Parameter name(0), Value(1), Units(2), Notes(3)
    cc = float(parameters_input[0][1]) #Coupling ratio (power)
    
    '''==INPUT SIGNALS======================================================'''
    # Load optical group data from input port 1 (upper)
    signal_type = 'Optical'
    time_array = input_signal_data[0][3] # Sampled time array
    psd_array_p1 = input_signal_data[0][4] # Noise groups
    opt_channels_p1 = input_signal_data[0][5] #Optical channel list

    # Load frequency, jones vector, signal & noise field envelopes for each optical channel of port 1
    channels_p1 = len(opt_channels_p1)
    wave_key_p1 = np.empty(channels_p1)
    wave_freq_p1 = np.empty(channels_p1)
    jones_vector_p1 = np.full([channels_p1, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels_p1[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv_p1 = np.full([channels_p1, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv_p1 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex)
    noise_field_rcv_p1 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels_p1): #Load wavelength channels
        wave_key_p1[ch] = opt_channels_p1[ch][0]
        wave_freq_p1[ch] = opt_channels_p1[ch][1]
        jones_vector_p1[ch] = opt_channels_p1[ch][2]
        opt_field_rcv_p1[ch, :] = opt_channels_p1[ch][3]
        noise_field_rcv_p1[ch, :] = opt_channels_p1[ch][4]
    
    # Load optical group data from input port 2 (lower)
    signal_type = 'Optical'
    time_array = input_signal_data[1][3] # Sampled time array
    psd_array_p2 = input_signal_data[1][4] # Noise groups
    opt_channels_p2 = input_signal_data[1][5] #Optical channel list

    # Load frequency, jones vector, signal & noise field envelopes for each optical channel of port 2
    channels_p2 = len(opt_channels_p2)
    wave_key_p2 = np.empty(channels_p2)
    wave_freq_p2 = np.empty(channels_p2)
    jones_vector_p2 = np.full([channels_p2, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels_p2[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv_p2 = np.full([channels_p2, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv_p2 = np.full([channels_p2, n], 0 + 1j*0, dtype=complex)
    noise_field_rcv_p2 = np.full([channels_p2, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels_p2): #Load wavelength channels
        wave_key_p2[ch] = opt_channels_p2[ch][0]
        wave_freq_p2[ch] = opt_channels_p2[ch][1]
        jones_vector_p2[ch] = opt_channels_p2[ch][2]
        opt_field_rcv_p2[ch, :] = opt_channels_p2[ch][3]
        noise_field_rcv_p2[ch, :] = opt_channels_p2[ch][4]
        
    '''==CALCULATIONS======================================================='''   
    # 2x2 symmetric optical coupler (scattering matrix) (Ref 1 - Eq 2.119)
    # t = s11/s22 = cos(kL) = , r = s12/s21 = j*sin(kL) where k is coupling coefficient & L is coupling length
    # s11/s22 = sqrt(1-cc), s12/s21 = j*sqrt(cc)
    # E1_out = s11*E1_in + s12*E2_in, E2_out = s21*E1_in + s22*E2_in
    if opt_channels_p1[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_output_p3 = np.full([channels_p1, 2, n], 0 + 1j*0, dtype=complex) 
        opt_field_output_p4 = np.full([channels_p1, 2, n], 0 + 1j*0, dtype=complex)
    else: # Polarization format: Exy
        opt_field_output_p3 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex) 
        opt_field_output_p4 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex)
    noise_field_output_p3 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex) 
    noise_field_output_p4 = np.full([channels_p1, n], 0 + 1j*0, dtype=complex)
    
    # Calculate fields exiting ports 3/4 (based on input fields at ports 1/2)
    # Only first channel is used for this model
    opt_field_output_p3[0] = opt_field_rcv_p1[0]*(np.sqrt(1-cc)) + opt_field_rcv_p2[0]*(1j*np.sqrt(cc))
    opt_field_output_p4[0] = opt_field_rcv_p1[0]*(1j*np.sqrt(cc)) + opt_field_rcv_p2[0]*(np.sqrt(1-cc)) 
    noise_field_output_p3[0] = noise_field_rcv_p1[0]*(np.sqrt(1-cc)) + noise_field_rcv_p2[0]*(1j*np.sqrt(cc))
    noise_field_output_p4[0] = noise_field_rcv_p1[0]*(1j*np.sqrt(cc)) + noise_field_rcv_p2[0]*(np.sqrt(1-cc)) 
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    optical_coupler_parameters = []
    optical_coupler_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    optical_coupler_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''  
    optical_channels_p3 = []
    optical_channels_p4 = []
    #Only use first channel and assume they have same wave_key/wavelength (based on p1)
    opt_ch_p3 = [int(wave_key_p1[0]), wave_freq_p1[0], jones_vector_p1[0], opt_field_output_p3[0], noise_field_output_p3[0]]
    optical_channels_p3.append(opt_ch_p3)
    opt_ch_p4 = [int(wave_key_p1[0]), wave_freq_p1[0], jones_vector_p1[0], opt_field_output_p4[0], noise_field_output_p4[0]]
    optical_channels_p4.append(opt_ch_p4)
    
    '''for ch in range(0, channels_p1):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_output[ch, :], noise_field_output[ch, :]]
        optical_channels.append(opt_ch)'''

    return ([[3, signal_type, fs, time_array, psd_array_p1, optical_channels_p3],
             [4, signal_type, fs, time_array, psd_array_p1, optical_channels_p4]], 
              optical_coupler_parameters, optical_coupler_results)

