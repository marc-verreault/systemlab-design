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
# Import config_port_viewers as cfg_elec
import importlib
cfg_port_viewers_path = str('syslab_config_files.config_port_viewers')
cfg_elec = importlib.import_module(cfg_port_viewers_path)
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

qtElectricalPortDataViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files',
                                              'ElectricalDataViewer.ui')
qtElectricalPortDataViewerFile = os.path.normpath(qtElectricalPortDataViewerFile)
Ui_PortDataWindow_Electrical, QtBaseClass = uic.loadUiType(qtElectricalPortDataViewerFile)

#import matplotlib
matplotlib.rcParams['figure.dpi'] = 80

# https://matplotlib.org/api/ticker_api.html#matplotlib.ticker.Formatter
matplotlib.rcParams['axes.formatter.useoffset'] = False # Removes offset from all plots
matplotlib.rcParams['axes.formatter.limits'] = [-4, 4] # Limits for exponential notation

# MV 20.01.r3 15-Jun-20
style_spin_box = """QSpinBox {color: darkBlue; background: white;
                              selection-color: darkBlue;
                              selection-background-color: white;}"""

style_combo_box = """QComboBox {color: darkBlue; background: white;
                              selection-color: darkBlue;
                              selection-background-color: white;}"""

class ElectricalPortDataAnalyzer(QtWidgets.QDialog, Ui_PortDataWindow_Electrical):
    '''
    Electrical signal format:
    portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4),
    amplitude_array(5), noise_array(6)    
    '''
    def __init__(self, signal_data, fb_name, port_name, direction, design_settings):
        QtWidgets.QDialog.__init__(self)
        Ui_PortDataWindow_Electrical.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)       
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        self.setStyleSheet(cfg_special.global_font) # MV 20.01.r1 17-Dec-2019
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.fb_name = fb_name
        self.port_name = port_name
        self.direction = direction
        #self.iteration = 1  
        self.signals = signal_data

        # MV 20.01.r3 15-Jun-20 Set iteration to reflect main application setting
        # (iterators spin box)
        current_iter = int(design_settings['current_iteration'])
        if (current_iter - 1) <= len(self.signals):
            self.iteration = current_iter
        else:
            self.iteration = int(len(self.signals))
        
        # MV 20.01.r3 13-Jun-20 Added functional block and port data info to
        # Window title box
        self.setWindowTitle('Electrical signal data analyzer (' + 
                            str(self.fb_name) + ', Port: ' + 
                            str(self.port_name) + ', Dir: ' + 
                            str(self.direction) + ')')
        
        # MV 20.01.r3 19-Jun-20: Reload config files
        importlib.reload(cfg_elec)
        importlib.reload(cfg_special)
        
        '''Time data tab (dataFrame)==================================================='''
        # TOP LEVEL SETTINGS--------------------------------------------------------------
        # MV 20.01.r2 27-Feb-20 IMPORTANT UPDATE
        # Core settings for port viewer are now derived from received signal statistics
        # (previously was using design settings). Due to signal processing functions such 
        # as re-sampling, local settings for a functional block may be different from
        # project settings
        
        # Time-window must be same for all functional blocks (taken from design settings)
        self.time_win = design_settings['time_window']
        # Calculate number of samples from port signal (will usually be same as design settings)
        self.samples = len(self.signals[self.iteration][4])
        # Calculate sampling frequency (for signal)
        self.fs = self.samples/self.time_win
        # Calculate sampling period (for signal)       
        self.s_period = 1/self.fs
        
        # Previous settings
        #self.samples = design_settings['num_samples']
        #self.fs = design_settings['sampling_rate']
        #self.s_period = design_settings['sampling_period']
        
        # Main settings for viewer (time-domain)
        self.totalSamplesTime.setText(str(format(self.samples, '0.3E')))
        self.samplingPeriod.setText(str(format(self.s_period, '0.3E')))
        self.timeWindow.setText(str(format(self.time_win, '0.3E')))
        #---------------------------------------------------------------------------------
        
        #Iterations group box (Time data tab)
        iterations = len(self.signals) # MV 20.01.r1 20-Jan-20
        self.spinBoxTime.setMaximum(iterations)
        self.spinBoxTime.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxTime.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsTime.setText(str(iterations))        
        self.spinBoxTime.valueChanged.connect(self.value_change_time)       
        #Signal type group box (Time data)
        self.signalCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.noiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.sigandnoiseCheckBox.stateChanged.connect(self.check_signal_changed_time)
        self.radioButtonMag.toggled.connect(self.check_signal_changed_time)        
        self.radioButtonLinearPwr.toggled.connect(self.check_signal_changed_time)
        self.radioButtonLogPwr.toggled.connect(self.check_signal_changed_time)
        #MV 20.01.r1 25-Nov-2019 (Sampling period overlay)
        # MV 20.01.r2 24-Feb-20 (changed to action box)
        self.actionSamplingPeriod.clicked.connect(self.check_signal_changed_time)   
        #Plot settings (Time data)
        self.checkBoxMajorGrid.stateChanged.connect(self.check_signal_changed_time)
        self.checkBoxMinorGrid.stateChanged.connect(self.check_signal_changed_time)
        self.checkBoxLegend.stateChanged.connect(self.check_signal_changed_time) 
        #Y-axis axis settings group box (Time data) 
        self.actionTimeWindowYAxis.clicked.connect(self.update_time_axis) 
        #Time axis settings group box (Time data)
        self.actionTimeWindow.clicked.connect(self.update_time_axis)
        # MV 20.01.r2 24-Feb-20
        self.samples_sym = design_settings['samples_per_sym']
    
        '''Freq data tab (dataFrameFreq)==============================================='''
        #Top level settings (Main sub-tab)  
        self.totalSamplesFreq.setText(str(format(design_settings['num_samples'], '0.3E'))) 
        #self.fs = design_settings['sampling_rate']
        self.samplingRate.setText(str(format(self.fs, '0.3E')))
        #Iterations group box (Main sub-tab)        
        self.spinBoxFreq.setMaximum(iterations)
        self.spinBoxFreq.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxFreq.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsFreq.setText(str(iterations))
        self.spinBoxFreq.valueChanged.connect(self.value_change_freq) 
        #Signal type group box (Main sub-tab) 
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
        
        '''Eye diagram tab (dataFrameEye)=============================================='''
        #Top level settings
        self.totalSamplesEye.setText(str(format(self.samples, '0.3E')))
        self.samplingPeriodEye.setText(str(format(self.s_period, '0.3E')))
        self.timeWindowEye.setText(str(format(self.time_win, '0.3E')))
        self.sym_period = 1/design_settings['symbol_rate']
        self.symbolPeriodEye.setText(str(format(self.sym_period, '0.3E')))
        #Iterations group box (Eye diagram)
        iterations = len(self.signals) # MV 20.01.r1 20-Jan-20   
        self.spinBoxEye.setMaximum(iterations)
        self.spinBoxEye.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxEye.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxEye.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxEye.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsEye.setText(str(iterations))        
        self.spinBoxEye.valueChanged.connect(self.value_change_eye)       
        #Signal type group box (Eye diagram)
        self.signalCheckBoxEye.stateChanged.connect(self.check_signal_changed_eye)
        self.sigandnoiseCheckBoxEye.stateChanged.connect(self.check_signal_changed_eye)
        self.radioButtonMagEye.toggled.connect(self.check_signal_changed_eye)        
        self.radioButtonLinearPwrEye.toggled.connect(self.check_signal_changed_eye)
        self.radioButtonLogPwrEye.toggled.connect(self.check_signal_changed_eye)    
        #Plot settings (Eye diagram)
        self.checkBoxMajorGridEye.stateChanged.connect(self.check_signal_changed_eye)
        self.checkBoxMinorGridEye.stateChanged.connect(self.check_signal_changed_eye)
        #Window settings group box (Eye diagram)
        self.windowEye.setText(str(format(3, 'n')))
        self.actionEyeWindow.clicked.connect(self.check_signal_changed_eye)
        self.checkBoxHistBoxes.stateChanged.connect(self.check_signal_changed_eye)
        # Window settings group box (Eye metrics) MV 20.01.r3 18-Jun-20
        try:
            if cfg_special.oma_reference: # Value is not None
                val = cfg_special.oma_reference
                self.omaRef.setText(str(format(val, '0.3E')))
            if cfg_special.decision_point_ui:
                val = cfg_special.decision_point_ui
                self.decisionPoint.setText(str(format(val, '0.2f')))
            else:
                self.decisionPoint.setText(str(format(0.5, '0.2f')))        
            if cfg_special.histogram_width: # Value is not None
                val = cfg_special.histogram_width
                self.histWidth.setText(str(format(val, '0.2f')))
            else:
                self.histWidth.setText(str(format(20, '0.2f')))
            if cfg_special.histogram_coverage: # Value is not None   
                val = cfg_special.histogram_coverage
                self.histCoverage.setText(str(format(val, '0.2f')))
            else:
                self.histCoverage.setText(str(format(99.9, '0.2f')))
        except:
            self.decisionPoint.setText(str(format(0.5, '0.2f')))
            self.histWidth.setText(str(format(20, '0.2f')))
            self.histCoverage.setText(str(format(99.9, '0.2f')))
        self.calculateEyeMetrics.clicked.connect(self.check_signal_changed_eye)
        
        # SETUP TOOL TIP FOR EYE DIAGRAM METRICS
        # Stressed Eye: “Know What You’re Really Testing With”, Primer
        # Tektronix White Paper, Tektronix (25 May 2010)
        # Source: https://www.tek.com/document/primer/stressed-eye-
        # know-what-you-re-really-testing        

        table_start = "<table width='250'><tr><td width='250'>"
        text_start = "<tr><td width='250'>"
        #text_end = "</td></tr></table>"
        text_end = "</td></table>"

        # Decision pt (y)
        title = "<b>Threshold (y)</b></td></tr>"
        desc = ("Decision level (y-axis) used for declaring Logic 1 " +
                "or Logic 0. Used to build upper and lower histograms. " +
                "When empty, the mean of the signal will be used.")
        self.label_threshold.setMouseTracking(True)
        self.label_threshold.setToolTip(table_start + title + text_start
                                        + desc + text_end)
        # Decision pt (UI)
        title = "<b>Decision pt (UI)</b></td></tr>"
        desc = ("Time point where threshold decision is made. " +
                "The default setting is 0.5 UI, or mid-point of the time interval of the eye.")
        self.label_decision.setMouseTracking(True)
        self.label_decision.setToolTip(table_start + title + text_start
                                        + desc + text_end)        
        # Hist width (%UI)
        title = "<b>Histogram width (%UI)</b></td></tr>"
        desc = ("Percentage in terms of unit time interval to be used to " +
                "define the width of the lower (L0) and upper (L1) histograms. " +
                "The center of the histogram will be placed at the <b>Decision pt</b>.")
        self.label_hist_width.setMouseTracking(True)
        self.label_hist_width.setToolTip(table_start + title + text_start
                                        + desc + text_end)        
        # Hist coverage
        title = "<b>Histogram coverage (%)</b></td></tr>"
        desc = ("Percentage of histogram data samples to be used to calculate " +
                "the OMA, eye height and VECP. For 99.9% coverage, " +
                "the samples comprising 0.05% of the top and bottom sections of " +
                " each histogram will be removed (clipped).")
        self.label_hist_coverage.setMouseTracking(True)
        self.label_hist_coverage.setToolTip(table_start + title + text_start
                                        + desc + text_end)        
        # OMA ref
        title = "<b>OMA (Ref)</b></td></tr>"
        desc = ("This value (Optical Modulation Amplitude) will be used to " +
                "calculate the VECP. When left blank, the OMA will be calculated " +
                "based on the histogram settings defined above.")
        self.label_oma_ref.setMouseTracking(True)
        self.label_oma_ref.setToolTip(table_start + title + text_start
                                        + desc + text_end)        
        # OMA
        title = "<b>OMA</b></td></tr>"
        desc = ("Calculated value of the OMA (<i>Mean_L1_hist - Mean_L0_hist</i>). " +
                "This value is only calculated when the <b>OMA (Ref)</b> field is empty.")
        self.label_oma.setMouseTracking(True)
        self.label_oma.setToolTip(table_start + title + text_start
                                        + desc + text_end)        
        # Eye height
        title = "<b>Eye height (Ao)</b></td></tr>"
        desc = ("Calculated value of the Eye height. </td></tr>" +
                " <i>(Mean_L1_hist - Width_L1_hist/2) - </td></tr>" +
                "(Mean_L0_hist + Width_L0_hist/2)</i>")
        self.label_eye_height.setMouseTracking(True)
        self.label_eye_height.setToolTip(table_start + title + text_start
                                        + desc + text_end)        
        # VECP
        title = "<b>VECP (dB)</b></td></tr>"
        desc = ("Vertical eye closure penalty. </td></tr>" +
                " <i>VECP = 10 x Log10(OMA/Ao)</i>")
        self.label_vecp.setMouseTracking(True)
        self.label_vecp.setToolTip(table_start + title + text_start
                                        + desc + text_end)
        
        '''Signal data tab (dataFrameSignal)==========================================='''
        #Iterations group box
        iterations = len(self.signals) # MV 20.01.r1 20-Jan-20  
        self.spinBoxSignalData.setMaximum(iterations)
        self.spinBoxSignalData.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalData.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsSignalData.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iteration_change_signal_data)
        #Domain setting group box
        self.radioButtonSigFreq.toggled.connect(self.update_signal_data)
        self.radioButtonSigTime.toggled.connect(self.update_signal_data)
        #E-field signal format group box
        self.radioButtonComplexSignalData.toggled.connect(self.update_signal_data)
        self.radioButtonPolarSignalData.toggled.connect(self.update_signal_data)
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
        iterations = len(self.signals) # MV 20.01.r1 20-Jan-20 
        self.spinBoxSignalMetrics.setMaximum(iterations)
        self.spinBoxSignalMetrics.setValue(self.iteration) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalMetrics.lineEdit().setReadOnly(True) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalMetrics.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # MV 20.01.r3 15-Jun-20
        self.spinBoxSignalMetrics.setStyleSheet(style_spin_box) # MV 20.01.r3 15-Jun-20
        self.totalIterationsSignalMetrics.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iteration_change_signal_metrics)
        
        '''Setup initial data for iteration 1 (default)================================'''
        signal_default = self.signals[self.iteration]    
        self.time = signal_default[4] #Time sampling points
        self.signal = signal_default[5] #Electrical amplitudes
        self.noise = signal_default[6] #Noise samples
        self.carrier = signal_default[2]
        
        # MV 20.01.r3 18-Jun-20: Calculate avg value of signal 
        # & apply to decision threshold
        avg_sig = np.mean(np.real(self.signal))
        try:        
            if cfg_special.decision_threshold: # Is not None
                val = cfg_special.decision_threshold
                self.decisionThreshold.setText(str(format(val, '0.3E')))
            else:
                self.decisionThreshold.setText(str(format(avg_sig, '0.3E')))
        except:
            self.decisionThreshold.setText(str(format(avg_sig, '0.3E')))
        
        '''Setup frequency domain analysis============================================='''
        # REF:  Fast Fourier Transform in matplotlib, 
        # An example of FFT audio analysis in matplotlib and the fft function.
        # Source: https://plot.ly/matplotlib/fft/(accessed 20-Mar-2018)  
        self.n = int(len(self.signal))
        T = self.n/self.fs #
        k = np.arange(self.n)
        self.frq = k/T # Positive/negative freq (double sided)
        self.frq_pos = self.frq[range(int(self.n/2))] # Positive freq only     
        # FFT computations (signal, noise, signal+noise)
        self.Y = np.fft.fft(self.signal)
        self.Y_pos = self.Y[range(int(self.n/2))]
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.Y_pos = self.Y_pos*np.sqrt(2)
        self.Y_pos[0] = self.Y_pos[0]/np.sqrt(2) # DC component is not doubled
        self.N = np.fft.fft(self.noise)
        self.N_pos = self.N[range(int(self.n/2))]
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.N_pos = self.N_pos*np.sqrt(2) 
        self.N_pos[0] = self.N_pos[0]/np.sqrt(2) # DC component is not doubled
        self.Y_N = np.fft.fft(self.signal+self.noise)
        self.Y_N_pos = self.Y_N[range(int(self.n/2))]
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.Y_N_pos = self.Y_N_pos*np.sqrt(2) 
        self.Y_N_pos[0] = self.Y_N_pos[0]/np.sqrt(2) # DC component is not doubled

        '''Setup background colors for frames=========================================='''
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (frame bkrd clr)
        color = QtGui.QColor(cfg_elec.electrical_frame_background_color) 
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
        p5  = self.graphFrameEye.palette() 
        p5.setColor(self.graphFrameEye.backgroundRole(), color)
        self.graphFrameEye.setPalette(p5)          
        p6  = self.dataFrameEye.palette() 
        p6.setColor(self.dataFrameEye.backgroundRole(), color)
        self.dataFrameEye.setPalette(p6) 
        p7  = self.dataFrameSignal.palette() 
        p7.setColor(self.dataFrameSignal.backgroundRole(), color)
        self.dataFrameSignal.setPalette(p7)
        p8  = self.dataFrameMetrics.palette() 
        p8.setColor(self.dataFrameMetrics.backgroundRole(), color)
        self.dataFrameMetrics.setPalette(p8) 
        
        '''Setup matplotlib figures and toolbars======================================='''
        #Time data tab
        self.graphLayout = QtWidgets.QVBoxLayout()
        # MV 20.01.r1 29-Oct-19 Added link to port viewers config file (fig bkrd clr)
        self.figure = plt.figure(facecolor = cfg_elec.electrical_time_fig_back_color)
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self.tab_time)
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)        
        #Freq data tab
        self.graphLayoutFreq = QtWidgets.QVBoxLayout()
        self.figure_freq = plt.figure(facecolor = cfg_elec.electrical_freq_fig_back_color)
        self.canvas_freq = FigureCanvas(self.figure_freq)     
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self.tab_freq)
        self.graphLayoutFreq.addWidget(self.canvas_freq)
        self.graphLayoutFreq.addWidget(self.toolbar_freq) 
        self.graphFrameFreq.setLayout(self.graphLayoutFreq) 
        #Eye diagram tab
        self.graphLayoutEye = QtWidgets.QVBoxLayout()
        self.figure_eye = plt.figure(facecolor = cfg_elec.electrical_eye_fig_back_color)
        self.canvas_eye = FigureCanvas(self.figure_eye)     
        self.toolbar_eye = NavigationToolbar(self.canvas_eye, self.tab_eye)
        self.graphLayoutEye.addWidget(self.canvas_eye)
        self.graphLayoutEye.addWidget(self.toolbar_eye) 
        self.graphFrameEye.setLayout(self.graphLayoutEye)
        
        '''Plot default graphs========================================================='''
        self.tabData.setCurrentWidget(self.tab_freq)
        self.figure_freq.set_tight_layout(True)
        self.plot_freq_domain(0)
        self.canvas_freq.draw()
        self.tabData.setCurrentWidget(self.tab_eye)
        self.figure_eye.set_tight_layout(True)
        self.plot_eye()
        self.canvas_eye.draw()
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
        self.signal = signal_updated[5] #Electrical amplitudes
        self.noise = signal_updated[6]
        self.carrier = signal_updated[3] #MV 20.01.r1 (23-Sep-2019)
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
            back_color = cfg_elec.electrical_time_plot_back_color
            self.ax = self.figure.add_subplot(111, facecolor = back_color)
            self.ax.clear()
            
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
                
            if self.radioButtonMag.isChecked() == 1:
                self.ax.set_ylabel('Magnitude') # MV 20.01.v3 17-Sep-20: Removed V
            elif self.radioButtonLinearPwr.isChecked() == 1:   
                self.ax.set_ylabel('Power (W)')
            else:
                self.ax.set_ylabel('Power (dBm)')
                           
             # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks        
            self.ax.xaxis.label.set_color(cfg_elec.electrical_time_labels_axes_color)
            self.ax.yaxis.label.set_color(cfg_elec.electrical_time_labels_axes_color)
            self.ax.tick_params(axis='both', which ='both', 
                                colors=cfg_elec.electrical_time_labels_axes_color)
            
            #sig = np.real(self.signal)
            #sig = np.abs(self.signal)
            #sig = np.imag(self.signal)
            #noise = np.real(self.noise)
            #sig_noise = np.real(self.signal + self.noise) # MV 20.01.r1 (Bug fix, previously
                                                          # was adding np.real(sig) + 
                                                          # np.real(noise))
                                                          
                                                          
            # Tests MV 20.01.r3 4-Jul-20
            '''sig_sign = np.sign(np.real(self.signal))
            sig_sign = np.sign(np.arctan2(sig_real, sig_imag)) 
            sig = np.abs(self.signal)*sig_sign'''
            
            '''sig_real = np.real(self.signal) 
            sig_imag = np.imag(self.signal) 
            sign = np.sign(np.arctan2(sig_imag, sig_real))          
            sig = np.abs(self.signal)*sign'''                                            
                                                          
            '''noise_real = np.real(self.noise) 
            noise_imag = np.imag(self.noise) 
            sign = np.sign(np.arctan2(noise_real, noise_imag))           
            noise = np.abs(self.noise)*sign'''                                                  
                                                          
    
            #20.01.r1 2 Sep 19 - Updated this section by introducing new functions
            #for plotting=====================================================================
            if self.signalCheckBox.checkState() == 2:
                sig = self.adjust_units_for_plotting_time(self.signal)
                self.set_signal_plot_time_domain(self.time, sig)    
    
            if self.noiseCheckBox.checkState() == 2:
                noise = self.adjust_units_for_plotting_time(self.noise)
                self.set_noise_plot_time_domain(self.time, noise)  
                self.set_noise_plot_time_domain(self.time, noise) 
                
            if self.sigandnoiseCheckBox.checkState() == 2:
                sig_and_noise = self.adjust_units_for_plotting_time(self.signal + self.noise)
                self.set_signal_and_noise_plot_time_domain(self.time, sig_and_noise)  
            #=================================================================================
            
            # MV 20.01.r1 25-Nov-19
            if (self.signalCheckBox.checkState() == 2 and self.samplingPeriodDataField.text() 
            and self.samplingPeriodOffset.text()):
                samplePeriod = float(self.samplingPeriodDataField.text())
                sample_spacing = int(np.round(self.fs*samplePeriod))
                time_offset = float(self.samplingPeriodOffset.text())
                start_index = int(np.round(time_offset*self.fs))
                if start_index < 0:
                    start_index = 0
                time_samples = self.time[start_index::sample_spacing]
                n_samples = len(time_samples)
                sampled_signal = np.zeros(n_samples)            
                sampled_signal = sig[start_index::sample_spacing]
            
                self.ax.plot(time_samples, sampled_signal, 
                         color = cfg_elec.electrical_time_sampling_color,
                         linestyle = cfg_elec.electrical_time_sampling_linestyle,
                         linewidth = cfg_elec.electrical_time_sampling_linewidth,
                         marker = cfg_elec.electrical_time_sampling_marker,
                         markersize = cfg_elec.electrical_time_sampling_markersize, 
                         label = 'Sampled signal')
            
            # MV 20.01.r1 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.ax.set_title('Time data (' + str(self.fb_name) + ', Port:' + str(self.port_name) +
                                              ', Dir:' + str(self.direction) + ')')
            
            # MV 20.01.r3 5-Jun-20
            self.ax.title.set_color(cfg_elec.electrical_time_labels_axes_color)
            self.ax.set_xlabel('Time (sec)')
            self.ax.set_aspect('auto')
            self.ax.format_coord = self.format_coord_time
            
            # MV 20.01.r1 Linked plot settings to config file variables (to provide ability to
            # manage look and feel of plots)  
            if self.checkBoxMajorGrid.checkState() == 2:
                self.ax.grid(True)  
                self.ax.grid(which='major', 
                             linestyle = cfg_elec.electrical_time_maj_grid_linestyle, 
                             linewidth = cfg_elec.electrical_time_maj_grid_linewidth, 
                             color = cfg_elec.electrical_time_maj_grid_color)
           
            if self.checkBoxMinorGrid.checkState() == 2:
                self.ax.minorticks_on()
                self.ax.grid(which='minor', 
                             linestyle = cfg_elec.electrical_time_min_grid_linestyle, 
                             linewidth = cfg_elec.electrical_time_min_grid_linewidth, 
                             color = cfg_elec.electrical_time_min_grid_color)
                
            if self.checkBoxLegend.isChecked() == 1:
                self.ax.legend()
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
            msg.setWindowTitle("Plotting error (Electrical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
            
    #20.01.r1 2 Sep 19 - Added new functions for plotting=================================
    def adjust_units_for_plotting_time(self, signal):
        if self.radioButtonMag.isChecked() == 1:
            signal = np.real(signal)
        elif self.radioButtonLinearPwr.isChecked() == 1:
            signal = signal*np.conjugate(signal) #MV 20.01.r3 4-Jul-20
            #signal = signal*signal 
        else:
#            if np.count_nonzero(signal) == np.size(signal): 
            signal = 10*np.log10(signal*np.conjugate(signal)*1e3) #MV 20.01.r3 4-Jul-20
            #signal = 10*np.log10(signal*signal*1e3)
            
#            else:
#                signal += 1e-15 #Set to very low value
#                signal = 10*np.log10(signal*signal*1e3)  
        return signal
      
    # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to provide ability to
    # manage look and feel of plots)
    def set_signal_plot_time_domain(self, time, signal):
        self.ax.plot(time, signal, 
                     color = cfg_elec.electrical_time_signal_color, 
                     linestyle = cfg_elec.electrical_time_signal_linestyle, 
                     linewidth= cfg_elec.electrical_time_signal_linewidth, 
                     marker = cfg_elec.electrical_time_signal_marker , 
                     markersize = cfg_elec.electrical_time_signal_markersize,
                     label = 'Electrical signal') 
        
    def set_noise_plot_time_domain(self, time, signal):
        self.ax.plot(time, signal, 
                     color = cfg_elec.electrical_time_noise_color, 
                     linestyle = cfg_elec.electrical_time_noise_linestyle, 
                     linewidth = cfg_elec.electrical_time_noise_linewidth, 
                     marker = cfg_elec.electrical_time_noise_marker, 
                     markersize = cfg_elec.electrical_time_noise_markersize,
                     label ='Electrical noise')   
        
    def set_signal_and_noise_plot_time_domain(self, time, signal):
        self.ax.plot(time, signal, 
                     color = cfg_elec.electrical_time_sig_noise_color, 
                     linestyle = cfg_elec.electrical_time_sig_noise_linestyle, 
                     linewidth = cfg_elec.electrical_time_sig_noise_linewidth, 
                     marker = cfg_elec.electrical_time_sig_noise_marker, 
                     markersize = cfg_elec.electrical_time_sig_noise_markersize,
                     label = 'Electrical signal + noise')
    #=====================================================================================
    
    def format_coord_time(self, x, y):
        return 'Time=%0.7E, Mag/Power=%0.7E' % (x, y)
    
    '''Freq data tab (plotting methods)================================================'''
    def value_change_freq(self):
        new_iteration = int(self.spinBoxFreq.value())
        signal_updated = self.signals[new_iteration]   
        self.Y = np.fft.fft(signal_updated[5])
        self.Y_pos = self.Y[range(int(self.n/2))]
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.Y_pos = self.Y_pos*np.sqrt(2)
        self.Y_pos[0] = self.Y_pos[0]/np.sqrt(2) # DC component is not doubled
        self.N = np.fft.fft(signal_updated[6])
        self.N_pos = self.N[range(int(self.n/2))] # Positive freq only
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.N_pos = self.N_pos*np.sqrt(2)
        self.N_pos[0] = self.N_pos[0]/np.sqrt(2) # DC component is not doubled
        self.Y_N = np.fft.fft(signal_updated[5]+signal_updated[6])
        self.Y_N_pos = self.Y_N[range(int(self.n/2))] # Positive freq only
        # MV 20.01.r3 20-Jul-20: Folding of spectrum
        self.Y_N_pos = self.Y_N_pos*np.sqrt(2)
        self.Y_N_pos[0] = self.Y_N_pos[0]/np.sqrt(2) # DC component is not doubled
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
            back_color = cfg_elec.electrical_freq_plot_back_color
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
                
            if self.radioButtonLinearFreq.isChecked() == 1:
                self.af.set_ylabel('Power (W)')
            elif self.radioButtonLinearFreqSpectral.isChecked() == 1:
                self.af.set_ylabel('Power (W/Hz)')
            elif self.radioButtonLogFreqSpectral.isChecked() == 1:
                self.af.set_ylabel('Power (dBm/Hz)')    
            else:
                self.af.set_ylabel('Power (dBm)')
                
            #==================================================================
            # 20.01.r1 2 Sep 19 - Updated this section by introducing new 
            # function to adjust plotting (adjust_units_for_plotting_freq)
            # MV 20.01.r3 8-Jul-20: Changed to Y*conj(Y), from abs(Y)*abs(Y)
            # MV 20.01.r3 18-Sep-20 Bug fix:
            # Y*conj(Y) is now divided by n^2, previously was incorrectly
            # dividing by n
            if self.signalCheckBoxFreq.checkState() == 2:

                if self.checkBoxDisplayNegFreq.checkState() == 2:
                    sig_pwr = self.Y*np.conjugate(self.Y)/(self.n*self.n)
                    sig_pwr = self.adjust_units_for_plotting_freq(sig_pwr)
                    self.set_signal_plot_freq_domain(self.frq, sig_pwr)                
                else:
                    sig_pwr = self.Y_pos*np.conjugate(self.Y_pos)/(self.n*self.n)
                    sig_pwr = self.adjust_units_for_plotting_freq(sig_pwr)
                    self.set_signal_plot_freq_domain(self.frq_pos, sig_pwr) 
                        
            if self.noiseCheckBoxFreq.checkState() == 2:
                if self.checkBoxDisplayNegFreq.checkState() == 2:
                    noise_pwr = self.N*np.conjugate(self.N)/(self.n*self.n)
                    noise_pwr = self.adjust_units_for_plotting_freq(noise_pwr)
                    self.set_noise_plot_freq_domain(self.frq, noise_pwr) 
                else:
                    noise_pwr = self.N_pos*np.conjugate(self.N_pos)/(self.n*self.n)
                    noise_pwr = self.adjust_units_for_plotting_freq(noise_pwr)
                    self.set_noise_plot_freq_domain(self.frq_pos, noise_pwr) 
                        
            if self.sigandnoiseCheckBoxFreq.checkState() == 2:
                if self.checkBoxDisplayNegFreq.checkState() == 2:
                    sig_noise_pwr = self.Y_N*np.conjugate(self.Y_N)/(self.n*self.n)
                    sig_noise_pwr = self.adjust_units_for_plotting_freq(sig_noise_pwr)
                    self.set_signal_and_noise_plot_freq_domain(self.frq, sig_noise_pwr)
                else:
                    sig_noise_pwr = self.Y_N_pos*np.conjugate(self.Y_N_pos)/(self.n*self.n)
                    sig_noise_pwr = self.adjust_units_for_plotting_freq(sig_noise_pwr)
                    self.set_signal_and_noise_plot_freq_domain(self.frq_pos, sig_noise_pwr)
            #==================================================================
            
            # MV 20.01.r1 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.af.set_title('Freq data (' + str(self.fb_name) + ', Port:' + str(self.port_name) +
                                              ', Dir:' + str(self.direction) + ')')
            
            # MV 20.01.r3 5-Jun-20
            self.af.title.set_color(cfg_elec.electrical_freq_labels_axes_color)
    
            self.af.set_xlabel('Freq (Hz)')
            self.af.set_aspect('auto')
            self.af.format_coord = self.format_coord_freq
            
            # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks               
            self.af.xaxis.label.set_color(cfg_elec.electrical_freq_labels_axes_color)
            self.af.yaxis.label.set_color(cfg_elec.electrical_freq_labels_axes_color)
            self.af.tick_params(axis='both', which ='both', 
                                colors=cfg_elec.electrical_freq_labels_axes_color)
    
            # Plot settings (grid and legend) 
            # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to 
            # provide ability to manage look and feel of plots)         
            if self.checkBoxMajorGridFreq.checkState() == 2:
                self.af.grid(True)  
                self.af.grid(which='major', 
                             linestyle = cfg_elec.electrical_freq_maj_grid_linestyle, 
                             linewidth = cfg_elec.electrical_freq_maj_grid_linewidth,
                             color = cfg_elec.electrical_freq_maj_grid_color)
           
            if self.checkBoxMinorGridFreq.checkState() == 2:
                self.af.minorticks_on()
                self.af.grid(which='minor', 
                             linestyle = cfg_elec.electrical_freq_min_grid_linestyle, 
                             linewidth = cfg_elec.electrical_freq_min_grid_linewidth,
                             color = cfg_elec.electrical_freq_min_grid_color)
            
            #20.01.r1 2 Sep 19 - Added check (was missing from earlier release)   
            if self.checkBoxLegend.isChecked() == 1:
                self.af.legend()
                
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
            msg.setWindowTitle("Plotting error (Electrical port viewer)")
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
#            if np.count_nonzero(signal) == np.size(signal):
            signal = 10*np.log10(signal*1e3/self.fs)                 
#            else:
#                signal += 1e-30 #Set zero elements to very low value
#                signal = 10*np.log10(signal*1e3/self.fs)  
        else:
#            if np.count_nonzero(signal) == np.size(signal):
            signal = 10*np.log10(signal*1e3)
#            else:
#                signal += 1e-30 #Set to very low value
#                signal = 10*np.log10(signal*1e3)  
        return signal
    #=====================================================================================
        
    # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to provide 
    # ability to manage look and feel of plots       
    def set_signal_plot_freq_domain(self, freq, signal):
        self.af.plot(freq, signal, 
                     color = cfg_elec.electrical_freq_signal_color, 
                     linestyle = cfg_elec.electrical_freq_signal_linestyle, 
                     linewidth = cfg_elec.electrical_freq_signal_linewidth, 
                     marker = cfg_elec.electrical_freq_signal_marker, 
                     markersize = cfg_elec.electrical_freq_signal_markersize,
                     label = 'Electrical signal') 
        
    def set_noise_plot_freq_domain(self, freq, signal):
        self.af.plot(freq, signal, 
                     color = cfg_elec.electrical_freq_noise_color, 
                     linestyle = cfg_elec.electrical_freq_noise_linestyle, 
                     linewidth = cfg_elec.electrical_freq_noise_linewidth, 
                     marker = cfg_elec.electrical_freq_noise_marker, 
                     markersize = cfg_elec.electrical_freq_noise_markersize,
                     label = 'Electrical noise')   
        
    def set_signal_and_noise_plot_freq_domain(self, freq, signal):
        self.af.plot(freq, signal, 
                     color = cfg_elec.electrical_freq_sig_noise_color, 
                     linestyle = cfg_elec.electrical_freq_sig_noise_linestyle, 
                     linewidth = cfg_elec.electrical_freq_sig_noise_linewidth, 
                     marker = cfg_elec.electrical_freq_sig_noise_marker, 
                     markersize = cfg_elec.electrical_freq_sig_noise_markersize,
                     label = 'Electrical signal + noise')
        
    def format_coord_freq(self, x, y):
        return 'Freq=%0.7E, Power=%0.7E' % (x, y)
        
    '''Eye diagram tab (plotting methods)=============================================='''   
    def value_change_eye(self):
        new_iteration = int(self.spinBoxEye.value())
        signal_updated = self.signals[new_iteration]
        self.signal = signal_updated[5] #Electrical amplitudes
        self.noise = signal_updated[6]       
        self.tabData.setCurrentWidget(self.tab_eye)       
        self.plot_eye()
        self.canvas_eye.draw()
        
    def check_signal_changed_eye(self):
        self.tabData.setCurrentWidget(self.tab_eye)       
        self.plot_eye()
        self.canvas_eye.draw()
        
    def plot_eye(self):
        try:
            self.figure_eye.clf() # MV 20.01.r1 30-Oct-2019
            # MV 20.01.r1 Added new feature to select plot area background color
            back_color = cfg_elec.electrical_eye_plot_back_color
            self.eye = self.figure_eye.add_subplot(111, facecolor = back_color)
            self.eye.clear()
            
            eye_num = 3
            eye_win = self.sym_period*eye_num 
            
            #Build arrays for plotting eye diagram=============================
            if (self.signalCheckBoxEye.checkState() == 2
                or self.sigandnoiseCheckBoxEye.checkState() == 2):
                #eye_num = 3
                #eye_win = self.sym_period*eye_num 
                if self.windowEye.text():
                    eye_num = int(round(float(self.windowEye.text())))
                    eye_win = self.sym_period*eye_num #Convert to time units      
                # Initialize array for time window associated with eye
                eye_section = np.array([])
    
                # Sample time data to be used for tiling
                # MV 20.01.r1 1-Nov-19 (replaced append operation with searchsorted)
                index_eye_win = np.searchsorted(self.time, eye_win, side='right')
                eye_section = self.time[0:index_eye_win]            
    
                #Rebuild time array by "tiling" time window defined for eye
                num_tiles = round(self.n/np.size(eye_section))
                eye_len = np.size(eye_section)
                time_wrapped = np.tile(eye_section, num_tiles)
                # Shorten arrays to be within a multiple of eye window                            
                time_wrapped = np.resize(time_wrapped, num_tiles*eye_len)
                signal = np.resize(self.signal, num_tiles*eye_len) # MV 20.01.r3 7-Jul-20
                noise = np.resize(self.noise, num_tiles*eye_len) # MV 20.01.r3 7-Jul-20
                # Re-organize arrays to match eye length
                time_wrapped = np.reshape(time_wrapped, (num_tiles, eye_len))
                signal = np.reshape(signal, (num_tiles, eye_len))
                noise = np.reshape(noise, (num_tiles, eye_len))
                
                #------------------------------------------------------------------
                # Eye metrics calculations
                # MV 20.01.r3 18-Jun-20
                if (self.decisionThreshold.text() and self.decisionPoint.text() 
                    and self.histWidth.text() and self.histCoverage.text()):
                    decision_th = float(self.decisionThreshold.text())
                    decision_pt = float(self.decisionPoint.text())
                    hist_width = float(self.histWidth.text())
                    hist_coverage = float(self.histCoverage.text())
                
                oma_ref = None
                if self.omaRef.text(): #Use as reference for VECP 
                    oma_ref = float(self.omaRef.text())
    
                # Find min/max time sampling points for eye window
                t_width_half = hist_width*0.01/2
                t_start = self.sym_period*(decision_pt - t_width_half)
                t_end = self.sym_period*(decision_pt + t_width_half)
                t_start_index = np.min(np.where(time_wrapped[0] >= t_start))
                t_end_index = np.max(np.where(time_wrapped[0] <= t_end))
                
                # Collect all samples that fall within time slice and 
                # split into upper (binary 1) and lower (binary 0) histograms
                # https://www.tutorialspoint.com/numpy/numpy_indexing_and_slicing.htm
                # https://thispointer.com/python-numpy-select-elements-or-indices-
                # by-conditions-from-numpy-array/
                signal_hist = np.real(signal[...,t_start_index:t_end_index+1])    
                signal_hist_upper = signal_hist[signal_hist > decision_th]
                signal_hist_lower = signal_hist[signal_hist <= decision_th]
                
                # Upper histogram statistics---------------------------------------
                clip_percent = (100 - hist_coverage)/2
                if np.size(signal_hist_upper) > 0:
                    upper_percentile_max = np.percentile(signal_hist_upper, 
                                                     hist_coverage + clip_percent)
                    upper_percentile_min =  np.percentile(signal_hist_upper,
                                             (100 - hist_coverage) - clip_percent)           
                    # Adjust histogram coverage (remove % of edges)
                    signal_hist_upper = signal_hist_upper[signal_hist_upper < 
                                                      upper_percentile_max]
                    signal_hist_upper = signal_hist_upper[signal_hist_upper >= 
                                                      upper_percentile_min]  
                # Calculate mean, min, and max values
                upper_histgr_mean = 0
                upper_histgr_max = 0
                upper_histgr_min = 0  
                if np.size(signal_hist_upper) > 0:
                    upper_histgr_mean = np.mean(signal_hist_upper)
                    upper_histgr_max = np.max(signal_hist_upper)
                    upper_histgr_min = np.min(signal_hist_upper)            
          
                # Lower histogram statistics---------------------------------------
                if np.size(signal_hist_lower) > 0:
                    lower_percentile_max = np.percentile(signal_hist_lower, 
                                                     hist_coverage + clip_percent)
                    lower_percentile_min =  np.percentile(signal_hist_lower,
                                             (100 - hist_coverage) - clip_percent)           
                    # Adjust histogram coverage (remove % of edges)           
                    signal_hist_lower = signal_hist_lower[signal_hist_lower < 
                                                      lower_percentile_max]
                    signal_hist_lower = signal_hist_lower[signal_hist_lower >= 
                                                      lower_percentile_min]
                # Calculate mean, min, and max values
                lower_histgr_mean = 0
                lower_histgr_max = 0
                lower_histgr_min = 0 
                if np.size(signal_hist_lower) > 0:
                    lower_histgr_mean = np.mean(signal_hist_lower)
                    lower_histgr_max = np.max(signal_hist_lower)
                    lower_histgr_min = np.min(signal_hist_lower)                
                
                # Calculate OMA
                if not oma_ref: # is None
                    oma_ref = upper_histgr_mean - lower_histgr_mean
                
                # Calculate Ao and VECP
                upper_edge = upper_histgr_mean - (upper_histgr_max - upper_histgr_min)/2
                lower_edge = lower_histgr_mean + (lower_histgr_max - lower_histgr_min)/2
                a_0 = upper_edge - lower_edge
                if a_0 > 0:
                    vecp = 10*np.log10(oma_ref/a_0)
                else:
                    vecp = 0
                
                # Output results
                self.resultOMA.setText(str(format(oma_ref, '0.3E')))
                self.resultA0.setText(str(format(a_0, '0.3E')))
                self.resultVECP.setText(str(format(vecp, '0.2f')))
                
                # Create bars for histograms---------------------------------------
                if self.checkBoxHistBoxes.checkState() == 2:
                    h_upper = upper_histgr_max - upper_histgr_min
                    h_lower = lower_histgr_max - lower_histgr_min
                    w = t_end - t_start
                    color_hist = cfg_elec.electrical_eye_hist_color
                    alpha_hist = cfg_elec.electrical_eye_hist_alpha
                    self.eye.bar(t_start, h_upper, w, upper_histgr_min, 
                                 alpha=alpha_hist, fill=1, color=color_hist, 
                                 zorder=20, edgecolor=color_hist,
                                 align='edge')
                    
                    self.eye.bar(t_start, h_lower, w, lower_histgr_min, 
                                 alpha=alpha_hist, fill=1, color=color_hist, 
                                 zorder=20, edgecolor=color_hist,
                                 align='edge')
                #------------------------------------------------------------------
            
            #Y-axis label settings
            if self.radioButtonMagEye.isChecked() == 1:
                self.eye.set_ylabel('Magnitude') # MV 20.01.r3 17-Sep-20 Removed V
            elif self.radioButtonLinearPwrEye.isChecked() == 1:   
                self.eye.set_ylabel('Power (W)')
            else:
                self.eye.set_ylabel('Power (dBm)')
    
            #Plot signals (signal or signal+noise)=================================
            if self.signalCheckBoxEye.checkState() == 2:           
                if self.radioButtonMagEye.isChecked() == 1:
                    self.set_signal_plot_eye_diagram(time_wrapped, signal, 0)
                elif self.radioButtonLinearPwrEye.isChecked() == 1:
                    self.set_signal_plot_eye_diagram(time_wrapped, signal, 1)
                else:
                    self.set_signal_plot_eye_diagram(time_wrapped, signal, 2)    
                  
            if self.sigandnoiseCheckBoxEye.checkState() == 2:            
                if self.radioButtonMagEye.isChecked() == 1:
                    self.set_signal_noise_plot_eye_diagram(time_wrapped, signal,
                                                           noise, 0)
                elif self.radioButtonLinearPwrEye.isChecked() == 1:
                    self.set_signal_noise_plot_eye_diagram(time_wrapped, signal,
                                                           noise, 1)
                else:
                    self.set_signal_noise_plot_eye_diagram(time_wrapped, signal,
                                                           noise, 2)
            
            # MV 20.01.r1 15-Sep-19 (Cleaned up title - was getting too long & causing 
            # issues with tight layout)
            self.eye.set_title('Eye diagram (' + str(self.fb_name) + ', Port:' + str(self.port_name) +
                                              ', Dir:' + str(self.direction) + ')')
            
            # MV 20.01.r3 5-Jun-20
            self.eye.title.set_color(cfg_elec.electrical_eye_labels_axes_color)
            
            self.eye.set_xlabel('Time (sec)')
            self.eye.set_aspect('auto')
            self.eye.format_coord = self.format_coord_eye
            
            # MV 20.01.r3 18-Jun-20 Set x-axis limits to exactly match
            # symbol period
            self.eye.set_xlim([0,eye_win])
            
            # MV 20.01.r1 3-Nov-2019 Color settings for x and y-axis labels and tick marks                   
            self.eye.xaxis.label.set_color(cfg_elec.electrical_eye_labels_axes_color)
            self.eye.yaxis.label.set_color(cfg_elec.electrical_eye_labels_axes_color)
            self.eye.tick_params(axis='both', which ='both', 
                                colors=cfg_elec.electrical_eye_labels_axes_color)
            
            # Plot settings (grid and legend)
            # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to 
            # provide ability to manage look and feel of plots)          
            if self.checkBoxMajorGridEye.checkState() == 2:
                self.eye.grid(True)  
                self.eye.grid(which='major', 
                              linestyle = cfg_elec.electrical_eye_maj_grid_linestyle, 
                              linewidth = cfg_elec.electrical_eye_maj_grid_linewidth, 
                              color = cfg_elec.electrical_eye_maj_grid_color)
           
            if self.checkBoxMinorGridEye.checkState() == 2:
                self.eye.minorticks_on()
                self.eye.grid(which='minor', 
                              linestyle = cfg_elec.electrical_eye_min_grid_linestyle, 
                              linewidth = cfg_elec.electrical_eye_min_grid_linewidth, 
                              color = cfg_elec.electrical_eye_min_grid_color )
        
        except: # MV 20.01.r2 24-Feb-20
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error plotting eye diagram')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Plotting error (Electrical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
    
    # MV 20.01.r1 Linked plot settings to config_port_viewers file variables (to provide 
    # ability to manage look and feel of plots)  
    def set_signal_plot_eye_diagram(self, time_wrapped, signal, signal_format):
        for i in range(len(time_wrapped)):
            if signal_format == 0: # MV 20.01.r3 7-Jul-20
                signal[i] = np.real(signal[i])
            if signal_format == 1:
                signal[i] = signal[i]*np.conjugate(signal[i]) # MV 20.01.r3 4-Jul-20
                #signal[i] = signal[i]*signal[i]
            if signal_format == 2:
                signal[i] = 10*np.log10(signal[i]*np.conjugate(signal[i])*1e3) # MV 20.01.r3 4-Jul-20
                #signal[i] = 10*np.log10(signal[i]*signal[i]*1e3)
            # MV 20.01.r3 10-Jul-20 Added alpha parameter to create density effect
            # Thanks to posters on stack overflow!
            # https://stackoverflow.com/questions/61574246/how-can-i-draw-an-eye-diagram-
            # like-plot-in-pandas (accessed 10-Jul-20)
            self.eye.plot(time_wrapped[i], signal[i], 
                          color = cfg_elec.electrical_eye_signal_color,
                          linestyle = cfg_elec.electrical_eye_signal_linestyle, 
                          linewidth = cfg_elec.electrical_eye_signal_linewidth, 
                          marker = cfg_elec.electrical_eye_signal_marker,
                          markersize = cfg_elec.electrical_eye_signal_markersize, 
                          zorder = 10, label ='Electrical signal',
                          alpha = cfg_elec.electrical_eye_signal_alpha)
            
    def set_signal_noise_plot_eye_diagram(self, time_wrapped, signal,
                                          noise, signal_format):
        for i in range(len(time_wrapped)):
            signal_noise = signal[i] + noise[i]
            if signal_format == 0: # MV 20.01.r3 7-Jul-20
                signal_noise = np.real(signal_noise)
            if signal_format == 1:
                signal_noise = signal_noise*np.conjugate(signal_noise) # MV 20.01.r3 4-Jul-20
                #signal_noise = signal_noise*signal_noise
            if signal_format == 2:
                signal_noise = 10*np.log10(signal_noise*np.conjugate(signal_noise)*1e3) # MV 20.01.r3 4-Jul-20
                #signal_noise = 10*np.log10(signal_noise*signal_noise*1e3)
            self.eye.plot(time_wrapped[i], signal_noise, 
                          color = cfg_elec.electrical_eye_sig_noise_color,
                          linestyle = cfg_elec.electrical_eye_sig_noise_linestyle, 
                          linewidth = cfg_elec.electrical_eye_sig_noise_linewidth, 
                          marker = cfg_elec.electrical_eye_sig_noise_marker,
                          markersize = cfg_elec.electrical_eye_sig_noise_markersize,
                          label = 'Electrical signal + noise',
                          alpha = cfg_elec.electrical_eye_sig_noise_alpha)
            
    '''def set_signal_plot_eye_hist(self, time_wrapped, signal, signal_format):
        time_wrapped_all = np.ravel(time_wrapped)
        signal_all = np.ravel(signal)
        from matplotlib import colors
        self.eye.hist2d(time_wrapped_all, signal_all, bins=300, cmap='inferno',
                        norm=colors.PowerNorm(0.5))'''
            
    def format_coord_eye(self, x, y):
        return 'Time=%0.7E, Mag/Power=%0.7E' % (x, y)
            
    '''Signal data tab=========================================================
    portID(0), signal_type(1), carrier(2), sample_rate(3), time_array(4), 
    amplitude_array(5), noise_array(6)
    '''
    def iteration_change_signal_data(self):
        new_iteration = int(self.spinBoxSignalData.value())
        signal_updated = self.signals[new_iteration]
        # Time domain data
        self.carrier = signal_updated[2]
        self.time = signal_updated[4] #MV 20.01.r2 15-Feb-20
        self.signal = signal_updated[5] #Electrical amplitudes
        self.noise = signal_updated[6]
        self.update_signal_data()
        # Freq domain data
        self.Y = np.fft.fft(signal_updated[5])
        self.Y_pos = self.Y[range(int(self.n/2))]
        self.N = np.fft.fft(signal_updated[6])
        self.N_pos = self.N[range(int(self.n/2))] # Positive freq only  
        self.Y_N = np.fft.fft(signal_updated[5]+signal_updated[6])
        self.Y_N_pos = self.Y_N[range(int(self.n/2))] # Positive freq only 
        
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
            self.signalBrowser.append('Signal data (electrical) - Iteration '+str(i))
            self.signalBrowser.append(self.fb_name + ', Port:' +
                                self.port_name + ', Dir:' + str(self.direction))
            self.signalBrowser.setCurrentFont(self.font_normal)
            self.signalBrowser.setTextColor(QtGui.QColor('#000000'))
            self.signalBrowser.append('Sample rate (Hz): ' + str(self.fs))
            self.signalBrowser.append('Carrier freq (Hz): ' + str(self.carrier))
            
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
        
            data1['index'] = index_array
            data2['index'] = index_array
               
            #Print signal data (magnitude) array
            self.signalBrowser.setCurrentFont(self.font_bold)
            self.signalBrowser.append(' ')
            if self.radioButtonSigTime.isChecked() == 1:
                data1['x'] = self.time[self.start_index-1:self.end_index-1]
                if self.radioButtonComplexSignalData.isChecked() == 1:
                    self.signalBrowser.append('Signal data (index, time(s), real, imag):')
                    data1['y'] = self.signal[self.start_index-1:self.end_index-1]
                else:
                    self.signalBrowser.append('Signal data (index, time(s), mag, phase):')
                    data1['y1'] = np.abs(self.signal[self.start_index-1:self.end_index-1])
                    data1['y2'] = np.angle(self.signal[self.start_index-1:self.end_index-1])
            else:
                data1['x'] = self.frq[self.start_index-1:self.end_index-1]
                if self.radioButtonComplexSignalData.isChecked() == 1:
                    self.signalBrowser.append('Signal data (index, freq(Hz), real, imag):') 
                    # MV 20.01.r3 18-Sep-20, FFT is not normalized, so need to divide by n
                    data1['y'] = self.Y[self.start_index-1:self.end_index-1]/self.n
                else:
                    self.signalBrowser.append('Signal data (index, freq(Hz), mag, phase):') 
                    # MV 20.01.r3 18-Sep-20, FFT is not normalized, so need to divide by n
                    data1['y1'] = np.abs(self.Y[self.start_index-1:self.end_index-1])/self.n
                    data1['y2'] = np.angle(self.Y[self.start_index-1:self.end_index-1])
                    
            # Adjust for linewidth setting      
            self.linewidth = 60
            if self.linewidthSignalData.text():
                self.linewidth = int(self.linewidthSignalData.text())
            
            # Print array (signal data)
            self.signalBrowser.setCurrentFont(self.font_normal)
            self.signalBrowser.append(np.array2string(data1, max_line_width = self.linewidth))
    
            #Print signal noise array
            self.signalBrowser.setCurrentFont(self.font_bold)
            self.signalBrowser.append(' ')
            if self.radioButtonSigTime.isChecked() == 1:
                data2['x'] = self.time[self.start_index-1:self.end_index-1]
                if self.radioButtonComplexSignalData.isChecked() == 1:
                    self.signalBrowser.append('Signal noise (index, time(s), real, imag):')
                    data2['y'] = self.noise[self.start_index-1:self.end_index-1]
                else:
                    self.signalBrowser.append('Signal noise (index, time(s), mag, phase):')
                    data2['y1'] = np.abs(self.noise[self.start_index-1:self.end_index-1])
                    data2['y2'] = np.angle(self.noise[self.start_index-1:self.end_index-1])
            else:
    
                data2['x'] = self.frq[self.start_index-1:self.end_index-1]
                if self.radioButtonComplexSignalData.isChecked() == 1:
                    self.signalBrowser.append('Signal noise (index, freq(Hz), real, imag):') 
                    data2['y'] = self.N[self.start_index-1:self.end_index-1]
                else:
                    self.signalBrowser.append('Signal noise (index, freq(Hz), mag, phase):')
                    data2['y1'] = np.abs(self.N[self.start_index-1:self.end_index-1])
                    data2['y2'] = np.angle(self.N[self.start_index-1:self.end_index-1])              
            
            # Print array (signal noise)
            self.signalBrowser.setCurrentFont(self.font_normal)
            self.signalBrowser.append(np.array2string(data2, max_line_width = self.linewidth))
    
            # Move cursor back to top of browser
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
            msg.setWindowTitle("Plotting error (Electrical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()

    '''Signal metrics tab=============================================================='''
    def iteration_change_signal_metrics(self):
        new_iteration = int(self.spinBoxSignalMetrics.value())
        signal_updated = self.signals[new_iteration]
        self.carrier = signal_updated[2]
        self.signal = signal_updated[5] #Electrical amplitudes
        self.noise = signal_updated[6]
        self.update_signal_metrics() 
    
    def update_signal_metrics(self):
        try:
            sig_mean = np.mean(np.real(self.signal))
            self.signalMean.setText(str(format(sig_mean, '0.3E')))
            sig_var = np.var(np.real(self.signal))
            self.signalVar.setText(str(format(sig_var, '0.3E')))
            sig_std_dev = np.std(np.real(self.signal))
            self.signalStdDev.setText(str(format(sig_std_dev, '0.3E')))
            sig_tot_pwr = np.sum(np.abs(self.signal)*np.abs(self.signal))
            self.signalTotalPwr.setText(str(format(sig_tot_pwr, '0.3E')))
            if sig_tot_pwr > 0:
                sig_tot_pwr_dbm = 10*np.log10(sig_tot_pwr*1e3)
                self.signalTotalPwrDbm.setText(str(format(sig_tot_pwr_dbm, '0.3E')))
            else:
                self.signalTotalPwrDbm.setText('NA')
            sig_avg_pwr = np.sum(np.abs(self.signal)*np.abs(self.signal))/self.n
            self.signalAvgPwr.setText(str(format(sig_avg_pwr, '0.3E')))
            if sig_avg_pwr > 0:
                sig_avg_pwr_dbm = 10*np.log10(sig_avg_pwr*1e3)
                self.signalAvgPwrDbm.setText(str(format(sig_avg_pwr_dbm, '0.3E')))
            else:
                self.signalAvgPwrDbm.setText('NA')
            #Noise metrics
            # Mean, variance and standard deviation of noise samples
            noise_mean = np.mean(np.real(self.noise))
            self.noiseMean.setText(str(format(noise_mean, '0.3E')))
            noise_var = np.var(np.real(self.noise))
            self.noiseVar.setText(str(format(noise_var, '0.3E')))
            noise_std_dev = np.std(np.real(self.noise))
            self.noiseStdDev.setText(str(format(noise_std_dev, '0.3E')))
            noise_tot_pwr = np.sum(np.abs(self.noise)*np.abs(self.noise))
            # Noise total power (over sampling bandwidth)
            self.noiseTotalPwr.setText(str(format(noise_tot_pwr, '0.3E')))
            if noise_tot_pwr > 0:
                noise_tot_pwr_dbm = 10*np.log10(noise_tot_pwr*1e3)
                self.noiseTotalPwrDbm.setText(str(format(noise_tot_pwr_dbm, '0.3E')))
            else:
                self.noiseTotalPwrDbm.setText('NA')
            # Noise average power (noise total/num of samples)
            noise_avg_pwr = np.sum(np.abs(self.noise)*np.abs(self.noise))/self.n
            self.noiseAvgPwr.setText(str(format(noise_avg_pwr, '0.3E')))
            if noise_avg_pwr > 0:
                noise_avg_pwr_dbm = 10*np.log10(noise_avg_pwr*1e3)
                self.noiseAvgPwrDbm.setText(str(format(noise_avg_pwr_dbm, '0.3E')))
            else:
                self.noiseAvgPwrDbm.setText('NA')
            # Noise spectral density
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
                
        except: # MV 20.01.r2 24-Feb-20
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
            msg.setWindowTitle("Plotting error (Electrical port viewer)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
    
        '''Close event================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_freq)
        plt.close(self.figure_eye)
    
        
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
