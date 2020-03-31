"""
QPainterPath definition for phase shifter (optical)
"""

from PyQt5 import QtCore, QtGui, QtWidgets



def run (x, y):
    
    #phi_sym = '\u03D5'
    #https://pythonforundergradengineers.com/unicode-characters-in-python.html
    #(accessed 24 Apr 2019)
    # https://en.wikipedia.org/wiki/Phi (accessed 24 Apr 2019)
    
    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    font = QtGui.QFont("Arial", 11)
    font.setItalic(True)
    icon_path_1.addText(x, y-2, font, 'y')
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.25))
    icon_1.setBrush(QtGui.QBrush(QtCore.Qt.blue))
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x-5, y-15)
    p2 = QtCore.QPointF(x-5, y+3)
    p3 = QtCore.QPointF(x-3, y+1)
    p4 = QtCore.QPointF(x-7, y+1)
    p5 = QtCore.QPointF(x-5, y+3)
    icon_path_2.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4, p5]))  
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    icon_2.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath()
    p1 = QtCore.QPointF(x-5, y-15)
    p2 = QtCore.QPointF(x-3, y-13)
    p3 = QtCore.QPointF(x-7, y-13)
    p4 = QtCore.QPointF(x-5, y-15)
    icon_path_3.addPolygon(QtGui.QPolygonF([p1, p2, p3, p4]))  
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 0.75 ))
    icon_3.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))    
      
    icon_paths = [icon_1, icon_2, icon_3]
    return icon_paths