"""
SystemLab-Design Version 20.01.r1
BER Analysis module
Version 2.0 (8-Nov-2019)
"""
import numpy as np
import config
import os
from scipy import special 
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
    
    path = settings['file_path_1']
    path = os.path.join(path, 'project_config.py')
    if os.path.isfile(path):
        import project_config as proj

    """Status messages-----------------------------------------------------------------------"""
    # Status message - initiation of fb_script (Sim status panel & Info/Status window)
    fb_title_string = 'Running ' + str(module_name) + ' - Iteration #: ' + str(iteration)
    config.status_message(fb_title_string)
    # Data display - title of current fb_script
    config.display_data(' ', ' ', False, False)
    fb_data_string = 'Data output for ' + str(module_name) + ' - Iteration #: '
    # Display data settings: Data title (str), Data (scalar, array, etc), 
    # Set to Bold?, Title & Data on separate lines?
    config.display_data(fb_data_string, iteration, False, True) 
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    ignore_bits_start = int(parameters_input[0][1])
    ignore_bits_end = int(parameters_input[1][1])
    cf_level = float(parameters_input[2][1])
    wtr_fall = int(parameters_input[3][1])
    data_panel_id = str(parameters_input[4][1])
    
    '''==CALCULATIONS======================================================='''
    binary_reference = input_signal_data[0][6]
    binary_recovered = input_signal_data[1][6]
    binary_seq_length = np.size(binary_reference)
    
    # Adjust sequence length
    start_index = ignore_bits_start
    binary_reference_adj = np.delete(binary_reference, slice(0, start_index))
    binary_recovered_adj = np.delete(binary_recovered, slice(0, start_index))
    seq_length_adj = np.size(binary_reference_adj)
    end_index = seq_length_adj - ignore_bits_end - 1
    binary_reference_adj = np.delete(binary_reference_adj, slice(end_index, seq_length_adj - 1))
    binary_recovered_adj = np.delete(binary_recovered_adj, slice(end_index, seq_length_adj - 1))
    seq_length_final = np.size(binary_reference_adj)
    
    # Calculate BER (X + Y)
    err_count = 0
    ber = 0
    for i in range(0, seq_length_final):
        if binary_reference_adj[i] != binary_recovered_adj[i]:
            err_count += 1
    if seq_length_final > 0:
        ber = err_count/seq_length_final  

    # Calculate accuracy of measured BER (based on confidence level)
    # Evaluating BER in wireless systems: confidence in waterfall curves
    # David Day and Scott Siclari, Aeroflex Inc
    # Source: https://m.eet.com/media/1137412/294532.pdf (accessed: 27-Jul-20)
    accuracy = 'NA'
    upper_ber_limit = 'NA'
    error=0.0
    if cf_level == 80:
        sigma = 1.28155
    elif cf_level == 90:
        sigma = 1.64485
    elif cf_level == 95:
        sigma = 1.95996
    else:
        sigma = 2.57583
    if err_count > 0:
        accuracy = 100*1.64485/np.sqrt(err_count)
        error = (accuracy)*ber
    else:
        if seq_length_final > 0:
            upper_ber_limit = -np.log(1-(cf_level/100))/seq_length_final
            
    '''==OUTPUT PARAMETERS LIST============================================='''
    ber_parameters = []
    ber_parameters = parameters_input
    
    '''==RESULTS============================================================'''
    results = []
    results.append(['Bit error rate', ber, ' ', ' ', False, '0.3E'])
    results.append(['Bit errors', err_count, ' ', ' ', False, 'n'])
    results.append(['Accuracy (confidence level: ' + str(cf_level) + ' %)', 
                             accuracy, '\u00B1' + '%', ' ', False, '0.2f'])
    results.append(['Upper BER limit (confidence level: ' + str(cf_level) + ' %)', 
                             upper_ber_limit, ' ', ' ', False, '0.3E'])
    
    #Send update to data panel
    config.data_tables[data_panel_id] = []
    data_list = []
    data_list.append(['Iteration #', iteration, '.0f', ' ', ' ', '#0000ff'])
    data_list.append(['Binary sequence length', binary_seq_length, '.0f', ' '])
    data_list.append(['Errored bits', err_count, '.0f', ' '])
    data_list.append(['Bit error rate', ber, '0.3E', ' '])
    config.data_tables[data_panel_id].extend(data_list)
    
    #Prepare data for ber waterfall curve
    if wtr_fall == 2 and os.path.isfile(path):
        if iteration == 1:
            proj.ber = []
            proj.error = []
            proj.ber.append(ber)
            proj.error.append(error)
            proj.simulation_analyzer = view.IterationsAnalyzer_BER(proj.rcv_pwr_dbm,
                                  proj.ber, error, proj.rcv_pwr_dbm, proj.ber_estimate, 'BER results', 'Bit error rate',
                                  'Optical power received (dBm)', 'log', 'linear', 'BER (simulation)', 'BER (Q-measured)')
            proj.simulation_analyzer.show()
        else:
            proj.ber.append(ber)
            proj.error.append(error)
            config.display_data('BER', proj.ber, 0, 0) 
            config.display_data('BER estimate', proj.ber_estimate, 0, 0) 
            config.display_data('Error', proj.error, 0, 0)
            proj.simulation_analyzer.figure.tight_layout(pad=0)
            proj.simulation_analyzer.plot_xy()
            proj.simulation_analyzer.canvas.draw()
        
    return ([], ber_parameters, results)