"""
SystemLab-Design Version 19.02
Functional block script: DC Blocker
Version 1.0 (19.02 13-Mar-2019)
"""

import numpy as np
import config

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
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))                                     
                                          
    '''==INPUT PARAMETERS============================'''
    
    '''==INPUT SIGNALS==============================='''
    sig_type = 'Electrical'
    carrier = 0
    time = input_signal_data[0][4]
    signal = input_signal_data[0][5]
    noise = np.zeros(n)   
    
    '''==CALCULATIONS==============================='''
    sig_avg = np.mean(signal)
    sig_out = signal - sig_avg
        
    '''==OUTPUT PARAMETERS LIST========================'''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS==================================='''
    script_results = []


    '''==RETURN (Output Signals, Parameters, Results)============'''
        
    return ([[2, sig_type, carrier, fs, time, sig_out, noise]], 
            script_parameters, script_results)
