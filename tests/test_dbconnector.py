import os
import sys
import unittest
sys.path.append('..')
from dbconnector import DbConnector
from sqlalchemy import *


class TestDbConnector(unittest.TestCase):
    def setUp(self):
        c = [{'name': 'call', 'type': Unicode},
             {'name': 'freq', 'type': Float},
             {'name': 'band', 'type': Unicode},
             {'name': 'dxcc', 'type': Integer},
             {'name': 'lat', 'type': Float},
             {'name': 'lon', 'type': Float},
             ]

        self.d = DbConnector('test_dbconnector', 'testlog', c)

        self.data = [{
            'call': 'KB6EE/' + str(i),
            'freq': 14.070,
            'band': '20m',
            'dxcc': 291,
            'lat': 123.00201213,
            'lon': 72.12321
        } for i in range(0, 50)]

    def tearDown(self):
        os.remove('test_dbconnector.db')

    def test_create_db(self):
        # This is a kind of janky way to test this, but it'll do for now.

        self.assertEqual(
            str(self.d.meta),
            'MetaData(bind=Engine(sqlite:///test_dbconnector.db))'
        )
        self.assertEqual(str(self.d.table), 'testlog')

    def test_add_get_logs(self):
        self.d.add_logs(self.data)
        self.d.get_logs()

        expected = self.data
        i = 1
        for row in expected:
            row['id'] = i
            i += 1

        self.assertEqual(self.d.rows, expected)

    def test_update_log(self):
        new_data = {'freq': 7.200, 'band': '40m'}

        new_row = {'id': 5, 'call': 'KB6EE/4', 'freq': 7.200, 'band': '40m',
                   'dxcc': 291, 'lat': 123.00201213, 'lon': 72.12321}

        self.d.add_logs(self.data)
        self.d.update_log(5, new_data)
        self.d.get_logs()

        self.assertEqual(self.d.rows[4], new_row)


if __name__ == '__main__':
    unittest.main()
