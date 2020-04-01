from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys

class MainWindow(QMainWindow):

    def __init__(self, url):
        super(MainWindow, self).__init__()
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))

        self.setFixedWidth(1300)
        self.setFixedHeight(900)
        self.setCentralWidget(self.browser)
        
        self.show()
        self.setWindowTitle("Pollution Map")
        