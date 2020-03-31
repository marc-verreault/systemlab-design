"""
QPainterPath definition for electrical adder

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addEllipse(x-12.5, y-12.5, 25, 25)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
    icon_1.setOpacity(0.2)
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    icon_path_2.moveTo(x-9, y+5)
    icon_path_2.cubicTo(x-4, y+7, x-3, y-10, x, y-10) #x1,y1,x2,y2,x_end,y_end
    icon_path_2.moveTo(x, y-10)
    icon_path_2.cubicTo(x+4, y-10, x+4, y+7, x+9, y+5) #x1,y1,x2,y2,x_end,y_end
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    
    icon_paths = [icon_1, icon_2]
    return icon_paths