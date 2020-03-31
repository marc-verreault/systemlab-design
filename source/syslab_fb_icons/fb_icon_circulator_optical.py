"""
QPainterPath definition for optical noise generator

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addEllipse(x-15, y-15, 30, 30)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    icon_1.setOpacity(0.2)
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    icon_path_2.moveTo(24.5, 12)
    icon_path_2.arcTo(5, 5, 20, 20, 20, 240)
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1.5 ))
	
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(25, 16)
    p2 = QtCore.QPointF(26, 10)
    p3 = QtCore.QPointF(22, 11)
    p4 = QtCore.QPointF(25, 16)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 )) 
    icon_3.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))	
    
    icon_paths = [icon_1, icon_2, icon_3]
    return icon_paths