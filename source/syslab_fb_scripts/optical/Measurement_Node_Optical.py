"""
SystemLab-Design Version 20.01.r1
Measurement node (Optical)
"""
import config
import numpy as np
from scipy import constants
#https://docs.scipy.org/doc/scipy/reference/constants.html
c = constants.c # Speed of light (m/s)
h = constants.h # Planck constant

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS===================================================='''
    module_name = 'Measurement Node (Optical)'
    # Main settings
    n = settings['num_samples'] # Total samples for simulation
    n = int(round(n))
    time = settings['time_window'] # Time window for simulation (sec)
    fs = settings['sampling_rate'] # Sample rate (default - Hz)
    f_sym = settings['symbol_rate'] # Symbol rate (default - Hz)
    samples_sym = settings['samples_per_sym'] # Samples per symbol
    t_step = settings['sampling_period'] # Sample period (Hz)
    # Iteration settings
    iteration = settings['current_iteration'] # Current iteration loop for simulation
    i_total = settings['iterations'] # Total iterations for simulation
    # Feedback settings
    segments = settings['feedback_segments'] # Number of integration segments
    segment = settings['feedback_current_segment'] # Current integration segment
    segment = int(round(segment))
    samples_segment = settings['samples_per_segment'] #Samples per feedback segment
    feedback_mode = settings['feedback_enabled'] #Feedback mode is enabled(2)/disabled(0)
    
    '''==Status message (send to Simulation status panel)==============================='''
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))                                     
                                          
    '''==INPUT PARAMETERS====================================================='''
    # Load parameters from FB parameters table [row][column]
    carrier_data_setting = str(parameters_input[0][1])
    display_x_y = int(parameters_input[1][1])
    display_x = int(parameters_input[2][1])
    display_y = int(parameters_input[3][1])
    time_period = float(parameters_input[4][1])
    
    '''==INPUT SIGNALS=====================================================
    Optical_signal: portID(0), sig_type(1), fs(2), time_array(3), psd_array(4), optical_group(5)
    Optical_channel(s): wave_key(0), wave_freq(1), jones_vector(2), e_field_array(3), noise_array(4)
    '''
    # Load optical group data from input port
    signal_type = input_signal_data[0][1]
    time_array = input_signal_data[0][3] 
    psd_array = input_signal_data[0][4] 
    opt_channels = input_signal_data[0][5] 
    # Load frequency, jones vector, signal & noise field envelopes for each optical channel
    channels = len(opt_channels)
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    pol_format = 'Exy'
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        pol_format = 'Ex-Ey'
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
    
    '''==CALCULATIONS/RESULTS================================================'''
    # Initialize results and data panel lists
    meaure_node_results = []
    #config.data_tables['opt_meas_1'] = []
    num_format_1 = '0.3E'
    num_format_2 = '0.1f'
    for ch in range(0, channels):
        # Prepare and add carrier data to results list
        wavelength = c/wave_freq[ch]
        if carrier_data_setting == 'Frequency':
            title_text = ('Optical metrics (THz) - Ch '+ str(ch+1) + ' (' 
                               + str(format(wave_freq[ch]*1e-12, '3.3f')) + ')')
        else:
            title_text = ('Optical metrics (nm) - Ch ' + str(ch+1) + ' (' 
                               + str(format(wavelength*1e9, '4.2f')) + ')')
        carrier_result =  [title_text, '', '', '', True]
        meaure_node_results.append(carrier_result)
        carrier_data_panel =  [title_text, '', '', '']
        #config.data_tables['opt_meas_1'].append(carrier_data_panel)
        # Calculate and add signal metrics to results list
        # X/Y-polarization data
        if display_x_y == 2: 
            tot_sig_pwr, avg_sig_pwr, ph_rate = calculate_signal_metrics('x-y', pol_format, opt_field_rcv[ch],
                                                                                                    jones_vector[ch], wave_freq[ch], n, time_period)
            photons_per_bit = ph_rate
            # Results list
            data_1 = ['Total signal power (X+Y)', tot_sig_pwr, 'W', '', False, num_format_1]
            data_2 = ['Average signal power (X+Y)', avg_sig_pwr, 'W', '', False, num_format_1]
            data_3 = ['Avg photons/bit (X+Y)', ph_rate, '', '', False, num_format_2]
            data_list = [data_1, data_2, data_3]
            meaure_node_results.extend(data_list)
            '''# Data panel list
            data_1 = ['Total signal power (X+Y)', tot_sig_pwr, num_format_1, 'W']
            data_2 = ['Average signal power (X+Y)',  avg_sig_pwr, num_format_1, 'W']
            data_3 = ['Avg photons/bit (X+Y)', ph_rate, num_format_2, '']
            data_list = [data_1, data_2, data_3]
            config.data_tables['opt_meas_1'] .extend(data_list)'''
        # X-polarization data
        if display_x == 2: 
            tot_sig_pwr, avg_sig_pwr, ph_rate = calculate_signal_metrics('x', pol_format, opt_field_rcv[ch],
                                                                                                    jones_vector[ch], wave_freq[ch], n, time_period)
            # Results list
            data_1 = ['Total signal power (X)', tot_sig_pwr, 'W', '', False, num_format_1]
            data_2 = ['Average signal power (X)', avg_sig_pwr, 'W', '', False, num_format_1]
            data_3 = ['Avg photons/bit (X)', ph_rate, '', '', False, num_format_2]
            data_list = [data_1, data_2, data_3]
            meaure_node_results.extend(data_list)
            '''# Data panel list
            data_1 = ['Total signal power (X)', tot_sig_pwr, num_format_1, 'W']
            data_2 = ['Average signal power (X)',  avg_sig_pwr, num_format_1, 'W']
            data_3 = ['Avg photons/bit (X)', ph_rate, num_format_2, '']
            data_list = [data_1, data_2, data_3]
            config.data_tables['opt_meas_1'] .extend(data_list)'''
        # Y-polarization data
        if display_y == 2: 
            tot_sig_pwr, avg_sig_pwr, ph_rate = calculate_signal_metrics('y', pol_format, opt_field_rcv[ch],
                                                                                                    jones_vector[ch], wave_freq[ch], n, time_period)
            # Results list
            data_1 = ['Total signal power (Y)', tot_sig_pwr, 'W', '', False, num_format_1]
            data_2 = ['Average signal power (Y)', avg_sig_pwr, 'W', '', False, num_format_1]
            data_3 = ['Avg photons/bit (Y)', ph_rate, '', '', False, num_format_2]
            data_list = [data_1, data_2, data_3]
            meaure_node_results.extend(data_list)
            '''# Data panel list
            data_1 = ['Total signal power (Y)', tot_sig_pwr, num_format_1, 'W']
            data_2 = ['Average signal power (Y)',  avg_sig_pwr, num_format_1, 'W']
            data_3 = ['Avg photons/bit (Y)', ph_rate, num_format_2, '']
            data_list = [data_1, data_2, data_3]
            config.data_tables['opt_meas_1'] .extend(data_list)'''
    
    '''==OUTPUT PARAMETERS LIST========================================='''
    meaure_node_parameters = []
    meaure_node_parameters = parameters_input #If NO changes are made to parameters
    
    '''==RETURN (Output Signals, Parameters, Results)=============================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_rcv[ch], noise_field_rcv[ch]]
        optical_channels.append(opt_ch)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels]], 
                 meaure_node_parameters, meaure_node_results)
    
# Method for calculating optical signal envelope metrics
def calculate_signal_metrics(pol, pol_format, sig_array, jones, wave, n, time_period):
    sig_pwr_array = np.zeros(n)
    if pol_format == 'Ex-Ey':
        if pol == 'x-y':
            sig_pwr_array = ( np.abs(sig_array[0])*np.abs(sig_array[0])
                                    + np.abs(sig_array[1])*np.abs(sig_array[1]) )
        elif pol == 'x':
            sig_pwr_array = np.abs(sig_array[0])*np.abs(sig_array[0])
        else:
            sig_pwr_array = np.abs(sig_array[1])*np.abs(sig_array[1])
    else:
        if pol == 'x-y':
            sig_pwr_array = ( np.abs(sig_array*jones[0])*np.abs(sig_array*jones[0])
                                    + np.abs(sig_array*jones[1])*np.abs(sig_array*jones[1]) )
        elif pol == 'x':
            sig_pwr_array = np.abs(sig_array*jones[0])*np.abs(sig_array*jones[0])
        else:
            sig_pwr_array = np.abs(sig_array*jones[1])*np.abs(sig_array*jones[1])
    total_sig_pwr = np.sum(sig_pwr_array)
    avg_sig_pwr = total_sig_pwr/n
    #Calculate average photons per bit
    ph_rate_sig = (avg_sig_pwr*time_period)/(h*wave)
    return total_sig_pwr, avg_sig_pwr, ph_rate_sig
