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
    This class provides functions to read/write QSO info to/from .adx files.

    The class is first created with a filename to use, and a mode is given upon
    instantiation that defines the intended operation, whether it is to
    import or export data. Note that using export operations when the mode is
    set to import (and vice versa) yields undefined behavour, so don't try :)
    """

    def __init__(self, file, mode="export"):
        """
        Create a new ADXFile that can be used to export QSOs into ADX files.

        :param file: Location of file.
        :param mode: Set mode ("import" or "export"). Default "export".
        :return: None
        """

        self.file = file
        self.mode = mode
        if self.mode == "export":
            self._tree = ElementTree(Element("ADX"))  # add root element <ADX>
            self._root = self._tree.getroot()  # use _add_tag() to add a subtag
            self._in_records = False  # are we currently writing records?
            self._records = None  # root tag for records
            self._header_written = False
        if self.mode == "import":
            if not os.path.exists(self.file):
                raise FileNotFoundError("File to import does not exist! "
                                        f"(got: {self.file})")
            self._root = ElementTree.parse(ElementTree(), self.file)

    def get_header(self):
        """
        Get the header for the file being imported.

        :returns: List of dicts of tags in the header.
        """
        header = self._root.find("HEADER")
        data = []
        for tag in header:
            data.append({
                "tag": tag.tag,
                "attrib": tag.attrib,
                "data": tag.text,
            })
        return data

    def return_all_records(self):
        """
        Return all records listed in the .adx file.

        :returns: List of dicts of records.
        """
        records = []
        records_root = self._root.find("RECORDS")
        for record in records_root:
            dict_record = {}
            for field in record:
                dict_record[field.tag] = field.text
            records.append(dict_record)
        return records

    def write_header(self, _adif_ver="3.0.8", _app_name="YARL"):
        """
        Write the header for an .adx file.

        :param _adif_ver: ADX version. (Default '3.0.8')
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
            # would be added (I think)
        header = _add_tag(self._root, "HEADER")
        _add_tag(header, "ADIF_VER", _adif_ver)
        _add_tag(header, "PROGRAMID", _app_name)
        _add_tag(parent=header,
                 name="APP",
                 data=datetime.now().__str__(),
                 attributes={
                     "PROGRAMID": _app_name,
                     "FIELDNAME": "GEN_TIME",
                     "TYPE": "S",
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
        if os.path.exists(self.file):
            raise FileExistsError("The location you'd like to export to "
                                  f"already exists. (got: {self.file})")
        self._tree.write(self.file, xml_declaration=True)
        return True
