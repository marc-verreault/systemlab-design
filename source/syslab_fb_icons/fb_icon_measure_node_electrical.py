"""
QPainterPath definition for optical noise generator

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addEllipse(x-12.5, y-12.5, 12.5, 12.5)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 1 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor('#f5f5f5')))
    #icon_1.setOpacity(0.5)
    
    icon_paths = [icon_1]
    return icon_paths