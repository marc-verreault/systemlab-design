"""
QPainterPath definition for Integrate and Dump
"""

from PyQt5 import QtCore, QtGui, QtWidgets



def run (x, y):
    
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    font = QtGui.QFont("Arial", 8)
    font.setItalic(True)
    icon_path_1.addText(x+4, y+4, font, "dt")
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.25 ))
    icon_1.setBrush(QtGui.QBrush(QtCore.Qt.black))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    icon_path_2.moveTo(x-5, y+15)
    icon_path_2.cubicTo(x-1, y+20, x+1, y-20, x+5, y-15) #x1,y1,x2,y2,x_end,y_end
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 1 ))
 
    icon_paths = [icon_1, icon_2]
    return icon_paths