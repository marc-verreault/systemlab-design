
Create a design project
=======================

In the following procedure, we will create functional blocks and scripts (a waveform 
generator that is connected to an amplifier) and assemble these into a design project folder.

  .. note:: 
    A completed version of this design can be found within the folder 
    *"systemlab_design\\systemlab_examples\\electrical\\gaussian_pulse_generator\\"* 

**Part 1: Create new functional blocks and layout the design**

1.  Launch a new application of SystemLab|Design by double left-clicking on the *SystemLab-Design.exe* 
    executable file.
2.  To create a new functional block, right-click anywhere on the **Project design space**
    and select **Add functional block**. *[A default functional block unit will be added
    to the project scene (Fig 1)]*. 
3.  To start editing the functional block, hover over the item and double left-click to
    open the **Functional block properties** dialog.

  .. figure:: Create_Design_Project_1.png
    :figclass: align-center    
    
    Fig 1: Add a functional block to the project design space
    
4.  To add ports, select the **Ports Manager** tab, and then click on the **Add port(s)** button.

  .. figure:: Create_Design_Project_2.png
    :figclass: align-center   
    :width: 450px   
    
    Fig 2: Functional block properties - Add port(s) action button

5.  From the **Add port(s)** edit dialog, type *'Pulse Sig'* into the Port name field, select 
    Cardinal point: **East**, Direction: **Out** and Signal type: **Electrical**.       
6.  Click on the **Apply** button to perform the port addition *[you will see the port
    details appear within the Ports Manager table]* and then click **Save** to finalize
    the changes.
    
  .. important::
    If the **Add port(s)** dialog is closed without saving, the changes will not be saved 
    to the functional block data model.
    
  .. figure:: Create_Design_Project_3.png
    :figclass: align-center   
    :width: 800px
    
    Fig 3: Functional block properties - Add port(s) dialog
    
7.  Enter *'Pulse Gen (Gaussian)'* in the field **Functional block name/ID** and 
    *'Pulse_Gaussian'*  in the **Script module name** field *[see Fig 3 right-side image]*. 
8.  Select **OK** to save the changes/close the **Functional block properties** for *Pulse Gen (Gaussian)*.  
9.  Right-click on the project design space and select **Add functional block**.
10. Open the **Functional block properties** for the new functional block, go to the **Ports 
    Manager** tab, select **Add port(s)** and create two new ports as follows: 
    
    a. Port name: *'Input'*, Cardinal point: **West**, Direction: **In**, Signal type: **Electrical**
       (remember to click **Apply** before proceeding to enter the data for the 2nd port).
    b. Port name: *'Gain Out'*, Cardinal point: **East**, Direction: **Out**, Signal type: **Electrical**.
    
  .. figure:: Create_Design_Project_3A.png
    :figclass: align-center 
    :width: 500 
    
    Fig 4: Add port(s) dialog for 'Amplifier'
       
11. Select **Apply**, followed by **Save**, to finalize the port changes.

  .. figure:: Create_Design_Project_4.png
    :figclass: align-center  
    :width: 500px 
    
    Fig 5: Functional block properties settings for Amplifier

12. Enter *'Amplifier'* into the **Functional block name/ID** field and *'Electrical_Amplifier_Pulse_Gen'* 
    into the **Script module name** field (see Fig 5).    
13. Select **OK** to save/close the **Functional block properties** dialog.   
14. To create a port link for the design project, perform the following steps:
    
    a. Hover your mouse over the blue (rectangular) output port of the *Pulse Gen (Gaussian)* functional block.
    b. Once you see a cross-hair icon appear, left-click/hold your mouse and move the
       mouse cursor towards the input port of the *Amplifier* functional block.
    c. Once directly over the Input port, release the mouse click *[the completed connection
       (solid line) should appear as shown in Fig 6]*.

  .. figure:: Create_Design_Project_5.png
    :figclass: align-center   
    
    Fig 6: Creating signal links between ports
    
  .. admonition:: About port (signal link) connections...
    
    Only connections from output to input ports are allowed. Also, if the downstream port 
    signal type is different than the upstream port signal type, no connection will be allowed.

    To delete a port signal link, hover directly over the connection and right-click
    select **Delete signal link**. 
    
**Part 3: Create a project folder**   

15. Before saving the project, go to the *systemlab_design* main folder and create a new folder 
    called *'gaussian_pulse_generator'*.
    
  .. warning::
    If the path which defines the location of a Python script contains empty spaces, the 
    file may not be directly accessible to the script editor. It is thus recommended to remove any blank 
    spaces in your project path definitions (this is why we have added underscores to our 
    new project folder).

16. Go to the **Project settings** for our design and enter into the **Project name** field 
    the name *'Gaussian Pulse Gen'*.
17. Within the **File path (project)** field enter the following file path: *'.\\gaussian_pulse_generator\\'*
    and select **OK** to save and close the **Project settings** dialog. 
18. Click on the **Save** icon to save the project file to the new location.

  .. note::
    Check the status bar (bottom of the application window) to confirm that the file was
    correctly saved. It will read as **File saved to: .\\gaussian_pulse_generator\\**
    
  .. important:: 
    Make sure to end the **File path (project)** field with a back slash.
    If there is no back slash, the design file will be saved to the root directory where
    the SystemLab|Design executable is located. The “.” before the design folder 
    represents the project file path for the software application folder. 
    The actual path is displayed in the **Project file path** panel (located also on the 
    bottom **Status bar**)
    
  .. figure:: Create_Design_Project_6.png
    :figclass: align-center   
    :width: 600
    
    Fig 7: Defining the File path for the Pulse Generator project
    
**Part 3: Create functional block scripts**
    
19. Open a session of SciTE by selecting **Edit/Open code/script editor** from the **Menu bar**.
20. From the SciTE dialog, select **File/Open**.
21. Go to the folder *systemlab_design/syslab_fb_scripts* and open the Python module called 
    *Script template V1 5-Mar-19.py*.  
    
  .. image:: Create_Design_Project_6A.png
    :align: center   
       
22. Save the script module as *'Pulse_Gaussian'* within our project folder *gaussian_pulse_generator*. 
23. Below "import config", add the following line: *[This action imports the SciPy 
    application package for signal processing]* ::
       
       from scipy import signal
    
24. Under the CALCULATIONS section, enter the following five lines of code: ::
    
       carrier = 0
       sig_type_out = 'Electrical'
       time_array = np.linspace(0, time, n)
       sig_array = signal.gausspulse(time_array, fc=10)
       noise_array = np.zeros(n)
       
  .. admonition:: How the signal arrays are built...
    
      In the code above we have defined a time line based on the **Project settings** *'time_window'*
      (duration of simulation in sec) and the number of samples (n) defined for the
      simulation (*'num_samples'*). These parameters are retrieved under the 'PROJECT SETTINGS' section 
      of the functional block script (see Fig 8). As this functional block is a source 
      (there are no input ports), we need to internally build the time array from these parameters. 
    
      The *Gaussian pulse generator* is based on the Scipy function (signal.gausspulse) for
      a Gaussian modulated sinusoid. The parameter **fc**, defines the center frequency for the
      pulse. The time_array defines the time-points (x-axis) to be used to build the Gaussian 
      pulse. Details on this feature can be found at: `scipy.signal.gausspulse <https://docs.scipy.org/doc/
      scipy/reference/generated/scipy.signal.gausspulse.html#scipy.signal.gausspulse>`_ 
      
  .. figure:: Create_Design_Project_7.png
    :figclass: align-center  
    :width: 400
    
    Fig 8: Portion of functional block script for Pulse_Gaussian (SciTE editor)
    
25. Under the "RETURN (Output Signals, Parameters, Results)" section, 
    uncomment the line of code immediately below the "ELECTRICAL" header (delete the 
    hash tag symbol on the line to uncomment) and update as follows: ::
    
       electrical_out = [1, sig_type_out, carrier, fs, time_array, sig_array, noise_array]
       
26. Uncomment the very last line of the script (starts with "return") and update as follows: ::
    
       return ([electrical_out], script_parameters, script_results)
    
  .. important::
  
    Make sure that the indentation matches the image of the script code as shown in Fig 9 below! 
    The spaces are shown within the code as small black dots. In Python, between indentations, 
    there are normally 4-8 spaces (in the example here we are using a 4-space convention).

    In Fig 9 (below) we have defined a return signal (electrical_out) which defines
    the output electrical data list that will be allocated to port ID 1. It is important
    to match the port ID defined in the script with the destination port ID that is
    defined in the functional block properties (the port ID can be verified by hovering
    over the destination output port with the design layout).
    
  .. figure:: Create_Design_Project_8.png
    :align: center
    :width: 600
    
    Fig 9: Portion of functional block script for Pulse_Gaussian (SciTE editor)   
        
27. Save all the changes made to the script *Pulse_Gaussian.py*.
28. Open the **Settings** dialog (from the **Tool bar**).
29. Under the **Simulation settings** tab, set the **Sample rate** to 200 and the **Simulation time**
    to 1 sec. 
30. Click on the **Apply** button. 
    
    *The Sample period, Total samples, and Samples/sym fields will be re-calculated 
    to match the new simulation settings. Also, the Sample rate and Simulation time 
    will be reformatted into exponential format (2.0000E+02 and 1.0000E+00)*.
    
  .. image:: Create_Design_Project_9.png
    :align: center
    :width: 400
    
31. Select the **OK** button to close the Settings dialog.     
32. Click on the **Start** button in the **Menu bar**.

    *The simulation status dialog will indicate that there was an error processing the
    Amplifier block (this is expected as we have not yet defined the script for the
    amplifier) however we should be able to confirm that the Pulse Gen (Gaussian) block
    ran successfully*.
   
  .. image:: Create_Design_Project_10.png
    :align: center 
    :width: 400   
    
33. To verify that we have a Gaussian pulse signal, hover over the output port of the
    *Pulse Gen (Gaussian)* functional block and double left-click your mouse to open the
    **Electrical signal data analyzer** dialog.
    
    *From the Time data tab (which plots electrical signal & noise arrays as a function of 
    the sampled time) we can see that the Gaussian pulse was successfully built by the 
    script routine*.  
    
  .. image:: Create_Design_Project_11.png
    :align: center   
    :width: 500px   
           
34. To verify the frequency domain signal, select the **Frequency data** tab.

    *As designed, the center frequency of the spectral profile of the Gaussian pulse is 
    confirmed to be 10 Hz!*
    
  .. image:: Create_Design_Project_12.png
    :align: center  
    :width: 500px     

35. Return to the SciTE editor dialog for the script module *Pulse_Gaussian*, select **File/Save As**, 
    and save the script under the new name *'Electrical_Amplifier_Pulse_Gen'*.
36. Update the new script as follows:
    
    Under the "INPUT PARAMETERS" section, add the line: ::
    
       gain_db = float(parameters_input[0][1])
    
    Under the "INPUT SIGNALS" section, add the lines: ::
   
       time_in = input_signal_data[0][4]
       sig_in = input_signal_data[0][5]
       
    Under the "CALCULATIONS" section, update the existing lines to the following: ::
      
       carrier = 0
       sig_type_out = 'Electrical'
       sig_array = sig_in*np.power(10, gain_db/20)
       noise_array = np.zeros(n)
       
  .. image:: Create_Design_Project_13.png
    :align: center 
    :width: 400 
    
37. Save all changes made to the script *Electrical_Amplifier_Pulse_Gen.py* and open the
    **Functional block settings** dialog for the *Amplifier* functional block.
38. Add to the first row of the **Input parameters** table the following settings:
    
    a. Parameter name: **Gain**, Value: **3**, and Units: **dB**.
    
  .. image:: Create_Design_Project_14.png
    :align: center 
    :width: 400px 
    
39. Select **OK** to save and close the **Functional block settings** dialog.
40. Click on the **Start** button in the **Tool bar** to re-run the simulation.
    
    *The simulation status dialog will indicate that there was an error processing
    the Amplifier block. An alarm was raised indicating that we have tried to allocate
    output signal data to an input port*.
    
  .. image:: Create_Design_Project_15.png
    :align: center 
    :width: 400px     
    
41. To fix this issue, return to the SciTE editor window for the script *Electrical_Amplifer_Pulse_Gen.py*
    and, under the "RETURN (Output Signals, Parameters, Results)" section, change the
    port ID field from **1** to **2**: ::
    
        electrical_out = [2, sig_type_out, carrier, fs, time_array, sig_array, noise_array]
        
**Part 4: Run the final simulation**
        
42. Click on the **Start** button in the **Tool bar** to re-run the simulation. *[The simulation should 
    now have completed with no issues!]* 
43. To verify that we have applied a gain to the input signal, hover over the output port 
    (filled blue box) of the *Amplifier* functional block and double left-click your mouse 
    to open the **Electrical signal data analyzer** dialog.
44. Within the **Signal type** group  (located in the left panel of the **Time data** tab), 
    change the y-axis unit from **Mag** to **Watts**. *[The peak signal level should read 2 Watts]*.
    
  .. image:: Create_Design_Project_16.png
    :align: center  
    :width: 500
         
45. Verify the input signal by hovering over the input port of the *Amplifier* functional
    block, double left-clicking and within the **Signal type** group, changing the y-axis unit
    from **Mag** to **Watts**.
    
    *The peak signal for the input pulse should read 1 Watt, thus confirming the 3 dB
    power gain setting for the Amplifier functional block*. 
    
  .. image:: Create_Design_Project_17.png
    :align: center 
    :width: 500
    
**This completes the tutorial for Creating the first design project!**
