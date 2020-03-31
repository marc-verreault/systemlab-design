'''
    SystemLab-Design Version 20.01
    Primary author: Marc Verreault
    Copyright (C) 2019-2020 SystemLab Inc. All rights reserved.
    
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

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter #Used for smoothing 
# Method for embedding Matplotlib canvases into Qt-designed QDialog interfaces
# Ref: https://matplotlib.org/gallery/user_interfaces/embedding_in_qt_sgskip.html
# Accessed: 11 Feb 2019
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Template for signal space analyzer (Note: File was built from QTCreator)
qtSignalSpaceViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'SignalSpaceViewer.ui')
qtSignalSpaceViewerFile = os.path.normpath(qtSignalSpaceViewerFile)
Ui_Signal_Space_Electrical, QtBaseClass = uic.loadUiType(qtSignalSpaceViewerFile)

# Template for generic 2D graphs (up to 5 tabs available,  more can be added)
qtIterationsViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'IterationsViewer.ui')
qtIterationsViewerFile = os.path.normpath(qtIterationsViewerFile)
Ui_Iterations_Analysis, QtBaseClass = uic.loadUiType(qtIterationsViewerFile)

# Template for X-Y quick graph
qtXYViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'XYViewer.ui')
qtXYViewerFile = os.path.normpath(qtXYViewerFile)
Ui_XY_Analysis, QtBaseClass = uic.loadUiType(qtXYViewerFile)

# Template for functional block status
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
    def __init__(self, title, signal_data_i, signal_data_q, signals_ref_i, signals_ref_q,
                 evm_p_res, evm_db_res):
        QtWidgets.QDialog.__init__(self)
        Ui_Signal_Space_Electrical.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        self.iteration = 1  
        self.title = title
        self.signals_i = signal_data_i
        self.signals_q = signal_data_q
        self.signals_ref_i = signals_ref_i
        self.signals_ref_q = signals_ref_q
        self.evm_p_res = evm_p_res
        self.evm_db_res = evm_db_res
        self.setWindowTitle('Signal space viewer: ' + str(title))
        
        # I-Q tab=========================================================================
        iterations = len(signal_data_i)   
        self.spinBoxTime.setMaximum(iterations)
        self.totalIterationsTime.setText(str(iterations))
        self.spinBoxTime.valueChanged.connect(self.valueChangeTime)
        num_sampling_points = len(self.signals_i[1])   
        self.totalSamplesTime.setText(str(format(num_sampling_points, '0.3E')))
        self.evm_per.setText(str(format(self.evm_p_res[1], '0.2f')))
        self.evm_db.setText(str(format(self.evm_db_res[1], '0.2f')))
        self.signalCheckBox.stateChanged.connect(self.checkSignalChangedIQ)
        self.sigandnoiseCheckBox.stateChanged.connect(self.checkSignalChangedIQ)
        self.checkBoxMajorGrid.stateChanged.connect(self.checkSignalChangedIQ)
        self.checkBoxMinorGrid.stateChanged.connect(self.checkSignalChangedIQ) 
        # MV 19.12.r1 26-Oct-19 - New features for managing data/display colors/markers
        self.comboBoxDisplayColor.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.checkBoxSquare.stateChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxMarkerRef.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxColorRef.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxMarkerSig.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxColorSig.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxColorMajor.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxColorMinor.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxWidthMajor.currentIndexChanged.connect(self.checkSignalChangedIQ)
        self.comboBoxWidthMinor.currentIndexChanged.connect(self.checkSignalChangedIQ)
        
        # MV 19.12.r1 26-Oct-19 (New tab for density/heat map)============================
        self.spinBoxTime_2.setMaximum(iterations)
        self.totalIterationsTime_2.setText(str(iterations))
        self.spinBoxTime_2.valueChanged.connect(self.valueChangeTime_2)
        self.totalSamplesTime_2.setText(str(format(num_sampling_points, '0.3E')))        
        self.evm_per_2.setText(str(format(self.evm_p_res[1], '0.2f')))
        self.evm_db_2.setText(str(format(self.evm_db_res[1], '0.2f')))
        self.grid_size.setText(str(500))
        self.gaussianFilterSigma.setText(str(1))
        self.pushButtonUpdateGrid.clicked.connect(self.checkSignalChangedDensity)
        self.comboBoxColorMap.currentIndexChanged.connect(self.checkSignalChangedDensity)
        self.pushButtonUpdateHeatMap.clicked.connect(self.checkSignalChangedDensity)
        self.checkBoxMajorGrid_2.stateChanged.connect(self.checkSignalChangedDensity)
        self.checkBoxMinorGrid_2.stateChanged.connect(self.checkSignalChangedDensity)
        self.comboBoxColorMajor_2.currentIndexChanged.connect(self.checkSignalChangedDensity)
        self.comboBoxColorMinor_2.currentIndexChanged.connect(self.checkSignalChangedDensity) 
        self.comboBoxWidthMajor_2.currentIndexChanged.connect(self.checkSignalChangedDensity)
        self.comboBoxWidthMinor_2.currentIndexChanged.connect(self.checkSignalChangedDensity)
        
        # MV 19.12.r1 26-Nov-19 
        self.tabData.currentChanged.connect(self.change_tab_event)

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
        # MV 19.12.r1 (new views for density plots)
        p3 = self.graphFrame_2.palette() 
        p3.setColor(self.graphFrame_2.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame_2.setPalette(p3)       
        p4 = self.dataFrame_2.palette()
        p4.setColor(self.dataFrame_2.backgroundRole(), QtGui.QColor(252,252,252))
        self.dataFrame_2.setPalette(p4)
        
        #Setup matplotlib figures and toolbars
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_xy)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)  
        
        # MV 19.12.r1 (new views for density plots)=======================================
        self.graphLayout_2 = QtWidgets.QVBoxLayout()
        self.figure_2 = plt.figure()
        self.canvas_2 = FigureCanvas(self.figure_2)     
        self.toolbar_2 = NavigationToolbar(self.canvas_2, self.tab_density)
        self.graphLayout_2.addWidget(self.canvas_2)
        self.graphLayout_2.addWidget(self.toolbar_2)
        self.graphFrame_2.setLayout(self.graphLayout_2)               
        self.tabData.setCurrentWidget(self.tab_density) 
        self.figure_2.set_tight_layout(True)
        self.plot_density()
        self.canvas_2.draw() 
        #self.tabData.setTabText(0, 'IQ Constellation: ' + str(title))
        #self.tabData.setTabText(1, 'Heat map: ' + str(title))
        #=================================================================================
        self.figure.set_tight_layout(True)
        self.plot_scatter()
        self.canvas.draw()
        self.tabData.setCurrentWidget(self.tab_xy) 
    
    '''I-Q tab========================================================================='''
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
        
    def checkSignalChangedIQ(self):    
        self.plot_scatter()
        self.canvas.draw()
        
    def plot_scatter(self):
        # Re-instantiate subplot & set background color
        self.figure.clf() # MV 19.12.r1 29_Oct-19
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        back_color = self.comboBoxDisplayColor.currentText()        
        self.ax.set_facecolor(back_color)
        # Plot reference symbol set
        if self.signalCheckBox.checkState() == 2:
            ref_color = self.comboBoxColorRef.currentText()
            ref_size = int(self.comboBoxMarkerRef.currentText())
            self.ax.plot(self.signal_ref_i, self.signal_ref_q, color=ref_color, linestyle='None',
                    linewidth=0.8, marker ='o', markersize=ref_size)
        # Plot received/recovered symbol set    
        if self.sigandnoiseCheckBox.checkState() == 2:
            sig_color = self.comboBoxColorSig.currentText()
            sig_size = int(self.comboBoxMarkerSig.currentText())
            self.ax.plot(self.signal_i, self.signal_q, color=sig_color, linestyle ='None', 
                    linewidth=0.8, marker ='o', markersize=sig_size)  
        #Set each axis to same min & max values   
        if self.checkBoxSquare.checkState() == 2:
            x_low, x_high = self.ax.get_xlim()
            y_low, y_high = self.ax.get_ylim()
            self.ax.set_ylim(min(x_low, y_low),max(x_high, y_high) )
            self.ax.set_xlim(min(x_low, y_low),max(x_high, y_high) ) 
            # Set the display aspect ratio to 1  
            # Ref: https://jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl/
            # Accessed 25-Oct-2019 - thanks to poster!
            self.ax.set_aspect(1.0/self.ax.get_data_ratio())
        # Add labels
        self.ax.set_xlabel('I (in phase)')
        self.ax.set_ylabel('Q (quadrature)')
        # Add grid line major (if enabled)
        if self.checkBoxMajorGrid.checkState() == 2:
            major_color = self.comboBoxColorMajor.currentText()
            major_width = float(self.comboBoxWidthMajor.currentText())
            self.ax.grid(True)  
            self.ax.grid(which='major', linestyle='-', 
                         linewidth=major_width, color=major_color)
        # Add grid line minor (if enabled)
        if self.checkBoxMinorGrid.checkState() == 2:
            self.ax.minorticks_on()
            minor_color = self.comboBoxColorMinor.currentText()
            minor_width = float(self.comboBoxWidthMinor.currentText())
            self.ax.grid(which='minor', linestyle='-', 
                         linewidth=minor_width, color=minor_color)
            
    '''Density plots==================================================================='''
    # New feature 19.12.r1 26-Oct-19           
    def valueChangeTime_2(self):
        new_iteration = int(self.spinBoxTime_2.value())       
        self.signal_i = self.signals_i[new_iteration]
        self.signal_q = self.signals_q[new_iteration]       
        self.evm_per_2.setText(str(format(self.evm_p_res[new_iteration], '0.2f')))
        self.evm_db_2.setText(str(format(self.evm_db_res[new_iteration], '0.2f')))        
        self.tabData.setCurrentWidget(self.tab_density)       
        self.plot_density()
        self.canvas_2.draw()
        
    def checkSignalChangedDensity(self):  
        self.plot_density()
        self.canvas_2.draw()
            
    def plot_density(self): 
        self.figure_2.clf() # MV 19.12.r1 29_Oct-19             
        self.ad = self.figure_2.add_subplot(111, facecolor = '#f9f9f9')
        self.ad.clear()
        color_map = self.comboBoxColorMap.currentText()
        # Set grid size for density plot
        if self.grid_size.text():
            n = int(self.grid_size.text())
        else:
            n = 500
        # Set sigma for filter
        if self.gaussianFilterSigma.text():
            s = float(self.gaussianFilterSigma.text())
        else:
            s = 1
        # Build histogram2d and apply data smoothing (Gaussian filter for imaging (scipy)
        # Code based on: https://stackoverflow.com/questions/2369492/generate-a-heatmap-
        # in-matplotlib-using-a-scatter-data-set (accessed 27-Oct-2019). Thanks to posters!
        try:
            dist, xedges, yedges = np.histogram2d(self.signal_i, self.signal_q, bins=n)
            dist = gaussian_filter(dist, sigma=s)
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]        
            self.ad.imshow(dist.T, extent=extent, origin='lower', cmap=color_map)
        except:
            pass
            #self.ad.imshow([0,0,0,0], extent=[0,0,0,0], origin='lower', cmap=color_map)
        #Set each axis to same min & max values   
#        x_low, x_high = self.ad.get_xlim()
#        y_low, y_high = self.ad.get_ylim()
#        self.ad.set_ylim(min(x_low, y_low),max(x_high, y_high) )
#        self.ad.set_xlim(min(x_low, y_low),max(x_high, y_high) )
        # Set the display aspect ratio to 1  
        # Ref: https://jdhao.github.io/2017/06/03/change-aspect-ratio-in-mpl/
        # Accessed 25-Oct-2019
#        self.ad.set_aspect(1.0/self.ad.get_data_ratio())        
        self.ad.set_xlabel('I (in phase)')
        self.ad.set_ylabel('Q (quadrature)')        
        # Add grid line major (if enabled)
        if self.checkBoxMajorGrid_2.checkState() == 2:
            major_color = self.comboBoxColorMajor_2.currentText()
            major_width = float(self.comboBoxWidthMajor_2.currentText())
            self.ad.grid(True)  
            self.ad.grid(which='major', linestyle='-', 
                         linewidth=major_width, color=major_color)
        # Add grid line minor (if enabled)
        if self.checkBoxMinorGrid_2.checkState() == 2:
            self.ad.minorticks_on()
            minor_color = self.comboBoxColorMinor_2.currentText()
            minor_width = float(self.comboBoxWidthMinor_2.currentText())
            self.ad.grid(which='minor', linestyle='-', 
                         linewidth=minor_width, color=minor_color)
    
    # MV 19.12.r1 26-Nov-2019       
    def change_tab_event(self):
        current_index = self.tabData.currentIndex()
        if current_index == 0: # tab_xy
            current_iteration = int(self.spinBoxTime_2.value())
            self.spinBoxTime.setValue(current_iteration)
        else:
            current_iteration = int(self.spinBoxTime.value())
            self.spinBoxTime_2.setValue(current_iteration)

    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_2)


class IterationsAnalyzer_BER_SER(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to: Electrical applications/QPSK Design/QPSK Design 22 Feb 2019
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.
    '''
    def __init__(self, data_x_1, data_y_1, data_x_2, data_y_2, title,
                         y_axis_name, x_axis_name, y_axis_scale, x_axis_scale, 
                         plot_1_label, plot_2_label):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.iteration = 1  
        self.data_x_1 = data_x_1
        self.data_y_1 = data_y_1
        self.data_x_2 = data_x_2
        self.data_y_2 = data_y_2 
        self.title = title
        self.y_axis_name = y_axis_name
        self.x_axis_name = x_axis_name
        self.x_axis_scale = x_axis_scale
        self.y_axis_scale = y_axis_scale
        self.plot_1_label = plot_1_label
        self.plot_2_label = plot_2_label
        
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
        self.tabData.setTabText(0, self.title)
        
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        self.figure.clf() # MV 19.12.r1 29_Oct-19
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x_1, self.data_y_1, color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3, label = self.plot_1_label)
        ax.plot(self.data_x_2, self.data_y_2, color = 'black', linestyle = '-',
                    linewidth= 0.8, marker = 'o', markersize = 3, label = self.plot_2_label)
            
        ax.set_title(self.title)
        ax.set_xlabel(self.x_axis_name)
        ax.set_ylabel(self.y_axis_name)
        ax.set_xscale(self.x_axis_scale)
        ax.set_yscale(self.y_axis_scale)
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        ax.legend(loc = 'upper right')
        
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
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
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
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        
class IterationsAnalyzer_Optical_Amp(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
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
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
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
        self.tabData.setTabText(0, 'Optical Amplifier Gain')
        
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x, self.data_y, color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3)
        ax.set_title('Amplifier gain')
        ax.set_xlabel('Input power (dBm)')
        ax.set_ylabel('Gain (dB)')
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        
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
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
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
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
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
        
class FBGAnalyzer(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to functional block: syslab_fb+_library/Analog Filter
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.   
    '''
    def __init__(self, wave, ref, trans, log_scale, z, n_profile):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.wave = wave
        self.ref = ref
        self.trans = trans
        self.log_scale = log_scale
        self.z = z
        self.n_profile = n_profile
        
        #Setup background colors for frames
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame.setPalette(p)       
        p2 = self.graphFrame_2.palette()
        p2.setColor(self.graphFrame_2.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame_2.setPalette(p2)
        
        # Setup Matplotlib figures and toolbars
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_xy)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)       
        self.graphFrame.setLayout(self.graphLayout)
        
        self.graphLayoutProfile = QtWidgets.QVBoxLayout()
        self.figure_profile = plt.figure()
        self.canvas_profile = FigureCanvas(self.figure_profile)     
        self.toolbar = NavigationToolbar(self.canvas_profile, self.tab_xy_2)
        self.graphLayoutProfile.addWidget(self.canvas_profile)
        self.graphLayoutProfile.addWidget(self.toolbar)       
        self.graphFrame_2.setLayout(self.graphLayoutProfile)        
        
        # Setup tab titles
        self.tabData.setCurrentWidget(self.tab_xy)
        self.tabData.setTabText(0, 'Reflection and transmission spectra (power)')
        self.tabData.setTabText(1, 'FBG index profile')
        
        # Plot figures
        self.figure_profile.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure_profile.set_tight_layout(True)
        self.plot_fbg_profile()
        self.canvas_profile.draw()        
            
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_fbg_spectra()
        self.canvas.draw()
    
    def plot_fbg_spectra(self):
        self.ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        self.ax.clear()
        if self.log_scale == 2:
            self.ref = 10*np.log10(self.ref)
            self.trans = 10*np.log10(self.trans)
        # Plot reflectivity
        self.ax.plot(self.wave, self.ref, color = 'blue', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 1, label = 'Reflectivity') 
        # Plot transmissivity
        self.ax2 = self.ax.twinx()
        self.ax2.plot(self.wave, self.trans, color = 'red', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 1, label = 'Transmissivity')
            
        self.ax.set_title('Transmission/Reflection Spectra')
        #https://stackoverflow.com/questions/14165344/matplotlib-coloring-axis-tick-labels/14165402
        self.ax.set_xlabel('Wavelength (nm)')
        self.ax.set_ylabel('Reflectivity', color = 'blue')
        if self.log_scale == 2:
            self.ax.set_ylabel('Reflectivity (dB)', color = 'blue')
            #self.ax.set_yscale('log')
        self.ax.tick_params(axis='y', colors='blue')
        self.ax2.set_ylabel('Transmissivity', color = 'red')
        if self.log_scale == 2:
            self.ax2.set_ylabel('Transmissivity (dB)', color = 'red')
            #self.ax2.set_yscale('log')
        self.ax2.tick_params(axis='y', colors='red')
        self.ax.set_aspect('auto')
        self.ax.grid(True)  
        self.ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        #self.ax.legend(loc='lower left')
        #self.ax2.legend(loc='upper left')
        
    def plot_fbg_profile(self):
        self.ap = self.figure_profile.add_subplot(111, facecolor = '#f9f9f9')
        self.ap.clear()
        self.ap.plot(self.z, self.n_profile, color = 'blue', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 1, label = 'Index modulation')
            
        self.ap.set_title('FBG index modulation profile')
        self.ap.set_xlabel('Z position (m)')
        self.ap.set_ylabel('Index')
        self.ap.set_aspect('auto')
        self.ap.grid(True)  
        self.ap.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        self.ap.minorticks_on()
        self.ap.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_profile)
        
        
class MZMAnalyzer(QtWidgets.QDialog, Ui_Iterations_Analysis):
    '''
    Linked to functional block: syslab_fb+_library/Mach-Zhender Modulator
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.   
    '''
    def __init__(self, v, e_field, e_field_bias, v_op):
        QtWidgets.QDialog.__init__(self)
        Ui_Iterations_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.v = v
        self.e_field = e_field
        self.e_field_bias = e_field_bias
        self.v_op = v_op
        
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
        self.graphFrame.setLayout(self.graphLayout)  
        #self.graphFrame_2.setLayout(self.graphLayoutPhase)
        
        # Setup tab titles
        self.tabData.setCurrentWidget(self.tab_xy)
        self.tabData.setTabText(0, 'Mach-Zhender modulator transfer function')
        #self.tabData.setTabText(1, 'Frequency response (phase)')
        
        # Plot figures
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_transfer_function()
        self.canvas.draw()
        
    def plot_transfer_function(self):
        self.ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        self.ax.clear()
        self.ax.plot(self.v, np.real(self.e_field), color = 'blue', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 0, label = 'E-field (real)')
                
        self.ax.plot(self.v, np.imag(self.e_field), color = 'red', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 0, label = 'E-field (imag)')
                
        self.ax.plot(self.v, np.abs(self.e_field)*np.abs(self.e_field), color = 'green', linestyle = '--', linewidth= 0.8,
                marker = 'o', markersize = 0, label = 'E-field (power)')
                
        self.ax.plot(self.v_op, np.abs(self.e_field_bias)*np.abs(self.e_field_bias), color = 'darkGreen', 
                     linestyle = '--', linewidth= 0, marker = 'o', markersize = 6, label = 'Operating point')
                
        self.ax.set_title('MZ modulator transfer function')
        self.ax.set_xlabel('V/Vpi')
        self.ax.set_ylabel('E-field')
        self.ax.set_aspect('auto')
        self.ax.grid(True)  
        self.ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        self.ax.legend(loc='lower right')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        
        
class X_Y_Analyzer(QtWidgets.QDialog, Ui_XY_Analysis):
    '''
    Used for quick graph feature
    Tab objects (QWidget) are named "tab_xy", "tab_xy_2", etc.
    Graph frame objects (QFrame) are named "graphFrame". "graphFrame_2", etc.
    '''
    def __init__(self, title, data_x_1, x_units, data_y_1, y_units):
        QtWidgets.QDialog.__init__(self)
        Ui_XY_Analysis.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        self.iteration = 1 
        self.title = title
        self.setWindowTitle('X-Y Quick View')
        self.data_x_1 = data_x_1
        self.data_y_1 = data_y_1
        self.x_units = x_units
        self.y_units = y_units
        
        #Setup background colors for frames
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), QtGui.QColor(252,252,252))
        self.graphFrame.setPalette(p)
        
        #Setup matplotlib figures and toolbars
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_xy)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        
        self.tabData.setTabText(0, str(self.title))
        self.tabData.setCurrentWidget(self.tab_xy)
        self.figure.tight_layout(pad=0.5, h_pad = 0.8)
        self.figure.set_tight_layout(True)
        self.plot_xy()
        self.canvas.draw()
        
    def plot_xy(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        ax.plot(self.data_x_1, self.data_y_1, color = 'blue', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 2)
        ax.set_title(str(self.title))
        ax.set_xlabel(str(self.x_units))
        ax.set_ylabel(str(self.y_units))
        ax.set_aspect('auto')
        ax.grid(True)  
        ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
        ax.minorticks_on()
        ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)        
        

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
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLabIcon128.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
    
'''===================================================================================='''