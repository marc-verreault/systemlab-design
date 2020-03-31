"""
BER Analysis module
Version 1.0 (19.02 23 Feb 2019)
"""
import numpy as np
import config
import project_optical_qpsk as project

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
    ignore_bits_start = int(parameters_input[0][1])
    ignore_bits_end = int(parameters_input[1][1])
    
    '''==CALCULATIONS======================================================='''
    binary_reference = input_signal_data[0][6]
    binary_recovered = input_signal_data[1][6]
    seq_length = np.size(binary_reference)
    
    # Adjust data set (ignore bits)
    # https://stackoverflow.com/questions/32682754/np-delete-and-np-s-whats-so-special-about-np-s
    start_index = ignore_bits_start
    binary_reference_adj = np.delete(binary_reference, slice(0, start_index))
    binary_recovered_adj = np.delete(binary_recovered, slice(0, start_index))
    seq_length_adj = np.size(binary_reference_adj)
    end_index = seq_length_adj - ignore_bits_end - 1
    binary_reference_adj = np.delete(binary_reference_adj, slice(end_index, seq_length_adj-1))
    binary_recovered_adj = np.delete(binary_recovered_adj, slice(end_index, seq_length_adj-1))
    seq_length_final = np.size(binary_reference_adj)
    
    # Calculate BER
    err_count = 0
    for i in range(0, seq_length_final):
        if binary_reference_adj[i] != binary_recovered_adj[i]:
            err_count += 1
    ber = err_count/seq_length_final  
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    ber_parameters = []
    ber_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    ber_results = []
    res_ber = ['Bit error rate', ber, ' ', ' ', False]
    num_errors = ['Bit errors', err_count, ' ', ' ', False]
    ber_results = [res_ber, num_errors]
    
    #Send update to data panel
    config.data_tables['opt_qpsk_2'] = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['Binary sequence length (orginal)', seq_length, '.0f', ' ']
    data_3 = ['Binary sequence length (for BER)', seq_length_final, '.0f', ' ']
    data_4 = ['Errored bits', err_count, '.0f', ' ']
    data_5 = ['Bit error rate', ber, '0.3E', ' ']
    data_6 = ['Bit error rate (th)', project.ber_th[iteration-1], '0.3E', ' ']
    data_list = [data_1, data_2, data_3, data_4, data_5, data_6]
    config.data_tables['opt_qpsk_2'].extend(data_list)
    
    #Prepare data for ber waterfall curve
    '''if iteration == 1:
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