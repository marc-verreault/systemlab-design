"""
Parameter help file for Transimpedance_Limiting_Amplifier model (Version 1.0 - 20.01.r3 13-Jul-20)

"""
# To vary the width of the tooltip pop-up, an html table format is used
# Source: https://stackoverflow.com/questions/17221621/how-to-set-qt-tooltip-width
# Accessed 22 May 2020
# Source for adding special symbols: https://www.w3schools.com/charsets/ref_utf_greek.asp

par_dict = {}

table_start = "<table width='300'><tr><td width='300'>"
text_start = "<tr><td width='300'>"
text_end = "</td></tr></table>"

# Transimpedance gain (Z)
par_title = '<b>Transimpedance gain (Z)</b></td></tr>'
par_text = ('Linear gain setting of transimpedance amplifier, applied to input ' +
            'signal and noise arrays.')
par_dict['Transimpedance gain (Z)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Noise definition (TIA)
par_title = '<b>Noise definition (TIA)</b></td></tr>'
par_text = ('<p>When set to <b>Input noise current</b>, the <b>Input referred noise current</b> ' +
            'parameter is used to calculate the equivalent output voltage noise of the TIA.</p>' +
            '<p>When set to <b>Input noise density</b>, the <b>Input noise current density</b> ' +
            'and <b>Effective noise bandwidth (TIA)</b> parameters are used to calculate the ' +
            'equivalent output voltage noise of the TIA.</p>')
par_dict['Noise definition (TIA)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Input referred noise current
par_title = '<b>Input referred noise current</b></td></tr>'
par_text = ('<p>Used when <b>Noise definition</b> is set to <b>Input noise current</b>. ' +
            'The equivalent output voltage noise is calculated as follows:<br>' +
            '<i>noise_voltage_variance = (i_noise_referred*Z)^2</i></p>')
par_dict['Input referred noise current'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Effective noise bandwidth (TIA)
par_title = '<b>Effective noise bandwidth (TIA) - ENB)</b></td></tr>'
par_text = ('Used to calculate input referred noise current when <b>Noise definition</b> is set ' +
            'to <b>Input noise density</b>.')
par_dict['Effective noise bandwidth (TIA)'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Input noise current density
par_title = '<b>Input noise current density</b></td></tr>'
par_text = ('Used to calculate input referred noise current when <b>Noise definition</b> is set ' +
            'to <b>Input noise density</b>. Input referred noise current is calculated as follows:<br> ' +
            '<i>i_noise_referred = ENB*Input_noise_density</i>.')
par_dict['Input noise current density'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Low-pass filter
par_title = '<b>Low-pass filter</b></td></tr>'
par_text = ('When set to <b>Low-pass (n=1)</b> or <b>Low-pass (n=2)</b>, the amplified signal ' +
            'and noise arrays will be filtered based on the parameters <b>Cut-off frequency</b> ' +
            'and <b>Filter Q-factor</b>. Note: The Q-factor parameter only applies to the second order (n=2) filter.')
par_dict['Low-pass filter'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Cut-off frequency
par_title = '<b>Cut-off frequency</b></td></tr>'
par_text = ('The 3 dB cut-off frequency of the low pass filter.')
par_dict['Cut-off frequency'] = (table_start + par_title + text_start
                                        + par_text + text_end)                                      
                                                                             
# Filter Q-factor (n=2)
par_title = "<b>Filter Q-factor (n=2)</b></td></tr>"
par_text = ('The Q-factor (resonance) of the second order filter.')
par_dict['Filter Q-factor (n=2)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Filter input noise array
par_title = "<b>Filter input noise array</b></td></tr>"
par_text = ('When checked, the low-pass filter transfer function will be ' + 
            'applied to the input noise array. If the upstream noise data has been ' +
            'calculated based on a defined receiver bandwidth, this parameter ' +
            'should be left un-checked.')
par_dict['Filter input noise array'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Build transfer function curves
par_title = "<b>Build transfer function curves</b></td></tr>"
par_text = ('When selected, filter transfer function curves for ' +
            'amplitude gain, phase delay and group delay are displayed.')
par_dict['Build transfer function curves'] = (table_start + par_title + text_start
                                        + par_text + text_end)                                          
                                        
# Signal-noise distribution
par_title = "<b>Signal-noise distribution</b></td></tr>"
par_text = ('When selected, an histogram of the signal + noise distribution of the TIA output ' +
            'eye is plotted.')
par_dict['Signal-noise distribution'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Number of histogram bins
par_title = "<b>Number of histogram bins</b></td></tr>"
par_text = ('Sets the number of histograms (resolution) to be used in building the signal + noise distribution.')
par_dict['Number of histogram bins'] = (table_start + par_title + text_start
                                        + par_text + text_end)                                              
                                        
# Enable limiting amplifier
par_title = "<b>Enable limiting amplifier</b></td></tr>"
par_text = ('<p>When checked, the limiting amplifier function of the TIA-LA is activated. When not checked, ' +
            'only the transimpedance function is modelled.')
par_dict['Enable limiting amplifier'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Differential output voltage swing (Vpp)
par_title = "<b>Differential output voltage swing (Vpp)</b></td></tr>"
par_text = ('Defines the minimum (-Vpp/2) and maximum (+Vpp/2) output voltage settings for the LA.')
par_dict['Differential output voltage swing'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Noise definition (LA)
par_title = "<b>Noise definition (LA)</b></td></tr>"
par_text = ('<p>When set to <b>Input sensitivity</b>, the <b>Input sensitivity</b> ' +
            'parameter is used to calculate the equivalent output voltage noise of the LA.</p>' +
            '<p>When set to <b>Referred noise density</b>, the <b>Input referred noise voltage</b> ' +
            'and <b>Effective noise bandwidth (LA)</b> parameters are used to calculate the ' +
            'equivalent output voltage noise of the LA.</p>')
par_dict['Noise definition (LA)'] = (table_start + par_title + text_start
                                        + par_text + text_end)    

# Input sensitivity (v_la)
par_title = "<b>Input sensitivity (v_la)</b></td></tr>"
par_text = ('Used when <b>Noise definition (LA)</b> is set to <b>Input sensitivity</b>. ' +
            'The limiting amplifier input referred noise is calculated as follows:<br>' +
            '<i>n_la = v_la*2/q_target</i><br>' + 
            'The equivalent output voltage noise is then calculated from:<br>' +
            '<i>v_la_rms = normal_dist(n_la*avg_linear_gain_la)</i>.')
par_dict['Input sensitivity'] = (table_start + par_title + text_start
                                        + par_text + text_end) 

# Effective noise bandwidth (LA)
par_title = "<b>Effective noise bandwidth (LA)</b></td></tr>"
par_text = ('Used to calculate the input sensitvity when <b>Noise definition (LA)</b> is set ' +
            'to <b>Referred noise density</b>.')
par_dict['Effective noise bandwidth (LA)'] = (table_start + par_title + text_start
                                        + par_text + text_end) 

# Input referred noise voltage
par_title = "<b>Input referred noise voltage</b></td></tr>"
par_text = ('Used to calculate the input sensitivity when <b>Noise definition (LA)</b> is set ' +
            'to <b>Referred noise density</b>. The input sensitivity is calculated as follows:<br>' +
            '<i>v_la = noise_voltage*sqrt(enb_la)</i>')
par_dict['Input referred noise voltage'] = (table_start + par_title + text_start
                                        + par_text + text_end)    

# Differential small signal gain
par_title = "<b>Differential small signal gain</b></td></tr>"
par_text = ('The linear voltage gain to be applied to the input signal and noise arrays. If the ' +
            'amplified signal exceeds the min/max voltage settings of the LA, the applied gain will be compressed ' +
            'to maintain a constant differential output voltage swing.')
par_dict['Differential small signal gain'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Transition data points
par_title = "<b>Transition data points</b></td></tr>"
par_text = ('The time data points used to specify the limiting amplifier rise/fall times.')
par_dict['Transition data points'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Transition time
par_title = "<b>Transition time</b></td></tr>"
par_text = ('The rise/fall time specification for the limiting amplifier. The signal response time ' +
             'is modified using a frequency-domain Gaussian transfer function.')
par_dict['Transition time'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Jitter (deterministic - PP)
par_title = "<b>Jitter (deterministic - PP)</b></td></tr>"
par_text = ('<p>The deterministic jitter model is based on the Dual Dirac assumption. For each ' +
            'symbol period, a random time shift of either <i>-j_det_pp/2</i> or <i>+j_det_pp/2</i> is applied ' +
            'to all sampled signals within the symbol period.</p>')
par_dict['Jitter (deterministic)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Jitter (random - RMS)
par_title = "<b>Jitter (random - RMS)</b></td></tr>"
par_text = ('Adds a randomly distributed time shift on top of the deterministic jitter ' +
            'time shift (<i>&mu; = jitter_det_shift, &sigma; = jitter_rms</i>).')
par_dict['Jitter (random)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Add noise array to signal array
par_title = "<b>Add noise array to signal array</b></td></tr>"
par_text = ('<p>When checked, the calculated TIA/LA noise data is added to the sampled ' +
            'signal data and the noise data is set to zero.</p>' +
            '<p>When not checked, the signal and noise data are kept in separate arrays.</p>')
par_dict['Add noise array to signal array'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Q target (link model)
par_title = "<b>Q target (link model)</b></td></tr>"
par_text = ('The Q target value is used to calculate the optical sensitivity needed to meet a BER target.<br> ' +
            'Note: The sensitivity calculation is informative and does not affect the noise ' +
            'settings of the TIA/LA.')
par_dict['Q target (link model)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# PIN/APD responsivity
par_title = "<b>PIN/APD responsivity</b></td></tr>"
par_text = ('The assumed value of the PIN/APD responsivity to be used in calculating the optical sensitivity.')
par_dict['PIN/APD responsivity'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Extinction ratio (linear)
par_title = "<b>Extinction ratio (linear)</b></td></tr>"
par_text = ('The assumed value of the received signal extinction ratio to be used in calculating the optical sensitivity.')
par_dict['Extinction ratio (linear)'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# ISI penalty
par_title = "<b>ISI penalty</b></td></tr>"
par_text = ('The assumed value of the intersymbol inteference (ISI) penalty to be used in calculating the optical sensitivity.')
par_dict['ISI penalty'] = (table_start + par_title + text_start
                                        + par_text + text_end)