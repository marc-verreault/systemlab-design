# systemlab-design

SystemLab-Design is a computational engineering software platform that can be used
to design, model and simulate multi-domain systems across several technologies 
and/or signal domains (optics/photonics, electronics, analog control systems, etc.)

Built for ease-of-use and flexibility, it can be quickly deployed to test out
design concepts and predict system performance. It can also be used as an
aid for teaching engineering principles or for sharing design ideas and concepts
among peers.

Future releases of SystemLab-Design are planned and your feedback on the performance
and features of this software is greatly welcome. Also, if you wish to contribute to
improving the capabilities of SystemLab-Design, please contact the primary
author for further information (marc.verreault@systemlabdesign.com)

For an overview of the software architecture please see the intro comments in the file 
*systemlab_main_v2001_r2.py* (under *systemlab-design/source*). This file is the main 
application module for the software.

Development and testing of the software can be done through the Spyder IDE and can be installed 
using the PIP utility (**pip install spyder**). Other IDE's can be used however.

INSTRUCTIONS ON HOW TO CREATE A BUILD OF SYSTEMLAB|DESIGN

SystemLab-Design 20.01 is a Python-based application that includes library links to PyQt 5.13.1, 
Numpy 1.17.2, Matplotlib 3.1.1, SciPy 1.3.1. It can be distributed to other users by preparing a 
distribution (dist) folder using PyInstaller.

Procedure:

1) Download and install the latest version (Windows x86-64 executable installer) of Python
from https://www.python.org/downloads/

2) After installation is complete, create a python virtual environment for the project. 

- Install the virtual environment feature by entering the command: **pip install virtualenv**
- Create a new virtual project folder by entering the command: **virtualenv new_project**
- Activate the new project as follows: **new_project\scripts\activate**

Note: Please see the following link for further details on how to create a virtual env: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

3) Within the activated virtual environment (terminal session), install the following modules using pip

- **pip install pyqt5**
- **pip install matplotlib**
- **pip install numpy**
- **pip install scipy**
- **pip install pyinstaller**
    
4) Open the file *systemlab_build_V2001.spec* and update the *pathex* (within **Analysis**) to the root 
path for the virtual environment folder. 

5) For the **exe = EXE (pyz, ...)** command line make sure to update the file path for *icon* and *version* to
include the full path (C:\\..) for the virtual environment folder.

6) Deactivate the virtual environment by running the command **deactivate**.

7) Run PyInstaller using the following command in the terminal: **pyinstaller C:\path_to_virtual_folder\systemlab_build_V2001.spec**

8) The build process may issue several warnings but should complete successfully. The distribution folder (*dist*) 
should appear within the virtual directory.

NOTE: A pre-installed version of SciTE 4.1.4 (free source code editor for Win32 and X) has been included with the 
source code. If you wish to install a newer version of SciTE, please make sure to set aside the current *SciTEGlobal.properties*
and *python.properties* files. These files have been customized for the SystemLab-Design application and it is recommended 
to use these modified versions in lieu of the default installed versions.


INSTRUCTIONS ON HOW TO CREATE A BUILD OF THE SYSTEMLAB|DESIGN DOCUMENTATION

The SystemLab-Design documentation is built using the Sphinx documentation generator (*Read the Docs* theme).
For information on getting started with Sphinx see: https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

Procedure:

1) From your project directory, launch a terminal session and install Sphinx: **pip install sphinx**

2) After the installation is complete, install the read the docs theme: **pip install sphinx_rtd_theme**

3) Run quick start to create your build env: **sphinx-quickstart**

   Make sure to accept all the defaults during the quick start procedure. Once complete, files will be created for *index.rst*,
   *config.py* and others, along with a *source* folder for adding images and reStructuredText documents.
   
4) Under the *source* folder, replace the files *conf.py* and *index.rst* with the versions that are located under 
   *systemlab-design/documentation_source*.
   
5) Under the *source* folder, add the files *LogoMakmr-9zOCZf* and the entire folder *syslab_documents* (located 
   under *systemlab-design/documentation_source*)

6) Under the *source/_static* folder add the file *custom-styles* (located under *systemlab-design/documentation_source*)

7) From the terminal session window, run the following command: **make html**

8) After the build is complete, go to the *build/html* folder and double-click on *index.html* to test the html 
   documentation.


