"""
Parameter help file for PIN_APD_Model (Version 3.0 - 20.01.r3 13-Jul-20)

References:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication
Systems and Networks (Artech House, 2013, Norwood, MA, USA). Kindle Edition.

"""
# To vary the width of the tooltip pop-up, an html table format is used
# Source: https://stackoverflow.com/questions/17221621/how-to-set-qt-tooltip-width
# Accessed 22 May 2020
# Special symbols: https://www.w3schools.com/charsets/ref_html_entities_4.asp

par_dict = {}

table_start = "<table width='300'><tr><td width='300'>"
text_start = "<tr><td width='300'>"
text_end = "</td></tr></table>"

# Optical regime
par_title = '<b>Optical regime</b></td></tr>'
par_text = ('<p>When set to <b>Incoherent</b>, the intensity of each input optical field ' +
            'is independently calculated and converted to a current. The currents are then added ' +
            'to provide the total input signal current</p>' +
            '<p>When set to <b>Coherent</b> the carrier frequencies are applied to the field ' +
            'envelopes and linearly superimposed to capture beating/interference effects. The total current '
            'is then calculated from the relation:<br><i>Resp&times;[E1 + E2 + ...]&times;conj[E1 + E2 + ...]</i></p>')
par_dict['Optical regime'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Detection model
par_title = '<b>Detection model</b></td></tr>'
par_text = ('<b>PIN</b>: Models a p-i-n photodetector.<br>' +
            '<b>APD</b>: Models an avalanche photodetector.')
par_dict['Detection model'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Responsivity model
par_title = '<b>Responsivity model</b></td></tr>'
par_text = ('<p>When set to <b>Direct</b>, responsivity is directly obtained from the ' +
            '<b>Responsivity</b> parameter.</p>' +
            '<p>When set to <b>QE</b>, responsivity is calculated ' + 
            'from:<br> <i>r = QE&times;q/h&times;frq</i></p>')
par_dict['Responsivity model'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Quantum efficiency
par_title = '<b>Quantum efficiency</b></td></tr>'
par_text = ('Used to calculate responsivity when <b>Responsivity model</b> is set to <b>QE</b>.')
par_dict['Quantum efficiency'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Responsivity
par_title = '<b>Responsivity</b></td></tr>'
par_text = ('Used to calculate responsivity when <b>Responsivity model</b> is set to <b>Direct</b>')
par_dict['Responsivity'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Dark current
par_title = '<b>Dark current</b></td></tr>'
par_text = ('Dark current parameter for the photodetector.')
par_dict['Dark current'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Receiver electrical bandwidth
par_title = '<b>Receiver electrical bandwidth (RBW)</b></td></tr>'
par_text = ('Effective electrical bandwidth of PIN/APD. Used when calculating ' +
             'the thermal and shot noise contributions of the photodetector.')
par_dict['Receiver electrical bandwidth'] = (table_start + par_title + text_start
                                        + par_text + text_end)                                      
                                                                             
# Q target
par_title = "<b>Q target</b></td></tr>"
par_text = ('The Q target value is used to calculate the optical sensitivity needed to meet a BER target.<br> ' +
             'Note: The sensitivity calculation is informative and does not affect the noise ' +
             'settings of the PIN/APD.')
par_dict['Q target'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Avalanche gain (M)
par_title = "<b>Avalanche gain (M)</b></td></tr>"
par_text = ('Gain (M) applied to the input responsivity when the <b>APD</b> model is selected.')
par_dict['Avalanche gain (M)'] = (table_start + par_title + text_start
                                        + par_text + text_end)   

# Excess noise factor model
par_title = "<b>Excess noise factor model</b></td></tr>"
par_text = ('Model to use in calculating the excess noise factor.')
par_dict['Excess noise factor model'] = (table_start + par_title + text_start
                                        + par_text + text_end)                                         

                                        
# Noise coefficient (x)
par_title = "<b>Noise coefficient (x)</b></td></tr>"
par_text = ('When set to <b>Noise coeff.</b> the excess noise factor is calculated ' +
            'as follows:<br><i>k<sup>x</sup></i>')
par_dict['Noise coefficient (x)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Ionization coefficient (k)
par_title = "<b>Ionization coefficient (k)</b></td></tr>"
par_text = ('When set to <b>Ionization coeff.</b> the excess noise factor is calculated ' +
            'as follows:<br><i>k&times;M + (1 - k)&times;(2 - 1/M)</i>')
par_dict['Ionization coefficient (k)'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Thermal noise (ON)
par_title = "<b>Thermal noise (ON)</b></td></tr>"
par_text = ('<p>When checked, the thermal noise contribution of the photodetector ' +
            'is added to the input electrical noise current.</p>' +
            '<p><b>Important:</b> If the TIA-LA component is included with the receiver model, ' +
            'the thermal noise calculation will be based on the input referred noise current ' +
            'specification of the TIA. In this case, the PIN/APD thermal noise model should be disabled.</p>')
par_dict['Thermal noise (ON)'] = (table_start + par_title + text_start
                                        + par_text + text_end)                                              
                                        
# Thermal noise model
par_title = "<b>Thermal noise model</b></td></tr>"
par_text = ('<p>When set to <b>Load resistance</b> the thermal noise is calculated as follows:<br>' +
            '<i>thermal_noise_variance = RBW&times;4&times;k&times;T&frasl; R_load</i></p>' +
            '<p>When set to <b>PSD</b> the thermal noise is calculated as follows:<br>' +
            '<i>thermal_noise_variance = RBW&times;PSD_thermal</i></p>' )
par_dict['Thermal noise model'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Thermal noise PSD
par_title = "<b>Thermal noise PSD (PSD_thermal)</b></td></tr>"
par_text = ('Power spectral density definition for thermal noise. Used when <b>Thermal noise model</b> ' +
            'is set to <b>PSD</b>.')
par_dict['Thermal noise PSD'] = (table_start + par_title + text_start
                                        + par_text + text_end)    

# Noise temperature (T)
par_title = "<b>Noise temperature (K)</b></td></tr>"
par_text = ('Noise temperature of load resistance. Used when <b>Thermal noise model</b> ' +
            'is set to <b>Load resistance</b>.')
par_dict['Noise temperature'] = (table_start + par_title + text_start
                                        + par_text + text_end) 

# Load resistance (R_load)
par_title = "<b>Load resistance (R_load)</b></td></tr>"
par_text = ('Load resistance of detection circuit. Used when <b>Thermal noise model</b> ' +
            'is set to <b>Load resistance</b>.')
par_dict['Load resistance'] = (table_start + par_title + text_start
                                        + par_text + text_end) 

# Shot noise (ON)
par_title = "<b>Shot noise (ON)</b></td></tr>"
par_text = ('When checked, the shot noise contribution of the photodetector ' +
            'will be added to the input electrical noise current.')
par_dict['Shot noise (ON)'] = (table_start + par_title + text_start
                                        + par_text + text_end)    

# Shot noise model
par_title = "<b>Shot noise model</b></td></tr>"
par_text = ('<p>When set to <b>Gaussian</b> the shot noise is calculated as follows:<br>' +
            '<i>shot_noise_variance = RBW&times;2&times;k&times;signal_current</i></p>' +           
            '<p>When set to <b>Poisson</b> the shot noise is calculated as follows:<br>' +
            '<i>avg_photons = signal_current&times;delta_t/q<br>' +
            'shot_current_rms = (q/delta_t)&times;poisson_dist(avg_photons)</i><br>' + 
            'where <i>delta_t</i> is the <i>sampling_period</i>.')
par_dict['Shot noise model'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Include optical noise
par_title = "<b>Include optical noise</b></td></tr>"
par_text = ('When checked, optical noise (ASE) will be included in the detection model.')
par_dict['Include optical noise'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Optical noise model
par_title = "<b>Optical noise model</b></td></tr>"
par_text = ('Set to <b>Analytical</b> by default. The Signal-ASE and ASE-ASE beating terms will be ' +
             'calculated based on the received optical noise.')
par_dict['Optical noise model'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                
# Optical filter bandwidth
par_title = "<b>Optical filter bandwidth</b></td></tr>"
par_text = ('This parameter is used to define the optical noise bandwidth for calculating the OSNR, Q(OSNR), ' +
            'and the ASE-ASE beat noise component.')
par_dict['Optical filter bandwidth'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Add noise current to signal
par_title = "<b>Add noise current to signal</b></td></tr>"
par_text = ('<p>When checked, the calculated PIN/APD noise data is added to the sampled ' +
            'signal data and the noise data is set to zero.</p>' +
            '<p>When not checked, the signal and noise data are kept in separate arrays.</p>')
par_dict['Add noise current to signal'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Display PIN/APD noise data
par_title = "<b>Display PIN/APD noise data</b></td></tr>"
par_text = ('When checked, results for thermal and shot noise statistics will be calculated and displayed.')
par_dict['Display PIN/APD noise data'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Display optical (ASE) noise data
par_title = "<b>Display optical (ASE) noise data</b></td></tr>"
par_text = ('When checked, results for ASE noise statistics will be calculated and displayed.')
par_dict['Display optical (ASE) noise data'] = (table_start + par_title + text_start
                                        + par_text + text_end)