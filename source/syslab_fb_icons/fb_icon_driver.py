"""
QPainterPath definition for electrical driver

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+2, y+28)
    p2 = QtCore.QPointF(x+8, y+28)
    p3 = QtCore.QPointF(x+8, y+12)
    p4 = QtCore.QPointF(x+14, y+12)
    p5 = QtCore.QPointF(x+14, y+28)
    p6 = QtCore.QPointF(x+20, y+28)
    p7 = QtCore.QPointF(x+20, y+12)
    p8 = QtCore.QPointF(x+23, y+12)
    p9 = QtCore.QPointF(x+23, y+28)
    p10 = QtCore.QPointF(x+26, y+28)
    p11 = QtCore.QPointF(x+26, y+12)
    p12 = QtCore.QPointF(x+29, y+12)
    p13 = QtCore.QPointF(x+29, y+28)
    p14 = QtCore.QPointF(x+34, y+28)
    
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11,
                                            p12, p13, p14]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_paths = [icon_1]
    return icon_paths