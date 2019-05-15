"""
QPainterPath definition for optical cross coupler

"""

from PyQt5 import QtCore, QtGui, QtWidgets

def run (x, y):

    icon_1 = QtWidgets.QGraphicsPathItem()
    icon_path_1 = QtGui.QPainterPath() 
    icon_path_1.addRect(x, y, 14, 4) #x,y,w,h
    icon_1.setPath(icon_path_1)
    icon_1.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    icon_1.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkRed)))
    icon_1.setOpacity(0.7)
    
    icon_2 = QtWidgets.QGraphicsPathItem()
    icon_path_2 = QtGui.QPainterPath() 
    icon_path_2.moveTo(x-12, y-4)
    icon_path_2.cubicTo(x-6, y-4, x-4, y+1.5, x, y+1.5) #x1,y1,x2,y2,x_end,y_end
    icon_2.setPath(icon_path_2)
    icon_2.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 )) 
    
    icon_3 = QtWidgets.QGraphicsPathItem()
    icon_path_3 = QtGui.QPainterPath() 
    icon_path_3.moveTo(x-12, y+9)
    icon_path_3.cubicTo(x-6, y+9, x-4, y+3, x, y+3) #x1,y1,x2,y2,x_end,y_end
    icon_3.setPath(icon_path_3)
    icon_3.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_4 = QtWidgets.QGraphicsPathItem()
    icon_path_4 = QtGui.QPainterPath() 
    icon_path_4.moveTo(x+14, y+1.5)
    icon_path_4.cubicTo(x+20, y+1.5, x+22, y-4, x+26, y-4) #x1,y1,x2,y2,x_end,y_end
    icon_4.setPath(icon_path_4)
    icon_4.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_5 = QtWidgets.QGraphicsPathItem()
    icon_path_5 = QtGui.QPainterPath() 
    icon_path_5.moveTo(x+14, y+3)
    icon_path_5.cubicTo(x+20, y+3, x+22, y+9, x+26, y+9) #x1,y1,x2,y2,x_end,y_end
    icon_5.setPath(icon_path_5)
    icon_5.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.darkRed), 0.75 ))
    
    icon_paths = [icon_1, icon_2, icon_3, icon_4, icon_5]
    return icon_paths
        
        
        
        