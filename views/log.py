from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from utils.multiview import View

class LogView(View):
    def __init__(self, mvp):
        super().__init__(mvp)
        self.loadMenu('config/log-menu.json')

        # initalizerators
        self.setupWidgets()
        self.setupLayouts()
        self.buildView()

    def setupWidgets(self):
        self.widgets = {}

        self.widgets['example'] = QPushButton('Whee')
        self.widgets['form'] = QGroupBox('Form')

        # form things
        self.widgets['form-call'] = QLineEdit()
        self.widgets['form-name'] = QLineEdit()

    def setupLayouts(self):
        self.formlay = QFormLayout()
        # initialize layouts
        self.layout = QGridLayout()

        # set layouts to widgets
        self.widgets['form'].setLayout(self.formlay)
        self.setViewLayout(self.layout)

    def buildView(self):
        # form
        self.formlay.addRow("Callsign", self.widgets['form-call'])
        self.formlay.addRow("Name", QLineEdit())

        # main layout
        self.layout.addWidget(self.widgets['example'], 0,0, 1,2)
        self.layout.addWidget(self.widgets['form'], 1,0)
        self.layout.setColumnStretch(1,3)
