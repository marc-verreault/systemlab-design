
Aide memoire
============

Output data table formatting
----------------------------

Use the following Python list format when adding a result to the **Output data** table 
of a functional block: :: 

    '''==RESULTS======================================================================='''
    # Name of the list of lists being returned by the fb_script method
    fb_name_results = []

    # When adding a header use the following format (the Boolean True is used to identify 
    # that this line is a header)
    header_main = ['Header title', '', '', '', True]
    
    # When adding data results, use the following format:
    data_1_result = ['Data name 1', data_value_1, 'units 1', 'notes 1', False, 'format 1']
    data_2_result = ['Data name 2', data_value_2, 'units 2', 'notes 1', False, 'format 2']
    
    # 'Data name 1' is a string
    # data_value_1 is a numerical result (float)
    # 'units 1' is a string - used to represent the results units (e.g. dBm, W, C, sec, etc.)
    # 'notes 1' is a string - used for adding further information
    # False is a Boolean - indicates that this line/list is a numerical result
    # 'format 1' is a string - used to specify the format of the numerical result:
    # Examples: '0.3E' -> 1.134E+02, '0.2f' -> 113.40
    
    # After all result and header lists are in place, assemble these into the main results
    # list
    fb_name_results = [header_main, data_1_result, data_2_result]
    
Data panels list formatting
---------------------------

Use the following Python list format when adding numerical results to a **Data panel** : :: 
   
    '''==DATA PANEL UPDATE========================================='''
    config_data_panel.data_table_1 = [] #This is the name of the list (defined in config_data_panels.py)
    data_1 = ['Data name 1', data_value_1, 'format 1', 'units 1', 'color name 1', 'color data 1']
    data_2 = ['Data name 2', data_value_2, 'format 2', 'units 2', 'color name 2', 'color data 2']
    data_list = [data_1, data_2]
    config_data_panel.data_table_1.extend(data_list) # Add data lists to table list
    
    # 'Data name 1' is a string
    # data_value_1 is a numerical result (float)
    # 'format 1' is a string - used to specify the format of the numerical result:
    # Examples: '0.3E' -> 1.134E+02, '0.2f' -> 113.40
    # 'units 1' is a string - used to represent the results units (e.g. dBm, W, C, sec, etc.)
    # 'color name 1' is a string - used to specify the color of 'Data name 1'
    # 'color name 2' is a string - used to specify the color of data_value_1 & 'units 1'
    # To define the color, used the HTML format: e.g. '#aa0000'
    # NOTE: The 'color name 1' and 'color name 2' list elements are optional. When not included,
    # default color settings will be used
    