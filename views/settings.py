from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from utils.multiview import View
from utils.onlinelookup import hamqth, olerror


class SettingsView(View):
    def __init__(self, mvp):
        super().__init__(mvp)
        self.loadMenu('config/log-menu.json') # not sure how I feel about this

        # variables
        self.ol = mvp.ol

        self.setupWidgets()
        self.setupLayouts()
        self.buildView()
        self.startLookup()

    def setupWidgets(self):
        self.widgets = {}

        self.widgets['lookup-area'] = QGroupBox('HamQTH')
        self.widgets['lookup-status'] = QLabel('Status: Not activated')
        self.widgets['lookup-user'] = QLineEdit()
        self.widgets['lookup-pass'] = QLineEdit()
        self.widgets['lookup-set'] = QPushButton('Set')

        self.widgets['lookup-key'] = QLineEdit()
        self.widgets['lookup-key-button'] = QPushButton('Set Key')

        # set signals
        self.widgets['lookup-set'].clicked.connect(self.olconnectsig)
        self.widgets['lookup-key-button'].clicked.connect(self.olkeysig)

        # options
        self.widgets['lookup-pass'].setEchoMode(QtWidgets.QLineEdit.Password)

    def setupLayouts(self):
        # init layouts
        self.layout = QGridLayout()
        self.lookuplayout = QGridLayout()

        # set layouts
        self.setViewLayout(self.layout)
        self.widgets['lookup-area'].setLayout(self.lookuplayout)

    def buildView(self):
        # lookup area
        self.lookuplayout.addWidget(QLabel('Username'), 0,0)
        self.lookuplayout.addWidget(self.widgets['lookup-user'], 0,1)
        self.lookuplayout.addWidget(QLabel('Password'), 1,0)
        self.lookuplayout.addWidget(self.widgets['lookup-pass'], 1,1)
        self.lookuplayout.addWidget(self.widgets['lookup-set'], 2,0, 1,2)
        self.lookuplayout.addWidget(self.widgets['lookup-status'], 3,0, 1,2)

        # main layout
        self.layout.addWidget(self.widgets['lookup-area'], 0,0)

        # options
        self.layout.setColumnStretch(1,2)
        self.layout.setRowStretch(1,2)

    def startLookup(self):
        try:
            self.ol.connect()
            self.widgets['lookup-status'].setText('Status: Connected')
        except olerror.LookupVerificationError as e:
            self.widgets['lookup-status'].setText('Status: bad login')
        except olerror.NoLoginError as e:
            self.widgets['lookup-status'].setText('Status: No login found')
        except olerror.BadLoginError as e:
            self.widgets['lookup-status'].setText('Status: Bad login info')
        except olerror.BadFormatError as e:
            self.widgets['lookup-status'].setText('Status: Something happened')

    # ## signals ## #

    def olconnectsig(self):
        username = self.widgets['lookup-user'].text()
        password = self.widgets['lookup-pass'].text()

        self.ol.createLogin(username, password)
        self.startLookup()

    def olkeysig(self):
        self.ol.initkey(self.widgets['lookup-key'].text())
