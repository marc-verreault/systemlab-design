"""
QPainterPath definition for photodiode model

Image based on diagrams shown at fololwing link:
https://www.sensorsmag.com/components/replacing-laser-diodes-leds-and-vice-versa
Accessed: 12 Dec 2018
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+28, y+8)
    p2 = QtCore.QPointF(x+28, y+15)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+23, y+15)
    p2 = QtCore.QPointF(x+33, y+15)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.75 ))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+28, y+15)
    p2 = QtCore.QPointF(x+33, y+25)
    p3 = QtCore.QPointF(x+23, y+25)
    p4 = QtCore.QPointF(x+28, y+15)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))  
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.75 ))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+28, y+25)
    p2 = QtCore.QPointF(x+28, y+32)
    icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.75 ))
    
    icon_5 = QtWidgets.QGraphicsPathItem()
    icon_path_5 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+4, y+16)
    p2 = QtCore.QPointF(x+18, y+16)
    p3 = QtCore.QPointF(x+14, y+14)
    p4 = QtCore.QPointF(x+14, y+18)
    p5 = QtCore.QPointF(x+18, y+16)
    icon_path_5.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1 ))
    icon_5.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_6 = QtWidgets.QGraphicsPathItem()
    icon_path_6 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x+4, y+22)
    p2 = QtCore.QPointF(x+18, y+22)
    p3 = QtCore.QPointF(x+14, y+20)
    p4 = QtCore.QPointF(x+14, y+24)
    p5 = QtCore.QPointF(x+18, y+22)
    icon_path_6.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_6.setPath(icon_path_6)
    icon_6.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1 ))
    icon_6.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4, icon_5, icon_6]
    
    
    
#    icon_path.addEllipse(center, 10, 10)
    
#    font = QtGui.QFont("Arial", 6)
#    icon_path.addText(x+5, y+5, font, 'LASER')
    return icon_paths


        

#    icon_path.setBrush(QtGui.QBrush(QtGui.QColor(61, 61, 61, 255), QtCore.Qt.SolidPattern))
    
#
#    center = QtCore.QPointF(x, y)
#    icon_path.addEllipse(center, 10, 10)
#    painter.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 ))
#    painter.drawPath(icon_path)
#    
##    font = QtGui.QFont("Arial", 6)
##    icon_path.addText(x+5, y+5, font, 'LASER')
#    return icon_path
        
        
        
        