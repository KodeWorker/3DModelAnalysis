# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextBrowser

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QTextCursor

class RecordBrowser(QTextBrowser):
    
    def __init__(self, parent):
        super(RecordBrowser, self).__init__()
        self.parent = parent
        self.initRecord()
    
    def initRecord(self):
        self.setStyleSheet('background-color: {}; color: {};'.format(
                            self.parent.backgroundColor,
                            self.parent.textColor))
        self.setReadOnly(True)
        
    def refresh(self, message):
        self.clear()
        self.insertText(message)
    
    def insertText(self, string):
        textCursor = self.textCursor()
        textCursor.movePosition(
            QTextCursor.End,
            QTextCursor.MoveAnchor
        )
        textCursor.insertText(string)
        
        #顯示最新插入文字
        scollBar = self.verticalScrollBar()
        scollBar.setValue(scollBar.maximum())
        
    def sizeHint(self):
        return QSize(self.parent.windowWidth, self.parent.windowHeight*0.25)