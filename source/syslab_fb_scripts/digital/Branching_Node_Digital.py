"""
SystemLab-Design Version 20.01.r1
Branching node (digital)
Version 1.0 (3-Oct-2019)
"""
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Branching node (digital)' 
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time_win = settings['time_window']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
   
    '''==INPUT PARAMETERS=================================================================
    '''
    signal_type = input_signal_data[0][1]
    symbol_rate = input_signal_data[0][2]
    bit_rate = input_signal_data[0][3]
    order = input_signal_data[0][4]
    time_array = input_signal_data[0][5]
    binary_received = input_signal_data[0][6]
    
    #Parameters table
    node_parameters = []
    node_parameters = parameters_input
    
    '''==CALCULATIONS=====================================================================
    '''

    '''==RESULTS==========================================================================
    '''
    node_results = []
        
    return ([[2, signal_type, symbol_rate, bit_rate, order, time_array, binary_received],
                  [3, signal_type, symbol_rate, bit_rate, order, time_array, binary_received]],
                  node_parameters, node_results)