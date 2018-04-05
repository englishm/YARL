from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from utils.multiview import View
from utils.onlinelookup import hamqth, olerror


class SettingsView(View):
    def __init__(self, mvp):
        super().__init__(mvp)
        self.loadMenu('config/log-menu.json')

        # variables
        self.ol = mvp.ol

        self.setup_widgets()
        self.setup_layouts()
        self.build_view()
        self.start_lookup()

    def setup_widgets(self):
        self.widgets = {}

        self.widgets['lookup-area'] = QGroupBox('HamQTH')
        self.widgets['lookup-status'] = QLabel('Status: Not activated')
        self.widgets['lookup-user'] = QLineEdit()
        self.widgets['lookup-pass'] = QLineEdit()
        self.widgets['lookup-set'] = QPushButton('Set')

        # set signals
        self.widgets['lookup-set'].clicked.connect(self.olconnectsig)
        self.widgets['lookup-pass'].returnPressed.connect(self.olconnectsig)

        # options
        self.widgets['lookup-pass'].setEchoMode(QtWidgets.QLineEdit.Password)

    def setup_layouts(self):
        # init layouts
        self.layout = QGridLayout()
        self.lookuplayout = QGridLayout()

        # set layouts
        self.setViewLayout(self.layout)
        self.widgets['lookup-area'].setLayout(self.lookuplayout)

    def build_view(self):
        # lookup area
        self.lookuplayout.addWidget(QLabel('Username'), 0, 0)
        self.lookuplayout.addWidget(self.widgets['lookup-user'], 0, 1)
        self.lookuplayout.addWidget(QLabel('Password'), 1, 0)
        self.lookuplayout.addWidget(self.widgets['lookup-pass'], 1, 1)
        self.lookuplayout.addWidget(self.widgets['lookup-set'], 2, 0, 1, 2)
        self.lookuplayout.addWidget(self.widgets['lookup-status'], 3, 0, 1, 2)

        # main layout
        self.layout.addWidget(self.widgets['lookup-area'], 0, 0)

        # options
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(1, 2)

    def start_lookup(self):
        try:
            self.ol.connect()
            self.widgets['lookup-status'].setText('Status: Connected')
        except olerror.LookupVerificationError as e:
            self.widgets['lookup-status'].setText('Status: Not connected')

    # ## signals ## #

    def olconnectsig(self):
        username = self.widgets['lookup-user'].text()
        password = self.widgets['lookup-pass'].text()

        self.ol.create_login(username, password)
        self.start_lookup()
