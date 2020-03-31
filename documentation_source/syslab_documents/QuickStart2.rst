
Quick start 2: How to setup iterations for a simulation
=======================================================

In the following quick start tutorial, we will setup a basic simulation that 
runs multiple iterations (each time changing the input parameters for a functional block).

**Part 1: Drag and drop the required components onto the design layout**

1.  Launch a new application of SystemLab|Design by double left-clicking on the *SystemLab-Design.exe* 
    executable file.
2.  Go to the **Functional block library** (left panel of GUI) and hover over the triangle
    in front of the *Waveform generators* group (under **Electrical**).
3.  Left-click mouse to expand the menu.
4.  Left-click select and hold over the **Sine Generator** component and start moving
    your mouse towards the design scene for Project_1.
5.  Release the mouse button anywhere over the design layout.     
    *[An icon representing a sinusoidal signal generator should appear on the layout]*.                

  .. image:: Quick_Start_1A.png
     :align: center

**Part 2: Setup the functional block script to update its parameters for each iteration**

6.  On the design layout (Project_1), double left-click on the **Sine** functional block. 
    *[The Functional block properties dialog will open]*.
7.  Next to the **Script module name** click on the **Edit Script** button.
    *[The Functional block script editor associated with the Sine Generator will open]*.
    
  .. image:: Quick_Start_1B.png
     :align: center
     :width: 400px

8.  On line 27 of the *Sine_Generator* script, comment out the current *freq*
    parameter definition and add the following new lines of code as shown below.
        
    *[The variable "iteration" is linked to the current iteration for the simulator (an 
    integer value of 1, 2, 3, ...n where n is the total number of iterations). For each 
    iteration, the "freq" parameter of the Sine Generator will be increased 
    based on the iteration value times the base frequency of 10 GHz]*
    
    ::
    
        '''==INPUT PARAMETERS=================='''
        #freq = float(parameters_input[0][1]) #Hz
        freq = iteration*10e9
        signal_amp = float(parameters_input[1][1]) #Peak amplitude (crest-to-crest = 2*Peak amplitude)
        bias = float(parameters_input[2][1])
        
9.  On line 46 of the *Sine_Generator* script, add two new lines of code just below
    *signal_gen_results = [ ]* as follows: ::
    
        '''==RESULTS===================================================='''
        signal_gen_results = []
        freq_result = ['Generator frequency', freq*1e-9, 'GHz', ' ', False]
        signal_gen_results = [freq_result]

10. Click on the **Save** icon in the **Tool Bar** to save all the changes.
11. Close the SciTE dialog (**File/Exit**)
12. Select **OK** to close the **Functional block properties** dialog.

**Part 3: Setup the desired number of iterations and run a simulation**

13. Select the **Settings** icon on the on the **Tool bar**, and within the **Simulation
    settings** tab of the **Project settings** dialog, change the **Number of iterations**
    from 1 to 5 (as shown below).

  .. image:: Quick_Start_1D.png
     :align: center
     :width: 400px

14. Select **OK** to save and close the **Project settings** dialog.
15. From the **Tool bar**, click on the blue **Start** button (blue triangle) to launch the 
    simulator. *[The Simulation status dialog should indicate that all iterations (in this
    case five) were successfully completed!]*.
16. Double left-click on the output port of the Sine generator to open the **Electrical signal data 
    analyzer** and select the **Frequency data** tab.
17. Within the **Iterations** group box you will see that the **Current** iteration spin box is
    set to "1". To change the current iteration, click on upper arrow of the spin box to increase the 
    iteration index to "2" and continue until reaching "5".
    
    *As shown in the images below (showing iteration 1 and 5) the signal data will be refreshed to reflect the current saved iteration 
    for the simulation. As designed, we see that the frequency increases from its start point of 10 GHz all 
    the way to 50 GHz. After a simulation, the signal data for all calculated ports in a design are saved 
    to data dictionaries and can be accessed through via the Iterations spin boxes located within each 
    tab of a port data viewer.*
    
  .. image:: Quick_Start_1X.png
     :align: center
     :width: 400px    

18. It is also possible to change iterations by clicking on the spin box located on
    the upper right of the main application window. Close the **Electrical Signal Data Analyzer**
    and set the current index of the main application **Iteration** spin box to 3 as shown below:
    
  .. image:: Quick_Start_1F.png
     :align: center
     :width: 400px 

 .. note:: 
    The **Iteration** spin box in the main application window is linked to data contained in 
    the functional blocks and data panels - the iteration spin boxes of the signal data viewers 
    operate independently.   

19. Hover your mouse over the **Sine** functional block to view the component status and results.

    *As shown below, the functional block result we created in step 9 is shown for 
    iteration 3 (displaying a frequency of 30 GHz). Using the iteration spin box in the upper right
    of the main application window, results from functional blocks and data panels can be analyzed
    quickly over all iterations. Similarly, by hovering over signal ports, signal metrics data can 
    be viewed for the selected iteration (see second figure below)*
    
  .. image:: Quick_Start_1Y.png
     :align: center
     :width: 300px      
    
    
    
    
    
    