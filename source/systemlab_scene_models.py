'''
    SystemLab-Design Version 20.01
    Primary author: Marc Verreault
    E-mail: marc.verreault@systemlabdesign.com
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
    Name: systemlab_scene_models
    SystemLab module for all data models available for use within a design space:
    (FunctionalBlock, SignalLink, DataBox, DescriptionBox, TextBox, LineArrow)
'''

class FunctionalBlock():
    '''Base class for the functional block. All information related to the properties
       of the functional block (input/output ports, parameters, etc.) is held 
       in this class. This class is the data model companion to the pyqt
       FunctionalBlockDesignView class
    '''  
    #Data attributes
    def __init__(self, fb_key, fb_name, display_name, display_port_name, fb_geometry,
                 fb_dim, fb_position, fb_script_module, fb_icon_display, fb_icon, fb_icon_x, fb_icon_y,
                 fb_parameters_list, fb_results_list, text_size, text_length, text_color,
                 text_bold, text_italic, fb_color, fb_color_2, fb_gradient, fb_border_color,
                 fb_border_style, text_pos_x, text_pos_y, port_label_size, port_label_bold,
                 port_label_italic, port_label_color):
        self.fb_key = fb_key #Track all functional blocks associated with a project (1,2,3...)
        self.fb_name = fb_name #User-defined name for functional block   
        self.display_name = display_name
        self.display_port_name = display_port_name
        
        #self.__FunctionalBlock_version = 1 #Version number of FunctionalBlock class
        
        # Data attributes linked to FunctionalBlockDesignView
        # (geometry/position/colors)
        self.fb_geometry = fb_geometry # [x, y, w, h]
        self.fb_dim = fb_dim # [width, height]
        self.fb_position = fb_position # [x pos, y pos]
        self.fb_color = fb_color
        self.fb_color_2 = fb_color_2
        self.fb_gradient = fb_gradient
        self.fb_border_color = fb_border_color
        self.fb_border_style = fb_border_style
        self.fb_icon_display = fb_icon_display
        self.fb_icon = fb_icon
        self.fb_icon_x = fb_icon_x
        self.fb_icon_y = fb_icon_y      
        #Attributes associated with FB title text
        self.text_size = text_size
        self.text_length = text_length
        self.text_color = text_color
        self.text_bold = text_bold
        self.text_italic = text_italic
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y    
        #Attributes associated with port label text
        self.port_label_size = port_label_size
        self.port_label_bold = port_label_bold
        self.port_label_italic = port_label_italic
        self.port_label_color = port_label_color
        
        # FB ports list (list of ports associated with the FB instance)
        # [portID, portName, portCardinal, portDirection, signal, connected, data_ready] 
        self.fb_ports_list = []
        
        # Attributes used during a simulation
        self.fb_calculation_status = 'Ready'
        self.status_counter = 0
        self.fb_script_module = fb_script_module
        
        #Lists for holding parameters and data results
        self.fb_parameters_list = fb_parameters_list
        self.fb_results_list = fb_results_list
        
        #Version tracking
        self.__version = 1
        
    def __repr__(self): #Return string method for print(object)
        return ( 'FB key:' + str(self.fb_key) + '; FB name:' + self.fb_name + '; ' + 
                str(self.display_name) + '; ' + str(self.display_port_name) + '; ' + 
                str(self.fb_geometry) + '; ' + str(self.fb_dim) + '; ' + 
                str(self.fb_position) + '; ' + str(self.fb_script_module) + '; ' + 
                str(self.fb_icon_display) + '; ' + str(self.fb_icon) + '; ' + 
                str(self.fb_icon_x) + '; ' + str(self.fb_icon_y) + '; ' + 
                str(self.fb_parameters_list) + '; ' + str(self.fb_results_list) + '; ' + 
                str(self.text_size) + '; ' + str(self.text_length) + '; ' + 
                str(self.text_color) + '; ' + str(self.text_bold) + '; ' + 
                str(self.text_italic) + '; ' + str(self.fb_color) + '; ' + 
                str(self.fb_color_2) + '; ' + str(self.fb_gradient) + '; ' + 
                str(self.fb_border_color) + '; ' + str(self.fb_border_style) + '; ' + 
                str(self.text_pos_x) + '; ' + str(self.text_pos_y) + '; ' + 
                str(self.port_label_size) + '; ' + str(self.port_label_bold) + '; ' + 
                str(self.port_label_italic) + '; ' + str(self.port_label_color) )
            
    #METHODS            
    def check_version(self):
        #No check needed for version 1
        pass

    
class SignalLink():
    '''Base class representing the signal links between ports. Holds information
       on the source and destination ports and signal type. When links are set
       (connected) the simulator transfers signal data from the source (transmit)
       to the destination (receiver) port.
    '''
    def __init__(self, link_key, link_name, fb_start_key, fb_start, start_port,
                 start_port_ID, fb_end_key, fb_end, end_port, end_port_ID, line_mode):
        self.link_key = link_key #Used to uniquely track all links within a scene
        self.link_name = link_name #Automatically generated
        self.fb_start_key = fb_start_key
        self.fb_start = fb_start
        self.start_port = start_port
        self.start_port_ID = start_port_ID
        self.fb_end_key = fb_end_key
        self.fb_end = fb_end
        self.end_port = end_port
        self.end_port_ID = end_port_ID
        self.line_mode = line_mode
        
        #Version tracking
        self.__version = 1
        
    def __repr__(self): #Return string method for print(object)
        return ( 'Signal key:' + str(self.link_key) + '; Signal name:' + 
                str(self.link_name) + '; ' + str(self.fb_start_key) + '; ' + 
                str(self.fb_start) + '; ' + str(self.start_port) + '; ' + 
                str(self.start_port_ID) + '; ' + str(self.fb_end_key) + '; ' + 
                str(self.fb_end) + '; ' + str(self.end_port) + '; ' + 
                str(self.end_port_ID) + '; ' + str(self.line_mode) )
        
    def check_version(self):
        #No check needed for version 1
        pass 


class DescriptionBox():
    '''Non critical class (not directly linked to the simulation process) 
       which can be used to visually represent rectangular regions for highlighting
       function types, sub-systems, etc. These can be applied anywhere in the 
       scene (for example, visually encapsulating a group of FB/components to
       describe a general function). This data class holds information on the
       boxes dimensions, colors and text attributes
    '''
    def __init__(self, desc_key, desc_text, box_position, box_dim, box_geometry,
                 text_width, fill_color, fill_color_2, opacity, gradient, border_color,
                 text_size, text_color, text_bold, text_italic, border_style,
                 border_width, text_pos_x, text_pos_y):
        
        self.desc_key = desc_key
        self.desc_text = desc_text
        self.box_position = box_position
        self.box_dim = box_dim
        self.box_geometry = box_geometry
        self.text_width = text_width  
        self.fill_color = fill_color
        self.fill_color_2 = fill_color_2
        self.opacity = opacity
        self.gradient = gradient
        self.border_color = border_color
        self.text_width = text_width
        self.text_size = text_size
        self.text_color = text_color
        self.text_bold = text_bold
        self.text_italic = text_italic
        self.border_style = border_style
        self.border_width = border_width
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        
        #Version tracking
        self.__version = 1

    def __repr__(self): #Return string method for print(object)
        return ( 'DescBox key:' + str(self.desc_key) + '; ' + str(self.desc_text) + 
                '; ' + str(self.box_position) + '; ' + str(self.box_dim) + '; ' + 
                str(self.box_geometry) + '; ' + str(self.text_width) + '; ' + 
                str(self.fill_color) + '; ' + str(self.fill_color_2) + '; ' + 
                str(self.opacity) + str(self.gradient) + '; ' + str(self.border_color) + 
                '; ' + str(self.text_width) + '; ' + str(self.text_size) + '; ' + 
                str(self.text_color) + '; ' + str(self.text_bold) + '; ' + 
                str(self.text_italic) + '; ' + str(self.border_style) + '; ' + 
                str(self.border_width) + '; ' + str(self.text_pos_x) + '; ' + 
                str(self.text_pos_y) )
        
    def check_version(self):
        #No check needed for version 1
        pass 
        
class DataBox():
    def __init__(self, data_key, title_text, title_geometry, title_position, title_width,
                 title_height, title_box_color, title_box_opacity, title_border_color,
                 title_text_width, title_text_size, title_text_color, title_text_bold,
                 title_text_italic, title_border_style, title_border_width, title_text_pos_x,
                 title_text_pos_y, data_box_geometry, data_box_position, data_box_width,
                 data_box_height, data_box_color, data_box_opacity, data_box_gradient,
                 data_border_color, data_box_border_style, data_box_border_width, 
                 data_text_size, data_width, value_width, data_text_pos_x, data_text_pos_y, 
                 data_source_file):
        
        self.data_key = data_key
        self.title_text = title_text
        self.title_geometry = title_geometry
        self.title_position = title_position
        self.title_width = title_width
        self.title_height = title_height    
        self.title_box_color = title_box_color
        self.title_box_opacity = title_box_opacity
#        self.title_box_gradient = title_box_gradient
        self.title_border_color = title_border_color
        self.title_text_width = title_text_width
        self.title_text_size = title_text_size
        self.title_text_color = title_text_color
        self.title_text_bold = title_text_bold
        self.title_text_italic = title_text_italic
        self.title_border_style = title_border_style
        self.title_border_width = title_border_width
        self.title_text_pos_x = title_text_pos_x
        self.title_text_pos_y = title_text_pos_y   
        #Data box/field settings
        self.data_box_geometry = data_box_geometry
        self.data_box_position = data_box_position
        self.data_box_width = data_box_width
        self.data_box_height = data_box_height    
        self.data_box_color = data_box_color
        self.data_box_opacity = data_box_opacity
        self.data_box_gradient = data_box_gradient
        self.data_border_color = data_border_color
        self.data_box_border_style = data_box_border_style
        self.data_box_border_width = data_box_border_width
        self.data_text_size = data_text_size
        self.data_width = data_width
        self.value_width = value_width
        self.data_text_pos_x = data_text_pos_x
        self.data_text_pos_y = data_text_pos_y
        #Source file (dictionary for importing data fields)
        self.data_source_file = data_source_file    
        
        #Version tracking
        self.__version = 1
        
    def __repr__(self): #Return string method for print(object)
        return ( 'DataBox key:' + str(self.data_key) + '; '+ str(self.title_text) + 
                '; ' + str(self.title_geometry) + '; ' + str(self.title_position) + 
                '; ' + str(self.title_width) + '; '+ str(self.title_height) + 
                '; ' + str(self.title_box_color) + '; '+ str(self.title_box_opacity) + 
                '; ' + str(self.title_border_color) + '; '+ str(self.title_text_width) + 
                '; ' + str(self.title_text_size) + '; '+ str(self.title_text_color) + 
                '; ' + str(self.title_text_bold) + '; '+ str(self.title_text_italic) + 
                '; ' + str(self.title_border_style) + '; '+ str(self.title_border_width) + 
                '; ' + str(self.title_text_pos_x) + '; '+ str(self.title_text_pos_y) + 
                '; ' + str(self.data_box_geometry) + '; '+ str(self.data_box_position) + 
                '; ' + str(self.data_box_width) + '; '+ str(self.data_box_height) + 
                '; ' + str(self.data_box_color) + '; '+ str(self.data_box_opacity) + 
                '; ' + str(self.data_box_gradient) + '; '+ str(self.data_border_color) + 
                '; ' + str(self.data_box_border_style) + 
                '; ' + str(self.data_box_border_width) + '; ' + str(self.data_text_size) + 
                '; ' + str(self.data_width) + str(self.value_width) + 
                '; ' + str(self.data_text_pos_x) + '; '+ str(self.data_text_pos_y) + 
                '; ' + str(self.data_source_file) )
        
    def check_version(self):
        #No check needed for version 1
        pass 
        
class TextBox(): 
    '''Data class for the companion pyqt class TextBoxDesignView. Can be used 
       to add text regions anywhere withion the design scene. 
       Non critical class (not directly linked to the simulation process)
    '''
    def __init__(self, text_key, text, text_position, text_geometry, text_width,
                 text_color, text_size, text_bold, text_italic, enable_background, 
                 background_color):
        
        self.text_key = text_key
        self.text = text
        self.text_width = text_width
        self.text_position = text_position
        self.text_geometry = text_geometry
        self.text_color = text_color
        self.text_size = text_size
        self.text_bold = text_bold
        self.text_italic = text_italic
        self.enable_background = enable_background
        self.background_color = background_color # Version 2
        
        #Version tracking
        self.__version = 1 
        self.__version = 2 # MV 20.01.r2 Added background color feature
        
    def __repr__(self): #Return string method for print(object)
        return ( 'TextBox key:' + str(self.text_key) + '; ' + str(self.text) + '; ' + 
                str(self.text_width) + '; ' + str(self.text_position) + '; ' + 
                str(self.text_geometry) + '; ' + str(self.text_color) + '; ' + 
                str(self.text_size) + '; ' + str(self.text_bold) + '; ' + 
                str(self.text_italic) + '; ' + str(self.text_italic) )
        
    def check_version(self):
        #No check needed for version 1
        pass 
    
    
#class RichTextBox(): # MV 20.01.r1
#    '''Data class for the companion pyqt class RichTextBoxDesignView. Can be used 
#       to add text regions anywhere withion the design scene. 
#       Non critical class (not directly linked to the simulation process)
#    '''
#    def __init__(self, text_key, html, text_position, text_geometry):
#        
#        self.text_key = text_key
#        self.html = html
#        self.text_position = text_position
#        self.text_geometry = text_geometry
#
#        #Version tracking
#        self.__version = 1
#        
#    def __repr__(self): #Return string method for print(object)
#        return ( 'TextBox key:' + str(self.text_key) + '; ' + str(self.html) + '; ' 
#                + str(self.text_position) + '; ' + str(self.text_geometry) )
#        
#    def check_version(self):
#        #No check needed for version 1
#        pass 
        
class LineArrow():
    '''Visual tool which includes a line with arrow. Can be used to highlight
       or bring attention to specific areas of a design layout. This class 
       holds the data asscoated with position and color of the line+arrow.
       Non critical class (not directly linked to the simulation process)
    '''  
    def __init__(self, key, position, geometry, color, line_width, line_style,
                 arrow):
        
        self.key = key
        self.position = position
        self.geometry = geometry
        self.color = color
        self.line_width = line_width
        self.line_style = line_style
        self.arrow = arrow
        
        #Version tracking
        self.__version = 1
        
    def __repr__(self): #Return string method for print(object)
        return ( 'LineArrow key:' + str(self.key) + '; ' + str(self.position) + '; ' + 
                str(self.geometry) + '; ' + str(self.color) + '; ' + 
                str(self.line_width) + '; ' + str(self.line_style) + 
                '; ' + str(self.arrow) )
        
    def check_version(self):
        #No check needed for version 1
        pass 
        
