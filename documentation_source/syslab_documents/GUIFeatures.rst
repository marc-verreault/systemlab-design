.. _gui-features-label:

GUI features overview
=====================

Main application interface
--------------------------

All system design projects can be built, managed, simulated and analyzed through SystemLab|Design's
main application interface (Fig 1) and includes the following main components.

  The **Functional block library** tree menu; where pre-defined components, devices or 
  subsystems can be quickly dragged & dropped onto any open project design space. New 
  functional blocks or modified/custom versions of existing ones can be added as needed to 
  this folder (in addition, using the *config_fb_library.py* module, the menu tree can be
  restructured as needed).

  The **Project design space**; where system building blocks can be created, assembled,
  interconnected and analyzed. Multiple projects can be opened simultaneously
  and are saved in binary format (using Python's **pickle** feature).
  
  The **Tool bar** feature which includes shortcut buttons and panels for managing your projects,
  setting up and running simulations, viewing your design project's global settings and 
  a status panel which provides information on the progress of a simulation.

  The **Menu bar** which includes **File** management functions, **Edit** features for copying
  and deleting project items, **Project** menu which can be used to add new items to a 
  design space, **Simulation** menu for starting, pausing or stopping simulations, and 
  **Help** menu which includes access to the on-line documentation portal.

  The **Status bar** which provides additional information on your projects, including
  **Info/Status**, **Project file path** and **Zoom** settings.

  .. figure:: GUI_Overview.png
    :align: center
    :alt: Fig 1: SystemLab|Design main application interface
    :figclass: align-center
    
    Fig 1: SystemLab|Design main application interface

Project settings dialog
----------------------------------

The **Project settings** dialog is where you can set and manage your design project attributes. 
It includes properties tabs for defining your simulation settings, project layout attributes, 
and advanced settings. 

  .. admonition:: How to access the Project properties dialog...
     
     To access the **Project properties** dialog, select the **Settings** icon on the Tool 
     bar or right-click and select **Project layout and settings** anywhere on the project 
     design space.
     
  .. note:: 
  
     For details on how to setup the simulation settings see :ref:`simulation-settings-label`.
     
  .. figure:: GUI_Project_Settings_1.png
    :align: center
    :figclass: align-center
    
    Fig 2: SystemLab|Design project settings dialog
     
At the top of the **Project settings** dialog you will find the input fields for **Project name**, 
**File path (project)**, and **File path (additional)**. 

    The **Project name** defines the name of your project and is the name that will be used if you 
    select **File/Save project** (you can save the project under a different name using 
    **File/Save project as...**).

    The **File path (project)** edit field is used to define the folder location where your design 
    project will be saved. If it is empty, the current working directory (*systemlab_design*) 
    will be used. This path is also used to search for the location of your scripts. If empty, 
    the application searches for the script module(s) within the current working directory. 
    
    The **File path (additional)** edit field can be used to define an additional file path 
    for locating your project scripts. During a simulation, the script file will be first be 
    searched for using the functional block library config file settings, followed by 
    **File path (project)**, and finally **File path (additional)**.
    
From the **Project layout settings** tab you can change the size of your project space (defined in 
pixels) and add a border by selecting the **Show border** check box. It is also possible to 
add a grid layout to the project design space by selecting the **Enable grid** check box. 
The size of the grid, line color and style can be modified as needed.

From the **Advanced settings** you can set the **Max number of calculation attempts** and the 
**Code/script editor command line path**. The latter allows you to select the editor to be 
used for opening and editing Python scripts (for further information on this setting, select 
the **Help** button next to the edit field).
    
Functional block properties dialog
----------------------------------

The **Functional block properties** dialog is the main interface from where you can create 
and manage your system's functional blocks and subsystems. It contains several properties 
tabs which are described in this section.

  .. admonition:: How to access the Functional block properties dialog...
     
     To access the **Functional block properties** dialog, hover over any functional block and 
     double left-click.

Functional block properties: Main settings, dimensions, text settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The upper portion of the **Functional block properties** dialog includes tabs for the 
**Functional block main settings**, **Functional block dimensions and colors** and 
**Functional block text settings**.

  .. figure:: GUI_Functional_Block_1.png
    :figclass: align-center
    
    Fig 3: Functional block overview (upper section)

**Functional block main settings**

The **Functional block main settings** tab is where the **Functional block name/ID** and **Script module 
name** are defined. By default the functional block title is displayed with the functional block 
item in the project design space. The functional block name display can be disabled by 
un-checking the **Display fb name** check box.

  .. admonition:: About functional block IDs...
     
     Functional blocks are managed internally by the software through the allocation of 
     functional block IDs (integer list). Each time a new functional block is added to a 
     design project space, it is provided with a unique ID (as shown in the 
     **Functional block name/ID** field). If a functional block is deleted, its ID is also deleted, 
     and is re-allocated later when another functional block is created (or an existing functional 
     block is copied). The process is automated and does not require any further actions 
     from the user.

An icon can also be added to the functional block item. Icon vector images are located under
*systemlab_main\\syslab_fb_icons*. The name of the associated icon file can be added to the 
**File name** data field and is displayed when the **Display icon** check box is checked. Also, 
the position of the icon, relative to the origin of the functional block, can be set in the 
**Pos(x/y)** field.

  .. note::
    The x-y origin of the functional block is defined as the upper left corner of the 
    rectangular image that represents the functional block. For example, if **Pos(x/y)** is 
    set to (0,0), the vector icon image will start to be drawn from the upper left corner of 
    the functional block image (unless an offset has been applied in the icon script)
    
  .. figure:: GUI_Functional_Block_1A.png
    :figclass: align-center
    :width: 300
    
    Fig 4: Example view of functional blocks that have icons. 

**Functional block dimensions and colors**

The **Functional block dimensions and colors** tab is where the dimensions of the functional block's 
rectangular image can be set, along with the fill color for the rectangle and the border 
settings. The functional block dimensions can also be set by right-clicking on the 
functional block image and selecting **Resize dimensions of functional block**.

**Functional block text settings**

The **Functional block text settings** tab is where the font size, style, color and position 
of the functional block title can be adjusted. In addition, the font size, style and color 
of the port name labels can be set within this tab. 

Functional block properties: Parameters, Ports Manager, Output Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The lower section of the **Functional block properties** dialog includes tabs for the 
**Input parameters**, **Ports manager** and **Output Data**.

**Input parameters**

The **Input parameters** tab is where the input parameters associated with the functional block 
script can be defined and updated. The **Parameter name**, its **Value**, the associated **Units** and 
**Notes** (explaining further the parameter's role) can be added to this table. The process for creating 
parameters is manual (to provide full flexibility) but includes several utility and convenience 
features on the right side of the table (see Fig 5). These include:

*  An **Insert row** function for adding new empty rows above a selected row in the table.
*  A **Delete row** function for deleting a selected row and its associated contents.
*  A **Copy row** function which saves all data contained within a selected row.
*  A **Paste row** function which replace all contents of a selected row with data saved 
   from a previous **Copy row** operation.
*  A **Move row up** function which moves a selected row up by one position on the list.
*  A **Move row down** function which moves a selected row down by one position on the list.
*  An **Insert header** function which adds a full width title header to the parameters list 
   (this is useful when wanting to divide your parameters into different functional groups).
*  An **Add list** function which creates a drop down list based on the information provided 
   in the **Notes** field.
*  An **Add check box** function which converts a **Value** field into a check box (this operation 
   only works if a **Value** field cell has been selected in the parameters table).
*  An **Update-Save table** function which aligns the column widths based on their contents 
   and saves the table contents to the functional block data model.

An example of an **Input parameters** table for a PIN/APD detector model is shown in Fig 5. 
All these settings are saved with the component and can be updated or re-organized as needed 
using the **Row operations** and **Other operations** group functions.

  .. figure:: GUI_Functional_Block_3.png
    :figclass: align-center
    :width: 500
    
    Fig 5: Functional block parameters table (example shown for PIN/APD detector model)

**Ports manager**

The **Ports manager** tab is where the ports associated with the functional block 
script can be defined. Ports are first created using the **Add port(s)** dialog and can be 
later edited using the **Edit port(s)** dialog. Ports that are no longer needed can be deleted 
using the **Delete port(s)** dialog. Additonally, convenience functions have been included 
to allow for ports to be shifted up (**Move port up**) or down (**Move port down**) the 
ports manager list. 

  .. figure:: GUI_Functional_Block_4.png
    :figclass: align-center
    
    Fig 6: Functional block ports manager table

The **Ports Manager** feature has been designed for maximum flexibility. Ports of any signal type, 
direction, and cardinal location (North, East, South, West) can be defined for functional 
blocks allowing for a variety of layout and interconnection models (Fig 7).

  .. figure:: GUI_Functional_Block_5.png
    :figclass: align-center
    :width: 450
    
    Fig 7: Functional block port layout example with signal links

  .. admonition:: About port IDs...
     
     Port IDs, similar to Functional block IDs, are unique integer identifiers that are 
     automatically allocated to each port in a functional block. When ports are deleted or 
     re-configured, the port ID numbering is automatically re-numbered to match the **Ports
     Manager** list (see the first column of the Ports Manager table in Fig 6).
     
**Output Data**

The **Output Data** tab is where custom results (returned as a list from the functional block 
script) are loaded for post-simulation viewing. An example output is shown in Fig 8 for the 
optical PIN detector. To learn more on how to create a results list, see :ref:`data-output-label`.

  .. figure:: GUI_Functional_Block_6.png
    :figclass: align-center
    :width: 350
    
    Fig 8: Functional block output data table (example shown for PIN/APD detector model)


Annotation & data display features
----------------------------------

When working on system designs, annotations can be added to the **Project design space** to 
provide visual highlighting and text-based description areas. SystemLab|Design includes the 
following annotation tools (which can be accessed from the **Project design space** using right-click 
and menu select - Fig 9):

  **Description boxes** which can be used to highlight various regions in the design space 
  (such as sub-systems or grouped functions).
  
  **Text boxes** which can be used to add short or long text (paragraph) descriptions for providing 
  more detail on general or specific system functions.
  
  **Line-arrows** which can be used to bring attention to specific parts of a design.
  
SystemLab|Design also includes specialized data viewers, called **Data panels**. They can be 
configured to provide customized lists of parameters and results originating from any system components 
in the project design space. Numerical results are transmitted to each **Data panel** during a 
simulation and are held in memory so that you can review data results for multiple iteration 
scenarios. To see how **Data panels** are used in a simulation, see :ref:`quick-start-2-label`.
  
  .. figure:: GUI_Design_Layout_1.png
    :figclass: align-center
    :width: 450
    
    Fig 9: Annotation and data panel features (Project design space)
    
    
  .. admonition:: How to access the properties dialog for annotations and data panels...
     
     To access and edit the properties of annotation items and data panels, hover
     over each item and double left-click.
     
For the **Description box**, properties that can be modified include the border color and 
style, the description box dimensions and fill color and the text field font size, color 
and position within the description box.
   
  .. image:: GUI_Design_Layout_2.png
    :align: center
    :width: 350

For the **Text box**, properties that can be modified include the font settings and color, 
the text field (which can have multiple lines) and a text field wrapping width setting
   
  .. image:: GUI_Design_Layout_3.png
    :align: center
    :width: 350px   
   
For the **Line-arrow**, properties that can be modified include the line color, width and 
style, and whether or not to include an arrow in the annotation item
   
  .. image:: GUI_Design_Layout_4.png
    :align: center
    :width: 350px   
    
For the **Data panel**, a variety of properties can be set or modified. These include 
the dimensions, border style, color and fill settings for the title and data sections. 
For further details on how to setup data panels in a design see :ref:`data-panel-label:`.

  .. image:: GUI_Design_Layout_5.png
    :align: center
    :width: 350px   
   