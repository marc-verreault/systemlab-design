'''
    SystemLab-Design Version 19.02
    Primary author: Marc Verreault
    Copyright (C) 2019 SystemLab Inc. All rights reserved.
    
    NOTICE==============================================================    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.    
    ====================================================================

    ABOUT THIS MODULE
    Name: systemlab_viewers
    Source code for building customized viewers and graphs (called during or after
    a simulation run)
'''

import os
import config
gui_ui_path = config.root_path
import numpy as np

import time as time_data

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from matplotlib import pyplot as plt
# Method for embedding Matplotlib canvases into Qt-designed QDialog interfaces
# Ref: https://matplotlib.org/gallery/user_interfaces/embedding_in_qt_sgskip.html
# Accessed: 11 Feb 2019
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Template for generic 2D graphs (up to 3 tabs available,  more can be added)
qtIterationsViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'IterationsViewer.ui')
qtIterationsViewerFile = os.path.normpath(qtIterationsViewerFile)
Ui_Iterations_Analysis, QtBaseClass = uic.loadUiType(qtIterationsViewerFile)

# Template for
qtFunctionalBlockStatusFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'FunctionalBlockStatus.ui')
qtFunctionalBlockStatusFile = os.path.normpath(qtFunctionalBlockStatusFile)
Ui_FunctionalBlockStatus, QtBaseClass = uic.loadUiType(qtFunctionalBlockStatusFile)

app_font_default = 'font-size: 8pt; font-family: Segoe UI;'

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 80

class IterationsAnalyzer_Opt_Amp(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.
    '''
    def __init__(self, data_x_1, data_y_1, data_x_2, data_y_2):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        self.iteration = 1  
        self.data_x_1 = data_x_1
        self.data_y_1 = data_y_1 
        self.data_x_2 = data_x_2
        self.data_y_2 = data_y_2
        
        
        #Setup background colors for frames
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame.setPalette(p)       
        p2 = self.graphFrame_2.palette()
        p2.setColor(self.graphFrame_2.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame_2.setPalette(p2)
        
        #Setup matplotlib figures and toolbars
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_xy)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        
        self.tabData.setCurrentWidget(self.tab_xy)
        self.tabData.setTabText(0, 'Optical amplifier characteristics')
        
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        ax = self.figure.add_subplot(211, facecolor = '#f9f9f9')
        ax2 = self.figure.add_subplot(212, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x_1, self.data_y_1, color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3)
                    
        ax2.plot(self.data_x_2, self.data_y_2, color = 'red', linestyle = '-',
                    linewidth= 0.8, marker = 'o', markersize = 3)
        
        #ax2.tick_params(axis='y', colors='red')
        #ax2.set_ylabel('', color = 'red')
        ax.set_title('Amplifier Gain (small signal)')
        ax.set_xlabel('Total input signal power (dBm)')
        ax.set_ylabel('Gain (dB)')
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
        ax2.set_title('Amplifier Gain (small signal)')
        ax2.set_xlabel('Total output signal power (dBm)')
        ax2.set_ylabel('Gain (dB)')
        ax2.set_aspect('auto')
        ax2.grid(True)  
        ax2.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax2.minorticks_on()
        ax2.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
        
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        
'''FUNCTIONS==========================================================================='''
    
def set_icon_window():
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLab_64.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
    
'''===================================================================================='''