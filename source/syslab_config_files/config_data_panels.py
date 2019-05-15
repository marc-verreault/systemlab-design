"""
SystemLab-Design 19.02
Configuration file for data panels
Version: 1.0 (27-Feb-2018)
"""

'''Data panel global initializations======================================================
'''
# Data table dictionaries (for exporting to data boxes in a scene)
# IMPORTANT: Each data box must be linked to a unique data_source_file name. It is
# recommended to link the ID to the project name followed by a number. For example,
# project "Laser" may have two data panels. Set these to laser_1 and laser_2.
data_box_dict = {}

#QPSK model (Electrical applications/QPSK Design)
data_table_qpsk_1_iterations = {}
data_table_qpsk_1 = []
data_table_qpsk_2_iterations = {}
data_table_qpsk_2 = []
data_table_qpsk_3_iterations = {}
data_table_qpsk_3 = []
data_box_dict['qpsk_1'] = data_table_qpsk_1_iterations
data_box_dict['qpsk_2'] = data_table_qpsk_2_iterations
data_box_dict['qpsk_3'] = data_table_qpsk_3_iterations

#Feedback project (Feedback applications)
data_table_cooling_1_iterations = {}
data_table_cooling_1 = []
data_box_dict['cooling_1'] = data_table_cooling_1_iterations

def update_data_tables_iteration(iteration, project_name):
    #QPSK project
    if project_name == 'QPSK Design':
        data_table_qpsk_1_iterations[iteration] = data_table_qpsk_1
        data_table_qpsk_2_iterations[iteration] = data_table_qpsk_2
        data_table_qpsk_3_iterations[iteration] = data_table_qpsk_3
        
    #Feedback project
    if project_name == 'Newton Law Cooling':
        data_table_cooling_1_iterations[iteration] = data_table_cooling_1
              
def update_data_dictionaries(project_name):
    #QPSK project
    if project_name == 'QPSK Design':
        data_box_dict['qpsk_1'] = data_table_qpsk_1_iterations
        data_box_dict['qpsk_2'] = data_table_qpsk_2_iterations
        data_box_dict['qpsk_3'] = data_table_qpsk_3_iterations
        
    #Feedback project
    if project_name == 'Newton Law Cooling':
        data_box_dict['cooling_1'] = data_table_cooling_1_iterations
