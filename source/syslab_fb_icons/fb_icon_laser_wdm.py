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
    p1 = QtCore.QPointF(x+18, y+11)
    p2 = QtCore.QPointF(x+32, y+11)
    p3 = QtCore.QPointF(x+28, y+9)
    p4 = QtCore.QPointF(x+28, y+13)
    p5 = QtCore.QPointF(x+32, y+11)
    icon_path_5.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), line_width_2 ))
    icon_5.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_6 = QtWidgets.QGraphicsPathItem()
    icon_path_6 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+18, y+17)
    p2 = QtCore.QPointF(x+32, y+17)
    p3 = QtCore.QPointF(x+28, y+15)
    p4 = QtCore.QPointF(x+28, y+19)
    p5 = QtCore.QPointF(x+32, y+17)
    icon_path_6.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_6.setPath(icon_path_6)
    icon_6.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), line_width_2 ))
    icon_6.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_7 = QtWidgets.QGraphicsPathItem()
    icon_path_7 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+18, y+32)
    p2 = QtCore.QPointF(x+18, y+23)
    p3 = QtCore.QPointF(x+21, y+23)
    p4 = QtCore.QPointF(x+21, y+32)
    p5 = QtCore.QPointF(x+27, y+32)
    p6 = QtCore.QPointF(x+27, y+23)
    p7 = QtCore.QPointF(x+30, y+23)
    p8 = QtCore.QPointF(x+30, y+32)
    p9 = QtCore.QPointF(x+33, y+32)
    p10 = QtCore.QPointF(x+33, y+23)
    icon_path_7.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]))  
    icon_7.setPath(icon_path_7)
    icon_7.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), line_width_1 ))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4, icon_5, icon_6, icon_7]
    return icon_paths
        
        
        
        