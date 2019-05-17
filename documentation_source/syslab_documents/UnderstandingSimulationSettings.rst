.. _simulation-settings-label:

Understanding simulation settings
=================================

Sample rate, Simulation time & Symbol rate
------------------------------------------

The primary simulation settings for a project are defined within the 
**Project settings/Simulation settings** tab. The **Number of iterations** (when performing 
parameter sweeping or repeating test runs) can be defined here, along with the sampling 
requirements for our simulation.

SystemLab|Design is designed primarily for block sequence simulation. All signals are 
stored as time-based, sampled signals to allow for the ability to access instantaneous 
values of a signal based on its time point in the simulation (also called 
`discrete-time signals <https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem>`_). 
To achieve this, a **Sample rate** and **Simulation time** must be defined for 
the entire simulation.

The **Sample rate** defines how many samples we wish to capture per second within the simulation 
window and is generally set to the Nyquist rate (twice the value of the highest frequency 
component we want to capture in representing an analog signal). When multiplied by the 
**Simulation time** we obtain the **Total samples** that will be required for our 
simulation. This number should be closely monitored as it is used by all the functional 
blocks to manage the input and output sizes of arrays, which in turn affects the time to 
perform calculations and visualize data!

  .. note::
   When running simulations which contain a very large number of data samples (1e6 or higher), 
   it is recommended to disable (uncheck) the **Save port data** check box in the **Tool bar**. 
   This will improve the simulation performance and reduce memory loading linked to populating 
   arrays for all data ports in the design. 

Another parameter that can be set in the project simulation settings is the **Symbol rate**. 
This parameter is useful when analyzing digital communications systems. These types of 
systems are generally defined by the transport of symbol blocks (representing a binary 
data collection) and operate at defined symbols/sec rate(s) (also called 
`baud rate <https://www.electronicdesign.com/communications/what-s-difference-between-bit-rate-and-baud-rate>`_). 

The **Symbol rate** is defined separately from the **Sample rate** but as a general rule, 
when running communications models, it’s recommended to maintain a **Sample rate** that is 
twice or greater than that of the **Symbol rate**.

  .. figure:: Simulation_Settings_1.png
    :figclass: align-center
    
    Fig 1: Main settings group for running a simulation. Key elements include the **Number 
    of iterations**, the **Sample rate**, the **Simulation time** and the **Symbol rate**
    
Confirming simulation settings with a signal data analyzer
----------------------------------------------------------

The following example **Electrical signal data analyzer** views (for a sampled electrical pulse 
stream) can be used to verify our simulation settings.

In the time-domain graph (Fig 2), the blue dots represent the sampled data points as a 
function of time. The separation between these samples is equivalent to the **Sample period** 
calculation (1E-11 sec) from the **Simulation settings** tab.

  .. figure:: Simulation_Settings_2.png
    :figclass: align-center
    :width: 450
    
    Fig 2: Example view of Time data tab (Electrical signal data viewer)

The inverse of the **Sample period** is the **Sample rate** (set to 1E+11 Hz) and is 
equivalent to the spacing between the data points in the frequency-domain graph (Fig 3).

  .. figure:: Simulation_Settings_3.png
    :figclass: align-center
    :width: 450  
        
    Fig 3: Example view of Frequency data tab (Electrical signal data viewer)

  .. note::
    Information on the simulator settings can also be found in the upper left corner of the 
    **Time data** tab (Total samples, Sample period, Time window) and **Frequency data** tab 
    (Total samples, Sample rate) of a signal data analyzer.

Feedback settings
-----------------

SystemLab|Design also has a feature for performing the dynamic analysis of systems. 
When **Enable feedback** is selected, SystemLab|Design will divide the **Simulation time** into 
**Feedback segments**. Each segment represents a shorter-time simulation that is run just like 
a normal simulation. These subsets are then concatenated together to complete a full 
picture of system performance over the defined time window of the simulation. 

This flexibility allows for output signals from downstream functional blocks to be used 
as inputs to upstream functional blocks (feedback loops). The resolution of the feedback 
system can be changed by increasing the number of segments. For further details on how to 
run simulations with feedback, see :ref:`feedback-label`.

  .. figure:: Simulation_Settings_4.png
    :figclass: align-center
    :width: 450  
    
    Fig 4: Feedback settings group (located under **Simulation settings** tab of **Project settings**)

