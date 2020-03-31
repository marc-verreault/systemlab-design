"""
QPainterPath definition for Optical Amplifier
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+5, y+27.5)
    p2 = QtCore.QPointF(x+15, y+27.5)
    p3 = QtCore.QPointF(x+15, y+7.5)
    p4 = QtCore.QPointF(x+20, y+7.5)
    p5 = QtCore.QPointF(x+20, y+27.5)
    p6 = QtCore.QPointF(x+30, y+27.5)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5, p6]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1 ))

    icon_paths = [icon_1]
    return icon_paths