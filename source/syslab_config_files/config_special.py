"""
SystemLab-Design 20.01.r1
Configuration file for various settings
Version: 1.0 (15-Nov-2019)
"""

'''Color settings for signal types (functional block ports and signal links)========
Refs: https://doc.qt.io/archives/qt-4.8/qt.html#GlobalColor-enum
'''
c_elec = [0, 0, 255] # Electrical signal (blue) (#0000ff)
c_opt = [128, 0, 0] # Optical signal (dark red) (#800000)
c_digital = [160, 160, 160] # Digital signal (gray) (#a0a0a4)
c_analog_1 = [0, 128, 0] # Analog signal 1 (dark green) (#008000)
c_analog_2 = [128, 0, 128] # Analog signal 2 (dark magenta) (#800080)
c_analog_3 =  [0, 128, 128] # Analog signal 2 (dark cyan) (#008080)
c_disabled =  [192, 192, 192] # Disabled (light gray) (#c0c0c0)

'''Hover display settings (functional block/ports)===================================
'''
display_fb_results_tool_tip = True # Display results for functional block (on hover)
display_fb_dim_coord_tool_tip = True # Display fb coordinates (on hover)
display_port_results_tool_tip = True # Display results for port object (on hover)

'''Highlight connections (signal links)==============================================
'''
highlight_links_on_hover = True # Highlight signal path on hover enter or move event

'''Functional block (left-double click)==============================================
'''
open_script_on_left_double_click = False # Opens script after left double-clicking on fb
                                         # Default opens fb properties dialog
                                         
'''Warning message (high number of samples)========================================
'''
num_samples_threshold = 1e6  # Issues warning before starting simulation (simulation can be
                             # aborted)
                             
'''Default font setting for dialogs=======================================================
'''
global_font = 'font-size: 8pt; font-family: Segoe UI;' # Can be specified in pixels (px)
                                                        # or points (pt)