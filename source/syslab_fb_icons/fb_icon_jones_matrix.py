"""
QPainterPath definition for Optical Amplifier
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+3, y)
    p2 = QtCore.QPointF(x-1, y)
    p3 = QtCore.QPointF(x-1, y+30)
    p4 = QtCore.QPointF(x+3, y+30)
    icon_path_1.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+27, y)
    p2 = QtCore.QPointF(x+31, y)
    p3 = QtCore.QPointF(x+31, y+30)
    p4 = QtCore.QPointF(x+27, y+30)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 )) 
    
    font = QtGui.QFont("Arial", 6)
    font.setItalic(True)
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    icon_path_3.addText(x+1.5, y+9, font, 'Jxx')
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.25))
    icon_3.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    icon_path_4.addText(x+16, y+9, font, 'Jxy')
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.25))
    icon_4.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
    
    icon_5 = QtWidgets.QGraphicsPathItem()
    icon_path_5 = QtGui.QPainterPath() 
    icon_path_5.addText(x+1.5, y+26, font, 'Jyx')
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.25))
    icon_5.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
    
    icon_6 = QtWidgets.QGraphicsPathItem()
    icon_path_6 = QtGui.QPainterPath() 
    icon_path_6.addText(x+16, y+26, font, 'Jyy')
    icon_6.setPath(icon_path_6)
    icon_6.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.25))
    icon_6.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4, icon_5, icon_6]
    return icon_paths
        
        
        
        