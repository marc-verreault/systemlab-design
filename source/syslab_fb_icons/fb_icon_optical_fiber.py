"""
QPainterPath definition for Optical Amplifier
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x, y+17.5)
    p2 = QtCore.QPointF(x+40, y+17.5)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    icon_path_2.addEllipse(x+11, y+5.5, 12, 12)
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    icon_path_3.addEllipse(x+14, y+5.5, 12, 12)
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    icon_path_4.addEllipse(x+17, y+5.5, 12, 12)
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4]
    return icon_paths
        
        
        
        