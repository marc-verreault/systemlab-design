
Working with Functional block scripts 
=====================================

How functional block scripts work
---------------------------------

The primary working unit of SystemLab|Design is the functional block (fb) script. Written
in Python, these scripts can be used to emulate a wide variety of virtual system functions.
All fb scripts must be written using the same input and output rules as defined through
a generic **run** method (called during the simulation routine).

  .. figure:: Functional_Block_Scripts_1.png
    :figclass: align-center  
    :width: 550px
    
    Fig 1: The fb script **run** method

The fb script first retrieves the **input_signals_data** list (from the fb input port(s) - when available), 
the **parameters_input** list and the **settings** dictionary for the simulation. 
Calculations are then performed on the data set and are formatted to be returned to the 
simulation routine in the form of output signal data array lists (**signals_data** - to be allocated to 
output ports, when needed), **results** and an updated **parameters** list (if needed).

Within the fb script, external modules can also be imported (project modules) to allow for
sharing and updating of data between functional blocks or to populate data panels and/or
build customized graphs & viewers.

  .. figure:: Functional_Block_Scripts_2.png
    :figclass: align-center  
    
    Fig 2: How functional block scripts work

Linking functional blocks to a script module
--------------------------------------------

It is important to ensure that every block in the design is linked to a valid script name
and location (the simulator performs checks for this and will stop the simulation and
issue an error message when a script name and path cannot be found).

The script name can be defined and edited by double left-clicking on the functional block
to access its properties menu. 

  .. image:: Functional_Block_Scripts_3.png
    :align: center
    :width: 400px
    
Also, to quickly confirm which script is being used, hover your mouse over any functional
block and a pop-up menu will display the script name associated with the fb. 

  .. image:: Functional_Block_Scripts_4.png
    :align: center
    :width: 300px

To find the script during a simulation, the **run_fb_script** method first searches in the
folders *syslab_fb_scripts/digital*, *syslab_fb_scripts/electrical* and *syslab_fb_scripts/optical*.
These folders house all the default (baseline) scripts and are linked to the **Functional
block library** on the left menu panel (this is where you can drag and drop pre-defined
components).

If the script cannot be found in these folders, then the **run_fb_script** method will check
the file paths that are defined in the **Project settings** for the design. These can be
accessed by selecting the **Settings** icon on the **Tool bar**. The dot (.) before
the first back slash references the current root directory where the application is running.
The second field can be used to specify another search folder location but can be left blank.

  .. important::
    If a design file/folder is created or moved outside of the main root folder (*systemlab_design*),
    the full path directory must be specified (C:\\user\\folder1\\).
    
  .. image:: Functional_Block_Scripts_5.png
    :align: center
    :width: 350px

Script files can be accessed, viewed and edited through SciTE (included by default with SystemLab|Design),
IDLE (Python’s Integrated Development and Learning Environment), or any other compatible
code reader (such as Notepad++). The editor can be launched directly from the
SystemLab|Design GUI (either from **Open code/script editor** in the **Menu bar**),
or from any of the **Functional block properties** dialogs (located next to the 
**Script module name** field).

Each script is structured as follows:

   The "PROJECT SETTINGS" section is where the global simulation settings are accessed
   (the **settings** input list is the source)

   The "INPUT PARAMETERS" section is where the **parameters_input** list is accessed (when
   parameters are defined in the properties panel) or where additional local parameters 
   can be defined.
   
   The "INPUT SIGNALS" section is where the “input_signals_data” list of data arrays
   information is accessed (this applies only to components with input ports).
   
   Data manipulation and other calculations/algorithms are performed within the
   "CALCULATIONS" section.
   
   Once calculations are complete, we prepare the data to be returned to the main
   simulation routine. The "RESULTS" section is where locally calculated results are
   exported to the **Output data** panel of the functional block and the "RETURN" section is
   where  output signals are formatted, along with the **results** list and the output
   parameters (if being overwritten), to be returned to the **run_fb_script** routine

  .. figure:: Functional_Block_Scripts_6.png
    :width: 450px
    :alt: Example fb_script viewed within Python IDLE
    :figclass: align-center
    
    Fig 3: Example fb_script viewed within Python IDLE 
    
    
    
    
