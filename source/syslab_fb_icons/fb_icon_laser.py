"""
QPainterPath definition for cw laser model

Image based on diagrams shown at fololwing link:
https://www.sensorsmag.com/components/replacing-laser-diodes-leds-and-vice-versa
Accessed: 12 Dec 2018
"""

from PyQt5 import QtCore, QtGui, QtWidgets



def run (x, y):
    line_width_1 = 0.75
    line_width_2 = 1
    
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+10, y+8)
    p2 = QtCore.QPointF(x+10, y+15)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), line_width_1 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+5, y+15)
    p2 = QtCore.QPointF(x+15, y+15)
    p3 = QtCore.QPointF(x+10, y+25)
    p4 = QtCore.QPointF(x+5, y+15)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))  
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), line_width_1 ))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+5, y+25)
    p2 = QtCore.QPointF(x+15, y+25)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), line_width_1 ))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+10, y+25)
    p2 = QtCore.QPointF(x+10, y+32)
    icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), line_width_1 ))
    
    icon_5 = QtWidgets.QGraphicsPathItem()
    icon_path_5 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+18, y+18)
    p2 = QtCore.QPointF(x+32, y+18)
    p3 = QtCore.QPointF(x+28, y+16)
    p4 = QtCore.QPointF(x+28, y+20)
    p5 = QtCore.QPointF(x+32, y+18)
    icon_path_5.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), line_width_2 ))
    icon_5.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_6 = QtWidgets.QGraphicsPathItem()
    icon_path_6 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+18, y+24)
    p2 = QtCore.QPointF(x+32, y+24)
    p3 = QtCore.QPointF(x+28, y+22)
    p4 = QtCore.QPointF(x+28, y+26)
    p5 = QtCore.QPointF(x+32, y+24)
    icon_path_6.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_6.setPath(icon_path_6)
    icon_6.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), line_width_2 ))
    icon_6.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4, icon_5, icon_6]
    return icon_paths
        
        
        
        