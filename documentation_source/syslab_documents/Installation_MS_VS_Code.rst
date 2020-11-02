
Set up VS Code as your default code editor
==========================================

By default SystemLab|Design runs the Scintilla/SciTE script editor when viewing and editing 
your project's Python scripts, however you can set up other Python-compatible script editors to 
view and edit your project models. This procedure describes how to install and set up Microsoft 
Visual Studio (VS) Code as your default project script editor.

To install Visual Studio (VS) Code on your computer, complete the following steps:

1. On your web browser, go to the Visual Studio home page (`VS Code Home Page <https://code.visualstudio.com>`_) 
   and select **Download for Windows**
   
   .. figure:: Installation_VS_Code_1.png
    :figclass: align-center
    :width: 550

2. Select the "Save file" option when prompted. 
      
3. Once downloaded, double left-click on *VSCodeUserSetup-x64-1.50.1.exe* (or more recent version) to initiate 
   the installation process.

4. After accepting the license agreement, select **Next**.

  .. figure:: Installation_VS_Code_2.png
    :figclass: align-center
    :width: 350

5. You will be prompted to select the destination folder where VS Code will be installed. It is recommended 
   to use the suggested folder location. Select **Next** to continue.
   
   .. figure:: Installation_VS_Code_2A.png
    :figclass: align-center
    :width: 350

6. You will be prompted to select where Setup should place the program short-cut. Select **Next** to continue.

   .. figure:: Installation_VS_Code_3.png
    :figclass: align-center
    :width: 350

7. Under the **Select Additional Tasks** it is recommended to check the box: *Add "Open with Code" action to Windows Explorer file context menu*.
   Note: The check box for *Add to PATH* should already be checked. If not, please make sure to check this box too! Select **Next** to 
   continue and then select the **Install** button.
   
   .. figure:: Installation_VS_Code_4.png
    :figclass: align-center
    :width: 350
	
   .. figure:: Installation_VS_Code_4A.png
    :figclass: align-center
    :width: 350
   
8. After the installation is complete select **Finish** to exit the setup process. 
   
   .. figure:: Installation_VS_Code_5.png
    :figclass: align-center
    :width: 350
	
To set up VS Code as the default script editor for SystemLab|Design, complete the following steps:
	
1. Open a new session of SystemLab|Design and select the **Settings** action button on the tool bar.

2. Under the **Advanced settings** tab, delete the current text in the **Code/Script editor command line path** value field and
   replace with the text 'code -r' as follows:
	
   .. figure:: Installation_VS_Code_6.png
    :figclass: align-center
    :width: 350

   .. tip::
    The '-r' argument is used to force new files to be opened in the same VS Code session or window. To open a new session/window each
    time VS Code is called, remove this argument.
    
3. Select **OK** to apply the settings.

4. From the **Menu bar**, select **Edit/Open code/script editor**. A command prompt followed by a new session
   of VS Code should appear as follows
   
   .. figure:: Installation_VS_Code_7.png
    :figclass: align-center
    :width: 550	
	
VS Code has now been setup as the default script editor for your project!
	
  .. important:: 
    
	The script editor command line path settings are specific to a project. To enable VS Code as the default editor for any new or
	existing projects, steps 1-3 must be repeated (and the project saved to file) for each applicable project.
	
	Please note that when working on a specific project, its project settings will also be used to define the script editor 
	command line path for opening configuration files under the **Edit menu** (e.g. Port viewers config file, Functional block 
	library config file, etc.).

	

