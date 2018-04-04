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
        self.widgets = dict()

        # initialize layouts
        self.layout = QGridLayout()
        self.infolay = QGridLayout()
        self.logbooklay = QGridLayout()

        # initalizerators
        self.setup_widgets()
        self.setup_layouts()
        self.build_view()

    def setup_widgets(self):
        self.widgets['info'] = QGroupBox('Info')

        # info things
        self.widgets['info-call'] = QLineEdit()
        self.widgets['info-name'] = QLineEdit()
        self.widgets['info-country'] = QLineEdit()

        self.widgets['log-call'] = QLineEdit()

        # Logbook
        self.widgets['logbook'] = QGroupBox('Logbook')
        self.widgets['logbook-table'] = QTableWidget()
        self.widgets['logbook-table'].setRowCount(5)
        self.widgets['logbook-table'].setColumnCount(5)

        # set signals
        self.widgets['log-call'].returnPressed.connect(self.lookupsig)

    def setup_layouts(self):

        # set layouts to widgets
        self.widgets['info'].setLayout(self.infolay)
        self.widgets['logbook'].setLayout(self.logbooklay)

        self.setViewLayout(self.layout)

    def build_view(self):
        # info
        self.infolay.addWidget(QLabel('Name'), 0, 0)
        self.infolay.addWidget(self.widgets['info-name'], 0, 1)
        self.infolay.addWidget(QLabel('Country'), 1, 0)
        self.infolay.addWidget(self.widgets['info-country'], 1, 1)

        self.infolay.setRowStretch(2, 4)

        # main layout
        self.layout.addWidget(QLabel('Enter Callsign'), 0, 0)
        self.layout.addWidget(self.widgets['log-call'], 1, 0)
        self.layout.addWidget(self.widgets['info'], 0, 2)
        self.layout.addWidget(self.widgets['logbook'], 2, 0, 1, 3)
        self.layout.setRowStretch(2, 4)
        self.layout.setColumnStretch(1, 1)

        # logbook
        self.logbooklay.addWidget(self.widgets['logbook-table'], 0, 0)

    # ## signals ## #

    def lookupsig(self):
        call = self.widgets['log-call'].text()

        if call == '':
            self.setStatus('no call to lookup')
            return

        result = self.ol.lookup(call)
        if result is None:
            self.setStatus('no call sign found')
            return

        self.setStatus('Callsign found')
        self.widgets['info'].setTitle('Info: ' + result.callsign)
        self.widgets['info-call'].setText(result.callsign)
        self.widgets['info-name'].setText(result.name)
        self.widgets['info-country'].setText(result.country)
