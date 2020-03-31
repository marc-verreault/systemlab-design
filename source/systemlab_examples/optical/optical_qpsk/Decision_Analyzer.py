"""
Decision Analyzer module
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
    module_name = 'Decision Analyzer'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    iterations = settings['iterations']
    time = settings['time_window']
    fs = settings['sampling_rate']
    
    config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))

    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS==================================================='''
    enable_diff_decoding = int(parameters_input[0][1])
    ignore_start_samples = int(parameters_input[1][1])
    ignore_end_samples = int(parameters_input[2][1])
    
    carrier = 0
    
    #Parameters table
    decision_parameters = []
    
    '''==CALCULATIONS======================================================='''
    #Calculate symbol error rate
    bit_rate = 100e9
    symbol_rate = 50e9
   
    samples_per_bit = int(fs/bit_rate)
    samples_per_symbol = int(fs/symbol_rate)
    n_sym = int(round(n/samples_per_symbol))
    
    # Symbols based on Decision I/Decision Q
    sym_i_in = input_signal_data[2][6] #Port ID 3
    sym_q_in = input_signal_data[3][6] #Port ID 4
    n_samples = np.size(sym_i_in)
    iq_decision = np.full(n_samples, 0 + 0j)
    iq_decision = sym_i_in + 1j*sym_q_in
    
    # Access reference (transmitted) symbol values for simulation (held in project)
    sym_i_ref = project.sym_ref_i
    sym_q_ref = project.sym_ref_q
    # Sampled signal and noise arrays
    sig_in_i = input_signal_data[0][5]
    sig_in_q = input_signal_data[1][5]
    time = input_signal_data[0][4]
    noise_i = input_signal_data[0][6]
    noise_q = input_signal_data[1][6]
    
    # Differential decoding of received symbols
    # http://staff.ustc.edu.cn/~jingxi/Lecture%209_10.pdf
    hyp = np.abs(iq_decision[0])
    if enable_diff_decoding == 2:
        iq_decision_decoded = np.full(n_samples, 0 + 0j)
        iq_decision_decoded[0] = iq_decision[0]
        for g in range(1, n_samples):
            ph_coded = np.angle(iq_decision[g])
            if ph_coded < 0:
                 ph_coded += 2*np.pi
            ph_ref = np.angle(iq_decision[g-1])
            if ph_ref < 0:
                 ph_ref += 2*np.pi
            # Modulo 2 subtraction including rotation of pi/4
            ph_decoded = np.mod((ph_coded - ph_ref - np.pi/4), 2*np.pi) 
            x = np.round(hyp*np.cos(ph_decoded))
            y = np.round(hyp*np.sin(ph_decoded))
            iq_decision_decoded[g] = x + 1j*y
            
        #Set decision array to decoded symbol phases
        iq_decision = iq_decision_decoded
    
    
    
    
    
    
    
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
        decision_samples_i = np.append(decision_samples_i, sig_in_i[int(sym*samples_per_symbol) - 1])
        decision_samples_q = np.append(decision_samples_q, sig_in_q[int(sym*samples_per_symbol) - 1])
        decision_noise_i = np.append(decision_noise_i, noise_i[int(sym*samples_per_symbol) - 1])
        decision_noise_q = np.append(decision_noise_q, noise_q[int(sym*samples_per_symbol) - 1])

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
    '''if iteration == 1:
        project.ser = []
        project.ser.append(ser)
        project.simulation_analyzer = view.IterationsAnalyzer_Optical_QPSK(project.photons_per_bit,
                              project.ser, project.photons_per_bit, project.ser_th)
        project.simulation_analyzer.show()
    else:
        project.ser.append(ser)
        project.simulation_analyzer.figure.tight_layout(pad=0)
        project.simulation_analyzer.plot_xy()
        project.simulation_analyzer.canvas.draw()'''
   
    #Prepare data for constellation view
    if iteration == 1:
        project.decision_samples_dict_i = {}
        project.decision_samples_dict_q = {}
        project.recovered_sig_dict_i = {}
        project.recovered_sig_dict_q = {}
        project.evm_results_per = {}
        project.evm_results_db = {}
        
        # Ignore sampling points (for viewing)
        #   i_q_sampled = np.delete(i_q_sampled, slice(0, ignore_start_samples))
        #    last_index = len(i_q_sampled)
        #  i_q_sampled = np.delete(i_q_sampled, slice(int(last_index - ignore_end_samples), last_index))
        
    i_sampled = np.real(i_q_sampled)
    q_sampled = np.imag(i_q_sampled)
    
    project.decision_samples_dict_i [iteration] = decision_samples_i
    project.decision_samples_dict_q [iteration] = decision_samples_q
    project.recovered_sig_dict_i [iteration] = decision_samples_i
    project.recovered_sig_dict_q [iteration] = decision_samples_q
    project.evm_results_per [iteration] = 0
    project.evm_results_db [iteration] = 0
    
    if iteration == iterations:
        project.constellation = view.SignalSpaceAnalyzer('Optical QPSK Analytical Model', 
                                                        project.decision_samples_dict_i,
                                                        project.decision_samples_dict_q,
                                                        project.recovered_sig_dict_i,
                                                        project.recovered_sig_dict_q,
                                                        project.evm_results_per,
                                                        project.evm_results_db)
        project.constellation.show()
    
  
    '''==RESULTS============================================================'''
    decision_results = []
    
    #Send update to data panel (opt_qpsk_1)
    config.data_tables['opt_qpsk_1'] = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['Number symbols received', n_sym, '.0f', 'a.u.']     
    data_3 = ['Number of errored symbols', err_count, '.0f', 'a.u.']  
    data_4 = ['SER', ser, '0.5E', 'a.u.']
    ser_th = project.ser_th[iteration-1]
    data_5 = ['SER (Th)', ser_th, '0.5E', 'a.u.']
    data_list = [data_1, data_2, data_3, data_4, data_5]
    config.data_tables['opt_qpsk_1'].extend(data_list)

    return ([], decision_parameters, decision_results)