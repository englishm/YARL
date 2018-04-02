"""Unit tests for the exports/adx.py module."""

import os
import sys
import unittest
sys.path.append("..")
from exports.adx import ADXFile, ADIFExportError, \
    ModeMismatchException


class TestADXExport(unittest.TestCase):
    test_path = "test_export.adx"

    def setUp(self):
        if os.path.exists(self.test_path):
            # rip that file
            os.remove(self.test_path)

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_creation(self):
        test_file = ADXFile(self.test_path)
        self.assertIsInstance(test_file, ADXFile)

    def test_double_header_fail(self):
        file = ADXFile(self.test_path)
        file.write_header()
        try:
            e = file.write_header()
        except Exception as f:
            e = f
        else:
            e = None
        finally:
            self.assertIsInstance(e, ADIFExportError)

    def test_import_method_exceptions(self):
        file = ADXFile(self.test_path)
        self.assertRaises(ModeMismatchException, file.get_header)
        self.assertRaises(ModeMismatchException, file.return_all_records)


class TestADXImport(unittest.TestCase):
    test_path = "test_import.adx"

    correct_header = [{
        "tag": "ADIF_VER",
        "attrib": {},
        "data": "3.0.8",
    }, {
        "tag": "PROGRAMID",
        "attrib": {},
        "data": "YARL",
    }, {
        "tag": "APP",
        "attrib": {
            "FIELDNAME": "GEN_TIME",
            "PROGRAMID": "YARL",
            "TYPE": "S",
        },
        "data": "2018-03-31 18:26:32.373506",
    }]
    correct_records = [{
        'TIME': '2018-03-31 12:22:15.552211',
        'CALL': 'KB6EE'
    }, {
        'TIME': '2011-11-11 14:41:56.921583',
        'CALL': 'D0VKN'
    }]

    def test_header_read(self):
        file = ADXFile("test_import.adx", mode="import")
        header = file.get_header()
        self.assertCountEqual(header, self.correct_header)

    def test_record_read(self):
        file = ADXFile("test_import.adx", mode="import")
        records = file.return_all_records()
        self.assertCountEqual(records, self.correct_records)

    def test_import_method_exceptions(self):
        file = ADXFile("test_import.adx", mode="import")
        self.assertRaises(ModeMismatchException, file.write_header)
        self.assertRaises(ModeMismatchException, file.write_record, dict())
        self.assertRaises(ModeMismatchException, file.write_file)


if __name__ == "__main__":
    unittest.main()
