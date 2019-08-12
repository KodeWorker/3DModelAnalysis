# -*- coding: utf-8 -*-
import sys
import psutil
import ctypes
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget, 
                             QLabel, QAction, QFileDialog, QActionGroup)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from gui.Canvas import CanvasView
from gui.Record import RecordBrowser
from gui.Dock import LeftRightDock
from gui.Multithreading import (MonitorThread)
from multiprocessing import freeze_support

import ConfigParser
import codecs

class ThreeDModelAnalysis(QMainWindow):
    
    def __init__(self):
        super(ThreeDModelAnalysis, self).__init__()
        self.initUI()
        
    def initUI(self):
        # parameters
        self.isLoad = False
        
        config = ConfigParser.ConfigParser()
        config.optionxform=str
        config.readfp(codecs.open('config/settings.conf', 'rb', "utf_8_sig"))
        
        self.title = config.get('TITLE', 'title')
        self.version = config.get('TITLE', 'version')
        
        self.backgroundColor = config.get('COLOR', 'backgroundColor')
        self.textColor = config.get('COLOR', 'textColor')
        self.blueprintColor = config.get('COLOR', 'blueprintColor')
        self.selLineColor = config.get('COLOR', 'selLineColor')
        self.delLineColor = config.get('COLOR', 'delLineColor')
        
        self.windowWidth = config.getfloat('WINDOW', 'windowWidth')
        self.windowHeight = config.getfloat('WINDOW', 'windowHeight')
        self.blueprintScale = config.getfloat('WINDOW', 'blueprintScale')
        self.drawLineWidth = config.getfloat('WINDOW', 'drawLineWidth')
        self.selLineWidth = config.getfloat('WINDOW', 'selLineWidth')
        
        self.monitor_sec = config.getint('CPU', 'monitor_sec')
        
        self.setWindowTitle(u'{} v{}'.format(self.title, self.version))   
        self.setWindowIcon(QIcon('assets/image/icon.png'))
        
        self.resize(self.windowWidth, self.windowHeight)
        center_point = QDesktopWidget().availableGeometry().center()
        self.frameGeometry().moveCenter(center_point)       
        
        self.canvas = CanvasView(self)
        self.canvasDock = LeftRightDock(u'Canvas', self)
        self.canvasDock.setWidget(self.canvas)
        self.addDockWidget(Qt.TopDockWidgetArea, self.canvasDock)
        
        self.record = RecordBrowser(self)
        self.recordDock = LeftRightDock(u'Info.', self)
        self.recordDock.setWidget(self.record)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.recordDock)

        self.initMenu()
        self.initTool()
        self.initStatus()
        
        # threadings
        self.monitorThread = MonitorThread(self.monitor_sec, self)
        self.monitorThread.start()
        
        self.show()
    
    def initMenu(self):
        self.OpenFileAct = QAction(QIcon('assets/image/open.png'), 'Open File', self)
        self.OpenFileAct.triggered.connect(self.OpenFile)
        self.OpenFileAct.setShortcut('Ctrl+O')
        
        self.menubar = self.menuBar()
        
        fileMenu = self.menubar.addMenu('File')
        fileMenu.addAction(self.OpenFileAct)
                
        self.TopViewAct = QAction(QIcon('assets/image/topview.png'), 'Top View', self)
        self.TopViewAct.triggered.connect(self.TopView)
        self.TopViewAct.setCheckable(True)
        self.FrontViewAct = QAction(QIcon('assets/image/frontview.png'), 'Front View', self)
        self.FrontViewAct.triggered.connect(self.FrontView)
        self.FrontViewAct.setCheckable(True)
        self.SideViewAct = QAction(QIcon('assets/image/sideview.png'), 'Side View', self)
        self.SideViewAct.triggered.connect(self.SideView)
        self.SideViewAct.setCheckable(True)
        
        ViewGroup = QActionGroup(self)
        ViewGroup.addAction(self.TopViewAct)
        ViewGroup.addAction(self.FrontViewAct)
        ViewGroup.addAction(self.SideViewAct)
        self.TopViewAct.setChecked(True)
        
        fileMenu = self.menubar.addMenu('View')
        fileMenu.addAction(self.TopViewAct)
        fileMenu.addAction(self.FrontViewAct)
        fileMenu.addAction(self.SideViewAct)
    
    def OpenFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open File', '', filter=self.tr('STEP Files (*.stp, *.step);;All Files (*)'))
        if filePath:
            self.isLoad = True
            self.canvas.scene.clear()
            self.record.insertText("[Open File] {}\n".format(filePath))
    
    def TopView(self):
        if self.isLoad:
            self.record.insertText("[Top View]\n")
            
    def FrontView(self):
        if self.isLoad:
            self.record.insertText("[Front View]\n")
            
    def SideView(self):
        if self.isLoad:
            self.record.insertText("[Side View]\n")
    
    def initTool(self):        
        pass
    
    def initStatus(self):
        self.statusbar = self.statusBar()
        self.memMessage = QLabel()
        self.cpuMessage = QLabel()
        self.memMessage.setAlignment(Qt.AlignRight)
        self.cpuMessage.setAlignment(Qt.AlignRight)
        
        self.showMemStatus(psutil.virtual_memory().percent)
        self.showCPUStatus(psutil.cpu_percent())
        self.statusbar.addPermanentWidget(self.memMessage)
        self.statusbar.addPermanentWidget(self.cpuMessage)
        
    def showMemStatus(self, percentage):
        self.memMessage.setText('mem. usage: <b>{}%</b>'.format(percentage))
        self.memMessage.update()
    
    def showCPUStatus(self, percentage):
        self.cpuMessage.setText('CPU usage: <b>{}%</b>'.format(percentage))
        self.cpuMessage.update()
    
    def closeEvent(self, event):
        self.monitorThread.terminate()
        
if __name__ == '__main__':
    freeze_support()
    
    # for taskbar icon
    appid = 'ThreeDModelAnalysis.app' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    app = QApplication(sys.argv)
    program = ThreeDModelAnalysis()
    sys.exit(app.exec_())