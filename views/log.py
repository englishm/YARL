from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from utils.multiview import View

class LogView(View):
    def __init__(self, mvp):
        super().__init__(mvp)
        self.loadMenu('config/log-menu.json')

        # variables
        self.ol = mvp.ol

        # initalizerators
        self.setupWidgets()
        self.setupLayouts()
        self.buildView()

    def setupWidgets(self):
        self.widgets = {}

        self.widgets['info'] = QGroupBox('Info')

        # info things
        self.widgets['info-call'] = QLineEdit()
        self.widgets['info-name'] = QLineEdit()
        self.widgets['info-country'] = QLineEdit()

        self.widgets['log-call'] = QLineEdit()

        # set signals
        self.widgets['log-call'].returnPressed.connect(self.lookupsig)

    def setupLayouts(self):
        # initialize layouts
        self.layout = QGridLayout()
        self.infolay = QGridLayout()

        # set layouts to widgets
        self.widgets['info'].setLayout(self.infolay)
        self.setViewLayout(self.layout)

    def buildView(self):
        # info
        self.infolay.addWidget(QLabel('Callsign'), 0,0)
        self.infolay.addWidget(self.widgets['info-call'], 0,1)
        self.infolay.addWidget(QLabel('Name'), 1,0)
        self.infolay.addWidget(self.widgets['info-name'], 1,1)
        self.infolay.addWidget(QLabel('Country'), 2,0)
        self.infolay.addWidget(self.widgets['info-country'], 2,1)

        self.infolay.setRowStretch(3,4)

        # main layout
        self.layout.addWidget(QLabel('Start with the callsign'), 0,0)
        self.layout.addWidget(self.widgets['log-call'], 1,0)
        self.layout.addWidget(self.widgets['info'], 0,2, 3,1)
        self.layout.setRowStretch(2,4)
        self.layout.setColumnStretch(1,1)

    ### signals ###

    def lookupsig(self):
        call = self.widgets['log-call'].text()

        if call == '':
            self.setStatus('no call to lookup')
            return

        result = self.ol.lookup(call)
        if result == None:
            self.setStatus('no call sign found')
            return

        self.widgets['info'].setTitle('Info: ' + result.callsign)
        self.widgets['info-call'].setText(result.callsign)
        self.widgets['info-name'].setText(result.name)
        self.widgets['info-country'].setText(result.country)
