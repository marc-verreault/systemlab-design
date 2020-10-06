"""
SystemLab-Design Version 19.02/20.01.r3
Functional block script: Analog Filter
Version 1.0 (13-Mar-2019/21-Jun-20)

Refs:
1) Chapter 8, Analog Filters 
Source: Analog Devices - from Google search: 'analog filter frequency response'
https://www.analog.com/media/en/training-seminars/design-handbooks/
Basic-Linear-Design/Chapter8.pdf
Accessed: 22-Feb-2019
2) An Introduction to Analog Filters, Ed Ramsden (Jul 1, 2001)
https://www.sensorsmag.com/components/introduction-to-analog-filters
Accessed: 13-Mar-2019
3) Analog Filter Design, poster: Strether Smith (19 Dec 2017)
https://blog.mide.com/analog-filter-design
Accessed: 12-Mar-2019 
4) Analog Filter Design Demystified, Tutorial 1795
https://www.maximintegrated.com/en/app-notes/index.mvp/id/1795
Accessed: 11-Mar-2019
5) A Filter Primer, Tutorial 733
https://www.maximintegrated.com/en/app-notes/index.mvp/id/733
Accessed: 12-Mar-2019 
6) High-pass filter (Wikipedia contributors)
https://en.wikipedia.org/wiki/High-pass_filter
Accessed: 11-Mar-2019
7) Sources of Phase Shift (Lab 3: Operational Amplifiers and First-Order Circuits)
http://www.tedpavlic.com/teaching/osu/ece209/lab3_opamp_FO/lab3_opamp_FO_phase_shift.pdf
Accessed: 13-Mar-2019 (via Ref 6)
"""
import numpy as np
import config

#import systemlab_viewers as view
#import importlib
#custom_viewers_path = str('syslab_config_files.systemlab_viewers')
#view = importlib.import_module(custom_viewers_path)

def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Analog filter' 
    n = settings['num_samples']
    n = int(round(n))
    iteration = settings['current_iteration']
    time = settings['time_window']
    fs = settings['sampling_rate']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.status.setText('Running ' + module_name + 
                                          ' - Iteration #: ' + str(iteration))
    config.app.processEvents()
    
    '''==INPUT PARAMETERS==================================================='''
    #Parameters table
    filter_type = str(parameters_input[0][1])
    freq_resp_curves = int(parameters_input[1][1])
    freq_cut_off = float(parameters_input[3][1])
    Q = float(parameters_input[4][1])
    freq_zero = float(parameters_input[5][1])
    
    '''==INPUT SIGNALS====================================================================
    '''
    sig_type = 'Electrical'
    carrier = 0
    time = input_signal_data[0][4]
    signal = input_signal_data[0][5]
    # MV 20.01.r3 21-Jun-20
    # Noise array was not being retrieved from to input port. Now fixed.
    # Not required to update fb script version
    # noise = np.zeros(n)  
    noise = input_signal_data[0][6]
    
    '''==CALCULATIONS=====================================================================
    '''
    # Convert freq cut-off units from Hz to rad/s
    w_0 = np.pi*2*freq_cut_off
    w_z = np.pi*2*freq_zero

    # Apply FFT (time -> freq domain)
    T = n/fs
    k = np.arange(n)
    frq = k/T # Positive/negative freq (double sided)
    Y = np.fft.fft(signal)
    N = np.fft.fft(noise) # MV 20.01.r3 21-Jun-20
    

    
    Y = np.fft.fftshift(Y)
    N = np.fft.fftshift(N)
    frq = frq - fs/2

    #frq = frq - frq[int(round(fft_size/2))]
    
    #Y = np.fft.fft(signal)
    #N = np.fft.fft(noise) # MV 20.01.r3 21-Jun-20
    
    # Apply transfer function (freq domain)
    if filter_type == 'Low-pass (n=1)':
        Y_trans = transfer_lowpass_1st_order(Y, frq, w_0, n)
        # MV 20.01.r3 21-Jun-20
        N_trans = transfer_lowpass_1st_order(N, frq, w_0, n)
    elif filter_type == 'High-pass (n=1)':
        Y_trans = transfer_highpass_1st_order(Y, frq, w_0, n)
        # MV 20.01.r3 21-Jun-20
        N_trans = transfer_highpass_1st_order(N, frq, w_0, n)
    elif filter_type == 'Low-pass (n=2)':
        Y_trans = transfer_lowpass_2nd_order(Y, frq, w_0, Q, n)  
        # MV 20.01.r3 21-Jun-20
        N_trans = transfer_lowpass_2nd_order(N, frq, w_0, Q, n)  
    elif filter_type == 'High-pass (n=2)':
        Y_trans = transfer_highpass_2nd_order(Y, frq, w_0, Q, n) 
        # MV 20.01.r3 21-Jun-20
        N_trans = transfer_highpass_2nd_order(N, frq, w_0, Q, n) 
    elif filter_type == 'Band-pass (n=2)':
        Y_trans = transfer_bandpass_2nd_order(Y, frq, w_0, Q, n)
        # MV 20.01.r3 21-Jun-20 
        N_trans = transfer_highpass_2nd_order(N, frq, w_0, Q, n)         
    elif filter_type == 'Notch (n=2)':
        Y_trans = transfer_notch_2nd_order(Y, frq, w_0, w_z, Q, n) 
        # MV 20.01.r3 21-Jun-20
        N_trans = transfer_notch_2nd_order(N, frq, w_0, w_z, Q, n) 
    elif filter_type == 'All-pass (n=2)':
        Y_trans = transfer_allpass_2nd_order(Y, frq, w_0, Q, n) 
        # MV 20.01.r3 21-Jun-20
        N_trans = transfer_allpass_2nd_order(N, frq, w_0, Q, n)
        
    # Building freq response curves
    if freq_resp_curves == 2:
        if config.sim_status_win_enabled == True:
            config.sim_status_win.textEdit.append('Building freq response curves...')
        mag = np.abs(Y_trans/Y)
        mag = 20*np.log10(mag)
        ph = np.angle(Y_trans/Y)
        ph = np.rad2deg(ph)
        # Create instance of graphing object
        config.analog_filter_graph = config.view.FilterAnalyzer(frq, 
                                                             mag, ph, n, freq_cut_off,
                                                             filter_type)
        config.analog_filter_graph.show()
    
    #Y_trans = np.fft.ifftshift(Y_trans)
    sig_out = np.fft.ifft(np.fft.ifftshift(Y_trans)) 
    
    #N_trans = np.fft.ifftshift(N_trans)
    noise_out = np.fft.ifft(np.fft.ifftshift(N_trans))
    #https://www.mathworks.com/matlabcentral/answers/17885-time-domain-signal-reconstruction-from-frequency-domain
    
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
    
    '''==RESULTS==========================================================================
    '''
    script_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=================================='''
    #MV 20.01.r3 21-Jun-20: Changed "noise" to "noise_out"
    return ([[2, sig_type, carrier, fs, time, sig_out, noise_out]], 
                 script_parameters, script_results)

def transfer_lowpass_1st_order(Y, frq, w_0, n):
    # w_0 / (s + w_0) Source: REFs 5,7
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = w_0 / (s + w_0)
        Y_trans[i] = Y[i] * H_w
    return Y_trans 

def transfer_highpass_1st_order(Y, frq, w_0, n):
    # s / (s + w_0) Source: REFs 6,7
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = s / (s + w_0)
        Y_trans[i] = Y[i] * H_w
    return Y_trans     
    
def transfer_lowpass_2nd_order(Y, frq, w_0, Q, n):
    # w_0^2 / (s^2 + (w_0/Q)*s + w_0^2) Source: REF 1 (Fig 8.10)
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = (w_0*w_0) / ((s*s) + ((w_0/Q)*s) + (w_0*w_0))
        Y_trans[i] = Y[i] * H_w
    return Y_trans

def transfer_highpass_2nd_order(Y, frq, w_0, Q, n):
    # s^2 / (s^2 + (w_0/Q)*s + w_0^2) Source: REF 1 (Fig 8.10)
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = (s*s) / ((s*s) + (w_0/Q)*s + (w_0*w_0))
        Y_trans[i] = Y[i] * H_w
    return Y_trans

def transfer_bandpass_2nd_order(Y, frq, w_0, Q, n):
    # (w_0/Q)*s / (s^2 + (w_0/Q)*s + w_0^2) Source: REF 1 (Fig 8.10)
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi        
        H_w = (w_0/Q)*s / ((s*s) + (w_0/Q)*s + (w_0*w_0))
        Y_trans[i] = Y[i] * H_w
    return Y_trans

def transfer_notch_2nd_order(Y, frq, w_0, w_z, Q, n):
    # (s^2 + w_z^2) / (s^2 + (w_0/Q)*s + w_0^2) Source: REF 1 (Fig 8.10)
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = ((s*s) + (w_z*w_z)) / ((s*s) + (w_0/Q)*s + (w_0*w_0))
        Y_trans[i] = Y[i] * H_w
    return Y_trans

def transfer_allpass_2nd_order(Y, frq, w_0, Q, n):
    # (s^2 - (w_0/Q)*s + w_0^2) / (s^2 + (w_0/Q)*s + w_0^2) Source: REF 1 (Fig 8.10)
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi
        H_w = ((s*s) - (w_0/Q)*s + (w_0*w_0)) / ((s*s) + (w_0/Q)*s + (w_0*w_0))
        Y_trans[i] = Y[i] * H_w
    return Y_trans