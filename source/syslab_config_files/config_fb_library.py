"""
SystemLab-Design 19.02
Configuration file for functional block library & scripts
Version: 1.0 (27-Feb-2018)
"""

'''Functional block scripts=============================================================
'''
# New folders can be added as needed to the syslab_fb_scripts folders and must be 
# added below to the scripts_path list. Otherwise, any fb_script names contained in these
# folders will not be found during a simulation.
# IMPORTANT: Do not change the name or location of the "syslab_fb_scripts" folder! To 
# access fb_scripts from another file/folder location, use the File path fields in 
# Project Settings
scripts_path_list = []
optical_scripts = '\\syslab_fb_scripts\\optical\\'
electrical_scripts = '\\syslab_fb_scripts\\electrical\\'
digital_scripts = '\\syslab_fb_scripts\\digital\\'

scripts_path_list.append(optical_scripts)
scripts_path_list.append(electrical_scripts)
scripts_path_list.append(digital_scripts)

'''Functional block library===============================================================
'''
# The baseline sections are optical, electrical & digital. Sections, groups and members
# can be modified (incl. addition or deletion of any of these items)
library_title = 'Functional block library (1)'
library_main_w = 180
library_main_h = 350

# OPTICAL=================================================================================
# Section title, RGBT numbers, Expanding (boolean)
optical_group_properties = ['Optical', 170, 0, 0, 25, True] 
optical_group  = []
optical_titles = ['Sources/Transmitters', 'Modulators', 'Detectors/Receivers', 
                  'Passive devices', 'Active devices']

opt_sources_transmitters = ['CW Laser', 'Noise Source - Optical']
opt_modulators = ['Mach-Zehnder Modulator']
opt_detectors_receivers = ['PIN-APD Detector']
opt_passive_devices = ['Optical Attenuator', 'X-Coupler (uni-dir)', 'X-Coupler (bi-dir)', 
                       'Optical Splitter', '90 Deg Optical Hybrid', 'Optical Phase Shift']
opt_active_devices = ['Optical Amplifier']

optical_group.append(optical_titles)
optical_group.append(opt_sources_transmitters)
optical_group.append(opt_modulators)
optical_group.append(opt_detectors_receivers)
optical_group.append(opt_passive_devices)
optical_group.append(opt_active_devices)

# ELECTRICAL==============================================================================
electrical_group_properties = ['Electrical', 0, 0, 255, 25, True]
electrical_group = []
electrical_titles = ['Waveform generators', 'Mathematical operators', 'Passive devices', 
                     'Active devices', 'Signal processing', 'Receivers']

elec_waveform_gen = ['Sine Generator', 'Cosine Generator', 'Function Generator',
                     'DC Source', 'Noise Source']
elec_math_operators = ['Adder', 'Subtractor', 'Multiplier']
elec_passives = ['Power Splitter']
elec_actives = ['Electrical Amplifier']
elec_sig_processing = ['Analog Filter']
elec_receivers = ['Decision Circuit', 'Integrate and Dump']

electrical_group.append(electrical_titles)
electrical_group.append(elec_waveform_gen)
electrical_group.append(elec_math_operators)
electrical_group.append(elec_passives)
electrical_group.append(elec_actives)
electrical_group.append(elec_sig_processing)
electrical_group.append(elec_receivers)

# DIGITAL=================================================================================
digital_group_properties = ['Digital', 200, 200, 200, 50, True]
digital_group = []
digital_titles = ['Binary processing', 'Symbol processing']

dgtl_binary = ['PRBS', '2-bit P-S Conv', '2-bit S-P Conv', 'BER Analyzer']
dgtl_symbol = ['IQ generator']

digital_group.append(digital_titles)
digital_group.append(dgtl_binary)
digital_group.append(dgtl_symbol)

# Combine all groups
fb_sections = [optical_group, electrical_group, digital_group]
fb_sections_properties = [optical_group_properties, electrical_group_properties,
                          digital_group_properties]

'''Functional block library (2)===========================================================
'''
#library_2_title = 'Functional block library (2)'
#library_2_w = 180
#library_2_h = 350
## Section title, RGBT numbers, Expanding (boolean)
#custom_group_properties = ['Custom', 170, 0, 0, 25, True] 
#custom_group  = []
#custom_titles = ['Custom devices 1', 'Custom devices 2']
#
#cust_1 = ['TBD', 'TBD']
#cust_2 = ['TBD', 'TBD']
#
#custom_group.append(custom_titles)
#custom_group.append(cust_1)
#custom_group.append(cust_2)

# Combine all groups
#fb_sections_2 = [custom_group]
#fb_sections_properties_2 = [custom_group_properties]
fb_sections_2 = []
fb_sections_properties_2 = []