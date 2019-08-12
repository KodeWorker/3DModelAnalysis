# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

class LeftRightDock(QDockWidget):

    def __init__(self, name, parent=None):
        super(LeftRightDock, self).__init__(parent)
        self.name = name
        self.parent = parent
        self.InitDock()
    
    def InitDock(self):
        self.setWindowTitle(self.name)
        self.setObjectName(self.name)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)