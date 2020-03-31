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
bit_rate = 100e9
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
sym_ref_i = None
sym_ref_q = None

#Graphs for BER/SER versus SNRpersym
simulation_analyzer = None #Global instantiation for IterationsAnalyzer class
ber = []
ber_th = []
ser = []
ser_th = []
photons_per_bit = []
snr_per_sym = []

#Constellation viewer
constellation = None #Global instantiation for SignalSpaceViewer class
decision_samples_dict_i = None
decision_samples_dict_q = None
recovered_sig_dict_i = None
recovered_sig_dict_q = None
evm_results_per = None
evm_results_db = None

#Constallation views for DSP
constellation_dsp = None
samples_dict_i = None
samples_dict_q = None
dsp_recovered_sig_dict_i = None
dsp_recovered_sig_dict_q = None
dsp_evm_results_per = None
dsp_evm_results_db = None

# Phase error estimate graph
ph_error_data = None