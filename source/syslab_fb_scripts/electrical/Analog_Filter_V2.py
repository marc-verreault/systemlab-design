"""
SystemLab-Design Version 20.01.r3 8-Jul-20
Functional block script: Analog Filter
Version 2.0 (8-Jul-20)

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
8) Wikipedia contributors, "Butterworth filter," Wikipedia, The Free Encyclopedia, 
https://en.wikipedia.org/w/index.php?title=Butterworth_filter&oldid=944627575 (accessed July 8, 2020).
9) Wikipedia contributors, "Bessel filter," Wikipedia, The Free Encyclopedia, 
https://en.wikipedia.org/w/index.php?title=Bessel_filter&oldid=965349735 (accessed July 8, 2020)
10) Group Delay, Christopher J. Struck, 
http://www.cjs-labs.com/sitebuildercontent/sitebuilderfiles/GroupDelay.pdf (accessed Julu 8, 2020)
"""
import numpy as np
import config

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
    order = int(parameters_input[1][1])
    order_bw = int(parameters_input[2][1])
    order_bt = int(parameters_input[3][1])
    freq_cut_off = float(parameters_input[5][1])
    Q = float(parameters_input[6][1])
    freq_zero = float(parameters_input[7][1])
    freq_resp_curves = int(parameters_input[8][1])
    
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

    """Apply FFT (time -> freq domain)-------------------------------------------------"""
    T = n/fs
    k = np.arange(n)
    frq = k/T # Positive/negative freq (double sided)
    Y = np.fft.fft(signal)
    Y = np.fft.fftshift(Y)
    N = np.fft.fft(noise)
    N = np.fft.fftshift(N)
    # Adjust frequencies
    frq = frq - frq[int(round(n/2))]
    
    """Apply transfer function (freq domain)--------------------------------------------"""
    if filter_type == 'Low-pass':
        if order == 1:
            Y_trans = transfer_lowpass_1st_order(Y, frq, w_0, n)
            N_trans = transfer_lowpass_1st_order(N, frq, w_0, n)
        else:
            Y_trans = transfer_lowpass_2nd_order(Y, frq, w_0, Q, n)
            N_trans = transfer_lowpass_2nd_order(N, frq, w_0, Q, n)  
    elif filter_type == 'Butterworth (Low-pass)':
        if order_bw == 2:
            Y_trans = transfer_lowpass_butterworth_2(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_2(N, frq, w_0, n) 
        elif order_bw == 3:
            Y_trans = transfer_lowpass_butterworth_3(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_3(N, frq, w_0, n) 
        elif order_bw == 4:
            Y_trans = transfer_lowpass_butterworth_4(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_4(N, frq, w_0, n) 
        elif order_bw == 5:
            Y_trans = transfer_lowpass_butterworth_5(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_5(N, frq, w_0, n) 
        elif order_bw == 6:
            Y_trans = transfer_lowpass_butterworth_6(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_6(N, frq, w_0, n)
        elif order_bw == 7:
            Y_trans = transfer_lowpass_butterworth_7(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_7(N, frq, w_0, n)
        elif order_bw == 8:
            Y_trans = transfer_lowpass_butterworth_8(Y, frq, w_0, n)
            N_trans = transfer_lowpass_butterworth_8(N, frq, w_0, n)
    elif filter_type == 'Bessel-Th (Low-pass)':
        if order_bt == 2:
            Y_trans = transfer_lowpass_bessel_thomson_2(Y, frq, w_0, n)
            N_trans = transfer_lowpass_bessel_thomson_2(N, frq, w_0, n) 
        elif order_bt == 3:
            Y_trans = transfer_lowpass_bessel_thomson_3(Y, frq, w_0, n)
            N_trans = transfer_lowpass_bessel_thomson_3(N, frq, w_0, n) 
        elif order_bt == 4:
            Y_trans =transfer_lowpass_bessel_thomson_4(Y, frq, w_0, n)
            N_trans = transfer_lowpass_bessel_thomson_4(N, frq, w_0, n) 
        elif order_bt == 5:
            Y_trans = transfer_lowpass_bessel_thomson_5(Y, frq, w_0, n)
            N_trans = transfer_lowpass_bessel_thomson_5(N, frq, w_0, n) 
    elif filter_type == 'High-pass':
        if order == 1:
            Y_trans = transfer_highpass_1st_order(Y, frq, w_0, n)
            N_trans = transfer_highpass_1st_order(N, frq, w_0, n)
        else:
            Y_trans = transfer_highpass_2nd_order(Y, frq, w_0, Q, n) 
            N_trans = transfer_highpass_2nd_order(N, frq, w_0, Q, n) 
    elif filter_type == 'Band-pass (n=2)':
        Y_trans = transfer_bandpass_2nd_order(Y, frq, w_0, Q, n)
        N_trans = transfer_highpass_2nd_order(N, frq, w_0, Q, n)         
    elif filter_type == 'Notch (n=2)':
        Y_trans = transfer_notch_2nd_order(Y, frq, w_0, w_z, Q, n) 
        N_trans = transfer_notch_2nd_order(N, frq, w_0, w_z, Q, n) 
    elif filter_type == 'All-pass (n=2)':
        Y_trans = transfer_allpass_2nd_order(Y, frq, w_0, Q, n) 
        N_trans = transfer_allpass_2nd_order(N, frq, w_0, Q, n)
        
    """Building freq response curves---------------------------------------------"""
    if freq_resp_curves == 2:
        if config.sim_status_win_enabled == True:
            config.sim_status_win.textEdit.append('Building freq response curves...')
        # Calculate magnitude
        mag = np.abs(Y_trans/Y)
        mag = 20*np.log10(mag)
        # Calculate phase
        ph = np.unwrap(np.angle(Y_trans/Y))
        ph = np.rad2deg(ph)
        # Calculate group delay
        # Negative derivative of phase (-d_ph/d_w) - Source: REF 10
        g_delay = np.zeros(n)
        for i in range (1, n-1):
            g_delay[i] = -1*( (ph[i+1] - ph[i-1])/(frq[i+1] - frq[i-1]) ) #Eq 4 (R 10)
        g_delay[0] = -1*( (ph[1] - ph[0])/(frq[1] - frq[0]) ) # Eq 6 (R 10)
        g_delay[-1] = -1*( (ph[-1] - ph[-2])/(frq[-1] - frq[-2]) ) # Eq 7 (R 10)
        g_delay = g_delay/360
        # Create instance of graphing object
        config.analog_filter_graph = config.view.FilterAnalyzer(frq, 
                                                             mag, ph, g_delay, n, freq_cut_off,
                                                             filter_type)
        config.analog_filter_graph.show()
    
    """Apply IFFT (Re-build time-domain signal)--------------------------------"""
    # REF: https://www.mathworks.com/matlabcentral/answers/17885-time-domain-
    # signal-reconstruction-from-frequency-domain (accessed 7-Jul-20)
    sig_out = np.fft.ifft(np.fft.ifftshift(Y_trans)) 
    noise_out = np.fft.ifft(np.fft.ifftshift(N_trans))
    
    '''==OUTPUT PARAMETERS LIST===========================================================
    '''
    script_parameters = []
    script_parameters = parameters_input #If NO changes are made to parameters
    
    '''==RESULTS==========================================================================
    '''
    script_results = []
    
    '''==RETURN (Output Signals, Parameters, Results)=================================='''
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
    
def transfer_lowpass_butterworth_2(Y, frq, w_0, n):
    # Polynomial factors: (s^2 + 1.4142s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 1 / ((s*s) + (np.sqrt(2)*s) + 1)
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_butterworth_3(Y, frq, w_0, n):
    # Polynomial factors: (s + 1)(s^2 + s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 1 / ((s + 1)*(s*s + s + 1))
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_butterworth_4(Y, frq, w_0, n):
    # Polynomial factors: (s^2 + 0.7654s + 1)(s^2 + 1.8478s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 1 / ((s*s + 0.7654*s + 1)*(s*s + 1.8478*s + 1))
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_butterworth_5(Y, frq, w_0, n):
    # Polynomial factors: (s + 1)(s^2 + 0.6180s + 1)(s^2 + 1.6180s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 1 / ((s + 1)*(s*s + 0.6180*s + 1)*(s*s + 1.6180*s + 1))
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_butterworth_6(Y, frq, w_0, n):
    # Polynomial factors: (s^2 + 0.5176s + 1)(s^2 + 1.4142s + 1)(s^2 + 1.9319s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 1 / ((s*s + 0.5176*s + 1)*(s*s + 1.4142*s + 1)*(s*s + 1.9319*s + 1))
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_butterworth_7(Y, frq, w_0, n):
    # Polynomial factors: (s + 1)(s^2 + 0.4450s + 1)(s^2 + 1.2470s + 1)(s^2 + 1.8019s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = ( 1 / ((s + 1)*(s*s + 0.4450*s + 1)*(s*s + 1.2470*s + 1)* 
                     (s*s + 1.8019*s + 1)) )
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_butterworth_8(Y, frq, w_0, n):
    # Polynomial factors: (s^2 + 0.3902s + 1)(s^2 + 1.1111s + 1) x ...
    # (s^2 + 1.6629s + 1)(s^2 + 1.9616s + 1) Source: REF 8
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = ( 1 / ((s*s + 0.3902*s + 1)*(s*s + 1.1111*s + 1) *
                     (s*s + 1.6629*s + 1)*(s*s + 1.9616*s + 1)) )
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_bessel_thomson_2(Y, frq, w_0, n):
    # Polynomial factors: (s^2 + 3s + 3) Source: REF 9
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 3.0 / (s*s + 3*s + 3)
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_bessel_thomson_3(Y, frq, w_0, n):
    # Polynomial factors: (s^3 + 6s^2 + 15s + 15) Source: REF 9
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 15.0 / (np.power(s, 3) + 6*s*s + 15*s + 15)
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_bessel_thomson_4(Y, frq, w_0, n):
    # Polynomial factors: (s^4 + 10s^3 + 45s^2 + 105s + 105) Source: REF 9
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = 105.0 / (np.power(s, 4) + 10*np.power(s, 3) + 45*s*s + 105*s + 105)
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    
def transfer_lowpass_bessel_thomson_5(Y, frq, w_0, n):
    # Polynomial factors: (s^5 + 15s^4 + 105s^3 + 420s^2 + 945s + 945) Source: REF 9
    Y_trans =  np.full(n, 0 + 1j*0, dtype=complex) 
    for i in range(0, n):
        s = 1j*frq[i]*2*np.pi/w_0
        H_w = ( 945.0 / (np.power(s, 5) + 15*np.power(s, 4) + 105*np.power(s, 3) +
                     420*s*s + 945*s + 945) )
        Y_trans[i] = Y[i] * H_w
    return Y_trans
    