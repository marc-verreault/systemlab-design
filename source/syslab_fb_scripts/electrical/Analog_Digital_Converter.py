"""
SystemLab-Design Version 20.01.r1
Functional block script: Analog Digital Converter (ADC)
Version 1.0 (28 Oct 2019)
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'ADC (Electrical)'
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))
    sampling_period = settings['sampling_period']
    time_window = settings['time_window']
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    f_sym = settings['symbol_rate']
    samples_per_sym = settings['samples_per_sym']
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
    
    '''==INPUT PARAMETERS========================================================='''
    #Load parameters from FB parameters table (Parameter name(0), Value(1), Units(2), Notes(3))
    mode = str(parameters_input[1][1])
    adc_fs = float(parameters_input[2][1]) #Hz
    # Quantization parameters
    res = int(parameters_input[4][1]) 
    ref_v_low = float(parameters_input[5][1]) 
    ref_v_high = float(parameters_input[6][1]) 
    
    '''==INPUT SIGNALS======================================================'''
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    #fs = input_signal_data[0][3]
    time_array = input_signal_data[0][4]
    sig_in = input_signal_data[0][5]
    noise_in = input_signal_data[0][6]
    
    '''==CALCULATIONS=======================================================''' 
    # Initialize output signal arrays (to zero)
    v_out = np.zeros(n)
    noise_out = np.zeros(n)
    # Calculate time sampling array for ADC (these define the sample and hold time indices)
    adc_sampling_period = 1/adc_fs
    adc_time_samples = np.arange(0, time_window, adc_sampling_period )
    index_start_sample_hold = np.searchsorted(time_array, adc_time_samples, side='left')
    # Update output voltages based on sample and hold conditions
    for i in range(0, len(adc_time_samples)-1):
        v_out[index_start_sample_hold[i]: index_start_sample_hold[i+1]] = sig_in[index_start_sample_hold[i]]
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    adc_parameters = []
    adc_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    adc_results = []

    '''==RETURN (Output Signals, Parameters, Results)=========================='''      
    electrical_out = [2, sig_type, carrier, fs, time_array, v_out, noise_out] 
    return ([electrical_out], adc_parameters, adc_results)

