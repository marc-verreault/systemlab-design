"""
SystemLab-Design Version 19.02

Branching node
"""
import config
import numpy as np

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'Measurment node'
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
    
    # Status message (send to Simulation status panel)
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))                                     
                                          
    '''==INPUT PARAMETERS==============================================================
    '''
    
    '''==INPUT SIGNALS====================================================================
    '''
    # Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), 
    # amplitude_array(5), noise_array(6)
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    fs = input_signal_data[0][3]
    time_array = input_signal_data[0][4]
    sig_in = input_signal_data[0][5]
    noise_in = input_signal_data[0][6]
    
    '''==CALCULATIONS=====================================================================
    '''
    #Calculate signal and noise powers
    sig_pwr = np.sum(np.abs(sig_in)*np.abs(sig_in))
    noise_pwr = np.sum(np.abs(noise_in)*np.abs(noise_in))
    
    noise_std_dev = np.std(np.real(noise_in))
    
    snr = sig_pwr/noise_pwr
    snr_db = 10*np.log10(snr)

    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    node_parameters = []
    node_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS==========================================================================
    '''
    node_results = []
    sig_pwr_result = ['Signal power', sig_pwr , ' ', ' ', False]
    noise_pwr_result = ['Noise power', noise_pwr , ' ', ' ', False]
    snr_result = ['Signal/noise ratio', snr, ' ', ' ', False]
    snr_db_result = ['Signal/noise ratio (dB)', snr_db, ' ', ' ', False]
    noise_std_result = ['Noise standard dev', noise_std_dev , ' ', ' ', False]
    node_results = [sig_pwr_result, noise_pwr_result, snr_result, snr_db_result, noise_std_result]
    
    '''==RETURN (Output Signals, Parameters, Results)==================================
    '''
    electrical_out_1 = [2, sig_type, carrier, fs, time_array, sig_in, noise_in]
    electrical_out_2 = [3, sig_type, carrier, fs, time_array, sig_in, noise_in]    
    return ([electrical_out_1, electrical_out_2], node_parameters, node_results)
