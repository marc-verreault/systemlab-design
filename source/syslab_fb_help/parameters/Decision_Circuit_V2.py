"""
Parameter help file for Decision Circuit (Version 2.0 - 20.01.r3 3-Aug-20)

"""
# To vary the width of the tooltip pop-up, an html table format is used
# Source: https://stackoverflow.com/questions/17221621/how-to-set-qt-tooltip-width
# Accessed 22 May 2020

par_dict = {}

table_start = "<table width='300'><tr><td width='300'>"
text_start = "<tr><td width='300'>"
text_end = "</td></tr></table>"

# Decision threshold model
par_title = "<b>Decision threshold model</b></td></tr>"
par_text = ('When set to defined, the <b>Decision threshold (defined)</b> parameter ' +
             'will be used to decide between the logic 1 and logic 0 levels. When set ' +
             'to <b>Signal average</b>, the average value of the input sampled signal will be used.')
par_dict['Decision threshold model'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Enable DC block
par_title = "<b>Enable DC block</b></td></tr>"
par_text = ('When checked, the DC component of the input sampled signal will be removed.')
par_dict['Enable DC block'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Normalize
par_title = "<b>Normalize</b></td></tr>"
par_text = ('When checked, the min and max points of the input sampled signal will be set ' +
            'between -1 and 1.')
par_dict['Normalize'] = (table_start + par_title + text_start
                                        + par_text + text_end)

# Decision threshold (defined)
par_title = "<b>Decision threshold (defined)</b></td></tr>"
par_text = ('Defines the y-axis decision point for deciding between logic 0 and logic 1.')
par_dict['Decision threshold (defined)'] = (table_start + par_title + text_start + 
                             par_text + text_end)

# Optimize decision threshold
par_title = "<b>Optimize decision threshold</b></td></tr>"
par_text = ('When checked, the decision point will be adjusted based on the following formula: <br>' +
            '<i>v<sub>th</sub> = (&sigma;<sub>1</sub>&times;&mu;<sub>0</sub> + &sigma;<sub>0</sub>&times;&mu;<sub>1</sub>)' +
            '/(&sigma;<sub>1</sub> + &sigma;<sub>0</sub>)</i>')
par_dict['Optimize decision threshold'] = (table_start + par_title + text_start + 
                             par_text + text_end)

# Decision time
par_title = "<b>Decision time</b></td></tr>"
par_text = ('The time sampling instant at which to  perform the decision. A setting of 0.5 ' +
            'represents the half-way point of the symbol period.')
par_dict['Decision time'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Add noise to signal
par_title = "<b>Add noise to signal</b></td></tr>"
par_text = ('When checked, any data contained in the noise array will be moved to the signal ' +
             ' array. ')
par_dict['Add noise to signal'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Display distribution
par_title = "<b>Display distribution</b></td></tr>"
par_text = ('When checked, the signal + noise distribution profile of the input signal at the time ' +
            'decision will be displayed')
par_dict['Display distribution'] = (table_start + par_title + text_start 
                               + par_text + text_end)

# Number of histogram bins
par_title = "<b>Number of histogram bins</b></td></tr>"
par_text = ('Defines the number of histograms to plot when mapping the signal + noise distribution.')
par_dict['Number of histogram bins'] = (table_start + par_title + text_start 
                               + par_text + text_end)