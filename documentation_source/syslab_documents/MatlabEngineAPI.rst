.. _matlab-api-label:

.. |reg|    unicode:: U+000AE .. REGISTERED SIGN

MATLAB engine API for Python
============================

As SystemLab|Design is based on the Python programming language, it is possible to call
MathWorks **MATLAB** |reg| as a computational engine from a functional block script. After 
creating an instance of the *MatlabEngine* class you can call MATLAB functions and algorithms 
and exchange data between the Python script and the MATLAB workspace.

The following procedure (for Windows 10) describes how to setup and run the **MATLAB** |reg| **Engine API for Python** |reg| . 

  .. important:: 
    
   To run the **MATLAB Engine API for Python** you must have a supported version 
   of MATLAB (R2014A or later) running on the same operating system where SystemLab|Design 
   is installed.
   
  .. important:: 
    
   MATLAB verifies the version of Python installed on your computer based on the system path (this
   can be verified by calling the **pyenv** function in the MATLAB command window). As the version of Python
   included with SystemLab|Design is a binary module it will not be registered under the Windows system path,
   and thus (assuming that you don't currently have Python installed on your computer) it may be necessary 
   to download and install a standalone version of Python on your computer prior to running
   the procedure below. A version of Python can be downloaded from https://www.python.org/download. 
   During installation make sure to check the box next to *Add Python to environment variables*.
   
Additional information on the use of this feature and its installation can be found on the 
MathWorks |reg| web site: `Calling MATLAB from Python 
<https://www.mathworks.com/help/matlab/matlab-engine-for-python.html?s_tid=CRUX_lftnav>`_.

**How to install the MATLAB Engine API for Python for SystemLab|Design**

1.  Launch the Windows command prompt window by entering in the search field from the taskbar
    **command** or **cmd**
2.  Below the **Command Prompt** select **Run as administrator**.

  .. image:: Matlab_API_1.png
    :align: center
    :width: 400px
	
3. A **User Account Control** dialog will open to confirm that you want to allow this app to 
   make changes to your device. Select **Yes** to continue.

  .. image:: Matlab_API_1A.png
    :align: center
    :width: 500px   
   	
4.  From the command prompt type: ::

        cd C:\path_to_matlab_root_dir\extern\engines\python
		
    **Note:** "path_to_matlab_root_dir" is for example "C:\\Program Files\\MATLAB\\R2020b".
	
  .. image:: Matlab_API_1B.png
    :align: center
    :width: 500px 
 
5.  From the command prompt type: ::

        python setup.py install --prefix="C:\path_to_systemlab_application\systemlab_design"
		
    **Note:** "path_to_systemlab_application" is the location where the "systemlab_design" folder
    is installed on your computer. *[The cmd window should output information indicating that
    the installation build is running, creating and copying files to the target directory.]*
    

  .. image:: Matlab_API_1C.png
    :align: center
    :width: 500px

6.  To verify that the MATLAB API was correctly installed check that there is a new
    folder *matlab* under the *...\\systemlab_design\\Lib\\site-packages* folder.
    
    **Note:** The "Lib/site-packages" folder is a new folder and may appear at the bottom of the 
    systemlab-design project files directory. Select the **Refresh** button of the Windows File Explorer 
    to move the folder to upper portion of the directory.

  .. image:: Matlab_API_2.png
    :align: center
    :width: 500px

7.  Select the folder *matlab* and drag and drop it to the folder *systemlab_design*. *[This step is 
    important as it will ensure that the matlab.engine can be located and successfully imported 
    from any functional block script.]*

  .. image:: Matlab_API_3.png
    :align: center
    :width: 500px

**Test that the MATLAB engine can be called from a functional block script**

8.  Launch a new application of SystemLab|Design by double left-clicking on the *SystemLab-Design.exe* 
    executable file.
9.  Add a new functional block to the default project scene with the following settings:
    
    a. Add one port to the functional block with the following settings: Port name: *'Out'*, Cardinal point: **East**, 
       Direction: **Out**, Signal type: **Electrical** (remember to click **Apply** before saving and closing the 
       **Add ports** dialog).
    b. Functional block name/ID: **MATLAB Test**
    c. Script module name: **Matlab_Run**
    
10. Open a session of **SciTE** (or equivalent) by selecting **Edit/Open code/script editor**.
11. Within the editing panel (under "1 Untitled") copy and paste the code as shown in the box 
    below. 
	
	Note: In the code below we initiate a new MATLAB process by calling **eng = matlab.engine.start_matlab()**. 
	We then build an array of ones within the MATLAB workspace and access this array using the 
	command **sig_array = matlab.double(eng.ones(1,n))**. 
	
	To ensure that the array matches the **Numpy** array format we use the command 
	**sig_array = np.asarray(sig_array[0])** to convert the Python list to a **Numpy** array. 
	The data from this array is then returned to the simulation algorithm and allocated to 
	the output port of the functional block.
	::
    
		import numpy as np
		import config
		import matlab.engine
		
		def run(input_signal_data, parameters_input, settings):
	  
			'''==PROJECT SETTINGS==================================================='''
			module_name = 'MATLAB Test'
			n = settings['num_samples']
			n = int(round(n))
			time = settings['time_window']
			fs = settings['sampling_rate']
			carrier = 0
			sig_type = 'Electrical'
			parameters_input = []

			'''==CALCULATIONS======================================================='''   
			time_array = np.linspace(0, time, n)
			noise_array = np.zeros(n)   
			
			if config.sim_status_win_enabled == True:
				config.sim_status_win.textEdit.append('Starting MATLAB Engine... ')
				config.app.processEvents()
			# Initiate a new MATLAB process
			eng = matlab.engine.start_matlab()
			# Build array (within MATLAB workspace) and access locally
			sig_array = matlab.double(eng.ones(1,n))
			# Change array from python list format to numpy array format
			sig_array = np.asarray(sig_array[0])
			# eng.desktop(nargout=0)

			if config.sim_status_win_enabled == True:
				config.sim_status_win.textEdit.append('Quiting MATLAB Engine... ')
				config.app.processEvents()
			eng.quit()

			matlab_results = []

			'''==RETURN (Output Signals, Parameters, Results)=================================='''
			
			electrical_signal = [1, sig_type, carrier, fs, time_array, sig_array, noise_array]
			return ([electrical_signal], parameters_input, matlab_results)

12. Save the file as *Matlab_Run.py* within the folder *systemlab_design* (make sure to include the suffix 
    .py in the **File Name** field when saving) and close the session of SciTE.
13. Start running a simulation [*The simulation should complete as shown below*]

  .. image:: Matlab_API_4.png
    :align: center
    :width: 500px
	
14. Double left click on the output port of **MATLAB Test** to verify that an output signal is
    created as shown below:
	
  .. image:: Matlab_API_5.png
    :align: center
    :width: 500px
|

  .. admonition:: About the MATLAB engine API for Python...
  
	As shown in this example, you can call any MATLAB function or a custom script (m-file) 
	directly from the functional block Python script. Data arguments can be passed from Python 
	to the MATLAB engine (in this example we have used the number of samples 'n') and returned 
	by declaring local variables in Python (in this example we used 'sig_array'). Also, any data types 
	within the MATLAB workspace can be accessed through the command **a = eng.workspace('data')** where 
	'a' is the local variable in Python and 'data' is a data variable located within the MATLAB workspace. 
	 
	Further information on how to exhange data between Python and MATLAB can be found on the 
	MathWorks |reg| web site: `Calling MATLAB from Python 
	<https://www.mathworks.com/help/matlab/matlab-engine-for-python.html?s_tid=CRUX_lftnav>`_.
	
	
  .. important:: 
    
	NOTE: To initiate a MATLAB process from within a functional block script the **import matlab.engine** 
	statement MUST be included at the beginning of the script. Also, once calculations linked to the 
	MATLAB process have been completed, the active session of the MATLAB engine MUST be closed by using the **eng.quit()** 
	command. If the process is not terminated, the functional block script will remain in a suspended state!
