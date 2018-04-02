#!/usr/bin/env python3
"""
Yet Another Radio Logger
Database Interface

Connects to a SQLite database
"""

from sqlalchemy import *


class DbConnector(object):
    def __init__(self, filename: str, name: str, columns: list,
                 path: str = ''):
        """
        Initialize a SQLite database with a table

        If the SQLite database file does not exist, it is created. Otherwise,
        it is accessed. A table is created within the database, or opened if
        it exists.

        :param filename: the filename for the database (without extension)
        :param name: the name of the table to be opened
        :param columns: a list of dictionaries describing the columns for the
            table being created. Each dictionary should have the format:
            `{'key': 'columnName', 'datatype': sqlalchemyType}`
            The sqlalchemy Column types are listed here:
            http://docs.sqlalchemy.org/en/latest/core/type_basics.html
        :param path: the absolute path to the database file. If not given,
            the default is '' (the current directory).
        """
        self.rows = None
        self.table = None

        self.db = create_engine('sqlite:///' + path + filename + '.db')

        if __debug__:
            self.db.echo = True

        self.meta = MetaData(self.db)
        self.open_table(name, columns)

    def open_table(self, name: str, columns: list):
        """
        If the table exists, load it; otherwise, create it

        :param name: the name of the table to be opened
        :param columns: a list of dictionaries describing the columns for the
            table being created. Each dictionary should have the format:
            `{'key': 'columnName', 'datatype': sqlalchemyType}`
            The sqlalchemy Column types are listed here:
            http://docs.sqlalchemy.org/en/latest/core/type_basics.html
        """
        if self.db.has_table(name):
            self.table = Table(name, self.meta,
                               keep_existing=True,
                               autoload=True,
                               autoload_with=self.db
                               )
        else:
            self.table = Table(name, self.meta,
                               Column('id', Integer, primary_key=True),
                               *[Column(col['name'], col['type'],
                                        default=null)
                                 for col in columns]
                               )
            self.table.create()

    def add_logs(self, logs):
        """
        Add a list of logs (dicts) to the table. Any column not filled should
        still have that key in the dictionary, but with a value of `None`.

        :param logs: a list of dicts of log entries
        """
        ins = self.table.insert()
        ins.execute(*logs)

    def get_logs(self):
        """
        Gets all logs in the table (for now)

        TODO: add WHERE clauses for filtering
        TODO: add select first n records
        """
        sel = self.table.select()
        logs = sel.execute()
        self.rows = [dict(r) for r in logs]

    def update_log(self, row_id, new_data):
        """
        Updates a log entry with new data

        :param row_id: the value of the 'id' column in the desired row
        :param new_data: a dictionary of any new values for that row
        """
        upd = self.table.update().where(self.table.c.id == row_id)\
                                 .values(new_data)
        upd.execute()


if __name__ == '__main__':
    # Testing code for the DbConnector class

    c = [{'name': 'callsign', 'type': String(40)},
         {'name': 'frequency', 'type': Float},
         ]

    # d creates/accesses the file test.db
    # and creates/accesses the table testlog
    d = DbConnector('test', 'testlog', c)
    # e creates another object accessing test.db
    # and creates/accesses another table, test2
    e = DbConnector('test', 'test2', c)

    data = [{'callsign': 'KB6EE', 'frequency': 7.4004},
            {'callsign': 'N0SSC', 'frequency': 14.07070},
            {'callsign': 'KZ0P', 'frequency': 14.070150},
            {'callsign': 'KB6EE', 'frequency': None},
            {'callsign': 'KZ0P', 'frequency': 14.070150},
            ]

    d.add_logs(data)
    d.get_logs()
    e.add_logs(data)
    e.get_logs()

    new_log = {'callsign': 'KX0P'}

    d.update_log('3', new_log)

    print(d.table)
