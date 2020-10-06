"""
SystemLab-Design 20.01.r3 19-Jun-20
Configuration port viewers file
"""

'''Port viewers plot settings==================================================
Update these settings to change the look & feel of port viewer 
figures and plots. 
Parameters include line colors/widths/styles, marker styles/sizes/colors, 
figure/plot background colors, grid styles/widths/colors, label/axis colors.
'''
"""Optical port viewer---------------------------------------------------------
"""
optical_frame_background_color = '#f9f9f9'
# Time-domain tab (data plots)
optical_time_fig_back_color = '#f9f9f9'
optical_time_plot_back_color = '#f9f9f9'
optical_time_labels_axes_color = 'black'
optical_time_signal_color = 'b'
optical_time_signal_linestyle = '--'
optical_time_signal_linewidth = 0.8
optical_time_signal_marker = 'o'
optical_time_signal_markersize = 3
optical_time_noise_color = 'r'
optical_time_noise_linestyle = '--'
optical_time_noise_linewidth = 0.8
optical_time_noise_marker = 'o'
optical_time_noise_markersize = 3
optical_time_sig_noise_color = 'g'
optical_time_sig_noise_linestyle = '--'
optical_time_sig_noise_linewidth = 0.8
optical_time_sig_noise_marker = 'o'
optical_time_sig_noise_markersize = 3
optical_time_phase_color = 'y'
optical_time_phase_linestyle = '--'
optical_time_phase_linewidth = 0.8
optical_time_phase_marker = 'o'
optical_time_phase_markersize = 3
# Time-domain tab (background and grid settings)
optical_time_maj_grid_linestyle = ':'
optical_time_maj_grid_linewidth = 0.5
optical_time_maj_grid_color = 'gray'
optical_time_min_grid_linestyle = ':'
optical_time_min_grid_linewidth = 0.5
optical_time_min_grid_color = 'lightGray'
# Freq-domain tab (data plots)
optical_freq_fig_back_color = '#505050'
optical_freq_plot_back_color = '#000000'
optical_freq_labels_axes_color = 'white'
optical_freq_signal_color = 'y'
optical_freq_signal_linestyle = '--'
optical_freq_signal_linewidth = 0.5
optical_freq_signal_marker = 'o'
optical_freq_signal_markersize = 2
optical_freq_noise_color = 'r'
optical_freq_noise_linestyle = '--'
optical_freq_noise_linewidth = 0.5
optical_freq_noise_marker = 'o'
optical_freq_noise_markersize = 2
optical_freq_sig_noise_color = 'g'
optical_freq_sig_noise_linestyle = '--'
optical_freq_sig_noise_linewidth = 0.5
optical_freq_sig_noise_marker = 'o'
optical_freq_sig_noise_markersize = 2
optical_freq_psd_noise_color = 'orange'
optical_freq_psd_noise_linestyle = '--'
optical_freq_psd_noise_linewidth = 0.5
optical_freq_psd_noise_marker = 'o'
optical_freq_psd_noise_markersize = 2
# Freq-domain tab (background and grid settings)
optical_freq_maj_grid_linestyle = '-'
optical_freq_maj_grid_linewidth = 0.5
optical_freq_maj_grid_color = 'darkGray'
optical_freq_min_grid_linestyle = '-'
optical_freq_min_grid_linewidth = 0.5
optical_freq_min_grid_color = 'darkGray'
# Freq-data (all ch) tab (data plots)
opt_chnls_freq_fig_back_color = '#505050'
opt_chnls_freq_plot_back_color = '#000000'
opt_chnls_freq_labels_axes_color = 'white'
opt_chnls_freq_signal_color = 'y'
opt_chnls_freq_signal_linestyle = '--'
opt_chnls_freq_signal_linewidth = 0.5
opt_chnls_freq_signal_marker = 'o'
opt_chnls_freq_signal_markersize = 2
opt_chnls_freq_noise_color = 'r'
opt_chnls_freq_noise_linestyle = '--'
opt_chnls_freq_noise_linewidth = 0.5
opt_chnls_freq_noise_marker = 'o'
opt_chnls_freq_noise_markersize = 2
opt_chnls_freq_sig_noise_color = 'g'
opt_chnls_freq_sig_noise_linestyle = '--'
opt_chnls_freq_sig_noise_linewidth = 0.5
opt_chnls_freq_sig_noise_marker = 'o'
opt_chnls_freq_sig_noise_markersize = 2
opt_chnls_freq_psd_noise_color = 'orange'
opt_chnls_freq_psd_noise_linestyle = '--'
opt_chnls_freq_psd_noise_linewidth = 0.5
opt_chnls_freq_psd_noise_marker = 'o'
opt_chnls_freq_psd_noise_markersize = 2
# Freq-domain tab (background and grid settings)
opt_chnls_freq_maj_grid_linestyle = '-'
opt_chnls_freq_maj_grid_linewidth = 0.5
opt_chnls_freq_maj_grid_color = 'darkGray'
opt_chnls_freq_min_grid_linestyle = '-'
opt_chnls_freq_min_grid_linewidth = 0.5
opt_chnls_freq_min_grid_color = 'darkGray'

"""Electrical port viewer---------------------------------------------------"""
electrical_frame_background_color = '#f9f9f9'
# Time-domain tab (data plots)
electrical_time_fig_back_color = '#f9f9f9'
electrical_time_plot_back_color = '#f9f9f9'
electrical_time_labels_axes_color = 'black'
electrical_time_signal_color = 'b'
electrical_time_signal_linestyle = '--'
electrical_time_signal_linewidth = 0.8
electrical_time_signal_marker = 'o'
electrical_time_signal_markersize = 3
electrical_time_noise_color = 'r'
electrical_time_noise_linestyle = '--'
electrical_time_noise_linewidth = 0.8
electrical_time_noise_marker = 'o'
electrical_time_noise_markersize = 3
electrical_time_sig_noise_color = 'g'
electrical_time_sig_noise_linestyle = '--'
electrical_time_sig_noise_linewidth = 0.8
electrical_time_sig_noise_marker = 'o'
electrical_time_sig_noise_markersize = 3
electrical_time_sampling_color = 'r'
electrical_time_sampling_linestyle = 'None'
electrical_time_sampling_linewidth = 0.8
electrical_time_sampling_marker = 'o'
electrical_time_sampling_markersize = 3
# Time-domain tab (background and grid settings)
electrical_time_maj_grid_linestyle = ':'
electrical_time_maj_grid_linewidth = 0.5
electrical_time_maj_grid_color = 'gray'
electrical_time_min_grid_linestyle = ':'
electrical_time_min_grid_linewidth = 0.5
electrical_time_min_grid_color = 'lightGray'
# Freq-domain tab (data plots)
electrical_freq_fig_back_color = '#505050'
electrical_freq_plot_back_color = '#000000'
electrical_freq_labels_axes_color = 'white'
electrical_freq_signal_color = 'y'
electrical_freq_signal_linestyle = '--'
electrical_freq_signal_linewidth = 0.5
electrical_freq_signal_marker = 'o'
electrical_freq_signal_markersize = 2
electrical_freq_noise_color = 'r'
electrical_freq_noise_linestyle = '--'
electrical_freq_noise_linewidth = 0.5
electrical_freq_noise_marker = 'o'
electrical_freq_noise_markersize = 2
electrical_freq_sig_noise_color = 'g'
electrical_freq_sig_noise_linestyle = '--'
electrical_freq_sig_noise_linewidth = 0.5
electrical_freq_sig_noise_marker = 'o'
electrical_freq_sig_noise_markersize = 2
# Freq-domain tab (background and grid settings)
electrical_freq_maj_grid_linestyle = '-'
electrical_freq_maj_grid_linewidth = 0.5
electrical_freq_maj_grid_color = 'darkGray'
electrical_freq_min_grid_linestyle = '-'
electrical_freq_min_grid_linewidth = 0.5
electrical_freq_min_grid_color = 'darkGray'
# Eye tab (data plots)
electrical_eye_fig_back_color = '#505050'
electrical_eye_plot_back_color = '#000000'
electrical_eye_labels_axes_color = 'white'
electrical_eye_signal_color = 'orange'
electrical_eye_signal_linestyle = '-'
electrical_eye_signal_linewidth = 0.25
electrical_eye_signal_alpha = 0.3 # MV 20.01.r3 10-Jul-20
electrical_eye_signal_marker = 'o'
electrical_eye_signal_markersize = 1
electrical_eye_sig_noise_color = 'crimson'
electrical_eye_sig_noise_linestyle = '-'
electrical_eye_sig_noise_linewidth = 0.25
electrical_eye_sig_noise_alpha = 0.3 # MV 20.01.r3 10-Jul-20
electrical_eye_sig_noise_marker = 'o'
electrical_eye_sig_noise_markersize = 1
# Eye tab (background and grid settings)
electrical_eye_maj_grid_linestyle = ':'
electrical_eye_maj_grid_linewidth = 0.5
electrical_eye_maj_grid_color = 'darkGray'
electrical_eye_min_grid_linestyle = ':'
electrical_eye_min_grid_linewidth = 0.5
electrical_eye_min_grid_color = 'darkGray'
electrical_eye_hist_color = 'magenta' #MV 20.01.r3 18-Jun-20
electrical_eye_hist_alpha = 1.0 #MV 20.01.r3 18-Jun-20

"""Digital port viewer------------------------------------------------------"""
digital_frame_background_color = '#f9f9f9'
# Time-domain tab (data plots)
digital_time_fig_back_color = '#f9f9f9'
digital_time_plot_back_color = '#f9f9f9'
digital_time_labels_axes_color = 'black'
digital_time_signal_color = 'b'
digital_time_signal_linestyle = '--'
digital_time_signal_linewidth = 0.8
digital_time_signal_marker = 'o'
digital_time_signal_markersize = 3
# Time-domain tab (background and grid settings)
digital_time_maj_grid_linestyle = ':'
digital_time_maj_grid_linewidth = 0.5
digital_time_maj_grid_color = 'gray'
digital_time_min_grid_linestyle = ':'
digital_time_min_grid_linewidth = 0.5
digital_time_min_grid_color = 'lightGray'
# Freq-domain tab (data plots)
digital_freq_fig_back_color = '#f9f9f9'
digital_freq_plot_back_color = '#f9f9f9'
digital_freq_labels_axes_color = 'black'
digital_freq_signal_color = 'b'
digital_freq_signal_linestyle = '--'
digital_freq_signal_linewidth = 0.8
digital_freq_signal_marker = 'o'
digital_freq_signal_markersize = 3
# Freq-domain tab (background and grid settings)
digital_freq_maj_grid_linestyle = ':'
digital_freq_maj_grid_linewidth = 0.5
digital_freq_maj_grid_color = 'darkGray'
digital_freq_min_grid_linestyle = ':'
digital_freq_min_grid_linewidth = 0.5
digital_freq_min_grid_color = 'darkGray'

"""Analog port viewer-------------------------------------------------------"""
analog_frame_background_color = '#f9f9f9'
# Time-domain tab (data plots)
analog_time_fig_back_color = '#f9f9f9'
analog_time_plot_back_color = '#f9f9f9'
analog_time_labels_axes_color = 'black'
analog_time_signal_color = 'b'
analog_time_signal_linestyle = '--'
analog_time_signal_linewidth = 0.8
analog_time_signal_marker = 'o'
analog_time_signal_markersize = 3
# Time-domain tab (background and grid settings)
analog_time_maj_grid_linestyle = ':'
analog_time_maj_grid_linewidth = 0.5
analog_time_maj_grid_color = 'gray'
analog_time_min_grid_linestyle = ':'
analog_time_min_grid_linewidth = 0.5
analog_time_min_grid_color = 'lightGray'
# Freq-domain tab (data plots)
analog_freq_fig_back_color = '#f9f9f9'
analog_freq_plot_back_color = '#f9f9f9'
analog_freq_labels_axes_color = 'black'
analog_freq_signal_color = 'b'
analog_freq_signal_linestyle = '--'
analog_freq_signal_linewidth = 0.8
analog_freq_signal_marker = 'o'
analog_freq_signal_markersize = 3
# Freq-domain tab (background and grid settings)
analog_freq_maj_grid_linestyle = ':'
analog_freq_maj_grid_linewidth = 0.5
analog_freq_maj_grid_color = 'gray'
analog_freq_min_grid_linestyle = ':'
analog_freq_min_grid_linewidth = 0.5
analog_freq_min_grid_color = 'lightGray'

"""Electrical port viewer (multiple plots)----------------------------------"""
m_electrical_frame_background_color = '#f9f9f9'
# Time-domain tab (data plots)
m_electrical_time_fig_back_color = '#f9f9f9'
m_electrical_time_plot_back_color = '#f9f9f9'
m_electrical_time_labels_axes_color = 'black'
m_electrical_time_signal_color = ['b', 'b', 'b', 'b']
m_electrical_time_signal_linestyle = ['--','--', '--', '--'] 
m_electrical_time_signal_linewidth = [0.8, 0.8, 0.8, 0.8]
m_electrical_time_signal_marker = ['o', 's', 'd', '^']
m_electrical_time_signal_markersize = [3, 3, 3, 3]
m_electrical_time_noise_color = ['r', 'r', 'r', 'r']
m_electrical_time_noise_linestyle = ['--','--', '--', '--'] 
m_electrical_time_noise_linewidth = [0.8, 0.8, 0.8, 0.8]
m_electrical_time_noise_marker = ['o', 's', 'd', '^']
m_electrical_time_noise_markersize = [3, 3, 3, 3]
m_electrical_time_sig_noise_color = ['g', 'g', 'g', 'g']
m_electrical_time_sig_noise_linestyle = ['--','--', '--', '--'] 
m_electrical_time_sig_noise_linewidth = [0.8, 0.8, 0.8, 0.8]
m_electrical_time_sig_noise_marker = ['o', 's', 'd', '^']
m_electrical_time_sig_noise_markersize = [3, 3, 3, 3]
# Time-domain tab (background and grid settings)
m_electrical_time_maj_grid_linestyle = ':'
m_electrical_time_maj_grid_linewidth = 0.5
m_electrical_time_maj_grid_color = 'gray'
m_electrical_time_min_grid_linestyle = ':'
m_electrical_time_min_grid_linewidth = 0.5
m_electrical_time_min_grid_color = 'lightGray'
# Freq-domain tab (data plots)
m_electrical_freq_fig_back_color = '#f9f9f9'
m_electrical_freq_plot_back_color = '#f9f9f9'
m_electrical_freq_labels_axes_color = 'black'
m_electrical_freq_signal_color = ['b', 'b', 'b', 'b']
m_electrical_freq_signal_linestyle = ['--','--', '--', '--'] 
m_electrical_freq_signal_linewidth = [0.8, 0.8, 0.8, 0.8]
m_electrical_freq_signal_marker = ['o', 's', 'd', '^']
m_electrical_freq_signal_markersize = [3, 3, 3, 3]
m_electrical_freq_noise_color = ['r', 'r', 'r', 'r']
m_electrical_freq_noise_linestyle = ['--','--', '--', '--'] 
m_electrical_freq_noise_linewidth = [0.8, 0.8, 0.8, 0.8]
m_electrical_freq_noise_marker = ['o', 's', 'd', '^']
m_electrical_freq_noise_markersize = [3, 3, 3, 3]
m_electrical_freq_sig_noise_color = ['g', 'g', 'g', 'g']
m_electrical_freq_sig_noise_linestyle = ['--','--', '--', '--'] 
m_electrical_freq_sig_noise_linewidth = [0.8, 0.8, 0.8, 0.8]
m_electrical_freq_sig_noise_marker = ['o', 's', 'd', '^']
m_electrical_freq_sig_noise_markersize = [3, 3, 3, 3]
# Freq-domain tab (background and grid settings)
m_electrical_freq_maj_grid_linestyle = ':'
m_electrical_freq_maj_grid_linewidth = 0.5
m_electrical_freq_maj_grid_color = 'gray'
m_electrical_freq_min_grid_linestyle = ':'
m_electrical_freq_min_grid_linewidth = 0.5
m_electrical_freq_min_grid_color = 'lightGray'