"""
QPainterPath definition for electrical adder

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addEllipse(x-12.5, y-12.5, 25, 25)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    icon_1.setOpacity(0.2)
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x-7.5, y)
    p2 = QtCore.QPointF(x+7.5, y)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x, y-7.5)
    p2 = QtCore.QPointF(x, y+7.5)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_paths = [icon_1, icon_2, icon_3]
    return icon_paths