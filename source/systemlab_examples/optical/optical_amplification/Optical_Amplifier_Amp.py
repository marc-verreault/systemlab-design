"""
SystemLab-Design Version 19.02
Functional block script: Optical Amplifier
Version 1.0 (19.02 23 Feb 2019)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) http://www2.engr.arizona.edu/~ece487/opamp1.pdf (accessed 17 Apr 2019)
"""
import numpy as np
import config

from scipy import constants # https://docs.scipy.org/doc/scipy/reference/constants.html

#import project_amplifier and systemlab_viewers
import project_amplifier as project
import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Amplifier'
    #Main settings
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))   
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    iteration = settings['current_iteration'] #Current iteration loop for simulation    
    iterations = settings['iterations'] #Total iterations for project
    
    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==INPUT PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Main amplifier parameters (header)
    g_o_db = float(parameters_input[1][1]) #Small signal gain
    pwr_sat_dbm = float(parameters_input[2][1]) #Saturated output power (dBm)
    nf_db = float(parameters_input[3][1]) #Noise figure (optical)
    #Operating parameters (header)
    mode = str(parameters_input[5][1])
    gain_setting_db = float(parameters_input[6][1]) 
    pwr_setting_dbm = float(parameters_input[7][1])
    # Noise analysis (header)
    add_ase = int(float(parameters_input[9][1]))
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3] 
    psd_array = input_signal_data[0][4] 
    optical_in = input_signal_data[0][5]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input = optical_in[0][3]
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    
    '''==CALCULATIONS======================================================='''       
    # Gain calculation
    g_o = np.power(10, g_o_db/10)
    pwr_in = np.mean(np.square(np.abs(e_field_input)))
    p_out = pwr_in * g_o
    pwr_sat = 1e-3*np.power(10, pwr_sat_dbm/10)

    # Solve large signal gain implicit equation (G = Go*exp(-((G-1)*Pout)/G*(Psat))
    # where Psat is the output saturation power (output power where gain (G) drops by 3 dB)
    # Ref 1, Eq. 2.92 & Ref 2
    g = g_o
    counter = 0
    resolution = 0.005 #Convergence criterium
    while True:
        if counter > 30: #Stop after 30 iterations
            break
        p_out_target = pwr_in * g
        g_target = g_o*np.exp(-((g-1)/g) * (p_out_target/pwr_sat))
        if g_target/g < 1 - resolution: #g is too high
            g = 0.5 * (g - g_target)
            counter += 1
        elif g_target/g > 1 + resolution: #g is too low
            g = 0.5 * (g_target + g)
            counter += 1
        else:
            break
    
    # Apply calculated gain to input signal/noise fields
    p_out = pwr_in * g
    if mode == 'None':
        pass
    elif mode == 'Gain control':
        gain_setting = np.power(10, gain_setting_db/10)
        if gain_setting < g:
            g = gain_setting
    else: 
        pwr_setting = 1e-3*np.power(10, pwr_setting_dbm/10) 
        if pwr_setting < p_out:
            g = pwr_setting/pwr_in

    e_field_output = e_field_input * np.sqrt(g)
    noise_array = noise_array * np.sqrt(g)
    
    # Amplifier ASE calculation
    nf = np.power(10, nf_db/10)
    psd_ase = (g - 1)*nf*constants.h*wave_freq/2 # Ref 1, Eq 4.34
    
    # Add noise to psd array
    ng = len(psd_array[0, :])
    psd_out = np.array([psd_array[0, :], np.zeros(ng)])
    for i in range(0, ng): # psd_out = psd_ase + psd_in*g 
        psd_out[1, i] = psd_ase + (psd_array[1, i]*g)
        
    # Integrate ase noise with time-domain noise?
    pwr_ase = 0
    if add_ase == 2:
        # Build time-domain freq points
        T = n/fs
        k = np.arange(n)
        frq = (k/T)
        frq = frq - frq[int(round(n/2))] + wave_freq
        ng_w = psd_array[0, 1] - psd_array[0, 0]
        for i in range(0, ng):
            if psd_array[0, i] > frq[0] and psd_array[0, i] < frq[n-1]:
                pwr_ase += psd_out[1, i]*ng_w
                
        #Convert to time-domain noise
        sigma_ase = np.sqrt(pwr_ase)
        noise_ase = np.random.normal(0, sigma_ase , n)
        noise_array += noise_ase
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    opt_amp_parameters = []
    opt_amp_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    opt_amp_results = []
    gain_db = 10*np.log10(g)
    gain_result =  ['Amplifier gain (dB)', gain_db, 'dB', ' ', False]
    gain_result_lin =  ['Amplifier gain (linear)', g, ' ', ' ', False]
    psd_amplifier_result = ['Amplifier ASE (avg PSD)', psd_ase, 'A^2/Hz', ' ', False]
    psd_ase_out_result = ['Output ASE (avg PSD)', pwr_ase/fs, 'A^2/Hz', ' ', False]
    opt_amp_results = [gain_result, gain_result_lin, psd_amplifier_result, psd_ase_out_result]
    
    '''=DATA LIST FOR GRAPHING==========================================='''
    
    if iteration == 1: 
        # First iteration - clear the contents of the gain_db list
        project.gain_db = []
    # List is updated with new gain value over each iteration
    project.gain_db.append(gain_db) 
     
    if iteration == iterations: 
        # Last iteration - instantiate the xy graph and display results
        project.amplifier_analyzer = view.IterationsAnalyzer_Optical_Amp(project.amp_input_power_dbm, 
                                                                                                    project.gain_db)
        project.amplifier_analyzer.show()

    '''==RETURN (Output Signals, Parameters, Results)=========================='''      
    optical_P2 = [[wave_key, wave_freq, jones_vector, e_field_output, noise_array]]
      
    return ([[2, signal_type, fs, time_array, psd_out, optical_P2]], 
              opt_amp_parameters, opt_amp_results)

