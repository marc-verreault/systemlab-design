"""
QPainterPath definition for Decision Circuit
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addRect(x, y, 45, 25)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    icon_path_2.addRect(x+2.5, y+1, 40, 9)
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    icon_2.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    icon_path_3.addRect(x+2.5, y+15, 40, 9)
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    icon_3.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+5, y+8.5)
    p2 = QtCore.QPointF(x+7, y+8.5)
    p3 = QtCore.QPointF(x+7, y+8.5)
    p4 = QtCore.QPointF(x+11, y+2.5)
    p5 = QtCore.QPointF(x+11, y+8.5)
    p6 = QtCore.QPointF(x+16, y+8.5)
    p7 = QtCore.QPointF(x+16, y+2.5)
    p8 = QtCore.QPointF(x+20, y+2.5)
    p9 = QtCore.QPointF(x+27, y+2.5)
    p10 = QtCore.QPointF(x+27, y+8.5)
    p11 = QtCore.QPointF(x+35, y+8.5)
    p12 = QtCore.QPointF(x+35, y+2.5)
    p13 = QtCore.QPointF(x+40, y+2.5)   
    icon_path_4.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5, p6, 
                                            p7, p8, p9, p10, p11, p12, p13]))
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.5 ))
    
    icon_5 = QtWidgets.QGraphicsPathItem()
    icon_path_5 = QtGui.QPainterPath() 
    p1 = QtCore.QPointF(x+5, y+22.5)
    p2 = QtCore.QPointF(x+7, y+22.5)
    p3 = QtCore.QPointF(x+7, y+16.5)
    p4 = QtCore.QPointF(x+11, y+16.5)
    p5 = QtCore.QPointF(x+14, y+22.5)
    p6 = QtCore.QPointF(x+16, y+22.5)
    p7 = QtCore.QPointF(x+16, y+16.5)
    p8 = QtCore.QPointF(x+20, y+16.5)
    p9 = QtCore.QPointF(x+27, y+16.5)
    p10 = QtCore.QPointF(x+27, y+22.5)
    p11 = QtCore.QPointF(x+35, y+22.5)
    p12 = QtCore.QPointF(x+35, y+16.5)
    p13 = QtCore.QPointF(x+40, y+19)   
    icon_path_5.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5, p6, 
                                            p7, p8, p9, p10, p11, p12, p13]))
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.5 ))
    
    icon_paths = [icon_2, icon_3, icon_4, icon_5]
    return icon_paths
        
        
        
        