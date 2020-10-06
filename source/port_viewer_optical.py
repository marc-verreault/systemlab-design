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

    ABOUT THIS MODULE
    SystemLab module for port analyzer(GUI) class: SignalAnalogOptical
'''
import os
import config
gui_ui_path = config.root_path

import sys # MV 20.01.r2 24-Feb-20
import traceback # MV 20.01.r2 24-Feb-20

# MV 20.01.r1 29-Oct-2019
# Import config_port_viewers as cfg_opt and config_special as cfg_special
import importlib
cfg_port_viewers_path = str('syslab_config_files.config_port_viewers')
cfg_opt = importlib.import_module(cfg_port_viewers_path)
cfg_special_path = str('syslab_config_files.config_special')
cfg_special = importlib.import_module(cfg_special_path)


import numpy as np
import matplotlib
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

#import matplotlib as mpl
matplotlib.rcParams['figure.dpi'] = 80

# https://matplotlib.org/api/ticker_api.html#matplotlib.ticker.Formatter
matplotlib.rcParams['axes.formatter.useoffset'] = False # Removes offset from all plots
matplotlib.rcParams['axes.formatter.limits'] = [-4, 4] # Limits for exponential notation

style = """QLineEdit { background-color: rgb(245, 245, 245); color: rgb(50, 50, 50) }"""

# MV 20.01.r3 15-Jun-20
style_spin_box = """QSpinBox {color: darkBlue; background: white;
                              selection-color: darkBlue;
                              selection-background-color: white;}"""

style_combo_box = """QComboBox {color: darkBlue; background: white;
                              selection-color: darkBlue;
                              selection-background-color: white;}"""


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
        self.setStyleSheet(cfg_special.global_font) # MV 20.01.r1 17-Dec-2019 
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.fb_name = fb_name
        self.port_name = port_name
        self.direction = direction
        self.signals = signal_data # List of signals for each iteration      
        self.fs = design_settings['sampling_rate'] 
        
        # MV 20.01.r3 15-Jun-20 Set iteration to reflect main application setting
        # (iterators spin box)
        current_iter = int(design_settings['current_iteration'])
        if (current_iter - 1) <= len(self.signals):
            self.iteration = current_iter
        else:
            self.iteration = int(len(self.signals))

        # MV 20.01.r3 13-Jun-20 Added functional block and port data info to
        # Window title box
        self.setWindowTitle('Optical signal data analyzer (' + 
                            str(self.fb_name) + ', Port: ' + 
                            str(self.port_name) + ', Dir: ' + 
                            str(self.direction) + ')')
        
        self.dual_pol_data = False # MV 20.01.r1 5-Dec-2019
        
        '''Time data tab (dataFrame)==================================================='''
        #Top level settings
        self.totalSamplesTime.setText(str(format(design_settings['num_samples'], '0.3E')))
        self.samplingPeriod.setText(str(format(design_settings['sampling_period'], '0.3E')))
        self.timeWindow.setText(str(format(design_settings['time_window'], '0.3E')))     
        #Iterations/Channels group box (Time data tab)
        iterations = len(signal_data)   
        self.spinBoxTime.setMaximum(iterations)
        self.spinBoxTime.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsTime.setText(str(iterations))        
        self.spinBoxTime.valueChanged.connect(self.iteration_change_time) 

        self.waveKeyListTime.setStyleSheet(style_combo_box) # MV 20.01.r3 15-Jun-20  
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
        self.spinBoxFreq.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsFreq.setText(str(iterations))
        self.spinBoxFreq.valueChanged.connect(self.iteration_change_freq) 
        #self.waveKeyListFreq.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.waveKeyListFreq.setStyleSheet(style_combo_box) # MV 20.01.r3 15-Jun-20
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
        #Y-axis settings group box (Main sub-tab) 
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
        self.spinBoxPol.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxPol.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxPol.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxPol.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsPol.setText(str(iterations))
        self.spinBoxPol.valueChanged.connect(self.iteration_change_pol)
        #self.waveKeyListPol.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.waveKeyListPol.setStyleSheet(style_combo_box) # MV 20.01.r3 15-Jun-20
        self.waveKeyListPol.currentIndexChanged.connect(self.iteration_change_pol)
        #Adjust view box
        self.elevationPosCurrent.setStyleSheet(style)
        self.azimuthPosCurrent.setStyleSheet(style)
        self.elevationPos.setText(str(format(10, 'n')))        
        self.azimuthPos.setText(str(format(25, 'n')))
        self.actionSphereView.clicked.connect(self.update_poincare_sphere)
        
        '''Signal data tab (dataFrameSignal)==========================================='''
        #Iterations group box
        iterations = len(signal_data)   
        self.spinBoxSignalData.setMaximum(iterations)
        self.spinBoxSignalData.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsSignalData.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iteration_change_signal_data)
        #self.waveKeyListSignalData.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.waveKeyListSignalData.setStyleSheet(style_combo_box) # MV 20.01.r3 15-Jun-20
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
        self.spinBoxSignalMetrics.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalMetrics.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalMetrics.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalMetrics.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsSignalMetrics.setText(str(iterations))
        self.spinBoxSignalMetrics.valueChanged.connect(self.iteration_change_signal_metrics)
        #self.waveKeyListSignalMetrics.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.waveKeyListSignalMetrics.setStyleSheet(style_combo_box) # MV 20.01.r3 15-Jun-20
        self.waveKeyListSignalMetrics.currentIndexChanged.connect(self.iteration_change_signal_metrics)
        #Polarization group box 
        self.radioButtonPolXYSignalMetrics.toggled.connect(self.update_signal_metrics)
        self.radioButtonPolXSignalMetrics.toggled.connect(self.update_signal_metrics)
        self.radioButtonPolYSignalMetrics.toggled.connect(self.update_signal_metrics)
        
        '''All channels tab (dataFrameAllCh)==============================================='''
        #Top level settings (Main sub-tab)  
        self.totalSamplesAllCh.setText(str(format(design_settings['num_samples'], '0.3E'))) 
        self.samplingRateAllCh.setText(str(format(self.fs, '0.3E')))
        #Iterations group box (Main sub-tab)        
        self.spinBoxAllCh.setMaximum(iterations)
        self.spinBoxAllCh.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxAllCh.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxAllCh.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxAllCh.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsAllCh.setText(str(iterations))
        # MV 20.01.r3 14-Jun-20 Was missing call to update channels after selecting
        # spin box
        self.spinBoxAllCh.valueChanged.connect(self.check_signal_changed_all_ch)
        #Spectral resolution group box (Main sub-tab) 
        self.signalCheckBoxEnableResolutionAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        self.actionResolutionWindowAllCh.clicked.connect(self.check_signal_changed_all_ch)
        #Signal type group box (Main sub-tab) 
        self.signalCheckBoxAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        self.noiseCheckBoxAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        self.sigandnoiseCheckBoxAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        self.noisegroupCheckBoxAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        self.radioButtonLinearAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.radioButtonLinearSpectralAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.radioButtonLogAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.radioButtonLogSpectralAllCh.toggled.connect(self.check_signal_changed_all_ch)
        #Polarization group box (Main sub-tab)
        self.radioButtonPolXYAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.radioButtonPolXAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.radioButtonPolYAllCh.toggled.connect(self.check_signal_changed_all_ch)
        #Plot settings (Main sub-tab)
        self.radioButtonHzAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.radioButtonNmAllCh.toggled.connect(self.check_signal_changed_all_ch)
        self.checkBoxMajorGridAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        self.checkBoxMinorGridAllCh.stateChanged.connect(self.check_signal_changed_all_ch)      
        self.checkBoxLegendAllCh.stateChanged.connect(self.check_signal_changed_all_ch)
        #Y-axis settings group box (Main sub-tab)
        self.actionWindowYAxisAllCh.clicked.connect(self.update_axis_all_ch)    
        #Freq axis settings group box (Main sub-tab)
        self.actionAllChWindow.clicked.connect(self.update_axis_all_ch)
        #Line and rectangular plots/annotations group boxes (Annotation sub-tab)
        
        '''Prepare signal data for iteration 1 (default)==============================='''
        signal_default = self.signals[self.iteration]
        self.time = signal_default[3] #Time sampling points
        self.noise_freq = signal_default[4] #MV 20.01.r1 
        optical_list = signal_default[5] #MV 20.01.r1 (previously signal_default[4])       
        self.signal = optical_list[0][3]
        self.noise = optical_list[0][4]
        # MV 20.01.r1 5-Dec-2019
        #https://stackoverflow.com/questions/21299798/check-if-numpy-array-is-multidimensional-or-not
        #https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.ndim.html
        if self.signal.ndim == 2: #X and Y pol are held in separate complex arrays (2, n) 
            self.dual_pol_data = True
        self.n = None
        if self.dual_pol_data:
            self.n = int(len(self.signal[0]))
        else:
            self.n = int(len(self.signal))
        #self.noise_freq = optical_list[0][5] #MV 20.01.r1
        
        self.jones_vector = optical_list[0][2]
        #Freq data tab (top level settings for channel info)
        self.channel_freq = optical_list[0][1]
        self.opticalChTime.setText(str(format(self.channel_freq, '0.5E')))
        self.opticalChFreq.setText(str(format(self.channel_freq, '0.5E')))  
        self.frq = self.update_freq_array(self.n, self.channel_freq)
        
        '''Prepare frequency domain analysis==========================================='''
        # REF:  Fast Fourier Transform in matplotlib, 
        # An example of FFT audio analysis in matplotlib and the fft function.
        # Source: https://plot.ly/matplotlib/fft/(accessed 20-Mar-2018) 
        '''self.Y_x = np.full(self.n, 0 + 1j*0, dtype=complex)
        self.Y_y = np.full(self.n, 0 + 1j*0, dtype=complex)
        self.Y_N_x = np.full(self.n, 0 + 1j*0, dtype=complex)
        self.Y_N_y = np.full(self.n, 0 + 1j*0, dtype=complex)
        self.Y = np.full(self.n, 0 + 1j*0, dtype=complex)
        self.Y_N = np.full(self.n, 0 + 1j*0, dtype=complex)       
        if self.dual_pol_data:
            self.Y_x = np.fft.fft(self.signal[0])
            self.Y_x = np.fft.fftshift(self.Y_x)   
            self.Y_y = np.fft.fft(self.signal[1])
            self.Y_y = np.fft.fftshift(self.Y_y)    
        else:
            self.Y = np.fft.fft(self.signal)
            self.Y = np.fft.fftshift(self.Y)
        self.frq = self.update_freq_array(self.n, self.channel_freq)
        #FFT computations (signal, noise, signal+noise)
        self.N = np.fft.fft(self.noise)
        self.N = np.fft.fftshift(self.N) 
        if self.dual_pol_data:
            self.Y_N_x = np.fft.fft(self.signal[0] + self.noise)
            self.Y_N_x = np.fft.fftshift(self.Y_N_x)
            self.Y_N_y = np.fft.fft(self.signal[1] + self.noise)
            self.Y_N_y = np.fft.fftshift(self.Y_N_y)
        else:
            self.Y_N = np.fft.fft(self.signal + self.noise)
            self.Y_N = np.fft.fftshift(self.Y_N)'''
        
        '''Setup background colors for frames=========================================='''
        p = self.graphFrame.palette()
        color = QtGui.QColor(cfg_opt.optical_frame_background_color) # MV 20.01.r1 29-Oct-19
        p.setColor(self.graphFrame.backgroundRole(), color)
        self.graphFrame.setPalette(p)       
        p2 = self.dataFrame.palette()
        p2.setColor(self.dataFrame.backgroundRole(), color)
        self.dataFrame.setPalette(p2)
        p3 = self.graphFrameFreq.palette() 
        p3.setColor(self.graphFrameFreq.backgroundRole(), color)
        self.graphFrameFreq.setPalette(p3)
        p4 = self.dataFrameFreq.palette() 
        p4.setColor(self.dataFrameFreq.backgroundRole(), color)
        self.dataFrameFreq.setPalette(p4)
        p5 = self.dataFrameMainFreq.palette() 
        p5.setColor(self.dataFrameMainFreq.backgroundRole(), color)
        self.dataFrameMainFreq.setPalette(p5)
        p6 = self.dataFrameAnnotationsFreq.palette()
        p6.setColor(self.dataFrameAnnotationsFreq.backgroundRole(), color)
        self.dataFrameAnnotationsFreq.setPalette(p6)
        p7 = self.dataFramePol.palette() 
        p7.setColor(self.dataFramePol.backgroundRole(), color)
        self.dataFramePol.setPalette(p7)
        p8 = self.graphFramePol.palette()
        p8.setColor(self.graphFramePol.backgroundRole(), color)
        self.graphFramePol.setPalette(p8)
        p9 = self.dataFrameAllCh.palette()
        p9.setColor(self.dataFrameAllCh.backgroundRole(), color)
        self.dataFrameAllCh.setPalette(p9)
        p10 = self.graphFrameAllCh.palette()
        p10.setColor(self.graphFrameAllCh.backgroundRole(), color)
        self.graphFrameAllCh.setPalette(p10)
        
        '''Setup matplotlib figures and toolbars======================================='''
        #Time data
        self.graphLayout = QtWidgets.QVBoxLayout()
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure = plt.figure(facecolor = cfg_opt.optical_time_fig_back_color)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.tab_time)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)
        #Frequency data
        self.graphLayoutFreq = QtWidgets.QVBoxLayout()
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure_freq = plt.figure(facecolor=cfg_opt.optical_freq_fig_back_color)
        self.canvas_freq = FigureCanvas(self.figure_freq)
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self.tab_freq)
        self.graphLayoutFreq.addWidget(self.canvas_freq)
        self.graphLayoutFreq.addWidget(self.toolbar_freq)
        self.graphFrameFreq.setLayout(self.graphLayoutFreq)
        #Polarization analyis
        self.graphLayoutPol = QtWidgets.QVBoxLayout()
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure_pol = plt.figure(facecolor=cfg_opt.optical_frame_background_color)
        self.canvas_pol = FigureCanvas(self.figure_pol)
        self.graphLayoutPol.addWidget(self.canvas_pol)
        self.graphFramePol.setLayout(self.graphLayoutPol)
        self.canvas_pol.mpl_connect('button_release_event', self.onclick)
        #All channels
        self.graphLayoutAllCh = QtWidgets.QVBoxLayout()
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure_all_ch = plt.figure(facecolor=cfg_opt.opt_chnls_freq_fig_back_color)
        self.canvas_all_ch = FigureCanvas(self.figure_all_ch)
        self.toolbar_all_ch = NavigationToolbar(self.canvas_all_ch, self.tab_channels)
        self.graphLayoutAllCh.addWidget(self.canvas_all_ch)
        self.graphLayoutAllCh.addWidget(self.toolbar_all_ch)
        self.graphFrameAllCh.setLayout(self.graphLayoutAllCh)  
                
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
        
        self.tabData.setCurrentWidget(self.tab_channels) 
        self.figure_all_ch.set_tight_layout(True)
        self.iteration_change_all_ch()
        self.canvas_all_ch.draw()       
           
        #Load wave key lists
        k = len(optical_list)
        for k in range(0, k):
            key = str(optical_list[k][0])
            self.waveKeyListTime.addItem(key) 
            self.waveKeyListFreq.addItem(key)
            self.waveKeyListPol.addItem(key)
            self.waveKeyListSignalData.addItem(key)
            self.waveKeyListSignalMetrics.addItem(key)
        self.numberOptChannels.setText(str(k+1)) #Update Rel 20.01.r1 28-Aug-19
                                                 #Added +1 to correct key index
                                                 
        '''Prepare default data for signal data and signal metrics viewers============='''
        self.iteration_change_signal_data()
        self.update_signal_data()
        self.update_signal_metrics()                                                     
                                                 
        #Return to time tab
        self.tabData.setCurrentWidget(self.tab_time)
        
    '''Time data tab (plotting methods)================================================'''
    def iteration_change_time(self):
        new_iteration = int(self.spinBoxTime.value())
        lineEdit = self.spinBoxTime.findChildren(QtWidgets.QLineEdit)
        lineEdit[0].deselect()
        config.app.processEvents()
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[5] #MV 20.01.r1 (previously signal_updated[4])
        
        key = str(self.waveKeyListTime.currentText())        
        for k in range(len(optical_list)):
            #MV Rel 20.01.r1 28-Aug-19: Converted key from str to int (dict was 
            #defaulting to last key)
            if optical_list[k][0] == int(key): 
                break
        index_key = k

        self.signal = optical_list[index_key][3] # X+Y (combined field)
        self.jones_vector = optical_list[index_key][2]
        self.noise = optical_list[index_key][4]           
        ch_freq = optical_list[index_key][1]
        self.opticalChTime.setText(str(format(ch_freq, '0.5E')))
        
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
        # MV 20.01.r1 Added new feature to select plot area background color
        back_color = cfg_opt.optical_time_plot_back_color
        self.ax = self.figure.add_subplot(111, facecolor = back_color)
        self.ax.clear() #MV Rel 20.01.r1 15-Sep-19
        
        #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
        self.ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
        self.ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
                    
        if axis_adjust == 1:
            if self.minTime.text() and self.maxTime.text():
                start_time = self.minTime.text()
                end_time = self.maxTime.text()
                self.ax.set_xlim(float(start_time), float(end_time))
            if self.startYAxisTime.text() and self.endYAxisTime.text():
                start_val = self.startYAxisTime.text()
                end_val = self.endYAxisTime.text()
                self.ax.set_ylim(float(start_val), float(end_val))    
            
        if self.radioButtonLinear.isChecked() == 1:
            self.ax.set_ylabel('Power (W)')
        else:
            self.ax.set_ylabel('Power (dBm)')
            
        pol = 'X-Y'
        if self.radioButtonPolX.isChecked() == 1:
            pol = 'X'
        if self.radioButtonPolY.isChecked() == 1:
            pol = 'Y'

        sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, self.signal,
                                                              self.noise, self.jones_vector)
        
        #20.01.r1 2 Sep 19 - Updated this section by introducing new functions=============
        #to adjust plotting (adjust_units_for_plotting_time)
        if self.signalCheckBox.checkState() == 2:
            if self.radioButtonLinear.isChecked() == 1:
                self.set_signal_plot_time_domain(sig_pwr) 
            else:
                # MV 20.01.r3 9-Jun-20: Changed sig_pwr to sig_pwr_dbm
                sig_pwr_dbm = self.adjust_units_for_plotting_time(sig_pwr)
                self.set_signal_plot_time_domain(sig_pwr_dbm)
            
        if self.noiseCheckBox.checkState() == 2:
            if self.radioButtonLinear.isChecked() == 1:
                self.set_noise_plot_time_domain(noise_pwr)
            else:
                # MV 20.01.r3 9-Jun-20: Changed noise_pwr to noise_pwr_dbm
                noise_pwr_dbm = self.adjust_units_for_plotting_time(noise_pwr)
                self.set_noise_plot_time_domain(noise_pwr_dbm)
            
        if self.sigandnoiseCheckBox.checkState() == 2:
            # MV 20.01.r3 9-Jun-20 Bug fix, was adding sig_pwr+noise_pwr directly
            # Correct calculation: np.abs(sig + noise)*np.abs(sig + noise)
            sig_noise_pwr = np.abs(sig + noise)*np.abs(sig + noise)
            if self.radioButtonLinear.isChecked() == 1:
                self.set_signal_and_noise_plot_time_domain(sig_noise_pwr)
            else:
                sig_noise_pwr_dbm = self.adjust_units_for_plotting_time(sig_noise_pwr)
                self.set_signal_and_noise_plot_time_domain(sig_noise_pwr_dbm)
        #=================================================================================
        if self.sigPhaseCheckBox.checkState() == 2:
            self.ax2 = self.ax.twinx()           
            # MV 20.01.r1 5-Dec-2019 Phase shown is for Exy
            if self.dual_pol_data:
                if np.abs(self.jones_vector[0]) > 0: # To avoid NaN condition (0/0)
                    phase_map = np.angle(self.signal[0]/self.jones_vector[0])
                else:
                    phase_map = np.angle(self.signal[1]/self.jones_vector[1])
            else:
                phase_map = np.angle(self.signal)
                
            if self.unwrapPhaseCheckBox.checkState() == 2:
                phase_map = np.unwrap(phase_map)
                
            if self.radioButtonDeg.isChecked() == 1:
                phase_map = np.rad2deg(phase_map)
                self.ax2.set_ylabel('Phase (deg)')
            else:
                self.ax2.set_ylabel('Phase (rad)')
                
            self.ax2.plot(self.time, phase_map, 
                          color=cfg_opt.optical_time_phase_color,
                          linestyle=cfg_opt.optical_time_phase_linestyle,
                          linewidth=cfg_opt.optical_time_phase_linewidth, 
                          marker=cfg_opt.optical_time_phase_marker,
                          markersize=cfg_opt.optical_time_phase_markersize, 
                          label = 'Optical phase')  
            self.ax2.set_aspect('auto')
        
        # MV 20.01.r1 15-Sep-19 (Shortended title - causing issues with tight layout)
        self.ax.set_title('Carrier envelope (' + str(self.fb_name) + ', Port:' + str(self.port_name) +
                                          ', Dir:' + str(self.direction) + ', Pol:' + str(pol) + ')')
        
        # MV 20.01.r3 5-Jun-20
        self.ax.title.set_color(cfg_opt.optical_time_labels_axes_color)
            
        self.ax.set_xlabel('Time (sec)')
        self.ax.set_aspect('auto')
        self.ax.format_coord = self.format_coord_time
        
        # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks        
        self.ax.xaxis.label.set_color(cfg_opt.optical_time_labels_axes_color)
        self.ax.yaxis.label.set_color(cfg_opt.optical_time_labels_axes_color)
        self.ax.tick_params(axis='both', which ='both', 
                            colors=cfg_opt.optical_time_labels_axes_color)
        
        #Plot settings (grid and legend)
        # MV 20.01.r1 Linked plot settings to config file variables (to provide ability to
        # manage look and feel of plots)  
        if self.checkBoxMajorGrid.checkState() == 2:
            self.ax.grid(True)  
            self.ax.grid(which='major', 
                         linestyle = cfg_opt.optical_time_maj_grid_linestyle, 
                         linewidth = cfg_opt.optical_time_maj_grid_linewidth, 
                         color = cfg_opt.optical_time_maj_grid_color)
       
        if self.checkBoxMinorGrid.checkState() == 2:
            self.ax.minorticks_on()
            self.ax.grid(which='minor', 
                         linestyle = cfg_opt.optical_time_min_grid_linestyle, 
                         linewidth = cfg_opt.optical_time_min_grid_linewidth, 
                         color = cfg_opt.optical_time_min_grid_color )
            
        if self.checkBoxLegend.isChecked() == 1:
            self.ax.legend()
            if self.sigPhaseCheckBox.checkState() == 2:
                self.ax2.legend()
                
    def set_signal_data(self, pol, signal, noise, jones):
        # MV 20.01.r1 5-Dec-2019 Updates to polarization arrays
        signal_return = None
        if pol == 'X':
            if self.dual_pol_data:
                signal_return = signal[0]
            else:
                signal_return = jones[0]*signal
            noise = jones[0]*noise
            # I = Sum of squared magnitude of Ex field 
            sig_power = np.abs(signal_return)*np.abs(signal_return)
            noise_power = np.abs(noise)*np.abs(noise)
        elif pol == 'Y':
            if self.dual_pol_data:
                signal_return = signal[1]
            else:
                signal_return = jones[1]*signal
            noise = jones[1]*noise
            # I = Sum of squared magnitude of Ey field 
            sig_power = np.abs(signal_return)*np.abs(signal_return)
            noise_power = np.abs(noise)*np.abs(noise)
        else:
            if self.dual_pol_data:
                if np.abs(jones[0]) > 0: # To avoid NaN condition (0/0)
                    signal_return = signal[0]/jones[0]
                else:
                    signal_return = signal[1]/jones[1]
                # I = Sum of squared magnitudes of Ex and Ey fields 
                sig_power =  (np.abs(signal[0]))**2 + (np.abs(signal[1]))**2
            else:
                signal_return = signal
                # I = Sum of squared magnitudes of Ex and Ey fields 
                sig_power = ( (np.abs(jones[0]*signal_return))**2 
                             + (np.abs(jones[1]*signal_return))**2 )
            noise_power = np.abs(noise)*np.abs(noise)
        return signal_return, noise, sig_power, noise_power
    
    #20.01.r1 2 Sep 19 - New functions for plotting=======================================
    def adjust_units_for_plotting_time(self, signal):
        if np.count_nonzero(signal) == np.size(signal): 
            signal = 10*np.log10(signal*1e3)
        else:
            signal += 1e-30 #Set to very low value
            signal = 10*np.log10(signal*1e3)  
        return signal
    
    
    # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to provide ability to
    # manage look and feel of plots)  
    def set_signal_plot_time_domain(self, signal):
        self.ax.plot(self.time, signal,
                     color = cfg_opt.optical_time_signal_color, 
                     linestyle = cfg_opt.optical_time_signal_linestyle, 
                     linewidth = cfg_opt.optical_time_signal_linewidth, 
                     marker = cfg_opt.optical_time_signal_marker, 
                     markersize = cfg_opt.optical_time_signal_markersize,
                     label = 'Optical signal') 
        
    def set_noise_plot_time_domain(self, signal):
        self.ax.plot(self.time, signal, 
                     color = cfg_opt.optical_time_noise_color, 
                     linestyle = cfg_opt.optical_time_noise_linestyle, 
                     linewidth = cfg_opt.optical_time_noise_linewidth, 
                     marker = cfg_opt.optical_time_noise_marker, 
                     markersize = cfg_opt.optical_time_noise_markersize,
                     label = 'Optical noise')   
        
    def set_signal_and_noise_plot_time_domain(self, signal):
        self.ax.plot(self.time, signal, 
                     color = cfg_opt.optical_time_sig_noise_color, 
                     linestyle = cfg_opt.optical_time_sig_noise_linestyle, 
                     linewidth = cfg_opt.optical_time_sig_noise_linewidth, 
                     marker = cfg_opt.optical_time_sig_noise_marker, 
                     markersize = cfg_opt.optical_time_sig_noise_markersize,
                     label = 'Optical signal + noise')
    #=====================================================================================
                
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
        lineEdit = self.spinBoxFreq.findChildren(QtWidgets.QLineEdit)
        lineEdit[0].deselect()
        config.app.processEvents()
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[5] #MV 20.01.r1 (previously signal_updated[4])
        
        key = str(self.waveKeyListFreq.currentText())        
        for k in range(len(optical_list)):
            #MV Rel 20.01.r1 28-Aug-19: Converted key from str to int (dict was 
            #defaulting to last key)
            if optical_list[k][0] == int(key):
                break
        index_key = k
        
        self.channel_freq = optical_list[index_key][1]
        self.opticalChFreq.setText(str(format(self.channel_freq, '0.5E')))
        
        #self.frq = self.update_freq_array(self.n, self.channel_freq)
        self.jones_vector = optical_list[index_key][2]
        self.signal = optical_list[index_key][3]
        self.noise = optical_list[index_key][4]
        # PSD noise array
        #self.noise_freq = optical_list[index_key][5]
        self.noise_freq = signal_updated[4] #MV 20.01.r1
        self.frq = self.update_freq_array(self.n, self.channel_freq)
          
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
        try:
            self.ng_w = self.noise_freq[0, 1] - self.noise_freq[0, 0]
            self.noise_freq_psd = self.noise_freq[1, :]
            self.noise_freq_pwr = self.noise_freq[1, :] * self.ng_w
            self.freq_points = self.noise_freq[0, :]
            
            pol = 'X+Y'
            if self.radioButtonPolXFreq.isChecked() == 1:
                pol = 'X'
                self.noise_freq_psd = 0.5*self.noise_freq_psd #MV 20.01.r1 7-Dec-19 (DoP is 0%)
                self.noise_freq_pwr = 0.5*self.noise_freq_pwr
                
            if self.radioButtonPolYFreq.isChecked() == 1:
                pol = 'Y'
                self.noise_freq_psd = 0.5*self.noise_freq_psd #MV 20.01.r1 7-Dec-19 (DoP is 0%)
                self.noise_freq_pwr = 0.5*self.noise_freq_pwr
    
            sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, self.signal,
                                                    self.noise, self.jones_vector)
            
            # Calculate fft for signal
            self.Y = np.fft.fft(sig)
            self.Y = np.fft.fftshift(self.Y)
            # MV 20.01.r3 18-Sep-20 Bug fix:
            # np.abs(self.Y)*np.abs(self.Y) is now divided by n^2, 
            # previously was incorrectly dividing by n
            # Same applies for noise and sig+noise
            optical_power_fft = np.abs(self.Y)*np.abs(self.Y)/(self.n*self.n)
            
            # Calculate fft for noise
            self.N = np.fft.fft(noise)
            self.N = np.fft.fftshift(self.N)
            optical_noise_fft = np.abs(self.N)*np.abs(self.N)/(self.n*self.n)
            
            # Calculate fft for signal + noise
            self.Y_N = np.fft.fft(sig + noise)
            self.Y_N = np.fft.fftshift(self.Y_N)
            optical_signal_and_noise_fft = np.abs(self.Y_N)*np.abs(self.Y_N)/(self.n*self.n)
            
            self.figure_freq.clf()
            # MV 20.01.r1 Added new feature to select plot area background color
            back_color = cfg_opt.optical_freq_plot_back_color
            self.af = self.figure_freq.add_subplot(111, facecolor = back_color)
            self.af.clear() #MV Rel 20.01.r1 15-Sep-19
                                                                                          
            #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
            self.af.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
            self.af.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
            
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
                
                #MV 20.01.r1 31-Aug-19 Added check in case field is left blank================
                if self.spectralResolution.text(): 
                    window = float(self.spectralResolution.text())
                else:
                    window = self.fs
                #=============================================================================
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
                optical_power_fft = self.adjust_units_for_plotting_freq(optical_power_fft)
                self.set_signal_plot_freq_domain(optical_power_fft)
    
            if self.noiseCheckBoxFreq.checkState() == 2:
                optical_noise_fft = self.adjust_units_for_plotting_freq(optical_noise_fft)
                self.set_noise_plot_freq_domain(optical_noise_fft)
                    
            if self.sigandnoiseCheckBoxFreq.checkState() == 2:
                optical_signal_and_noise_fft = self.adjust_units_for_plotting_freq(optical_signal_and_noise_fft)
                self.set_signal_and_noise_plot_freq_domain(optical_signal_and_noise_fft)
                    
            if self.noisegroupCheckBoxFreq.checkState() == 2:
                if self.radioButtonLinearFreq.isChecked() == 1:
                    self.set_psd_noise_plot_freq_domain(self.noise_freq_pwr)
                elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                    self.set_psd_noise_plot_freq_domain(self.noise_freq_psd)
                elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                    self.set_psd_noise_plot_freq_domain(10*np.log10(self.noise_freq_psd*1e3))   
                else:
                    self.set_psd_noise_plot_freq_domain(10*np.log10(self.noise_freq_pwr*1e3))
            
            # MV 20.01.r1 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.af.set_title('Freq data (' + str(self.fb_name) + ', Port:' + str(self.port_name) +
                                              ', Dir:' + str(self.direction) + ', Pol:' + str(pol) + ')')
            
            # MV 20.01.r3 5-Jun-20
            self.af.title.set_color(cfg_opt.optical_freq_labels_axes_color)
            
            self.af.set_aspect('auto')
            self.af.format_coord = self.format_coord_freq
            
            # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks        
            self.af.xaxis.label.set_color(cfg_opt.optical_freq_labels_axes_color)
            self.af.yaxis.label.set_color(cfg_opt.optical_freq_labels_axes_color)
            self.af.tick_params(axis='both', which ='both', 
                                colors=cfg_opt.optical_freq_labels_axes_color)
    
            # Plot settings (grid and legend)-------------------------------------------------
            # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to 
            # provide ability to manage look and feel of plots) 
            # Display major grid (if checked)
            if self.checkBoxMajorGridFreq.checkState() == 2:
                self.af.grid(True)  
                self.af.grid(which='major', 
                             linestyle = cfg_opt.optical_freq_maj_grid_linestyle, 
                             linewidth = cfg_opt.optical_freq_maj_grid_linewidth, 
                             color = cfg_opt.optical_freq_maj_grid_color)
            # Display minor grid (if checked)
            if self.checkBoxMinorGridFreq.checkState() == 2:
                self.af.minorticks_on()
                self.af.grid(which='minor', 
                             linestyle = cfg_opt.optical_freq_min_grid_linestyle, 
                             linewidth = cfg_opt.optical_freq_min_grid_linewidth, 
                             color = cfg_opt.optical_freq_min_grid_color)
            # Display legend (if checked)    
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
        except:
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
            msg.setWindowTitle("Plotting error (Optical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
                    
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
    
    # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to provide ability to
    # manage look and feel of plots)          
    def set_signal_plot_freq_domain(self, signal):
        self.af.plot(self.freq_plot, signal, 
                     color = cfg_opt.optical_freq_signal_color, 
                     linestyle = cfg_opt.optical_freq_signal_linestyle, 
                     linewidth = cfg_opt.optical_freq_signal_linewidth, 
                     marker = cfg_opt.optical_freq_signal_marker, 
                     markersize = cfg_opt.optical_freq_signal_markersize,
                     label = 'Optical signal') 
        
    def set_noise_plot_freq_domain(self, signal):
        self.af.plot(self.freq_plot, signal, 
                     color = cfg_opt.optical_freq_noise_color, 
                     linestyle = cfg_opt.optical_freq_noise_linestyle, 
                     linewidth = cfg_opt.optical_freq_noise_linewidth, 
                     marker = cfg_opt.optical_freq_noise_marker, 
                     markersize = cfg_opt.optical_freq_noise_markersize,
                     label = 'Optical noise')   
        
    def set_signal_and_noise_plot_freq_domain(self, signal):
        self.af.plot(self.freq_plot, signal, 
                     color = cfg_opt.optical_freq_sig_noise_color, 
                     linestyle = cfg_opt.optical_freq_sig_noise_linestyle, 
                     linewidth = cfg_opt.optical_freq_sig_noise_linewidth, 
                     marker = cfg_opt.optical_freq_sig_noise_marker, 
                     markersize = cfg_opt.optical_freq_sig_noise_markersize,
                     label = 'Optical signal + noise')
        
    def set_psd_noise_plot_freq_domain(self, signal):
        self.af.plot(self.freq_points, signal, 
                     color = cfg_opt.optical_freq_psd_noise_color, 
                     linestyle = cfg_opt.optical_freq_psd_noise_linestyle, 
                     linewidth = cfg_opt.optical_freq_psd_noise_linewidth, 
                     marker = cfg_opt.optical_freq_psd_noise_marker, 
                     markersize = cfg_opt.optical_freq_psd_noise_markersize,
                     label = 'Optical noise groups')
        
    def format_coord_freq(self, x, y):
        return 'Freq=%0.7E, Power=%0.7E' % (x, y)
    
    '''Polarization analysis tab (plotting methods)===================================='''
    def iteration_change_pol(self):
        new_iteration = int(self.spinBoxPol.value())
        lineEdit = self.spinBoxPol.findChildren(QtWidgets.QLineEdit)
        lineEdit[0].deselect()
        config.app.processEvents()
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[5] #MV 20.01.r1 (previously signal_updated[4])
        
        key = str(self.waveKeyListPol.currentText())        
        for k in range(len(optical_list)):
            #MV Rel 20.01.r1 28-Aug-19: Converted key from str to int (dict was always 
            #defaulting to last key)
            if optical_list[k][0] == int(key):
                break
        index_key = k
        
        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.jones_vector = optical_list[index_key][2]
        
        self.tabData.setCurrentWidget(self.tab_polarization) 
        self.plot_poincare_sphere()
        
    def update_poincare_sphere(self):
        self.plot_poincare_sphere()
        
    def plot_poincare_sphere(self):   
        # Ref 1: The Poincaré Sphere, Optipedia
        # https://spie.org/publications/fg05_p10-11_poincare_sphere?SSO=1
        # (accessed 7-Dec-2019)
        # Ref 2: Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical 
        # Communication Systems and Networks, (Artech House, 2013, Norwood, MA, USA). 
        # Kindle Edition. Chapter 10.13 Stokes Vector and Poincare Sphere
        # Ref 3: Zhou, Xiang. Enabling Technologies for High Spectral-efficiency 
        # Coherent Optical Communication Networks (Wiley Series in Microwave and Optical 
        # Engineering) Wiley. Kindle Edition. 
        try:
            self.figure_pol.clf()
            self.p_sph = self.figure_pol.add_subplot(111, projection='3d')
    
            #Stokes parameters
            sig_x = np.full(self.n, 0 + 1j*0, dtype=complex)
            sig_y = np.full(self.n, 0 + 1j*0, dtype=complex)
            if self.dual_pol_data:
                sig_x = self.signal[0]
                sig_y = self.signal[1]
            else:
                sig_x = self.jones_vector[0]*self.signal
                sig_y = self.jones_vector[1]*self.signal
            sig_x_pwr = np.abs(sig_x)*np.abs(sig_x)
            sig_y_pwr = np.abs(sig_y)*np.abs(sig_y)
            # Stokes Vector (Ref 3, Eq 6.4)
            # P0 = Ex^2 + Ey^2 overall intensity
            # P1 = Ex^2 - Ey^2 intensity difference
            # P2 = 2*Ex*Ey*cos(phi) (P_pi/4 - P_-pi/4)
            # P3 = 2*Ex*Ey*sin(phi) (P_RHC - P_LNC)
            P0 = sig_x_pwr + sig_y_pwr
            P1 = sig_x_pwr - sig_y_pwr 
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
            self.p_sph.plot_surface(x, y, z, rstride=4, cstride=3, alpha = 0.4, linewidth = 1.0,
                               color='#e0e0e0')
            if P0.all() > 0:
                self.p_sph.scatter(S1_avg, S2_avg, S3_avg, color = 'blue', marker = 'o')
                x = [0, S1_avg]
                y = [0, S2_avg]
                z = [0, S3_avg]
                '''self.p_sph.scatter(S1, S2, S3, color = 'blue', marker = 'o')
                x = [0, S1]
                y = [0, S2]
                z = [0, S3]'''          
                self.p_sph.plot(x, y, z, color = 'blue')
            
            # Plot S1, S2, S3 axes   
            self.p_sph.plot([0, 1.5], [0, 0], [0, 0], color = 'black', linestyle=':')
            self.p_sph.plot([0, 0], [0, 1.5], [0, 0], color = 'black', linestyle=':')
            self.p_sph.plot([0, 0], [0, 0], [0, 1.5], color = 'black', linestyle=':')        
            self.p_sph.set_xlabel('S1') 
            self.p_sph.set_ylabel('S2')
            self.p_sph.set_zlabel('S3')
            self.p_sph.text(0, 0, 1.6, 'S3', color = 'black')
            self.p_sph.text(0, 1.6, 0, 'S2', color = 'black') #MV 20.01.r1 7-Dec-2019 Corrected: Changed from S1 to S2
            self.p_sph.text(1.6, 0, 0, 'S1', color = 'black') #MV 20.01.r1 7-Dec-2019 Corrected: Changed from S2 to S1
                 
            # MV 20.01.r1 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.p_sph.set_title('Poincare sphere (' + str(self.fb_name) + ', Port:' 
                                                   + str(self.port_name) + ', Dir:' 
                                                   + str(self.direction) + ')')
            
            self.p_sph.xaxis.pane.fill = False
            self.p_sph.yaxis.pane.fill = False
            self.p_sph.zaxis.pane.fill = False
            self.p_sph.xaxis.pane.set_edgecolor('w')
            self.p_sph.yaxis.pane.set_edgecolor('w')
            self.p_sph.zaxis.pane.set_edgecolor('w')
            #Elevation and azimuth settings (camera view)
            self.elev = 10
            self.az = 25
            if self.azimuthPos.text() and self.elevationPos.text():
                self.elev = self.elevationPos.text()
                self.az = self.azimuthPos.text()
            self.p_sph.view_init(elev=float(self.elev), azim=float(self.az))
            self.elevationPosCurrent.setText(str(format(float(self.elev), '0.1f')))
            self.azimuthPosCurrent.setText(str(format(float(self.az), '0.1f')))
            self.canvas_pol.draw()
    
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error plotting Poincare sphere')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Optical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
        
    def onclick(self, event):
        azim = self.p_sph.azim
        elev = self.p_sph.elev
        self.elevationPosCurrent.setText(str(format(elev, '0.1f')))
        self.azimuthPosCurrent.setText(str(format(azim, '0.1f')))
    
    '''Signal data tab================================================================='''
    def iteration_change_signal_data(self):
        new_iteration = int(self.spinBoxSignalData.value())
        lineEdit = self.spinBoxSignalData.findChildren(QtWidgets.QLineEdit)
        lineEdit[0].deselect()
        config.app.processEvents()
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[5] #MV 20.01.r1 (previously signal_updated[4])
        
        key = str(self.waveKeyListSignalData.currentText())        
        for k in range(len(optical_list)):
            #MV Rel 20.01.r1 28-Aug-19: Converted key from str to int (dict was always 
            #defaulting to last key)
            if optical_list[k][0] == int(key):
                break
        index_key = k
        
        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.noise = optical_list[index_key][4]
        self.jones_vector = optical_list[index_key][2]
        self.channel_freq = optical_list[index_key][1]    
        self.frq = self.update_freq_array(self.n, self.channel_freq) 
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
            sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, self.signal, self.noise, 
                                                                  self.jones_vector) 
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
                    # MV 20.01.r3 18-Sep-20 Divide by n added (FFT normalization is set to None)
                    data1['y'] = self.Y[self.start_index-1:self.end_index-1]/self.n
                else:
                    self.signalBrowser.append('Signal data (index, freq(Hz), e_field(mag), e-field(ph)):')
                    # MV 20.01.r3 18-Sep-20 Divide by n added (FFT normalization is set to None)
                    data1['y1'] = np.abs(self.Y[self.start_index-1:self.end_index-1])/self.n
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
                    # MV 20.01.r3 18-Sep-20 Divide by n added (FFT normalization is set to None)
                    data1['y'] = self.N[self.start_index-1:self.end_index-1]/self.n
                else:
                    self.signalBrowser.append('Noise data (index, freq(Hz), e_field(mag), e-field(ph)):')
                    # MV 20.01.r3 18-Sep-20 Divide by n added (FFT normalization is set to None)
                    data1['y1'] = np.abs(self.N[self.start_index-1:self.end_index-1])/self.n
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
            cursor.setPosition(0)
            self.signalBrowser.setTextCursor(cursor) 
        except:
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
            msg.setWindowTitle("Plotting error (Optical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
        
    '''Signal metrics tab=================================================================
    '''
    def iteration_change_signal_metrics(self):
        new_iteration = int(self.spinBoxSignalMetrics.value())
        lineEdit = self.spinBoxSignalMetrics.findChildren(QtWidgets.QLineEdit)
        lineEdit[0].deselect()
        config.app.processEvents()
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[5] #MV 20.01.r1 (previously signal_updated[4])
        
        key = str(self.waveKeyListSignalMetrics.currentText())        
        for k in range(len(optical_list)):
            #MV Rel 20.01.r1 28-Aug-19: Converted key from str to int (dict was always 
            #defaulting to last key)
            if optical_list[k][0] == int(key):
                break
        index_key = k
        
        self.signal = optical_list[index_key][3] #Electrical amplitudes
        self.noise = optical_list[index_key][4]
        self.jones_vector = optical_list[index_key][2]
        self.channel_freq = optical_list[index_key][1]
        self.update_signal_metrics()       
        
    def update_signal_metrics(self):
        try:
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
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error displaying signal metrics')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Optical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
            
    '''All channels tab plotting methods (new feature 20.01.r1)===========================
    '''   
    def iteration_change_all_ch(self):
        new_iteration = int(self.spinBoxAllCh.value())
        lineEdit = self.spinBoxAllCh.findChildren(QtWidgets.QLineEdit)
        lineEdit[0].deselect()
        config.app.processEvents()
        signal_updated = self.signals[new_iteration]
        optical_list = signal_updated[5] #MV 20.01.r1 (previously signal_updated[4])
        # Find min and max optical carrier frequencies & build extended freq axis  
        
        # MV 20.01.r3 17-Jun-20 Clean up of min/max frequency calculations
        frequencies = []
        for k in range(0, len(optical_list)):
            frequencies.append(optical_list[k][1])
        freq_min = min(frequencies)
        freq_max = max(frequencies)
              
        '''freq_min = optical_list[0][1]
        freq_max = optical_list[0][1]
        freq_sum = 0
        for k in range(1, len(optical_list)):
            freq = optical_list[k][1]
            freq_sum += freq
            if freq_max < freq:
                freq_max = freq
            if freq_min > freq: 
                freq_min = freq'''
        
        # Calculate center frequency of channel list
        freq_sum = 0       
        if freq_sum > 1:
            freq_ctr = freq_sum/(len(optical_list)-1)
        else:
            freq_ctr = freq_min
        self.opticalCtrFreq.setText(str(format(freq_ctr, '0.5E')))
        self.numberOptChannelsAllCh.setText(str(format(len(optical_list), 'n')))
        
        # Build consolidated freq axis      
        self.freq_x_axis = np.arange( freq_min - (self.fs/2), freq_max + (self.fs/2), 
                                int(np.round((self.fs/self.n))) )
        
        self.freq_axis_size = np.size(self.freq_x_axis)
        
        # Prepare signal arrays for frequency noise groups
        # self.noise_freq = optical_list[0][5] #MV 20.01.r1
        self.noise_freq = signal_updated[4] #MV 20.01.r1
        self.ng_w = self.noise_freq[0, 1] - self.noise_freq[0, 0]
        self.noise_freq_psd = self.noise_freq[1, :]
        self.noise_freq_pwr = self.noise_freq[1, :] * self.ng_w
        self.freq_points = self.noise_freq[0, :]
        
        if (self.radioButtonPolXAllCh.isChecked() == 1 or 
        self.radioButtonPolYAllCh.isChecked() == 1):
            self.noise_freq_psd = 0.5*self.noise_freq_psd
            self.noise_freq_pwr = 0.5*self.noise_freq_pwr
        
        # Initialize
        if (self.signalCheckBoxAllCh.checkState() == 2 or 
            self.noiseCheckBoxAllCh.checkState() == 2 or
            self.sigandnoiseCheckBoxAllCh.checkState() == 2):
            self.all_ch_field_env_fft = np.full(self.freq_axis_size, 0 + 1j*0, dtype=complex) 
            self.all_ch_noise_env_fft = self.all_ch_field_env_fft.copy()
            self.all_ch_field_noise_env_fft = self.all_ch_field_env_fft.copy()
            
            pol = 'X-Y'
            if self.radioButtonPolXAllCh.isChecked() == 1:
                pol = 'X'
            if self.radioButtonPolYAllCh.isChecked() == 1:
                pol = 'Y'  
        
            # Iterate through all optical channels
            for k in range(len(optical_list)):       
                channel_freq = optical_list[k][1]
                frq = self.update_freq_array(self.n, channel_freq)
                current_jones_vector = optical_list[k][2]            
                current_signal_field = optical_list[k][3]
                current_noise_field = optical_list[k][4]
                
                sig, noise, sig_pwr, noise_pwr = self.set_signal_data(pol, current_signal_field,
                                                current_noise_field, current_jones_vector)   
                
                # Calculate fft for signal
                self.Y = np.fft.fft(sig)
                self.Y = np.fft.fftshift(self.Y)
                
                # Calculate fft for noise
                self.N = np.fft.fft(noise)
                self.N = np.fft.fftshift(self.N)
                
                # Calculate fft for signal + noise
                self.Y_N = np.fft.fft(sig + noise)
                self.Y_N = np.fft.fftshift(self.Y_N)  
            
                # Map field envelopes to extended frequency axis
                # MV 20.01.r3 17-Jun-20 Cleaned up code for field envelope
                # mapping
                j = np.max(np.where(self.freq_x_axis <= frq[0]))
                
                '''j = 0
                while True:
                    if self.freq_x_axis[j] == self.freq_x_axis[-1]: #Last element of array
                        break
                    if (frq[0] >= self.freq_x_axis[j] and frq[0] < self.freq_x_axis[j+1]):
                        break
                    else:
                        j += 1'''
            
                self.all_ch_field_env_fft[j:j+self.n] += self.Y[0:self.n]
                self.all_ch_noise_env_fft[j:j+self.n] += self.N[0:self.n]
                self.all_ch_field_noise_env_fft[j:j+self.n] += self.Y_N[0:self.n]
                
        self.plot_all_channels(0)
        self.canvas_all_ch.draw()

    def check_signal_changed_all_ch(self):
        self.tabData.setCurrentWidget(self.tab_channels) 
        self.iteration_change_all_ch()
        self.plot_all_channels(0)
        self.canvas_all_ch.draw()
        
    def update_axis_all_ch(self):
        self.plot_all_channels(1)
        self.canvas_all_ch.draw()
        
    def plot_all_channels(self, axis_adjust): 
        try:
            pol = 'X-Y'
            if self.radioButtonPolXAllCh.isChecked() == 1:
                pol = 'X'
            if self.radioButtonPolYAllCh.isChecked() == 1:
                pol = 'Y'        
                    
            self.figure_all_ch.clf()
            # MV 20.01.r1 Added new feature to select plot area background color
            back_color = cfg_opt.opt_chnls_freq_plot_back_color # MV 20.01.r3 (5-Jun-20)
            self.a_ch = self.figure_all_ch.add_subplot(111, facecolor = back_color)
                                                                                          
            #http://greg-ashton.physics.monash.edu/setting-nice-axes-labels-in-matplotlib.html
            self.a_ch.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
            self.a_ch.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
            
            if axis_adjust == 1:
                if self.minFreqAllCh.text() and self.maxFreqAllCh.text():
                    start_freq = self.minFreqAllCh.text()
                    end_freq = self.maxFreqAllCh.text()
                    self.a_ch.set_xlim(float(start_freq), float(end_freq))
                if self.startYAxisAllCh.text() and self.endYAxisAllCh.text():
                    start_val = self.startYAxisAllCh.text()
                    end_val = self.endYAxisAllCh.text()
                    self.a_ch.set_ylim(float(start_val), float(end_val))   
                
            if self.signalCheckBoxAllCh.checkState() == 2:
                # MV 20.01.r3 18-Sep-20 Bug fix:
                # np.abs(self.Y)*np.abs(self.Y) is now divided by n^2, 
                # previously was incorrectly dividing by n
                # Same applies for noise and sig+noise
                self.optical_power_fft = (abs(self.all_ch_field_env_fft)
                                          *abs(self.all_ch_field_env_fft)/(self.n*self.n))  
            
            if self.noiseCheckBoxAllCh.checkState() == 2:
                self.optical_noise_fft = (abs(self.all_ch_noise_env_fft)
                                          *abs(self.all_ch_noise_env_fft)/(self.n*self.n))
            
            if self.sigandnoiseCheckBoxAllCh.checkState() == 2:
                self.optical_signal_and_noise_fft = (abs(self.all_ch_field_noise_env_fft)
                                              *abs(self.all_ch_field_noise_env_fft)/(self.n*self.n))
            
            #Update spectral resolution for plot (if selected)
            if self.signalCheckBoxEnableResolutionAllCh.checkState() == 2:
                optical_power_fft_avg = np.zeros(self.freq_axis_size)
                optical_noise_fft_avg = np.zeros(self.freq_axis_size)
                optical_signal_and_noise_fft_avg = np.zeros(self.freq_axis_size)
                
                if self.spectralResolutionAllCh.text():
                    window = float(self.spectralResolutionAllCh.text())
                else:
                    window = self.fs
                
                x = int(round(window/self.fs))
                if x > 1:
                    for i in range(0,np.size(self.freq_x_axis)-1):
                        for a in range(-x,x):
                            if (i+a < 0) or (i+a > np.size(self.freq_x_axis)-1): 
                                pass
                            else:
                                if self.signalCheckBoxAllCh.checkState() == 2:
                                    optical_power_fft_avg[i] += self.optical_power_fft[i+a]
                                if self.noiseCheckBoxAllCh.checkState() == 2:
                                    optical_noise_fft_avg[i] += self.optical_noise_fft[i+a]
                                if self.sigandnoiseCheckBoxAllCh.checkState() == 2:
                                    optical_signal_and_noise_fft_avg[i] += self.optical_signal_and_noise_fft[i+a]
                    self.optical_power_fft = optical_power_fft_avg
                    self.optical_noise_fft = optical_noise_fft_avg
                    self.optical_signal_and_noise_fft = optical_signal_and_noise_fft_avg
            
            if self.radioButtonLinearAllCh.isChecked() == 1:
                self.a_ch.set_ylabel('Power (W)')
            elif self.radioButtonLinearSpectralAllCh.isChecked() == 1:
                self.a_ch.set_ylabel('Power (W/Hz)')
            elif self.radioButtonLogSpectralAllCh.isChecked() == 1:
                self.a_ch.set_ylabel('Power (dBm/Hz)')    
            else:
                self.a_ch.set_ylabel('Power (dBm)')
               
            if self.radioButtonNmAllCh.isChecked() == 1:
                self.freq_plot = (constants.c/self.freq_x_axis)*1e9
                self.a_ch.set_xlabel('Freq (nm)')
            else:
                self.freq_plot = self.freq_x_axis
                self.a_ch.set_xlabel('Freq (Hz)')
                
            if self.signalCheckBoxAllCh.checkState() == 2:
                self.optical_power_fft = self.adjust_units_for_plotting(self.optical_power_fft)
                self.set_signal_plot_all_ch(self.optical_power_fft)
    
            if self.noiseCheckBoxAllCh.checkState() == 2:
                self.optical_noise_fft = self.adjust_units_for_plotting(self.optical_noise_fft)
                self.set_noise_plot_all_ch(self.optical_noise_fft)
                    
            if self.sigandnoiseCheckBoxAllCh.checkState() == 2:
                self.optical_signal_and_noise_fft = self.adjust_units_for_plotting(self.optical_signal_and_noise_fft)
                self.set_signal_and_noise_plot_all_ch(self.optical_signal_and_noise_fft)             
                    
            if self.noisegroupCheckBoxAllCh.checkState() == 2:
                if self.radioButtonLinearAllCh.isChecked() == 1:
                    self.set_psd_noise_plot_all_ch(self.noise_freq_pwr)
                elif self.radioButtonLinearSpectralAllCh.isChecked() == 1:
                    self.set_psd_noise_plot_all_ch(self.noise_freq_psd)
                elif self.radioButtonLogSpectralAllCh.isChecked() == 1:
                    self.set_psd_noise_plot_all_ch(10*np.log10(self.noise_freq_psd*1e3))
                else:
                    self.set_psd_noise_plot_all_ch(10*np.log10(self.noise_freq_pwr*1e3))
            
            # MV 20.01.r1 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.a_ch.set_title('Freq data - all ch (' + str(self.fb_name) + ', Port:' 
                                                     + str(self.port_name) + ', Dir:'
                                                     + str(self.direction) + ', Pol:' 
                                                     + str(pol) + ')')
            
            # MV 20.01.r3 5-Jun-20
            self.a_ch.title.set_color(cfg_opt.opt_chnls_freq_labels_axes_color)
            
            self.a_ch.set_aspect('auto')
            self.a_ch.format_coord = self.format_coord_all_ch
            
            # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks        
            self.a_ch.xaxis.label.set_color(cfg_opt.opt_chnls_freq_labels_axes_color)
            self.a_ch.yaxis.label.set_color(cfg_opt.opt_chnls_freq_labels_axes_color)
            self.a_ch.tick_params(axis='both', which ='both', 
                                colors=cfg_opt.opt_chnls_freq_labels_axes_color)
            
            # Plot settings (grid and legend)
            # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to 
            # provide ability to manage look and feel of plots)  
            if self.checkBoxMajorGridAllCh.checkState() == 2:
                self.a_ch.grid(True)
                self.a_ch.grid(which='major', 
                               linestyle = cfg_opt.opt_chnls_freq_maj_grid_linestyle, 
                               linewidth = cfg_opt.opt_chnls_freq_maj_grid_linewidth, 
                               color = cfg_opt.opt_chnls_freq_maj_grid_color)
           
            if self.checkBoxMinorGridAllCh.checkState() == 2:
                self.a_ch.minorticks_on()
                self.a_ch.grid(which='minor', 
                               linestyle = cfg_opt.opt_chnls_freq_min_grid_linestyle, 
                               linewidth = cfg_opt.opt_chnls_freq_min_grid_linewidth, 
                               color = cfg_opt.opt_chnls_freq_min_grid_color)
                
            if self.checkBoxLegendAllCh.isChecked() == 1:
                self.a_ch.legend()
        
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error plotting multi-channel view')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Optical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
            
    def adjust_units_for_plotting(self, signal):
        if self.radioButtonLinearAllCh.isChecked() == 1:
            pass
        elif self.radioButtonLinearSpectralAllCh.isChecked() == 1:
            signal = signal/self.fs
        elif self.radioButtonLogSpectralAllCh.isChecked() == 1:
            if np.count_nonzero(signal) == np.size(signal):
                signal = 10*np.log10(signal*1e3/self.fs)                 
            else:
                signal += 1e-30 #Set zero elements to very low value
                signal = 10*np.log10(signal*1e3/self.fs)  
        else:
            if np.count_nonzero(signal) == np.size(signal):
                signal = 10*np.log10(signal*1e3)
            else:
                signal += 1e-30#Set zero elements to very low value
                signal = 10*np.log10(signal*1e3)  
        return signal
    
    # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to 
    # provide ability to manage look and feel of plots)  
    def set_signal_plot_all_ch(self, signal):
        self.a_ch.plot(self.freq_plot, signal, 
                       color = cfg_opt.opt_chnls_freq_signal_color,
                       linestyle = cfg_opt.opt_chnls_freq_signal_linestyle, 
                       linewidth = cfg_opt.opt_chnls_freq_signal_linewidth, 
                       marker = cfg_opt.opt_chnls_freq_signal_marker, 
                       markersize = cfg_opt.opt_chnls_freq_signal_markersize,
                       label='Optical signal') 
        
    def set_noise_plot_all_ch(self, signal):
        self.a_ch.plot(self.freq_plot, signal, 
                       color = cfg_opt.opt_chnls_freq_noise_color, 
                       linestyle = cfg_opt.opt_chnls_freq_noise_linestyle, 
                       linewidth = cfg_opt.opt_chnls_freq_noise_linewidth, 
                       marker = cfg_opt.opt_chnls_freq_noise_marker, 
                       markersize = cfg_opt.opt_chnls_freq_noise_markersize,
                       label='Optical noise')   
        
    def set_signal_and_noise_plot_all_ch(self, signal):
        self.a_ch.plot(self.freq_plot, signal, 
                       color = cfg_opt.opt_chnls_freq_sig_noise_color,
                       linestyle = cfg_opt.opt_chnls_freq_sig_noise_linestyle, 
                       linewidth = cfg_opt.opt_chnls_freq_sig_noise_linewidth, 
                       marker = cfg_opt.opt_chnls_freq_sig_noise_marker, 
                       markersize = cfg_opt.opt_chnls_freq_sig_noise_markersize,
                       label='Optical signal + noise')
        
    def set_psd_noise_plot_all_ch(self, signal):
        self.a_ch.plot(self.freq_points, signal,
                       color = cfg_opt.opt_chnls_freq_psd_noise_color, 
                       linestyle = cfg_opt.opt_chnls_freq_psd_noise_linestyle, 
                       linewidth= cfg_opt.opt_chnls_freq_psd_noise_linewidth, 
                       marker = cfg_opt.opt_chnls_freq_psd_noise_marker, 
                       markersize = cfg_opt.opt_chnls_freq_psd_noise_markersize,
                       label='Optical noise groups')
        
    def format_coord_all_ch(self, x, y):
        return 'Freq=%0.7E, Power=%0.7E' % (x, y)
 
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_freq)
        plt.close(self.figure_pol)
        plt.close(self.figure_all_ch)
                       
'''FUNCTIONS================================================================'''
#def set_mpl_cursor():
#    mplcursors.cursor(multiple=False).connect("add", 
#                     lambda sel: sel.annotation.get_bbox_patch().set(fc="lightyellow", alpha=1))
    
def set_icon_window():
    icon_path = os.path.join(config.root_path, 'syslab_gui_icons', 'SysLabIcon128.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
'''========================================================================='''
