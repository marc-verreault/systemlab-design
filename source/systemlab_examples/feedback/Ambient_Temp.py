"""
Ambient temp
"""

import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=================================================================
    '''
    module_name = 'Ambient temp'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
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
    temp_ambient = float(parameters_input[0][1])
    
    '''==CALCULATIONS=====================================================================
    '''
    time_array = np.linspace(0, time, n)
    temp_array = np.full(n, temp_ambient)
   
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    ambient_parameters = []
    ambient_parameters = parameters_input
  
    '''==RESULTS==========================================================================
    '''
    ambient_results = []
    
    return ([[1, signal_type, fs, time_array, temp_array]],
            ambient_parameters, ambient_results)

