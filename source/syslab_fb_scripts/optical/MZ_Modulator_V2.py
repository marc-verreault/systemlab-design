"""
SystemLab-Design Version 20.01.r1
Functional block script: Mach Zhender Modulator
Version 2.0 (26 Sep 2019)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
"""
import numpy as np
import config

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS=============================================================='''
    module_name = 'MZM'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate']
    
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS=================================================================
    '''
    # Load parameters from FB parameters table
    # Parameter name(0), Value(1), Units(2), Notes(3)
    v_pi = float(parameters_input[0][1]) #Differential drive voltage (V)
    loss =  float(parameters_input[1][1]) #Insertion loss (dB)
    e_ratio = float(parameters_input[2][1]) #Extinction ratio (dB)
    disp_trans_fcn = int(parameters_input[3][1]) #Display transfer function?
    
    '''==INPUT SIGNALS===================================================================='''
    # Load optical group data from input port
    signal_type = input_signal_data[0][1]
    time_array = input_signal_data[0][3] # Sampled time array
    psd_array = input_signal_data[0][4] # Noise groups
    opt_channels = input_signal_data[0][5] #Optical channel list
    
    # Load frequency, jones vector, signal & noise field envelopes for each optical channel
    channels = len(opt_channels)
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2:
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector[ch] = opt_channels[ch][2]
        opt_field_rcv[ch] = opt_channels[ch][3]
        noise_field_rcv[ch] = opt_channels[ch][4]
        
    # Load electrical driver data
    v1 = input_signal_data[1][5] #Upper arm (input port ID = 3)
    v2 = input_signal_data[2][5] #Lower arm (input port ID = 4)
    
    '''==CALCULATIONS=====================================================================
    '''   
    # MZ modulator transfer function (Ref 1, Eq 5.56)
    # Eout = 0.5*[exp(j*(pi/v_pi)*V1) + exp(j*(pi/v_pi)*V2)]*Ein, where V1/V2 are 
    # upper/lower arm driver voltages
    e_ratio_linear = np.power(10, -e_ratio/10)
    loss_linear = np.power(10, -loss/10)
    if opt_channels[0][3].ndim == 2:
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels):
        #Signal field
        opt_field_out[ch] = np.sqrt(loss_linear) * opt_field_rcv[ch]*0.5*( (1+np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*v1)
                                + (1- np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*v2) )
        #Noise field
        noise_field_out[ch] = np.sqrt(loss_linear) * noise_field_rcv[ch]*0.5*( (1+np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*v1)
                                + (1- np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*v2) )
                             
    #Calculate DC bias of each arm & operating point of modulator
    Y_v1 = np.fft.fft(v1)/n
    Y_v2 = np.fft.fft(v2)/n
    v1_bias = np.real(Y_v1[0])
    v2_bias = np.real(Y_v2[0])
    v_op_point = (v1_bias - v2_bias)/v_pi
    
    if disp_trans_fcn == 2: #Based on Fig 5-15 of Ref 1
        # Assume input field amplitude is 1
        v = np.linspace(-2.0, 2.0, 200) #V/Vpi linear range
        v_tf = v*v_pi
        # Calculate e-field for all voltage points of v
        e_field = np.sqrt(loss_linear)*0.5*( (1+np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*(v_tf/2))
                             + (1- np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi/v_pi)*(-v_tf/2)) )
        # Determine e-field at operating point
        e_field_at_bias = np.sqrt(loss_linear)*0.5*( (1+np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi)*(v_op_point/2))
                             + (1- np.sqrt(e_ratio_linear))*np.exp(1j*(np.pi)*(-v_op_point/2)) )
        
        #Create an MZM graphing object (with data) and display results
        config.mzm_graph = config.view.MZMAnalyzer(v, e_field, e_field_at_bias,
                                                                   v_op_point)
        config.mzm_graph.show()
        
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    MZM_parameters = []
    MZM_parameters = parameters_input 
    
    '''==RESULTS==========================================================================
    '''
    MZM_results = []
    v_pi_result = [' Differential drive voltage', v_pi, 'V', ' ', False,  '0.2f']
    v1_bias_result = ['DC bias upper arm (V)', v1_bias, 'V', ' ', False,  '0.2f']
    v2_bias_result = ['DC bias lower arm (V)', v2_bias, 'V ', ' ', False,  '0.2f']
    mz_op_voltage_result = ['Operating point (V/Vpi)', v_op_point, ' ', ' ', False, '0.2f']
    
    MZM_results = [v_pi_result, v1_bias_result, v2_bias_result, mz_op_voltage_result]

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels]], MZM_parameters, MZM_results)

