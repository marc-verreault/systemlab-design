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
    Name: systemlab_set_link
    SystemLab module for building and updating signal connections between functional
    blocks: SetLink, LinksDesignPathView
    
    Sections of code design below (__init__, setFromPort, setToPort, setEndPos, setBeginPos)
    based on 'DiagramEditorProto.py' (class connection, portItem, diagramEditor, diagramScene)
    Author first name: Windel - many thanks to the author!
    Copy of original code is located at the end of this module
    Source - Creating a diagram editor,
    http://www.windel.nl/?section=pyqtdiagrameditor (downloaded 11 Feb 2018)
'''
# MV 20.01.r1 3-Nov-2019
import importlib
config_special_path = str('syslab_config_files.config_special')
config_sp = importlib.import_module(config_special_path)

from PyQt5 import QtCore, QtGui, QtWidgets

# MV 20.01.r2.custom 3-Jun-20
import sys
import traceback

class SetLink(): 
    '''Used to create signal links between FB ports
    '''    
    def __init__(self, fromPort, toPort, lineMode, project_scene):
        self.fromPort = fromPort
        self.lineMode = lineMode
        self.pos1 = None
        self.pos2 = None
        self.port_offset = 15
        self.endConnectState = False
        self.project_scene = project_scene
        if fromPort:
            self.pos1 = fromPort.scenePos()  
            fromPort.posCallbacks.append(self.setBeginPos)
            self.toPort = toPort
            
        # Create connection items (GraphicsLineItem or GraphicsPathItem)
        # and add to scene
        signal = fromPort.signal_type       
        self.portlink = LinksDesignPathView(signal, None, None, None, None, None, self.project_scene) 
        self.project_scene.addItem(self.portlink)         
      
    def setFromPort(self, fromPort): # Beginning of of link creation (hover start port)
        self.fromPort = fromPort
        if self.fromPort:
            self.pos1 = fromPort.scenePos()
            self.fromPort.posCallbacks.append(self.setBeginPos)
            #print(self.fromPort.posCallbacks)
         
    def setToPort(self, toPort): # End of of link creation (hover end port)
        self.toPort = toPort
        if self.toPort:
            self.pos2 = toPort.scenePos()
            self.toPort.posCallbacks.append(self.setEndPos)
            #print(self.toPort.posCallbacks)
            
    def setEndPos(self, endpos): # End position re-set (from movement)
        #print('Set end position')
        self.pos2 = endpos        
        if self.lineMode == True:
            self.set_linear_link()
        else:
            self.set_polygon_link() 
            
    def setBeginPos(self, pos1): # End position re-set (from movement)
        #print('Set begin position')
        self.pos1 = pos1        
        if self.lineMode == True:
            self.set_linear_link()
        else:
            self.set_polygon_link()
            
    def set_linear_link(self): #Create straight line connection 
        path = QtGui.QPainterPath()
        try: # MV 20.01.r3 9-Jun-20
            pos_start = QtCore.QPointF(self.pos1)        
            pos_end = QtCore.QPointF(self.pos2)
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Error processing reset links')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
            msg.setWindowTitle("Processing error: Reset links")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
        
        path.addPolygon(QtGui.QPolygonF([pos_start, pos_end]))
        self.portlink.setPath(path)

    def set_polygon_link(self): #Create elbow connection
        path = QtGui.QPainterPath()
        try: # MV 20.01.r3 9-Jun-20
            pos_start = QtCore.QPointF(self.pos1)
            delta_x = abs(self.pos2.x() - self.pos1.x())
            delta_y = abs(self.pos2.y() - self.pos1.y())
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Error processing reset links')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
            msg.setWindowTitle("Processing error: Reset links")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
                
        pos_int_count = 2
        
        #Upper left quadrant to lower right quadrant===========================
        if self.pos2.x() > self.pos1.x() and self.pos2.y() > self.pos1.y():
            if self.fromPort.port_cardinal == 'South':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(),
                                                   self.pos1.y() + delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() + delta_y/2)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() + delta_y + self.port_offset)
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 3
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 1  
                
            elif self.fromPort.port_cardinal == 'North':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() - self.port_offset)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() + delta_y + self.port_offset)                       
                        pos_int_count = 4
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 3
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(),
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 3
                        
            elif self.fromPort.port_cardinal == 'East':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y())
                        pos_int_count = 1
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() + delta_y
                                                   + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() + delta_y
                                                   + self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x
                                                   + self.port_offset, self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + delta_y)
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() + delta_y)
                        
            else: #From West
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y() + delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() + delta_y/2)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y() + delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + delta_y/2)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 4
                    else:                    
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset,
                                                   self.pos1.y() + delta_y)
        
        #Lower left quadrant to upper right quadrant===========================            
        elif self.pos2.x() > self.pos1.x() and self.pos2.y() <= self.pos1.y():
            if self.fromPort.port_cardinal == 'South':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(),
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x/2,
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() + delta_x,
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_count = 4
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() + self.port_offset) 
                        # MV 20.01.r1 - Bug fix
                        # Changed sign in "self.pos1.y() - self.port_offset"
                        # to "self.pos1.y() + self.port_offset"
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 3
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2, 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x/2, 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 3
                
            elif self.fromPort.port_cardinal == 'North':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() - delta_y/2)
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(),
                                                   self.pos1.y() - delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() - delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset,
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 3
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 1  
                        
            elif self.fromPort.port_cardinal == 'East':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x/2, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y())
                        pos_int_count = 1
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset, 
                                                   self.pos1.y() - delta_y)
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + delta_x/2, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + delta_x/2, 
                                                   self.pos1.y() - delta_y)   
                        
            else: #From West
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() + delta_x + self.port_offset, 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 4
                    else:                    
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - self.port_offset, 
                                                   self.pos1.y() - delta_y)
        
        #Lower right quadrant to upper left quadrant===========================
        elif self.pos2.x() <= self.pos1.x() and self.pos2.y() <= self.pos1.y():
            if self.fromPort.port_cardinal == 'South':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_count = 4
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + self.port_offset)
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 3
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 3
                
            elif self.fromPort.port_cardinal == 'North':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() - delta_y/2)
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 1
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 3 
                        
            elif self.fromPort.port_cardinal == 'East':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() - delta_y - self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() - delta_y)
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() - delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x - 2*self.port_offset,
                                                   self.pos1.y() - delta_y/2)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() - delta_x - 2*self.port_offset, 
                                                   self.pos1.y() - delta_y)
                        pos_int_count = 4         
                        
            else:
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() - delta_y)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y())
                        pos_int_count = 1
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() - delta_y)
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() - delta_y)
        
        #Upper right quadrant to lower left quadrant===========================    
        else:
            if self.fromPort.port_cardinal == 'South':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + delta_y/2)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 1 
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 3
                
            elif self.fromPort.port_cardinal == 'North':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() - self.port_offset)
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_count = 4
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 3
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x(), 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() - self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 3
                
            elif self.fromPort.port_cardinal == 'East':
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y() + delta_y)
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x() + self.port_offset, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() + self.port_offset,
                                                   self.pos1.y() + delta_y/2)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x - 2*self.port_offset, 
                                                   self.pos1.y() + delta_y/2)
                        pos_int_4 = QtCore.QPointF(self.pos1.x() - delta_x - 2*self.port_offset, 
                                                   self.pos1.y() + delta_y)
                        pos_int_count = 4    
                        
            else:
                if self.endConnectState == True:
                    if self.toPort.port_cardinal == 'North':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y())
                        pos_int_count = 1
                    elif self.toPort.port_cardinal == 'South':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_3 = QtCore.QPointF(self.pos1.x() - delta_x, 
                                                   self.pos1.y() + delta_y + self.port_offset)
                        pos_int_count = 3
                    elif self.toPort.port_cardinal == 'East':
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x/2, 
                                                   self.pos1.y() + delta_y)
                    else:
                        pos_int_1 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset,
                                                   self.pos1.y())
                        pos_int_2 = QtCore.QPointF(self.pos1.x() - delta_x - self.port_offset, 
                                                   self.pos1.y() + delta_y)

        pos_end = QtCore.QPointF(self.pos2)
        
        #Setup polygon path....
        if self.endConnectState == True:
            if pos_int_count == 1:
                path.addPolygon(QtGui.QPolygonF([pos_start, pos_int_1, pos_end]))
            elif pos_int_count == 2:
                path.addPolygon(QtGui.QPolygonF([pos_start, pos_int_1, 
                                                 pos_int_2, pos_end]))
            elif pos_int_count == 3:                   
                path.addPolygon(QtGui.QPolygonF([pos_start, pos_int_1, pos_int_2,
                                                 pos_int_3, pos_end]))
            else:
                path.addPolygon(QtGui.QPolygonF([pos_start, pos_int_1, pos_int_2,
                                                 pos_int_3, pos_int_4, pos_end]))
        else:
            path.addPolygon(QtGui.QPolygonF([pos_start, pos_end]))
        self.portlink.setPath(path)

    def delete(self):
        self.project_scene.removeItem(self.portlink)
        

class LinksDesignPathView(QtWidgets.QGraphicsPathItem):
    '''Create signal links between compatible ports
    '''  
    #Data attributes
    def __init__(self, signal, fromPort_portID, fromPort_fb_key, toPort_portID, 
                 toPort_fb_key, link_key, project_scene, parent = None):  
        super(LinksDesignPathView, self).__init__(parent)
        self.setFlag(self.ItemIsSelectable, False)
        self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor)) 
        #---------------------------------------------------------------------------------
        # MV 20.01.r1 1-Nov-19. Added conditions for hover enter/leave events
        # to ensure that delete signal link menu (on right click) loses focus after 
        # leaving the hover region for a connection path
        # Code changes based on posts from stackoverflow
        # https://stackoverflow.com/questions/50347595/mouse-hover-over-a-pyside-
        # qgraphicspathitem (accessed 1-Nov-2019) 
        # Thanks to users 'chengxudude' and 'eyllanesc' for sharing sample code
        self.setAcceptHoverEvents(True)
        self.hover = False
        #---------------------------------------------------------------------------------
        self.signal = signal   
        self.fromPort_portID = fromPort_portID
        self.fromPort_fb_key = fromPort_fb_key
        self.toPort_portID = toPort_portID
        self.toPort_fb_key = toPort_fb_key
        self.link_key = link_key
        self.project_scene = project_scene       
        self.setZValue(-50)
    
    def set_line_color(self, signal, link_complete, highlight): # MV 20.01.r1 1-Nov-19
        if link_complete == False:
            pen_style = QtCore.Qt.DashLine
        else:
            pen_style = QtCore.Qt.SolidLine
            
        # MV 20.01.r1 1-Nov-19: New condition for highlighting connections when hover
        # event is activated
        if highlight == True and config_sp.highlight_links_on_hover == True:
            pen_width = 3
            alpha = 100
        else:
            pen_width = 1
            alpha = 255
        
        # MV 20.01.r1 Colors now linked to global config file
        if signal == 'Electrical':
            r = config_sp.c_elec[0]
            g = config_sp.c_elec[1]
            b = config_sp.c_elec[2]
        elif signal == 'Optical':
            r = config_sp.c_opt[0]
            g = config_sp.c_opt[1]
            b = config_sp.c_opt[2]
        elif signal == 'Digital':
            r = config_sp.c_digital[0]
            g = config_sp.c_digital[1]
            b = config_sp.c_digital[2] 
        elif signal == 'Analog (1)':
            r = config_sp.c_analog_1[0]
            g = config_sp.c_analog_1[1]
            b = config_sp.c_analog_1[2]                         
        elif signal == 'Analog (2)':
            r = config_sp.c_analog_2[0]
            g = config_sp.c_analog_2[1]
            b = config_sp.c_analog_2[2] 
        elif signal == 'Analog (3)':
            r = config_sp.c_analog_3[0]
            g = config_sp.c_analog_3[1]
            b = config_sp.c_analog_3[2] 
        else:
            r = config_sp.c_disabled[0]
            g = config_sp.c_disabled[1]
            b = config_sp.c_disabled[2]            
        self.setPen(QtGui.QPen(QtGui.QColor(r, g, b, alpha), pen_width, pen_style))  
            
    # MV 20.01.r1 1-Nov-19. Added conditions for hover enter/leave events ()--------------
    def hoverEnterEvent(self, event): #QMouseEvent
        self.hover = True      
        self.set_line_color(self.signal, True, True)
        self.update() 
    
    def hoverLeaveEvent(self, event):
        self.hover = False
        self.set_line_color(self.signal, True, False)
        self.update()
       
    def boundingRect(self):
        return self.shape().boundingRect()
    
    def shape(self): # Use path stroker to create hover/selection that surrounds path
                     # with specified width (much easier to select and delete)
        s = QtGui.QPainterPathStroker()    
        s.setWidth(10)
        s.setCapStyle(QtCore.Qt.FlatCap)
        path = s.createStroke(self.path())
        return path  
    #-------------------------------------------------------------------------------------
    
    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != QtCore.Qt.LeftButton) and self.hover == True:
            # MV 20.01.r1 Added condition for hover event. Ensures that delete
            # signal link does not appear outside of hover region for a link (removes
            # focus)
            self.setFlag(self.ItemIsSelectable, True)
            self.setSelected(True)
            #------------------------------------------------------------------------
            menu = QtWidgets.QMenu()
            delete_link_action = menu.addAction("Delete signal link?")
            action = menu.exec_(mouseEvent.screenPos())
            #self.update()
            if action == delete_link_action:
                items = self.project_scene.items(mouseEvent.scenePos())
                for line_item in items:
                    if type(line_item) is LinksDesignPathView:                        
                        #Retrieve associated port data from LinkDesignView instance
                        fb_start_key = line_item.fromPort_fb_key
                        fb_start_portID = line_item.fromPort_portID
                        fb_end_key = line_item.toPort_fb_key
                        fb_end_portID = line_item.toPort_portID                      
                        #Retrieve link_key from the start port
                        start_fb = self.project_scene.fb_design_view_list[fb_start_key]
                        link_key = start_fb.ports[fb_start_portID].link_key                      
                        #Update affected ports to reflect changes to link status
                        start_fb.ports[fb_start_portID].link_key = None
                        start_fb.ports[fb_start_portID].link_name = None
                        start_fb.ports[fb_start_portID].connected = False                       
                        end_fb = self.project_scene.fb_design_view_list[fb_end_key]
                        end_fb.ports[fb_end_portID].link_key = None
                        end_fb.ports[fb_end_portID].link_name = None
                        end_fb.ports[fb_end_portID].connected = False
                        
                        # MV 20.01.r3 25-Jun-20
                        # The signal object for the port is deleted and
                        # re-instantiated (clears port data, for example 
                        # after completion of a simulation)
                        end_fb.update_port(fb_end_key, fb_end_portID)
                        
                        # Remove and delete qgraphicslineitem
                        self.project_scene.removeItem(line_item)                        
                        del line_item
                        #Delete associated signal link class                      
                        del self.project_scene.signal_links_list[link_key]
                        break
        else:
            self.setFlag(self.ItemIsSelectable, False)

'''=======================================================================================
Portions of code design (primarily the class connection, diagramEditor, diagramScene)
is based on 'DiagramEditorProto.py' (author first name: Windel)
Copy of original code is shown at end of module (for reference) - many thanks to the author!
[Source code] - Creating a diagram editor,
http://www.windel.nl/?section=pyqtdiagrameditor (downloaded 11 Feb 2018)'''

#!/usr/bin/python

#from PyQt4 import QtGui, QtCore
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
#import sys
#
#class Connection:
#   """
#    - fromPort
#    - toPort
#   """
#   def __init__(self, fromPort, toPort):
#      self.fromPort = fromPort
#      self.pos1 = None
#      self.pos2 = None
#      if fromPort:
#         self.pos1 = fromPort.scenePos()
#         fromPort.posCallbacks.append(self.setBeginPos)
#      self.toPort = toPort
#      # Create arrow item:
#      self.arrow = ArrowItem()
#      editor.diagramScene.addItem(self.arrow)
#   def setFromPort(self, fromPort):
#      self.fromPort = fromPort
#      if self.fromPort:
#         self.pos1 = fromPort.scenePos()
#         self.fromPort.posCallbacks.append(self.setBeginPos)
#   def setToPort(self, toPort):
#      self.toPort = toPort
#      if self.toPort:
#         self.pos2 = toPort.scenePos()
#         self.toPort.posCallbacks.append(self.setEndPos)
#   def setEndPos(self, endpos):
#      self.pos2 = endpos
#      self.arrow.setLine(QLineF(self.pos1, self.pos2))
#   def setBeginPos(self, pos1):
#      self.pos1 = pos1
#      self.arrow.setLine(QLineF(self.pos1, self.pos2))
#   def delete(self):
#      editor.diagramScene.removeItem(self.arrow)
#      # Remove position update callbacks:
#
#class ParameterDialog(QDialog):
#   def __init__(self, parent=None):
#      super(ParameterDialog, self).__init__(parent)
#      self.button = QPushButton('Ok', self)
#      l = QVBoxLayout(self)
#      l.addWidget(self.button)
#      self.button.clicked.connect(self.OK)
#   def OK(self):
#      self.close()
#
#class PortItem(QGraphicsEllipseItem):
#   """ Represents a port to a subsystem """
#   def __init__(self, name, parent=None):
#      QGraphicsEllipseItem.__init__(self, QRectF(-6,-6,12.0,12.0), parent)
#      self.setCursor(QCursor(QtCore.Qt.CrossCursor))
#      # Properties:
#      self.setBrush(QBrush(Qt.red))
#      # Name:
#      self.name = name
#      self.posCallbacks = []
#      self.setFlag(self.ItemSendsScenePositionChanges, True)
#   def itemChange(self, change, value):
#      if change == self.ItemScenePositionHasChanged:
#         for cb in self.posCallbacks:
#            cb(value)
#         return value
#      return super(PortItem, self).itemChange(change, value)
#   def mousePressEvent(self, event):
#      editor.startConnection(self)
#
## Block part:
#class HandleItem(QGraphicsEllipseItem):
#   """ A handle that can be moved by the mouse """
#   def __init__(self, parent=None):
#      super(HandleItem, self).__init__(QRectF(-4.0,-4.0,8.0,8.0), parent)
#      self.posChangeCallbacks = []
#      self.setBrush(QtGui.QBrush(Qt.white))
#      self.setFlag(self.ItemIsMovable, True)
#      self.setFlag(self.ItemSendsScenePositionChanges, True)
#      self.setCursor(QtGui.QCursor(Qt.SizeFDiagCursor))
#
#   def itemChange(self, change, value):
#      if change == self.ItemPositionChange:
#         x, y = value.x(), value.y()
#         # This cannot be a signal because this is not a QObject
#         for cb in self.posChangeCallbacks:
#            res = cb(x, y)
#            if res:
#               x, y = res
#               value = QPointF(x, y)
#         return value
#      # Call superclass method:
#      return super(HandleItem, self).itemChange(change, value)
#
#class BlockItem(QGraphicsRectItem):
#   """ 
#      Represents a block in the diagram
#      Has an x and y and width and height
#      width and height can only be adjusted with a tip in the lower right corner.
#
#      - in and output ports
#      - parameters
#      - description
#   """
#   def __init__(self, name='Untitled', parent=None):
#      super(BlockItem, self).__init__(parent)
#      w = 60.0
#      h = 40.0
#      # Properties of the rectangle:
#      self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
#      self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
#      self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
#      self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
#      # Label:
#      self.label = QGraphicsTextItem(name, self)
#      # Create corner for resize:
#      self.sizer = HandleItem(self)
#      self.sizer.setPos(w, h)
#      self.sizer.posChangeCallbacks.append(self.changeSize) # Connect the callback
#      #self.sizer.setVisible(False)
#      self.sizer.setFlag(self.sizer.ItemIsSelectable, True)
#
#      # Inputs and outputs of the block:
#      self.inputs = []
#      self.inputs.append( PortItem('a', self) )
#      self.inputs.append( PortItem('b', self) )
#      self.inputs.append( PortItem('c', self) )
#      self.outputs = []
#      self.outputs.append( PortItem('y', self) )
#      # Update size:
#      self.changeSize(w, h)
#   def editParameters(self):
#      pd = ParameterDialog(self.window())
#      pd.exec_()
#
#   def contextMenuEvent(self, event):
#      menu = QMenu()
#      menu.addAction('Delete')
#      pa = menu.addAction('Parameters')
#      pa.triggered.connect(self.editParameters)
#      menu.exec_(event.screenPos())
#
#   def changeSize(self, w, h):
#      """ Resize block function """
#      # Limit the block size:
#      if h < 20:
#         h = 20
#      if w < 40:
#         w = 40
#      self.setRect(0.0, 0.0, w, h)
#      # center label:
#      rect = self.label.boundingRect()
#      lw, lh = rect.width(), rect.height()
#      lx = (w - lw) / 2
#      ly = (h - lh) / 2
#      self.label.setPos(lx, ly)
#      # Update port positions:
#      if len(self.inputs) == 1:
#         self.inputs[0].setPos(-4, h / 2)
#      elif len(self.inputs) > 1:
#         y = 5
#         dy = (h - 10) / (len(self.inputs) - 1)
#         for inp in self.inputs:
#            inp.setPos(-4, y)
#            y += dy
#      if len(self.outputs) == 1:
#         self.outputs[0].setPos(w+4, h / 2)
#      elif len(self.outputs) > 1:
#         y = 5
#         dy = (h - 10) / (len(self.outputs) + 0)
#         for outp in self.outputs:
#            outp.setPos(w+4, y)
#            y += dy
#      return w, h
#
#class ArrowItem(QGraphicsLineItem):
#   def __init__(self):
#      super(ArrowItem, self).__init__(None)
#      self.setPen(QtGui.QPen(QtCore.Qt.red,2))
#      self.setFlag(self.ItemIsSelectable, True)
#   def x(self):
#      pass
#
#class EditorGraphicsView(QGraphicsView):
#   def __init__(self, scene, parent=None):
#      QGraphicsView.__init__(self, scene, parent)
#   def dragEnterEvent(self, event):
#      if event.mimeData().hasFormat('component/name'):
#         event.accept()
#   def dragMoveEvent(self, event):
#      if event.mimeData().hasFormat('component/name'):
#         event.accept()
#   def dropEvent(self, event):
#      if event.mimeData().hasFormat('component/name'):
#         name = str(event.mimeData().data('component/name'))
#         b1 = BlockItem(name)
#         b1.setPos(self.mapToScene(event.pos()))
#         self.scene().addItem(b1)
#
#class LibraryModel(QStandardItemModel):
#   def __init__(self, parent=None):
#      QStandardItemModel.__init__(self, parent)
#   def mimeTypes(self):
#      return ['component/name']
#   def mimeData(self, idxs):
#      mimedata = QMimeData()
#      for idx in idxs:
#         if idx.isValid():
#            txt = self.data(idx, Qt.DisplayRole)
#            mimedata.setData('component/name', txt)
#      return mimedata
#
#class DiagramScene(QGraphicsScene):
#   def __init__(self, parent=None):
#      super(DiagramScene, self).__init__(parent)
#   def mouseMoveEvent(self, mouseEvent):
#      editor.sceneMouseMoveEvent(mouseEvent)
#      super(DiagramScene, self).mouseMoveEvent(mouseEvent)
#   def mouseReleaseEvent(self, mouseEvent):
#      editor.sceneMouseReleaseEvent(mouseEvent)
#      super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
#
#class DiagramEditor(QWidget):
#   def __init__(self, parent=None):
#      QtGui.QWidget.__init__(self, parent)
#      self.setWindowTitle("Diagram editor")
#
#      # Widget layout and child widgets:
#      self.horizontalLayout = QtGui.QHBoxLayout(self)
#      self.libraryBrowserView = QtGui.QListView(self)
#      self.libraryModel = LibraryModel(self)
#      self.libraryModel.setColumnCount(1)
#      # Create an icon with an icon:
#      pixmap = QPixmap(60, 60)
#      pixmap.fill()
#      painter = QPainter(pixmap)
#      painter.fillRect(10, 10, 40, 40, Qt.blue)
#      painter.setBrush(Qt.red)
#      painter.drawEllipse(36, 2, 20, 20)
#      painter.setBrush(Qt.yellow)
#      painter.drawEllipse(20, 20, 20, 20)
#      painter.end()
#
#      self.libItems = []
#      self.libItems.append( QtGui.QStandardItem(QIcon(pixmap), 'Block') )
#      self.libItems.append( QtGui.QStandardItem(QIcon(pixmap), 'Uber Unit') )
#      self.libItems.append( QtGui.QStandardItem(QIcon(pixmap), 'Device') )
#      for i in self.libItems:
#         self.libraryModel.appendRow(i)
#      self.libraryBrowserView.setModel(self.libraryModel)
#      self.libraryBrowserView.setViewMode(self.libraryBrowserView.IconMode)
#      self.libraryBrowserView.setDragDropMode(self.libraryBrowserView.DragOnly)
#
#      self.diagramScene = DiagramScene(self)
#      self.diagramView = EditorGraphicsView(self.diagramScene, self)
#      self.horizontalLayout.addWidget(self.libraryBrowserView)
#      self.horizontalLayout.addWidget(self.diagramView)
#
#      # Populate the diagram scene:
#      b1 = BlockItem('SubSystem1')
#      b1.setPos(50,100)
#      self.diagramScene.addItem(b1)
#      b2 = BlockItem('Unit2')
#      b2.setPos(-250,0)
#      self.diagramScene.addItem(b2)
#
#      self.startedConnection = None
#   def startConnection(self, port):
#      self.startedConnection = Connection(port, None)
#   def sceneMouseMoveEvent(self, event):
#      if self.startedConnection:
#         pos = event.scenePos()
#         self.startedConnection.setEndPos(pos)
#   def sceneMouseReleaseEvent(self, event):
#      # Clear the actual connection:
#      if self.startedConnection:
#         pos = event.scenePos()
#         items = self.diagramScene.items(pos)
#         for item in items:
#            if type(item) is PortItem:
#               self.startedConnection.setToPort(item)
#         if self.startedConnection.toPort == None:
#            self.startedConnection.delete()
#         self.startedConnection = None
#
#if __name__ == '__main__':
#   app = QtGui.QApplication(sys.argv)
#   global editor
#   editor = DiagramEditor()
#   editor.show()
#   editor.resize(700, 800)
#   app.exec_()

''' Copy of code sample from https://stackoverflow.com/questions/50347595/mouse-hover-
over-a-pyside-qgraphicspathitem (accessed 1-Nov-2019). User: eyllanesc'''
#class Edge(QtGui.QGraphicsPathItem):
#    def __init__(self):
#        QtGui.QGraphicsPathItem.__init__(self)
#        self.setAcceptsHoverEvents(True)
#        path = QtGui.QPainterPath()
#        x1 = -100
#        x2 = 120
#        y1 = -100
#        y2 = 120
#        dx = abs(x1-x2)/2
#        dy = abs(y1-y2)/2
#        a = QtCore.QPointF(x1, y1)
#        b = a + QtCore.QPointF(dx, 0)
#        d = QtCore.QPointF(x2, y2)
#        c = d - QtCore.QPointF(dy, 0)
#        path.moveTo(a)
#        path.cubicTo(b,c,d)
#        self.setPath(path)
#
#        self.hover = False
#
#    def hoverEnterEvent(self, event):
#        QtGui.QGraphicsPathItem.hoverEnterEvent(self, event)
#        self.hover = True
#        self.update()
#
#    def hoverMoveEvent(self, event):
#        # print(event)
#        QtGui.QGraphicsPathItem.hoverMoveEvent(self, event)
#
#    def hoverLeaveEvent(self, event):
#        QtGui.QGraphicsPathItem.hoverLeaveEvent(self, event)
#        self.hover = False
#        self.update()        
#
#    def boundingRect(self):
#        return self.shape().boundingRect()
#
#    def paint(self, painter, option, widget):
#        c = QtCore.Qt.red if self.hover else QtCore.Qt.black
#        painter.setPen(QtGui.QPen(c, 10, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
#        painter.drawPath(self.path())
#
#        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
#        painter.drawPath(self.shape())
#
#    def shape(self):
#        s = QtGui.QPainterPathStroker()    
#        s.setWidth(30)
#        s.setCapStyle(QtCore.Qt.RoundCap)
#        path = s.createStroke(self.path())
#        return path



