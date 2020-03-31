"""
SystemLab-Design Version 20.01.r1
Optical Fiber Linear
Version 1.0 (11 Sep 2019)

Models the linear impairments of loss and chromatic dispersion 
for a single mode fiber.

REFS
1) Shaham Sharifian, 'Chromatic dispersion compensation by signal predistortion:
linear and nonlinear filtering', Communications Systems Group, Department of Signals and Systems,
Chalmers University of Technology, Goteborg, Sweden, 2010
https://pdfs.semanticscholar.org/acd2/dc8fec1e2821f7baa02fd845a87779412bba.pdf
(accessed 16 Sep 2019)
2) Optical Communication Systems (OPT428) Govind P. Agrawal, Institute of Optics,
University of Rochester, Rochester, NY (2006) http://www2.optics.rochester.edu/users/gpa/opt428b.pdf
(accessed 26 Sep 2019)
3) Takashi Ito, Ondrej Slezak, Masahiro Yoshita, Hidefumi Akiyama, and Yohei Kobayashi,
"High-precision group-delay dispersion measurements of optical fibers via fingerprint-spectral 
wavelength-to-time mapping," Photon. Res. 4, 13-16 (2016) 
http://www.opticsjournal.net/ViewFull0.htm?aid=OJ160926000009u1w4z7
(accessed 27 Sep 2019)
"""

import numpy as np
import config
from scipy import constants

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Optical Fiber (Linear)'
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

    '''==PARAMETERS================================================'''
    # Load parameters from FB parameters table (Parameter name(0), Value(1), Units(2), Notes(3))
    # Primary parameters (header)
    length = float(parameters_input[1][1]) #Length of fiber (in km)
    alpha_db =  float(parameters_input[2][1]) # Loss coefficient (dB/km)
    #  Linear propagation (disp) parameters
    include_beta1 = int(parameters_input[4][1]) # Include beta 1?
    n_eff =  float(parameters_input[5][1]) # Effective group index of refraction
    include_beta2 = int(parameters_input[6][1]) # Include beta 2?
    disp = float(parameters_input[7][1])  # Dispersion parameter (ps/(km*nm))
    include_beta3 = int(parameters_input[8][1]) # Include beta 3?
    slope = float(parameters_input[9][1])  # Dispersion parameter (ps/(km*nm*nm))
    # Constants
    pi = constants.pi
    c = constants.c

    '''==INPUT SIGNALS=============================================='''
    # Load optical group data from input port
    signal_type = 'Optical'
    time_array = input_signal_data[0][3] # Sampled time array
    psd_array = input_signal_data[0][4] # Noise groups
    opt_channels = input_signal_data[0][5] #Optical channel list

    # Load frequency, jones vector, signal & noise field envelopes for each optical channel
    channels = len(opt_channels)
    wave_key = np.empty(channels)
    wave_freq = np.empty(channels)
    jones_vector = np.full([channels, 2], 0 + 1j*0, dtype=complex) 
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_rcv = np.full([channels, 2, n], 0 + 1j*0, dtype=complex) 
    else: # Polarization format: Exy
        opt_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_rcv = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    for ch in range(0, channels): #Load wavelength channels
        wave_key[ch] = opt_channels[ch][0]
        wave_freq[ch] = opt_channels[ch][1]
        jones_vector[ch] = opt_channels[ch][2]
        opt_field_rcv[ch] = opt_channels[ch][3]
        noise_field_rcv[ch] = opt_channels[ch][4]

    '''==CALCULATIONS=============================================='''
    # Calculate signal loss
    link_loss_db = alpha_db*length
    link_loss_linear = np.power(10, -link_loss_db/10)
    if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
        opt_field_out = np.full([channels, 2, n], 0 + 1j*0, dtype=complex)
    else: # Polarization format: Exy
        opt_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex) 
    noise_field_out = np.full([channels, n], 0 + 1j*0, dtype=complex)
    for ch in range(0, channels):
        opt_field_out[ch] = np.sqrt(link_loss_linear)*opt_field_rcv[ch]
        noise_field_out[ch] = np.sqrt(link_loss_linear)*noise_field_rcv[ch]

    # Calculate linear propagation parameters
    # Prepare freq array
    T = n/fs
    k = np.arange(n)
    frq = k/T # Positive/negative freq (double sided) 
    # Initialize wave/beta arrays
    beta_1 = 0
    wave = np.empty(channels)
    beta_2 = np.empty(channels)
    beta_3 = np.empty(channels)

    for ch in range(0, channels):
        frq = frq - frq[int(round(n/2))] + wave_freq[ch]
        # Apply FFT (time -> freq domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_x = np.fft.fft(opt_field_out[ch, 0])
            Y_x = np.fft.fftshift(Y_x)
            Y_y = np.fft.fft(opt_field_out[ch, 1])
            Y_y = np.fft.fftshift(Y_y)
        else:
            Y = np.fft.fft(opt_field_out[ch])
            Y = np.fft.fftshift(Y)
        Y_N = np.fft.fft(noise_field_out[ch])
        Y_N = np.fft.fftshift(Y_N)
        # Calculate betas----------------------------------------------------------------------------------
        # Freq domain transfer function: H(w) = exp(-j*beta(w)*length) 
        # beta(w) = beta_0 + beta_1(w-w0) + 1/2*beta_2(w-w0)^2 + 1/6*beta_3(w-w0)^3 + ...
        # Disp  = (-2*pi*c/lambda^2)*beta_2  (Ref 2, Slide 95)
        # Slope = (2*pi*c/lambda^2)^2*beta_3 (Ref 2, Slide 95)
        wave[ch] = c/wave_freq[ch] #m
        beta_2[ch] = 0
        beta_3[ch] = 0
        a = (wave[ch]*wave[ch])/(2*pi*c) 
        if include_beta1 == 2:
            beta_1 = n_eff/c
        if include_beta2 == 2:
            beta_2[ch] = -disp*a*1e-6 #s^2/m  ( beta2 =-D*(lambda^2/2*pi*c) )
        if include_beta3 == 2:
            beta_3[ch] = slope*a*a*1e3 #s^3/m ( beta3 = S*(lambda^2/2*pi*c)^2 )
            #Other equation (Ref 1/Eq 2.15: beta3 = (S - (4*pi*c/lambda^3)*beta2)*(lambda^2/2*pi*c)^2
        # Apply transfer function to field envelope of each channel
        for i in range(0, n):
            #H(w) = exp(-j*(beta_2*length*w^2)/2) where w = 2*pi*freq
            w = 2*pi*frq[i]
            wo = 2*pi*wave_freq[ch]
            w = w - wo
            # Apply linear dispersion transfer function
            if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
                Y_x[i] = Y_x[i] * np.exp( -1j*length*1e3*( (beta_1*w) + ((beta_2[ch]*w*w)/2)
                                            + ((beta_3[ch]*w*w*w)/6)) )
                Y_y[i] = Y_y[i] * np.exp( -1j*length*1e3*( (beta_1*w) + ((beta_2[ch]*w*w)/2)
                                            + ((beta_3[ch]*w*w*w)/6)) )
            else:
                Y[i] = Y[i] * np.exp( -1j*length*1e3*( (beta_1*w) + ((beta_2[ch]*w*w)/2)
                                            + ((beta_3[ch]*w*w*w)/6)) )
                                            
            Y_N[i] = Y_N[i] * np.exp( -1j*length*1e3*( (beta_1*w) + ((beta_2[ch]*w*w)/2)
                                            + ((beta_3[ch]*w*w*w)/6)) )
        # Apply FFT (freq -> time domain)
        if opt_channels[0][3].ndim == 2: # Polarization format: Ex-Ey
            Y_x = np.fft.fftshift(Y_x)
            opt_field_out[ch, 0] = np.fft.ifft(Y_x)
            Y_y = np.fft.fftshift(Y_y)
            opt_field_out[ch, 1] = np.fft.ifft(Y_y)
        else:
            Y = np.fft.fftshift(Y)
            opt_field_out[ch] = np.fft.ifft(Y)
        Y_N = np.fft.fftshift(Y_N)
        noise_field_out[ch] = np.fft.ifft(Y_N)
        
    '''==OUTPUT PARAMETERS LIST======================================='''
    opt_fiber_parameters = []
    opt_fiber_parameters = parameters_input
  
    '''==RESULTS==================================================='''
    opt_fiber_results = []
    beta_1_result = ['Beta 1', beta_1, 's/m', ' ', False, '0.3E']
    transit_time_result = ['Transit time', beta_1*length*1e3, 's', ' ', False, '0.3E']
    opt_fiber_results = [beta_1_result, transit_time_result]
    for ch in range(0, channels):
        beta_2_result = ['Beta 2 (' + str(format(wave[ch]*1e9, '0.3f')) + ' nm)', 
                                    beta_2[ch], 's^2/m', ' ', False, '0.3E']
        opt_fiber_results.append(beta_2_result)
        disp_2_result = ['Beta 2 x L (' + str(format(wave[ch]*1e9, '0.3f')) + ' nm)', 
                                    beta_2[ch]*length*1e3, 's^2', ' ', False, '0.3E']
        opt_fiber_results.append(disp_2_result)
        beta_3_result = ['Beta 3 (' + str(format(wave[ch]*1e9, '0.3f')) + ' nm)', 
                                    beta_3[ch], 's^3/m', ' ', False, '0.3E']
        opt_fiber_results.append(beta_3_result)
        disp_3_result = ['Beta 3 x L (' + str(format(wave[ch]*1e9, '0.3f')) + ' nm)', 
                                    beta_3[ch]*length*1e3, 's^3', ' ', False, '0.3E']
        opt_fiber_results.append(disp_3_result)

    '''==RETURN (Output Signals, Parameters, Results)========================================='''   
    optical_channels = []
    for ch in range(0, channels):
        opt_ch = [int(wave_key[ch]), wave_freq[ch], jones_vector[ch], opt_field_out[ch], noise_field_out[ch]]
        optical_channels.append(opt_ch)
    
    return ([[2, signal_type, fs, time_array, psd_array, optical_channels]], opt_fiber_parameters, opt_fiber_results)

