# systemlab-design
Multi-domain simulator for systems prototyping

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
author for further information

For information on the software architecture see the intro comments to..

Development and testing of the software has been done using the Spyder IDE (version 3.3.2), 
which can be 

INSTRUCTIONS ON HOW TO CREATE A BUILD OF SYSTEMLAB|DESIGN

SystemLab-Design is a Python-based application that includes library links to PyQt 5.12.2/Qt 5.12.3, 
Numpy 1.16.3, Matplotlib 3.0.3, SciPy 1.2.1. It can be distributed to other users by preparing a 
distribution (dist) folder using PyInstaller.

1 - Creating the build environment

1A) Download and install the latest version (Windows x86-64 executable installer) of Python
from "https://www.python.org/downloads/"
1B) After installation is complete, create a virtual project folder
