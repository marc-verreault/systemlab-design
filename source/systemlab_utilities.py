'''
    SystemLab-Design Version 20.01
    Copyright © 2019-2020 SystemLab Inc. All rights reserved.
    
    NOTICE================================================================================   
    This file is part of SystemLab-Design 20.01.
    
    SystemLab-Design 20.01 is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    SystemLab-Design 20.01 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SystemLab-Design 20.01.  If not, see <https://www.gnu.org/licenses/>.    
    ======================================================================================

    ABOUT THIS MODULE
    Name: systemlab_utilities
    Common procedures used in algorithms and fb scripts
'''
      
def adjust_units_time(unit_format):
    #Converts values defined in ms, us, ns, ps and fs into seconds
    unit_adjust = 1
    if unit_format == 'ms':
        unit_adjust = 1e-3
    elif unit_format == 'us':
        unit_adjust = 1e-6
    elif unit_format == 'ns':
        unit_adjust = 1e-9
    elif unit_format == 'ps': 
        unit_adjust = 1e-12
    elif unit_format == 'fs': 
        unit_adjust = 1e-15
    return unit_adjust

def adjust_units_freq(unit_format):
    #Converts values defined in kHz, MHz, GHz, THz into Hz
    unit_adjust = 1
    if unit_format == 'kHz':
        unit_adjust = 1e3
    elif unit_format == 'MHz':
        unit_adjust = 1e6
    elif unit_format == 'GHz':
        unit_adjust = 1e9
    elif unit_format == 'THz': 
        unit_adjust = 1e12
    return unit_adjust

def adjust_units_wave(unit_format):
    #Converts values defined in um, nm into m
    unit_adjust = 1
    if unit_format == 'um':
        unit_adjust = 1e-6
    elif unit_format == 'nm':
        unit_adjust = 1e-9
    return unit_adjust