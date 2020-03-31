.. _add-functional-block-to-library-label:

How to add a functional block to the library
============================================

In the following tutorial, we will create a new functional block and script for a DC Block 
device and add it as a new item in the functional block library menu tree. As a final step 
we will create an icon for the DC Block device.

  .. note:: 
    A completed version of this design can be found within the folder 
    *"systemlab_design\\systemlab_examples\\electrical\\dc_block\\"* 

**Part 1: Create the new functional block (DC Block)**

1.  Launch a new application of SystemLab|Design by double left-clicking on the 
    *"SystemLab-Design.exe"* executable file.
2.  From the **Menu bar**, select **File/Open project** and go to the folder 
    *"systemlab_design\\syslab_fb_library"*.
3.  Select the design project *"Noise Source"* (it will have a suffix ".slb") and 
    click on the **Open** button. 
4.  On the project design space, hover over the Noise Source functional block item, 
    right-click mouse and select **Delete functional block**.   
5.  Within the same area of the project design space, right-click mouse and select **Add functional 
    block**.
6.  Double left-click on **Functional_block_1** to open the Functional block properties.
7.  Update the following data fields under the **Functional block main settings**:   

    a. Set the **Functional block/name/ID** to: "DC Block"
    b. Set the **Script module name** to: "DC_Block"
    c. Uncheck the **Display fb name** check box
    
  .. image:: Add_FB_1.png
    :align: center
    :width: 350
    
8.  Update the following data fields under the **Functional block dimensions and colors**:   

    a. Set the **Dimensions/Width** to: 30
    b. Set the **Dimensions/Height** to: 30
    
  .. image:: Add_FB_2.png
    :align: center
    :width: 350
    
9.  Under the **Ports Manager** tab, add two new ports as follows:

    a. Port name: *'Input'*, Cardinal point: **West**, Direction: **In**, Signal type: **Electrical**
       (remember to click **Apply** before proceeding to enter the data for the 2nd port).
    b. Port name: *'Output'*, Cardinal point: **East**, Direction: **Out**, Signal type: **Electrical**
    c. Select **Apply**, followed by **Save**, to finalize the port changes.
    
  .. image:: Add_FB_3.png
    :align: center
    :width: 350

10. Select **OK** to close the **Functional block settings** dialog. 
11. Anywhere on the design project space, right-click mouse and select **Project amd layout settings**.
12. Within the **Project name** data field change the text to "DC Block". 
13. Hover over the text that is labeled as "Electrical", and double left-click to open the **Text 
    field properties** dialog.
14. Within the **Text field** region change the text "Noise Source" to "DC Block" and select **OK**.
    *[The design project space should appear as shown below.]*
    
  .. image:: Add_FB_4.png
    :align: center
    
15. From the **Tool bar**, select the **Save** icon to save the new functional block to the 
    *syslab_fb_library*.
    
**Part 2: Create the associated fb_script for the DC Block**
    
16. Open a session of SciTE by selecting **Open Python code/script editor** from the **Menu bar**.
17. From the SciTE dialog, select **File/Open**.
18. Go to the folder *"systemlab_design/syslab_fb_scripts/electrical"* and open the Python module called 
    *"Integrate_And_Dump.py"*.   
19. Starting from the "INPUT PARAMETERS" commented line all the way to the **return** function, 
    replace the code in the *"Integrate_And_Dump.py"* module with the following code segment: ::
          
        '''==INPUT PARAMETERS============================'''
    
        '''==INPUT SIGNALS==============================='''
        sig_type = 'Electrical'
        carrier = 0
        time = input_signal_data[0][4]
        signal = input_signal_data[0][5]
        noise_out = input_signal_data[0][6]  
    
        '''==CALCULATIONS================================'''
        sig_avg = np.mean(np.real(signal))
        sig_out = signal - sig_avg
        
        '''==OUTPUT PARAMETERS LIST======================'''
        script_parameters = []
        script_parameters = parameters_input
        
        '''==RESULTS====================================='''
        script_results = []
        
        '''==RETURN (Output Signals, Parameters, Results)============'''
        
        return ([[2, sig_type, carrier, fs, time, sig_out, noise_out]], 
                script_parameters, script_results)
    
20. Save the script module as "DC_Block". 

**Part 3: Add the DC Block to the Functional block library menu tree**

21. From the **Menu bar** select **Edit/Functional block libray config file/Edit**.
22. Go to line 67 of the script, and add "DC Block" to the list **elec_math_operators** as 
    follows: ::
    
        elec_math_operators = ['Branching Node (Electrical)', 'Adder', 'Subtractor', 'Multiplier',
                       'Sign Inverter', 'Vertical Shift', 'Phase Shift (Electrical)', 'DC Block']

23. Save the script module and close the SciTE session.
24. From the **Menu bar** select **Edit/Functional block libray config file/Reload**. *[This action 
    will re-import the functional block library config file into SystemLab-Design and re-instantiate 
    the functional block tree menu object.]*
25. Go to the **Functional block library** (left panel of GUI) and hover over the triangle
    in front of the **Mathematical operators** group (under **Electrical**).
26. Left-click mouse to expand the menu *[The DC Block item should be displayed at the bottom 
    of the list].* 
27. Left-click select and hold over the **DC Block** component and starting moving
    your mouse towards the design scene for **Project_1**.
28. Release the mouse button anywhere over the design layout *[The DC Block functional block 
    should appear on the layout as shown below.]* 
    
  .. image:: Add_FB_5.png
    :align: center
    :width: 350
    
29. To test if the new functional block is working as expected, we will add a **Sine Generator** 
    to the project design space. Select the arrow next to the **Waveform generators** group 
    to expand the menu and drag and drop a **Sine Generator** onto the design layout.
30. Connect the output port of the **Sine Generator** to the input port of the **DC Block** 
    as follows:
    
  .. image:: Add_FB_6.png
    :align: center   
    
31. Double left-click on **Sine Generator** to open the Functional block properties.
32. Under **Input Parameters**, set the **Bias** parameter value to "2" and select **OK** to 
    save the changes and close the dialog.
33. On the **Tool bar**, select the **Settings** button to open the **Project settings** dialog 
    and set the **Simulation time** data field to "1.00E-09".
34. On the **Tool bar**, select the **Start** button to initiate the simulator. 
35. Double left-click over the **DC Block** input port to open its **Electrical signal data 
    analyzer** dialog. Open also the signal data viewer for the **DC Block** output port.
    
    *The amplitude bias of the input sinusoidal waveform should have been removed 
    by the DC Block (as shown in Fig 2 below).*
    
  .. figure:: Add_FB_7.png
    :align: center 
    :width: 450
    
    Fig 1: DC Block input signal
    
  .. figure:: Add_FB_8.png
    :align: center 
    :width: 450
    
    Fig 2: DC Block output signal
    
**Part 4: Create and add an icon for the DC Block**

36. Open a session of SciTE by selecting **Edit/Open code/script editor** from the **Menu bar**.
37. From the SciTE dialog, select **File/Open**.
38. Navigate to the folder *"systemlab_design/syslab_fb_icons"* and open the Python module called 
    *fb_icon_driver.py*.
39. Save the file as *"fb_icon_dc_block.py"* (Note: It's important to include the suffix *".py"* 
    so that the editor will save the file as a Python compatible file) 
40. Within the code for *"fb_icon_dc_block.py"*, delete the entire code for the **def run (x,y)** 
    method and replace with the following lines of code: ::
    
        def run (x, y):
            icon_1 = QtWidgets.QGraphicsPathItem()
            icon_path_1 = QtGui.QPainterPath() 
            p1 = QtCore.QPointF(x, y+15)
            p2 = QtCore.QPointF(x+12, y+15)
            icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
            icon_1.setPath(icon_path_1)
            icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75))
            
            icon_2 = QtWidgets.QGraphicsPathItem()
            icon_path_2 = QtGui.QPainterPath() 
            p1 = QtCore.QPointF(x+12.5, y+5)
            p2 = QtCore.QPointF(x+12.5, y+25)
            icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
            icon_2.setPath(icon_path_2)
            icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75))
            
            icon_3 = QtWidgets.QGraphicsPathItem()
            icon_path_3 = QtGui.QPainterPath() 
            p1 = QtCore.QPointF(x+17.5, y+5)
            p2 = QtCore.QPointF(x+17.5, y+25)
            icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
            icon_3.setPath(icon_path_3)
            icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75))
            
            icon_4 = QtWidgets.QGraphicsPathItem()
            icon_path_4 = QtGui.QPainterPath() 
            p1 = QtCore.QPointF(x+17.5, y+15)
            p2 = QtCore.QPointF(x+30, y+15)
            icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2]))
            icon_4.setPath(icon_path_4)
            icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75))
    
            icon_paths = [icon_1, icon_2, icon_3, icon_4]
            return icon_paths
        
41. On the **Tool bar**, click the **Save** icon to save the changes.
42. Double left-click on **DC Block** to open the Functional block properties.
43. Under **Icon settings** add the following text to the **File name** data field:
    *"fb_icon_dc_block"* .
44. Make sure that the **Display icon** check box is checked and select **OK** to save the 
    changes and close the properties dialog. *[The DC Block functional should now include an 
    icon as shown below]* .
    
   .. image:: Add_FB_9.png
    :align: center 
    
**This completes the tutorial on how to add a functional block to the library!** 
    
    