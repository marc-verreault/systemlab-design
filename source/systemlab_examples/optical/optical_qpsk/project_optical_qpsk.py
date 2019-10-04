"""
SystemLab project file
Optical QPSK transmitter design
Version 1.0 20 Jul 2018 (Marc Verreault)
"""
import numpy as np

# Simulation settings
# NOTE: Time window and sampling rate are defined from the application window
# The symbol rate can be locally defined or controlled from the application/project
# settings
bit_rate = 10e9
modulation_type = 'QPSK' #QPSK/8QAM/16QAM/64QAM

if modulation_type == 'QPSK':
    N = 2
    symbol_rate = bit_rate/N
    I = [-1, 1]
    Q = [-1, 1]
elif modulation_type == '8QAM':
    N = 3
    symbol_rate = bit_rate/N
    I_inner = [-1, 1]
    Q_inner = [-1, 1] 
    a = (1 + np.sqrt(3))/np.sqrt(2)
    I_outer = [-a, a] #Needs to be rotated +45 deg
    Q_outer = [-a, a] #Needs to be rotated +45 deg
elif modulation_type == '16QAM':
    N = 4
    symbol_rate = bit_rate/N
    I = [-3, -1, 1, 3]
    Q = [-3, -1, 1, 3]
else: #64QAM
    N = 6
    symbol_rate = bit_rate/N
    I = [-7, -5, -3, -1, 1, 3, 5, 7]
    Q = [-7, -5, -3, -1, 1, 3, 5, 7]  
    

# Symbol sequences used for calculating SER
symbol_seq_odd = None
sym_seq_even = None


#Graphs for BER/SER versus SNRpersym
simulation_analyzer = None #Global instantiation for IterationsAnalyzer class
ber = []
ber_th = []
ser = []
ser_th = []
snr_per_sym = []
snr_per_bit = []

#Constellation viewer
constellation = None #Global instantiation for SignalSpaceViewer class
decision_samples_dict_i = None
decision_samples_dict_q = None