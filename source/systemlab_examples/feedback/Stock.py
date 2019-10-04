"""
Stock
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=================================================================
    '''
    module_name = 'Stock'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    iterations = settings['iterations']
    time = settings['time_window']
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
    temp = float(parameters_input[0][1]) * (1 + 0.5*((i - 1)/iterations))
    
    '''==CALCULATIONS=====================================================================
    '''
    time_array = np.linspace(0, time, n)
    temp_array = np.full(n, temp)
   
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    stock_parameters = []
    stock_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    stock_results = []
    
    return ([[1, signal_type, fs, time_array, temp_array]],
            stock_parameters, stock_results)

