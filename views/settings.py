from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import json

from utils.multiview import View
from utils.onlinelookup import hamqth, olerror


class SettingsView(View):
    def setup_view(self):
        # variables
        self.ol = self.parent.parent.ol

        self.enabled_fields = self.parent.access('log').enabled_fields
        self.fields = self.parent.access('log').fields

        # init layouts
        self.layout = QGridLayout()
        self.lookuplayout = QGridLayout()
        self.customlayout = QGridLayout()

        self.widgets = dict()

        self.setup_widgets()
        self.setup_layouts()
        self.build_view()
        self.start_lookup()

    def setup_widgets(self):
        # lookup
        self.widgets['lookup-box'] = QGroupBox('HamQTH')
        self.widgets['lookup-status'] = QLabel('Status: Not activated')
        self.widgets['lookup-user'] = QLineEdit()
        self.widgets['lookup-pass'] = QLineEdit()
        self.widgets['lookup-set'] = QPushButton('Set')

        # customize
        self.widgets['enabled-box'] = QGroupBox('Customize Layout')
        self.widgets['en-rep'] = QCheckBox('Report')
        self.widgets['en-freq'] = QCheckBox('Frequency')
        self.widgets['en-other'] = QCheckBox('Other')
        self.widgets['en-save'] = QPushButton('Save Layout')

        # set signals
        self.widgets['lookup-set'].clicked.connect(self.olconnectsig)
        self.widgets['lookup-pass'].returnPressed.connect(self.olconnectsig)

        self.set_checked()

        # options
        self.widgets['en-rep'].toggled\
            .connect(lambda: self.togglefield('en-rep', 'rep-box'))
        self.widgets['en-freq'].toggled\
            .connect(lambda: self.togglefield('en-freq', 'freq-box'))
        self.widgets['en-other'].toggled\
            .connect(lambda: self.togglefield('en-other', 'other-box'))
        self.widgets['en-save'].clicked.connect(self.laysavesig)
        self.widgets['lookup-pass'].setEchoMode(QtWidgets.QLineEdit.Password)

    def setup_layouts(self):
        # set layouts
        self.set_layout(self.layout)
        self.widgets['lookup-box'].setLayout(self.lookuplayout)
        self.widgets['enabled-box'].setLayout(self.customlayout)

    def build_view(self):
        # lookup area
        self.lookuplayout.addWidget(QLabel('Username'), 0, 0)
        self.lookuplayout.addWidget(self.widgets['lookup-user'], 0, 1)
        self.lookuplayout.addWidget(QLabel('Password'), 1, 0)
        self.lookuplayout.addWidget(self.widgets['lookup-pass'], 1, 1)
        self.lookuplayout.addWidget(self.widgets['lookup-set'], 2, 0, 1, 2)
        self.lookuplayout.addWidget(self.widgets['lookup-status'], 3, 0, 1, 2)

        # customize area
        self.customlayout.addWidget(self.widgets['en-rep'], 0, 0)
        self.customlayout.addWidget(self.widgets['en-freq'], 1, 0)
        self.customlayout.addWidget(self.widgets['en-other'], 2, 0)
        self.customlayout.addWidget(self.widgets['en-save'], 4, 0)

        # main layout
        self.layout.addWidget(self.widgets['lookup-box'], 0, 0)
        self.layout.addWidget(self.widgets['enabled-box'], 1, 0)

        # options
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(1, 2)
        self.customlayout.setRowStretch(3, 4)

    def set_checked(self):
        for i in self.fields['enabled']:
            print(i)
            box = str(self.fields['enabled'][i])
            print(box)
            if box in self.widgets:
                print('yay')
                print(self.widgets[box])
                self.widgets[box].setChecked(True)
        for i in self.fields['disabled']:
            if i in self.parent.access('log').widgets:
                self.parent.access('log').widgets[i].setVisible(False)

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

    def togglefield(self, caller, field):
        if field in self.fields['enabled']:
            # set abled status
            tmpd = self.fields['enabled'][field]
            del self.fields['enabled'][field]
            self.fields['disabled'][field] = tmpd

            # do the thing
            self.parent.access('log').widgets[field].setVisible(False)
            print(field, 'now off...', self.fields['enabled'])
        elif field in self.fields['disabled']:
            # set abled status
            tmpd = self.fields['disabled'][field]
            del self.fields['disabled'][field]
            self.fields['enabled'][field] = tmpd

            self.parent.access('log').widgets[field].setVisible(True)
            print(field, 'now on...', self.fields['disabled'])

    def laysavesig(self):
        with open('config/log-layout.json', 'w') as f:
            json.dump(self.fields, f)
