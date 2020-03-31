"""
QPainterPath definition for Optical Amplifier
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x, y+15)
    p2 = QtCore.QPointF(x+8, y+15)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+10, y+20)
    p2 = QtCore.QPointF(x+10, y+10)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 )) 
    icon_2.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+14, y+20)
    p2 = QtCore.QPointF(x+14, y+10)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 )) 
    icon_3.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+18, y+20)
    p2 = QtCore.QPointF(x+18, y+10)
    icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 )) 
    icon_4.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_5 = QtWidgets.QGraphicsPathItem()
    icon_path_5 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+22, y+20)
    p2 = QtCore.QPointF(x+22, y+10)
    icon_path_5.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 )) 
    icon_5.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_6 = QtWidgets.QGraphicsPathItem()
    icon_path_6 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+26, y+20)
    p2 = QtCore.QPointF(x+26, y+10)
    icon_path_6.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_6.setPath(icon_path_6)
    icon_6.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 )) 
    icon_6.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    
    icon_7 = QtWidgets.QGraphicsPathItem()
    icon_path_7 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+30, y+20)
    p2 = QtCore.QPointF(x+30, y+10)
    icon_path_7.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_7.setPath(icon_path_7)
    icon_7.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.5 )) 
    icon_7.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))

    icon_8 = QtWidgets.QGraphicsPathItem()
    icon_path_8 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+32, y+15)
    p2 = QtCore.QPointF(x+41, y+15)
    icon_path_8.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_8.setPath(icon_path_8)
    icon_8.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 )) 
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4, icon_5, icon_6, icon_7, icon_8]
    return icon_paths
        
        
        
        