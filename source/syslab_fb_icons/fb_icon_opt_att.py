"""
QPainterPath definition for optical attenuator
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addEllipse(x-7.5, y-7.5, 10, 10)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    icon_1.setOpacity(0.8)

    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x-9.5, y+4.5)
    p2 = QtCore.QPointF(x+4, y-9)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1.25 )) 
    icon_2.setOpacity(0.8)
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+4.5, y-9.5)
    p2 = QtCore.QPointF(x+3, y-6)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1 )) 
    icon_3.setOpacity(0.8)   
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+4.5, y-9.5)
    p2 = QtCore.QPointF(x+1, y-8)
    icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 1 ))   
    icon_4.setOpacity(0.8)
    

    icon_paths = [icon_1, icon_2, icon_3, icon_4]
    return icon_paths