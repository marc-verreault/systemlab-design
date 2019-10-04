"""
Branch node
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Branch'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(i))
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==PARAMETERS=======================================================================
    '''
    signal_type = 'Analog (1)'
    time_in = input_signal_data[0][3]
    temp_in = input_signal_data[0][4]
    
    '''==CALCULATIONS=====================================================================
    '''
            
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    b_parameters = []
    b_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    b_results = []
    
    return ([[2, signal_type, fs, time_in, temp_in], [3, signal_type, fs, time_in, temp_in]],
            b_parameters, b_results)

