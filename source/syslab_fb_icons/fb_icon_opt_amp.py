"""
QPainterPath definition for Optical Amplifier
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x, y+15)
    p2 = QtCore.QPointF(x+12, y+15)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+12, y+25)
    p2 = QtCore.QPointF(x+12, y+5)
    p3 = QtCore.QPointF(x+32, y+15)
    p4 = QtCore.QPointF(x+12, y+25)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 )) 
    icon_2.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))

    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+32, y+15)
    p2 = QtCore.QPointF(x+41, y+15)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 )) 
    
    icon_paths = [icon_1, icon_2, icon_3]
    return icon_paths
        
        
        
        