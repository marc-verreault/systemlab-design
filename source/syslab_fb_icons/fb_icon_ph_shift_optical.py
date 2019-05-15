"""
QPainterPath definition for phase shifter (optical)
"""

from PyQt5 import QtCore, QtGui, QtWidgets



def run (x, y):
    
    phi_sym = '\u03D5'
    #https://pythonforundergradengineers.com/unicode-characters-in-python.html
    #(accessed 24 Apr 2019)
    # https://en.wikipedia.org/wiki/Phi (accessed 24 Apr 2019)
    
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    font = QtGui.QFont("Arial", 12)
    font.setItalic(True)
    icon_path_1.addText(x, y, font, phi_sym)
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 0.25))
    icon_1.setBrush(QtGui.QBrush(QtCore.Qt.black))
       
    icon_paths = [icon_1]
    return icon_paths