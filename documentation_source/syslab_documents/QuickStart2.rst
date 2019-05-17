.. _quick-start-2-label:

Quick start 2: Run an example model with iterations
===================================================

In the following quick start tutorial, we will open an existing example design that includes
iterations, data panels, and customized graphs.

1.  Launch a new application of SystemLab|Design by double left-clicking on the 
    *SystemLab-Design.exe* executable file.
2.  From the **Menu bar**, select **File/Open project** and go to the folder 
    *systemlab_design\\systemlab_examples\\electrical\\qpsk_design*
3.  Select the design project *QPSK Design* (it will have a suffix ".slb") and 
    click on the **Open** button. *[The QPSK design example should appear as shown below]*
    
  .. image:: Quick_Start_2_1.png
    :align: center

4.  Click the **Start** button (blue triangle) on the **Tool bar** to start the simulation.

    *The simulation will run for 12 iterations and should take 1-2 minutes to complete. During 
    the simulation a waterfall graph viewer (Fig 2) will be instantiated and updated after each iteration 
    (plotting symbol error rate (SER) as a function of signal to noise ratio per symbol (SNR/sym)).    
    After the simulation is complete, you will also see a customized graph that displays 
    the IQ signal space results for the simulation (Fig 3). Both of these types of graphs are commonly 
    used when analyzing higher order digital modulation systems such as quadrature phase shift 
    keying.*
    
  .. figure:: Quick_Start_2_1A.png
    :figclass: align-center
    :width: 550
    
    Fig 2: Simulation results viewer (SER Results QPSK)
     
5.  Minimize the **SER results QPSK** graph by selecting the **Minimize** icon on the upper 
    right corner of the graph viewer.
6.  On the **Signal space analyzer** viewer, hover your mouse over the spin box that is located 
    in the **Iterations** group box (Fig 3) and left-click a few times to change the **Current** 
    iteration setting.
    
      .. figure:: Quick_Start_2_2.png
        :figclass: align-center
        :width: 450
    
        Fig 3: Signal space analyzer (customized viewer) for QPSK design 
    
    *As the iteration index increases you will notice the improvement in the resolution of the 
    IQ constellations (iteration 12 is shown in Fig 3) - for the simulation we have linked the 
    iteration number value to the signal to noise ratio (see example code in Fig 4), thus 
    reducing the noise loading as the iteration number increases.*
    
      .. figure:: Quick_Start_2_1B.png
        :figclass: align-center
        :width: 550
    
        Fig 4: Python script code that is used to calculate the SNR per symbol parameter (located 
        in NRZ_Gen_I.py) 
      
    *Customized graphs such as these are built from the "systemlab_viewers.py" Python module 
    (located within systemlab_design\\syslab_config_files). During the QPSK simulation, instances 
    of these graphing objects are first declared within the functional block script for the 
    "Decision Analyzer". These graph views are then populated with data results from 
    dictionaries that are built as the simulation progresses.* 
    
7.  Taking a closer look at the project design space, you will notice that there are 
    three panels (all with a yellow background) on the design that are not connected to any functional 
    blocks. These are called **Data panels** and are specialized data objects designed to present 
    numerical data originating from any of the functional blocks in your design. For the QPSK 
    design there are data panels for *Impairment metrics*, *Decision Results* and *BER Results*. 
    In the upper right corner of the SystemLab|Design application, you will see a spin box 
    called **Iteration** (Fig 1). Like the **Signal space analyzer**, left-click on the 
    spin box to decrease or increase the iteration number.
    
    *As the iteration index changes you will notice that the "Data panel" results are updated 
    accordingly. The logic is the same as for the customized viewers. Python dictionaries
    are populated with numerical results during each simulation iteration and are accessed 
    by the "Data panel" objects and in turn displayed in the project design space. Data panels can 
    be viewed as "virtual test instruments" and are useful for presenting or highlighting 
    specific results, validating calculations or analyzing performance trends based on changing 
    input conditions.*
    
  .. admonition:: About Python dictionaries...
    
    `Dictionaries <https://www.w3schools.com/python/python_dictionaries.asp>`_ are powerful Python 
    composite data types used for managing collections of objects. In the SystemLab|Design 
    architecture they are used frequently, including tracking data results that are associated 
    with an iteration. 
    
    They are built using a key-element combination. Duing simulations, dictionaries are populated 
    with a key (the iteration #) and an associated data element (usually a list) that contains 
    signal data arrays, results, parameters, text data, etc. When a specific iteration # is requested, 
    for example when there is a change in the spin box setting for a signal data viewer, the associated 
    data object/list is accessed for processing. Dictionary entries can be grown or shrunk, making 
    it an excellent tool for saving and tracking data when the size of the data collection is 
    not known in advance.
    
8.  In addition to customized graphs and data panels, the sampled signal data for all ports 
    (and iterations) are held in memory for post-simulation analysis. For example, let's take 
    a look at the output port for the integrate & dump functional block. Hover your mouse over the 
    dark blue port of the **I&D (I)** functional block and double left-click to access the 
    **Electrical signal data analyzer** dialog. 
9.  There's a lot of sampled data in our simulation so we will take a look at a smaller 
    segment of the simulation data. One way to do this is to use the zoom feature (magnifying glass) 
    located on the navigation tool bar just below the graph. We will use another method 
    by defining the start and end values for the x-axis and y-axis. On the left panel of the **Time 
    data** tab, enter the numbers "0" and "1e-8" in the respective data fields for **Time (min)** and 
    **Time (max)** (these fields are located within the **Time axis min/max settings** 
    group box). Once these settings have been entered, select the **Apply** button at the 
    bottom of the group box.
10. Under the **Y-axis min/max settings** group box, set the **Start value** and **End value** 
to "100" and "-100" and select **Apply**. 
    
    *The graph will be refreshed and should look similar to the plot shown in Fig 5. 
    The Integrate and Dump receiver is called a matched filter in that it is designed to provide 
    the optimum signal to noise ratio condition prior to making a decision on the received 
    sampled symbol data (all received samples for a given symbol period are first added together 
    and then at the last sample point the data is dumped and re-set before starting to integrate the next 
    set of sampled received data - hence the saw tooth look of the received sampled data set). 
    Like the customized viewers, the sampled data for each iteration can be accessed 
    for this port by adjusting the spin box setting of the "Current" data field within the 
    "Iteration" group box.*
    
    *Please note that when changing the iteration number, the entire sampled 
    data set will be re-plotted for the specified iteration. To refocus the plotting region 
    (after changing an iteration setting), re-select the "Apply" buttons at the bottom of 
    the "Y-axis min/max settings" and "Time axis min/max settings" group boxes.* 
    
  .. figure:: Quick_Start_2_3.png
    :figclass: align-center
    
    Fig 5: Electrical signal data analyzer view for output of I&D (I) - QPSK Design
  
**In this tutorial we have reviewed the iterations feature of SystemLab|Design and how 
it can be applied towards building customized graphs and displaying performance trends 
with data panels.**
    
For more information on building customized graphs see :ref:`customized-graphs-label`
    
    
