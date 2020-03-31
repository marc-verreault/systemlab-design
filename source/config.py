"""
SystemLab-Design 20.01.r1
Configuration file
Version: 1.0 (27-Feb-2019)
Version: 2.0 (25_Oct-2019)
"""
import os
test = os.getcwd()
root_path = os.path.dirname(__file__)
root_path = os.getcwd()

app = None #Used for app.processEvents (called with main application & fb scripts)
status = None #Info/Status box (called with main application & fb scripts)
text_source = ''

'''Simulator default settings=============================================================
'''
sampling_rate_default = 1.00E+11 #Hz
sample_period_default = 1.00E-11 #sec
simulation_time_default = 1.00E-08 #sec
num_samples_default = 1.000E+03 #samples number: n

'''Simulator global initializations (flags/windows)=======================================
The simulation status GUI instance 'sim_status_win' is shared between the main
application and the script modules used for each functional block calculation
'''
sim_status_win = None # Simulation status panel (global instance)
sim_status_win_enabled = True # When True, status window is active
sim_data_view = None # Data viewer panel (global instance)
sim_data_activate = False # When True, data window will be displayed/active
sim_graph_view = None # Graph viewer (global instance) MV 20.01.r2 2 Feb 20
sim_pause_flag = False # Boolean flag for pausing simulation
stop_sim_flag = False # Boolean flag for stopping simulation

'''Data panel global initializations======================================================
Data table dictionaries (for exporting to data boxes in a scene)
IMPORTANT: Each data box must be linked to a unique data_source_file name. It is
recommended to link the ID to the project name followed by a number. For example,
project "Laser" may have two data panels. Set these to laser_1 and laser_2.
'''
data_box_dict = {} # Containing dictionary for all data panel objects, holds data_tables
                   # and data_tables_iterations

data_tables = {} # Dictionary for tracking data results lists for each data panel

data_tables_iterations = {} # Nested dictionary that saves/tracks data_tables over multiple
                            # iterations
                            
'''Graph initializations==================================================================
Initialization of graphing objects that have been integrated into fb library
'''
import importlib
custom_viewers_path = str('syslab_config_files.systemlab_viewers')
view = importlib.import_module(custom_viewers_path)

fbg_graph = None # Graph object for FBG functional block
analog_filter_graph = None # Graph object for Analog filter functional block
mzm_graph = None # Graph object for Mach-Zhender modulator functional block


# New feature 20.01.r2 17-Feb-20 (quick view of arbitrary x-y data points)   
xy_graph_dict = {}

def set_new_key(object_list):
    i = 1 
    while (i in object_list): #Set new key for object dictionary
        i += 1 
    return i

def display_xy_data(title, x_data, x_units, y_data, y_units):
    i = set_new_key(xy_graph_dict) 
    xy_graph_dict[i] = view.X_Y_Analyzer(title, x_data, x_units, y_data, y_units)
    xy_graph_dict[i].show()

'''def display_xy_data(title, x_data, y_data):
    xy_graph_dict = view.X_Y_Analyzer(title, x_data, y_data)
    return graph_xy'''
    
'''Functions==============================================================================
'''
def display_data(text, data, new_line):
    if sim_data_activate == True:
        if new_line == True:
            sim_data_view.dataEdit.append(text)
            sim_data_view.dataEdit.append(str(data))
        else:
            sim_data_view.dataEdit.append(text + str(data))
        
def status_message(text):      
    if sim_status_win_enabled == True:
        sim_status_win.textEdit.append(text)
    status.setText(text)
    app.processEvents()



