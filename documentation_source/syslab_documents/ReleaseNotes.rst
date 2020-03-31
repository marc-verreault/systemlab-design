.. |reg|    unicode:: U+000AE .. REGISTERED SIGN

Release Notes
=============

Version: 20.01.r1 (27 Jan 2020)
---------------------------------

**Highlights**

Version 20.01.r1 is the second major release of SystemLab|Design and includes
the following new features and improvements:

*  Several new components (21) have been added to the Functional block library including:

   * Optical (Sources/Transmitters): **CW Laser Array**, **Gaussian Pulse (Optical)**
   * Optical (Signal processing): **Branching node (Optical)**, **Optical Filter (Band Pass)**
   * Optical (Passive devices (fiber)): **Optical Fiber (Linear)**
   * Optical (Passive devices (couplers/splitters)): **Optical Splitter (4-port)**
   * Optical (Passive devices (other)): **Optical Attenuator**, **Optical Circulator**, **Fiber Bragg Grating**  
   * Optical (Polarization devices): **Polarization Beam Splitter**, **Polarization Beam Combiner**, 
     **Jones Matrix**
   * Optical (Analyzers): **Measurement Node (Optical)**
   * Electrical (Waveform generators): **Gaussian Pulse Generator**
   * Electrical (Mathematical operators): **Branching Node (Electrical)**, **Sign Inverter**, 
     **Vertical Shift**, **Phase Shift (Electrical)**
   * Electrical (Receivers): **Comparator**, **Analog to Digital Converter**
   * Digital: **Branching Node (Digital)**

*  All optical functional blocks have been updated to support the processing of 
   multiple wavelengths.
*  The polarization feature for optical signals has been updated to support two field formats: 
   combined field (Exy) or separate fields (Ex and Ey).
*  To support the analysis of multi-wavelength designs, the **Optical signal data analyzer** 
   viewer now includes an integrated spectrum analyzer feature (tab **Freq Data (all channels)**).
*  The **Data panels** feature no longer requires the manual addition 
   of dictionary entries to the *config_data_panels* file. Data panel additions and 
   deletions are now managed automatically through an internal global dictionary.
*  An **Undo** action has been added to the **Edit** menu item. This new feature tracks project space 
   deletion events so that they can be reversed if needed.
*  Functional blocks now include new context menu items for directly accessing **Parameters** and 
   **Results** tables (per iteration).
*  A short-cut to access a functional block's **script editor** has been added to the 
   functional block context menu.
*  A short-cut to update the number of iterations for a simulation has been added to the **Project design space** 
   context menu.
*  New generic **Digital**, **Electrical** and **Optical** functional blocks 
   (with associated scripts) have been added to the **Project design layout** context menu.
*  Short-cuts to edit and reload the **config_special.py**, **config_fb_library.py**, **config_port_viewers.py**, 
   and **systemlab_viewers.py** configuration files have been added to the **Edit** menu item. The **Reload** action 
   allows for a config file to be manually reloaded into the application thus no longer requiring for the application 
   to be restarted for settings to take effect.
*  The Functional block hover tool tip feature has been enhanced and includes the ability 
   to view **simulation results** associated with the functional block's script calculations.
*  The **Signal port hover menu tool tip** feature has been enhanced to include the ability   
   to view summary metrics for a signal (total/average power, mean/standard deviation/variance).
*  Signal connections can now be optionally highlighted (following a hover event) to better 
   visualize their routing.
*  A new **View** menu item has been added to the **Menu bar**. It includes zoom-in, zoom-out, and actual size 
   adjustments along with the ability to fit all items/functional blocks within a project view.
*  A **Wave-Freq Converter** calculator feature has been added to the **Tools** menu item (to help in quickly
   calculating the equivalent frequency or wavelength value of a carrier).
*  As SystemLab|Design is based on the Python programming language, it is possible to call
   MathWorks **MATLAB** |reg| as a computational engine from a functional block script. 
   A new documentation section has been added to the *Advanced Topics*
   section (:ref:`matlab-api-label`) and provides details on how to install the 
   MATLAB engine API, call MATLAB functions and algorithms, 
   and interchange data between a Python script and a MATLAB workspace.

**Notes about this release**

*  SystemLab|Design project files (.slb) can only be opened from the SystemLab|Design 
   main application (it is not currently possible to double-click on a project design file 
   to initiate a SystemLab|Design session).
*  The properties dialog windows for **Functional blocks**, **Project settings**, **Data panels**, 
   **Text boxes**, **Description boxes** and **Line-Arrows** are modal. When one of these 
   windows is activated, interactions with other open windows will not be possible until 
   these dialogs are closed.
   
**Known bugs**

*  The SystemLab|Design application may remain open after several attempts are made to shut down 
   the application (**Quit application** procedure). To force the application to shut down, 
   activate the Windows Task Manager (**ctrl-alt-delete**), and right-click select **End task** 
   on the application *Multi-domain system simulator*. Target release for fixing is TBD.

Version: 19.02.r1 (10 May 2019)
---------------------------------

**Highlights**

We are pleased to announce the first official release of SystemLab|Design; a Python-based, 
open-source, software simulation platform optimized for the rapid development and virtual 
prototyping of multi-domain systems.

The core features being introduced in this release include:

*  A **2D project design and layout** environment for creating and modeling multi-domain 
   system prototypes using analog and digital based building blocks (for further details on 
   main application interface features see :ref:`gui-features-label`) 
*  An automated **end-to-end simulation engine** for assessing the performance of virtual system
   designs, including dynamic (feedback) systems modeling (see :ref:`simulator-operations-label` 
   for further details on the capabilities of the simulation engine)
*  A comprehensive post-simulation analysis via **port-based signal data viewers** (time-domain, 
   frequency-domain, polarization analysis, statistical metrics)
*  A **systems-level performance analysis** tool kit, including iteration sweeping of input 
   parameters, custom viewers/graphs, and data panels. To see these tools in action, see 
   :ref:`quick-start-2-label`)
*  A **Functional block library** menu which provides access to pre-defined optical, electrical 
   and digital system components that can be dragged and dropped onto your design layout. 

**Notes about this release**

*  The ability to **Undo** or **Redo** keyboard actions has not been implemented in this release 
   but is planned for a future release.
*  SystemLab|Design project files (.slb) can only be opened from the SystemLab|Design 
   main application (it is not currently possible to double-click on a project design file 
   to initiate a SystemLab|Design session).
*  The properties dialog windows for **Functional blocks**, **Project settings**, **Data panels**, 
   **Text boxes**, **Description boxes** and **Line-Arrows** are modal. When one of these 
   windows is activated, interactions with other open windows will not be possible until 
   any of these dialogs is closed.
*  The Functional block library currently provides access to 29 pre-defined functional block 
   elements. These represent a sample of the components typically found in optical and 
   electrical communication and sensor systems. More functional block elements will be 
   added in future updates. If you would like to assist in developing new functional models 
   for future releases, your contributions would be greatly appreciated! For further 
   information on how you can help, please contact us at info@systemlabdesign.com
*  An initial set of example designs can be found under *systemlab_design/systemlab_examples*.
   More example designs will be added in future updates.