# -*- coding: utf-8 -*-
# reference: 
#   1. https://stackoverflow.com/questions/14279162/qt-qgraphicsscene-drawing-arc
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsView)
from PyQt5.QtCore import (QSize)
from PyQt5.QtGui import (QColor, QPainter)
from PyQt5.QtOpenGL import (QGLWidget, QGLFormat, QGL)
        
class CanvasScene(QGraphicsScene):
    
    def __init__(self, parent):
        super(CanvasScene, self).__init__()
        self.parent = parent
        self.initScene()
        
    def initScene(self, x=0, y=0):
        self.setBackgroundBrush(QColor(self.parent.parent.backgroundColor))
                
    def mousePressEvent(self, event):
        # 滑鼠點擊
        pass
    
    def mouseReleaseEvent(self, event):
        # 滑鼠釋放
        pass
                    
    def mouseMoveEvent(self, event):
        # 滑鼠移動
        pass
    
class CanvasView(QGraphicsView):
    
    def __init__(self, parent):
        super(CanvasView, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setMouseTracking(True)
        self.scene = CanvasScene(self)
        self.setScene(self.scene)        
        self.ratio = 1
        
        # OpenGL
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setOptimizationFlags(QGraphicsView.DontSavePainterState);
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse);
        
        self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers | QGL.DirectRendering), self))
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.update()
                
    def sizeHint(self):
        return QSize(self.parent.windowWidth, self.parent.windowHeight*0.75)
    
    def keyPressEvent(self, event):
        if event.nativeScanCode() == 78 or event.nativeScanCode() == 13:            
            self.ratio *= 2
            self.scale(2, 2)
            self.scene.update()
            self.parent.record.insertText(u'Zoom In: {:.2f}%\n'.format(self.ratio*100))
            
        elif event.nativeScanCode() == 74 or event.nativeScanCode() == 12:            
            self.ratio *= .5
            self.scale(.5, .5)
            self.scene.update()
            self.parent.record.insertText(u'Zoom Out: {:.2f}%\n'.format(self.ratio*100))