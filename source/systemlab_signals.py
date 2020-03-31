'''
    SystemLab-Design Version 20.01
    Primary author: Marc Verreault
    E-mail: marc.verreault@systemlabdesign.com
    Copyright © 2019-2020 SystemLab Inc. All rights reserved.
    
    LICENSE NOTICE=========================================================  
    This file is part of SystemLab-Design 20.01.
    
    SystemLab-Design 20.01 is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    SystemLab-Design 19.02 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SystemLab-Design 20.01.  If not, see <https://www.gnu.org/licenses/>.    
    =======================================================================
    
    ABOUT THIS MODULE
    Name: systemlab_signals
    SystemLab module for signal classes:
    SignalAnalogElectrical, SignalAnalogOpticalCollection, SignalAnalogOptical,
    SignalDigital, SignalGeneric, SignalGeneric2, SignalGeneric3 
'''

class SignalAnalogElectrical():
    
    def __init__(self, portID, signal_type, carrier, sample_rate, time_array, amplitude_array, noise_array):
        self.portID = portID
        self.signal_type = signal_type
        self.sample_rate = sample_rate
        self.time_array = time_array
        self.amplitude_array = amplitude_array
        self.noise_array = noise_array
        self.carrier = carrier
         
    def __repr__(self): #Return string method for print(object)
        return 'Port ID: ' + str(self.portID) + ' Signal type: ' + self.signal_type + '\n' \
        + 'Sample rate (Hz): ' + str(self.sample_rate) + ' Carrier (Hz): ' + str(self.carrier) + '\n' \
        + 'Time array: ' + str(self.time_array) + '\n' \
        + 'Amp array: ' + str(self.amplitude_array) + '\n' \
        + 'Noise array: ' + str(self.noise_array)
        
class SignalAnalogOpticalCollection():
    
    def __init__(self, portID, signal_type, sample_rate, time_array, psd_array):
        self.portID = portID
        self.signal_type = signal_type
        self.sample_rate = sample_rate
        self.time_array = time_array 
        self.psd_array = psd_array #MV (19.02.r2 8-Sep-19) Moved from SignalAnalogOptical 
        self.wave_channel_group = {} #MV (19.02.r2 8-Sep-19) Renamed from wave_channel_dict 

class SignalAnalogOptical():
    
    def __init__(self, wave_key, wave_channel, jones_vector, envelope_array, noise_array):
        self.wave_key = wave_key
        self.wave_channel = wave_channel
        self.jones_vector = jones_vector
        self.envelope_array = envelope_array
        self.noise_array = noise_array
        #self.psd_array = psd_array
      
#    def __repr__(self): #Return string method for print(object)
#        return ': ' + str(self.portID) + ' Signal type: ' + self.signal_type + '\n' \
#        + 'Wave channel (THz): ' + str(self.wave_channel) + ' Jones matrix: ' + str(self.jones_vector) + '\n' \
#        + 'Sample rate (Hz): ' + str(self.sample_rate) + '\n' \
#        + 'Time array: ' + str(self.time_array) + '\n' \
#        + 'Amp array: ' + str(self.amplitude_array) + '\n' \
#        + 'PSD array: ' + str(self.noise_array)
  
#    def __init__(self, portID, signal_type, wave_key, wave_channel, jones_vector, 
#                 sample_rate, time_array, envelope_array, noise_array, psd_array):
#        self.portID = portID
#        self.signal_type = signal_type
#        self.wave_key = wave_key
#        self.wave_channel = wave_channel
#        self.jones_vector = jones_vector
#        self.sample_rate = sample_rate
#        self.time_array = time_array
#        self.envelope_array = envelope_array
#        self.psd_array = psd_array
#      
#    def __repr__(self): #Return string method for print(object)
#        return 'Port ID: ' + str(self.portID) + ' Signal type: ' + self.signal_type + '\n' \
#        + 'Wave channel (THz): ' + str(self.wave_channel) + ' Jones matrix: ' + str(self.jones_vector) + '\n' \
#        + 'Sample rate (Hz): ' + str(self.sample_rate) + '\n' \
#        + 'Time array: ' + str(self.time_array) + '\n' \
#        + 'Amp array: ' + str(self.amplitude_array) + '\n' \
#        + 'PSD array: ' + str(self.noise_array)
         
class SignalDigital():
    
    def __init__(self, portID, signal_type, symbol_rate, bit_rate, order, time_array, discrete_array):
        self.portID = portID
        self.signal_type = signal_type
        self.symbol_rate = symbol_rate
        self.bit_rate = bit_rate
        self.order = order
        self.time_array = time_array
        self.discrete_array = discrete_array
         
#     def __repr__(self): #Return string method for print(object)
#         return 'Port ID: ' + str(self.portID) + ' Signal type: ' + self.signal_type + '\n' \
#         + 'Sample rate (Hz): ' + str(self.sample_rate) + ' Carrier (Hz): ' + str(self.carrier) + '\n' \
#         + 'Time array: ' + str(self.time_array) + '\n' \
#         + 'Amp array: ' + str(self.amplitude_array)
         
         
class SignalAnalogGeneric():
    
    def __init__(self, portID, signal_type, sample_rate, time_array, amplitude_array):
        self.portID = portID
        self.signal_type = signal_type
        self.sample_rate = sample_rate
        self.time_array = time_array
        self.amplitude_array = amplitude_array
        
class SignalAnalogGeneric2():
    
    def __init__(self, portID, signal_type, sample_rate, time_array, amplitude_array):
        self.portID = portID
        self.signal_type = signal_type
        self.sample_rate = sample_rate
        self.time_array = time_array
        self.amplitude_array = amplitude_array
        
class SignalAnalogGeneric3():
    
    def __init__(self, portID, signal_type, sample_rate, time_array, amplitude_array):
        self.portID = portID
        self.signal_type = signal_type
        self.sample_rate = sample_rate
        self.time_array = time_array
        self.amplitude_array = amplitude_array
         
#    def __repr__(self): #Return string method for print(object)
#        return 'Port ID: ' + str(self.portID) + ' Signal type: ' + self.signal_type + '\n' \
#        + 'Sample rate (Hz): ' + str(self.sample_rate) + ' Carrier (Hz): ' + str(self.carrier) + '\n' \
#        + 'Time array: ' + str(self.time_array) + '\n' \
#        + 'Amp array: ' + str(self.amplitude_array) + '\n' \
#        + 'Noise array: ' + str(self.noise_array)