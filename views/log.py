from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import webbrowser
from datetime import datetime
from sqlalchemy import Unicode, Integer, Float

from utils.multiview import View
from utils.onlinelookup import hamqth, olerror
from utils.dbconnector.dbconnector import DbConnector


class LogView(View):
    def __init__(self, mvp):
        super().__init__(mvp)
        self.loadMenu('config/log-menu.json')

        # variables
        self.ol = mvp.ol
        self.widgets = dict()
        self.logee = None

        # initialize layouts
        self.layout = QGridLayout()
        self.logbooklay = QGridLayout()
        self.timelay = QGridLayout()
        self.calllay = QGridLayout()
        self.replay = QGridLayout()

        # initalizerators
        self.setup_widgets()
        self.setup_layouts()
        self.build_view()

    def setup_widgets(self):
        # Logbook
        self.widgets['logbook'] = QGroupBox('Logbook')
        self.widgets['logbook-table'] = QTableWidget()
        self.widgets['logbook-refresh'] = QPushButton('Refresh Logbook')

        # log info
        self.widgets['call-box'] = QGroupBox('Callsign')
        self.widgets['date-box'] = QGroupBox('Date/Time (UTC)')
        self.widgets['rep-box'] = QGroupBox('Report')

        self.widgets['call'] = QLineEdit()
        self.widgets['call-more'] = QPushButton('More')
        self.widgets['call-qrz'] = QPushButton('QRZ')
        self.widgets['call-name'] = QLineEdit()
        self.widgets['call-loc'] = QLineEdit()

        self.widgets['date-time'] = QLineEdit()
        self.widgets['date-month'] = QLineEdit()
        self.widgets['date-day'] = QLineEdit()
        self.widgets['date-year'] = QLineEdit()
        self.widgets['date-get'] = QPushButton('Now')

        self.widgets['rep-sent'] = QLineEdit()
        self.widgets['rep-recv'] = QLineEdit()

        # set signals
        self.widgets['call'].returnPressed.connect(self.lookupsig)
        self.widgets['logbook-refresh'].clicked.connect(self.load_table)
        self.widgets['date-get'].clicked.connect(self.timesig)
        self.widgets['call-qrz'].clicked.connect(self.qrzsig)

        # options
        self.widgets['call-more'].setDisabled(True)
        self.widgets['call-qrz'].setDisabled(True)
        self.widgets['call'].setPlaceholderText('Call')
        self.widgets['call-loc'].setPlaceholderText('Location')
        self.widgets['call-name'].setPlaceholderText('Name')

        self.widgets['date-time'].setPlaceholderText('Time')
        self.widgets['date-day'].setPlaceholderText('Day')
        self.widgets['date-month'].setPlaceholderText('Month')
        self.widgets['date-year'].setPlaceholderText('Year')

        self.widgets['call-more'].setFixedWidth(50)
        self.widgets['call-qrz'].setFixedWidth(50)
        self.widgets['date-day'].setFixedWidth(50)
        self.widgets['date-time'].setFixedWidth(50)
        self.widgets['date-month'].setFixedWidth(50)
        self.widgets['date-year'].setFixedWidth(50)
        self.widgets['rep-sent'].setFixedWidth(30)
        self.widgets['rep-recv'].setFixedWidth(30)

        self.widgets['date-time'].setValidator(QIntValidator())
        self.widgets['date-day'].setValidator(QIntValidator())
        self.widgets['date-month'].setValidator(QIntValidator())
        self.widgets['date-year'].setValidator(QIntValidator())
        self.widgets['rep-sent'].setValidator(QIntValidator())
        self.widgets['rep-recv'].setValidator(QIntValidator())

        self.widgets['rep-sent'].setText('59')
        self.widgets['rep-recv'].setText('59')

    def setup_layouts(self):

        # set layouts to widgets
        self.widgets['logbook'].setLayout(self.logbooklay)
        self.widgets['date-box'].setLayout(self.timelay)
        self.widgets['call-box'].setLayout(self.calllay)
        self.widgets['rep-box'].setLayout(self.replay)

        self.setViewLayout(self.layout)

    def build_view(self):
        # time layout
        self.timelay.addWidget(QLabel('Date:'), 0, 0)
        self.timelay.addWidget(self.widgets['date-day'], 0, 1)
        self.timelay.addWidget(QLabel('/'), 0, 2)
        self.timelay.addWidget(self.widgets['date-month'], 0, 3)
        self.timelay.addWidget(QLabel('/'), 0, 4)
        self.timelay.addWidget(self.widgets['date-year'], 0, 5)
        self.timelay.addWidget(QLabel('Time:'), 1, 0)
        self.timelay.addWidget(self.widgets['date-time'], 1, 1)
        self.timelay.addWidget(self.widgets['date-get'], 1, 2, 1, 4)

        # callsign layout
        self.calllay.addWidget(self.widgets['call'], 0, 0)
        self.calllay.addWidget(self.widgets['call-loc'], 0, 1, 1, 2)
        self.calllay.addWidget(self.widgets['call-name'], 1, 0)
        self.calllay.addWidget(self.widgets['call-more'], 1, 1)
        self.calllay.addWidget(self.widgets['call-qrz'], 1, 2)

        # contact layout
        self.replay.addWidget(QLabel('Sent'), 0, 0)
        self.replay.addWidget(self.widgets['rep-sent'], 0, 1)
        self.replay.addWidget(QLabel('Received'), 1, 0)
        self.replay.addWidget(self.widgets['rep-recv'], 1, 1)

        # logbook
        self.logbooklay.addWidget(self.widgets['logbook-table'], 0, 0)
        self.load_table()

        # main layout
        self.layout.addWidget(self.widgets['call-box'], 0, 0)
        self.layout.addWidget(self.widgets['date-box'], 0, 1)
        self.layout.addWidget(self.widgets['rep-box'], 0, 2)
        self.layout.addWidget(self.widgets['logbook'], 1, 0, 1, 4)

        # options
        self.layout.setRowStretch(1, 4)
        self.layout.setColumnStretch(3, 4)

    # ## signals ## #

    def lookupsig(self):
        call = self.widgets['call'].text()

        if call == '':
            self.setStatus('no call to lookup')
            return

        try:
            self.logee = self.ol.lookup(call)
        except olerror.LookupResultError:
            self.logee = None
            self.widgets['call-more'].setDisabled(True)
            self.widgets['call-qrz'].setDisabled(True)
            self.setStatus('No call sign found')
            return
        except olerror.LookupVerificationError:
            self.logee = None
            self.widgets['call-more'].setDisabled(True)
            self.widgets['call-qrz'].setDisabled(True)
            self.setStatus('Login failed')
            return

        # set ui things
        self.setStatus('Callsign found')
        self.widgets['call-more'].setDisabled(False)
        self.widgets['call-qrz'].setDisabled(False)
        self.widgets['call'].setText(self.logee.callsign)
        self.widgets['call-name'].setText(self.logee.name)
        self.widgets['call-loc'].setText(self.logee.qth)

    def qrzsig(self):
        webbrowser.open(f'http://qrz.com/db/{self.logee.callsign}')

    def timesig(self):
        # extract date and time
        timestr = str(datetime.utcnow())
        times = timestr.strip().split()
        date = times[0].split('-')
        time = times[1]

        # set widgets
        self.widgets['date-day'].setText(date[2])
        self.widgets['date-month'].setText(date[1])
        self.widgets['date-year'].setText(date[0])
        self.widgets['date-time'].setText(time[:2] + time[3:5])

    def load_table(self):
        cols = [
            {'name': 'call', 'type': Unicode},
            {'name': 'name', 'type': Unicode},
            {'name': 'qth', 'type': Unicode},
            {'name': 'dxcc', 'type': Integer},
            {'name': 'freq', 'type': Float},
        ]
        disp = {'call': 'Callsign',
                'name': 'Name',
                'qth': 'QTH',
                'dxcc': 'DXCC Entity',
                'freq': 'Frequency'}

        keys = ['call', 'name', 'qth', 'dxcc', 'freq']

        data = [{
            'call': 'KB6EE/' + str(i),
            'name': 'test name',
            'qth': 'atlantis',
            'dxcc': str(13 + i),
            'freq': str(round(7.202 + i, 6))
        } for i in range(0, 50)]

        # print(data)

        self.widgets['logbook-table'].setRowCount(len(data))
        self.widgets['logbook-table'].setColumnCount(len(cols))

        for i in range(0, len(cols)):
            self.widgets['logbook-table']\
                .setHorizontalHeaderItem(i, QTableWidgetItem(disp[keys[i]]))

        for i in range(0, len(data)):
            for j in range(0, len(cols)):
                self.widgets['logbook-table']\
                    .setItem(i, j, QTableWidgetItem(data[i][keys[j]]))
