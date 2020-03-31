"""
SystemLab-Design Version 19.12
Generic module (electrical)
"""
import config

def run(input_signal_data, parameters_input, settings):

    '''==PROJECT SETTINGS======================================================='''
    module_name = 'Generic module - electrical'
    # Main settings
    n = settings['num_samples'] # Total samples for simulation
    n = int(round(n))
    time = settings['time_window'] # Time window for simulation (sec)
    fs = settings['sampling_rate'] # Sample rate (default - Hz)
    f_sym = settings['symbol_rate'] # Symbol rate (default - Hz)
    samples_sym = settings['samples_per_sym'] # Samples per symbol
    t_step = settings['sampling_period'] # Sample period (Hz)
    # Iteration settings
    iteration = settings['current_iteration'] # Current iteration loop for simulation
    i_total = settings['iterations'] # Total iterations for simulation
    # Feedback settings
    segments = settings['feedback_segments'] # Number of integration segments
    segment = settings['feedback_current_segment'] # Current integration segment
    segment = int(round(segment))
    samples_segment = settings['samples_per_segment'] #Samples per feedback segment
    feedback_mode = settings['feedback_enabled'] #Feedback mode is enabled(2)/disabled(0)
    
    '''==Status message (send to Simulation status panel)===================================='''
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))                                     
                                          
    '''==INPUT PARAMETERS======================================================'''
    # Load parameters from FB parameters table [row][column]
    # Parameter name(0), Value(1), Units(2), Notes(3)
    # e.g. par_1 = float(parameters_input[0][1])
    # e.g. par_2 = str(parameters_input[1][1])
    
    # Local/additional parameters
    # e.g. par_3 = 'abc'
    # e.e. par_4 = 100
    
    '''==INPUT SIGNALS=====================================================
    Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), amplitude_array(5), noise_array(6)
    For further info see:
    https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/SignalsLibrary.html
    Note: If there is no input signal, settings must be locally declared
    '''
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    fs = input_signal_data[0][3]
    time_array = input_signal_data[0][4]
    sig_in = input_signal_data[0][5]
    noise_in = input_signal_data[0][6]
    
    '''==CALCULATIONS========================================================='''
    sig_out = sig_in
    noise_out = noise_in

    '''==OUTPUT PARAMETERS LIST================================================='''
    generic_parameters = []
    generic_parameters = parameters_input
  
    '''==RESULTS=========================================================
    # Results are returned and loaded into 'Output data table' tab of functional block 
    # For further info see:
    # https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/AideMemoire.html
    '''
    generic_results = []
    # result_1 = ['Name_1', value_1, 'units_1', 'Description_1', False, 'format']
    # result_2 = ['Name_2', value_2, 'units_2', 'Description_2', False, 'format']]
    # generic_results = [result_1, result_2]
    
    '''==DATA PANEL(S)=====================================================
    # Used to export data to Data panel viewers (optional)
    # For further info see:
    # https://systemlabdesign.com/syslab_documentation/_build/html/syslab_documents/AideMemoire.html
    '''
    # config.data_tables['data_table_1'] = [] # 'Data_table_1' is linked to the data field Data source file name
    # data_1 = ['Data name 1', data_value_1, 'format 1', 'units 1', 'color name 1', 'color data 1']
    # data_2 = ['Data name 2', data_value_2, 'format 2', 'units 2', 'color name 2', 'color data 2']
    # data_list = [data_1, data_2]
    # config.data_tables['data_table_1'] .extend(data_list) # Add data lists to table list
    
    '''==RETURN (Output Signals, Parameters, Results)================================='''
    electrical_out = [2, sig_type, carrier, fs, time_array, sig_out, noise_out]   
    return ([electrical_out], generic_parameters, generic_results)
