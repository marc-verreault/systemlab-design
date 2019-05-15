"""
SystemLab-Design 19.02
Configuration file
Version: 1.0 (27-Feb-2018)

"""
import os
test = os.getcwd()
root_path = os.path.dirname(__file__)
root_path = os.getcwd()

#import importlib
#custom_viewers_path = str('syslab_config_files.systemlab_viewers')
#view = importlib.import_module(custom_viewers_path)
#
#fb_status_dialog = view.FunctionalBlockStatusGUI()

app = None
status = None

text_source = ''

'''Simulator default settings=============================================================
'''
sampling_rate_default = 1.00E+11 #Hz
sample_period_default = 1.00E-11 #sec
simulation_time_default = 1.00E-08 #sec
num_samples_default = 1.000E+03 #samples number: n

'''Simulator global initializations (flags/windows)=======================================
'''
# The simulation status GUI instance 'sim_status_win' is shared between
# the main application and the script modules used for each functional
# block calculation
sim_status_win = None # Simulation status panel (global instance)
sim_status_win_enabled = True # When True, status window is active
sim_data_view = None # Data viewer panel (global instance)
sim_data_activate = False # When True, data window wiull be displayed/active
sim_pause_flag = False # Boolean flag for pausing simulation
stop_sim_flag = False # Boolean flag for stopping simulation