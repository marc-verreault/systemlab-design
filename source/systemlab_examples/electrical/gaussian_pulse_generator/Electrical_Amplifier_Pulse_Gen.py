"""
SystemLab-Design Version 19.12

SCRIPT TEMPLATE FOR FUNCTIONAL BLOCKS
Version: 2.0
Date: 20-Dec-2019
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
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()

    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))                                     
                                          
    '''==INPUT PARAMETERS=======================================================
    Load parameters from FB parameters table [row][column]
    Parameter name(0), Value(1), Units(2), Notes(3)
    '''
    #par_1 = float(parameters_input[0][1])
    #par_2 = str(parameters_input[1][1])
    #Additional parameters (local)
    #par_3 = 'abc'
    #par_4 = 100
    
    gain_db = float(parameters_input[0][1])
    
    '''==INPUT SIGNALS==========================================================
    Digital: portID(0), signal_type(1), symbol_rate(2), bit_rate(3), order(4), time_array(5), discrete_array(6)
    Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), amplitude_array(5), noise_array(6)
    Optical_signal: portID(0), sig_type(1), fs(2), time_array(3), psd_array(4), optical_group(5)
    Optical_channel(s): wave_key(0), wave_freq(1), jones_vector(2), e_field_array(3), noise_array(4)
    For further info see:
    https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/SignalsLibrary.html
    Note: If there is no input signal, output settings must be locally declared
    '''
    time_array = input_signal_data[0][4]
    sig_in = input_signal_data[0][5]
    
    '''==CALCULATIONS=====================================================================
    '''
    carrier = 0
    sig_type = 'Electrical'
    sig_array = sig_in*np.power(10, gain_db/20)
    noise_array = np.zeros(n)
    
    '''==OUTPUT PARAMETERS LIST===================================================
    '''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
    #par_1 = ['Par_1', value, 'units', 'Description']   
    #script_parameters = [par_1, par_2]
  
    '''==RESULTS========================================================
    Results are returned and loaded into 'Output data table' tab of functional block. 
    For further info see:
    https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/AideMemoire.html
    '''
    script_results = []
    #result_1 = ['Name_1', value_1, 'units_1', 'Description_1', False, 'format']
    #result_2 = ['Name_2', value_2, 'units_2', 'Description_2', False, 'format']]
    #script_results = [result_1, result_2]
    
    '''==DATA PANEL(S)=====================================================
    Used to export data to Data panel viewers (optional)
    For further info see:
    https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/AideMemoire.html
    config.data_tables['data_table_1'] = [] # 'Data_table_1' is linked to the data field Data source file name
    data_1 = ['Data name 1', data_value_1, 'format 1', 'units 1', 'color name 1', 'color data 1']
    data_2 = ['Data name 2', data_value_2, 'format 2', 'units 2', 'color name 2', 'color data 2']
    data_list = [data_1, data_2]
    config.data_tables['data_table_1'] .extend(data_list) # Add data lists to table list
    '''

    '''==RETURN (Output Signals, Parameters, Results)==================================
    '''
    #DIGITAL  
    #digital_out = [1, signal_type, symbol_rate, bit_rate, order, time_array, digital_output]
    #return ([digital_out], script_parameters, script_results)
    
    #ELECTRICAL        
    electrical_out = [2, sig_type, carrier, fs, time_array, sig_array, noise_array]
    return ([electrical_out], script_parameters, script_results)
    
    #OPTICAL
    #optical_channels = []
    #for ch in range(0, channels):
    #    opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], 
    #    opt_field_out[ch], noise_field_out[ch]]
    #    optical_channels.append(opt_ch)
    #return ([[1, signal_type, fs, time_array, psd_array, optical_channels]], 
    #              script_parameters, script_results)
