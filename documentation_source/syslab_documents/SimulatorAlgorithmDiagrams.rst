
Simulator algorithm flow diagrams
=================================

.. _main-simulator-label:

Main simulation algorithm
-------------------------

The flow diagram for the main simulation algorithm is shown in Fig 1. 

Upon initiating a simulation run, all functional blocks for the design layout are retrieved 
and their calculation status flags are reset. 

The main simulation loop (box with dotted lines) is called for every iteration and 
stays in a **while True** loop until all functional blocks have been calculated or cannot 
be calculated after several attempts (for example if an input port has not been connected 
to an upstream port). 

After the main simulation loop has been completed, data tables (when set) for the iteration 
are saved and updated, and the simulation algorithm proceeds to perform the next iteration 
(or exits if the final iteration has been completed).

  .. figure:: Main_Simulation_Loop.png
    :figclass: align-center
    
    Fig 1: SystemLab|Design main simulation algorithm

fb_script method
----------------

The flow diagram for the **fb_script** method is shown in Fig 2. 

When a functional block is ready for calculation, the **fb_script** method is called. 
First, the input port signals data arrays, design settings and parameters list are retrieved 
and the Python script associated with the functional block is loaded. The run method of the 
script module is then called, and once complete, returns the output signal data arrays, 
modified parameters and output data results. 

The output port signals data, functional block parameters, and output results are then saved 
to their respective iterations dictionaries so that they can be accessed for post-simulation 
analysis. 


  .. figure:: Functional_Block_Script.png
    :figclass: align-center  
     
    Fig 2: Functional block script (fb_script method)