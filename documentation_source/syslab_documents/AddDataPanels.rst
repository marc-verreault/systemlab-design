.. _data-panel-label:

How to add data panels to a design
==================================

In the following tutorial, we will add **Data panels** to an existing example design. 

  .. note:: 
    A completed version of this design (including the updated *"config_data_panels.py"* file) 
    can be found within the folder *"systemlab_design\\systemlab_examples\\optical\\optical_direct_detection_completed\\"* 

**Part 1: Open the design projects "QPSK Design" and "Optical transmission IM"**

1.  Launch a new application of SystemLab|Design by double left-clicking on the 
    *SystemLab-Design.exe* executable file.
2.  From the **Menu bar**, select **File/Open project** and navigate to the folder 
    *"systemlab_design\\systemlab_examples\\optical\\optical_direct_detection"*
3.  Select the design project *"Optical transmission IM"* (it will have a suffix ".slb") and 
    click on the **Open** button.
4.  From the **Menu bar**, select **File/Open project** and navigate to the folder 
    *"systemlab_design\\systemlab_examples\\electrical\\qpsk_design"*
5.  Select the project *"QPSK Design"* and click on the **Open** button.

**Part 2: Add new data panel objects to the project design space**

6.  Within the *"QPSK Design"* project design space, hover over the data panel for **BER Results** 
    and right-click and select **Copy/paste data panel to another project**.
7.  Within the **Select project for pasting** dialog, select *"Optical transmission IM"* from 
    the pull down menu and select **OK**. *[A copy of the BER Results data panel will appear 
    within the project design space for "Optical transmission IM"]*
    
  .. image:: Data_Panel_1.png
    :align: center
    
8.  Close the design project *"QPSK Design"* by left-clicking on the **Close tab** (**X** 
    icon next to the project name in the upper left tab for the project design space of *"QPSK Design"*).
9.  Within the "Optical transmission IM" project design space, double left-click on the **BER Results** 
    data panel item to open its **Data panel properties** dialog box (make sure to hover over 
    the yellow (data section) region, as the title section will not activate the dialog).
10. In the data field for **Data source file name** change the text to: "opt_im_1".

  .. image:: Data_Panel_2.png
    :align: center

11. Select **OK** to save the save the changes and close the dialog *[Note: A warning message 
    will appear (Incomptable file name key for data panel). This is to be expected, 
    as we have not yet setup the data panel's associated data objects in the config_data_panels.py 
    file]*
12. Select **OK** to close the warning message.
13. Hover over the data panel for **BER Results** and right-click and select **Copy/paste data panel** 
    (**Note:** You will see the same warning message as step 11. Select **OK** to close the warning message.)
14. Double left-click on the copied version of **BER Results** to open its **Data panel properties**.
15. In the data field for **Data source file name** change the text to: "opt_im_2".
16. Select the **Title section (text settings)** tab and update the **Title** field to "Receiver Analysis".

  .. image:: Data_Panel_3.png
    :align: center
    
17. Select **OK** to save the changes and close the dialog (Note: You will see once 
    again the warning message as step 11. Select **OK** to close the warning message.)

**Part 3: Create new data table lists and dictionaries for Optical transmission IM 
(config_data_panels.py)**

18. Open a session of SciTE by selecting **Edit/Open code/script editor** from the **Menu bar**.
19. From the SciTE dialog, select **File/Open**.
20. Navigate to the main application folder *"systemlab_design"* and go to the folder *"syslab_config_files"*. 
    Open the Python module named *"config_data_panels.py"*.   
21. Below the code for **#Feedback project (Feedback applications)** (lines 26-29), insert the 
    following lines of code: ::
    
        #Optical transmission IM
        data_table_opt_im_1_iterations = {}
        data_table_opt_im_1 = []
        data_table_opt_im_2_iterations = {}
        data_table_opt_im_2 = []
        data_box_dict['opt_im_1'] = data_table_opt_im_1_iterations
        data_box_dict['opt_im_2'] = data_table_opt_im_2_iterations
        
22. Below the code for **#Feedback project** (lines 46-48), insert the 
    following lines of code: ::
    
        #Optical transmission IM
        if project_name == 'Optical transmission IM':
            data_table_opt_im_1_iterations[iteration] = data_table_opt_im_1     
            data_table_opt_im_2_iterations[iteration] = data_table_opt_im_2
            
23. Below the code for **#Feedback project** (lines 62-64), insert the 
    following lines of code: ::
    
        #Optical transmission IM
        if project_name == 'Optical transmission IM':
            data_box_dict['opt_im_1'] = data_table_opt_im_1_iterations     
            data_box_dict['opt_im_2'] = data_table_opt_im_2_iterations

    *For the code additions above, we first define new dictionary and list objects for 
    the two data tables that we will be using within the "Optical transmission IM" design project. 
    During a simulation, for each iteration, each data table list (data_table_opt_im_1, 
    data_table_opt_im_2), is added to its associated dictionary (data_table_opt_im_1_iterations, 
    data_table_opt_im_2_iterations).* 
    
    *These dictionaries are then added to the main dictionary "data_box_dict" which tracks all 
    data panels across projects. When a data panel in a project design space is updated, 
    the "data_box_dict" dictionary is accessed and the iterations dictionary associated 
    with the data panel ID ('opt_im_1', 'opt_im_2') is located (this is the information 
    we entered in the "Data source file name" field in steps 10 and 15).*
    
  .. important:: 
    Make sure that the **project_name** text string (used in the methods **update_data_tables_iteration** 
    and **update_data_dictionaries**) is identical to the project title used in the main application 
    interface. If they do not match, the data panel will not be able to display any data 
    (the data section will be empty).
    
24. Click on the **Save** icon in the **Tool Bar** to save all the changes.
25. Close the SciTE dialog (**File/Exit**)
    
**Part 4: Update the fb_scripts for "BER Analysis" and "PIN-APD"**

26. Double left-click on **BER Analysis** to open its functional block properties.
27. Select the **Edit script** icon (next to **Script module name**) to view the script for 
    *"BER_Analysis_Opt_IM"*.
28. Below Line 7 (**import config**) insert the following lines of code: ::

        import importlib
        data_panels_path = str('syslab_config_files.config_data_panels')
        config_data_panel = importlib.import_module(data_panels_path)
        
    *This section of code imports the module config_data_panels.py so that we can access and 
    populate the data table list "data_table_opt_im_1" (which we instantiated in step 21).*
        
29. Under the section for "RESULTS", after **ber_results** (line 49), insert the following 
    lines of code: :: 

        #Send update to data box (data_table_opt_im_1)
        config_data_panel.data_table_opt_im_1 = []
        data_1 = ['Iteration #', iteration, '0.0f', ' ']
        data_2 = ['Binary sequence length', binary_seq_length, 'n', ' ']
        data_3 = ['Errored bits', err_count, '0.0f', ' ']
        data_4 = ['Bit error rate', ber, '0.2E', ' ']
        data_list = [data_1, data_2, data_3, data_4]
        config_data_panel.data_table_opt_im_1.extend(data_list)
        
    *In this section of code, four numerical results (from the CALCULATIONS section) are 
    added to the data table list "data_table_opt_im_1".*
        
30. Click on the **Save** icon in the **Tool Bar** to save all the changes.
31. Close the SciTE dialog (**File/Exit**)
32. Close the functional block properties for **BER Analysis**.
33. Double left-click on **PIN-APD** to open its functional block properties.
34. Select the **Edit script** icon (next to **Script module name**) to view the script for 
    *"PIN_Model_Opt_IM"*.
35. Below Line 20 (**view = importlib.import_module(custom_viewers_path)**) insert the following 
    lines of code: ::

        data_panels_path = str('syslab_config_files.config_data_panels')
        config_data_panel = importlib.import_module(data_panels_path)
        
36. Below lines 355-364 (**pin_results** list definition) insert the following lines of code: ::
  
        '''==DATA PANEL UPDATE========================================='''
        config_data_panel.data_table_opt_im_2 = []
        data_1 = ['Iteration #', iteration, '.0f', ' ']
        data_2 = ['Received power (dBm)', rcv_pwr_dbm, '0.2f', ' ']
        data_3A = ['Q (target)', Q_target, '0.1f', ' ']
        data_3B = ['BER (target)', ber_target, '0.2E', ' ']
        data_3C = ['Q (measured)', Q_measured, '0.2f', ' ']
        data_4 = ['Optical receiver sensitivity (dBm)', pwr_sensitivity_dbm, '0.2f', ' ']
        data_list = [data_1, data_2, data_3A, data_3B, data_3C, data_4]
        config_data_panel.data_table_opt_im_2.extend(data_list)       
    
37. Click on the **Save** icon in the **Tool Bar** to save all the changes.
38. Close the SciTE dialog (**File/Exit**).
39. Close the functional block properties for **PIN-APD**.
40. Drag the data panel for **Receiver Analysis** and place it over the **Decision Circuit** 
    functional block as follows (to drag scene items, left-click hold on the item to be 
    dragged and left-click release once in the target postion)
    
  .. figure:: Data_Panel_4.png
    :align: center 
    
    Fig 1: Copy/paste data panel to anothe project
    
41. Select the **Save** icon on the **Tool bar** of the main application to save all the 
    changes made to the project design for "Optical transmission IM".
    
    *Before running our test simulation, we will need to restart the application to reload 
    the latest versions of the external Python modules, including "config_data_panels.py"* 
    
42. Close the current session of SystemLab|Design by selecting **File/Quit application**.
43. Launch a new application of SystemLab|Design by double left-clicking on the 
    *"SystemLab-Design-1902.exe"* executable file.
44. From the **Menu bar**, select **File/Open project** and re-open the design project 
    *"Optical transmission IM"* (located under *"systemlab_design\\systemlab_examples\\optical\\optical_direct_detection"* ).  
    
**Part 5: Run a simulation to test the operation of the data panels**    
    
45. On the **Tool bar**, select the **Start** button to initiate the simulator. *[Data results 
    should appear in both data panels as shown below.]* 
    
  .. image:: Data_Panel_5.png
    :align: center    
    
46. We see that the data results for the **Receiver Analysis** panel are exceeding the panel's 
    dimensions. To adjust the panel's dimension settings, double left-click to open its 
    properties and update the following data fields:
    
    a. Under **Title section (box settings)** set **Dimensions (w)** to "200".
    b. Under **Data section (box settings)** set **Dimensions (w)** to "200" and 
       **Dimensions (h)** to "80".
    c. Under **Data section (field settings)** set **Data field width** to "140" and 
       **Value field width** to "50".
    d. Select **OK** to save all changes and to close the dialog.
       
  .. image:: Data_Panel_6.png
    :align: center  
    :width: 500  
    
47. On the **Tool bar**, select the **Start** button to re-run the simulator. *[The data panel 
    dimensions should now be aligned with the results!]*   

  .. image:: Data_Panel_7.png
    :align: center   
    
**This completes the tutorial on how to add data panels to a design!**  