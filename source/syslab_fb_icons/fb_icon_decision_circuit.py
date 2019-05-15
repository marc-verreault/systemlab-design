"""
QPainterPath definition for Decision Circuit
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x, y+15)
    p2 = QtCore.QPointF(x+15, y+15)
    p3 = QtCore.QPointF(x+15, y-15)
    p4 = QtCore.QPointF(x+30, y-15)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))

    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x, y)
    p2 = QtCore.QPointF(x+30, y)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.75, QtCore.Qt.DotLine)) 
    
    icon_paths = [icon_1, icon_2]
    return icon_paths
        
        
        
        