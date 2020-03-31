"""
Decision Analyzer module
"""

import numpy as np
import config
import project_qpsk as project

#import systemlab_viewers as view
import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Decision Analyzer'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    iterations = settings['iterations']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
        config.app.processEvents()

    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
#    bit_rate_input = input_signal_data[0][3]
    carrier = 0
    
    #Parameters table
    decision_parameters = []
    
    '''==CALCULATIONS======================================================='''
    #Calculate symbol error rate
    bit_rate = 10e9
    symbol_rate = 5e9
   
    samples_per_bit = int(fs/bit_rate)
    samples_per_symbol = int(fs/symbol_rate)
    n_sym = int(round(n/samples_per_symbol))
    
    sym_i_in = input_signal_data[2][6]
    sym_q_in = input_signal_data[3][6]   
    sym_i_ref = project.symbol_seq_even
    sym_q_ref = project.symbol_seq_odd
    
    int_sig_in_i = input_signal_data[0][5]
    int_sig_in_q = input_signal_data[1][5]
    time = input_signal_data[0][4]
    int_noise_i = input_signal_data[0][6]
    int_noise_q = input_signal_data[1][6]
    
    #Calculate symbol error rate (SER)
    err_count = 0
    for sym in range (0, n_sym):
        if sym_i_in[sym] != sym_i_ref[sym] or sym_q_in[sym] != sym_q_ref[sym]:
            err_count += 1

    ser = err_count/n_sym
    
    #Calculate EVM and prepare constellation
    decision_samples_i = np.array([])
    decision_samples_q = np.array([])
    decision_noise_i = np.array([])
    decision_noise_q = np.array([])
    
    for sym in range(1, n_sym+1):
        decision_samples_i = np.append(decision_samples_i, int_sig_in_i[int(sym*samples_per_symbol) - 1])
        decision_samples_q = np.append(decision_samples_q, int_sig_in_q[int(sym*samples_per_symbol) - 1])
        decision_noise_i = np.append(decision_noise_i, int_noise_i[int(sym*samples_per_symbol) - 1])
        decision_noise_q = np.append(decision_noise_q, int_noise_q[int(sym*samples_per_symbol) - 1])

        recovered_symbol_i = decision_samples_i - decision_noise_i
        recovered_symbol_q = decision_samples_q - decision_noise_q
    
    #EVM calculation
    avg_ref_pwr = ( (np.sum(np.square(recovered_symbol_i))
                  + np.sum(np.square(recovered_symbol_q)))/n_sym )
    sum_iq_pwr_err = 0
    for sym in range (0, n_sym):
        err_i = (decision_samples_i[sym] - recovered_symbol_i[sym])
        err_i_pwr = np.square(err_i)
        err_q = (decision_samples_q[sym] - recovered_symbol_q[sym])
        err_q_pwr = np.square(err_q)
        sum_iq_pwr_err +=  err_i_pwr + err_q_pwr
        
    evm_rms = np.sqrt((sum_iq_pwr_err/float(n_sym))/avg_ref_pwr)
    evm_per = evm_rms*100
    if evm_rms > 0:
        evm_db = 20*np.log10(evm_rms)
    else:
        evm_db = 0

    #Prepare data for ser waterfall curve
    if iteration == 1:
        project.ser = []
        project.ser.append(ser)
        project.simulation_analyzer = view.IterationsAnalyzer_BER_SER(project.snr_per_sym,
                              project.ser, project.snr_per_sym, project.ser_th,  'SER results', 'Symbol error rate',
                              'SNR per sym', 'log', 'linear', 'SER (simulation)', 'SER (theoretical)')
        project.simulation_analyzer.show()
    else:
        project.ser.append(ser)
        project.simulation_analyzer.figure.tight_layout(pad=0)
        project.simulation_analyzer.plot_xy()
        project.simulation_analyzer.canvas.draw()
   
    #Prepare data for constellation view
    if iteration == 1:
        project.decision_samples_dict_i = {}
        project.decision_samples_dict_q = {}
        project.recovered_sig_dict_i = {}
        project.recovered_sig_dict_q = {}
        project.evm_results_per = {}
        project.evm_results_db = {}
        
    project.decision_samples_dict_i [iteration] = decision_samples_i
    project.decision_samples_dict_q [iteration] = decision_samples_q
    project.recovered_sig_dict_i [iteration] = recovered_symbol_i
    project.recovered_sig_dict_q [iteration] = recovered_symbol_q
    project.evm_results_per [iteration] = evm_per
    project.evm_results_db [iteration] = evm_db
    
    if iteration == iterations:
        project.constellation = view.SignalSpaceAnalyzer('Electrical QPSK', 
                                                        project.decision_samples_dict_i,
                                                        project.decision_samples_dict_q,
                                                        project.recovered_sig_dict_i,
                                                        project.recovered_sig_dict_q,
                                                        project.evm_results_per,
                                                        project.evm_results_db)
        project.constellation.show()
  
    '''==RESULTS============================================================'''
    decision_results = []
    #Send update to data box (data_table_1)
    config.data_tables['qpsk_3'] = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['Number symbols received', n_sym, '0.2E', 'a.u.']        
    data_3 = ['SER', ser, '0.4E', 'a.u.']
    data_list = [data_1, data_2, data_3]
    config.data_tables['qpsk_3'].extend(data_list)

    return ([], decision_parameters, decision_results)