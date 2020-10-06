"""
QPainterPath definition for TIA-LA
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x, y+15)
    p2 = QtCore.QPointF(x+3, y+15)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+1, y+32)
    p2 = QtCore.QPointF(x+1, y-2)
    p3 = QtCore.QPointF(x+41, y+15)
    p4 = QtCore.QPointF(x+1, y+32)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 )) 
    #icon_2.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))

    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+42.5, y+15)
    p2 = QtCore.QPointF(x+44, y+15)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2]))
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 )) 
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    font = QtGui.QFont("Arial", 7)
    font.setItalic(True)
    icon_path_4.addText(x+2, y+18, font, "TIA-LA")
    icon_4.setPath(icon_path_4)
    icon_4.setBrush(QtGui.QBrush(QtCore.Qt.blue))
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.1 ))
    
    icon_paths = [icon_2, icon_4]
    return icon_paths
        
        
        
        