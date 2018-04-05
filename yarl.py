# Main script for YARL
# Yet Another Radio Logger

import sys, os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from utils.multiview import MultiView
from utils.onlinelookup import hamqth, olerror
from views.log import LogView
from views.settings import SettingsView


class Yarl(MultiView):
    def __init__(self):
        # formalities
        super().__init__()

        # variables
        self.title = 'Yet Another Radio Logger'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400

        # shared online lookup objectd
        self.ol = hamqth.HamQTHLookup()

        # setup
        self.setupWindow()
        self.setupWidgets()
        self.setupLayouts()
        self.build()

        # show
        self.show()

    def setupWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create the bars
        self.createMenuBar()
        self.createStatusBar()

    def setupWidgets(self):
        # widget time
        self.widgets = {}

        self.widgets['main'] = QWidget()
        self.widgets['settings'] = QPushButton('Settings')
        self.widgets['log'] = QPushButton('Log')

        # set signals
        self.widgets['settings'].clicked.connect(self.settingssig)
        self.widgets['log'].clicked.connect(self.logsig)

        # initialize views
        self.logview = self.addView(LogView(self))
        self.settingsview = self.addView(SettingsView(self))

        # set first view
        # for now, the logview is the first
        self.setCurrentView(self.logview)

    def setupLayouts(self):
        self.layout = QGridLayout()

        self.widgets['main'].setLayout(self.layout)

    def build(self):
        self.layout.addWidget(self.widgets['log'], 0, 0)
        self.layout.addWidget(self.widgets['settings'], 0, 1)
        self.layout.addWidget(self.getViewer(), 1, 0, 1, 3)

        # options
        self.layout.setColumnStretch(2, 4)

        # final thing
        self.setCentralWidget(self.widgets['main'])

    # ## signals ## #

    def settingssig(self):
        self.setCurrentView(self.settingsview)

    def logsig(self):
        self.setCurrentView(self.logview)


if __name__ == '__main__':
    # QT IT UP
    app = QApplication(sys.argv)

    # initalize classes
    win = Yarl()

    # execute, clean up, and exit
    sys.exit(app.exec_())
