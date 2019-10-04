"""
SystemLab-Design Version 19.02

SCRIPT TEMPLATE FOR FUNCTIONAL BLOCKS
Version: 1.0
Date: 5-March-2019
"""

import numpy as np
import config
from scipy import signal

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'Script template'
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))    
    time = settings['time_window'] #Time window for simulation (sec)
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    f_sym = settings['symbol_rate'] #Symbol rate (default - Hz)
    t_step = settings['sampling_period'] #Sample period (Hz)
    #Iteration settings
    iteration = settings['current_iteration'] #Current iteration loop for simulation
    i_total = settings['iterations'] #Total iterations for simulation (default - 1)
    #Feedback settings
    segments = settings['feedback_segments'] #Number of integration segments
    segment = settings['feedback_current_segment'] #Current intgration segment
    segment = int(round(segment))
    feedback_mode = settings['feedback_enabled'] #Feedback mode is enabled(2)/disabled(0)
    
    # Status message (send to Simulation status panel)
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    # Data output (when enabled) - sent to Data window
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))                                     
                                          
    '''==INPUT PARAMETERS=============================================================='''
    # Load parameters from FB parameters table [row][column]
    # Parameter name(0), Value(1), Units(2), Notes(3)
    # e.g. par_1 = float(parameters_input[0][1])
    # e.g. par_2 = str(parameters_input[1][1])

    # Additional parameters (local)
#    par_3 = 'abc'
#    par_4 = 100
    
    '''==INPUT SIGNALS====================================================================
    '''
    # input_signal_data = [[signal_port_a], [signal_port_b], ...]
    # Digital: portID(0), signal_type(1), symbol_rate(2), bit_rate(3), order(4),
    # time_array(5), discrete_array(6)
    # Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), 
    # amplitude_array(5), noise_array(6)
    # Optical collection: [portID(0), signal_type(1), sample_rate(2), time_array(3), 
    # optical_channel_list(4)]
    # Optical_channel_list:
    # [[wave_key(0), wave_channel(1), jones_matrix(2), envelope_array(3), noise_array(4),
    # psd_array(5)], [wave_key(0), wave_channel(1), jones_matrix(2), envelope_array(3),
    # noise_array(4), psd_array(5)],...]
    # input_data_1 = input_signal_data[a][b], where a is list index and b is element index
    # for list a
    
    '''==CALCULATIONS=====================================================================
    '''
    #config.sim_status_win.textEdit.append('Data: ' + str(input_data
        
    carrier = 0
    sig_type_out = 'Electrical'
    time_array = np.linspace(0, time, n)
    sig_array = signal.gausspulse(time_array, fc=10)
    noise_array = np.zeros(n)
        
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
#    par_1 = ['Par_1', value, 'units', 'Description']   
#    script_parameters = [par_1, par_2]
  
    '''==RESULTS==========================================================================
    '''
    script_results = []
#    result_1 = ['Name_1', value_1, 'units_1', 'Description_1']
#    result_2 = ['Name_2', value_2, 'units_2', 'Description_2']
#    script_results = [result_1, result_2]
    
    '''==DATA PANEL=======================================================================
    '''
    #Send update to data panel (data_table_1)
#    data_1 = ['Name_1', value_1, 'units_1']
#    data_2 = ['Name_2', value_2, 'units_2']
#    config.data_table_1.append(data_1)
#    config.data_table_2.append(data_2)    


    '''==RETURN (Output Signals, Parameters, Results)=================================='''
# DIGITAL  
#      digital_out = [1, signal_type, symbol_rate, bit_rate, order, time_array, binary_array]
# ELECTRICAL        
    electrical_out = [1, sig_type_out, carrier, fs, time_array, sig_array, noise_array]
# OPTICAL
#      optical_group = [[wave_key, wave_freq, jones_vector, e_field_array, noise_array, psd_array]]
#      optical_out = [3, signal_type, fs, time_array, optical_group]
    return ([electrical_out], script_parameters, script_results)
