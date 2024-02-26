#!/usr/bin/python3
"""FILE STORAGE UNITTESTS"""
import inspect
import models
import pep8
import unittest
import json
FileStorage = models.engine.file_storage.FileStorage


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
        self.assertEqual(result.total_errors, 0, "Found code style errors.")

    def test_pep8_test_file_storage(self):
        """TESTS PEP8 CONFORMANCE OF THE TEST FILE"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files([
            "modles/tests/test_models/test_engine/test_file_storage"])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")
