"""
SystemLab-Design Version 20.01.r1

Multiple Port Viewer (Electrical)
"""
import port_viewer_multiple_electrical as viewer
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'Multiple Port Viewer (Electrical)'
    #Iteration settings
    iteration = settings['current_iteration'] #Current iteration loop for simulation
    iterations = settings['iterations']
    
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


    '''==CALCULATIONS=====================================================================
    '''
    if iteration == 1:
        config.signals = []
        config.signals.append(input_signal_data)
    if iteration == iterations:
        config.signals.append(input_signal_data)
        view_data = viewer.ElectricalDataAnalyzerMultiplePort(config.signals, parameters_input, settings )
        view_data.show()

    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    node_parameters = []
    node_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS==========================================================================
    '''
    node_results = []

    '''==RETURN (Output Signals, Parameters, Results)==================================
    '''
    return ([], node_parameters, node_results)
