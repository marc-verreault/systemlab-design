"""
SystemLab-Design Version 19.02
Functional block script: PIN_APD_Model
Version 1.0 (19.02 23 Feb 2019)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) Optical Communication Systems(OPT428), Govind P. Agrawal, Institute of Optics University of Rochester
http://www2.optics.rochester.edu/users/gpa/opt428a.pdf (accessed 14 Feb 2019)

"""
import os
import numpy as np
import config
from scipy import constants, special #https://docs.scipy.org/doc/scipy/reference/constants.html

import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'PIN'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']
    samples_per_sym = settings['samples_per_sym']
      
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
    #Parameter name(0), Value(1), Units(2), Notes(3)
    #General parameters (header)
    detection_model = str(parameters_input[1][1]) # Detection model (PIN, APD)
    r_qe_active = str(parameters_input[2][1]) #Responsivity model type (QE, direct)
    r_direct = float(parameters_input[3][1]) #Responsivity (W/A)
    i_d = float(parameters_input[4][1]) #Dark current (A)
    rbw = float(parameters_input[5][1]) #Receiver bandwidth (Hz)
    Q_target = float(parameters_input[6][1])
    #APD parameters (header)
    gain = float(parameters_input[8][1]) #Average avalanche gain
    x = float(parameters_input[9][1]) #Noise coefficient
    #Noise parameters (header)
    th_noise_active = int(parameters_input[11][1])#Thermal noise ON/OFF
    th_noise_model = str(parameters_input[12][1])
    th_noise_psd = float(parameters_input[13][1]) #Thermal noise PSD (A^2/Hz)
    shot_noise_active = int(parameters_input[14][1]) #Shot noise ON/OFF
    shot_noise_model = str(parameters_input[15][1]) 
    include_optical_noise = int(parameters_input[16][1]) 
    optical_noise_model = str(parameters_input[17][1]) 
    add_noise_to_signal = int(parameters_input[18][1]) 

    #Additional parameters
    qe = 1 #Quantum efficiency of detector
    r_load = 50 #Load resistance (ohm)
    T = 290 #Temperature (K)
    signal_type = 'Electrical'
    
    '''==INPUT SIGNAL======================================================='''
    time_array = input_signal_data[0][3]
    psd_array = input_signal_data[0][4]
    optical_in = input_signal_data[0][5]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    jones_vector = optical_in[0][2]
    e_field_input = optical_in[0][3]
    noise_field = optical_in[0][4]

    '''==CALCULATIONS======================================================='''
    q = constants.e # Electron charge
    h = constants.h # Planck constant

    #Calculate responsivity
    r = r_direct
    if r_qe_active == 'QE':
        r = (qe*q)/(h*(wave_freq)) # R = QE*q/h*(wave_freq)  (Ref 1, Eq 2.117)
    if detection_model == 'APD':
        r = r*gain
        
    # Calculate total and average received optical signal power
    rcv_pwr_total = np.sum(np.abs(e_field_input)*np.abs(e_field_input))
    rcv_pwr = np.mean(np.abs(e_field_input)*np.abs(e_field_input))
    
    # Calculate received optical noise power
    opt_noise_pwr = np.sum(np.abs(noise_field)*np.abs(noise_field))
    opt_noise_psd = opt_noise_pwr/fs
    if opt_noise_psd > 0:
        opt_noise_psd_dbm = 10*np.log10(opt_noise_psd*1e3)
    else:
        opt_noise_psd_dbm = 'NA'
    i_noise_opt = r*np.real(noise_field*np.conjugate(noise_field))
    
    #Convert optical power input signal to current signal
    if include_optical_noise == 2 and optical_noise_model == 'Numerical':
        #Signal and noise electrical field envelopes are added
        e_field_input += noise_field
    i_signal = r*np.real(e_field_input*np.conjugate(e_field_input)) 
    i_signal_mean = np.mean(i_signal)
    
    #Calculate average number of received photons (per symbol period)
    photons_avg = round( ((i_signal_mean*t_step)/(q*r)) * samples_per_sym )

    #APD calculations
    enf = np.power(gain, x) #Excess noise factor
    
    #Calculate thermal noise (Ref 1, Section 4.1.6)
    i_th = np.zeros(n)
    th_sigma = 0
    th_variance = 0
    if th_noise_active == 2:
        if th_noise_model == 'PSD': #Calculate thermal noise based on PSD (defined)
            th_variance = rbw*th_noise_psd #Ref 1, Eq 4.32
        else: #Calculate thermal noise variance based on load resistance (circuit model)
            k = constants.k # Boltzmann constant
            th_variance = rbw*4*k*T/r_load #Ref 1, Eq 4.32
        th_sigma = np.sqrt(th_variance)
        i_th = np.random.normal(0, th_sigma , n) #Thermal noise current array
    
    #Calculate shot noise (Ref 1, Section 4.1.4)
    i_shot = np.zeros(n)
    shot_sigma = 0
    shot_sigma_avg = 0
    shot_variance_avg = 0
    if shot_noise_active == 2:
        for i in range (0, n):
            if shot_noise_model == 'Gaussian' or detection_model == 'APD':
                shot_variance = 2*q*i_signal[i]*rbw #Ref 1, Eq 4.24
                if detection_model == 'APD':
                    shot_variance = np.square(gain)*enf*shot_variance      
                shot_sigma = np.sqrt(shot_variance)
                i_shot_sample = np.random.normal(0, shot_sigma, 1)                
            else: #Poisson
                mean_photons = round( (i_signal[i]*t_step) / q ) #Ref 1, Eq. 4.20
                photons_detected = np.random.poisson(mean_photons, 1)
                i_shot_sample = photons_detected*q/t_step #Convert to current (Ref 1, Eq. 4.22)
            i_shot[i] = i_shot_sample
        #Calculate average photons + shot noise variance
        shot_variance_avg = 2*q*i_signal_mean*rbw
        shot_sigma_avg = np.sqrt(shot_variance_avg)
        
    #Calculate noise variances (analytical) for case of optical pre-amplifier
    #Ref 1, Eq 4.41 and 4.4.2
    i_sig_ase = np.zeros(n)
    i_ase_ase = np.zeros(n)
    sig_ase_variance = 0
    ase_ase_variance = 0
    nf = 3.2
    gain = 100 #Gain of last stage (pre-amplifier)
    bw_opt = 2*rbw # Optical bandwidth (filter)
    if include_optical_noise == 2 and optical_noise_model == 'Analytical':
         # Perform these calculation if using equations to calculate beating 
         # components of optical signal and noise
        psd_ase = (gain - 1)*nf*constants.h*wave_freq
        #Signal-ASE beating: 4*(R)^2*G*amp_in_pwr*S_ase*rbw  (sig pwr is relative to amplifier in)
        sig_ase_variance = 4*(r**2)*rcv_pwr*psd_ase*rbw 
        #ASE-ASE beating: 2*(R)^2*(S_ase)^2*(2*opt_bw - rbw)*rbw
        ase_ase_variance = 2*(r**2)*(psd_ase**2)*((2*bw_opt) - rbw)*rbw
        sigma_sig_ase  = np.sqrt(sig_ase_variance)
        sigma_ase_ase  = np.sqrt(ase_ase_variance)
        i_sig_ase = np.random.normal(0, sigma_sig_ase , n)
        i_ase_ase = np.random.normal(0, sigma_ase_ase , n)
        
    #Dark current noise (Ref 1, Section 4.1.5)
    noise_d_variance = 2*q*i_d*rbw
    if detection_model == 'APD':
        noise_d_variance = np.square(gain)*enf*noise_d_variance
    noise_d_sigma = np.sqrt(noise_d_variance)
    i_d_noise = np.random.normal(0, noise_d_sigma, n)

    #Noise statistics (thermal) - for results
    th_psd_measured = np.var(i_th)/rbw
    if th_psd_measured > 0:
        th_psd_measured_dbm = 10*np.log10(th_psd_measured*1e3)
    else:
        th_psd_measured_dbm = 'NA'
    th_noise_current_measured = np.sqrt(np.var(i_th))
    
    #Noise statistics (shot) - for results
    shot_psd_measured = np.var(i_shot)/rbw
    if shot_psd_measured > 0:
        shot_psd_measured_dbm = 10*np.log10(shot_psd_measured*1e3)
    else:
        shot_psd_measured_dbm = 'NA'
    shot_noise_current_measured = np.sqrt(np.var(i_shot))
    
    #Noise statistics (dark) - for results
    dark_psd_measured = np.var(i_d_noise)/rbw
    if dark_psd_measured > 0:
        dark_psd_measured_dbm = 10*np.log10(dark_psd_measured*1e3)
    else:
        dark_psd_measured_dbm = 'NA'
    dark_noise_current_measured = np.sqrt(np.var(i_d_noise))
    
    #Noise statistics (sig_ase) - for results
    sig_ase_psd_measured = np.var(i_sig_ase)/rbw
    if sig_ase_psd_measured > 0:
        sig_ase_psd_measured_dbm = 10*np.log10(sig_ase_psd_measured*1e3)
    else:
        sig_ase_psd_measured_dbm = 'NA'
    sig_ase_current_measured = np.sqrt(np.var(i_sig_ase))
    
    #Noise statistics (ase_ase) - for results
    ase_ase_psd_measured = np.var(i_ase_ase)/rbw
    if ase_ase_psd_measured > 0:
        ase_ase_psd_measured_dbm = 10*np.log10(ase_ase_psd_measured*1e3)
    else:
        ase_ase_psd_measured_dbm = 'NA'
    ase_ase_current_measured = np.sqrt(np.var(i_ase_ase))
    
    #Total noise current (calculated)
    i_noise_calculated = np.sqrt( th_variance + shot_variance_avg + noise_d_variance
                                              + sig_ase_variance + ase_ase_variance )
    
    #Total noise current (measured)
    i_noise_measured = np.sqrt( np.var(i_th) + np.var(i_shot)+ np.var(i_d_noise)
                                               + np.var(i_sig_ase) + np.var(i_ase_ase) )
    
    # Noise current
    i_noise = i_th + i_shot + i_d_noise + i_sig_ase + i_ase_ase
    
    # Add noise arrays to detected signal
    if add_noise_to_signal == 2:
        i_signal = i_signal + i_noise
        
    # Calculate Q (based on noise data) - OOK (Ref 1, Eq 4.5.7)
    # (I1 - I0)/(sigma_1 + sigma_0) = 2*avg_current/(sigma_1 + sigma_0) 
    sigma_1 = np.sqrt( np.var(i_th) + np.var(i_shot)+ np.var(i_d_noise) 
                                 + np.var(i_sig_ase) + np.var(i_ase_ase) )
    sigma_0 = np.sqrt( np.var(i_th) + np.var(i_d_noise) + np.var(i_ase_ase))
    if sigma_1 == 0 and sigma_0 == 0:
        Q_measured = 'NA'
    else:
        Q_measured = (2*i_signal_mean) / (sigma_1 + sigma_0)
    
    # Calculate receiver sensitivities===============================================
    # Thermal noise limited case (for PIN)/Shot noise limited case (for APD) 
    # Ref 1, Eq. 4.66
    M = 1
    F_M = 1
    if detection_model == 'APD':
        M = gain
        F_M = enf
    pwr_sensitivity = (Q_target/r) * ((th_noise_current_measured/M) + (q*Q_target*F_M*rbw))
    pwr_sensitivity_dbm = 10*np.log10(pwr_sensitivity*1e3)
    
    #Pre-amplifier (optical noise) Ref 1 - Eq 4.75
    pwr_sensitivity_amp = ( nf*constants.h*wave_freq*rbw*((Q_target**2)
                                         + Q_target*np.sqrt((bw_opt/rbw)-0.5)) )
    pwr_sensitivity_amp_dbm = 10*np.log10(pwr_sensitivity_amp*1e3)
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    pin_parameters = []
    pin_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    pin_results = []
    # General results
    header_main_results = ['General results', '', '', '', True]
    avg_photocurrent_result = ['Average photocurrent (detected)', i_signal_mean*1e3,
                               'mA', ' ', False]
    avg_num_photons_per_sym = ['Average photons received per symbol period',
                               photons_avg, '', '', False]
    opt_noise_psd_in_result = ['Optical noise PSD (before detection)',
                               opt_noise_psd_dbm, 'dBm/Hz', '', False]
    responsivity_result = ['Responsivity', r, 'A/W', ' ', False]
    excess_noise_factor = ['Excess noise factor (APD)', enf, ' ', ' ', False]
    
    # Noise data (thermal)
    header_thermal_results = ['Noise statistics (thermal)', '', '', '', True]
    th_psd_measured_result = ['Thermal noise PSD (linear)', th_psd_measured,
                              'A^2/Hz', ' ', False]
    th_psd_measured_dbm_result = ['Thermal noise PSD (log)', th_psd_measured_dbm,
                                  'dBm/Hz', ' ', False]
    th_sigma_measured_result = ['Thermal noise current', 
                                th_noise_current_measured*1e9, 'nA', ' ', False]
    # Noise data(shot)
    header_shot_results = ['Noise statistics (shot)', '', '', '', True]
    shot_psd_result = ['Shot noise PSD (linear)', shot_psd_measured, 'A^2/Hz', ' ',
                         False]
    shot_psd_dbm_result = ['Shot noise PSD (log)', shot_psd_measured_dbm, 'dBm/Hz', ' ',
                         False]
    shot_sigma_result = ['Shot noise current', shot_noise_current_measured*1e9, 'nA', ' ',
                         False]
                         
    # Noise data (dark current)
    header_dark_results = ['Noise statistics (dark current)', '', '', '', True]
    dark_psd_result = ['Dark current noise PSD (linear)', dark_psd_measured, 'A^2/Hz', ' ',
                         False]
    dark_psd_dbm_result = ['Dark current noise PSD (log)', dark_psd_measured_dbm, 'dBm/Hz', ' ',
                         False]
    dark_sigma_result = ['Dark current noise', dark_noise_current_measured*1e9, 'nA', ' ',
                         False]
                         
    # Noise data (sig-ASE)
    header_sig_ase_results = ['Noise statistics analytical (Sig-ASE)', '', '', '', True]
    sig_ase_psd_measured_result = ['Sig-ASE PSD (linear)', sig_ase_psd_measured,
                              'A^2/Hz', ' ', False]
    sig_ase_psd_measured_dbm_result = ['Sig-ASE PSD (log)', sig_ase_psd_measured_dbm,
                                  'dBm/Hz', ' ', False]
    sig_ase_current_measured_result = ['Sig-ASE noise current', 
                                sig_ase_current_measured*1e9, 'nA', ' ', False]
                                
    # Noise data (sig-ASE)
    header_ase_ase_results = ['Noise statistics analytical (ASE-ASE)', '', '', '', True]
    ase_ase_psd_measured_result = ['ASE-ASE PSD (linear)', ase_ase_psd_measured,
                              'A^2/Hz', ' ', False]
    ase_ase_psd_measured_dbm_result = ['ASE-ASE PSD (log)', ase_ase_psd_measured_dbm,
                                  'dBm/Hz', ' ', False]
    ase_ase_current_measured_result = ['ASE-ASE noise current', 
                                ase_ase_current_measured*1e9, 'nA', ' ', False]                           

    # Performance results (Gaussian analysis)
    header_perf_results = ['Performance data (Gaussian analysis)', '', '', '', True]
    # Received power (optical) - average
    rcv_pwr_dbm = 10*np.log10(rcv_pwr*1e3)
    rcv_pwr_result =  ['Received optical pwr (avg)', rcv_pwr_dbm, 'dBm', ' ', False]
    # Noise current (total)
    noise_current_result = ['Total noise current', i_noise_measured*1e9, 'nA', ' ', False]
    # Q/BER target
    q_target_result = ['Q (target)', Q_target, ' ', ' ', False, '0.1f']
    ber_target = 0.5*special.erfc(Q_target/np.sqrt(2)) #Ref 1, Eq. 4.56
    ber_target_result = ['BER (target)', ber_target, ' ', ' ', False]
    # Q measured
    q_result = ['Q (measured)', Q_measured, ' ', ' ', False, '0.3f']
    # SNR
    if i_noise_calculated == 0:
        snr = 'NA'
        snr_db = 'NA'
    else:
        snr = np.square(i_signal_mean)/np.square(i_noise_calculated)
        snr_db =  10*np.log10(snr)
    snr_result = ['SNR ', snr, ' ', ' ', False, '0.3f']
    snr_db_result = ['SNR (dB)', snr_db, 'dB', ' ', False, '0.3f']
    # Sensitivity (optical)
    sensitivity_result = ['Optical receiver sensitivity - th/shot', pwr_sensitivity, 'W', ' ', False]
    sensitivity_dbm_result = ['Optical receiver sensitivity - th/shot (dBm)', pwr_sensitivity_dbm, 'dBm', ' ', False]

    pin_results = [header_main_results, avg_photocurrent_result, rcv_pwr_result, opt_noise_psd_in_result, 
                   avg_num_photons_per_sym, responsivity_result, excess_noise_factor, header_thermal_results,
                   th_psd_measured_result, th_psd_measured_dbm_result, th_sigma_measured_result, 
                   header_shot_results, shot_psd_result, shot_psd_dbm_result, shot_sigma_result, 
                   header_dark_results, dark_psd_result, dark_psd_dbm_result, dark_sigma_result, 
                   header_sig_ase_results, sig_ase_psd_measured_result, sig_ase_psd_measured_dbm_result, 
                   sig_ase_current_measured_result, header_ase_ase_results, ase_ase_psd_measured_result, 
                   ase_ase_psd_measured_dbm_result, ase_ase_current_measured_result, 
                   header_perf_results, noise_current_result, q_target_result, ber_target_result, q_result, snr_result,
                   snr_db_result, sensitivity_result, sensitivity_dbm_result]

    '''==DATA PANEL UPDATE========================================='''
    config.data_tables['opt_im_2'] = []
    data_1 = ['Iteration #', iteration, '.0f', ' ']
    data_2 = ['Received power (dBm)', rcv_pwr_dbm, '0.2f', ' ']
    data_3A = ['Q (target)', Q_target, '0.1f', ' ']
    data_3B = ['BER (target)', ber_target, '0.2E', ' ']
    data_3C = ['Q (measured)', Q_measured, '0.2f', ' ']
    data_4 = ['Optical receiver sensitivity (dBm)', pwr_sensitivity_dbm, '0.2f', ' ']
    data_list = [data_1, data_2, data_3A, data_3B, data_3C, data_4]
    config.data_tables['opt_im_2'].extend(data_list)
    
    '''==RETURN (Output Signals, Parameters, Results)==================================''' 
    return ([[2, signal_type, 0, fs, time_array, i_signal, i_noise]],
            pin_parameters, pin_results)

