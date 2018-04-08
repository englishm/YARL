from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from utils.multiview import View
from utils.onlinelookup import hamqth, olerror


class SettingsView(View):
    def setup_view(self):
        # variables
        self.ol = self.parent.parent.ol

        self.enabled_fields = self.parent.access('log').enabled_fields

        # init layouts
        self.layout = QGridLayout()
        self.lookuplayout = QGridLayout()
        self.enabledlayout = QGridLayout()

        self.widgets = dict()

        self.setup_widgets()
        self.setup_layouts()
        self.build_view()
        self.start_lookup()

    def setup_widgets(self):
        self.widgets['lookup-box'] = QGroupBox('HamQTH')
        self.widgets['lookup-status'] = QLabel('Status: Not activated')
        self.widgets['lookup-user'] = QLineEdit()
        self.widgets['lookup-pass'] = QLineEdit()
        self.widgets['lookup-set'] = QPushButton('Set')

        self.widgets['enabled-box'] = QGroupBox('Toggle Sections')
        self.widgets['en-rep'] = QCheckBox('Enable Report')
        self.widgets['en-freq'] = QCheckBox('Enable Frequency')
        self.widgets['en-other'] = QCheckBox('Enable Other')

        self.widgets['set-call'] = QWidget()
        self.widgets['set-date'] = QWidget()
        self.widgets['set-rep'] = QWidget()
        self.widgets['set-freq'] = QWidget()
        self.widgets['set-other'] = QWidget()

        self.widgets['set'] = QToolBox()

        self.widgets['set'].insertItem(0, self.widgets['set-call'], 'Callsign')
        self.widgets['set'].insertItem(1, self.widgets['set-date'],
                                       'Date/Time')
        self.widgets['set'].insertItem(2, self.widgets['set-rep'], 'Report')
        self.widgets['set'].insertItem(3, self.widgets['set-freq'],
                                       'Frequency')
        self.widgets['set'].insertItem(4, self.widgets['set-other'], 'Other')

        # set signals
        self.widgets['lookup-set'].clicked.connect(self.olconnectsig)
        self.widgets['lookup-pass'].returnPressed.connect(self.olconnectsig)

        # self.widgets['en-time'].toggled\
        #    .connect(lambda: self.togglefield('date-box'))
        # self.widgets['en-call'].toggled\
        #    .connect(lambda: self.togglefield('call-box'))
        self.widgets['en-rep'].toggled\
            .connect(lambda: self.togglefield('rep-box'))
        self.widgets['en-freq'].toggled\
            .connect(lambda: self.togglefield('freq-box'))
        self.widgets['en-other'].toggled\
            .connect(lambda: self.togglefield('other-box'))

        # options
        self.widgets['lookup-pass'].setEchoMode(QtWidgets.QLineEdit.Password)

    def setup_layouts(self):
        # view set layouts
        self.lcall = QVBoxLayout()
        self.ldate = QVBoxLayout()
        self.lrep = QVBoxLayout()
        self.lfreq = QVBoxLayout()
        self.lother = QVBoxLayout()

        # set layouts
        self.set_layout(self.layout)
        self.widgets['lookup-box'].setLayout(self.lookuplayout)
        self.widgets['enabled-box'].setLayout(self.enabledlayout)
        self.widgets['set-call'].setLayout(self.lcall)
        self.widgets['set-date'].setLayout(self.ldate)
        self.widgets['set-rep'].setLayout(self.lrep)
        self.widgets['set-freq'].setLayout(self.lfreq)
        self.widgets['set-other'].setLayout(self.lother)

    def build_view(self):
        # lookup area
        self.lookuplayout.addWidget(QLabel('Username'), 0, 0)
        self.lookuplayout.addWidget(self.widgets['lookup-user'], 0, 1)
        self.lookuplayout.addWidget(QLabel('Password'), 1, 0)
        self.lookuplayout.addWidget(self.widgets['lookup-pass'], 1, 1)
        self.lookuplayout.addWidget(self.widgets['lookup-set'], 2, 0, 1, 2)
        self.lookuplayout.addWidget(self.widgets['lookup-status'], 3, 0, 1, 2)

        self.lrep.addWidget(self.widgets['en-rep'])
        # self.enabledlayout.addWidget(self.widgets['en-call'], 1, 0)
        self.lfreq.addWidget(self.widgets['en-freq'])
        self.lother.addWidget(self.widgets['en-other'])

        self.enabledlayout.addWidget(self.widgets['set'], 0, 0)

        # main layout
        self.layout.addWidget(self.widgets['lookup-box'], 0, 0)
        self.layout.addWidget(self.widgets['enabled-box'], 1, 0)

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

    def togglefield(self, field):
        if field in self.enabled_fields:
            self.parent.access('log').widgets[field].setVisible(False)
            self.enabled_fields.remove(field)
            print(field, 'now off...', self.enabled_fields)
        else:
            self.parent.access('log').widgets[field].setVisible(True)
            self.enabled_fields.remove(field)
            print(field, 'now on...', self.enabled_fields)
