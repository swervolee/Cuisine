#!/usr/bin/python3
"""FILE STORAGE UNITTESTS"""
import inspect
import models
import pep8
import unittest
import json
FileStorage = models.engine.file_storage.FileStorage
from models.engine import file_storage
from models.base_model import BaseModel
classes = {"BaseModel": BaseModel}


class TestFileStorageDocs(unittest.TestCase):
    """Tests pycodestyle"""

    @classmethod
    def setUpClass(cls):
        """DOC TEST SET UP"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_file_storage(self):
        """TESTS PYCODESTYLE CONFORMANCE FOR FILE_STORAGE"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/file_storage.py"])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors in file_storage.py."
        )

    def test_file_storage_docstring(self):
        """TESTS IF FILE STORAGE HAS A DOCSTRING"""
        self.assertIsNot(file_storage.__doc__, None,
                         "File storage needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "File storage needs documentation")

    def test_file_storage_class_docstring(self):
        """TESTS IF THE FILESTORAGE CLASS HAS A DOCSTRING"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs documentation")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs documentation")

    def test_FileStorage_class_functions_docstrings(self):
        """TESTS FILE STORAGE CLASSES DOCSTRINGS"""
        for function in self.fs_f:
            self.assertIsNot(function[1].__doc__, None,
                             "{} method needs a docstring".format(function[0]))
            self.assertTrue(len(function[1].__doc__) >=1,
                            "{} method needs a dodcstring".format(function[0]))


class TestFileStorage(unittest.TestCase):
    """TESTS THE FILESTORAGE CLASS"""
    @unittest.skipIf(models.storage == "db", "not testin database")
    def test_all_returns_dict(self):
        storage = FileStorage()
        all_items = storage.all()
        self.assertEqual(type(all_items), dict)
        self.assertIs(all_items, storage._FileStorage__objects)

    @unittest.skipIf(models.storage == "db", "not testing database")
    def test_fileStorage_new_method(self):
        """TESTS THE FILESTORAGE METHOD NEW"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save
