"""
QPainterPath definition for tiem shift (electrical)
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):
    
    delta_time_sym = '\u0394' + 't'
    # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=768
    # (accessed June 25, 2020). 
    
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    font = QtGui.QFont("Arial", 10)
    font.setItalic(True)
    icon_path_1.addText(x, y, font, delta_time_sym)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.1))
    icon_1.setBrush(QtGui.QBrush(QtCore.Qt.blue))
       
    icon_paths = [icon_1]
    return icon_paths