"""
QPainterPath definition for polarization beam splitter (optical)
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+0.5, y+19.5)
    p2 = QtCore.QPointF(x+19.5, y+0.5)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
       
    icon_paths = [icon_1]
    return icon_paths