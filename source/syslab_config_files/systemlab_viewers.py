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

# Template for signal space analyzer (Note: File was built from QTCreator)
qtSignalSpaceViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'SignalSpaceViewer.ui')
qtSignalSpaceViewerFile = os.path.normpath(qtSignalSpaceViewerFile)
Ui_Signal_Space_Electrical, QtBaseClass = uic.loadUiType(qtSignalSpaceViewerFile)

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


class SignalSpaceAnalyzer(QtWidgets.QDialog, Ui_Signal_Space_Electrical):
    '''
    Linked to: Electrical applications/QPSK Design/QPSK Design 22 Feb 2019  
    '''    
    def __init__(self, signal_data_i, signal_data_q, signals_ref_i, signals_ref_q,
                 evm_p_res, evm_db_res):
        QtWidgets.QDialog.__init__(self)
        Ui_Signal_Space_Electrical.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)   
        self.iteration = 1  
        self.signals_i = signal_data_i
        self.signals_q = signal_data_q
        self.signals_ref_i = signals_ref_i
        self.signals_ref_q = signals_ref_q
        self.evm_p_res = evm_p_res
        self.evm_db_res = evm_db_res
        
        iterations = len(signal_data_i)   
        self.spinBoxTime.setMaximum(iterations)
        self.totalIterationsTime.setText(str(iterations))
        self.spinBoxTime.valueChanged.connect(self.valueChangeTime)
        
        num_sampling_points = len(self.signals_i[1])   
        self.totalSamplesTime.setText(str(format(num_sampling_points, '0.3E')))
        
        self.evm_per.setText(str(format(self.evm_p_res[1], '0.2f')))
        self.evm_db.setText(str(format(self.evm_db_res[1], '0.2f')))
        
        self.signalCheckBox.stateChanged.connect(self.checkSignalChangedTime)
        self.sigandnoiseCheckBox.stateChanged.connect(self.checkSignalChangedTime)
        
        self.checkBoxMajorGrid.stateChanged.connect(self.checkSignalChangedTime)
        self.checkBoxMinorGrid.stateChanged.connect(self.checkSignalChangedTime)    
        
        #Setup initial data for iteration 1 (default)
        self.signal_i = self.signals_i[self.iteration]
        self.signal_q = self.signals_q[self.iteration]  
        self.signal_ref_i = self.signals_ref_i[self.iteration]
        self.signal_ref_q = self.signals_ref_q[self.iteration]  
        
        #Setup background colors for frames
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame.setPalette(p)       
        p2 = self.dataFrame.palette()
        p2.setColor(self.dataFrame.backgroundRole(), QtGui.QColor(252,252,252))
        self.dataFrame.setPalette(p2)
        
        #Setup matplotlib figures and toolbars
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_xy)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        
        self.tabData.setCurrentWidget(self.tab_xy) 
        self.figure.set_tight_layout(True)
        self.plot_scatter()
        self.canvas.draw()
        
    def valueChangeTime(self):
        new_iteration = int(self.spinBoxTime.value())
        
        self.signal_i = self.signals_i[new_iteration]
        self.signal_q = self.signals_q[new_iteration]
        self.signal_ref_i = self.signals_ref_i[new_iteration]
        self.signal_ref_q = self.signals_ref_q[new_iteration]
        
        self.evm_per.setText(str(format(self.evm_p_res[new_iteration], '0.2f')))
        self.evm_db.setText(str(format(self.evm_db_res[new_iteration], '0.2f')))
        
        self.tabData.setCurrentWidget(self.tab_xy)       
        self.plot_scatter()
        self.canvas.draw()
        
    def checkSignalChangedTime(self):
        self.tabData.setCurrentWidget(self.tab_xy)       
        self.plot_scatter()
        self.canvas.draw()
        
    def plot_scatter(self):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        
        if self.signalCheckBox.checkState() == 2:
            ax.plot(self.signal_ref_i, self.signal_ref_q, color = 'b', linestyle = 'None',
                    linewidth= 0.8, marker = 'o', markersize = 3)
        if self.sigandnoiseCheckBox.checkState() == 2:
            ax.plot(self.signal_i, self.signal_q, color = 'r',
                    linestyle = 'None', linewidth= 0.8, marker = 'o', markersize = 2)  
            
        x_low, x_high = ax.get_xlim()
        y_low, y_high = ax.get_ylim()
        ax.set_ylim(min(x_low, y_low),max(x_high, y_high) )
        ax.set_xlim(min(x_low, y_low),max(x_high, y_high) )            
        ax.set_title('IQ data - electrical')
        ax.set_xlabel('I')
        ax.set_ylabel('Q')
        
        if self.checkBoxMajorGrid.checkState() == 2:
            ax.grid(True)  
            ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
       
        if self.checkBoxMinorGrid.checkState() == 2:
            ax.minorticks_on()
            ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
            
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)


class IterationsAnalyzer_QPSK(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to: Electrical applications/QPSK Design/QPSK Design 22 Feb 2019
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
        self.tabData.setTabText(0, 'SER results')
        
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x_1, self.data_y_1, color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3)
        ax.plot(self.data_x_2, self.data_y_2, color = 'black', linestyle = '-',
                    linewidth= 0.8, marker = 'o', markersize = 3)
            
        ax.set_title('SER results QPSK')
        ax.set_xlabel('SNR per symbol (dB)')
        ax.set_ylabel('Symbol error rate')
        ax.set_yscale('log')
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        
        
class IterationsAnalyzer_NewtonCooling(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to: Feedback applications/Newton Law Cooling 22 Feb 2019
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.  
    '''
    def __init__(self, data_x, data_y):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        self.iteration = 1  
        self.data_x = data_x
        self.data_y = data_y
        
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
        self.tabData.setTabText(0, 'Results')
        
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x[1], self.data_y[1], color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3)
        ax.plot(self.data_x[2], self.data_y[2], color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3) 
        ax.plot(self.data_x[3], self.data_y[3], color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3)
            
        ax.set_title('Cooling curves')
        ax.set_xlabel('time(sec)')
        ax.set_ylabel('Temp (stock) - C')
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
class IterationsAnalyzer_FabryPerot(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to: Optical applications/Interferometric devices/Fabry-Perot/FP Interferometer Steady State
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.  
    '''
    def __init__(self, data_x, data_y):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        self.iteration = 1  
        self.data_x = data_x
        self.data_y = data_y
        
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
        self.tabData.setTabText(0, 'Results')
        
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x, self.data_y, color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3)
            
        ax.set_title('FP resonator')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Transmitted power - W')
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        
class FilterAnalyzer(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to functional block: syslab_fb+_library/Analog Filter
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.   
    '''
    def __init__(self, freq, mag, phase, n, f_cut, filt_type):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        self.iteration = 1  
        self.freq = freq
        self.mag = mag
        self.phase = phase
        self.n = n
        self.f_cut = f_cut
        self.filt_type = filt_type
        
        #Setup background colors for frames
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame.setPalette(p)       
        p2 = self.graphFrame_2.palette()
        p2.setColor(self.graphFrame_2.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame_2.setPalette(p2)
        
        # Setup Matplotlib figures and toolbars
        # Layout/figure instances for Freq resp (mag)
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_xy)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        
        # Layout/figure instances for Freq resp (mag)
        self.graphLayoutPhase = QtWidgets.QVBoxLayout()
        self.figure_phase = plt.figure()
        self.canvas_phase = FigureCanvas(self.figure_phase)     
        self.toolbar_phase = NavigationToolbar(self.canvas_phase, self.tab_xy_2)
        self.graphLayoutPhase.addWidget(self.canvas_phase)
        self.graphLayoutPhase.addWidget(self.toolbar_phase)
        
        self.graphFrame.setLayout(self.graphLayout)  
        self.graphFrame_2.setLayout(self.graphLayoutPhase)
        
        # Setup tab titles
        self.tabData.setTabText(0, 'Frequency response (magnitude)')
        self.tabData.setTabText(1, 'Frequency response (phase)')
        
        # Plot figures
        # Mag response
        self.figure_phase.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure_phase.set_tight_layout(True)
        self.plot_phase_resp()
        self.canvas_phase.draw()
        # Phase response
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_mag_resp()
        self.canvas.draw()
        
    def plot_mag_resp(self):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.freq, self.mag, color = 'blue', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 1)
        
        #Add 3 dB line
        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()
        y = [-3, -3]
        x = [xmin, xmax]    
        ax.plot(x, y, color = 'red', linestyle = '--', linewidth= 0.8)         
        ax.text(x[1], y[1], '-3 dB', withdash=True, ha='center',
                                 va='center', style = 'italic', zorder = 25,
                                 bbox=dict(facecolor='white', edgecolor='red', alpha=1))
        # Add freq cut-off line
        y = [ymin, ymax]
        x = [self.f_cut, self.f_cut]    
        ax.plot(x, y, color = 'red', linestyle = '--', linewidth= 0.8)  
        ax.text(x[1], y[1], 'fc', withdash=True, ha='center',
                                 va='center', style='italic', zorder = 25,
                                 bbox=dict(facecolor='white', edgecolor='red', alpha=1))
            
        ax.set_title('Freq response (mag) - ' + str(self.filt_type))
        ax.set_xlabel('Freq (Hz)')
        ax.set_xscale('log')
        ax.set_yscale('linear')
        ax.set_ylabel('abs(H)-dB')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    def plot_phase_resp(self):
        ap = self.figure_phase.add_subplot(111, facecolor = '#f9f9f9')
        ap.clear()
        ap.plot(self.freq, self.phase, color = 'blue', linestyle = '--', linewidth= 0.8,
                                marker = 'o', markersize =1)
        
        # Add freq cut-off line
        ymin, ymax = ap.get_ylim()
        xmin, xmax = ap.get_xlim()
        y = [ymin, ymax]
        x = [self.f_cut, self.f_cut]    
        ap.plot(x, y, color = 'red', linestyle = '--', linewidth= 0.8)  
        ap.text(x[1], y[1], 'fc', withdash=True, ha='center',
                                 va='center', style='italic', zorder = 25, bbox=dict(facecolor='white', 
                                 edgecolor='red', alpha=1))
            
        ap.set_title('Freq response (phase) - ' + str(self.filt_type))
        ap.set_xlabel('Freq (Hz)')
        ap.set_xscale('log')
        ap.set_ylabel('angle(H)-deg')
        ap.grid(True)  
        ap.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ap.minorticks_on()
        ap.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_phase)
        
class FunctionalBlockStatusGUI(QtWidgets.QDialog, Ui_FunctionalBlockStatus):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_FunctionalBlockStatus.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        #Version tracking
        self.__version = 1
         
    def check_version(self):
        pass #No check needed for version 1
        
    def text_update(self, text):
        self.textEdit.append(text)
        
    def update_progress_bar(self, progress):
        self.progressBar.setValue(progress)
        
'''FUNCTIONS==========================================================================='''
    
def set_icon_window():
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLab_64.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
    
'''===================================================================================='''