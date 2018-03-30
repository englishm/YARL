import sys, os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from utils.multiview import MultiView
from views.log import LogView
from views.sampleview import view1


class Yarl(MultiView):
    def __init__(self):
        super().__init__()
        self.title = 'Yet Another Radio Logger'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 400

        self.createMenuBar()
        self.createStatusBar()

        # init
        self.setWindow()
        self.setViews()

        self.setCentralWidget(self.getViewer())
        self.show()

    def setWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setViews(self):
        # initialize views
        self.logview = self.addView(LogView(self))
        self.tmp = self.addView(view1(self))

        # set first view
        # for now, the logview is the first
        self.setCurrentView(self.logview)


if __name__ == '__main__':
    # QT IT UP
    app = QApplication(sys.argv)

    # initalize classes
    win = Yarl()

    # execute, clean up, and exit
    sys.exit(app.exec_())
