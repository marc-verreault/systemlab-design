'''
    SystemLab-Design Version 19.02
    Primary author: Marc Verreault
    E-mail: marc.verreault@systemlabdesign.com
    Copyright © 2019 SystemLab Inc. All rights reserved.
    
    NOTICE================================================================================    
    This file is part of SystemLab-Design 19.02.
    
    SystemLab-Design 19.02 is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    SystemLab-Design 19.02 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SystemLab-Design 19.02.  If not, see <https://www.gnu.org/licenses/>.   
    ======================================================================================

    ABOUT THIS MODULE
    SystemLab module for port analyzer(GUI) class: SignalAnalogOptical
'''
import os
import config
gui_ui_path = config.root_path
import numpy as np
from scipy import constants

from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib.pyplot as plt
# Method for embedding Matplotlib canvases into Qt-designed QDialog interfaces
# Ref: https://matplotlib.org/gallery/user_interfaces/embedding_in_qt_sgskip.html
# Accessed: 11 Feb 2019
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from mpl_toolkits.mplot3d import Axes3D

qtOpticalPortDataViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'OpticalDataViewer.ui')
qtOpticalPortDataViewerFile = os.path.normpath(qtOpticalPortDataViewerFile)
Ui_PortDataWindow_Optical, QtBaseClass = uic.loadUiType(qtOpticalPortDataViewerFile)

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 80

# https://matplotlib.org/api/ticker_api.html#matplotlib.ticker.Formatter
mpl.rcParams['axes.formatter.useoffset'] = False # Removes offset from all plots
mpl.rcParams['axes.formatter.limits'] = [-4, 4] # Limits for exponential notation

style = """QLineEdit { background-color: rgb(245, 245, 245); color: rgb(50, 50, 50) }"""

class OpticalPortDataAnalyzer(QtWidgets.QDialog, Ui_PortDataWindow_Optical):
    '''Optical: portID(0), signal_type(1), wave_key(2), wave_channel(3), jones_vector(4), sample_rate(5), 
       time_array(6), envelope_array(7), noise_array(8), psd_array(9)
    '''
    def __init__(self, signal_data, fb_name, port_name, direction, design_settings):
        QtWidgets.QDialog.__init__(self)
        Ui_PortDataWindow_Optical.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)        
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.fb_name = fb_name
        self.port_name = port_name
        self.direction = direction
        self.iteration = 1  
        self.signals = signal_data # List of signals for each iteration      
        self.fs = design_settings['sampling_rate']   
        
        '''Time data tab (dataFrame)==================================================='''
        #Top level settings
        self.totalSamplesTime.setText(str(format(design_settings['num_samples'], '0.3E')))
        self.samplingPeriod.setText(str(format(design_settings['sampling_period'], '0.3E')))
        self.timeWindow.setText(str(format(design_settings['time_window'], '0.3E')))     
        #Iterations/Channels group box (Time data tab)
        iterations = len(signal_data)   
        self.spinBoxTime.setMaximum(iterations)
        self.totalIterationsTime.setText(str(iterations))        
        self.spinBoxTime.valueChanged.connect(self.iteration_change_time)  
        self.waveKeyListTime.currentIndexChanged.connect(self.iteration_change_time)
        #Signal type group box (Time data)
        self.signalCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.noiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.sigandnoiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.radioButtonLinear.toggled.connect(self.check_signal_changed_time)
        self.radioButtonLog.toggled.connect(self.check_signal_changed_time)
        #Polarization group box (Time data)
        self.radioButtonPolXY.toggled.connect(self.check_signal_changed_time)
        self.radioButtonPolX.toggled.connect(self.check_signal_changed_time)
        self.radioButtonPolY.toggled.connect(self.check_signal_changed_time)
        #Phase group box (Time data)
        self.sigPhaseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.unwrapPhaseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.radioButtonDeg.toggled.connect(self.check_signal_changed_time)
        self.radioButtonRad.toggled.connect(self.check_signal_changed_time)      
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
        self.samplingRate.setText(str(format(self.fs, '0.3E')))
        #Iterations group box (Main sub-tab)        
        self.spinBoxFreq.setMaximum(iterations)
        self.totalIterationsFreq.setText(str(iterations))
        self.spinBoxFreq.valueChanged.connect(self.iteration_change_freq) 
        self.waveKeyListFreq.currentIndexChanged.connect(self.iteration_change_freq)
        #Spectral resolution group box (Main sub-tab) 
        self.signalCheckBoxEnableResolution.stateChanged.connect(self.check_signal_changed_freq)
        self.actionResolutionWindow.clicked.connect(self.check_signal_changed_freq)
        #Signal type group box (Main sub-tab) 
        self.signalCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.noiseCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.sigandnoiseCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.noisegroupCheckBoxFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.radioButtonLinearFreq.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonLinearFreqSpectral.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonLogFreq.toggled.connect(self.check_signal_changed_freq) 
        self.radioButtonLogFreqSpectral.toggled.connect(self.check_signal_changed_freq) 
        #Polarization group box (Main sub-tab) 
        self.radioButtonPolXYFreq.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonPolXFreq.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonPolYFreq.toggled.connect(self.check_signal_changed_freq)
        #Plot settings (Main sub-tab) 
        self.radioButtonHz.toggled.connect(self.check_signal_changed_freq)
        self.radioButtonNm.toggled.connect(self.check_signal_changed_freq)
        self.checkBoxMajorGridFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.checkBoxMinorGridFreq.stateChanged.connect(self.check_signal_changed_freq)        
        self.checkBoxLegendFreq.stateChanged.connect(self.check_signal_changed_freq)
        #Y-axis axis settings group box (Main sub-tab) 
        self.actionFreqWindowYAxis.clicked.connect(self.update_axis_freq)       
        #Freq axis settings group box (Main sub-tab) 
        self.actionFreqWindow.clicked.connect(self.update_axis_freq)
        #Line and rectangular plots/annotations group boxes (Annotation sub-tab)
        self.checkBoxLine1ViewMarkerFreq.toggled.connect(self.check_signal_changed_freq)
        self.checkBoxLine1ViewLabelFreq.toggled.connect(self.check_signal_changed_freq)
        self.checkBoxLine1ViewLengthFreq.toggled.connect(self.check_signal_changed_freq)
        self.checkBoxLine2ViewMarkerFreq.toggled.connect(self.check_signal_changed_freq)
        self.checkBoxLine2ViewLabelFreq.toggled.connect(self.check_signal_changed_freq)
        self.checkBoxLine2ViewLengthFreq.toggled.connect(self.check_signal_changed_freq)        
        self.checkBoxRectViewLabelFreq.toggled.connect(self.check_signal_changed_freq)  
        self.checkBoxRectViewDimFreq.toggled.connect(self.check_signal_changed_freq)  
        self.checkBoxRectViewFillFreq.toggled.connect(self.check_signal_changed_freq)  
        self.checkBoxDisplayLine1Freq.stateChanged.connect(self.check_signal_changed_freq)
        self.checkBoxDisplayLine2Freq.stateChanged.connect(self.check_signal_changed_freq)
        self.checkBoxDisplayRectFreq.stateChanged.connect(self.check_signal_changed_freq)
        self.actionUpdateAnnotationsFreq.clicked.connect(self.check_signal_changed_freq)
        
        '''Polarization analysis tab (dataFramePol)===================================='''
        #Top level settings (Main sub-tab)  
        self.totalSamplesFreq.setText(str(format(design_settings['num_samples'], '0.3E'))) 
        self.samplingRate.setText(str(format(self.fs, '0.3E')))
        self.numberOptChannels.setText(str(1))
        #Iterations group box (Main sub-tab)        
        self.spinBoxPol.setMaximum(iterations)
        self.totalIterationsPol.setText(str(iterations))
        self.spinBoxPol.valueChanged.connect(self.iteration_change_pol)
        self.waveKeyListPol.currentIndexChanged.connect(self.iteration_change_pol)
        #Adjust view box
        self.elevationPosCurrent.setStyleSheet(style)
        self.azimuthPosCurrent.setStyleSheet(style)
        self.elevationPos.setText(str(format(30, 'n')))        
        self.azimuthPos.setText(str(format(45, 'n')))
        self.actionSphereView.clicked.connect(self.update_poincare_sphere)
        
        '''Signal data tab (dataFrameSignal)==========================================='''
        #Iterations group box
        iterations = len(signal_data)   
        self.spinBoxSignalData.setMaximum(iterations)
        self.totalIterationsSignalData.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iteration_change_signal_data)
        self.waveKeyListSignalData.currentIndexChanged.connect(self.iteration_change_signal_data)
        #Domain setting group box
        self.radioButtonSigFreq.toggled.connect(self.update_signal_data)
        self.radioButtonSigTime.toggled.connect(self.update_signal_data)
        #E-field signal format group box
        self.radioButtonComplexSignalData.toggled.connect(self.update_signal_data)
        self.radioButtonPolarSignalData.toggled.connect(self.update_signal_data)
        #Polarization group box
        self.radioButtonPolXYSignal.toggled.connect(self.update_signal_data)
        self.radioButtonPolXSignal.toggled.connect(self.update_signal_data)
        self.radioButtonPolYSignal.toggled.connect(self.update_signal_data)
        #Adjust samples group box
        self.totalSamplesSignalData.setStyleSheet(style)
        self.totalSamplesSignalData.setText(str(format(design_settings['num_samples'], 'n')))
        self.minIndexSignalData.setText(str(1))
        self.maxIndexSignalData.setText(str(format(design_settings['num_samples'], 'n')))
        self.actionSetIndicesSignalData.clicked.connect(self.update_signal_data)
        #View settings group box
        self.linewidthSignalData.setText(str(60))
        self.actionSetLinewidthSignalData.clicked.connect(self.update_signal_data)
        
        '''Signal metrics tab (dataFrameMetrics)======================================='''
        #Iterations group box
        iterations = len(signal_data)   
        self.spinBoxSignalMetrics.setMaximum(iterations)
        self.totalIterationsSignalMetrics.setText(str(iterations))
        self.spinBoxSignalMetrics.valueChanged.connect(self.iteration_change_signal_metrics)
        self.waveKeyListSignalMetrics.currentIndexChanged.connect(self.iteration_change_signal_metrics)
        #Polarization group box 
        self.radioButtonPolXYSignalMetrics.toggled.connect(self.update_signal_metrics)
        self.radioButtonPolXSignalMetrics.toggled.connect(self.update_signal_metrics)
        self.radioButtonPolYSignalMetrics.toggled.connect(self.update_signal_metrics)
        
        '''Prepare signal data for iteration 1 (default)==============================='''
        signal_default = self.signals[self.iteration]
        self.time = signal_default[3] #Time sampling points
        optical_list = signal_default[4]
        self.signal = optical_list[0][3]
        self.sig_phase = np.angle(self.signal)
        self.sig_phase_unwrap = np.unwrap(self.sig_phase)
        self.noise = optical_list[0][4]
        self.noise_freq = optical_list[0][5]
        self.jones_vector = optical_list[0][2]
        #Freq data tab (top level settings for channel info)
        self.channel_freq = optical_list[0][1]
        self.opticalChTime.setText(str(format(self.channel_freq, '0.3E')))
        self.opticalChFreq.setText(str(format(self.channel_freq, '0.3E')))
        
        '''Prepare frequency domain analysis==========================================='''
        # REF:  Fast Fourier Transform in matplotlib, 
        # An example of FFT audio analysis in matplotlib and the fft function.
        # Source: https://plot.ly/matplotlib/fft/(accessed 20-Mar-2018) 
        self.n = int(len(self.signal))
        self.frq = self.update_freq_array(self.n, self.channel_freq)
        #FFT computations (signal, noise, signal+noise)
        self.Y = np.fft.fft(self.signal)
        self.Y = np.fft.fftshift(self.Y)
        self.N = np.fft.fft(self.noise)
        self.N = np.fft.fftshift(self.N)
        self.Y_N = np.fft.fft(self.signal+self.noise)
        self.Y_N = np.fft.fftshift(self.Y_N)
        
        '''Setup background colors for frames=========================================='''
        p = self.graphFrame.palette()
        color = QtGui.QColor(252,252,252)
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
        p5  = self.dataFrameMainFreq.palette() 
        p5.setColor(self.dataFrameMainFreq.backgroundRole(), color)
        self.dataFrameMainFreq.setPalette(p5)
        p6  = self.dataFrameAnnotationsFreq.palette() 
        p6.setColor(self.dataFrameAnnotationsFreq.backgroundRole(), color)
        self.dataFrameAnnotationsFreq.setPalette(p6)
        p7  = self.dataFramePol.palette() 
        p7.setColor(self.dataFramePol.backgroundRole(), color)
        self.dataFramePol.setPalette(p7)
        p8  = self.graphFramePol.palette() 
        p8.setColor(self.graphFramePol.backgroundRole(), color)
        self.graphFramePol.setPalette(p8)
        
        '''Setup matplotlib figures and toolbars======================================='''
        #Time data
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_time)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        #Frequency data
        self.graphLayoutFreq = QtWidgets.QVBoxLayout()
        self.figure_freq = plt.figure()
        self.canvas_freq = FigureCanvas(self.figure_freq)     
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self.tab_freq)
        self.graphLayoutFreq.addWidget(self.canvas_freq)
        self.graphLayoutFreq.addWidget(self.toolbar_freq) 
        self.graphFrameFreq.setLayout(self.graphLayoutFreq) 
        #Polarization analyis
        self.graphLayoutPol = QtWidgets.QVBoxLayout()
        self.figure_pol = plt.figure()
        self.canvas_pol = FigureCanvas(self.figure_pol)     
        self.graphLayoutPol.addWidget(self.canvas_pol)
        self.graphFramePol.setLayout(self.graphLayoutPol)
        self.canvas_pol.mpl_connect('button_release_event', self.onclick)
                
        self.tabData.setCurrentWidget(self.tab_freq)
        self.figure_freq.set_tight_layout(True)
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        
        self.tabData.setCurrentWidget(self.tab_time) 
        self.figure.set_tight_layout(True)
        self.plot_time_domain(0)
        self.canvas.draw()
        
        self.tabData.setCurrentWidget(self.tab_polarization) 
        self.figure_pol.set_tight_layout(True)
        self.plot_poincare_sphere()
        self.canvas_pol.draw()
        
        '''Prepare default data for signal data and signal metrics viewers============='''
        self.update_signal_data()
        self.update_signal_metrics()               
        #Load wave key lists
        k = len(optical_list)
        for k in range(0, k):
            key = str(optical_list[k][0])
            self.waveKeyListTime.addItem(key) 
            self.waveKeyListFreq.addItem(key)
            self.waveKeyListPol.addItem(key)
            self.waveKeyListSignalData.addItem(key)
            self.waveKeyListSignalMetrics.addItem(key)
        self.numberOptChannels.setText(str(k))    
        
        #Return to time tab
        self.tabData.setCurrentWidget(self.tab_time)
        
    '''Time data tab (plotting methods)================================================'''
    def iteration_change_time(self):
        new_iteration = int(self.spinBoxTime.value())
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[4]
        
        key = str(self.waveKeyListTime.currentText())        
        for k in range(len(optical_list)):
            if optical_list[k][0] == key:
                break
        index_key = k

        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.sig_phase = np.angle(self.signal)
        self.sig_phase_unwrap = np.unwrap(self.sig_phase)
        self.noise = optical_list[index_key][4]
        self.jones_vector = optical_list[index_key][2]
        
        ch_freq = optical_list[index_key][1]
        self.opticalChTime.setText(str(format(ch_freq, '0.3E')))
        
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
        self.figure.clf()
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        
        #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
        ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True))
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True))
                    
        if axis_adjust == 1:
            if self.minTime.text() and self.maxTime.text():
                start_time = self.minTime.text()
                end_time = self.maxTime.text()
                ax.set_xlim(float(start_time), float(end_time))
            if self.startYAxisTime.text() and self.endYAxisTime.text():
                start_val = self.startYAxisTime.text()
                end_val = self.endYAxisTime.text()
                ax.set_ylim(float(start_val), float(end_val))    
            
        if self.radioButtonLinear.isChecked() == 1:
            ax.set_ylabel('Power (W)')
        else:
            ax.set_ylabel('Power (dBm)')
            
        pol = 'X-Y'
        if self.radioButtonPolX.isChecked() == 1:
            pol = 'X'
        if self.radioButtonPolY.isChecked() == 1:
            pol = 'Y'

        sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, self.signal, 
                                                              self.noise, self.jones_vector)
        
        if self.signalCheckBox.checkState() == 2:
            if self.radioButtonLinear.isChecked() == 1:
                ax.plot(self.time, sig_pwr, color = 'b', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3, label='Optical signal')
            else:
                ax.plot(self.time, 10*np.log10(sig_pwr*1e3), color = 'b', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3, label='Optical signal')
            
        if self.noiseCheckBox.checkState() == 2:
            if self.radioButtonLinear.isChecked() == 1:
                ax.plot(self.time, noise_pwr, color = 'r', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3, label='Optical noise')
            else:
                ax.plot(self.time, 10*np.log10(noise_pwr*1e3), color = 'r', linestyle = '--',
                    linewidth= 0.8, marker = 'o', markersize = 3, label='Optical noise')
            
        if self.sigandnoiseCheckBox.checkState() == 2:
            if self.radioButtonLinear.isChecked() == 1:
                ax.plot(self.time, sig_pwr+noise_pwr, color = 'g',
                    linestyle = '--', linewidth= 0.8, marker = 'o', markersize = 3,
                    label='Optical signal + noise')
            else:
                ax.plot(self.time, 10*np.log10((sig_pwr+noise_pwr)*1e3), color = 'g',
                    linestyle = '--', linewidth= 0.8, marker = 'o', markersize = 3, 
                    label='Optical signal + noise')
        
        if self.sigPhaseCheckBox.checkState() == 2:
            ax2 = ax.twinx()
            
            phase_map = self.sig_phase
            if self.unwrapPhaseCheckBox.checkState() == 2:
                phase_map = self.sig_phase_unwrap
                
            if self.radioButtonDeg.isChecked() == 1:
                phase_map = np.rad2deg(phase_map)
                ax2.set_ylabel('Phase (deg)')
            else:
                ax2.set_ylabel('Phase (rad)')
                
            ax2.plot(self.time, phase_map, color = 'y',
                    linestyle = '-', linewidth= 0.8, marker = 'o',
                    markersize = 3, label = 'Optical phase')  
            ax2.set_aspect('auto')
            
        ax.set_title('Sampled envelope - optical ('+ self.fb_name + ', Port:' +
                                self.port_name + ', Dir:' + str(self.direction) +
                                ', Pol:' + pol + ')')
        ax.set_xlabel('Time (sec)')
        ax.set_aspect('auto')
        ax.format_coord = self.format_coord_time
        
        #Plot settings (grid and legend)
        if self.checkBoxMajorGrid.checkState() == 2:
            ax.grid(True)  
            ax.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
       
        if self.checkBoxMinorGrid.checkState() == 2:
            ax.minorticks_on()
            ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
            
        if self.checkBoxLegend.isChecked() == 1:
            ax.legend()
            if self.sigPhaseCheckBox.checkState() == 2:
                ax2.legend()
                
    def set_signal_data(self, pol, signal, noise, jones):
        if pol == 'X':
            signal = jones[0]*signal
            noise = jones[0]*noise
            sig_power = np.abs(signal)*np.abs(signal)
            noise_power = np.abs(noise)*np.abs(noise)
        elif pol == 'Y':
            signal = jones[1]*signal
            noise = jones[1]*noise
            sig_power = np.abs(signal)*np.abs(signal)
            noise_power = np.abs(noise)*np.abs(noise)
        else:
            sig_power = ( (np.abs(jones[0]*signal)**2 +
                            (np.abs(jones[1]*signal)) **2) )
            noise_power = ( (np.abs(jones[0]*noise)**2 +
                            (np.abs(jones[1]*noise)) **2) )
        return signal, noise, sig_power, noise_power
                
    def format_coord_time(self, x, y):
        return 'Time=%0.7E, Power=%0.7E' % (x, y)
           
    '''Freq data tab plotting methods=================================================='''
    def update_freq_array(self, n, channel_freq):
        # REF:  Fast Fourier Transform in matplotlib, 
        # An example of FFT audio analysis in matplotlib and the fft function.
        # Source: https://plot.ly/matplotlib/fft/(accessed 20-Mar-2018) 
        T = n/self.fs
        k = np.arange(n)
        frq = (k/T) # Positive/negative freq (double sided) 
        frq = frq - frq[int(round(n/2))] + channel_freq #Adjust for optical carrier
        return frq
        
    def iteration_change_freq(self):
        new_iteration = int(self.spinBoxFreq.value())
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[4]
        
        key = str(self.waveKeyListFreq.currentText())        
        for k in range(len(optical_list)):
            if optical_list[k][0] == key:
                break
        index_key = k
        
        self.channel_freq = optical_list[index_key][1]
        self.opticalChFreq.setText(str(format(self.channel_freq, '0.3E')))
        
        self.n = int(len(self.signal))
        self.frq = self.update_freq_array(self.n, self.channel_freq)
        
        self.Y = np.fft.fft(optical_list[index_key][3])
        self.Y = np.fft.fftshift(self.Y)
        self.N = np.fft.fft(optical_list[index_key][4])
        self.N = np.fft.fftshift(self.N)     
        self.Y_N = np.fft.fft(optical_list[index_key][3]+optical_list[index_key][4])
        self.Y_N = np.fft.fftshift(self.Y_N)
        # PSD noise array
        self.noise_freq = optical_list[index_key][5]
        
        self.tabData.setCurrentWidget(self.tab_freq)       
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        
    def check_signal_changed_freq(self):
        self.tabData.setCurrentWidget(self.tab_freq)    
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        
    def update_axis_freq(self):
        self.plot_freq_domain(1)
        self.canvas_freq.draw()
        
    def plot_freq_domain(self, axis_adjust):  
        # Prepare signal arrays for frequency noise groups
        self.ng_w = self.noise_freq[0, 1] - self.noise_freq[0, 0]
        self.noise_freq_psd = self.noise_freq[1, :]
        self.noise_freq_pwr = self.noise_freq[1, :] * self.ng_w
        self.freq_points = self.noise_freq[0, :]
        
        # Adjust signals for polarization setting
        if self.radioButtonPolXFreq.isChecked() == 1:
            # Apply jones vector (x-pol) to sampled sig arrays
            Y_x = self.jones_vector[0]*self.Y
            N_x = self.jones_vector[0]*self.N
            Y_N_x = self.jones_vector[0]*self.Y_N
            optical_power_fft = abs(Y_x)*abs(Y_x)/self.n
            optical_noise_fft = abs(N_x)*abs(N_x)/self.n
            optical_signal_and_noise_fft = abs(Y_N_x)*abs(Y_N_x)/self.n
            # Apply jones vector (x-pol) to frequency noise groups
            pol_adj_x =  abs(self.jones_vector[0])*abs(self.jones_vector[0])
            self.noise_freq_psd = pol_adj_x*self.noise_freq_psd
            self.noise_freq_pwr = pol_adj_x*self.noise_freq_pwr
            # Text for graph title
            pol = 'X'
            
        elif self.radioButtonPolYFreq.isChecked() == 1:
            # Apply jones vector (y-pol) to sampled sig arrays
            Y_y = self.jones_vector[1]*self.Y
            N_y = self.jones_vector[1]*self.N
            Y_N_y = self.jones_vector[1]*self.Y_N
            optical_power_fft = abs(Y_y)*abs(Y_y)/self.n
            optical_noise_fft = abs(N_y)*abs(N_y)/self.n
            optical_signal_and_noise_fft = abs(Y_N_y)*abs(Y_N_y)/self.n   
            # Apply jones vector (x-pol) to frequency noise groups
            pol_adj_y = abs(self.jones_vector[1])*abs(self.jones_vector[1])
            self.noise_freq_psd = pol_adj_y*self.noise_freq_psd
            self.noise_freq_pwr = pol_adj_y*self.noise_freq_pwr
            # Text for graph title
            pol = 'Y'
        else:
            # Apply jones vector (x+y-pol) to sampled sig arrays
            optical_power_fft = ( (np.abs(self.jones_vector[0]*self.Y)**2 +
                            (np.abs(self.jones_vector[1]*self.Y)) **2) )/self.n
            optical_noise_fft =  ( (np.abs(self.jones_vector[0]*self.N)**2 +
                            (np.abs(self.jones_vector[1]*self.N)) **2) )/self.n
            optical_signal_and_noise_fft = ( (np.abs(self.jones_vector[0]*self.Y_N)**2 +
                            (np.abs(self.jones_vector[1]*self.Y_N)) **2) )/self.n
            # Text for graph title
            pol = 'X+Y'
        
        self.figure_freq.clf()
        self.af = self.figure_freq.add_subplot(111, facecolor = '#f9f9f9')
                                                                                      
        #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
        self.af.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True))
        self.af.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True))
        
        if axis_adjust == 1:
            if self.minFreq.text() and self.maxFreq.text():
                start_freq = self.minFreq.text()
                end_freq = self.maxFreq.text()
                self.af.set_xlim(float(start_freq), float(end_freq))
            if self.startYAxisFreq.text() and self.endYAxisFreq.text():
                start_val = self.startYAxisFreq.text()
                end_val = self.endYAxisFreq.text()
                self.af.set_ylim(float(start_val), float(end_val))    
            
        if self.signalCheckBoxEnableResolution.checkState() == 2:
            optical_power_fft_avg = np.zeros(self.n)
            optical_noise_fft_avg = np.zeros(self.n)
            optical_signal_and_noise_fft_avg = np.zeros(self.n)
            
            window = float(self.spectralResolution.text())
            x = int(round(window/self.fs))
            if x > 1:
                for i in range(0,self.n):
                    for a in range(-x,x):
                        if (i+a < 0) or (i+a > self.n-1): 
                            pass
                        else:
                            optical_power_fft_avg[i] += optical_power_fft[i+a]
                            optical_noise_fft_avg[i] += optical_noise_fft[i+a]
                            optical_signal_and_noise_fft_avg[i] += optical_signal_and_noise_fft[i+a]
                optical_power_fft = optical_power_fft_avg
                optical_noise_fft = optical_noise_fft_avg
                optical_signal_and_noise_fft = optical_signal_and_noise_fft_avg

        if self.radioButtonLinearFreq.isChecked() == 1:
            self.af.set_ylabel('Power (W)')
        elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
            self.af.set_ylabel('Power (W/Hz)')
        elif self.radioButtonLogFreqSpectral.isChecked() == 1:
            self.af.set_ylabel('Power (dBm/Hz)')    
        else:
            self.af.set_ylabel('Power (dBm)')
           
        if self.radioButtonNm.isChecked() == 1:
            self.freq_plot = (constants.c/self.frq)*1e9
            self.af.set_xlabel('Freq (nm)')
        else:
            self.freq_plot = self.frq
            self.af.set_xlabel('Freq (Hz)')
            
        if self.signalCheckBoxFreq.checkState() == 2:
            if self.radioButtonLinearFreq.isChecked() == 1:
                self.set_signal_plot_freq_domain(optical_power_fft)
            elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                self.set_signal_plot_freq_domain(optical_power_fft/self.fs)
            elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                self.set_signal_plot_freq_domain(10*np.log10(optical_power_fft*1e3/self.fs))   
            else:
                self.set_signal_plot_freq_domain(10*np.log10(optical_power_fft*1e3))

        if self.noiseCheckBoxFreq.checkState() == 2:
            if self.radioButtonLinearFreq.isChecked() == 1:
                self.set_noise_plot_freq_domain(optical_noise_fft)
            elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                self.set_noise_plot_freq_domain(optical_noise_fft/self.fs)
            elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                self.set_noise_plot_freq_domain(10*np.log10(optical_noise_fft*1e3/self.fs))   
            else:
                self.set_noise_plot_freq_domain(10*np.log10(optical_noise_fft*1e3))
                
        if self.sigandnoiseCheckBoxFreq.checkState() == 2:
            if self.radioButtonLinearFreq.isChecked() == 1:
                self.set_signal_and_noise_plot_freq_domain(optical_signal_and_noise_fft)
            elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                self.set_signal_and_noise_plot_freq_domain(optical_signal_and_noise_fft/self.fs)
            elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                self.set_signal_and_noise_plot_freq_domain(10*np.log10(optical_signal_and_noise_fft*1e3/self.fs))   
            else:
                self.set_signal_and_noise_plot_freq_domain(10*np.log10(optical_signal_and_noise_fft*1e3)) 
                
        if self.noisegroupCheckBoxFreq.checkState() == 2:
            if self.radioButtonLinearFreq.isChecked() == 1:
                self.set_psd_noise_plot_freq_domain(self.noise_freq_pwr)
            elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                self.set_psd_noise_plot_freq_domain(self.noise_freq_psd)
            elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                self.set_psd_noise_plot_freq_domain(10*np.log10(self.noise_freq_psd*1e3))   
            else:
                self.set_psd_noise_plot_freq_domain(10*np.log10(self.noise_freq_pwr*1e3))
            
        self.af.set_title('Freq data - optical ('+ self.fb_name + ', Port:' +
                            self.port_name + ', Dir:' + str(self.direction) +
                                ', Pol:' + pol + ')')
        self.af.set_aspect('auto')
        self.af.format_coord = self.format_coord_freq

        #Plot settings (grid and legend)        
        if self.checkBoxMajorGridFreq.checkState() == 2:
            self.af.grid(True)  
            self.af.grid(which='major', linestyle=':', linewidth=0.5, color='gray')
       
        if self.checkBoxMinorGridFreq.checkState() == 2:
            self.af.minorticks_on()
            self.af.grid(which='minor', linestyle=':', linewidth=0.5, color='lightGray')
            
        if self.checkBoxLegendFreq.isChecked() == 1:
            self.af.legend()
        
        #Annotations
        if self.checkBoxDisplayLine1Freq.isChecked() == 1: #Line 1
            if (self.x1Line1Freq.text() and self.y1Line1Freq.text() and self.x2Line1Freq.text()
            and self.y2Line1Freq.text() and self.line1LabelFreq.text() and self.line1ColorFreq.text()):
                x_line1_freq = [float(self.x1Line1Freq.text()), float(self.x2Line1Freq.text()) ]
                y_line1_freq = [float(self.y1Line1Freq.text()), float(self.y2Line1Freq.text()) ]
                dx = x_line1_freq[1] - x_line1_freq[0]
                dy = y_line1_freq[1] - y_line1_freq[0]
                line1_label = str(self.line1LabelFreq.text())
                line1_color = str(self.line1ColorFreq.text())
                if self.checkBoxLine1ViewMarkerFreq.isChecked() == 1:
                    self.af.plot(x_line1_freq, y_line1_freq, color = line1_color, linestyle = '--', 
                                 linewidth= 1, label= line1_label, marker = 'o', markersize = 4)
                else:
                    self.af.plot(x_line1_freq, y_line1_freq, color = line1_color, linestyle = '--',
                                 linewidth= 1, label= line1_label)
                    
                if self.checkBoxLine1ViewLabelFreq.isChecked() == 1:
                    self.af.text(x_line1_freq[1]+(abs(dx)*0.03), y_line1_freq[1]+(abs(dy)*0.03), 
                                 line1_label, ha='left', va='center', withdash=True, 
                                 style='italic', color = line1_color, zorder = 25)
                    
                if self.checkBoxLine1ViewLengthFreq.isChecked() == 1:
                    length = np.sqrt(dx**2 + dy**2)
                    length = str(format(length, '0.3E'))
                    x = (x_line1_freq[0] + dx/2)
                    y = (y_line1_freq[0] + dy/2)
                    self.af.text(x, y, length, withdash=True, ha='center',
                                 va='center', zorder = 25, bbox=dict(facecolor='white', 
                                 edgecolor=line1_color, alpha=1))
                
        if self.checkBoxDisplayLine2Freq.isChecked() == 1: #Line 2
            if (self.x1Line2Freq.text() and self.y1Line2Freq.text() and self.x2Line2Freq.text()
            and self.y2Line2Freq.text() and self.line2LabelFreq.text() and self.line2ColorFreq.text()):
                x_line2_freq = [float(self.x1Line2Freq.text()), float(self.x2Line2Freq.text()) ]
                y_line2_freq = [float(self.y1Line2Freq.text()), float(self.y2Line2Freq.text()) ]
                dx = x_line2_freq[1] - x_line2_freq[0]
                dy = y_line2_freq[1] - y_line2_freq[0]
                line2_label = str(self.line2LabelFreq.text())
                line2_color = str(self.line2ColorFreq.text())
                if self.checkBoxLine2ViewMarkerFreq.isChecked() == 1:
                    self.af.plot(x_line2_freq, y_line2_freq, color = line2_color, linestyle = '--', 
                                 linewidth= 1, label= line2_label, marker = 'o', markersize = 4)
                else:
                    self.af.plot(x_line2_freq, y_line2_freq, color = line2_color, linestyle = '--',
                                 linewidth= 1, label= line2_label)
                    
                if self.checkBoxLine2ViewLabelFreq.isChecked() == 1:
                    self.af.text(x_line2_freq[1]+(abs(dx)*0.03), y_line2_freq[1]+(abs(dy)*0.03),
                                 line2_label, ha='left', va='center', withdash=True,
                                 style='italic', color = line2_color, zorder = 25)
                    
                if self.checkBoxLine2ViewLengthFreq.isChecked() == 1:
                    length = np.sqrt(dx**2 + dy**2)
                    length = str(format(length, '0.3E'))
                    x = (x_line2_freq[0] + dx/2)
                    y = (y_line2_freq[0] + dy/2)
                    self.af.text(x, y, length, withdash=True, ha='center',
                                 va='center', zorder = 25, bbox=dict(facecolor='white', 
                                 edgecolor=line2_color, alpha=1))
                
        if self.checkBoxDisplayRectFreq.isChecked() == 1:
            if (self.x1DataFreq.text() and self.y1DataFreq.text() 
                and self.lengthFreq.text() and self.heightFreq.text() 
                and self.rectLabelFreq.text() and self.rectColorFreq.text()):
                x1 = float(self.x1DataFreq.text())
                y1 = float(self.y1DataFreq.text())
                length = float(self.lengthFreq.text())
                height = float(self.heightFreq.text())
                rect_label = str(self.rectLabelFreq.text())
                rect_color = str(self.rectColorFreq.text())
                if self.checkBoxRectViewFillFreq.isChecked() == 1:
                    self.af.bar(x1, height, length, y1, alpha=0.2, fill=1, 
                                color=rect_color, edgecolor=rect_color)
                else:
                    self.af.bar(x1, height, length, y1, alpha=0.5, fill=0, 
                                edgecolor=rect_color)
                
                if self.checkBoxRectViewLabelFreq.isChecked() == 1:
                    self.af.text(x1-(length/2), y1, rect_label, ha='left',
                                va='bottom', withdash=True, style='italic', 
                                color = rect_color, zorder = 25)
                    
                if self.checkBoxRectViewDimFreq.isChecked() == 1:
                    l = str(format(length, '0.3E'))
                    h = str(format(height, '0.3E'))
                    x = x1 + (length/2)
                    y = y1 + (height/2)
                    self.af.text(x1, y1, l, withdash=True, ha='center',
                                 va='center', zorder = 25, 
                                 bbox=dict(facecolor='white',edgecolor=rect_color, alpha=1))
                    self.af.text(x, y, h, withdash=True, ha='center',
                                 va='center', zorder = 25, 
                                 bbox=dict(facecolor='white',edgecolor=rect_color, alpha=1))
            
    def set_signal_plot_freq_domain(self, signal):
        self.af.plot(self.freq_plot, signal, color = 'b', linestyle = '--', 
                    linewidth= 0.8, marker = 'o', markersize = 3,
                    label='Optical signal') 
        
    def set_noise_plot_freq_domain(self, signal):
        self.af.plot(self.freq_plot, signal, color = 'r', linestyle = '--', 
                    linewidth= 0.8, marker = 'o', markersize = 3,
                    label='Optical noise')   
        
    def set_signal_and_noise_plot_freq_domain(self, signal):
        self.af.plot(self.freq_plot, signal, color = 'g', linestyle = '--', 
                    linewidth= 0.8, marker = 'o', markersize = 3,
                    label='Optical signal + noise')
        
    def set_psd_noise_plot_freq_domain(self, signal):
        self.af.plot(self.freq_points, signal, color = 'orange', linestyle = '--', 
                    linewidth= 0.8, marker = 'o', markersize = 3,
                    label='Optical noise groups')
        
    def format_coord_freq(self, x, y):
        return 'Freq=%0.7E, Power=%0.7E' % (x, y)
    
    '''Polarization analysis tab (plotting methods)===================================='''
    def iteration_change_pol(self):
        new_iteration = int(self.spinBoxPol.value())
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[4]
        
        key = str(self.waveKeyListPol.currentText())        
        for k in range(len(optical_list)):
            if optical_list[k][0] == key:
                break
        index_key = k
        
        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.jones_vector = optical_list[index_key][2]
        
        self.tabData.setCurrentWidget(self.tab_polarization) 
        self.plot_poincare_sphere()
        
    def update_poincare_sphere(self):
        self.plot_poincare_sphere()
        
    def plot_poincare_sphere(self):        
        self.figure_pol.clf()
        self.p_sph = self.figure_pol.add_subplot(111, projection='3d')

        #Stokes parameters
        sig_x = self.jones_vector[0]*self.signal
        sig_x_pwr = np.abs(sig_x)*np.abs(sig_x)
        sig_y = self.jones_vector[1]*self.signal
        sig_y_pwr = np.abs(sig_y)*np.abs(sig_y)
        P0 = sig_x_pwr + sig_y_pwr #P0 = Ex^2 + Ey^2 overall intensity
        P1 = sig_x_pwr - sig_y_pwr #P1 = Ex^2 - Ey^2 intensity difference
        phi = np.angle(self.jones_vector[1]) - np.angle(self.jones_vector[0])
        P2 = 2*np.abs(sig_x)*np.abs(sig_y)*np.cos(phi) #P2 = 2*Ex*Ey*cos(phi)
        P3 = 2*np.abs(sig_x)*np.abs(sig_y)*np.sin(phi) #P3 = 2*Ex*Ey*sin(phi)
        
        #Normalize and calculate average values
        if P0.all() > 0:
            S0 = P0/P0
            S1 = P1/P0
            S2 = P2/P0
            S3 = P3/P0
            S0_avg = np.sum(S0)/self.n
            S1_avg = np.sum(S1)/self.n
            S2_avg = np.sum(S2)/self.n
            S3_avg = np.sum(S3)/self.n
            self.stokesPar0.setText(str(format(S0_avg, '0.3E')))
            self.stokesPar1.setText(str(format(S1_avg, '0.3E')))
            self.stokesPar2.setText(str(format(S2_avg, '0.3E')))
            self.stokesPar3.setText(str(format(S3_avg, '0.3E')))
        
            deg_of_pol = np.sqrt((S1_avg*S1_avg)+(S2_avg*S2_avg)+(S3_avg*S3_avg))/S0_avg
            azimuth = 0.5*np.arctan(S2_avg/S1_avg)
            ellipticity = 0.5*np.arcsin(S3_avg/S0_avg)
            self.deg_pol.setText(str(format(deg_of_pol, '0.3E')))
            self.azimuth.setText(str(format(np.rad2deg(azimuth), '0.3E')))
            self.ellipticity.setText(str(format(np.rad2deg(ellipticity), '0.3E')))
        
        #Plot surface and polarization state
        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)    
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        self.p_sph.plot_surface(x, y, z, rstride=4, cstride=3, alpha = 0.5, linewidth = 1.5,
                           color='#e0e0e0')
        if P0.all() > 0:
            self.p_sph.scatter(S1_avg, S2_avg, S3_avg, color = 'blue', marker = 'o')
            x = [0, S1_avg]
            y = [0, S2_avg]
            z = [0, S3_avg]
            self.p_sph.plot(x, y, z, color = 'blue')
        self.p_sph.plot([0, 1.5], [0, 0], [0, 0], color = 'black', linestyle=':')
        self.p_sph.plot([0, 0], [0, -1.5], [0, 0], color = 'black', linestyle=':')
        self.p_sph.plot([0, 0], [0, 0], [0, 1.5], color = 'black', linestyle=':')
        
        self.p_sph.set_xlabel('S1')
        self.p_sph.set_ylabel('S2')
        self.p_sph.set_zlabel('S3')
        self.p_sph.text(0, 0, 1.6, 'S3', color = 'black')
        self.p_sph.text(0, -1.6, 0, 'S1', color = 'black')
        self.p_sph.text(1.6, 0, 0, 'S2', color = 'black')
        
        self.p_sph.set_title('Poincare sphere - (' + self.fb_name + ', Port:' +
                                self.port_name + ', Dir:' + str(self.direction) + ' )')
        
        self.p_sph.xaxis.pane.fill = False
        self.p_sph.yaxis.pane.fill = False
        self.p_sph.zaxis.pane.fill = False
        self.p_sph.xaxis.pane.set_edgecolor('w')
        self.p_sph.yaxis.pane.set_edgecolor('w')
        self.p_sph.zaxis.pane.set_edgecolor('w')
        #Elevation and azimuth settings (camera view)
        self.elev = 30
        self.az = 45
        if self.azimuthPos.text() and self.elevationPos.text():
            self.elev = self.elevationPos.text()
            self.az = self.azimuthPos.text()
        self.p_sph.view_init(elev=float(self.elev), azim=float(self.az))
        self.elevationPosCurrent.setText(str(format(float(self.elev), '0.1f')))
        self.azimuthPosCurrent.setText(str(format(float(self.az), '0.1f')))
        self.canvas_pol.draw()
        
    def onclick(self, event):
        azim = self.p_sph.azim
        elev = self.p_sph.elev
        self.elevationPosCurrent.setText(str(format(elev, '0.1f')))
        self.azimuthPosCurrent.setText(str(format(azim, '0.1f')))
    
    '''Signal data tab================================================================='''
    def iteration_change_signal_data(self):
        new_iteration = int(self.spinBoxSignalData.value())
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[4]
        
        key = str(self.waveKeyListSignalData.currentText())        
        for k in range(len(optical_list)):
            if optical_list[k][0] == key:
                break
        index_key = k
        
        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.noise = optical_list[index_key][4]
        self.jones_vector = optical_list[index_key][2]
        self.channel_freq = optical_list[index_key][1]    
        self.n = int(len(self.signal))
        self.frq = self.update_freq_array(self.n, self.channel_freq)
        self.Y = np.fft.fft(self.signal)
        self.Y = np.fft.fftshift(self.Y)
        self.N = np.fft.fft(self.noise)
        self.N = np.fft.fftshift(self.N)     
        self.Y_N = np.fft.fft(self.signal + self.noise)
        self.Y_N = np.fft.fftshift(self.Y_N)
        self.update_signal_data()
        
    def update_signal_data(self):
        self.tabData.setCurrentWidget(self.tab_signal)
        self.signalBrowser.clear() 
        #Signal data (base data)
        self.font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
        self.font_normal = QtGui.QFont("Arial", 8, QtGui.QFont.Normal)
        self.signalBrowser.setCurrentFont(self.font_bold)
        self.signalBrowser.setTextColor(QtGui.QColor('#007900'))
        i = int(self.spinBoxSignalData.value())
        self.signalBrowser.append('Signal data (optical) - Iteration '+str(i))
        #Check polarization setting
        pol = 'X-Y'
        if self.radioButtonPolXSignal.isChecked() == 1:
            pol = 'X'
        if self.radioButtonPolYSignal.isChecked() == 1:
            pol = 'Y'
        #Prepare and display port information (fb and port names, direction)  
        self.signalBrowser.append(self.fb_name + ', Port:' +
                            self.port_name + ', Dir:' + str(self.direction) +
                                ', Pol:' + pol)
        self.signalBrowser.setCurrentFont(self.font_normal)
        self.signalBrowser.setTextColor(QtGui.QColor('#000000'))
        #Display frequency and Jones Vector
        self.signalBrowser.append('Frequency (Hz): ' + str(self.channel_freq))
        self.signalBrowser.append('Jones vector: ' + str(self.jones_vector))
        
        #Adjust for new index range (if required)
        self.start_index = int(float(self.minIndexSignalData.text()))
        self.end_index = int(float(self.maxIndexSignalData.text())) + 1        
        index_array = np.arange(self.start_index, self.end_index, 1)
        array_size = self.end_index - self.start_index
        self.adjustedSamplesSignalData.setText(str(format(array_size, 'n')))
        
        #Prepare structured array for string output to text browser
        if self.radioButtonComplexSignalData.isChecked() == 1:
            data1 = np.zeros(array_size, dtype={'names':('index', 'x', 'y'),
                                               'formats':('i4', 'f8', 'c16')})
    
            data2 = np.zeros(array_size, dtype={'names':('index', 'x', 'y'),
                                               'formats':('i4', 'f8', 'c16')})
        else:
            data1 = np.zeros(array_size, dtype={'names':('index', 'x', 'y1', 'y2'),
                                               'formats':('i4', 'f8', 'f8', 'f8')})

            data2 = np.zeros(array_size, dtype={'names':('index', 'x', 'y1', 'y2'),
                                               'formats':('i4', 'f8', 'f8', 'f8')})  
    
        data3 = np.zeros(len(self.freq_points), dtype={'names':('x', 'y'), 
                         'formats':('f8', 'f8')}) 
    
        data1['index'] = index_array
        data2['index'] = index_array
        
        #Retrieve signal data arrays
        sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, self.signal, 
                                                              self.noise, self.jones_vector) 
        #Update freq domain arrays (to adjust for pol)
        self.Y = np.fft.fft(sig)
        self.Y = np.fft.fftshift(self.Y)
        self.N = np.fft.fft(noise)
        self.N = np.fft.fftshift(self.N)     
        
        self.signalBrowser.setCurrentFont(self.font_bold)
        self.signalBrowser.append(' ')
        if self.radioButtonSigTime.isChecked() == 1:
            data1['x'] = self.time[self.start_index-1:self.end_index-1]
            if self.radioButtonComplexSignalData.isChecked() == 1:
                self.signalBrowser.append('Signal data (index, time(s), e_field):')
                data1['y'] = sig[self.start_index-1:self.end_index-1]
            else:
                self.signalBrowser.append('Signal data (index, time(s), e_field(mag), e-field(ph)):')
                data1['y1'] = np.abs(sig[self.start_index-1:self.end_index-1])
                data1['y2'] = np.angle(sig[self.start_index-1:self.end_index-1])
                
        else:
            data1['x'] = self.frq[self.start_index-1:self.end_index-1]
            if self.radioButtonComplexSignalData.isChecked() == 1:
                self.signalBrowser.append('Signal data (index, freq(Hz), e_field):')
                data1['y'] = self.Y[self.start_index-1:self.end_index-1]
            else:
                self.signalBrowser.append('Signal data (index, freq(Hz), e_field(mag), e-field(ph)):')
                data1['y1'] = np.abs(self.Y[self.start_index-1:self.end_index-1])
                data1['y2'] = np.angle(self.Y[self.start_index-1:self.end_index-1])
        self.signalBrowser.setCurrentFont(self.font_normal)
                
        self.linewidth = 60
        if self.linewidthSignalData.text():
            self.linewidth = int(self.linewidthSignalData.text())

        self.signalBrowser.append(np.array2string(data1, max_line_width = self.linewidth))
        
        self.signalBrowser.setCurrentFont(self.font_bold)
        self.signalBrowser.append(' ')
        if self.radioButtonSigTime.isChecked() == 1:           
            data2['x'] = self.time[self.start_index-1:self.end_index-1]
            if self.radioButtonComplexSignalData.isChecked() == 1:
                self.signalBrowser.append('Noise data (index, time(s), e_field):')
                data2['y'] = noise[self.start_index-1:self.end_index-1]
            else:
                self.signalBrowser.append('Noise data (index, time(s), e_field(mag), e-field(ph)):')
                data2['y1'] = np.abs(noise[self.start_index-1:self.end_index-1])
                data2['y2'] = np.angle(noise[self.start_index-1:self.end_index-1])
        else:
            data2['x'] = self.frq[self.start_index-1:self.end_index-1]
            if self.radioButtonComplexSignalData.isChecked() == 1:
                self.signalBrowser.append('Noise data (index, freq(Hz), e_field):')
                data1['y'] = self.N[self.start_index-1:self.end_index-1]
            else:
                self.signalBrowser.append('Noise data (index, freq(Hz), e_field(mag), e-field(ph)):')
                data1['y1'] = np.abs(self.N[self.start_index-1:self.end_index-1])
                data1['y2'] = np.angle(self.N[self.start_index-1:self.end_index-1]) 
        self.signalBrowser.setCurrentFont(self.font_normal)
        self.signalBrowser.append(np.array2string(data2, max_line_width = self.linewidth))
        
        if self.radioButtonSigFreq.isChecked() == 1:
            self.signalBrowser.setCurrentFont(self.font_bold)
            self.signalBrowser.append(' ')
            self.signalBrowser.append('PSD data (freq(Hz), PSD(W/Hz):')
            self.signalBrowser.setCurrentFont(self.font_normal)
            self.signalBrowser.append('Freq group width(Hz): '+ str(self.ng_w))
            data3['x'] = self.freq_points
            data3['y'] = self.noise_freq_psd
            self.signalBrowser.append(np.array2string(data3, max_line_width = self.linewidth))
        
        cursor = self.signalBrowser.textCursor()
        cursor.setPosition(0);
        self.signalBrowser.setTextCursor(cursor);    
        
    '''Signal metrics tab=================================================================
    '''
    def iteration_change_signal_metrics(self):
        new_iteration = int(self.spinBoxSignalMetrics.value())
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[4]
        
        key = str(self.waveKeyListSignalMetrics.currentText())        
        for k in range(len(optical_list)):
            if optical_list[k][0] == key:
                break
        index_key = k
        
        
        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.noise = optical_list[index_key][4]
        self.jones_vector = optical_list[index_key][2]
        self.channel_freq = optical_list[index_key][1]
        self.update_signal_metrics()
        
    def update_signal_metrics(self):
        pol = 'X-Y'
        if self.radioButtonPolXSignalMetrics.isChecked() == 1:
            pol = 'X'
        if self.radioButtonPolYSignalMetrics.isChecked() == 1:
            pol = 'Y'
        
        sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, self.signal, 
                                                              self.noise, self.jones_vector)
        # Signal statistics
        sig_mean = np.mean(sig_pwr)
        self.signalMean.setText(str(format(sig_mean, '0.3E')))
        noise_var = np.var(sig_pwr)
        self.signalVar.setText(str(format(noise_var, '0.3E')))
        noise_std_dev = np.std(sig_pwr)
        self.signalStdDev.setText(str(format(noise_std_dev, '0.3E')))
        
        sig_tot_pwr = np.sum(sig_pwr)
        self.signalTotalPwr.setText(str(format(sig_tot_pwr, '0.3E')))
        if sig_tot_pwr > 0:
            sig_tot_pwr_dbm = 10*np.log10(sig_tot_pwr*1e3)
            self.signalTotalPwrDbm.setText(str(format(sig_tot_pwr_dbm, '0.3E')))   
        else:
            self.signalTotalPwrDbm.setText('NA')
             
        sig_avg_pwr = np.sum(sig_pwr)/self.n
        self.signalAvgPwr.setText(str(format(sig_avg_pwr, '0.3E')))       
        if sig_avg_pwr > 0:
            sig_avg_pwr_dbm = 10*np.log10(sig_avg_pwr*1e3)
            self.signalAvgPwrDbm.setText(str(format(sig_avg_pwr_dbm, '0.3E')))
        else:
            self.signalAvgPwrDbm.setText('NA')
        
        # Noise statistics
        noise_mean = np.mean(noise_pwr)
        self.noiseMean.setText(str(format(noise_mean, '0.3E')))
        noise_var = np.var(noise_pwr)
        self.noiseVar.setText(str(format(noise_var, '0.3E')))
        noise_std_dev = np.std(noise_pwr)
        self.noiseStdDev.setText(str(format(noise_std_dev, '0.3E')))
        
        noise_tot_pwr = np.sum(noise_pwr)
        self.noiseTotalPwr.setText(str(format(noise_tot_pwr, '0.3E')))      
        if noise_tot_pwr > 0:
            noise_tot_pwr_dbm = 10*np.log10(noise_tot_pwr*1e3)
            self.noiseTotalPwrDbm.setText(str(format(noise_tot_pwr_dbm, '0.3E')))   
        else:
            self.noiseTotalPwrDbm.setText('NA')
            
        noise_avg_pwr = np.sum(noise_pwr)/self.n
        self.noiseAvgPwr.setText(str(format(noise_avg_pwr, '0.3E')))        
        if noise_avg_pwr > 0:
            noise_avg_pwr_dbm = 10*np.log10(noise_avg_pwr*1e3)
            self.noiseAvgPwrDbm.setText(str(format(noise_avg_pwr_dbm, '0.3E')))
        else:
            self.noiseAvgPwrDbm.setText('NA')
             
        psd_linear = noise_tot_pwr/self.fs
        self.noisePSDLinear.setText(str(format(psd_linear, '0.3E')))
        if psd_linear > 0:   
            psd_linear_dbm = 10*np.log10(psd_linear*1e3)
            self.noisePSDLineardBm.setText(str(format(psd_linear_dbm, '0.3E'))) 
        else:
            self.noisePSDLineardBm.setText('NA')   
        # Noise spectral density (avg) - PSD/num samples
        psd_linear_avg = noise_tot_pwr/self.fs/self.n
        self.noisePSDLinearAvg.setText(str(format(psd_linear_avg, '0.3E')))
        if psd_linear_avg > 0:   
            psd_linear_dbm_avg = 10*np.log10(psd_linear_avg*1e3)
            self.noisePSDLineardBmAvg.setText(str(format(psd_linear_dbm_avg, '0.3E'))) 
        else:
            self.noisePSDLineardBmAvg.setText('NA')       
 
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_freq)
        plt.close(self.figure_pol)
               
'''FUNCTIONS================================================================'''
#def set_mpl_cursor():
#    mplcursors.cursor(multiple=False).connect("add", 
#                     lambda sel: sel.annotation.get_bbox_patch().set(fc="lightyellow", alpha=1))
    
def set_icon_window():
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLab_64.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
'''========================================================================='''
