"""
SystemLab-Design Version 19.02

SIgn inversion/invertor
"""
import config
import numpy as np

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'Sign invertor'
    #Iteration settings
    iteration = settings['current_iteration'] #Current iteration loop for simulation
    
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
    sig_out = np.negative(sig_in)
    noise_out = np.negative(noise_in)

    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    node_parameters = []
    node_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS==========================================================================
    '''
    node_results = []

    '''==RETURN (Output Signals, Parameters, Results)==================================
    '''
    electrical_out_1 = [2, sig_type, carrier, fs, time_array, sig_out, noise_out]
    return ([electrical_out_1], node_parameters, node_results)
