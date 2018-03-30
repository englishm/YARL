"""Unit tests for the exports/adx.py module."""

import os
import sys
import unittest
sys.path.append("..")
from exports.adx import ADXFile, ADIFExportError

test_path = "test_export.adx"


class TestADXFile(unittest.TestCase):
    def test_creation(self):
        if os.path.exists(test_path):
            # rip that file
            os.remove(test_path)

        test_file = ADXFile(test_path)
        self.assertIsInstance(test_file, ADXFile)

    def test_creation_fail(self):
        if not os.path.exists(test_path):
            open(test_path, "w+").close()
        try:
            e = ADXFile(test_path)
        except Exception as f:
            e = f
        else:
            e = None
        finally:
            self.assertIsInstance(e, FileExistsError)

    def test_write_fail(self):
        if os.path.exists(test_path):
            os.remove(test_path)
        file = ADXFile(test_path)
        file.write_header()
        open(test_path, "w+").close()
        try:
            e = file.write_file()
        except Exception as f:
            e = f
        else:
            e = None
        finally:
            self.assertIsInstance(e, FileExistsError)

    def test_double_header_fail(self):
        if os.path.exists(test_path):
            os.remove(test_path)
        file = ADXFile(test_path)
        file.write_header()
        try:
            e = file.write_header()
        except Exception as f:
            e = f
        else:
            e = None
        finally:
            self.assertIsInstance(e, ADIFExportError)

if __name__ == "__main__":
    unittest.main()
