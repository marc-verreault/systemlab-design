"""
DECISION CIRCUIT
Version 2.0 (20.01.r3 11-Jun-20)
Associated functional block: syslab_fb_library/Decision Circuit

The Decision Circuit script performs binary decisions (0/1) on a sampled
input electrical signal array. If the sampled electrical signal is below the 
set decision level, a binary 0 is declared, else a binary 1 is declared.

By default the decision mode is set to "Defined" and the value entered in
the "Decision level" parameter field is used to perform the decision.
When the DC signal block is applied (default) the decision level can normally
be set near zero but it is recommended to inspect the signal waveform and
adjust accordingly.

Alternatively, the decison mode can be set to "Signal average". For this mode,
the decision level is set to the average value of the received sampled signal
array

The decision point is set by default to the middle of the received symbol period
but can be adjusted to be earlier (< 0.5) or later (> 0.5).

1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.

"""
import os
import numpy as np
import config
import copy
from scipy import special 

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = settings['fb_name']
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']
    f_sym = settings['symbol_rate']
    
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
    
    '''==INPUT PARAMETERS===================================================
    '''
    decision_mode = str(parameters_input[0][1])
    dc_block = int(parameters_input[1][1])
    normalize = int(parameters_input[2][1])
    decision_th = float(parameters_input[3][1])
    optimize_decision_th = int(parameters_input[4][1])
    decision_pt = float(parameters_input[5][1])
    add_noise_to_signal  = int(parameters_input[6][1])
    dist_plot = int(parameters_input[8][1])
    n_bins = int(parameters_input[9][1])
    data_panel_id = str(parameters_input[11][1])
    data_att_1 = str(parameters_input[12][1])
    data_att_2 = str(parameters_input[13][1])
    
    '''==CALCULATIONS=======================================================
    '''
    order = 1
    bit_rate = f_sym*order
    samples_per_sym = int(fs/f_sym)
    n_sym = int(round(n/samples_per_sym))
    sig_type = input_signal_data[0][1]
    carrier = input_signal_data[0][2]
    time_array = input_signal_data[0][4]
    sampled_sig_in = copy.deepcopy(input_signal_data[0][5])
    noise_array = copy.deepcopy(input_signal_data[0][6])
    
    if add_noise_to_signal == 2:
        sampled_sig_in += noise_array
        noise_array = np.zeros(n)
    digital_out = np.zeros(n_sym, dtype = int)
    sig_avg = np.mean(np.real(sampled_sig_in))
    
    #DC block (if enabled)
    if dc_block == 2:
        sampled_sig_in = sampled_sig_in - sig_avg
        #config.display_xy_data('Signal after DC block', time, 'Time (s)', sampled_sig_in, 'Magnitude')
        
    if normalize == 2:
        if dc_block == 0:
            sampled_sig_in = sampled_sig_in - sig_avg
        sampled_sig_in = sampled_sig_in/np.max(np.real(sampled_sig_in))
        # Re-calculate signal average
        sig_avg = np.mean(np.real(sampled_sig_in))
        #config.display_xy_data('Signal after Normalize', time, 'Time (s)', sampled_sig_in, 'Magnitude')
    
    if decision_mode == 'Signal average':
        decision_th = sig_avg
        
    # Perform decisions (@ decision point)
    decision_samples = np.zeros(n_sym)
    for sym in range(0, n_sym):
        sampling_index = int(sym*samples_per_sym + round(samples_per_sym*decision_pt))
        decision_samples[sym] = sampled_sig_in[sampling_index]
        if decision_samples[sym] >= decision_th:
            digital_out[sym] = 1
            
    # Calculate statistics
    v0_mean = np.mean(decision_samples[decision_samples < decision_th])
    v0_sigma = np.std(decision_samples[decision_samples < decision_th])
    v1_mean = np.mean(decision_samples[decision_samples > decision_th])
    v1_sigma = np.std(decision_samples[decision_samples > decision_th])
    q_measured = (v1_mean - v0_mean)/(v1_sigma + v0_sigma )
    ber_estimate = 0.5*special.erfc(q_measured/np.sqrt(2))
    
    # Optimized decision point (informative) REF 1, Eq 4.55
    decision_opt = (v1_sigma*v0_mean + v0_sigma*v1_mean)/(v1_sigma+v0_sigma)
    
    # Perform decisions (@ decision point)
    if optimize_decision_th == 2:
        decision_th = decision_opt
        for sym in range(0, n_sym):
            if decision_samples[sym] >= decision_th:
                digital_out[sym] = 1
    
    # Distribution analysis
    if dist_plot == 2:
        title = 'Signal amplitude distribution (' + module_name + ' - Iteration ' + str(iteration) + ')'
        config.dist_graph[module_name + str(iteration)] = config.view.Distribution_Analysis(title, decision_samples,
                                                                                      'Signal (V)', n_bins, decision_th, v1_mean,
                                                                                      v0_mean, v1_sigma, v0_sigma)
        config.dist_graph[module_name + str(iteration)].show()
        
    # Send data to project folder (only if project file has been created)
    if os.path.isfile(path):
        if iteration == 1:
            if data_att_1:
                setattr(proj, data_att_1, [])
                getattr(proj, data_att_1).append(q_measured)
            if data_att_2:
                setattr(proj, data_att_2, [])
                getattr(proj, data_att_2).append(ber_estimate)
        else:
            if data_att_1:
                getattr(proj, data_att_1).append(q_measured)
            if data_att_2:
                getattr(proj, data_att_2).append(ber_estimate)
            
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    decision_parameters = []
    decision_parameters = parameters_input

    '''==RESULTS============================================================'''
    results = []
    results.append(['Threshold level (used for decision)', decision_th,  ' ', ' ', False, '0.3E'])
    results.append(['Optimized decision threshold', decision_opt,  ' ', ' ', False, '0.3E'])
    results.append(['V1 mean (at decision pt)', v1_mean,  ' ', ' ', False, '0.3E'])
    results.append(['V0 mean (at decision pt)', v0_mean, ' ', ' ', False, '0.3E'])
    results.append(['V1 std dev (at decision pt)', v1_sigma, ' ', ' ', False, '0.3E'])
    results.append(['Q measured (at decision pt)', q_measured, ' ', ' ', False, '0.2f'])
    results.append(['BER estimated (at decision pt)', ber_estimate, ' ', ' ', False, '0.3E'])
    
    '''==RESULTS============================================================'''
    c_analytical = 'blue'
    config.data_tables[data_panel_id] = []
    data_list = []
    data_list.append(['Iteration #', iteration, '0.0f', ' ', ' ', c_analytical])
    data_list.append(['Q (measured)', q_measured, '0.2f', ' '])
    data_list.append(['BER (estimated)', ber_estimate, '0.3E', ' ', ' ', c_analytical])
    config.data_tables[data_panel_id].extend(data_list)
    
    return ([[2, 'Digital', f_sym, bit_rate, order, time_array, digital_out],
                  [3, sig_type, carrier, fs, time_array, sampled_sig_in, noise_array]],
                decision_parameters, results)



