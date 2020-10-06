'''
    SystemLab-Design Version 20.01
    Primary author: Marc Verreault
    E-mail: marc.verreault@systemlabdesign.com
    Copyright © 2019-2020 SystemLab Inc. All rights reserved.
    
    NOTICE================================================================================   
    This file is part of SystemLab-Design 20.01.
    
    SystemLab-Design 20.01 is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    SystemLab-Design 20.01 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SystemLab-Design 20.01.  If not, see <https://www.gnu.org/licenses/>.    
    ======================================================================================
    
    SystemLab module for port analyzer(GUI) classes: SignalAnalogGeneric
'''
import os
import config
gui_ui_path = config.root_path

import sys # MV 20.01.r2 24-Feb-20
import traceback # MV 20.01.r2 24-Feb-20

# MV 20.01.r1 29-Oct-2019
# Import config_port_viewers as cfg_analog
import importlib
cfg_port_viewers_path = str('syslab_config_files.config_port_viewers')
cfg_analog = importlib.import_module(cfg_port_viewers_path)
cfg_special_path = str('syslab_config_files.config_special')
cfg_special = importlib.import_module(cfg_special_path)

import numpy as np
import matplotlib

from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib.pyplot as plt
# Method for embedding Matplotlib canvases into Qt-designed QDialog interfaces
# Ref: https://matplotlib.org/gallery/user_interfaces/embedding_in_qt_sgskip.html
# Accessed: 11 Feb 2019
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

qtAnalogPortDataViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'AnalogDataViewer.ui')
qtAnalogPortDataViewerFile = os.path.normpath(qtAnalogPortDataViewerFile)
Ui_PortDataWindow_Analog, QtBaseClass = uic.loadUiType(qtAnalogPortDataViewerFile)

#import matplotlib as mpl
matplotlib.rcParams['figure.dpi'] = 80

# MV 20.01.r3 15-Jun-20
style_spin_box = """QSpinBox {color: darkBlue; background: white;
                              selection-color: darkBlue;
                              selection-background-color: white;}"""


class AnalogPortDataAnalyzer(QtWidgets.QDialog, Ui_PortDataWindow_Analog):
    '''
    Analog signal format:
    portID(0), signal_type(1), sample_rate(2), time_array(3), amplitude_array(4)    
    '''
    def __init__(self, signal_data, fb_name, port_name, direction, design_settings):
        QtWidgets.QDialog.__init__(self)
        Ui_PortDataWindow_Analog.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)       
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        self.setStyleSheet(cfg_special.global_font) # MV 20.01.r1 17-Dec-2019
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.fb_name = fb_name
        self.port_name = port_name
        self.direction = direction
        
        # MV 20.01.r3 13-Jun-20 Added functional block and port data info to
        # Window title box
        self.setWindowTitle('Analog signal data analyzer (' + 
                            str(self.fb_name) + ', Port: ' + 
                            str(self.port_name) + ', Dir: ' + 
                            str(self.direction) + ')')
        #self.iteration = 1  
        self.signals = signal_data
        
        # MV 20.01.r3 15-Jun-20 Set iteration to reflect main application setting
        # (iterators spin box)        
        self.signals = signal_data        
        current_iter = int(design_settings['current_iteration'])
        if (current_iter - 1) <= len(self.signals):
            self.iteration = current_iter
        else:
            self.iteration = int(len(self.signals))
        
        '''Time data tab (dataFrame)==================================================='''
        #Top level settings
        self.samples = design_settings['num_samples']
        self.totalSamplesTime.setText(str(format(self.samples, '0.3E')))
        self.s_period = design_settings['sampling_period']
        self.samplingPeriod.setText(str(format(self.s_period, '0.3E')))
        self.time_win = design_settings['time_window']
        self.timeWindow.setText(str(format(self.time_win, '0.3E')))     
        #Iterations group box (Time data tab)
        iterations = len(signal_data)   
        self.spinBoxTime.setMaximum(iterations)
        self.spinBoxTime.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsTime.setText(str(iterations))        
        self.spinBoxTime.valueChanged.connect(self.value_change_time)       
#        #Signal type group box (Time data)
#        self.signalCheckBox.stateChanged.connect(self.check_signal_changed_time)
#        self.noiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
#        self.sigandnoiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
#        self.radioButtonMag.toggled.connect(self.check_signal_changed_time)        
#        self.radioButtonLinearPwr.toggled.connect(self.check_signal_changed_time)
#        self.radioButtonLogPwr.toggled.connect(self.check_signal_changed_time)     
        #Plot settings (Time data)
        self.checkBoxMajorGrid.stateChanged.connect(self.check_signal_changed_time)
        self.checkBoxMinorGrid.stateChanged.connect(self.check_signal_changed_time)
        self.checkBoxLegend.stateChanged.connect(self.check_signal_changed_time) 
        #Y-axis axis settings group box (Time data) 
        self.actionTimeWindowYAxis.clicked.connect(self.update_time_axis) 
        #Time axis settings group box (Time data)
        self.actionTimeWindow.clicked.connect(self.update_time_axis)
    
        '''Freq data tab (dataFrameFreq)==============================================='''
        #Top level settings (Main sub-tab)  
        self.totalSamplesFreq.setText(str(format(design_settings['num_samples'], '0.3E'))) 
        self.fs = design_settings['sampling_rate']
        self.samplingRate.setText(str(format(self.fs, '0.3E')))
        #Iterations group box (Main sub-tab)        
        self.spinBoxFreq.setMaximum(iterations)
        self.spinBoxFreq.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsFreq.setText(str(iterations))
        self.spinBoxFreq.valueChanged.connect(self.value_change_freq) 
        #Signal type group box (Main sub-tab) 
#        self.signalCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
#        self.noiseCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
#        self.sigandnoiseCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
#        self.radioButtonLinearFreq.toggled.connect(self.check_signal_changed_freq)
#        self.radioButtonLinearFreqSpectral.toggled.connect(self.check_signal_changed_freq)
#        self.radioButtonLogFreq.toggled.connect(self.check_signal_changed_freq) 
#        self.radioButtonLogFreqSpectral.toggled.connect(self.check_signal_changed_freq) 
        #Plot settings (Main sub-tab) 
        self.checkBoxMajorGridFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.checkBoxMinorGridFreq.stateChanged.connect(self.check_signal_changed_freq)        
        self.checkBoxLegendFreq.stateChanged.connect(self.check_signal_changed_freq) 
        #Y-axis axis settings group box (Main sub-tab) 
        self.actionFreqWindowYAxis.clicked.connect(self.updateAxisFreq)  
        #Freq axis settings group box (Main sub-tab)
        self.checkBoxDisplayNegFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.actionFreqWindow.clicked.connect(self.updateAxisFreq)
        
        '''Signal data tab (dataFrameSignal)==========================================='''
        #Iterations group box
        iterations = len(signal_data)   
        self.spinBoxSignalData.setMaximum(iterations)
        self.spinBoxSignalData.setValue(self.iteration)
        self.spinBoxSignalData.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsSignalData.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iteration_change_signal_data)
        #Domain setting group box
        self.radioButtonSigFreq.toggled.connect(self.update_signal_data)
        self.radioButtonSigTime.toggled.connect(self.update_signal_data)
#        #E-field signal format group box
#        self.radioButtonComplexSignalData.toggled.connect(self.update_signal_data)
#        self.radioButtonPolarSignalData.toggled.connect(self.update_signal_data)
        #Adjust samples group box
        self.totalSamplesSignalData.setText(str(format(self.samples, 'n')))
        self.adjustedSamplesSignalData.setText(str(format(self.samples, 'n')))
        self.minIndexSignalData.setText(str(1))
        self.maxIndexSignalData.setText(str(format(self.samples, 'n')))
        self.actionSetIndicesSignalData.clicked.connect(self.update_signal_data)
        #View settings group box
        self.linewidthSignalData.setText(str(60))
        self.actionSetLinewidthSignalData.clicked.connect(self.update_signal_data)
        
        '''Signal metrics data tab====================================================='''
        #Iterations group box
        iterations = len(signal_data)   
        self.spinBoxSignalMetrics.setMaximum(iterations)
        self.spinBoxSignalMetrics.setValue(self.iteration)
        self.spinBoxSignalMetrics.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsSignalMetrics.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iteration_change_signal_metrics)
        
        '''Setup initial data for iteration 1 (default)================================'''
        signal_default = self.signals[self.iteration]    
        self.time = signal_default[3] #Time sampling points
        self.signal = signal_default[4]
        self.sig_type = signal_default[1]
        
        '''Setup frequency domain analysis============================================='''
        self.n = int(len(self.signal))
        T = self.n/self.fs #
        k = np.arange(self.n)
        self.frq = k/T # Positive/negative freq (double sided)
        self.frq_pos = self.frq[range(int(self.n/2))] # Positive freq only     
        #FFT computations (signal, noise, signal+noise)
        self.Y = np.fft.fft(self.signal)
        self.Y_pos = self.Y[range(int(self.n/2))]
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.Y_pos = self.Y_pos*np.sqrt(2)
        self.Y_pos[0] = self.Y_pos[0]/np.sqrt(2) # DC component is not doubled

        '''Setup background colors for frames=========================================='''
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (frame bkrd clr)
        color = QtGui.QColor(cfg_analog.analog_frame_background_color) 
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), color)
        self.graphFrame.setPalette(p)       
        p2 = self.dataFrame.palette()
        p2.setColor(self.dataFrame.backgroundRole(), color)
        self.dataFrame.setPalette(p2)
        p3 = self.graphFrameFreq.palette() 
        p3.setColor(self.graphFrameFreq.backgroundRole(), color)
        self.graphFrameFreq.setPalette(p3)
        p4  = self.dataFrameFreq.palette() 
        p4.setColor(self.dataFrameFreq.backgroundRole(), color)
        self.dataFrameFreq.setPalette(p4)
        p7  = self.dataFrameSignal.palette() 
        p7.setColor(self.dataFrameSignal.backgroundRole(), color)
        self.dataFrameSignal.setPalette(p7)
        p8  = self.dataFrameMetrics.palette() 
        p8.setColor(self.dataFrameMetrics.backgroundRole(), color)
        self.dataFrameMetrics.setPalette(p8) 
        
        '''Setup matplotlib figures and toolbars======================================='''
        #Time data tab
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_time)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        #Freq data tab
        self.graphLayoutFreq = QtWidgets.QVBoxLayout()
        self.figure_freq = plt.figure()
        self.canvas_freq = FigureCanvas(self.figure_freq)     
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self.tab_freq)
        self.graphLayoutFreq.addWidget(self.canvas_freq)
        self.graphLayoutFreq.addWidget(self.toolbar_freq) 
        self.graphFrameFreq.setLayout(self.graphLayoutFreq) 
        
        '''Plot default graphs========================================================='''
        self.tabData.setCurrentWidget(self.tab_freq)
        self.figure_freq.set_tight_layout(True)
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        self.tabData.setCurrentWidget(self.tab_time) 
        self.figure.set_tight_layout(True)
        self.plot_time_domain(0)
        self.canvas.draw()
        
        '''Prepare default data for signal data viewer================================='''
        self.update_signal_data()
        self.update_signal_metrics()
        #Return to time tab
        self.tabData.setCurrentWidget(self.tab_time)
    
    '''Time data tab (plotting methods)================================================'''
    def value_change_time(self):
        new_iteration = int(self.spinBoxTime.value())
        signal_updated = self.signals[new_iteration]
        self.signal = signal_updated[4]  
        self.tabData.setCurrentWidget(self.tab_time)       
        self.plot_time_domain(0)
        self.canvas.draw()
        
    def check_signal_changed_time(self):
        self.tabData.setCurrentWidget(self.tab_time)       
        self.plot_time_domain(0)
        self.canvas.draw()
        
    def update_time_axis(self):
        self.plot_time_domain(1)
        self.canvas.draw()
        
    def plot_time_domain(self, axis_adjust):
        try:
            self.figure.clf() #MV Rel 20.01.r1 15-Sep-19
            # MV 20.01.r1 Added new feature to select plot area background color
            back_color = cfg_analog.analog_time_plot_back_color
            ax = self.figure.add_subplot(111, facecolor = back_color)
            ax.clear()
                
            if axis_adjust == 1:
                if self.minTime.text() and self.maxTime.text():
                    start_time = self.minTime.text()
                    end_time = self.maxTime.text()
                    ax.set_xlim(float(start_time), float(end_time))
                if self.startYAxisTime.text() and self.endYAxisTime.text():
                    start_val = self.startYAxisTime.text()
                    end_val = self.endYAxisTime.text()
                    ax.set_ylim(float(start_val), float(end_val))
                
            ax.set_ylabel('Magnitude')
            ax.plot(self.time, self.signal, 
                    color = cfg_analog.analog_time_signal_color, 
                    linestyle = cfg_analog.analog_time_signal_linestyle,
                    linewidth = cfg_analog.analog_time_signal_linewidth, 
                    marker = cfg_analog.analog_time_signal_marker, 
                    markersize = cfg_analog.analog_time_signal_markersize,
                    label = 'Analog signal')
            
            # MV 19.02.r2 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            ax.set_title('Time data - ' + str(self.sig_type) 
                         + ' (' + str(self.fb_name) + ', Port:' 
                         + str(self.port_name)
                         + ', Dir:' + str(self.direction) + ')')
            
            ax.set_xlabel('Time (sec)')
            ax.set_aspect('auto')
            ax.format_coord = self.format_coord_time
            
            # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks    
            ax.xaxis.label.set_color(cfg_analog.analog_time_labels_axes_color)
            ax.yaxis.label.set_color(cfg_analog.analog_time_labels_axes_color)
            ax.tick_params(axis='both', which ='both', 
                                colors=cfg_analog.analog_time_labels_axes_color)
            
            # MV 20.01.r1 Linked plot settings to config file variables (to provide ability to
            # manage look and feel of plots)    
            if self.checkBoxMajorGrid.checkState() == 2:
                ax.grid(True)  
                ax.grid(which='major', 
                        linestyle = cfg_analog.analog_time_maj_grid_linestyle, 
                        linewidth = cfg_analog.analog_time_maj_grid_linewidth, 
                        color = cfg_analog.analog_time_maj_grid_color)
           
            if self.checkBoxMinorGrid.checkState() == 2:
                ax.minorticks_on()
                ax.grid(which='minor', 
                        linestyle = cfg_analog.analog_time_min_grid_linestyle, 
                        linewidth = cfg_analog.analog_time_min_grid_linewidth, 
                        color = cfg_analog.analog_time_min_grid_color)
                
            if self.checkBoxLegend.isChecked() == 1:
                ax.legend()
        
        except: # MV 20.01.r2 24-Feb-20
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error plotting time domain signals')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Analog port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
    
    def format_coord_time(self, x, y):
        return 'Time=%0.7E, Mag=%0.7E' % (x, y)
    
    '''Freq data tab (plotting methods)================================================'''    
    def value_change_freq(self):
        new_iteration = int(self.spinBoxFreq.value())
        signal_updated = self.signals[new_iteration]   
        self.Y = np.fft.fft(signal_updated[4])
        self.Y_pos = self.Y[range(int(self.n/2))]
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.Y_pos = self.Y_pos*np.sqrt(2)
        self.Y_pos[0] = self.Y_pos[0]/np.sqrt(2) # DC component is not doubled
        self.tabData.setCurrentWidget(self.tab_freq)       
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        
    def check_signal_changed_freq(self):
        self.tabData.setCurrentWidget(self.tab_freq)       
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        
    def updateAxisFreq(self):
        self.plot_freq_domain(1)
        self.canvas_freq.draw()
        
    def plot_freq_domain(self, axis_adjust):
        try:
            self.figure_freq.clf() #MV Rel 20.01.r1 15-Sep-19
            # MV 20.01.r1 Added new feature to select plot area background color
            back_color = cfg_analog.analog_freq_plot_back_color
            self.af = self.figure_freq.add_subplot(111, facecolor = back_color)
            self.af.clear()  
            
            if axis_adjust == 1:
                if self.minFreq.text() and self.maxFreq.text():
                    start_freq = self.minFreq.text()
                    end_freq = self.maxFreq.text()
                    self.af.set_xlim(float(start_freq), float(end_freq))
                if self.startYAxisFreq.text() and self.endYAxisFreq.text():
                    start_val = self.startYAxisFreq.text()
                    end_val = self.endYAxisFreq.text()
                    self.af.set_ylim(float(start_val), float(end_val))    
                
            self.af.set_ylabel('Abs')
                    
            # MV 20.01.r1 Linked plot settings to config file variables (to provide ability to
            # manage look and feel of plots) 
            if self.checkBoxDisplayNegFreq.checkState() == 2:
                self.af.plot(self.freq, np.abs(self.Y)/self.n, 
                             color = cfg_analog.analog_freq_signal_color, 
                             linestyle = cfg_analog.analog_freq_signal_linestyle, 
                             linewidth= cfg_analog.analog_freq_signal_linewidth, 
                             marker = cfg_analog.analog_freq_signal_marker,
                             markersize = cfg_analog.analog_req_signal_markersize,
                             label = 'Analog signal') 
            else:
                self.af.plot(self.frq_pos, np.abs(self.Y_pos)/self.n, 
                             color = cfg_analog.analog_freq_signal_color, 
                             linestyle = cfg_analog.analog_freq_signal_linestyle, 
                             linewidth = cfg_analog.analog_freq_signal_linewidth, 
                             marker = cfg_analog.analog_freq_signal_marker,
                             markersize = cfg_analog.analog_freq_signal_markersize,
                             label = 'Analog signal')             
            
            
            # MV 19.02.r2 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.af.set_title('Freq data - ' + str(self.sig_type) + ' (' + str(self.fb_name) + ', Port:' 
                                                 + str(self.port_name) +
                                              ', Dir:' + str(self.direction) + ')')
    
            self.af.set_xlabel('Freq (Hz)')
            self.af.set_aspect('auto')
            self.af.format_coord = self.format_coord_freq
            
            # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks    
            self.af.xaxis.label.set_color(cfg_analog.analog_freq_labels_axes_color)
            self.af.yaxis.label.set_color(cfg_analog.analog_freq_labels_axes_color)
            self.af.tick_params(axis='both', which ='both', 
                                colors=cfg_analog.analog_freq_labels_axes_color)
            
            # MV 20.01.r1 Linked plot settings to config file variables (to provide ability to
            # manage look and feel of plots)  
            if self.checkBoxMajorGridFreq.checkState() == 2:
                self.af.grid(True)  
                self.af.grid(which='major', 
                             linestyle = cfg_analog.analog_freq_maj_grid_linestyle, 
                             linewidth = cfg_analog.analog_freq_maj_grid_linewidth, 
                             color = cfg_analog.analog_freq_maj_grid_color)
           
            if self.checkBoxMinorGridFreq.checkState() == 2:
                self.af.minorticks_on()
                self.af.grid(which='minor', 
                             linestyle = cfg_analog.analog_freq_min_grid_linestyle, 
                             linewidth = cfg_analog.analog_freq_min_grid_linewidth, 
                             color = cfg_analog.analog_freq_min_grid_color)
                
        except: # MV 20.01.r2 24-Feb-20
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error plotting frequency domain signals')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Analog port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
        
    def format_coord_freq(self, x, y):
        return 'Freq=%0.7E, Abs=%0.7E' % (x, y)
                
    '''Signal data tab=========================================================
    portID(0), signal_type(1), sample_rate(2), time_array(3), amplitude_array(4)
    '''
    def iteration_change_signal_data(self):
        new_iteration = int(self.spinBoxSignalData.value())
        signal_updated = self.signals[new_iteration]
        self.signal = signal_updated[4] #Electrical amplitudes
        self.update_signal_data()
        
    def update_signal_data(self):
        try:
            self.tabData.setCurrentWidget(self.tab_signal)
            self.signalBrowser.clear()
            #Signal data (base data)
            self.font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
            self.font_normal = QtGui.QFont("Arial", 8, QtGui.QFont.Normal)
            self.signalBrowser.setCurrentFont(self.font_bold)
            self.signalBrowser.setTextColor(QtGui.QColor('#007900'))
            i = int(self.spinBoxSignalData.value())
            #Signal data type, iteration # and fb/port information
            self.signalBrowser.append('Signal analog - Iteration '+str(i))
            self.signalBrowser.append(self.fb_name + ', Port:' +
                                self.port_name + ', Dir:' + str(self.direction))
            self.signalBrowser.setCurrentFont(self.font_normal)
            self.signalBrowser.setTextColor(QtGui.QColor('#000000'))
            self.signalBrowser.append('Sample rate (Hz): ' + str(self.fs))
            #Signal data units
            self.signalBrowser.setCurrentFont(self.font_bold)
            if self.radioButtonSigTime.isChecked() == 1:
                self.signalBrowser.append('Signal analog (index, time(s), magnitude):')
            else:
                self.signalBrowser.append('Signal analog (index, freq(Hz), abs):') 
            self.signalBrowser.setCurrentFont(self.font_normal)
            
            #Adjust for new index range (if required)
            self.start_index = int(self.minIndexSignalData.text())
            self.end_index = int(self.maxIndexSignalData.text()) + 1     
            index_array = np.arange(self.start_index, self.end_index, 1)
            array_size = self.end_index - self.start_index
            self.adjustedSamplesSignalData.setText(str(format(array_size, 'n')))
            
            #Prepare structured array for string output to text browser
            data = np.zeros(array_size, dtype={'names':('index', 'x', 'y'),
                                                   'formats':('i4', 'f8', 'f8')})
          
            data['index'] = index_array
            
            if self.radioButtonSigTime.isChecked() == 1:
                data['x'] = self.time[self.start_index-1:self.end_index-1]
                data['y'] = self.signal[self.start_index-1:self.end_index-1]
            else:
                data['x'] = self.frq[self.start_index-1:self.end_index-1]
                # MV 20.01.r3 18-Sep-20 Added division by n (normalization)
                data['y'] = self.Y[self.start_index-1:self.end_index-1]/self.n
            
            self.linewidth = 60
            if self.linewidthSignalData.text():
                self.linewidth = int(self.linewidthSignalData.text())
    
            self.signalBrowser.append(np.array2string(data, max_line_width = self.linewidth))
            
            cursor = self.signalBrowser.textCursor()
            cursor.setPosition(0)
            self.signalBrowser.setTextCursor(cursor)
            
        except: # MV 20.01.r2 24-Feb-20
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error displaying signal data')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Analog  port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()

    '''Signal metrics tab=============================================================='''
    def iteration_change_signal_metrics(self):
        new_iteration = int(self.spinBoxSignalMetrics.value())
        signal_updated = self.signals[new_iteration]
        #self.carrier = signal_updated[2]
        self.signal = signal_updated[5] #Electrical amplitudes
        #self.noise = signal_updated[6]
        self.update_signal_metrics() 
    
    def update_signal_metrics(self):
        sig_mean = np.mean(self.signal)
        self.signalMean.setText(str(format(sig_mean, '0.3E')))
        sig_var = np.var(self.signal)
        self.signalVar.setText(str(format(sig_var, '0.3E')))
        sig_std_dev = np.std(self.signal)
        self.signalStdDev.setText(str(format(sig_std_dev, '0.3E')))
    
        '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_freq)
        
'''FUNCTIONS==========================================================================='''
#def set_mpl_cursor():
#    mplcursors.cursor(multiple=False).connect("add", 
#                     lambda sel: sel.annotation.get_bbox_patch().set(fc="lightyellow", alpha=1))
    
def set_icon_window():
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLabIcon128.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
    
'''===================================================================================='''
