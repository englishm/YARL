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
        self.infolay = QGridLayout()
        self.logbooklay = QGridLayout()
        self.timelay = QGridLayout()
        self.calllay = QGridLayout()

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

        # Logbook
        self.widgets['logbook'] = QGroupBox('Logbook')
        self.widgets['logbook-table'] = QTableWidget()
        self.widgets['logbook-refresh'] = QPushButton('Refresh Logbook')

        # log info
        self.widgets['call-box'] = QGroupBox('Callsign')
        self.widgets['date-box'] = QGroupBox('Date/Time')

        self.widgets['call'] = QLineEdit()
        self.widgets['call-info'] = QPushButton('Info')
        self.widgets['call-qrz'] = QPushButton('QRZ')

        self.widgets['date-time'] = QLineEdit()
        self.widgets['date-month'] = QLineEdit()
        self.widgets['date-day'] = QLineEdit()
        self.widgets['date-year'] = QLineEdit()
        self.widgets['date-get'] = QPushButton('Get time')
        self.widgets['date-reset'] = QPushButton('Reset time')

        # set signals
        self.widgets['call'].returnPressed.connect(self.lookupsig)
        self.widgets['logbook-refresh'].clicked.connect(self.load_table)
        self.widgets['date-get'].clicked.connect(self.timesig)
        self.widgets['date-reset'].clicked.connect(self.timeresetsig)
        self.widgets['call-qrz'].clicked.connect(self.qrzsig)

        # options
        self.widgets['call-info'].setDisabled(True)
        self.widgets['call-qrz'].setDisabled(True)

        self.widgets['date-time'].setPlaceholderText('Time')
        self.widgets['date-day'].setPlaceholderText('Day')
        self.widgets['date-month'].setPlaceholderText('Month')
        self.widgets['date-year'].setPlaceholderText('Year')

        self.widgets['date-day'].setFixedWidth(50)
        self.widgets['date-time'].setFixedWidth(50)
        self.widgets['date-month'].setFixedWidth(50)
        self.widgets['date-year'].setFixedWidth(50)

        self.widgets['date-time'].setValidator(QIntValidator())
        self.widgets['date-day'].setValidator(QIntValidator())
        self.widgets['date-month'].setValidator(QIntValidator())
        self.widgets['date-year'].setValidator(QIntValidator())

    def setup_layouts(self):

        # set layouts to widgets
        self.widgets['info'].setLayout(self.infolay)
        self.widgets['logbook'].setLayout(self.logbooklay)
        self.widgets['date-box'].setLayout(self.timelay)
        self.widgets['call-box'].setLayout(self.calllay)

        self.setViewLayout(self.layout)

    def build_view(self):
        '''
        # info
        self.infolay.addWidget(QLabel('Name'), 0, 0)
        self.infolay.addWidget(self.widgets['info-name'], 0, 1)
        self.infolay.addWidget(QLabel('Country'), 1, 0)
        self.infolay.addWidget(self.widgets['info-country'], 1, 1)
        self.infolay.addWidget(self.widgets['date-time'], 2, 0)
        self.infolay.addWidget(self.widgets['date-get'], 3, 0)
        self.infolay.setRowStretch(4, 4)
        '''

        # time layout
        self.timelay.addWidget(self.widgets['date-day'], 0, 0)
        self.timelay.addWidget(self.widgets['date-month'], 0, 1)
        self.timelay.addWidget(self.widgets['date-year'], 0, 2)
        self.timelay.addWidget(self.widgets['date-time'], 0, 3)
        self.timelay.addWidget(self.widgets['date-get'], 1, 0, 1, 2)
        self.timelay.addWidget(self.widgets['date-reset'], 1, 2, 1, 2)

        # callsign layout
        self.calllay.addWidget(self.widgets['call'], 0, 0, 1, 2)
        self.calllay.addWidget(self.widgets['call-info'], 1, 0)
        self.calllay.addWidget(self.widgets['call-qrz'], 1, 1)

        # main layout
        self.layout.addWidget(self.widgets['call-box'], 0, 0)
        self.layout.addWidget(self.widgets['date-box'], 0, 1)
        self.layout.addWidget(self.widgets['logbook'], 1, 0, 1, 3)

        # options
        self.layout.setRowStretch(3, 4)
        self.layout.setColumnStretch(2, 4)

        '''
        self.layout.addWidget(QLabel('Enter Callsign'), 0, 0)
        self.layout.addWidget(self.widgets['call'], 1, 0)
        self.layout.addWidget(self.widgets['info'], 0, 2)
        self.layout.addWidget(self.widgets['logbook-refresh'], 1, 1)
        self.layout.addWidget(self.widgets['logbook'], 2, 0, 1, 3)
        self.layout.setRowStretch(2, 4)
        self.layout.setColumnStretch(1, 1)
        '''

        # logbook
        self.logbooklay.addWidget(self.widgets['logbook-table'], 0, 0)

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
            self.widgets['call-info'].setDisabled(True)
            self.widgets['call-qrz'].setDisabled(True)
            self.setStatus('No call sign found')
            return
        except olerror.LookupVerificationError:
            self.logee = None
            self.widgets['call-info'].setDisabled(True)
            self.widgets['call-qrz'].setDisabled(True)
            self.setStatus('Login failed')
            return

        # set ui things
        self.setStatus('Callsign found')
        self.widgets['call-info'].setDisabled(False)
        self.widgets['call-qrz'].setDisabled(False)
        self.widgets['info'].setTitle('Info: ' + self.logee.callsign)
        self.widgets['info-call'].setText(self.logee.callsign)
        self.widgets['info-name'].setText(self.logee.name)
        self.widgets['info-country'].setText(self.logee.country)

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

    def timeresetsig(self):
        self.widgets['date-time'].setText('')
        self.widgets['date-day'].setText('')
        self.widgets['date-month'].setText('')
        self.widgets['date-year'].setText('')

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

        print(data)

        self.widgets['logbook-table'].setRowCount(len(data))
        self.widgets['logbook-table'].setColumnCount(len(cols))

        for i in range(0, len(cols)):
            self.widgets['logbook-table']\
                .setHorizontalHeaderItem(i, QTableWidgetItem(disp[keys[i]]))

        for i in range(0, len(data)):
            for j in range(0, len(cols)):
                self.widgets['logbook-table']\
                    .setItem(i, j, QTableWidgetItem(data[i][keys[j]]))
