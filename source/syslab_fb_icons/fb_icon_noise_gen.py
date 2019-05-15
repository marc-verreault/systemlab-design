"""
QPainterPath definition for noise generator

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addEllipse(x-12.5, y-12.5, 25, 25)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 1.5 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
    icon_1.setOpacity(0.1)
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath()   
    p1 = QtCore.QPointF(x-8, y-2)
    p2 = QtCore.QPointF(x-7, y+7)
    p3 = QtCore.QPointF(x-6, y-4)
    p4 = QtCore.QPointF(x-5, y+8)
    p5 = QtCore.QPointF(x-4, y-7)
    p6 = QtCore.QPointF(x-3, y)
    p7 = QtCore.QPointF(x-2, y-6)
    p8 = QtCore.QPointF(x-1, y+3)
    p9 = QtCore.QPointF(x, y-4)
    p10 = QtCore.QPointF(x+1, y)
    p11 = QtCore.QPointF(x+2, y+9)
    p12 = QtCore.QPointF(x+3, y+5)
    p13 = QtCore.QPointF(x+4, y-7)
    p14 = QtCore.QPointF(x+5, y+4)
    p15 = QtCore.QPointF(x+6, y-7)
    p16 = QtCore.QPointF(x+7, y+5)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5, p6, p7, p8, 
                                            p9, p10, p11, p12, p13, p14, p15, p16]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.red), 0.75 ))
    
    icon_paths = [icon_1, icon_2]
    return icon_paths