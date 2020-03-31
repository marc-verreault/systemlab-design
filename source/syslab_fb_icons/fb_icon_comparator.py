"""
QPainterPath definition for electrical adder

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x-7.5, y-10)
    p2 = QtCore.QPointF(x+29, y+10)
    p3 = QtCore.QPointF(x-7.5, y+30)
    p4 = QtCore.QPointF(x-7.5, y-10)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
    icon_1.setOpacity(0.2)
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x-3, y+4)
    p2 = QtCore.QPointF(x+3, y+4)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x, y+1)
    p2 = QtCore.QPointF(x, y+7)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x-3, y+16)
    p2 = QtCore.QPointF(x+3, y+16)
    icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4]
    return icon_paths