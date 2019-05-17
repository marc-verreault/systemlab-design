
Release Notes
=============

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