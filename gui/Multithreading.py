# -*- coding: utf-8 -*-
import psutil
from PyQt5.QtCore import (QThread, pyqtSignal)

class MonitorThread(QThread):
    memUsageSlot = pyqtSignal(float)
    cpuUsageSlot = pyqtSignal(float)
    
    def __init__(self, secs ,parent):
        QThread.__init__(self)
        self.secs = secs
        self.parent = parent
        self.memUsageSlot.connect(self.parent.showMemStatus)
        self.cpuUsageSlot.connect(self.parent.showCPUStatus)
    
    def run(self):
        while True:
            self.sleep(self.secs)
            self.memUsageSlot.emit(psutil.virtual_memory().percent)
            self.cpuUsageSlot.emit(psutil.cpu_percent())