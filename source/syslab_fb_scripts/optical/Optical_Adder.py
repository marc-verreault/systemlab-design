"""
SystemLab-Design Version 20.01.r1
Generic module (optical)
"""
import config
import numpy as np

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS===================================================='''
    module_name = 'Generic module - optical'
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
    # Parameter name(0), Value(1), Units(2), Notes(3)
    # e.g. par_1 = float(parameters_input[0][1])
    # e.g. par_2 = str(parameters_input[1][1])
    
    # Local/additional parameters
    # e.g. par_3 = 'abc'
    # e.e. par_4 = 100
    
    '''==INPUT SIGNALS=====================================================
    Optical_signal: portID(0), sig_type(1), fs(2), time_array(3), psd_array(4), optical_group(5)
    Optical_channel(s): wave_key(0), wave_freq(1), jones_vector(2), e_field_array(3), noise_array(4)
    For further info see:
    https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/SignalsLibrary.html
    Note: If there is no input signal, settings must be locally declared
    '''
    # LOAD OPTICAL CHANNELS FROM PORT 1--------------------------------------
    signal_type = input_signal_data[0][1]
    time_array = input_signal_data[0][3] 
    psd_array_1 = input_signal_data[0][4] 
    opt_channels_1 = input_signal_data[0][5] 
    # Load frequency, jones vector, signal & noise field envelopes for each optical channel
    channels_1 = len(opt_channels_1)
    wave_key_1 = np.empty(channels_1)
    wave_freq_1 = np.empty(channels_1)
    jones_vector_1 = np.full([channels_1, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels_1[0][3].ndim == 2:
        opt_field_rcv_1 = np.full([channels_1, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_rcv_1 = np.full([channels_1, n], 0 + 1j*0, dtype=complex) 
    noise_field_rcv_1 = np.full([channels_1, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels_1): #Load wavelength channels
        wave_key_1[ch] = opt_channels_1[ch][0]
        wave_freq_1[ch] = opt_channels_1[ch][1]
        jones_vector_1[ch] = opt_channels_1[ch][2]
        opt_field_rcv_1[ch] = opt_channels_1[ch][3]
        noise_field_rcv_1[ch] = opt_channels_1[ch][4]
        
    # LOAD OPTICAL CHANNELS FROM PORT 2--------------------------------------
    if len(input_signal_data) == 2: #2nd port has signal data
        psd_array_2 = input_signal_data[1][4] 
        opt_channels_2 = input_signal_data[1][5] 
        # Load frequency, jones vector, signal & noise field envelopes for each optical channel
        channels_2 = len(opt_channels_2)
        wave_key_2 = np.empty(channels_2)
        wave_freq_2 = np.empty(channels_2)
        jones_vector_2 = np.full([channels_2, 2], 0 + 1j*0, dtype=complex) 
        if opt_channels_2[0][3].ndim == 2:
            opt_field_rcv_2 = np.full([channels_2, 2, n], 0 + 1j*0, dtype=complex) 
        else:
            opt_field_rcv_2 = np.full([channels_2, n], 0 + 1j*0, dtype=complex) 
        noise_field_rcv_2 = np.full([channels_2, n], 0 + 1j*0, dtype=complex) 
        for ch in range(0, channels_2): #Load wavelength channels
            wave_key_2[ch] = opt_channels_2[ch][0]
            wave_freq_2[ch] = opt_channels_2[ch][1]
            jones_vector_2[ch] = opt_channels_2[ch][2]
            opt_field_rcv_2[ch] = opt_channels_2[ch][3]
            noise_field_rcv_2[ch] = opt_channels_2[ch][4]
    else:
        channels_2 = 0
            
    '''==OUTPUT PARAMETERS LIST========================================='''
    generic_parameters = []
    generic_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS========================================================
    # Results are returned and loaded into 'Output data table' tab of functional block. 
    # For further info see:
    # https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/AideMemoire.html
    '''
    generic_results = []
    # result_1 = ['Name_1', value_1, 'units_1', 'Description_1', False, 'format']
    # result_2 = ['Name_2', value_2, 'units_2', 'Description_2', False, 'format']]
    # generic_results = [result_1, result_2]
    
    '''==DATA PANEL(S)=====================================================
    # Used to export data to Data panel viewers (optional)
    # For further info see:
    # https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/AideMemoire.html
    '''
    # config.data_tables['data_table_1'] = [] # 'Data_table_1' is linked to the data field Data source file name
    # data_1 = ['Data name 1', data_value_1, 'format 1', 'units 1', 'color name 1', 'color data 1']
    # data_2 = ['Data name 2', data_value_2, 'format 2', 'units 2', 'color name 2', 'color data 2']
    # data_list = [data_1, data_2]
    # config.data_tables['data_table_1'] .extend(data_list) # Add data lists to table list

    '''==RETURN (Output Signals, Parameters, Results)=============================='''
    optical_channels = []
    for ch in range(0, channels_1):
        opt_ch = [int(wave_key_1[ch]), wave_freq_1[ch], jones_vector_1[ch], opt_field_rcv_1[ch], noise_field_rcv_1[ch]]
        optical_channels.append(opt_ch)
    for ch in range(0, channels_2):
        opt_ch = [int(wave_key_2[ch]), wave_freq_2[ch], jones_vector_2[ch], opt_field_rcv_2[ch], noise_field_rcv_2[ch]]
        optical_channels.append(opt_ch)
    
    return ([[3, signal_type, fs, time_array, psd_array_1, optical_channels]], generic_parameters, generic_results)
