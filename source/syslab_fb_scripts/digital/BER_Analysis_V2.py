"""
SystemLab-Design Version 20.01.r1
BER Analysis module
Version 2.0 (8-Nov-2019)
"""
import numpy as np
import config
#import project

#import systemlab_viewers as view
import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'BER Analysis'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    ber_parameters = []
    
    '''==CALCULATIONS======================================================='''
    binary_reference = input_signal_data[0][6]
    binary_recovered = input_signal_data[1][6]
    binary_seq_length = np.size(binary_reference)
    
    # Calculate BER
    err_count = 0
    for i in range(0, binary_seq_length):
        if binary_reference[i] != binary_recovered[i]:
            err_count += 1
    ber = err_count/binary_seq_length   
  
    '''==RESULTS============================================================'''
    ber_results = []
    res_ber = ['Bit error rate', ber, ' ', ' ', False]
    num_errors = ['Bit errors', err_count, ' ', ' ', False]
    ber_results = [res_ber, num_errors]
    
    '''#Send update to data panel
    config.data_tables['ber_1'] = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['Binary sequence length', binary_seq_length, '.0f', ' ']
    data_3 = ['Errored bits', err_count, '.0f', ' ']
    data_4 = ['Bit error rate', ber, '0.3E', ' ']
    data_5 = ['Bit error rate (th)', project.ber_th[iteration-1], '0.3E', ' ']
    data_list = [data_1, data_2, data_3, data_4, data_5]
    config.data_tables['ber_1'].extend(data_list)'''
    
    '''#Prepare data for ber waterfall curve
    if iteration == 1:
        project.ber = []
        project.ber.append(ber)
        project.simulation_analyzer = view.IterationsAnalyzer_BER_SER(project.photons_per_bit,
                              project.ber, project.photons_per_bit, project.ber_th, 'BER results', 'Bit error rate',
                              'Photons/bit', 'log', 'log', 'BER (simulation)', 'BER (theoretical)')
        project.simulation_analyzer.show()
    else:
        project.ber.append(ber)
        project.simulation_analyzer.figure.tight_layout(pad=0)
        project.simulation_analyzer.plot_xy()
        project.simulation_analyzer.canvas.draw()'''
        
    return ([], ber_parameters, ber_results)