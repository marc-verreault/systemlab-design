"""
Parameter help file for CW Laser (Version 3.0 - 20.01.r3 14-Jun-20)

"""
# To vary the width of the tooltip pop-up, an html table format is used
# Source: https://stackoverflow.com/questions/17221621/how-to-set-qt-tooltip-width
# Accessed 22 May 2020

par_dict = {}

table_start = "<table width='300'><tr><td width='300'>"
text_start = "<tr><td width='300'>"
text_end = "</td></tr></table>"

# Wave key
par_title = "<b>Wave key</b></td></tr>"
par_text = ('Wave channel identification code (integer). Use different codes to ' +
            'represent different wavelength carriers.')
par_dict['Wave key'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Optical wavelength unit
par_title = "<b>Optical wavelength unit</b></td></tr>"
par_text = ("Wavelength units to be used in defining center frequency of"
            + " optical channel. Units are in 'nm' or 'THz'.")
par_dict['Optical wavelength unit'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Wavelength/frequency
par_title = "<b>Optical wavelength/frequency</b></td></tr>"
par_text = "Center wavelength/frequency setting of the CW laser."
par_dict['Wavelength/frequency'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Optical power unit
par_title = "<b>Optical power unit</b></td></tr>"
par_text = "Units to be used in defining the output optical power (mW or dBm)."
par_dict['Optical power unit'] = (table_start + par_title + text_start + 
                             par_text + text_end)

# Optical power
par_title = "<b>Optical power</b></td></tr>"
par_text = "Output power setting of CW laser. Defined in milliWatts (mW) or dBm."
par_dict['Optical power'] = (table_start + par_title + text_start + 
                             par_text + text_end)

# Laser linewidth
par_title = "<b>Laser linewidth</b></td></tr>"
par_text = ('The laser linewidth specification of the laser (in MHz). ' +
            'Represents the spectral width (FWHM) of the laser due to phase noise. ' +
            'The phase noise is based on the random walk noise model with standard deviation of:<br><br>' +
            '<i>&sigma;<sub>phase</sub> = sqrt(2&times;&pi;&times;linewidth)<br>' +
            'phase_walk = normal_dist(&sigma;<sub>phase</sub>)&times;sqrt(sample_period)</i>')
par_dict['Laser linewidth'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Optical phase
par_title = "<b>Optical phase</b></td></tr>"
par_text = ('Initial phase setting of optical field envelope.')
par_dict['Optical phase'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Reference bandwidth
par_title = "<b>Reference bandwidth (RBW)</b></td></tr>"
par_text = ('Reference bandwidth (linked to the receiver) to be used in calculating the ' +
            'time-domain RIN.')
par_dict['Reference bandwidth'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# RIN
par_title = "<b>RIN</b></td></tr>"
par_text = ('Relative intensity noise (RIN) specification of the laser.')
par_dict['RIN'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Include RIN in noise model
par_title = "<b>Include RIN in noise model</b></td></tr>"
par_text = ('When checked, the RIN contribution of the laser ' +
            'will be added to the optical noise field envelope. The RIN contribution ' +
            'is calculated as follows:<br>' +
            '<i>power<sub>RIN</sub> = RIN<sub>linear</sub>&times;RBW&times;(power<sub>sig</sub>)<sup>2</sup></i>')
par_dict['Include RIN in noise model'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Add RIN to time domain signal
par_title = "<b>Add RIN to time domain signal</b></td></tr>"
par_text = ('<p>When checked, the RIN optical noise field envelope is added to the optical signal ' +
            'field envelope.</p>' +
            '<p>When not checked, the signal and noise field envelopes are kept in separate arrays.</p>')
par_dict['Add RIN to time domain signal'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Polarization (azimuth)
par_title = "<b>Polarization (azimuth)</b></td></tr>"
par_text = ('Orientation of the polarization ellipse (0 to 90 deg)')
par_dict['Polarization (azimuth)'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Polarization (ellipticity)
par_title = "<b>Polarization (ellipticity)</b></td></tr>"
par_text = ('Ellipticity angle (-45 to 45 deg). Set to 0 for linear polarization')
par_dict['Polarization (ellipticity)'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Complex field format
par_title = "<b>Complex field format</b></td></tr>"
par_text = ('<p>When set to Exy, the optical field polarization state is represented with ' +
            'one array and X/Y polarization data are extracted using the Jones vector.</p>' +
            '<p>When set to Ex-Ey, the optical field polarization states are represented with ' +
            'two separate arrays. This format should be used when, for example, modeling polarization-multiplexed ' +
            'communication systems.</p>')
par_dict['Complex field format'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Power spectral density
par_title = "<b>Power spectral density</b></td></tr>"
par_text = ('Power spectral density (representing optical noise such as ' +
            'amplified spontaneous emission) to be applied to each frequency group/sub-band.')
par_dict['Power spectral density'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Noise groups (total)
par_title = "<b>Noise groups (total)</b></td></tr>"
par_text = ('Number of noise groups/sub-bands to be created.')
par_dict['Noise groups (total)'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Start frequency
par_title = "<b>Start frequency</b></td></tr>"
par_text = ('Start frequency (Hz) for the first frequency sub-band. This ' +
            'frequency represents the center position of the sub-band.')
par_dict['Start frequency'] = (table_start + par_title + text_start 
                               + par_text + text_end)
                               
# End frequency
par_title = "<b>End frequency</b></td></tr>"
par_text = ('End frequency (Hz) for the last frequency sub-band. This ' +
            'frequency represents the center position of the sub-band.')
par_dict['End frequency'] = (table_start + par_title + text_start 
                               + par_text + text_end)
                               
# Add ASE to time domain noise
par_title = "<b>Add ASE to time domain noise</b></td></tr>"
par_text = ('<p>When checked, all frequency noise groups that overlap with the optical ' +
            'field sampling bandwidth will be converted to a time-domain noise signal. ' +
            'The time-domain noise (Gaussian white noise) is calculated as follows:<br><br>' +
            '<i>&sigma;<sub>ase</sub> = sqrt(0.5&times;pwr<sub>ase</sub>)</i> where,<br>' +
            '<i>pwr<sub>ase</sub> = &sum;psd_array[i]*noise_group_bandwidth[i]</i></p>' +
            '<p>Note: The noise power is divided by 2 as noise is allocated ' +
            'between the real and imaginary parts of the complex noise field.</p>')
par_dict['Add ASE to time domain noise'] = (table_start + par_title + text_start 
                               + par_text + text_end)
                               
# Add ASE to time domain signal
par_title = "<b>Add ASE to time domain signal</b></td></tr>"
par_text = ('<p>When checked, the time-domain optical noise data is added to the optical field ' +
            'envelope.</p>' +
            '<p>When not checked, the signal and noise field data are kept in separate arrays.</p>')
par_dict['Add ASE to time domain signal'] = (table_start + par_title + text_start 
                               + par_text + text_end)