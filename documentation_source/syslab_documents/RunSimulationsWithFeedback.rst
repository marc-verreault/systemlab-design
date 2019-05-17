.. _feedback-label:

Running simulations with feedback
=================================

In the following tutorial we will review the dynamic systems modeling capabilties of 
SystemLab|Design.

**Open the design project "Newton Law Cooling" and run a simulation with feedback**

1.  Launch a new application of SystemLab|Design by double left-clicking on the 
    *SystemLab-Design.exe* executable file.
2.  From the **Menu bar**, select **File/Open project** and navigate to the folder 
    *"systemlab_design\\systemlab_examples\\feedback\\"*
3.  Select the design project *"Newton Law Cooling"* (it will have a suffix ".slb") and 
    click on the **Open** button.
4.  On the **Tool bar**, select the **Start** button to initiate the simulator. 

    *The simulation will run for a short period of time and results will be displayed as 
    shown in the graph below. The three curves represent the temperature reduction of a stock 
    of pre-heated water that has been left to cool over a period of 100 seconds. The start 
    temperature for each curve is 80, 93.33 and 106.67 C and the ambient temperature is 20 C*.
    
   .. image:: Feedback_1.png
    :align: center 
    :width: 450

5. Double left-click on **Flow-Cooling** to open its functional block properties and 
   select the **Ports Manager** tab.
   
   *To build a feedback loop in a simulation (between functional blocks), one or more ports 
   must be designated as "In-Feedback". In this example, input port 4 of the "Flow-Cooling" 
   functional block has been set to Direction = "In-Feedback" (see below)*.
   
   .. image:: Feedback_2.png
    :align: center 
    :width: 550 
    
**How feedback segments are processed by a functional block script**

6. Select the **Edit script** icon (next to **Script module name**) to view the script for 
   *"Flow_Cooling"*.
    
   On lines 52-56, the following code is used to initiate the feedback mode of operation: ::
   
        if segment == 1 or feedback_mode == 0: #First iteration of feedback mode simulation
            fdk.temp_sig_out = np.zeros(n)
            feed_temp_in = stock_temp_in
        else:
            feed_temp_in = input_signal_data[2][4] #Use feedback signal
    
   When **Feedback mode** is enabled for a simulation, each simulation iteration will be 
   repeated multiple times based on the project settings parameter **Feedback segments**. 
   Each segment represents a shorter-time simulation that is run just like a normal simulation. 
   These subsets are then concatenated together to form a complete picture of system 
   performance over the defined time window of the simulation. 
   
   For the first simulation segment, there is no return signal available at the "In-Feedback" 
   port of the **Flow-Cooling** as this port has a downstream source (in this case the 
   **Branch** node) and the feedback signal is set to the input stock temperature (the 
   startimg temperature for the simulation). For follow-on segments (else condition), a 
   return signal is available and the signal data from the "In-Feedback" port is used.
   
   On lines 63-74, the following code is used to perform the calculation of the output 
   temperature for a segment: :: 
   
       if feedback_mode == 2:
           segment_length = float(n)/float(segments)
           start_index = int(round(segment * segment_length) - segment_length)
           dT_over_dt = -cooling_rate*(feed_temp_in[start_index] - amb_temp_in[0])
           dT = dT_over_dt * segment_length * t_step
           if config.sim_data_activate == True:
               config.sim_data_view.dataEdit.append('dT:')
               config.sim_data_view.dataEdit.append(str(dT))
           for seg in range(start_index, n):
               fdk.temp_sig_out[seg] = feed_temp_in[seg - int(segment_length)] + dT
       else:
           fdk.temp_sig_out = stock_temp_in
           
   When **Feedback mode** is enabled for a simulation (feedback_mode == 2), the change in 
   temperature for a defined time span is calculated using the differential equation 
   *dT/dt = -k(T-Ta)* where k is the cooling rate parameter and Ta is the ambient temp [1]_.
   
   The **Feedback segments** setting is used to define the number segments for the simulation 
   iteration. This regulates the time step delta (dt), which is represented numerically 
   by the number of samples per segment (as shown in the data field **Samples/seg** under 
   **Project settings/Feedback settings**)           
           
**How to change the feedback settings for a dynamic systems simulation** 

7. Select the **Settings** icon on the **Tool bar** menu to view the **Project settings** 
   for the *"Newton Law Cooling"* design project.
8. Under the Feedback settings tab, change the **Feedback segments** from **100** to **25** 
   and select **OK** to update the settings and close the dialog.
    
  .. image:: Feedback_3.png
     :align: center 
     :width: 450 
   
9. On the **Tool bar**, select the **Start** button to initiate the simulator.
   
   *The simulation curves, as shown below, now map the temperature change over 25 feedback 
   segments (vs 100). This reduces the resolution of the signal information over time but 
   also reduces the overall simulation time.*
   
   .. note::
     The maximum resolution setting for the feedback mode is 1 sample/segment. To increase 
     further the time resolution of a feedback model, simply increase the **Sample rate** 
     setting.  
     
  .. image:: Feedback_4.png
     :align: center 
     :width: 450     
   
.. [1] Other differential equations, https://www.ugrad.math.ubc.ca/coursedoc/math100/notes/diffeqs/cool.html
       (accessed April 26, 2019). 