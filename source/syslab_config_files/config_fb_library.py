'''
SystemLab-Design 20.01
Configuration file for functional block library & scripts
Version: 1.0 (27-Feb-2018)
Version: 2.0 (7-Sep-2019)
Version: 3.0 (5-Mar-2020)
'''

'''Functional block scripts===========================================
    New folders can be added as needed to the syslab_fb_scripts folders and must be
    added below to the scripts_path list. Otherwise, any fb_script names contained in these
    folders will not be found during a simulation.
    IMPORTANT: Do not change the name or location of the "syslab_fb_scripts" folder! To 
    access fb_scripts from another file/folder location, use the File path fields in Project Settings
'''
scripts_path_list = []
optical_scripts = '\\syslab_fb_scripts\\optical\\'
electrical_scripts = '\\syslab_fb_scripts\\electrical\\'
digital_scripts = '\\syslab_fb_scripts\\digital\\'

scripts_path_list.append(optical_scripts)
scripts_path_list.append(electrical_scripts)
scripts_path_list.append(digital_scripts)

'''Functional block library===========================================
    The baseline sections are optical, electrical & digital. Sections, groups and members
    can be modified (incl. addition or deletion of any of these items)
'''
fb_library_group = []
fb_library_group_properties = []
fb_library_group_settings = []

library_title = 'Functional block library (1)'
library_title_background_color = '#dddddd'
library_main_w = 250 #Height of menu tree window
library_main_h = 400 #Width of menu tree window
lib_settings_1 = [library_title, library_title_background_color, library_main_w, library_main_h]
fb_library_group_settings.append(lib_settings_1)

''' OPTICAL------------------------------------------------------------------------'''
optical_group_properties = ['Optical', 170, 0, 0, 25, True] ## Section title, RGBT numbers, Expanding (boolean)
optical_group  = []
optical_titles = ['Sources/Transmitters', 'Modulators', 'Signal processing/routing', 
                        'Fibers', 'Couplers/splitters/attenuators', 'Polarization devices', 
                        'Amplifiers', 'Detectors/Receivers', 'Analyzers']

opt_sources_transmitters = ['CW Laser', 'CW Laser Array', 'Gaussian Pulse (Optical)', 
                                           'Noise Source - Optical']
opt_modulators = ['Mach-Zehnder Modulator']
opt_signal_processing = ['Branching node (Optical)', 'Optical Circulator', 
                                      'Optical Filter (Band Pass)', 'Fiber Bragg Grating', 
                                      'Optical Phase Shift']
opt_passive_devices_fiber = ['Optical Fiber (Linear)']
opt_passive_devices_couplers = ['Optical Attenuator', 'X-Coupler (uni-dir)', 
                                                 'X-Coupler (bi-dir)', 'Optical Splitter', 
                                                 'Optical Splitter (4 Port)']
opt_pol_devices = ['Polarization Beam Splitter', 'Polarization Beam Combiner', 'Jones Matrix']
opt_active_devices = ['Optical Amplifier']
opt_detectors_receivers = ['PIN-APD Detector', '90 Deg Optical Hybrid']
opt_analyzers = ['Measurement Node (Optical)']

optical_group.append(optical_titles)
optical_group.append(opt_sources_transmitters)
optical_group.append(opt_modulators)
optical_group.append(opt_signal_processing)
optical_group.append(opt_passive_devices_fiber)
optical_group.append(opt_passive_devices_couplers)
optical_group.append(opt_pol_devices)
optical_group.append(opt_active_devices)
optical_group.append(opt_detectors_receivers)
optical_group.append(opt_analyzers)

''' ELECTRICAL--------------------------------------------------------------------'''
electrical_group_properties = ['Electrical', 0, 0, 255, 25, True]
electrical_group = []
electrical_titles = ['Waveform generators', 'Mathematical operators', 'Splitters', 
                     'Amplifiers', 'Signal processing', 'Receivers', 'Analyzers']

elec_waveform_gen = ['Sine Generator', 'Cosine Generator', 'Function Generator', 
                     'Gaussian Pulse Generator', 'DC Source', 'Noise Source']
elec_math_operators = ['Branching Node (Electrical)', 'Adder', 'Subtractor', 'Multiplier',
                       'Sign Inverter', 'Vertical Shift', 'Phase Shift (Electrical)']
elec_passives = ['Power Splitter']
elec_actives = ['Electrical Amplifier']
elec_sig_processing = ['Analog Filter']
elec_receivers = ['Decision Circuit', 'Integrate and Dump', 'Comparator', 'Analog to Digital Converter']
elec_analyzers = ['Measurement Node (Electrical)', 'Multiple Port Viewer (Electrical)']

electrical_group.append(electrical_titles)
electrical_group.append(elec_waveform_gen)
electrical_group.append(elec_math_operators)
electrical_group.append(elec_passives)
electrical_group.append(elec_actives)
electrical_group.append(elec_sig_processing)
electrical_group.append(elec_receivers)
electrical_group.append(elec_analyzers)

''' DIGITAL-------------------------------------------------------------------------'''
digital_group_properties = ['Digital', 200, 200, 200, 50, True]
digital_group = []
digital_titles = ['Binary functional blocks', 'Symbol functional blocks', 'Analyzers']

dgtl_binary = ['PRBS', '2-bit P-S Conv', '2-bit S-P Conv', 'Branching Node (Digital)']
dgtl_symbol = ['IQ generator']
dgtl_analyzers = ['BER Analyzer']

digital_group.append(digital_titles)
digital_group.append(dgtl_binary)
digital_group.append(dgtl_symbol)
digital_group.append(dgtl_analyzers)

'''Combine all groups--------------------------------------------------------------'''
fb_sections = [optical_group, electrical_group, digital_group]
fb_sections_properties = [optical_group_properties, electrical_group_properties,
                                      digital_group_properties]
                                      
fb_library_group.append(fb_sections)
fb_library_group_properties.append(fb_sections_properties)

'''Functional block library (2)================================================
'''
'''library_title = 'Functional block library (2)'
library_title_background_color = '#dddddd'
library_main_w = 250 #Width of menu tree window
library_main_h = 130 #Height of menu tree window
lib_settings_2 = [library_title, library_title_background_color, library_main_w, library_main_h]

## Section title, RGBT numbers, Expanding (boolean)
custom_group_properties = ['Custom', 170, 0, 0, 25, True] 
custom_group  = []
custom_titles = ['Custom devices 1', 'Custom devices 2']

cust_1 = ['TBD', 'TBD']
cust_2 = ['TBD', 'TBD']

custom_group.append(custom_titles)
custom_group.append(cust_1)
custom_group.append(cust_2)

fb_sections_2 = [custom_group]
fb_sections_properties_2 = [custom_group_properties]

fb_library_group_settings.append(lib_settings_2)
fb_library_group.append(fb_sections_2)
fb_library_group_properties.append(fb_sections_properties_2)'''
