"""
SystemLab project file
QPSK Design
Version 1.0 3 Apr 2018 (Marc Verreault)
"""


# Simulation settings
# NOTE: Time window and sampling rate are defined from the application window
# The symbol rate can be locally defined or controlled from the application/project
# settings
bit_rate = 10e9
sym_per_bit = 2
symbol_rate = 5e9
order = 2
sig_voltage = 1

carrier_freq = 5e9 #Hz

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
recovered_sig_dict_i = None
recovered_sig_dict_q = None
evm_results_per = None
evm_results_db = None