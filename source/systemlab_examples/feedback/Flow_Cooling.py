"""
Feedback node
"""

import numpy as np
import config
import project_feedback as fdk

#import systemlab_viewers as view
import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=================================================================
    '''
    module_name = 'Flow_Cooling'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    segment = int(round(segment))
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']
    
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(i))

    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==INPUT PARAMETERS=================================================================
    '''
    cooling_rate = float(parameters_input[0][1])/100 
    
    '''==INPUT SIGNALS====================================================================
    '''
    signal_type = 'Analog (1)'
    time = input_signal_data[0][3]       
    stock_temp_in = input_signal_data[0][4]
    amb_temp_in = input_signal_data[1][4]
    
    if segment == 1 or feedback_mode == 0: #First iteration of feedback mode simulation
        fdk.temp_sig_out = np.zeros(n)
        feed_temp_in = stock_temp_in
    else:
        feed_temp_in = input_signal_data[2][4] #Use feedback signal
    
    '''==CALCULATIONS=====================================================================
    '''
#   REF/Source: http://www.ugrad.math.ubc.ca/coursedoc/math100/notes/diffeqs/cool.html
#   (Accessed: 2 Feb 2019)
    
    if feedback_mode == 2:
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        dT_over_dt = -cooling_rate*(feed_temp_in[start_index] - amb_temp_in[0])
        dT = dT_over_dt * segment_length * t_step
        if config.sim_data_activate == True:
            config.sim_data_view.dataEdit.append('dT:')
            config.sim_data_view.dataEdit.append(str(dT))
        for seg in range(start_index, n):
            fdk.temp_sig_out[seg] = feed_temp_in[seg - int(segment_length)] + dT
    else:
        fdk.temp_sig_out = stock_temp_in

    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    flow_parameters = []
    flow_parameters = parameters_input
    
    #Prepare data for cooling (decay) curves
    if i == 1 and segment == 1:
        fdk.time_dict = {}
        fdk.time_dict[1] = []
        fdk.time_dict[2] = []
        fdk.time_dict[3] = []
        fdk.stock_temp_dict = {}
        fdk.stock_temp_dict[1] = []
        fdk.stock_temp_dict[2] = []
        fdk.stock_temp_dict[3] = []

    fdk.stock_temp_dict[i].append(feed_temp_in[start_index])
    fdk.time_dict[i].append(time[start_index])
    
    if i == 3 and segment == segments:
        fdk.simulation_analyzer = view.IterationsAnalyzer_NewtonCooling(fdk.time_dict,
                             fdk.stock_temp_dict) 
        fdk.simulation_analyzer.show()

    '''==RESULTS==========================================================================
    '''
    flow_results = []
    
    #Send update to data box (data_table_cooling_1)
    config.data_tables['cooling_1'] = []
    data1 = ['Iteration #', i, 'n','']
    data2 = ['Ambient temp.', amb_temp_in[0], '0.2f','deg C']
    data3 = ['Intial stock temp', stock_temp_in[0], '0.2f','deg C']
    data4 = ['Final stock temp', feed_temp_in[start_index], '0.3f', 'deg C']
    data_list = [data1, data2, data3, data4]
    config.data_tables['cooling_1'] .extend(data_list)
        
    return ([[2, signal_type, fs, time, fdk.temp_sig_out]],
            flow_parameters, flow_results)

