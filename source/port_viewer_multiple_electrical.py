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
    
    SystemLab module for port analyzer(GUI) classes: SignalAnalogElectrical
'''
import os
import config
gui_ui_path = config.root_path

import sys # MV 20.01.r2 24-Feb-20
import traceback # MV 20.01.r2 24-Feb-20

# MV 20.01.r1 29-Oct-2019
# Import config_port_viewers as cfg_m_elec
import importlib
cfg_port_viewers_path = str('syslab_config_files.config_port_viewers')
cfg_m_elec = importlib.import_module(cfg_port_viewers_path)
cfg_special_path = str('syslab_config_files.config_special')
cfg_special = importlib.import_module(cfg_special_path)

import numpy as np

from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib.pyplot as plt
# Method for embedding Matplotlib canvases into Qt-designed QDialog interfaces
# Ref: https://matplotlib.org/gallery/user_interfaces/embedding_in_qt_sgskip.html
# Accessed: 11 Feb 2019
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

qtElectricalMultiPortViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files',
                                              'ElectricalDataViewerMultiple.ui')
qtElectricalMultiPortViewerFile = os.path.normpath(qtElectricalMultiPortViewerFile)
Ui_MultiPortDataWindow_Electrical, QtBaseClass = uic.loadUiType(qtElectricalMultiPortViewerFile)

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 80

# https://matplotlib.org/api/ticker_api.html#matplotlib.ticker.Formatter
mpl.rcParams['axes.formatter.useoffset'] = False # Removes offset from all plots
mpl.rcParams['axes.formatter.limits'] = [-4, 4] # Limits for exponential notation

class ElectricalDataAnalyzerMultiplePort(QtWidgets.QDialog, Ui_MultiPortDataWindow_Electrical):
    '''
    Electrical signal format:
    portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4),
    amplitude_array(5), noise_array(6)    
    '''
    def __init__(self, signals, parameters, design_settings):
        QtWidgets.QDialog.__init__(self)
        Ui_MultiPortDataWindow_Electrical.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)       
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        self.setStyleSheet(cfg_special.global_font) # MV 20.01.r1 17-Dec-2019
        self.signals = signals
        self.parameters = parameters
        
        '''Time data tab (dataFrame)==================================================='''
        # TOP LEVEL SETTINGS--------------------------------------------------------------
        # MV 20.01.r2 2-Mar-20 IMPORTANT UPDATE
        # Core settings for port viewer are now derived from recived signal statistics
        # (previously was using design settings). Due to signal processing functions such 
        # as re-sampling, local settings for a functional block may be different from
        # project settings
        
        # Time-window must be same for all functional blocks (taken from design settings)
        self.time_win = design_settings['time_window']
        # Calculate number of samples from port signal (will usually be same as design settings)
        self.samples = len(self.signals[0][0][4])
        # Calculate sampling frequency (for signal)
        self.fs = self.samples/self.time_win
        # Calculate sampling period (for signal)       
        self.s_period = 1/self.fs
        #---------------------------------------------------------------------------------
        
        #self.samples = design_settings['num_samples'] MV 20.01.r2 2-Mar-20
        self.totalSamplesTime.setText(str(format(self.samples, '0.3E')))
        #self.s_period = design_settings['sampling_period'] MV 20.01.r2 2-Mar-20
        self.samplingPeriod.setText(str(format(self.s_period, '0.3E')))
        self.time_win = design_settings['time_window']
        self.timeWindow.setText(str(format(self.time_win, '0.3E')))     
        #Iterations group box (Time data tab)
        iterations = design_settings['iterations']  
        self.spinBoxTime.setMaximum(iterations)
        self.totalIterationsTime.setText(str(iterations))        
        self.spinBoxTime.valueChanged.connect(self.value_change_time)       
        #Signal type group box (Time data)
        self.radioButtonOverlay.toggled.connect(self.check_signal_changed_time)
        self.signalCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.noiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.sigandnoiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.radioButtonMag.toggled.connect(self.check_signal_changed_time)        
        self.radioButtonLinearPwr.toggled.connect(self.check_signal_changed_time)
        self.radioButtonLogPwr.toggled.connect(self.check_signal_changed_time)     
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
        #self.fs = design_settings['sampling_rate'] #MV 20.01.r2 2-Mar-20
        self.samplingRate.setText(str(format(self.fs, '0.3E')))
        #Iterations group box (Main sub-tab)        
        self.spinBoxFreq.setMaximum(iterations)
        self.totalIterationsFreq.setText(str(iterations))
        self.spinBoxFreq.valueChanged.connect(self.value_change_freq) 
        #Signal type group box (Main sub-tab) 
        self.radioButtonFreqOverlay.toggled.connect(self.check_signal_changed_freq)
        self.signalCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.noiseCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.sigandnoiseCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.radioButtonLinearFreq.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonLinearFreqSpectral.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonLogFreq.toggled.connect(self.check_signal_changed_freq) 
        self.radioButtonLogFreqSpectral.toggled.connect(self.check_signal_changed_freq) 
        #Plot settings (Main sub-tab) 
        self.checkBoxMajorGridFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.checkBoxMinorGridFreq.stateChanged.connect(self.check_signal_changed_freq)        
        self.checkBoxLegendFreq.stateChanged.connect(self.check_signal_changed_freq) 
        #Y-axis axis settings group box (Main sub-tab) 
        self.actionFreqWindowYAxis.clicked.connect(self.updateAxisFreq)  
        #Freq axis settings group box (Main sub-tab)
        self.checkBoxDisplayNegFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.actionFreqWindow.clicked.connect(self.updateAxisFreq)
        
        '''Setup initial data for iteration 1 (default)================================'''
        signal_default = self.signals[0]
        self.time = signal_default[0][4]
        self.sig = []
        self.noise = []
        for i in range(0, len(signal_default)):
            self.sig.append(signal_default[i][5])
            self.noise.append(signal_default[i][6])      
        
        '''Setup frequency domain analysis============================================='''
        # REF:  Fast Fourier Transform in matplotlib, 
        # An example of FFT audio analysis in matplotlib and the fft function.
        # Source: https://plot.ly/matplotlib/fft/(accessed 20-Mar-2018)  
        self.n = self.samples
        T = self.n/self.fs #
        k = np.arange(self.n)
        self.frq = k/T # Positive/negative freq (double sided)
        self.frq_pos = self.frq[range(int(self.n/2))] # Positive freq only     
        #FFT computations (signal, noise, signal+noise)        
        self.Y = []
        self.Y_pos = []
        self.N = []
        self.N_pos = []
        self.Y_N = []
        self.Y_N_pos = []
        for i in range(0, len(signal_default)):
            Y = np.fft.fft(signal_default[i][5])
            Y_pos = Y[range(int(self.n/2))]
            self.Y.append(Y)
            self.Y_pos.append(Y_pos)
            N = np.fft.fft(signal_default[i][6])
            N_pos = N[range(int(self.n/2))]
            self.N.append(N)
            self.N_pos.append(N_pos)
            Y_N = np.fft.fft(signal_default[i][5]+signal_default[i][6])
            Y_N_pos = Y_N[range(int(self.n/2))]
            self.Y_N.append(Y_N)
            self.Y_N_pos.append(Y_N_pos)

        '''Setup background colors for frames=========================================='''
        color = QtGui.QColor(cfg_m_elec.m_electrical_frame_background_color) 
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
        
        '''Setup matplotlib figures and toolbars======================================='''
        #Time data tab
        self.graphLayout = QtWidgets.QVBoxLayout()
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure = plt.figure(facecolor = cfg_m_elec.m_electrical_time_fig_back_color)
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_time)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        #Freq data tab
        self.graphLayoutFreq = QtWidgets.QVBoxLayout()
         # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure_freq = plt.figure(facecolor = cfg_m_elec.m_electrical_freq_fig_back_color)
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

        self.tabData.setCurrentWidget(self.tab_time)
    
    '''Time data tab (plotting methods)================================================'''
    def value_change_time(self):
        new_iteration = int(self.spinBoxTime.value())
        signal_updated = self.signals[new_iteration-1]
        self.sig = []
        self.noise = []
        for i in range(0, len(signal_updated)):
            self.sig.append(signal_updated[i][5])
            self.noise.append(signal_updated[i][6]) 
        #self.signal = signal_updated[5] #Electrical amplitudes
        #self.noise = signal_updated[6]
        #self.carrier = signal_updated[3] #MV 20.01.r1 (23-Sep-2019)
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
            m = len(self.signals[0])
            self.ax = []
            color = cfg_m_elec.m_electrical_time_plot_back_color
            if self.radioButtonOverlay.isChecked() == 1:           
                x_plot =  self.figure.add_subplot(1,1,1, facecolor = color)
                self.ax.append(x_plot) 
                self.ax[0].clear()
            else:
                for x in range(0, m):
                    x_plot =  self.figure.add_subplot(m,1,x+1, facecolor = color)
                    self.ax.append(x_plot)                                
                for x in range(0, m):
                    self.ax[x].clear()
            
            #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
            if self.radioButtonOverlay.isChecked() == 1:
                self.ax[0].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                       useOffset=False))
                self.ax[0].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                       useOffset=False))
            else:
                for x in range(0, m):
                    if x < m-1:
                        self.ax[x].xaxis.set_major_formatter(plt.NullFormatter())
                    else:
                        self.ax[x].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                           useOffset=False))
                        self.ax[x].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                           useOffset=False))
                
            if axis_adjust == 1:
                if self.minTime.text() and self.maxTime.text():
                    start_time = self.minTime.text()
                    end_time = self.maxTime.text()
                    if self.radioButtonOverlay.isChecked() == 1:
                        self.ax[0].set_xlim(float(start_time), float(end_time))
                    else:
                        for x in range(0, m):
                            self.ax[x].set_xlim(float(start_time), float(end_time))
                if self.startYAxisTime.text() and self.endYAxisTime.text():
                    start_val = self.startYAxisTime.text()
                    end_val = self.endYAxisTime.text()
                    if self.radioButtonOverlay.isChecked() == 1:
                        self.ax[0].set_ylim(float(start_val), float(end_val))
                    else:
                        for x in range(0, m):
                            self.ax[x].set_ylim(float(start_val), float(end_val))
                
            if self.radioButtonMag.isChecked() == 1:
                if self.radioButtonOverlay.isChecked() == 1:
                    self.ax[0].set_ylabel('Mag(V)')
                else:
                    for x in range(0, m):
                        self.ax[x].set_ylabel('Mag(V): p'+ str(x+1))
            
            elif self.radioButtonLinearPwr.isChecked() == 1: 
                if self.radioButtonOverlay.isChecked() == 1:
                    self.ax[0].set_ylabel('Power(W)')
                else:
                    for x in range(0, m):
                        self.ax[x].set_ylabel('Power(W): p'+ str(x+1))
            
            else:
                if self.radioButtonOverlay.isChecked() == 1:
                    self.ax[0].set_ylabel('Power(dBm)') 
                else:
                    for x in range(0, m):
                        self.ax[x].set_ylabel('Power(dBm): p'+ str(x+1))
            
            #Access port viewer settings for plot styles        
            self.colors_time = cfg_m_elec.m_electrical_time_signal_color
            self.colors_noise = cfg_m_elec.m_electrical_time_noise_color
            self.colors_sig_noise = cfg_m_elec.m_electrical_time_sig_noise_color
            self.linestyle_time = cfg_m_elec.m_electrical_time_signal_linestyle
            self.linestyle_noise = cfg_m_elec.m_electrical_time_noise_linestyle
            self.linestyle_sig_noise = cfg_m_elec.m_electrical_time_sig_noise_linestyle       
            self.linewidth_time = cfg_m_elec.m_electrical_time_signal_linewidth
            self.linewidth_noise = cfg_m_elec.m_electrical_time_noise_linewidth
            self.linewidth_sig_noise = cfg_m_elec.m_electrical_time_sig_noise_linewidth                  
            self.markers_time = cfg_m_elec.m_electrical_time_signal_marker
            self.markers_noise = cfg_m_elec.m_electrical_time_noise_marker
            self.markers_sig_noise = cfg_m_elec.m_electrical_time_sig_noise_marker
            self.markersize_time = cfg_m_elec.m_electrical_time_signal_markersize
            self.markersize_noise = cfg_m_elec.m_electrical_time_noise_markersize
            self.markersize_sig_noise = cfg_m_elec.m_electrical_time_sig_noise_markersize
    
            for i in range(0, m):
                sig = np.real(self.sig[i])
                noise = np.real(self.noise[i])
                sig_and_noise = sig + noise
                if self.signalCheckBox.checkState() == 2:
                    sig = self.adjust_units_for_plotting_time(sig)                
                    self.set_signal_plot_time_domain(self.time, sig, i+1)    
                if self.noiseCheckBox.checkState() == 2:
                    noise = self.adjust_units_for_plotting_time(noise)
                    self.set_noise_plot_time_domain(self.time, noise, i+1)                
                if self.sigandnoiseCheckBox.checkState() == 2:
                    sig_and_noise = self.adjust_units_for_plotting_time(sig+noise)
                    self.set_signal_and_noise_plot_time_domain(self.time, sig_and_noise, i+1)
    
            if self.radioButtonOverlay.isChecked() == 1:
                self.ax[0].set_title('Time data (all ports)')
                self.ax[0].set_xlabel('Time (sec)')
                self.ax[0].set_aspect('auto')
                self.ax[0].format_coord = self.format_coord_time
            else:
                for x in range(0, m):
                    #self.ax[x].set_title('Time data (Port ' + str(x+1) + ')')
                    if x == m-1:
                        self.ax[x].set_xlabel('Time (sec)')
                    self.ax[x].set_aspect('auto')
                    self.ax[x].format_coord = self.format_coord_time
                       
            if self.radioButtonOverlay.isChecked() == 1:
                self.ax[0].xaxis.label.set_color(cfg_m_elec.m_electrical_time_labels_axes_color)
                self.ax[0].yaxis.label.set_color(cfg_m_elec.m_electrical_time_labels_axes_color)
                self.ax[0].tick_params(axis='both', which ='both', 
                                colors=cfg_m_elec.m_electrical_time_labels_axes_color)
            else:
                for x in range(0, m):
                    if x == m-1:
                        self.ax[x].xaxis.label.set_color(cfg_m_elec.m_electrical_time_labels_axes_color)
                        self.ax[x].yaxis.label.set_color(cfg_m_elec.m_electrical_time_labels_axes_color)
                        self.ax[x].tick_params(axis='both', which ='both', 
                                colors=cfg_m_elec.m_electrical_time_labels_axes_color)           
                
            if self.checkBoxMajorGrid.checkState() == 2:
                if self.radioButtonOverlay.isChecked() == 1:
                    self.ax[0].grid(True)  
                    self.ax[0].grid(which='major', 
                                    linestyle = cfg_m_elec.m_electrical_time_maj_grid_linestyle, 
                                    linewidth = cfg_m_elec.m_electrical_time_maj_grid_linewidth, 
                                    color = cfg_m_elec.m_electrical_time_maj_grid_color)                
                else:
                    for x in range(0, m):
                        self.ax[x].grid(True)  
                        self.ax[x].grid(which='major', 
                                        linestyle = cfg_m_elec.m_electrical_time_maj_grid_linestyle, 
                                        linewidth = cfg_m_elec.m_electrical_time_maj_grid_linewidth, 
                                        color = cfg_m_elec.m_electrical_time_maj_grid_color)
           
            if self.checkBoxMinorGrid.checkState() == 2:
                if self.radioButtonOverlay.isChecked() == 1:
                    self.ax[0].minorticks_on()
                    self.ax[0].grid(which='minor', 
                                    linestyle = cfg_m_elec.m_electrical_time_min_grid_linestyle, 
                                    linewidth = cfg_m_elec.m_electrical_time_min_grid_linewidth, 
                                    color = cfg_m_elec.m_electrical_time_min_grid_color)                
                else:
                    for x in range(0, m):
                        self.ax[x].minorticks_on()
                        self.ax[x].grid(which='minor', 
                                        linestyle = cfg_m_elec.m_electrical_time_min_grid_linestyle, 
                                        linewidth = cfg_m_elec.m_electrical_time_min_grid_linewidth, 
                                        color = cfg_m_elec.m_electrical_time_min_grid_color)
                
            if self.checkBoxLegend.isChecked() == 1:
                if self.radioButtonOverlay.isChecked() == 1:
                    self.ax[0].legend(loc='upper right') 
                else:
                    for x in range(0, m):
                        self.ax[x].legend(loc='upper right')
                        
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
            msg.setWindowTitle("Plotting error (Multi-channel electrical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
            
    #20.01.r1 2 Sep 19 - Added new functions for plotting=================================
    def adjust_units_for_plotting_time(self, signal):
        if self.radioButtonMag.isChecked() == 1:
            pass
        elif self.radioButtonLinearPwr.isChecked() == 1:
            signal = signal*signal
        else:
            if np.count_nonzero(signal) == np.size(signal): 
                signal = 10*np.log10(signal*signal*1e3)
            else:
                signal += 1e-30 #Set to very low value
                signal = 10*np.log10(signal*signal*1e3)  
        return signal
    
    def set_signal_plot_time_domain(self, time, signal, num):
        if self.radioButtonOverlay.isChecked() == 1:
            self.ax[0].plot(time, signal, 
                            color = self.colors_time[num-1], 
                            linestyle = self.linestyle_time[num-1], 
                            linewidth= self.linewidth_time[num-1], 
                            marker = self.markers_time[num-1], 
                            markersize = self.markersize_time[num-1],
                            label = 'Electrical signal (Port: ' + str(num) + ')')
        else:
            self.ax[num-1].plot(time, signal,
                                color = self.colors_time[0], 
                                linestyle = self.linestyle_time[0], 
                                linewidth= self.linewidth_time[0], 
                                marker = self.markers_time[0], 
                                markersize = self.markersize_time[0],
                                label = 'Electrical signal (Port: ' + str(num) + ')')
        
    def set_noise_plot_time_domain(self, time, signal, num):
        if self.radioButtonOverlay.isChecked() == 1:
            self.ax[0].plot(time, signal, 
                            color = self.colors_noise[num-1], 
                            linestyle = self.linestyle_noise[num-1], 
                            linewidth = self.linewidth_noise[num-1], 
                            marker = self.markers_noise[num-1],
                            markersize = self.markersize_noise[num-1],
                            label = 'Electrical noise (Port: ' + str(num) + ')')
        else:
            self.ax[num-1].plot(time, signal, 
                                color = self.colors_noise[0], 
                                linestyle = self.linestyle_noise[0], 
                                linewidth = self.linewidth_noise[0], 
                                marker = self.markers_noise[0], 
                                markersize = self.markersize_noise[0],
                                label = 'Electrical noise: (Port: ' + str(num) + ')')
        
    def set_signal_and_noise_plot_time_domain(self, time, signal, num):
        if self.radioButtonOverlay.isChecked() == 1:
            self.ax[0].plot(time, signal, 
                            color = self.colors_sig_noise[num-1], 
                            linestyle = self.linestyle_noise[num-1], 
                            linewidth = self.linewidth_noise[num-1],
                            marker = self.markers_sig_noise[num-1],
                            markersize = self.markersize_sig_noise[num-1],
                            label = 'Electrical signal + noise (Port: ' + str(num) + ')')
        else:
            self.ax[num-1].plot(time, signal, 
                                color = self.colors_sig_noise[0],
                                linestyle = self.linestyle_noise[0], 
                                linewidth = self.linewidth_noise[0], 
                                marker = self.markers_sig_noise[0],
                                markersize = self.markersize_sig_noise[0],
                                label = 'Electrical signal + noise (Port: ' + str(num) + ')')
    #=====================================================================================
    
    def format_coord_time(self, x, y):
        return 'Time=%0.7E, Mag/Power=%0.7E' % (x, y)
    
    '''Freq data tab (plotting methods)================================================'''

    def value_change_freq(self):
        new_iteration = int(self.spinBoxFreq.value())
        signal_updated = self.signals[new_iteration-1] 
        
        self.Y = []
        self.Y_pos = []
        self.N = []
        self.N_pos = []
        self.Y_N = []
        self.Y_N_pos = []
        for i in range(0, len(signal_updated)):
            Y = np.fft.fft(signal_updated[i][5])
            Y_pos = Y[range(int(self.n/2))]
            self.Y.append(Y)
            self.Y_pos.append(Y_pos)
            N = np.fft.fft(signal_updated[i][6])
            N_pos = N[range(int(self.n/2))]
            self.N.append(N)
            self.N_pos.append(N_pos)
            Y_N = np.fft.fft(signal_updated[i][5]+signal_updated[i][6])
            Y_N_pos = Y_N[range(int(self.n/2))]
            self.Y_N.append(Y_N)
            self.Y_N_pos.append(Y_N_pos)

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
            self.figure_freq.clf()
            m = len(self.signals[0])
            self.af = []
            color = cfg_m_elec.m_electrical_freq_plot_back_color
            if self.radioButtonFreqOverlay.isChecked() == 1:
                f_plot =  self.figure_freq.add_subplot(1,1,1, facecolor = color)
                self.af.append(f_plot) 
                self.af[0].clear()
            else:
                for x in range(0, m):
                    f_plot =  self.figure_freq.add_subplot(m,1,x+1, facecolor = color)
                    self.af.append(f_plot)                                
                for x in range(0, m):
                    self.af[x].clear()
                    
            #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
            if self.radioButtonFreqOverlay.isChecked() == 1:
                self.af[0].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                       useOffset=False))
                self.af[0].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                       useOffset=False))
            else:
                for x in range(0, m):
                    if x < m-1:
                        self.af[x].xaxis.set_major_formatter(plt.NullFormatter())
                    else:
                        self.af[x].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                           useOffset=False))
                        self.af[x].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, 
                           useOffset=False))
            
            if axis_adjust == 1:
                if self.minFreq.text() and self.maxFreq.text():
                    start_freq = self.minFreq.text()
                    end_freq = self.maxFreq.text()
                    if self.radioButtonFreqOverlay.isChecked() == 1:
                        self.af[0].set_xlim(float(start_freq), float(end_freq))
                    else:
                        for x in range(0, m):
                            self.af[x].set_xlim(float(start_freq), float(end_freq))
                if self.startYAxisFreq.text() and self.endYAxisFreq.text():
                    start_val = self.startYAxisFreq.text()
                    end_val = self.endYAxisFreq.text()
                    if self.radioButtonFreqOverlay.isChecked() == 1:
                        self.af[0].set_ylim(float(start_val), float(end_val))
                    else:
                        for x in range(0, m):
                            self.af[x].set_ylim(float(start_val), float(end_val))    
                
            if self.radioButtonLinearFreq.isChecked() == 1:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].set_ylabel('Power(W)') 
                else:
                    for x in range(0, m):
                        self.af[x].set_ylabel('Power(W): p'+ str(x+1))
            
            elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].set_ylabel('Power(W/Hz)')
                else:
                    for x in range(0, m):
                        self.af[x].set_ylabel('Power(W/Hz): p'+ str(x+1))
            
            elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].set_ylabel('Power(dBm/Hz)')   
                else:
                    for x in range(0, m):
                        self.af[x].set_ylabel('Power(dBm/Hz): p'+ str(x+1))   
            else:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].set_ylabel('Power(dBm)')
                else:
                    for x in range(0, m):
                        self.af[x].set_ylabel('Power(dBm): p'+ str(x+1))
            
            #Access port viewer settings for plot styles        
            self.colors_freq = cfg_m_elec.m_electrical_freq_signal_color
            self.colors_noise = cfg_m_elec.m_electrical_freq_noise_color
            self.colors_sig_noise = cfg_m_elec.m_electrical_freq_sig_noise_color
            self.linestyle_freq = cfg_m_elec.m_electrical_freq_signal_linestyle
            self.linestyle_noise = cfg_m_elec.m_electrical_freq_noise_linestyle
            self.linestyle_sig_noise = cfg_m_elec.m_electrical_freq_sig_noise_linestyle      
            self.linewidth_freq = cfg_m_elec.m_electrical_freq_signal_linewidth
            self.linewidth_noise = cfg_m_elec.m_electrical_freq_noise_linewidth
            self.linewidth_sig_noise = cfg_m_elec.m_electrical_freq_sig_noise_linewidth                   
            self.markers_freq = cfg_m_elec.m_electrical_freq_signal_marker
            self.markers_noise = cfg_m_elec.m_electrical_freq_noise_marker
            self.markers_sig_noise = cfg_m_elec.m_electrical_freq_sig_noise_marker
            self.markersize_freq = cfg_m_elec.m_electrical_freq_signal_markersize
            self.markersize_noise = cfg_m_elec.m_electrical_freq_noise_markersize
            self.markersize_sig_noise = cfg_m_elec.m_electrical_freq_sig_noise_markersize
            
            for i in range(0, m):             
                if self.signalCheckBoxFreq.checkState() == 2:
                    if self.checkBoxDisplayNegFreq.checkState() == 2:
                        sig_pwr = np.square(np.abs(self.Y[i]))/self.n
                        sig_pwr = self.adjust_units_for_plotting_freq(sig_pwr)
                        self.set_signal_plot_freq_domain(self.frq, sig_pwr, i+1)                
                    else:
                        sig_pwr = np.square(np.abs(self.Y_pos[i]))/self.n
                        sig_pwr = self.adjust_units_for_plotting_freq(sig_pwr)
                        self.set_signal_plot_freq_domain(self.frq_pos, sig_pwr, i+1) 
                            
                if self.noiseCheckBoxFreq.checkState() == 2:
                    if self.checkBoxDisplayNegFreq.checkState() == 2:
                        noise_pwr = np.square(np.abs(self.N[i]))/self.n 
                        noise_pwr = self.adjust_units_for_plotting_freq(noise_pwr)
                        self.set_noise_plot_freq_domain(self.frq, noise_pwr, i+1) 
                    else:
                        noise_pwr = np.square(np.abs(self.N_pos[i]))/self.n
                        noise_pwr = self.adjust_units_for_plotting_freq(noise_pwr)
                        self.set_noise_plot_freq_domain(self.frq_pos, noise_pwr, i+1) 
                            
                if self.sigandnoiseCheckBoxFreq.checkState() == 2:
                    if self.checkBoxDisplayNegFreq.checkState() == 2:
                        sig_noise_pwr = np.square(np.abs(self.Y_N[i]))/self.n  
                        sig_noise_pwr = self.adjust_units_for_plotting_freq(sig_noise_pwr)
                        self.set_signal_and_noise_plot_freq_domain(self.frq, sig_noise_pwr, i+1)
                    else:
                        sig_noise_pwr = np.square(np.abs(self.Y_N_pos[i]))/self.n
                        sig_noise_pwr = self.adjust_units_for_plotting_freq(sig_noise_pwr)
                        self.set_signal_and_noise_plot_freq_domain(self.frq_pos, sig_noise_pwr, i+1)
            
            if self.radioButtonFreqOverlay.isChecked() == 1:
                self.af[0].set_title('Freq data (all ports)')
                self.af[0].set_xlabel('Freq (Hz)')
                self.af[0].set_aspect('auto')
                self.af[0].format_coord = self.format_coord_freq
            else:
                for x in range(0, m):
                    if x == m-1:
                        self.af[x].set_xlabel('Freq (Hz)')
                    self.af[x].set_aspect('auto')
                    self.af[x].format_coord = self.format_coord_freq
                    
            if self.radioButtonFreqOverlay.isChecked() == 1:
                self.af[0].xaxis.label.set_color(cfg_m_elec.m_electrical_freq_labels_axes_color)
                self.af[0].yaxis.label.set_color(cfg_m_elec.m_electrical_freq_labels_axes_color)
                self.af[0].tick_params(axis='both', which ='both', 
                                colors=cfg_m_elec.m_electrical_freq_labels_axes_color)
            else:
                for x in range(0, m):
                    if x == m-1:
                        self.af[x].xaxis.label.set_color(cfg_m_elec.m_electrical_freq_labels_axes_color)
                        self.af[x].yaxis.label.set_color(cfg_m_elec.m_electrical_freq_labels_axes_color)
                        self.af[x].tick_params(axis='both', which ='both', 
                                colors=cfg_m_elec.m_electrical_freq_labels_axes_color)  
            
            if self.checkBoxMajorGridFreq.checkState() == 2:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].grid(True)  
                    self.af[0].grid(which = 'major', 
                                    linestyle = cfg_m_elec.m_electrical_freq_maj_grid_linestyle, 
                                    linewidth = cfg_m_elec.m_electrical_freq_maj_grid_linewidth, 
                                    color = cfg_m_elec.m_electrical_freq_maj_grid_color)  
                else:
                    for x in range(0, m):
                        self.af[x].grid(True)  
                        self.af[x].grid(which = 'major', 
                                        linestyle = cfg_m_elec.m_electrical_freq_maj_grid_linestyle, 
                                        linewidth = cfg_m_elec.m_electrical_freq_maj_grid_linewidth, 
                                        color = cfg_m_elec.m_electrical_freq_maj_grid_color)  
           
            if self.checkBoxMinorGridFreq.checkState() == 2:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].minorticks_on()
                    self.af[0].grid(which = 'minor', 
                                    linestyle = cfg_m_elec.m_electrical_freq_min_grid_linestyle, 
                                    linewidth = cfg_m_elec.m_electrical_freq_min_grid_linewidth, 
                                    color = cfg_m_elec.m_electrical_freq_min_grid_color)               
                else:
                    for x in range(0, m): 
                        self.af[x].minorticks_on()
                        self.af[x].grid(which = 'minor',
                                       linestyle = cfg_m_elec.m_electrical_freq_min_grid_linestyle, 
                                       linewidth = cfg_m_elec.m_electrical_freq_min_grid_linewidth, 
                                       color = cfg_m_elec.m_electrical_freq_min_grid_color)   
            
            if self.checkBoxLegendFreq.isChecked() == 1:
                if self.radioButtonFreqOverlay.isChecked() == 1:
                    self.af[0].legend(loc='upper right')
                else:
                    for x in range(0, m): 
                        self.af[x].legend(loc='upper right')
        
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
            msg.setWindowTitle("Plotting error (Multi-channel electrical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
    
    #20.01.r1 2 Sep 19 - Added new function to adjust units before plotting===============
    def adjust_units_for_plotting_freq(self, signal):
        if self.radioButtonLinearFreq.isChecked() == 1:
            pass
        elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
            signal = signal/self.fs
        elif self.radioButtonLogFreqSpectral.isChecked() == 1:
            if np.count_nonzero(signal) == np.size(signal):
                signal = 10*np.log10(signal*1e3/self.fs)                 
            else:
                signal += 1e-30 #Set zero elements to very low value
                signal = 10*np.log10(signal*1e3/self.fs)  
        else:
            if np.count_nonzero(signal) == np.size(signal):
                signal = 10*np.log10(signal*1e3)
            else:
                signal += 1e-30 #Set to very low value
                signal = 10*np.log10(signal*1e3)  
        return signal
    #=====================================================================================
            
    def set_signal_plot_freq_domain(self, freq, signal, num):
        if self.radioButtonFreqOverlay.isChecked() == 1:
            self.af[0].plot(freq, signal, 
                            color = self.colors_freq[num-1], 
                            linestyle = self.linestyle_freq[num-1], 
                            linewidth= self.linewidth_freq[num-1], 
                            marker = self.markers_freq[num-1], 
                            markersize = self.markersize_freq[num-1],
                            label = 'Electrical signal: ' + str(num)) 
        else:
            self.af[num-1].plot(freq, signal, 
                                color = self.colors_freq[0], 
                                linestyle = self.linestyle_freq[0], 
                                linewidth= self.linewidth_freq[0], 
                                marker = self.markers_freq[0], 
                                markersize = self.markersize_freq[0],
                                label = 'Electrical signal: ' + str(num)) 
        
    def set_noise_plot_freq_domain(self, freq, signal, num):
        if self.radioButtonFreqOverlay.isChecked() == 1:
            self.af[0].plot(freq, signal, 
                            color = self.colors_noise[num-1], 
                            linestyle = self.linestyle_noise[num-1], 
                            linewidth = self.linewidth_noise[num-1], 
                            marker = self.markers_noise[num-1],
                            markersize = self.markersize_noise[num-1],
                            label = 'Electrical noise: ' + str(num))   
        else:
            self.af[num-1].plot(freq, signal, 
                                color = self.colors_noise[0], 
                                linestyle = self.linestyle_noise[0], 
                                linewidth = self.linewidth_noise[0], 
                                marker = self.markers_noise[0],
                                markersize = self.markersize_noise[0],
                                label = 'Electrical noise: ' + str(num))   
        
    def set_signal_and_noise_plot_freq_domain(self, freq, signal, num):
        if self.radioButtonFreqOverlay.isChecked() == 1:
            self.af[0].plot(freq, signal, 
                            color = self.colors_sig_noise[num-1], 
                            linestyle = self.linestyle_noise[num-1], 
                            linewidth = self.linewidth_noise[num-1],
                            marker = self.markers_sig_noise[num-1],
                            markersize = self.markersize_sig_noise[num-1],
                            label = 'Electrical signal + noise: ' + str(num))             
        else:
            self.af[num-1].plot(freq, signal, 
                                color = self.colors_sig_noise[0], 
                                linestyle = self.linestyle_noise[0], 
                                linewidth = self.linewidth_noise[0],
                                marker = self.markers_sig_noise[0],
                                markersize = self.markersize_sig_noise[0],
                                label = 'Electrical signal + noise: ' + str(num)) 
        
    def format_coord_freq(self, x, y):
        return 'Freq=%0.7E, Power=%0.7E' % (x, y)
    
        
'''FUNCTIONS==========================================================================='''   
def set_icon_window():
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLabIcon128.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon    
'''===================================================================================='''
