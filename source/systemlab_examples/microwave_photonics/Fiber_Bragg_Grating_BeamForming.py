"""
Fiber Bragg Grating (Bi-directional)
Version 1.0 (19.12.r1 11 Sep 2019)

References:
1) Fiber Bragg Grating Modeling, Yue Qiu & Yunlong Sheng; Center for Optics, Photonics and Lasers, 
Laval University - http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.492.5371&rep=rep1&type=pdf
(accessed 11-Sep-2019)
2) Bettini, Paolo et al. “Development and experimental validation of a numerical tool for structural health
and usage monitoring systems based on chirped grating sensors.” Sensors (Basel, Switzerland) 
vol. 15,1 1321-41. 12 Jan. 2015 - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4327079/
(accessed 10-Sep-2019)
3) Tosi, Daniele. “Review of Chirped Fiber Bragg Grating (CFBG) Fiber-Optic Sensors and 
Their Applications.” Sensors (Basel, Switzerland) vol. 18,7 2147. 4 Jul. 2018
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6068677/ (accessed 1-Oct-2019)
4) G. Palumbo, D. Tosi, A. Iadicicco and S. Campopiano, "Analysis and Design of Chirped Fiber Bragg
Grating for Temperature Sensing for Possible Biomedical Applications," in IEEE Photonics Journal, 
vol. 10, no. 3, pp. 1-15, June 2018
https://ieeexplore.ieee.org/document/8345713 (accessed 1-Oct-2019)
5) Ashry, Islam, Ali Elrashidi, Amr M. Mahros, Mohammed J. Alhaddad and Khaled M. Elleithy. 
“Investigating the performance of apodized Fiber Bragg gratings for sensing applications.” 
Proceedings of the 2014 Zone 1 Conference of the American Society for Engineering Education (2014): 1-5.
Source: http://www.asee.org/documents/zones/zone1/2014/Professional/PDFs/41.pdf (accessed 3-Dec-2019)
6) Wikipedia contributors, "Window function," Wikipedia, The Free Encyclopedia, 
https://en.wikipedia.org/w/index.php?title=Window_function&oldid=928906024 (accessed December 3, 2019). 
7) Abas AF, Aladadi YT, Alresheedi MT (2017) Euclidian Distance Method for Optimizing Linearly 
Chirped Fiber Bragg Grating Apodization Profile. Res J Opt Photonics 1:1
https://www.scitechnol.com/peer-review/euclidian-distance-method-for-optimizing-linearly-chirped-
fiber-bragg-grating-apodization-profile-tTSH.php?article_id=7017 (accessed 3-Dec-2019)
"""

import numpy as np
import config
from scipy import constants

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Fiber Bragg Grating'
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
        
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    
    '''==PARAMETERS========================================================='''
    # Load parameters from FB parameters table (format: Parameter name(0), Value(1), Units(2), Notes(3))
    # Main design parameters
    bragg_wave = float(parameters_input[1][1])*1e-9 #Design wavelength for grating (nm) - converted to m
    n_eff =  float(parameters_input[2][1]) # Effective refractive index of grating
    n_mod = float(parameters_input[3][1])  # Background modulation index
    L = float(parameters_input[4][1])*1e-3 #Grating length (mm) - converted to m
    N = int(parameters_input[5][1]) #Number of sections for transfer matrix method
    apod = str(parameters_input[6][1]) #Apodization profile
    # Chirp setting
    chirp_coeff = float(parameters_input[8][1]) # nm/mm
    # Graphs 
    display_graphs = int(parameters_input[10][1]) 
    pts = int(parameters_input[11][1])
    spacing =  float(parameters_input[12][1])*1e-9 #Convert from nm to m
    start_wave = float(parameters_input[13][1])*1e-9 #Start wavelenght for graphing (nm) - converted to m
    log_scale = int(parameters_input[14][1]) # Display graph results in log scale
    
    #Constants
    pi = constants.pi
    c = constants.c
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]
    psd_array = input_signal_data[0][4]
    opt_channels = input_signal_data[0][5] #Optical channel list
    # Extract signal and noise field envelopes for each optical channel
    channels = len(opt_channels)
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2:
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else:
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex)
    #Load wavelength channels
    for ch in range(0, channels): 
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector[ch] = opt_channels[ch][2]
        opt_field_rcv[ch] = opt_channels[ch][3]
        noise_field_rcv[ch] = opt_channels[ch][4]
    
    '''==CALCULATIONS======================================================='''
    #Prepare transfer matrix
    dz = L/N #units: m
    r = np.full([channels, n], 0 + 1j*0, dtype=complex)
    t = np.full([channels, n], 0 + 1j*0, dtype=complex)
    grating_strength = np.empty(channels)
    wave = np.empty([channels, n])
    
    # Setup apodization profile
    profile_z = set_apodization_profile(apod, dz, N, L)
    
    # Prepare freq array
    T = n/fs
    k = np.arange(n)
    frq = k/T # Positive/negative freq (double sided)
    
    # Initialize output field arrays for all optical channels
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_trans = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
        opt_field_ref = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
    else: # Polarization format: Exy
        opt_field_trans = np.full([channels, n], 0 + 1j*0, dtype=complex)
        opt_field_ref = np.full([channels, n], 0 + 1j*0, dtype=complex)
    
    #Loop over each optical channel
    for ch in range(0, channels):
        if config.sim_status_win_enabled == True:
            config.sim_status_win.textEdit.append('Running coupled mode transmission calculation: Ch ' 
                                                                    + str(wave_freq[ch]))
            config.app.processEvents()
            
        # Apply FFT (time -> freq domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_trans_x = np.fft.fft(opt_field_rcv[ch, 0])
            Y_trans_x = np.fft.fftshift(Y_trans_x)
            Y_trans_y = np.fft.fft(opt_field_rcv[ch, 1])
            Y_trans_y = np.fft.fftshift(Y_trans_y)
            Y_ref_x = np.fft.fft(opt_field_rcv[ch, 0])
            Y_ref_x = np.fft.fftshift(Y_ref_x)
            Y_ref_y = np.fft.fft(opt_field_rcv[ch, 1])
            Y_ref_y = np.fft.fftshift(Y_ref_y)
        else:
            Y_trans = np.fft.fft(opt_field_rcv[ch])
            Y_trans = np.fft.fftshift(Y_trans)
            Y_ref = np.fft.fft(opt_field_rcv[ch])
            Y_ref = np.fft.fftshift(Y_ref)
        
        #Loop over each frequency point of the channel envelope
        for i in range(0, n):
            #Provide update on calculation status
            display_cmt_progress(i, n)
            # Setup frequency array (for envelope)
            frq = frq - frq[int(round(n/2))] + wave_freq[ch]
            wave[ch] = c/frq
            # Grating strength calculation (for results)
            ac_cross_c = (pi/wave[ch, int(round(n/2))])*n_mod
            grating_strength[ch] = ac_cross_c*L
            
            # Initialize transfer function matrices
            T = np.full([2, 2], 0 + 1j*0, dtype=complex)
            T_section = np.full([2, 2], 0 + 1j*0, dtype=complex)
            
            #CMT model--------------------------------------------------------------------------------------------
            for m in range (N-1, -1, -1): #T = T(M)*T(M-1)*...*T(2)*T(1)
                bragg_wave_chirp = bragg_wave + (chirp_coeff*1e-6)*m*(L/N) #Eq 5 (Ref 3) Lg = L/N
                if m == N-1:
                    design_wave_chirp = bragg_wave_chirp
                ac_cross_c = (pi/wave[ch, i])*n_mod*profile_z[m] #(pi/lambda)*mod_index*profile(z) 
                detuning = 2*pi*n_eff*( (1/wave[ch, i]) - (1/(bragg_wave_chirp)) )
                dc_self_c = detuning + ((2*pi/wave[ch, i])*n_mod*profile_z[m])
            
                # Calculate gamma
                if ( (ac_cross_c*ac_cross_c) > (dc_self_c*dc_self_c) ):
                    gamma = np.sqrt( (ac_cross_c*ac_cross_c) - (dc_self_c*dc_self_c) )
                else:
                    gamma = 1j*np.sqrt( (dc_self_c*dc_self_c) - (ac_cross_c*ac_cross_c) )
            
                # Calculate transfer matrix element values (for m-th section)
                T_section[0,0] = np.cosh(gamma*dz)  - 1j*(dc_self_c/gamma)*np.sinh(gamma*dz) #T11
                T_section[0,1] = -1j*(ac_cross_c/gamma)*np.sinh(gamma*dz) #T12
                T_section[1,0] = 1j*(ac_cross_c/gamma)*np.sinh(gamma*dz) #T21
                T_section[1,1] = np.cosh(gamma*dz) +1j*(dc_self_c/gamma)*np.sinh(gamma*dz) #T22
            
                # Matrix multiplication (NumPy matmul)
                if m == N-1:
                    T = T_section
                else:
                    T = np.matmul(T, T_section) 
            #--------------------------------------------------------------------------------------------------------
            # Calculate reflection and transmission coefficients (amplitude)
            r[ch, i] = -T[1,0]/T[0,0] #T21/T11
            t[ch, i] = 1/T[0,0] #1/T11
            
            if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
                Y_trans_x[i] = Y_trans_x[i]*t[ch, i]
                Y_trans_y[i] = Y_trans_y[i]*t[ch, i]
                Y_ref_x[i] = Y_ref_x[i]*r[ch, i]
                Y_ref_y[i] = Y_ref_y[i]*r[ch, i]
            else:
                Y_trans[i] = Y_trans[i]*t[ch, i]
                Y_ref[i] = Y_ref[i]*r[ch, i]
            
           #opt_field_trans[ch, i] = t[ch, i]*opt_field_rcv[ch, i] 
           #opt_field_ref[ch, i] = r[ch, i]*opt_field_rcv[ch, i] 
            
            #r[ch] = -T[1,0]/T[0,0] #T21/T11
            #t[ch] = 1/T[0,0] #1/T11
        # Apply FFT (freq -> time domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_trans_x = np.fft.fftshift(Y_trans_x)
            opt_field_trans[ch, 0] = np.fft.ifft(Y_trans_x)
            Y_trans_y = np.fft.fftshift(Y_trans_y)
            opt_field_trans[ch, 1] = np.fft.ifft(Y_trans_y)
            Y_ref_x = np.fft.fftshift(Y_ref_x)
            opt_field_ref[ch, 0] = np.fft.ifft(Y_ref_x)
            Y_ref_y = np.fft.fftshift(Y_ref_y)
            opt_field_ref[ch, 1] = np.fft.ifft(Y_ref_y)
        else:
            Y_trans = np.fft.fftshift(Y_trans)
            opt_field_trans[ch] = np.fft.ifft(Y_trans)
            Y_ref = np.fft.fftshift(Y_ref)
            opt_field_ref[ch] = np.fft.ifft(Y_ref)
        
    if display_graphs == 2:
        if config.sim_status_win_enabled == True:
            config.sim_status_win.textEdit.append('Running coupled mode transmission calculation for graphing')
            config.app.processEvents()
        #Create transmissivity and reflectivity curves
        r_graph =np.full(pts, 0 + 1j*0, dtype=complex) 
        t_graph =np.full(pts, 0 + 1j*0, dtype=complex) 
        wave_graph = np.empty(pts)
        ref_graph = np.empty(pts)
        trans_graph = np.empty(pts)
        for i in range(0, pts):
            wave_graph[i] = start_wave + (i*spacing)
            T = np.full([2, 2], 0 + 1j*0, dtype=complex)
            T_section = np.full([2, 2], 0 + 1j*0, dtype=complex)
            
            #CMT model--------------------------------------------------------------------------------------------
            for m in range (N-1, -1, -1): #T = T(M)*T(M-1)*...*T(2)*T(1)
                bragg_wave_chirp = bragg_wave + (chirp_coeff*1e-6)*m*(L/N)
                detuning = 2*pi*n_eff*( (1/wave_graph[i]) - (1/(bragg_wave_chirp)) )
                dc_self_c = detuning + ((2*pi/wave_graph[i])*n_mod*profile_z[m]) 
                ac_cross_c = (pi/wave_graph[i])*n_mod*profile_z[m] #(pi/lambda)*mod_index*profile(z)
                
                # Calculate gamma
                if ( (ac_cross_c*ac_cross_c) > (dc_self_c*dc_self_c) ):
                    gamma = np.sqrt( (ac_cross_c*ac_cross_c) - (dc_self_c*dc_self_c) )
                else:
                    gamma = 1j*np.sqrt( (dc_self_c*dc_self_c) - (ac_cross_c*ac_cross_c) )
                    
                # Calculate transfer matrix element values (for m-th section)
                T_section[0,0] = np.cosh(gamma*dz)  - 1j*(dc_self_c/gamma)*np.sinh(gamma*dz) #T11
                T_section[0,1] = -1j*(ac_cross_c/gamma)*np.sinh(gamma*dz) #T12
                T_section[1,0] = 1j*(ac_cross_c/gamma)*np.sinh(gamma*dz) #T21
                T_section[1,1] = np.cosh(gamma*dz) +1j*(dc_self_c/gamma)*np.sinh(gamma*dz) #T22
                
                # Matrix multiplication (numpy matmul)
                if m == N-1:
                    T = T_section
                else:
                    T = np.matmul(T, T_section)
            
            # Calculate transmission & reflection coefficients
            r_graph[i] = -T[1,0]/T[1,1] #T21/T11
            t_graph[i] = 1/T[0,0] #1/T11
            
            # Add data points to graph arrays
            wave_graph[i] = wave_graph[i]*1e9 #Convert to nm
            ref_graph[i] = np.abs(r_graph[i])*np.abs(r_graph[i])
            trans_graph[i] = np.abs(t_graph[i])*np.abs(t_graph[i])
            z_pos = np.linspace(0, L, N)
            index_profile = profile_z*n_mod
            
        #Create an FBG graphing object (with data) and display results
        config.fbg_graph = config.view.FBGAnalyzer(wave_graph, 
                                                    ref_graph, trans_graph, log_scale, 
                                                    z_pos, index_profile)
        config.fbg_graph.show()
    
    #Calculate transmitted and reflected fields
    '''for ch in range(0, channels):
        #opt_field_trans[ch, :] = t[ch, :]*opt_field_rcv[ch, :] 
        opt_field_trans[ch, :] = np.matmul(t[ch, :], opt_field_rcv[ch, :])
        opt_field_ref[ch, :] = r[ch, :]*opt_field_rcv[ch, :] '''

    '''==OUTPUT PARAMETERS LIST============================================='''
    fbg_parameters = []
    fbg_parameters = parameters_input
  
    '''==RESULTS========================================================'''
    fbg_results = []
    design_wave_chirp_start_result = ['Design wavelength - start', bragg_wave*1e9, 'nm', ' ', False, '0.3E']
    design_wave_chirp_end_result = ['Design wavelength - end (linear chirp)', design_wave_chirp*1e9, 'nm', ' ', False, '0.3E']
    fbg_results = [design_wave_chirp_start_result, design_wave_chirp_end_result]
    for ch in range(0, channels):
        strength_result = ['Grating strength (' + str(format(wave[ch, int(round(n/2))]*1e9, '0.3f')) + ' nm)', 
                                    grating_strength[ch], '', ' ', False, '0.2f']
        fbg_results.append(strength_result)
        
    #Send update to data box (fbg_1)
    config.data_tables['fbg_1'] = []
    data_1 = ['Design wavelength - start (nm)',  bragg_wave*1e9, '4.2f', ' ']
    data_2 = ['Design wavelength - end (linear chirp) (nm)', design_wave_chirp*1e9, '4.2f', ' ']
    data_list = [data_1, data_2]
    config.data_tables['fbg_1'].extend(data_list)

    '''==RETURN (Output Signals, Parameters, Results)================================='''   
    optical_channels_tx = []
    optical_channels_ref = []
    for ch in range(0, channels):
        opt_ch_tx = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], 
                            opt_field_trans[ch], noise_field_rcv[ch]]
        optical_channels_tx.append(opt_ch_tx)
        opt_ch_ref = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], 
                            opt_field_ref[ch], noise_field_rcv[ch]]
        optical_channels_ref.append(opt_ch_ref)

    return ([[2, signal_type, fs, time_array, psd_array, optical_channels_ref],
                   [3, signal_type, fs, time_array, psd_array, optical_channels_tx]], fbg_parameters, fbg_results)
                   
def set_apodization_profile(profile, dz, N, L):
    profile_z = np.full(N, 1.0) #Uniform profile
    if profile == 'Sine': # Ref 5, Eq 7
        for m in range(0, N):
            z = dz*m
            profile_z[m] *= np.sin(np.pi*z/L) 
    elif profile == 'Power-of-sine': # Ref 5, Eq 7
        alpha = 2 #When set to 2, this is raised-cosine/Hann window
        for m in range(0, N):
            z = dz*m
            profile_z[m] *= np.power(np.sin(np.pi*z/L), alpha)
    elif profile == 'Hamming': # Ref 5, Eq 8
        h = 0.9
        for m in range(0, N):
            z = dz*m
            x = 2*np.pi*(z - 0.5*L)/L     
            profile_z[m] *= (1 + h*np.cos(x))/(1 + h)
    elif profile == 'Sinc': # Ref 5, Eq 6
        for m in range(0, N):
            z = dz*m
            x = 2*np.pi*(z - 0.5*L)/L
            if np.abs(x) <= 0.000001: #Limit function when approaching x = 0
                profile_z[m] *= 1
            else:
                profile_z[m] *= np.sin(x)/x   
    elif profile == 'Gaussian': # Ref 5, Eq 7
        alpha = 1
        for m in range(0, N):
            z = dz*m
            x = (z - 0.5*L)/L
            profile_z[m] *= np.exp(-alpha*(np.power(x, 2)))
    elif profile == 'Tanh': # Ref 5/Eq 9; Ref 7/Eq 1
        alpha = 3
        beta = 1
        for m in range(0, N):
            z = dz*m
            if z <= L/2:
                profile_z[m] *= np.power(np.tanh(2*alpha*z/L)/np.tanh(alpha), beta)
            else:
                profile_z[m] *= np.tanh(2*alpha*(L-z)/L)/np.tanh(alpha)
    return profile_z

def display_cmt_progress(i, n):       
    if i == int(round(n/4)):
        config.sim_status_win.textEdit.append('25% complete')
    if i == int(round(n/2)):
        config.sim_status_win.textEdit.append('50% complete')
    if i == int(round(n*3/4)):
        config.sim_status_win.textEdit.append('75% complete')
    if i == n - 1:
        config.sim_status_win.textEdit.append('100% complete')
    config.app.processEvents()

