# Main script for YARL
# Yet Another Radio Logger

import sys
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from utils.multiview import MultiView
from utils.onlinelookup import hamqth, olerror
from views.log import LogView
from views.settings import SettingsView


class Yarl(QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # window variables
        self.title = 'Yet Another Radio Logger'
        self.left = 10
        self.top = 10
        self.width = 650
        self.height = 500

        # other variables
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

        # bars
        self.mb = self.menuBar()
        self.sb = self.statusBar()

    def setupWidgets(self):
        # widget time
        self.widgets = {}

        self.widgets['main'] = QWidget()
        self.widgets['settings'] = QPushButton('Settings')
        self.widgets['log'] = QPushButton('Log')

        self.mv = MultiView(self.mb, self.sb, self)

        # setup multiview
        self.mv.add_view('log', LogView(self.mv))
        self.mv.add_view('settings', SettingsView(self.mv))
        self.mv.set_view('log')

        # set signals
        self.widgets['settings'].clicked.connect(self.settingssig)
        self.widgets['log'].clicked.connect(self.logsig)

    def setupLayouts(self):
        self.layout = QGridLayout()

        self.widgets['main'].setLayout(self.layout)

    def build(self):
        self.layout.addWidget(self.widgets['log'], 0, 0)
        self.layout.addWidget(self.widgets['settings'], 0, 1)
        self.layout.addWidget(self.mv.get_widget(), 1, 0, 1, 3)

        # options
        self.layout.setColumnStretch(2, 4)

        # final thing
        self.setCentralWidget(self.widgets['main'])

    # ## signals ## #

    def settingssig(self):
        self.mv.set_view('settings')

    def logsig(self):
        self.mv.set_view('log')


if __name__ == '__main__':
    # QT IT UP
    app = QApplication(sys.argv)

    # initalize classes
    win = Yarl()

    # execute, clean up, and exit
    sys.exit(app.exec_())
