"""
SystemLab-Design Version 20.01.r3 16-Jun-20
Functional block script: PIN_APD_Model
Version 1.0 (19.02.r1 23 Feb 2019)
Version 2.0 (15 Nov 2019)
Version 3.0 (16 Jun 2020)

Refs:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication Systems and Networks, 
(Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) Optical Communication Systems(OPT428), Govind P. Agrawal, Institute of Optics University of Rochester
http://www2.optics.rochester.edu/users/gpa/opt428a.pdf (accessed 14 Feb 2019)
3) Sfez, Tristan; Investigation of Surface Electromagnetic Waves with Multi-Heterodyne Scanning Near-Field
Optical Microscopy, Thesis No 4671, École Polytechnique Fédérale de Lausanne (2010)
Source: https://pdfs.semanticscholar.org/8f29/d261b038c5634118ae330bf95869741fbd31.pdf
(Accessed 12-Nov-2019)
4) Optical Communication Systems(OPT428), Govind P. Agrawal, Institute of Optics University of Rochester
http://www2.optics.rochester.edu/users/gpa/opt428c.pdf (accessed 20 Aug 2020)

"""
import os
import numpy as np
import copy
import config
from scipy import constants, special 
#https://docs.scipy.org/doc/scipy/reference/constants.html

import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = settings['fb_name']
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']
    samples_per_sym = settings['samples_per_sym']
    
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
    
    '''==INPUT PARAMETERS========================================================='''
    # Load parameters from FB parameters table (Parameter name(0), Value(1), Units(2), Notes(3))
    # General parameters (header)
    opt_regime = str(parameters_input[1][1]) # Optical regime (Coherent, Incoherent)
    detection_model = str(parameters_input[2][1]) # Detection model (PIN, APD)
    r_qe_active = str(parameters_input[3][1]) #Responsivity model type (QE, direct)
    qe = float(parameters_input[4][1]) #Quantum efficiency
    r_direct = float(parameters_input[5][1]) #Responsivity (W/A)
    i_d = float(parameters_input[6][1])*1e-9 #Dark current (nA -> A)
    rbw = float(parameters_input[7][1]) #Receiver bandwidth (Hz)
    q_target = float(parameters_input[8][1])
    # Export q target to proj config
    # proj.q_target = q_target
    # APD parameters (header)
    m_apd = float(parameters_input[10][1]) #Average avalanche gain
    enf_model = str(parameters_input[11][1])
    x_apd = float(parameters_input[12][1]) # Noise coefficient (x)
    k_apd = float(parameters_input[13][1]) # Ionization coefficient (k)
    # Noise parameters (header)
    th_noise_active = int(parameters_input[15][1])#Thermal noise ON/OFF
    th_noise_model = str(parameters_input[16][1])
    th_noise_psd = float(parameters_input[17][1]) #Thermal noise PSD (A^2/Hz)
    noise_temp = float(parameters_input[18][1]) #Thermal noise temperature (K)
    r_load = float(parameters_input[19][1]) #Load resistance (ohm)
    shot_noise_active = int(parameters_input[20][1]) #Shot noise ON/OFF
    shot_noise_model = str(parameters_input[21][1]) 
    include_optical_noise = int(parameters_input[22][1]) 
    optical_noise_model = str(parameters_input[23][1])
    opt_filter_bw = float(parameters_input[24][1])*1e9
    # Output noise settings (header)
    add_noise_to_signal = int(parameters_input[26][1])
    # Results settings (header)
    display_pin_apd_noise_metrics = int(parameters_input[28][1])
    display_optical_noise_metrics = int(parameters_input[29][1])
    ch_key_ref = int(parameters_input[30][1])
    data_panel_id = str(parameters_input[31][1])
    enable_data_export = int(parameters_input[32][1])
    data_att_1 = str(parameters_input[33][1])
    
    '''==INPUT SIGNAL======================================================='''
    time_array = input_signal_data[0][3]
    psd_array = input_signal_data[0][4]
    opt_channels = input_signal_data[0][5] #Optical channel list
    channels = len(opt_channels)
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    
    """Extract signal and noise field envelopes for each optical channel--------------------------------"""
    signal_type = 'Electrical'
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    if opt_channels[0][3].ndim == 2:
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex)
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    #noise_field_rcv_cpol = np.full([channels, n], 0 + 1j*0, dtype=complex)  
    #noise_field_rcv_orth = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        opt_field_rcv[ch] = copy.deepcopy(opt_channels[ch][3])
        jones_vector[ch] = copy.deepcopy(opt_channels[ch][2])
        noise_field_rcv[ch] = copy.deepcopy(opt_channels[ch][4])
        # Co-polarized component of noise field (50% of received ASE power)
        #noise_field_rcv_cpol[ch] = copy.deepcopy(opt_channels[ch][4])/np.sqrt(2)
        # Orthogonal component of noise field (50% of received ASE power)
        #noise_field_rcv_orth[ch] = copy.deepcopy(opt_channels[ch][4])/np.sqrt(2)

    '''==CALCULATIONS======================================================='''
    q = constants.e # Electron charge
    h = constants.h # Planck constant
    pi = constants.pi
    
    """ Calculate OSNR--------------------------------------------------------------------"""
    rcv_sig_pwr_ch = 0
    rcv_noise_pwr_ch = 0
    ch_index = 0
    indices = np.where(wave_key == ch_key_ref)
    if np.size(indices[0]) > 0:
        ch_index = indices[0][0]
    T = n/fs
    k_freq = np.arange(n)
    frq = k_freq/T # Positive/negative freq (double sided)
    frq = frq - frq[int(round(n/2))] + wave_freq[ch_index]
    
    Y = np.fft.fftshift(np.fft.fft(opt_field_rcv[ch_index]))
    N = np.fft.fftshift(np.fft.fft(noise_field_rcv[ch_index]))
    tr_fcn_filt = rect_profile(frq, wave_freq[ch_index], opt_filter_bw)
    Y = Y*tr_fcn_filt
    N = N*tr_fcn_filt
    
    osnr_sig_array = np.fft.ifft(np.fft.ifftshift(Y))
    osnr_noise_array = np.fft.ifft(np.fft.ifftshift(N))
    rcv_sig_pwr_ch = calculate_total_opt_pwr(osnr_sig_array)
    rcv_noise_pwr_ch = calculate_total_opt_pwr(osnr_noise_array)
    
    if rcv_noise_pwr_ch > 0 and rcv_sig_pwr_ch > 0:
        osnr_linear = rcv_sig_pwr_ch/rcv_noise_pwr_ch
        osnr = 10*np.log10(osnr_linear)
    else:
        osnr = 'NA'
    if osnr != 'NA':
        #q_osnr = np.sqrt((osnr_linear/2) * (opt_filter_bw/rbw))
        # Ref 4, slide 286 (assumes NRZ, infinite extinction ratio, ASE only)
        q_osnr = (osnr_linear*np.sqrt(opt_filter_bw/rbw)) / (np.sqrt(2*osnr_linear + 1) + 1)
    else:
        q_osnr = 'NA'
    m = opt_filter_bw/rbw
    # Ref 4, slide 286 (assumes NRZ, infinite extinction ratio, ase only)
    osnr_target = (2*q_target*q_target/m) + (2*q_target/np.sqrt(m))
    osnr_target = 10*np.log10(osnr_target)
        
    """ Calculate responsivities (for each channel)--------------------------------------------------------------"""
    r = np.empty(channels)
    for ch in range(0, channels):
        r[ch] = r_direct
    if r_qe_active == 'QE':
        for ch in range(0, channels):
            r[ch] = (qe*q)/(h*(wave_freq[ch])) # R = QE*q/h*(wave_freq)  (Ref 1, Eq 2.117)
            
    """ Extinction ratio calculation--------------------------------------------------------------------------------"""
    ch_index = 0
    indices = np.where(wave_key == ch_key_ref)
    if np.size(indices[0]) > 0: 
        ch_index = indices[0][0]
    P0 = 0
    P1 = 0
    avg_pwr = calculate_avg_opt_pwr(opt_field_rcv[ch_index] + noise_field_rcv[ch_index])
    count_P0 = 0
    count_P1 = 0
    for i in range(0, n):
        pwr = np.square(np.abs(opt_field_rcv[ch_index, i] + noise_field_rcv[ch_index, i]))
        if pwr  > avg_pwr:
            P1 += pwr
            count_P1 += 1
        else:
            P0 += pwr
            count_P0 += 1
    if count_P1 > 0:
        P1 = P1/count_P1
    P0 = P0/count_P0
    ext_ratio_linear = P1/P0
    
    # Export extinction ratio to project config
    #proj.ext_ratio_linear = ext_ratio_linear
    ext_ratio_rcvr_db = 10*np.log10(P1/P0)
    r_ext = P0/P1
    
    """ Calculate total received fields-----------------------------------------------------------------------------"""
    e_field_input_super_x = np.full(n, 0 + 1j*0, dtype=complex) 
    e_field_input_super_y = np.full(n, 0 + 1j*0, dtype=complex)
    e_field_noise_super_x = np.full(n, 0 + 1j*0, dtype=complex)  
    e_field_noise_super_y = np.full(n, 0 + 1j*0, dtype=complex)
    
    for ch in range(0, channels):
        # If coherent selected, model interference effects (signal beating)
        if opt_regime == 'Coherent': 
            for i in range (0, n):
                if opt_channels[0][3].ndim == 2:
                    opt_field_rcv[ch, 0, i] = opt_field_rcv[ch, 0, i]*np.exp(1j*2*pi*wave_freq[ch]*time_array[i])
                    opt_field_rcv[ch, 1, i] = opt_field_rcv[ch, 1, i]*np.exp(1j*2*pi*wave_freq[ch]*time_array[i])
                else:
                    opt_field_rcv[ch, i] = opt_field_rcv[ch, i]*np.exp(1j*2*pi*wave_freq[ch]*time_array[i])
                # Co-polarized component of noise field
                #noise_field_rcv_cpol[ch, i] = noise_field_rcv_cpol[ch, i]*np.exp(1j*2*pi*wave_freq[ch]*time_array[i])
                
            # Add channel fields together (linear superposition)
            if opt_channels[0][3].ndim == 2:
                e_field_input_super_x += opt_field_rcv[ch, 0]
                e_field_input_super_y += opt_field_rcv[ch, 1]
                e_field_noise_super_x += jones_vector[ch, 0] * (noise_field_rcv[ch])
                e_field_noise_super_y += jones_vector[ch, 1] * (noise_field_rcv[ch])
            else:
                e_field_input_super_x += opt_field_rcv[ch]
                e_field_noise_super_x += noise_field_rcv[ch] 
                #e_field_noise_super_x += noise_field_rcv_cpol[ch]
                
            # If optical noise/numerical is selected, add noise field to received signals 
            # NOT BEING CALLED-------------
            if include_optical_noise == 2 and optical_noise_model == 'Numerical':
                if opt_channels[0][3].ndim == 2:
                    e_field_input_super_x += e_field_noise_super_x
                    e_field_input_super_y += e_field_noise_super_y
                else:
                    e_field_input_super_x += e_field_noise_super_x
                    
        """ Calculate received optical powers - |E(t)|^2-----------------------------------------------------------"""
        rcv_pwr_total = 0
        rcv_pwr = 0
        opt_noise_pwr_total = 0
        opt_noise_pwr = 0
        if opt_regime == 'Coherent': 
            if opt_channels[0][3].ndim == 2:
                # Total power
                rcv_pwr_total = calculate_total_opt_pwr(e_field_input_super_x)
                rcv_pwr_total += calculate_total_opt_pwr(e_field_input_super_y)
                # Average power
                rcv_pwr = calculate_avg_opt_pwr(e_field_input_super_x)
                rcv_pwr += calculate_avg_opt_pwr(e_field_input_super_y)
                # Noise power (total)
                opt_noise_pwr_total = calculate_total_opt_pwr(e_field_noise_super_x)
                opt_noise_pwr_total += calculate_total_opt_pwr(e_field_noise_super_y)
                opt_noise_pwr = calculate_avg_opt_pwr(e_field_noise_super_x)
                opt_noise_pwr += calculate_avg_opt_pwr(e_field_noise_super_y)
            else:
                rcv_pwr_total = calculate_total_opt_pwr(e_field_input_super_x)
                rcv_pwr = calculate_avg_opt_pwr(e_field_input_super_x)
                opt_noise_pwr_total = calculate_total_opt_pwr(e_field_noise_super_x)
                opt_noise_pwr = calculate_avg_opt_pwr(e_field_noise_super_x)
        else:
            if opt_channels[0][3].ndim == 2:
                rcv_pwr_total += calculate_total_opt_pwr(opt_field_rcv[ch, 0])
                rcv_pwr_total += calculate_total_opt_pwr(opt_field_rcv[ch, 1])
                rcv_pwr += calculate_avg_opt_pwr(opt_field_rcv[ch, 0])
                rcv_pwr += calculate_avg_opt_pwr(opt_field_rcv[ch, 1])
            else:
                rcv_pwr_total += calculate_total_opt_pwr(opt_field_rcv[ch])
                rcv_pwr += calculate_avg_opt_pwr(opt_field_rcv[ch])
            opt_noise_pwr_total += calculate_total_opt_pwr(noise_field_rcv[ch])
            opt_noise_pwr += calculate_avg_opt_pwr(noise_field_rcv[ch])
            
    # Calculate noise PSD
    opt_noise_psd = opt_noise_pwr_total/fs/n
    if opt_noise_psd > 0:
        opt_noise_psd_dbm = 10*np.log10(opt_noise_psd*1e3)
    else:
        opt_noise_psd_dbm = 'NA'
    
    """Calculate detector currents -------------------------------------------------------------------"""
    i_signal = np.zeros(n)
    m = 1
    if detection_model == 'APD':
        m = m_apd
    r_mean = np.mean(r)
    # COHERENT MODEL----------------------------------------------------
    # Ref 3 (Eq 3.10): I(t) = [E1(Ch1) + E(Ch2) + ... + E(ChN)] x [(E1(Ch1) + E(Ch2) + ... + E(ChN)]*
    # i_received = responsivity*I(t)
    # Export responsivity to project config
    # proj.r = r_mean*m # Include amplification factor for APD
    if opt_regime == 'Coherent': 
        if opt_channels[0][3].ndim == 2:
            i_signal = m*r_mean*np.real(e_field_input_super_x*np.conjugate(e_field_input_super_x)) 
            i_signal += m*r_mean*np.real(e_field_input_super_y*np.conjugate(e_field_input_super_y)) 
        else:
            i_signal = m*r_mean*np.real(e_field_input_super_x*np.conjugate(e_field_input_super_x))
            
        '''if include_optical_noise == 2 and optical_noise_model == 'Numerical':
            for ch in range(0, channels):
                i_signal += m*r[ch]*np.square(np.abs(noise_field_rcv_orth[ch]))'''
    else:
        for ch in range(0, channels):
            i_signal += m*r[ch]*np.square(np.abs(opt_field_rcv[ch]))
    
    i_signal_mean = np.mean(i_signal)
    # Calculate average number of received photons (per symbol period)
    photons_avg = np.round( ((i_signal_mean*t_step)/(q*r[0])) * samples_per_sym )

    # APD excess noise factor calculation (x is noise coefficient, k is ionization coefficient)
    # Ref 1, Eqs 4.27/4.28 & Table 4.1
    # InGaAs (x=0.5-0.8, k=0.3-0.6), Ge (x=1.0, k=0.7-1.0), 
    # Si (x=0.4-0.5, k=0.02-0.04)
    if enf_model == 'Noise coeff.':
        enf_apd = np.power(m_apd, x_apd) # Excess noise factor
    else:
        enf_apd = k_apd*m_apd + (1 - k_apd)*(2 - (1/m_apd))
        
    """Calculate thermal noise (Ref 1, Section 4.1.6)------------------------------------------------"""
    i_th = np.zeros(n)
    th_sigma = 0
    th_variance = 0
    if th_noise_active == 2:
        if th_noise_model == 'PSD': #Calculate thermal noise based on PSD (defined)
            th_variance = rbw*th_noise_psd #Ref 1, Eq 4.32
        else: #Calculate thermal noise variance based on load resistance (circuit model)
            k = constants.k # Boltzmann constant
            th_variance = rbw*4*k*noise_temp/r_load #Ref 1, Eq 4.32
        th_sigma = np.sqrt(th_variance)
        i_th = np.random.normal(0, th_sigma , n) # Thermal noise current array
    
    """Calculate shot noise (Ref 1, Section 4.1.4)----------------------------------------------------"""
    i_shot = np.zeros(n)
    shot_sigma = 0
    shot_sigma_avg = 0
    shot_variance_avg = 0
    if shot_noise_active == 2:
        for i in range (0, n):
            if shot_noise_model == 'Gaussian' or detection_model == 'APD':
                shot_variance = 2*q*i_signal[i]*rbw # Ref 1, Eq 4.24
                if detection_model == 'APD':
                    # MV 20.01.r3 15-Jun-20: Bug fix, i_signal was already increased by 
                    # factor of m_apd (during i_signal calculation) so m_apd^2 was changed
                    # to m_apd
                    shot_variance = m_apd*enf_apd*shot_variance 
                shot_sigma = np.sqrt(shot_variance)
                i_shot_sample = np.random.normal(0, shot_sigma, 1)                
            else: #Poisson
                mean_photons = round( (i_signal[i]*t_step) / q ) #Ref 1, Eq. 4.20
                photons_detected = np.random.poisson(mean_photons, 1)
                i_shot_sample = photons_detected*q/t_step # Convert to current (Ref 1, Eq. 4.22)
                i_shot_sample = i_shot_sample - i_signal[i] # MV 20.01.r3 21-Aug-20
            i_shot[i] = i_shot_sample
        # Calculate average photons + shot noise variance
        shot_variance_avg = 2*q*i_signal_mean*rbw
        shot_sigma_avg = np.sqrt(shot_variance_avg)
        
    """Calculate noise variances (ASE)-----------------------------------------------------------------"""
    i_sig_ase = np.zeros(n)
    i_ase_ase = np.zeros(n)
    sig_ase_variance = 0
    ase_ase_variance = 0
    sig_ase_variance_avg = 0
    count = 0
    pwr_ase = 0
    psd_ase = 0
    if include_optical_noise == 2 and optical_noise_model == 'Analytical':
        # Check if psd has already been converted (from optical noise received)
        if opt_noise_psd_dbm < -200.0: 
            ng_w = psd_array[0, 1] - psd_array[0, 0]
            ng = len(psd_array[0, :])
            for ch in range(0, channels):
                # Build time-domain freq points
                T = n/fs
                k = np.arange(n)
                frq = (k/T)
                frq = frq - frq[int(round(n/2))] + wave_freq[ch]
                for i in range(0, ng):
                    if psd_array[0, i] > frq[0] and psd_array[0, i] < frq[n-1]:
                        count += 1
                        pwr_ase += 2*psd_array[1, i]*ng_w # Ref 1, Eq 4.37 (Pwr = 2*psd_ase*bw)
                        #psd_ase += psd_array[1, i]
                        psd_array[1, i] = 0
            # Calculate average PSD
            #psd_ase = psd_ase/count
            psd_ase = pwr_ase/fs
        else:
            psd_ase = opt_noise_psd
        # Ref 1, Eq 4.42 & Ref 4, Slide 271
        ase_ase_variance = 2*(r_mean**2)*(psd_ase**2)*((2*opt_filter_bw) - rbw)*rbw
        i_ase_ase = np.random.normal(0, np.sqrt(ase_ase_variance), n)
        # Calculate signal-ase beating noise
        for i in range (0, n):
            s_pwr = np.square(np.abs(opt_field_rcv[ch_index, i]))
            # Ref 1, Eq 4.43 & Ref 4, Slide 271
            sig_ase_variance = 4*(r_mean**2)*(s_pwr*psd_ase)*rbw
            i_sig_ase[i] = np.random.normal(0, np.sqrt(sig_ase_variance), 1)
        # Calculate average variance (all samples)
        sig_ase_variance_avg = 4*(r_mean**2)*rcv_pwr*psd_ase*rbw

    """Calculation of noise statistics for results-----------------------------------------------------"""
    # Dark current noise (Ref 1, Section 4.1.5)
    noise_d_variance = 2*q*i_d*rbw
    if detection_model == 'APD':
        noise_d_variance = np.square(m_apd)*enf_apd*noise_d_variance #Ref 1, Eq 4.30
    noise_d_sigma = np.sqrt(noise_d_variance)
    i_d_noise = np.random.normal(0, noise_d_sigma, n)
    
    # Noise statistics (thermal) - for results
    th_psd_measured = np.var(i_th)/rbw
    if th_psd_measured > 0:
        th_psd_measured_dbm = 10*np.log10(th_psd_measured*1e3)
    else:
        th_psd_measured_dbm = 'NA'
    th_noise_current_measured = np.sqrt(np.var(i_th))
    
    # Noise statistics (shot) - for results
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
                                              + sig_ase_variance_avg + ase_ase_variance )
    
    #Total noise current (measured)
    i_noise_measured = np.sqrt( np.var(i_th) + np.var(i_shot)+ np.var(i_d_noise)
                                               + np.var(i_sig_ase) + np.var(i_ase_ase) )
    
    #Calculate noise current (total)--------------------------------------------------------------------
    i_noise = i_th + i_shot + i_d_noise + i_sig_ase + i_ase_ase
    
    """Add noise current to detected signal (if add signal to noise is True)--------------------------"""
    if add_noise_to_signal == 2:
        i_signal = i_signal + i_noise
        i_noise = np.zeros(n) # MV 20.01.r3 22-Jun-20
    i_mean = np.mean(i_signal)
    i_mean_1 = np.mean(i_signal[i_signal > i_mean])
    i_mean_0 = np.mean(i_signal[i_signal < i_mean])
    i_sigma_1 = np.std(i_signal[i_signal > i_mean])
    i_sigma_0 = np.std(i_signal[i_signal < i_mean])
    if i_sigma_1 == 0 and i_sigma_0 == 0:
        q_measured = 'NA'
    else:
        q_measured =  (i_mean_1 - i_mean_0)/(i_sigma_1 + i_sigma_0)
    
    """Calculate receiver sensitivities--------------------------------------------------------------------"""
    # Ref 1, Eq. 4.66
    m = 1
    f_m = 1
    if detection_model == 'APD':
        m = m_apd
        f_m = enf_apd
    pwr_sensitivity = (q_target/r_mean) * ((th_noise_current_measured/m) + (q*q_target*f_m*rbw))
    pwr_sensitivity_dbm = 10*np.log10(pwr_sensitivity*1e3)
    
    #Pre-amplifier (optical noise) Ref 1 - Eq 4.75
    #pwr_sensitivity_amp = ( nf*constants.h*wave_freq_mean*rbw*((q_target**2)
    #                                     + q_target*np.sqrt((bw_opt/rbw)-0.5)) )
    #pwr_sensitivity_amp_dbm = 10*np.log10(pwr_sensitivity_amp*1e3)
    
    # Calculations of receiver sensitivity with extinction ratio
    q_target_ex = q_target*( (1 + r_ext)/(1 - r_ext) )
    pwr_sensitivity_ex = (q_target_ex/r_mean) * ((th_noise_current_measured/m) + (q*q_target_ex*f_m*rbw))
    pwr_sensitivity_ex_dbm = 10*np.log10(pwr_sensitivity_ex*1e3)
    pwr_penalty_ext_dB = pwr_sensitivity_ex_dbm - pwr_sensitivity_dbm
    
    '''==OUTPUT PARAMETERS LIST============================================='''
    pin_apd_parameters = []
    pin_apd_parameters = parameters_input
  
    '''==RESULTS============================================================'''
    results = []
    """ Noise metrics-----------------------------------------------------------------------------"""
    # General results
    results.append(['General results', '', '', '', True])
    #rcv_pwr = 1 # MV 20.01.r3 4-Jun-20 (Commented out)
    rcv_pwr_dbm = 10*np.log10(rcv_pwr*1e3)
    results.append(['Received optical pwr (avg)', rcv_pwr_dbm, 'dBm', ' ', False, '0.2f'])
    results.append(['Average photons received per symbol period', photons_avg, '', '', False])
    results.append(['Average photocurrent (detected)', i_signal_mean*1e3, 'mA', ' ', False])
    results.append(['Optical noise PSD (before detection)', opt_noise_psd_dbm, 'dBm/Hz', '', False, '0.2f'])
    results.append(['Responsivity (mean)', r_mean, 'A/W', ' ', False, '0.2f'])
    results.append(['Excess noise factor (APD)', enf_apd, ' ', ' ', False, '0.2f'])
    
    if display_pin_apd_noise_metrics == 2:
        # Noise data (thermal)
        results.append(['Noise statistics (thermal)', '', '', '', True])
        results.append(['Thermal noise PSD (linear)', th_psd_measured, 'A^2/Hz', ' ', False])
        results.append(['Thermal noise PSD (log)', th_psd_measured_dbm, 'dBm/Hz', ' ', False])
        results.append(['Thermal noise current', th_noise_current_measured*1e9, 'nA', ' ', False])
                                
        # Noise data (shot)
        results.append(['Noise statistics (shot)', '', '', '', True])
        results.append(['Shot noise PSD (linear)', shot_psd_measured, 'A^2/Hz', ' ', False])
        results.append(['Shot noise PSD (log)', shot_psd_measured_dbm, 'dBm/Hz', ' ', False])
        results.append(['Shot noise current', shot_noise_current_measured*1e9, 'nA', ' ', False])
                         
        # Noise data (dark current)
        results.append(['Noise statistics (dark current)', '', '', '', True])
        results.append(['Dark current noise PSD (linear)', dark_psd_measured, 'A^2/Hz', ' ', False])
        results.append(['Dark current noise PSD (log)', dark_psd_measured_dbm, 'dBm/Hz', ' ', False])
        results.append(['Dark current noise', dark_noise_current_measured*1e9, 'nA', ' ', False])
                         
    if display_optical_noise_metrics == 2:
        # Noise data (sig-ASE)
        results.append(['Noise statistics analytical (Sig-ASE)', '', '', '', True])
        results.append(['Sig-ASE PSD (linear)', sig_ase_psd_measured, 'A^2/Hz', ' ', False])
        results.append(['Sig-ASE PSD (log)', sig_ase_psd_measured_dbm, 'dBm/Hz', ' ', False])
        results.append(['Sig-ASE noise current', sig_ase_current_measured*1e9, 'nA', ' ', False])
                                
        # Noise data (sig-ASE)
        results.append(['Noise statistics analytical (ASE-ASE)', '', '', '', True])
        results.append(['ASE-ASE PSD (linear)', ase_ase_psd_measured, 'A^2/Hz', ' ', False])
        results.append(['ASE-ASE PSD (log)', ase_ase_psd_measured_dbm, 'dBm/Hz', ' ', False])
        results.append(['ASE-ASE noise current', ase_ase_current_measured*1e9, 'nA', ' ', False])

    """ Receiver performance metrics-----------------------------------------------------------"""
    results.append(['Performance metrics', '', '', '', True])
    ber_estimate = 0.5*special.erfc(q_measured/np.sqrt(2))
    results.append(['Extinction ratio (P1/P0 - linear)' ,ext_ratio_linear, ' ', ' ', False, '0.3f'])
    results.append(['Extinction ratio (P1/P0)', ext_ratio_rcvr_db, 'dB', ' ', False, '0.2f'])
    results.append(['Extinction ratio (P0/P1 - linear)' , r_ext*100, '%', ' ', False, '0.2f'])
    #penalty = 10*np.log10((1+r_ext)/((1-r_ext)))
    #penalty = 10*np.log10((ext_ratio_linear+1)/((ext_ratio_linear-1)))
    #results.append(['Penalty', penalty, 'dB', ' ', False, '0.2f'])
    # Noise current (total)
    results.append(['Total noise current', i_noise_measured*1e9, 'nA', ' ', False])
    # Q/BER target
    results.append(['Q (target)', q_target, ' ', ' ', False, '0.2f'])
    ber_target = 0.5*special.erfc(q_target/np.sqrt(2)) #Ref 1, Eq. 4.56
    results.append(['BER (target)', ber_target, ' ', ' ', False])
    # Q measured
    results.append(['Q (measured)', q_measured, ' ', ' ', False, '0.2f'])
    # OSNR
    #results.append(['OSNR linear (avg sig pwr)', osnr_linear, ' ', ' ', False, '0.2f'])
    results.append(['OSNR (avg sig pwr)', osnr, 'dB', ' ', False, '0.2f'])
    results.append( ['Q (OSNR) - ideal ER, ASE only', q_osnr, ' ', ' ', False, '0.2f'])
    results.append( ['OSNR target - ideal ER, ASE only', osnr_target, 'dB', ' ', False, '0.2f'])
    # SNR
    if i_noise_calculated == 0:
        snr = 'NA'
        snr_db = 'NA'
    else:
        snr = np.square(i_signal_mean)/np.square(i_noise_calculated)
        snr_db =  10*np.log10(snr)
    #results.append(['SNR ', snr, ' ', ' ', False, '0.3f'])
    results.append(['SNR (dB)', snr_db, 'dB', ' ', False, '0.3f'])
    # Sensitivity (optical)
    #results.append(['Optical receiver sensitivity - th/shot', pwr_sensitivity, 'W', ' ', False])
    results.append(['Optical receiver sensitivity - th/shot', pwr_sensitivity_dbm, 'dBm', ' ', False, '0.2f'])
    #results.append(['Optical receiver sensitivity - th/shot', pwr_sensitivity, 'W', ' ', False])
    results.append(['Optical receiver sensitivity - th/shot/ER', pwr_sensitivity_ex_dbm, 'dBm', ' ', False, '0.2f'])
    
    # Send data to project folder (only if project file has been created)----------------------------
    if os.path.isfile(path) and enable_data_export == 2:
        if iteration == 1:
            setattr(proj, data_att_1, [])
            getattr(proj, data_att_1).append(rcv_pwr_dbm)
        else:
            getattr(proj, data_att_1).append(rcv_pwr_dbm)

    """Data panel output-------------------------------------------------------------------------------------"""
    c_analytical = 'blue'
    config.data_tables[data_panel_id] = []
    data_list = []
    data_list.append(['Iteration #', iteration, '0.0f', ' ', ' ', c_analytical])
    data_list.append(['Responsivity', r_mean, '0.2f', 'A/W', ' ', c_analytical])
    #data_list.append(['Target Q for link', q_target, '0.1f', ' '])
    #data_list.append(['Target BER for link', ber_target, '0.3E', ' '])
    #data_list.append(['Q measured (noise)', q_measured, '0.2f', ' '])
    data_list.append(['Optical pwr received (avg)',  rcv_pwr_dbm, '0.2f', 'dBm'])
    data_list.append(['Extinction ratio (linear)', ext_ratio_linear, '0.3f', ' '])
    data_list.append(['Extinction ratio (ER)', ext_ratio_rcvr_db, '0.2f', 'dB'])
    #data_list.append(['Receiver sensitivity (noise)', pwr_sensitivity_dbm, '0.2f', 'dBm'])
    #data_list.append(['ER power penalty', pwr_penalty_ext_dB, '0.2f', 'dB'])
    #data_list.append(['Receiver sensitivity (noise/ER)', pwr_sensitivity_ex_dbm, '0.2f', 'dBm'])
    config.data_tables[data_panel_id].extend(data_list)
    
    '''==RETURN (Output Signals, Parameters, Results)==================================''' 
    return ([[2, signal_type, 0, fs, time_array, i_signal, i_noise]],
            pin_apd_parameters, results)
            
def calculate_total_opt_pwr(input_field):
    return np.sum(np.abs(input_field)*np.abs(input_field))
    
def calculate_avg_opt_pwr(input_field):
    return np.mean(np.abs(input_field)*np.abs(input_field))
    
def rect_profile(frq, ctr_freq, bw):
    tr_fcn_filter = np.full(np.size(frq), 0 + 1j*0, dtype=complex)
    for i in range(0, np.size(frq)):
        if frq[i] >= ctr_freq - (bw/2) and frq[i] <= ctr_freq + (bw/2):
            tr_fcn_filter[i] = 1 + 1j*0
    return tr_fcn_filter
    
# Future feature
# Source: https://www.edmundoptics.com.sg/f/ingaas-photodiodes/12621/, Technical Images tab
# Typical Spectral Responsivity
'''800, 0.1
900, 0.25
1000, 0.56
1100, 0.68
1200, 0.78
1300, 0.87
1400, 0.915
1450, 0.93
1500, 0.95
1550, 0.96
1600, 0.93
1700, 0.4
1800, 0.0'''
