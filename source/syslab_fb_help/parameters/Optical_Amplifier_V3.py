"""
Parameter help file for Optical Amplifier (Version 3.0 - 20.01.r3 14-Jun-20)

References:
1) Cvijetic, M., and Djordjevic, Ivan B.; Advanced Optical Communication
Systems and Networks (Artech House, 2013, Norwood, MA, USA). Kindle Edition.
2) Section 5: Optical Amplifiers, Course Notes (authors unknown)
Source: http://www2.engr.arizona.edu/~ece487/opamp1.pdf 
(accessed 17 Apr 2019)
3) Introduction to Optical Amplifiers (authors unknown)
Source: http://opti500.cian-erc.org/opti500/pdf/sm/Introduction%
20to%20Optical%20Ampflifers%20Module.pdf
(accessed 14 June 2020)

"""
# To vary the width of the tooltip pop-up, an html table format is used
# Source: https://stackoverflow.com/questions/17221621/how-to-set-qt-tooltip-width
# Accessed 22 May 2020

par_dict = {}

table_start = "<table width='200'><tr><td width='200'>"
text_start = "<tr><td width='200'>"
text_end = "</td></tr></table>"

# Small signal gain
par_title = "<b>Small signal gain</b></td></tr>"
par_text = ("Amplifier gain under linear operation (no saturation).")
par_dict['Small signal gain'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Saturated output pwr
par_title = "<b>Saturated output pwr</b></td></tr>"
par_text = "Used to define point where gain compresses by 3 dB."
par_dict['Saturated output pwr'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Noise Figure
par_title = "<b>Noise Figure</b></td></tr>"
par_text = "Optical noise figure of amplifier. Used to set ASE power spectral density."
par_dict['Noise Figure'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Amplifier bandwidth
par_title = "<b>Amplifier bandwidth</b></td></tr>"
par_text = ("Bandwidth of amplifier where gain and ASE is applied. Channels outside" +
                      " this range will have a gain of 1 and no ASE noise will be added.")
par_dict['Amplifier bandwidth'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Center frequency
par_title = "<b>Center frequency</b></td></tr>"
par_text = ("Center frequency of amplifier bandwidth window.")
par_dict['Center frequency'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
# Operating mode
par_title = "<b>Operating mode</b></td></tr>"
par_text = ("Used to adjust gain or output power of amplifier. If set to <b>Gain " +
                     "control</b>, the total amplifier gain will be set to the value of the " +
                     "<b>Gain setting</b> parameter. " +
                     "If set to <b>Power control</b>, the gain will be set to the total output target " +
                     "of the <b>Power setting</b> parameter. In both cases the setting will only be met if the " +
                     "amplifier is not saturated.")
par_dict['Operating mode'] = (table_start + par_title + text_start
                                        + par_text + text_end)
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        