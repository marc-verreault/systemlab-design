"""
QPainterPath definition for ADC (Electrical)
"""

from PyQt5 import QtCore, QtGui, QtWidgets



def run (x, y):  
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    font = QtGui.QFont("Arial", 10)
    font.setItalic(True)
    icon_path_1.addText(x, y, font, "A/D")
    icon_1.setPath(icon_path_1)
    icon_1.setBrush(QtGui.QBrush(QtCore.Qt.black))
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.1 ))
       
    icon_paths = [icon_1]
    return icon_paths