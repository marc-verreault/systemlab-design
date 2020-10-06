"""
TRANSIMPEDANCE/LIMITING AMPLIFIER
Version 1.0 (20.01.r3 26-Jun-20)
Associated functional block: syslab_fb_library/TIA-LA

Performs the functions of Transimpedance amplification (current to voltage conversion) 
and limiter (sets output voltage to min/max rails for decision/logic circuit)

REF 1: "Accurately Estimating Optical Receiver Sensitivity", Application Note HFAN-3.0.0
(Rev. 1; 04/08), Maxim Integrated, www.maximintegrated.com (accessed 22 Jun 20)
REF 2: "Optical receiver performance evaluation", Application Note 1938 HFAN-03.0.2, 
Maxim Integrated, www.maximintegrated.com (accessed 22 Jun 20)
REF 3: Behzad Razavi. 2012. Design of Integrated Circuits for Optical
Communications (2nd. ed.). McGraw-Hill, Inc., USA.
REF 4: Group Delay, Christopher J. Struck, http://www.cjs-labs.com/sitebuildercontent/
sitebuilderfiles/GroupDelay.pdf (accessed Julu 8, 2020)
REF 5: Jitter Separation in High Speed Digital Design, Gustaaf Sutorius, Agilent Technologies
Source: https://www.keysight.com/upload/cmc_upload/All/Download2.pdf (accessed 10-Jul-20)
"""
# import project_config as proj
import os
import numpy as np
import config
import copy
from scipy import signal, special

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS===================================================
    '''
    module_name = settings['fb_name']
    n = settings['num_samples'] #Total samples for simulation
    n = int(round(n))    
    time = settings['time_window'] #Time window for simulation (sec)
    fs = settings['sampling_rate'] #Sample rate (default - Hz)
    f_sym = settings['symbol_rate'] #Symbol rate (default - Hz)
    t_step = settings['sampling_period'] #Sample period (Hz)
    iteration = settings['current_iteration'] #Current iteration loop for simulation
    i_total = settings['iterations'] #Total iterations for simulation (default - 1)
    
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
                                          
    '''==INPUT PARAMETERS================================================
    '''
    # TIA settings
    z_tia = float(parameters_input[1][1])*1e3 # kohm -> ohm
    tia_noise_model = str(parameters_input[2][1])
    i_noise_referred = float(parameters_input[3][1])*1e-6 # uA -> A
    enb = float(parameters_input[4][1])*1e9 # GHz -> Hz
    i_noise_density = float(parameters_input[5][1])*1e-12 # pA/sqrt(Hz) -> A/sqrt(Hz)
    # TIA (filter model)
    filter_type = str(parameters_input[7][1])
    freq_cut_off = float(parameters_input[8][1])*1e9 # GHz -> Hz
    Q = float(parameters_input[9][1])
    include_noise_array = int(parameters_input[10][1]) # MV 20.01.r3 26-Aug-20
    # TIA analysis graphs
    freq_resp_curves = int(parameters_input[12][1])
    dist_plot = int(parameters_input[13][1])
    n_bins = int(parameters_input[14][1])
    # LA settings
    enable_la = int(parameters_input[16][1])
    output_v_swing = float(parameters_input[17][1])*1e-3 # mV -> V
    la_noise_model = str(parameters_input[18][1])
    v_sens_la = float(parameters_input[19][1])*1e-3 # mV -> V
    enb_la = float(parameters_input[20][1])*1e9 # GHz -> Hz
    v_noise_density = float(parameters_input[21][1])*1e-9 # nV/sqrt(Hz) -> V/sqrt(Hz)
    gain_la = float(parameters_input[22][1]) # dB
    trans_points = str(parameters_input[23][1])
    rise_fall_time = float(parameters_input[24][1])*1e-12 # ps -> s
    jitter_det = float(parameters_input[25][1])*1e-12 # ps -> s
    jitter_rdm = float(parameters_input[26][1])*1e-12 # ps -> s
    # Add noise array to signal array
    add_noise_to_signal = int(parameters_input[28][1])
    # Receiver sensitivity calculations
    q_target = float(parameters_input[30][1])
    r = float(parameters_input[31][1]) # Upstream PIN/APD responsivity
    r_e = float(parameters_input[32][1])
    isi_penalty = float(parameters_input[33][1]) # dB
    # Settings for results/data panels
    data_panel_id = str(parameters_input[35][1])
    
    '''==INPUT SIGNALS========================================
    '''
    # Electrical: portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), 
    # amplitude_array(5), noise_array(6)
    time_array = input_signal_data[0][4]
    sig_in = np.zeros(n)
    noise_in = np.zeros(n)
    sig_in = copy.deepcopy(input_signal_data[0][5])
    noise_in = copy.deepcopy(input_signal_data[0][6])
    
    '''==CALCULATIONS=========================================
    '''
    carrier = 0
    sig_type_out = 'Electrical'
    
    """Transimpedance calculations-------------------------------------------------------------
    """
    # Apply gain to signal (converts current to voltage)
    sig_array = sig_in*z_tia # V=IR
    noise_array = noise_in*z_tia # V=IR
    
    """TIA filtering-----------------------------------------------------------------------------"""
    if filter_type != 'Ideal (no filter)':
        # Convert freq cut-off units from Hz to rad/s
        w_0 = np.pi*2*freq_cut_off
        Y, frq = convert_freq_domain(sig_array, fs, n)
        N, frq = convert_freq_domain(noise_array, fs, n)
        if filter_type == 'Low-pass (n=1)':
            Y_trans = transfer_lowpass_1st_order(Y, frq, w_0, fs, n)
            N_trans = transfer_lowpass_1st_order(N, frq, w_0, fs, n)
        elif filter_type == 'Low-pass (n=2)':
            Y_trans = transfer_lowpass_2nd_order(Y, frq, w_0, Q, fs, n)  
            N_trans = transfer_lowpass_2nd_order(N, frq, w_0, Q, fs, n)  
        # Build freq response curve (if selected)
        if freq_resp_curves == 2:
            build_freq_response_curve(Y, Y_trans, frq, n, freq_cut_off, filter_type)
        # Convert back to time domain
        sig_array = np.fft.ifft(np.fft.ifftshift(Y_trans))
        if include_noise_array == 2: # MV 20.01.r3 26-Aug-20
            noise_array = np.fft.ifft(np.fft.ifftshift(N_trans))
    
    """Noise calculations (TIA)----------------------------------------------------------------"""
    tia_v_noise = np.zeros(n)
    if tia_noise_model != 'Disabled':
        # Calculate output noise voltage (based on input referred noise current/density)
        if tia_noise_model == 'Input noise density':
            i_noise_referred = i_noise_density*np.sqrt(enb)
        #output_noise_variance = np.square(i_noise_referred*z_tia)
        #v_noise_sigma = np.sqrt(output_noise_variance)
        #config.display_data('Voltage sigma (TIA): ', v_noise_sigma, 0, 0) 
        # Add noise to noise array
        tia_v_noise = np.random.normal(0, i_noise_referred*z_tia, n)
        noise_array += tia_v_noise
    else: # Input referred noise is not modeled
        i_noise_referred = 0
    
    """Calculate performance metrics--------------------------------------------------------"""
    # Calculate estimated BER for q target
    ber_target = 0.5*special.erfc(q_target/np.sqrt(2))
    # Current (noise) from PIN/APD
    i_noise_input = np.sqrt(np.var(noise_in))
    # Input referred noise current (TIA)
    i_noise_input_tia_la = i_noise_referred
    # Noise current total (TIA and PIN/APD)
    n_rms =  np.sqrt(np.var(noise_in) + np.square(i_noise_referred))
    
    # Calculate minimum OMA and sensitivity (based on q target)
    isi = 0
    if isi_penalty != 0:
        isi = 1 - np.power(10, -isi_penalty/10)
    #config.display_data('ISI (%): ', 100*isi, 0, 0) 
    min_i_pp = 2*q_target*n_rms/(1 - isi)
    oma_min = min_i_pp/r
    p_avg_min = 10*np.log10(1e3*(oma_min/2)*(r_e + 1)/(r_e - 1))
    
    # Signal statistics (post-TIA)
    sig_total = np.real(sig_array + noise_array)
    sig_avg = np.mean(sig_total)
    sig_P1 = sig_total[sig_total > sig_avg]
    sig_P0 = sig_total[sig_total < sig_avg]
    v1_mean = np.mean(sig_P1)
    v0_mean = np.mean(sig_P0)
    v1_sigma = np.std(sig_P1)
    v0_sigma = np.std(sig_P0)
    q_measured = (v1_mean - v0_mean)/(v1_sigma + v0_sigma)
    v_pp= v1_mean - v0_mean
    ber_estimate = 0.5*special.erfc(q_target/np.sqrt(2))
    
    # Distribution analysis
    if dist_plot == 2:
        title = 'Signal/Noise distribution (TIA output)'
        #sig_dist = np.real(sig_array) + np.real(noise_array)
        config.dist_graph['TIA'] = config.view.Distribution_Analysis(title, sig_total,
                                                                                      'Signal (V)', n_bins, 
                                                                                      None, v1_mean, v0_mean, 
                                                                                      v1_sigma, v0_sigma)
        config.dist_graph['TIA'].show()
        
    """LIMITING AMPLIFIER CALCULATIONS-----------------------------------------
    """
    n_la = 0
    gain_avg = 1
    v_ratio = np.ones(n)
    if enable_la == 2:
        """Noise calculations (LA)---------------------------------------------------------"""
        if la_noise_model == 'Disabled':
            v_sens_la = 0
        elif la_noise_model == 'Referred noise density':
            v_sens_la = v_noise_density*np.sqrt(enb_la)
        n_la = v_sens_la/(2*q_target)
        
        # Input referred noise (TIA + LA)
        i_noise_input_tia_la = (np.sqrt(np.square(i_noise_referred) 
                                          + np.square(n_la/z_tia)))
        v_noise = np.random.normal(0, i_noise_input_tia_la*z_tia, n)
        noise_array += v_noise - tia_v_noise
        
        # Add noise to sig_array
        sig_array += noise_array
        noise_array = np.zeros(n)
        
        """Perform DC offset and apply gain---------------------------------------"""
        # DC offset
        sig_avg = np.mean(sig_array)
        sig_array = sig_array - sig_avg
        # Calculate linear gain (small signal)
        gain_la_linear = np.power(10, gain_la/20)
        v_rail = output_v_swing/2
        # Calculate gain array
        for i in range(0, n):
            # Calculate ratio of input voltage to voltage swing (0.5*PtP)
            # signal_total = np.abs(noise_array[i]) + np.abs(sig_array[i])
            v_ratio[i] = v_rail/np.abs(sig_array[i])
            if v_ratio[i] > gain_la_linear: # Maximum linear gain available
                v_ratio[i] = gain_la_linear
        # Calculate average gain applied to all sampled signals
        gain_avg = np.mean(v_ratio)
        sig_array = sig_array*v_ratio
        
        '''http://www.ecircuitcenter.com/OpModels/Tanh_Stage/Tanh_Stage.htm
        for i in range(0, n):
            slope = 100
            k =  sig_array[i]/v_rail
            sig_array[i] = v_rail * np.tanh(k*slope)'''

        """Apply rise/fall time to signal-----------------------------------------------"""
        # REF: Wikipedia contributors, "Rise time," Wikipedia, The Free Encyclopedia, 
        # https://en.wikipedia.org/w/index.php?title=Rise_time&oldid=946919388
        # (accessed June 24, 2020).
        if rise_fall_time > 0:
            sig_array = apply_rise_fall_time(sig_array, trans_points, rise_fall_time, fs, n)
            
        """Apply jitter (random and deterministic)----------------------------------------------------"""
        # Based on Dual Dirac Assumption (Jitter_total = Jitter_deterministic + Jitter_random)
        # exp(-(signal - j_det/2)^2/2*j_rms^2) + exp(-(signal + j_det/2)^2/2*j_rms^2)
        # REF 5 (slide 21)
        samples_per_sym = int(round(fs/f_sym))
        n_symbols = int(round(n/samples_per_sym))
        if jitter_det > 0.0 or jitter_rdm > 0.0:
            for i in range(0, n_symbols-1):
                dirac = np.random.randint(2)
                if dirac == 0:
                    dirac = -1
                dirac_offset = float(dirac)*jitter_det/2 + np.random.normal(0, jitter_rdm)
                idx_1 = i*samples_per_sym
                idx_2 = (i+1)*samples_per_sym
                sig_array[idx_1:idx_2] = np.interp(time_array[idx_1:idx_2] + dirac_offset, 
                                                                    time_array[idx_1:idx_2], sig_array[idx_1:idx_2])
        
        """Calculate performance metrics-----------------------------------------------------------"""
        # Noise current total (TIA, LA and PIN/APD)
        n_rms = np.sqrt(np.var(noise_in) + np.square(i_noise_referred) 
                                + np.square(n_la/z_tia))
        # Calculate minimum OMA and sensitivity (based on q target)
        min_i_pp = 2*q_target*n_rms/(1 - isi)
        oma_min = min_i_pp/r
        p_avg_min = 10*np.log10(1e3*(oma_min/2)*(r_e + 1)/(r_e - 1))
        
        # Calculate voltage sigma for TIA/LA
        #output_noise_variance = np.square(i_noise_referred*z_tia) + np.square(n_la*gain_avg) 
        #v_noise_sigma = np.sqrt(output_noise_variance)
        #config.display_data('Voltage sigma (TIA+LA): ', v_noise_sigma, 0, 0)
        
        """Noise calculations (LA)-------------------------------------------------------------------"""
        # Apply LA voltage noise to output noise array (Note: average gain is used)
        #la_v_noise = np.random.normal(0, n_la, n)
        #tia_v_noise = np.random.normal(0, n_la*gain_la_linear, n)
        #noise_array += la_v_noise*gain_la_linear
        
        #output_noise_variance = np.square(n_rms*z_tia)
        #v_noise_sigma = np.sqrt(output_noise_variance)
        
        #la_v_noise = np.random.normal(0, v_noise_sigma, n)
        #noise_array += la_v_noise
    
    # Add noise to signal array? Applies to TIA only model
    if add_noise_to_signal == 2:
        sig_array += noise_array
        noise_array = np.zeros(n)
            
    # Send data to project folder (only if project file has been created)
    if os.path.isfile(path):
        if iteration == 1:
            proj.q_measured = []
            proj.q_measured.append(q_measured)
            proj.ber_estimate = []
            proj.ber_estimate.append(ber_estimate)
        else:
            proj.q_measured.append(q_measured)
            proj.ber_estimate.append(ber_estimate)
    
    '''==OUTPUT PARAMETERS LIST=======================================================
    '''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
  
    '''==RESULTS===================================================================
    '''
    results = []
    results.append(['TIA/LA Metrics', ' ', ' ', ' ', True])
    results.append(['Noise current from photodetector', i_noise_input*1e6, 'uA', ' ', False, '0.3f'])
    results.append(['Input referred noise current (TIA)', i_noise_referred*1e6, 'uA', ' ', False, '0.3f'])
    results.append(['Input referred noise voltage (LA)', n_la*1e3, 'mV', ' ', False, '0.3f'])
    #results.append(['Input referred noise (TIA/LA)', i_noise_input_tia_la*1e6, 'uA', ' ', False, '0.3f'])
    results.append(['Total noise current at TIA input', n_rms*1e6, 'uA', ' ', False, '0.3f'])
    results.append(['Input voltage swing at LA', v_pp*1e3, 'mV', ' ', False, '0.2f'])
    results.append(['Transimpendance gain (TIA)', z_tia*1e-3, 'k'+'\u2126', ' ', False, '0.2f'])
    results.append(['Average gain (LA)', gain_avg, ' ', ' ', False, '0.2f'])
    results.append(['OMA (Q target)', oma_min*1e6, 'uW', ' ', False, '0.3f'])
    results.append(['Receiver sensitivity (Q target)', p_avg_min, 'dBm', ' ', False, '0.2f'])
    results.append(['Receiver Q statistics', ' ', ' ', ' ', True])
    results.append(['V1 mean (all samples)', v1_mean, ' ', ' ', False, '0.3E'])
    results.append(['V0 mean (all samples)', v0_mean, ' ', ' ', False, '0.3E'])
    results.append(['V1 std dev (all samples)', v1_sigma, ' ', ' ', False, '0.3E'])
    results.append(['V0 std dev (all samples)', v0_sigma, ' ', ' ', False, '0.3E'])
    results.append(['Q measured (all samples)', q_measured, ' ', ' ', False, '0.2f'])
    
    """Data panel output-------------------------------------------------------------------------------------"""
    c_analytical = 'blue'
    config.data_tables[data_panel_id] = []
    data_list = []
    data_list.append(['Iteration #', iteration, '0.0f', ' ', ' ', c_analytical])
    data_list.append(['--------------------------TIA/LA Metrics----------------------------', 
                               ' ', ' ', ' ', '#5e5e5e'])
    data_list.append(['Noise current from photodetector', i_noise_input*1e6, '0.3f', 'uA'])
    data_list.append(['Input referred noise current (TIA)', i_noise_referred*1e6, '0.3f', 'uA'])
    data_list.append(['Input referred noise voltage (LA)', n_la*1e3, '0.3f', 'mV'])
    #data_list.append(['Input referred noise (TIA/LA)', i_noise_input_tia_la*1e6, '0.3f', 'uA'])
    data_list.append(['Total noise current at TIA input', n_rms*1e6, '0.3f', 'uA'])
    data_list.append(['Input voltage swing at LA', v_pp*1e3, '0.2f', 'mV'])
    data_list.append(['Transimpendance gain (TIA)', z_tia*1e-3, '0.2f', 'k'+'\u2126'])
    data_list.append(['Average gain (LA)', gain_avg, '0.2f', ' '])
    
    data_list.append(['--------------------------Link Analysis ----------------------------',
                               ' ', ' ', ' ', '#5e5e5e'])
    data_list.append(['Q (measured)', q_measured, '0.2f', ' '])
    data_list.append(['Target Q for link', q_target, '0.2f', ' ', ' ', c_analytical])
    data_list.append(['Target BER for link', ber_target, '0.3E', ' ', ' ', c_analytical])
    data_list.append(['OMA (Q target)', oma_min*1e6, '0.3f', 'uW', ' ', c_analytical])
    data_list.append(['Receiver sensitivity (Q target)', p_avg_min, '0.2f', 'dBm', ' ', c_analytical])
    # Add data_list entries to data tables dictionary
    config.data_tables[data_panel_id].extend(data_list)
    
    '''==RETURN (Output Signals, Parameters, Results)==================================
    '''
    electrical_out = [2, sig_type_out, carrier, fs, time_array, sig_array, noise_array]
    return ([electrical_out], script_parameters, results)
    
def transfer_lowpass_1st_order(Y, frq, w_0, fs, n):
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = w_0 / (s + w_0)
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_2nd_order(Y, frq, w_0, Q, fs, n):   
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = (w_0*w_0) / ((s*s) + ((w_0/Q)*s) + (w_0*w_0))
        Y_trans[i] = Y[i] * H_w
    return Y_trans

def convert_freq_domain(sig, fs, n):
    T = n/fs
    k = np.arange(n)
    frq = k/T
    frq = frq - frq[int(round(n/2))]
    return np.fft.fftshift(np.fft.fft(sig)), frq
    
def apply_rise_fall_time(sig, trans_points, rise_fall_time, fs, n):
    if trans_points == '10%-90%':
        bw = 0.34/rise_fall_time # Based on t_r = 4/sigma*(inv_error_function(0.8))
        sigma = bw/0.0935
    else:
        bw = 0.22/rise_fall_time # Based on t_r = 4/sigma*(inv_error_function(0.6))
        sigma = bw/0.0935
    # Apply filtering
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    Y, frq = convert_freq_domain(sig, fs, n)
    bw = 0.35/rise_fall_time
    w_0 = np.pi*2*bw
    for i in range(0, n):
        w = frq[i]*2*np.pi
        Y_trans[i] = Y[i] * np.exp(-np.square(w/sigma))
    # Convert back to time domain and return
    return np.fft.ifft(np.fft.ifftshift(Y_trans))
    
def build_freq_response_curve(Y, Y_trans, frq, n, freq_cut_off, filter_type):
        mag = np.abs(Y_trans/Y)
        mag = 20*np.log10(mag)
        ph = np.rad2deg(np.unwrap(np.angle(Y_trans/Y)))
        # Calculate group delay
        # Negative derivative of phase (-d_ph/d_w) - Source: REF 4
        g_delay = np.zeros(n)
        for i in range (1, n-1):
            g_delay[i] = -1*( (ph[i+1] - ph[i-1])/(frq[i+1] - frq[i-1]) ) #Eq 4 (R 4)
        g_delay[0] = -1*( (ph[1] - ph[0])/(frq[1] - frq[0]) ) # Eq 6 (R 4)
        g_delay[-1] = -1*( (ph[-1] - ph[-2])/(frq[-1] - frq[-2]) ) # Eq 7 (R 4)
        g_delay = g_delay/360
        
        # Create instance of FilterAnalyzer class
        config.analog_filter_graph = config.view.FilterAnalyzer(frq, 
                                                                 mag, ph, g_delay, n, freq_cut_off,
                                                                 filter_type)
        config.analog_filter_graph.show()
