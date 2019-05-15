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

    SystemLab module for port analyzer(GUI) classes: SignalDigital
'''

import os
import config
gui_ui_path = config.root_path
import numpy as np

from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib.pyplot as plt
# Method for embedding Matplotlib canvases into Qt-designed QDialog interfaces
# Ref: https://matplotlib.org/gallery/user_interfaces/embedding_in_qt_sgskip.html
# Accessed: 11 Feb 2019
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

qtDigitalPortDataViewerFile = os.path.join(gui_ui_path, 'syslab_gui_files', 'DigitalDataViewer.ui')
qtDigitalPortDataViewerFile = os.path.normpath(qtDigitalPortDataViewerFile)
Ui_PortDataWindow_Digital, QtBaseClass = uic.loadUiType(qtDigitalPortDataViewerFile)

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 80

     
class DigitalPortDataAnalyzer(QtWidgets.QDialog, Ui_PortDataWindow_Digital):
    '''
    Digital signal format:
    portID(0), signal_type(1), symbol_rate(2), bit_rate(3), order(4), 
    time_array(5), discrete_array(6)
    
    '''
    def __init__(self, signal_data, fb_name, port_name, direction, design_settings):
        QtWidgets.QDialog.__init__(self)
        Ui_PortDataWindow_Digital.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.fb_name = fb_name
        self.port_name = port_name
        self.direction = direction
#        plt.ion() #Interactive mode for plotting
             
        iterations = len(signal_data)   
        self.spinBoxTime.setMaximum(iterations)
        self.spinBoxFreq.setMaximum(iterations)
        self.totalIterationsTime.setText(str(iterations))
        self.totalIterationsFreq.setText(str(iterations))
        self.spinBoxTime.valueChanged.connect(self.valueChangeTime)
        self.spinBoxFreq.valueChanged.connect(self.valueChangeFreq)        
        self.displayUnitInterval.toggled.connect(self.checkSignalChangedSequence)
        self.displayTime.toggled.connect(self.checkSignalChangedSequence)   
        
        self.actionSeqWindow.clicked.connect(self.updateTimeAxis)
        self.actionFreqWindow.clicked.connect(self.updateFreqAxis)
        self.checkBoxDisplayNegFreq.stateChanged.connect(self.checkSignalChangedFreq)
        
        #Signal data tab (dataFrameSignal)===================================== 
        #Iterations group box
        iterations = len(signal_data)   
        self.spinBoxSignalData.setMaximum(iterations)
        self.totalIterationsSignalData.setText(str(iterations))
        self.spinBoxSignalData.valueChanged.connect(self.iterationChangeSignalData)
        #Domain setting group box
        self.radioButtonSigFreq.toggled.connect(self.updateSignalData)
        self.radioButtonSigTime.toggled.connect(self.updateSignalData)
        #X-axis signal format group box
        self.radioButtonUnitSignalData.toggled.connect(self.updateSignalData)
        self.radioButtonTimeSignalData.toggled.connect(self.updateSignalData)
        #Adjust samples group box
        self.actionSetIndicesSignalData.clicked.connect(self.updateSignalData)
        #View settings group box
        self.linewidthSignalData.setText(str(60))
        self.actionSetLinewidthSignalData.clicked.connect(self.updateSignalData)

        #Setup initial data for iteration 1 (default)
        self.iteration = 1  
        self.signals = signal_data
        self.total_samples = design_settings['num_samples']
        self.sample_rate = design_settings['sampling_rate']
        self.sampling_period = design_settings['sampling_period']
        signal_default = self.signals[self.iteration]
        self.time = signal_default[5] #Sampled time array
        self.discrete = signal_default[6] #Digital samples
        self.seq_length = len(self.discrete) #Length of data sequence (number of symbols)
        self.units = np.linspace(1, self.seq_length, self.seq_length, dtype = 'int') #Unit interval
        self.totalSamples.setText(str(format(self.total_samples, '0.3E')))
        self.totalBits.setText(str(format(self.seq_length, '0.3E')))       
        self.totalSymbols.setText(str(format((self.seq_length/signal_default[4]), '0.3E')))
        self.bitRate.setText(str(format(signal_default[3], '0.3E')))
        self.symbolRate.setText(str(format(signal_default[2], '0.3E')))
        self.symbolOrder.setText(str(signal_default[4]))

        self.samples_per_bit = int(round(self.sample_rate/signal_default[3]))
        self.samplesBit.setText(str(format(self.samples_per_bit, '0.3E')))
        self.samples_per_symbol = int(round(self.sample_rate/signal_default[2])) 
        self.samplesSymbol.setText(str(format(self.samples_per_symbol, '0.3E')))
        
        self.discrete_time = []

        for sym in range(0,self.seq_length):
            i = 0
            while i < int(self.samples_per_symbol):
                self.discrete_time.append(self.discrete[sym])
                i += 1

        #Setup frequency domain analysis================================================
        # REF:  Fast Fourier Transform in matplotlib, 
        # An example of FFT audio analysis in matplotlib and the fft function.
        # Source: https://plot.ly/matplotlib/fft/(accessed 20-Mar-2018) 
        self.totalSamplesFreq.setText(str(format(self.total_samples, '0.3E')))
        self.samplingPeriod.setText(str(format(self.sampling_period, '0.3E')))
        self.samplingRate.setText(str(format(self.sample_rate, '0.3E')))
    
        self.n = int(len(self.discrete_time))
        T = self.n/self.sample_rate
        k = np.arange(self.n)
        self.frq = k/T # Positive/negative freq (double sided)
        self.frq_pos = self.frq[range(int(self.n/2))] # Positive freq only (single sided)
        
        #FFT computation
        self.Y = np.fft.fft(self.discrete_time)/self.n
        self.Y_pos = self.Y[range(int(self.n/2))]
        #===============================================================================
        
        #Setup background colors for frames
        p = self.graphFrame.palette() 
        p.setColor(self.graphFrame.backgroundRole(), QtGui.QColor(250,250,250))
        self.graphFrame.setPalette(p)       
        p2 = self.dataFrame.palette()
        p2.setColor(self.dataFrame.backgroundRole(), QtGui.QColor(250,250,250))
        self.dataFrame.setPalette(p2)
        p3 = self.graphFrameFreq.palette() 
        p3.setColor(self.graphFrameFreq.backgroundRole(), QtGui.QColor(250,250,250))
        self.graphFrameFreq.setPalette(p3)
        p4  = self.dataFrameFreq.palette() 
        p4.setColor(self.dataFrameFreq.backgroundRole(), QtGui.QColor(250,250,250))
        self.dataFrameFreq.setPalette(p4)
        
        #Setup matplotlib figures and toolbars
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.figure = plt.figure()
        self.figure.set_tight_layout(True)
        self.canvas = FigureCanvas(self.figure)   
        self.toolbar = NavigationToolbar(self.canvas, self.tab_sequence)   
        self.graphLayout.addWidget(self.canvas)
        self.graphLayout.addWidget(self.toolbar)
        self.graphFrame.setLayout(self.graphLayout)

        self.graphLayoutFreq = QtWidgets.QVBoxLayout()
        self.figure_freq = plt.figure()
        self.canvas_freq = FigureCanvas(self.figure_freq)     
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self.tab_freq)
        self.graphLayoutFreq.addWidget(self.canvas_freq)
        self.graphLayoutFreq.addWidget(self.toolbar_freq)
        self.graphFrameFreq.setLayout(self.graphLayoutFreq)
        
        self.tabData.setCurrentWidget(self.tab_freq)
        self.plot_freq_domain(0)
#        set_mpl_cursor()
        self.figure_freq.set_tight_layout(True)
        self.tabData.setCurrentWidget(self.tab_sequence)
        self.plot_sequence(0)
#        set_mpl_cursor()
        
        #Prepare default data for signal data viewer===================================
        self.totalSamplesSignalData.setText(str(format(self.seq_length, 'n')))
        self.minIndexSignalData.setText(str(1))
        self.maxIndexSignalData.setText(str(format(self.seq_length, 'n')))
        self.updateSignalData()
        #Return to sequence tab
        self.tabData.setCurrentWidget(self.tab_sequence)
        
    def valueChangeTime(self):
        new_iteration = int(self.spinBoxTime.value())
        signal_updated = self.signals[new_iteration]

        self.time = signal_updated[5] #Sampled time array
        self.discrete = signal_updated[6] #Digital samples
        self.seq_length = len(self.discrete) #Length of data sequence (number of bits/symbols)
        self.units = np.linspace(1, self.seq_length, self.seq_length, dtype = 'int') #Unit interval
        self.totalSamples.setText(str(format(self.total_samples, '0.3E')))
        self.totalBits.setText(str(format(self.seq_length, '0.3E')))       
        self.totalSymbols.setText(str(format((self.seq_length/signal_updated[4]), '0.3E')))
        self.bitRate.setText(str(format(signal_updated[3], '0.3E')))
        self.symbolRate.setText(str(format(signal_updated[2], '0.3E')))
        self.symbolOrder.setText(str(signal_updated[4]))
        
        self.samples_per_bit = int(round(self.sample_rate/signal_updated[3]))
        self.samplesBit.setText(str(format(self.samples_per_bit, '0.3E')))
        self.samples_per_symbol = int(round(self.sample_rate/signal_updated[2]))      
        self.samplesSymbol.setText(str(format(self.samples_per_symbol, '0.3E')))
        
        self.discrete_time = []
        for sym in range(0,self.seq_length):
            i = 0
            while i < int(self.samples_per_symbol):
                self.discrete_time.append(self.discrete[sym])
                i += 1
        
        self.tabData.setCurrentWidget(self.tab_sequence)       
        self.plot_sequence(0)
#        set_mpl_cursor()
        self.canvas.draw()
        
    def checkSignalChangedSequence(self):
        self.tabData.setCurrentWidget(self.tab_sequence)       
        self.plot_sequence(0)
#        set_mpl_cursor()
        self.canvas.draw()
        
    def updateTimeAxis(self):
        self.plot_sequence(1)
#        set_mpl_cursor()
        self.canvas.draw()
        
    def plot_sequence(self, time_axis_adjust):
        ax = self.figure.add_subplot(111, facecolor = '#f9f9f9')
        ax.clear()
        
        if time_axis_adjust == 1:
            start_unit = self.minUnit.text()
            end_unit = self.maxUnit.text()
            ax.set_xlim(float(start_unit), float(end_unit))
            
        if self.displayTime.isChecked() == 1:
            ax.plot(self.time, self.discrete_time, color = 'b', linestyle = '--', linewidth= 0.8, marker = 'o', markersize = 3)            
            ax.set_xlabel('Time (sec)')
        if self.displayUnitInterval.isChecked() == 1:
            ax.plot(self.units, self.discrete, color = 'b', linestyle = '--', linewidth= 0.8, marker = 'o', markersize = 3)            
            ax.set_xlabel('Symbol index')   
            
        ax.set_title('Sequence data - digital ('+ self.fb_name + ': ' +
                            self.port_name + ' ' + str(self.direction) + ')')
        ax.set_ylabel('Discrete value (a.u.)')
        ax.set_aspect('auto')
        ax.format_coord = self.format_coord_seq
                
        self.canvas.draw()
        
    def format_coord_seq(self, x, y):
        return 'Time/Samples=%0.7E, Mag=%0.7E' % (x, y)
        
    def valueChangeFreq(self):
        new_iteration = int(self.spinBoxFreq.value())
        signal_updated = self.signals[new_iteration]   
        
        self.discrete = signal_updated[6] #Digital samples
        self.seq_length = len(self.discrete) #Length of data sequence (number of bits/symbols)
        self.totalSamples.setText(str(format(self.total_samples, '0.3E')))
        
        self.samples_per_symbol = int(round(self.sample_rate/signal_updated[2]))      
        
        self.totalSamplesFreq.setText(str(format(self.total_samples, '0.3E')))
        self.samplingPeriod.setText(str(format(self.sampling_period, '0.3E')))
        self.samplingRate.setText(str(format(self.sample_rate, '0.3E')))
        
        self.discrete_time = []
        for sym in range(0,self.seq_length):
            i = 0
            while i < int(self.samples_per_symbol):
                self.discrete_time.append(self.discrete[sym])
                i += 1
        
        self.Y = np.fft.fft(self.discrete_time)/self.n # fft computing and normalization
        self.Y_pos = self.Y[range(int(self.n/2))]
        self.tabData.setCurrentWidget(self.tab_freq)       
        self.plot_freq_domain(0)
#        set_mpl_cursor()
        self.canvas_freq.draw()
        
    def checkSignalChangedFreq(self):
        self.tabData.setCurrentWidget(self.tab_freq)       
        self.plot_freq_domain(0)
#        set_mpl_cursor()
        self.canvas_freq.draw()
        
    def updateFreqAxis(self):
        self.plot_freq_domain(1)
#        set_mpl_cursor()
        self.canvas_freq.draw()
        
    def plot_freq_domain(self, freq_axis_adjust):
        af = self.figure_freq.add_subplot(111, facecolor = '#f9f9f9')
        af.clear()
        
        if freq_axis_adjust == 1:
            start_freq = self.minFreq.text()
            end_freq = self.maxFreq.text()
            af.set_xlim(float(start_freq), float(end_freq))
        
        if self.checkBoxDisplayNegFreq.checkState() == 2:
            af.plot(self.frq, abs(self.Y), color = 'b', linestyle = '--', 
                    linewidth= 0.8, marker = 'o', markersize = 3)  
        else:
            af.plot(self.frq_pos, abs(self.Y_pos), color = 'b', linestyle = '--', 
                    linewidth= 0.8, marker = 'o', markersize = 3)
        af.set_title('Freq data - digital ('+ self.fb_name + ': ' +
                            self.port_name + ' ' + str(self.direction) + ')')
        af.set_xlabel('Freq (Hz)')
        af.set_ylabel('|Y(freq)|')
        af.set_aspect('auto')
        af.format_coord = self.format_coord_freq
        
    def format_coord_freq(self, x, y):
        return 'Freq=%0.7E, Mag=%0.7E' % (x, y)
        
    '''Signal data tab=========================================================
    '''
    def iterationChangeSignalData(self):
        new_iteration = int(self.spinBoxSignalData.value())
        signal_updated = self.signals[new_iteration]

        self.time = signal_updated[5] #Sampled time array
        self.discrete = signal_updated[6] #Digital samples
        self.seq_length = len(self.discrete) #Length of data sequence (number of bits/symbols)
        self.units = np.linspace(1, self.seq_length, self.seq_length, dtype = 'int') #Unit interval
        
        self.samples_per_bit = int(round(self.sample_rate/signal_updated[3]))
        self.samples_per_symbol = int(round(self.sample_rate/signal_updated[2]))      
        
        self.discrete_time = []
        for sym in range(0,self.seq_length):
            i = 0
            while i < int(self.samples_per_symbol):
                self.discrete_time.append(self.discrete[sym])
                i += 1
                
        self.updateSignalData()
        
    def updateSignalData(self):
        self.tabData.setCurrentWidget(self.tab_signal)
        self.signalBrowser.clear()
        
        #Signal data (base data)
        self.font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
        self.font_normal = QtGui.QFont("Arial", 8, QtGui.QFont.Normal)
        self.signalBrowser.setCurrentFont(self.font_bold)
        self.signalBrowser.setTextColor(QtGui.QColor('#007900'))
        i = int(self.spinBoxSignalData.value())
        self.signalBrowser.append('Signal data (digital) - Iteration '+str(i))
        self.signalBrowser.setCurrentFont(self.font_normal)
        self.signalBrowser.setTextColor(QtGui.QColor('#000000'))
        
        #Signal data title
        self.signalBrowser.setCurrentFont(self.font_bold)
        if self.radioButtonUnitSignalData.isChecked() == 1:
            self.signalBrowser.append('Signal data (symbol index, discrete value ):')
        else:
            self.signalBrowser.append('Signal data (index, time (s), discrete value ):')
        self.signalBrowser.setCurrentFont(self.font_normal)
        
        #Adjust for new index range (if required)
        if self.radioButtonUnitSignalData.isChecked() == 1:
            self.totalSamplesSignalData.setText(str(format(self.seq_length, 'n')))
            self.minIndexSignalData.setText(str(1))
            self.maxIndexSignalData.setText(str(format(self.seq_length, 'n')))
        else:
            self.totalSamplesSignalData.setText(str(format(self.total_samples, 'n')))
            self.minIndexSignalData.setText(str(1))
            self.maxIndexSignalData.setText(str(format(self.total_samples, 'n')))
         
        self.start_index = int(self.minIndexSignalData.text())
        self.end_index = int(self.maxIndexSignalData.text()) + 1     
        index_array = np.arange(self.start_index, self.end_index, 1)
        array_size = self.end_index - self.start_index
        
        #Prepare structured array for string output to text browser
        if self.radioButtonUnitSignalData.isChecked() == 1:
            data = np.zeros(array_size, dtype={'names':('index', 'y'),
                                               'formats':('i4', 'i4')})
        else:
            data = np.zeros(array_size, dtype={'names':('index', 'x', 'y'),
                                               'formats':('i4', 'f8', 'i4')})
        data['index'] = index_array
        
        if self.radioButtonSigTime.isChecked() == 1:
            if self.radioButtonUnitSignalData.isChecked() == 1:
                data['y'] = self.discrete[self.start_index-1:self.end_index-1]
            else:
                data['x'] = self.time[self.start_index-1:self.end_index-1]
                data['y'] = self.discrete_time[self.start_index-1:self.end_index-1]
        else:
            pass
#            data['x'] = self.frq[self.start_index-1:self.end_index-1]
#            if self.radioButtonComplexSignalData.isChecked() == 1:
#                data['y'] = self.Y[self.start_index-1:self.end_index-1]
#            else:
#                data['y1'] = np.abs(self.Y[self.start_index-1:self.end_index-1])
#                data['y2'] = np.angle(self.Y[self.start_index-1:self.end_index-1])
        
        self.linewidth = 60
        if self.linewidthSignalData.text():
            self.linewidth = int(self.linewidthSignalData.text())

        self.signalBrowser.append(np.array2string(data, max_line_width = self.linewidth))
        
        cursor = self.signalBrowser.textCursor()
        cursor.setPosition(0);
        self.signalBrowser.setTextCursor(cursor);
        
    '''Close event====================================================================='''
    def closeEvent(self, event):
        plt.close(self.figure)
        plt.close(self.figure_freq)
        
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
