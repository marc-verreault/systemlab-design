"""
Cavity FP
"""

import numpy as np
import config
from scipy import constants
# REF: https://docs.scipy.org/doc/scipy/reference/constants.html
import project_fabry_perot as project

#import systemlab_viewers as view
import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)


def run(input_signal_data, parameters_input, settings):
    
    '''==PROJECT SETTINGS==================================================='''
    module_name = 'Phase shift'
    n = settings['num_samples']
    n = int(round(n))
    i = settings['current_iteration']
    segments = settings['feedback_segments']
    segment = settings['feedback_current_segment']
    feedback_mode = settings['feedback_enabled']
    time = settings['time_window']
    fs = settings['sampling_rate']
    t_step = settings['sampling_period']

    if config.sim_status_win_enabled == True:
        config.sim_status_win.textEdit.append('Starting ' + module_name + 
                                          ' - Iteration #: ' + str(i))
        config.app.processEvents()
    if config.sim_data_activate == True:
        config.sim_data_view.dataEdit.append('Data output for ' + module_name + 
                                          ' - Iteration #: ' + str(i))
    
    '''==PARAMETERS========================================================='''
    #Load parameters from FB parameters table
    #Format: Parameter name(0), Value(1), Units(2), Notes(3)
    d = float(parameters_input[0][1]) # Cavity length (m)
    index = float(parameters_input[1][1]) #Refractive index within cavity
    r = float(parameters_input[2][1])
    
    '''==INPUT SIGNALS======================================================'''
    signal_type = 'Optical'
    time_array = input_signal_data[0][3]  
    optical_in = input_signal_data[0][4]
    wave_key = optical_in[0][0]
    wave_freq = optical_in[0][1]
    e_field_input_port_1 = optical_in[0][3]
    jones_vector = optical_in[0][2]
    noise_array = optical_in[0][4]
    psd_array = optical_in[0][5]
    
    '''==CALCULATIONS=======================================================
    '''
    ph_shift = 2*np.pi*index*d/(constants.c/wave_freq)
    time_delay = 2*index*d/constants.c
    if time_delay > 0:
        fsr = 1/time_delay
    
    t = 1-r

    e_field_trans = np.full(n, 0 + 1j*0, dtype=complex) 
    e_field_ref = np.full(n, 0 + 1j*0, dtype=complex)
    
    a_trans = -np.square(t)*np.exp(-1j*ph_shift)/(1 - np.square(r)*np.exp(-2j*ph_shift))
    
    if feedback_mode == 2:
        segment_length = float(n)/float(segments)
        start_index = int(round(segment * segment_length) - segment_length)
        for seg in range(start_index, n): 
            e_field_trans[seg] = e_field_input_port_1[seg]*a_trans
            e_field_ref[seg] = e_field_input_port_1[seg]
    else:
        e_field_trans = e_field_input_port_1*a_trans
        e_field_ref = e_field_input_port_1
        
    '''==OUTPUT PARAMETERS LIST============================================='''
    cavity_parameters = []
    cavity_parameters = parameters_input

    '''==RESULTS============================================================'''
    cavity_results = []
    ph_shift_result = ['Phase shift (one-way)', ph_shift, 'rad', ' ']
    time_delay_result = ['Optical time delay (one-way)', time_delay, 's', ' ']
    fsr_result = ['Free spectral range', fsr*1e-12, 'THz', ' ']
    cavity_results = [ph_shift_result, time_delay_result, fsr_result]
    
    trans_power = np.average(np.abs(e_field_trans)*np.abs(e_field_trans))/n
    
    if i == 1:
        project.trans_1 = []
        project.trans_1.append(trans_power)
        project.simulation_analyzer = view.IterationsAnalyzer_FabryPerot(project.wave,
                              project.trans_1)
        project.simulation_analyzer.show()
    else:
        project.trans_1.append(trans_power)
        project.simulation_analyzer.figure.tight_layout(pad=0)
        project.simulation_analyzer.plot_xy()
        project.simulation_analyzer.canvas.draw()

    '''==RETURN (Output Signals, Parameters, Results)=========================='''
    optical_out_2 = [[wave_key, wave_freq, jones_vector, e_field_trans, noise_array, psd_array]]
    optical_out_3 = [[wave_key, wave_freq, jones_vector, e_field_ref, noise_array, psd_array]] 
      
    return ([[2, signal_type, fs, time_array, optical_out_2],
             [3, signal_type, fs, time_array, optical_out_3]], 
              cavity_parameters, cavity_results)

