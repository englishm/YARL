"""
This module provides a class that handles exporting a database to .adx format.
"""

import os
from datetime import datetime
from xml.etree.ElementTree import Element, ElementTree  # should be all we need


def _add_tag(parent, name, data=None, attributes={}):
    """
    Function to add a new element to a parent element.

    :param parent: Tag to add subtag to
    :param name: Name of the new element
    :param data: Content of the new element (default None)
    :param attributes: Dictionary of attributes of the new element (default {})
    :return: The newly created element
    """
    new_tag = Element(name, attributes)
    if data is not None:
        new_tag.text = data
    parent.append(new_tag)
    return new_tag


class ADIFExportError(Exception):
    """Raised when there is an error exporting to an .adx file."""


class ADXFile:
    """
    This class provides an API for exporting QSO information to a .adx file.

    This class provides 3 functions that can be called to add QSO information
    to a .adx file. The file that will be written to is passed in as a path
    during instantiation. The class checks if the path is OK to use, and if it
    is, you can then use
    """

    def __init__(self, file):
        """
        Create a new ADXFile that can be used to export QSOs into ADX files.

        :param file: Location to create file at.
        :return: None
        """
        # we're going to throw an error if the location to export to already
        # exists. It shouldn't, if the GUI is done right, but that's ok.
        if not os.path.exists(file):
            self.location = file
        else:
            raise FileExistsError("The location you'd like to export to "
                                  f"already exists. (got: {file})")

        self._tree = ElementTree(Element("ADX"))  # add the root element, <ADX>
        self._root = self._tree.getroot()  # use _add_tag() to add a subtag
        self._in_records = False  # are we currently writing records?
        self._records = None  # root tag for records
        self._header_written = False

    def write_header(self, _adif_ver="3.0.8", _app_name="YARL"):
        """
        Write the header for an .adx file.

        :param _adif_ver: ADIF version. (Default '3.0.8')
        :param _app_name: Name of the application. Default "YARL"
        :return: None
        :raise: ADIFExportError if called twice.
        """
        if self._header_written:
            raise ADIFExportError(
                "Attempted adding header to file which already had a header")
        if self._in_records:
            raise ADIFExportError(
                "Cannot add header while we're already writing records")
            # Technically, it is possible, but it is not defined in the ADIF
            # documentation if it can be added to the end (which is where it
            # would be added (I think))

        header = _add_tag(self._root, "HEADER")
        _add_tag(header, "ADIF_VER", _adif_ver)
        _add_tag(header, "PROGRAMID", _app_name)
        _add_tag(parent=header,
                 name="APP",
                 data=datetime.now().__str__(),
                 attributes={
                            "PROGRAMID": _app_name,
                            "FIELDNAME": "GEN_TIME",  # time file was written
                            "TYPE": "S",  # S data type indicator for string
                            }
                 )
        self._header_written = True

    def write_record(self, data: dict):
        """Add a new record to the file to be exported."""
        if not self._in_records and self._records is None:
            self._records = _add_tag(self._root, "RECORDS")
            self._in_records = True
        current_record = _add_tag(self._records, "RECORD")
        for key in data:  # next line: TODO: custom fields, metadata
            modified_key = key.upper().replace(" ", "_")
            modified_data = data[key]
            if type(modified_data) != str:
                modified_data = str(modified_data)
            _add_tag(current_record, name=modified_key, data=modified_data)

    def write_file(self):
        """Write the final tree to file."""
        if os.path.exists(self.location):
            raise FileExistsError("The location you'd like to export to "
                                  f"already exists. (got: {self.location})")
        self._tree.write(self.location)
        return True
