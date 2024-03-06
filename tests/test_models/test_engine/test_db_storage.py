#!/usr/bin/python3
"""
DATABASE TESTS
"""

from datetime import datetime
import inspect
from models.engine import db_storage
from models import storage
import os
import json
import unittest
from models.base_model import BaseModel
from models.recipe import Recipe
from models.user import User
from models.tag import Tag
from models.comment import Comment
import pep8
DBStorage = db_storage.DBStorage

classes = {"BaseModel": BaseModel,
           "User": User,
           "Recipe": Recipe,
           "Tag": Tag,
           "Comment": Comment
           }


class TestDBStorge_docs(unittest.TestCase):
    """
    TEST DBSTORAGE DOCS
    """
    @classmethod
    def setUpClass(cls):
        """
        TEST SETUP
        """
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_comformance_db_storage(self):
        """
        TEST WHETHER DB STORAGAE PASSES PEP8
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors")

    def test_test_db_storage_pep8(self):
        """
        CHECKS IF THIS FILE COMFORMS TO PEP8
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ["tests/test_models/test_engine/test_db_storage.py"])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors")

    def test_db_storage_docstrings(self):
        """
        TEST DOCSTRINGS
        """
        for item in [db_storage.__doc__, DBStorage.__doc__]:
            with self.subTest(function=item):
                self.assertIsNot(item, None)
                self.assertTrue(len(item) > 1,
                                "db  storage missing docstring")

    def test_db_storage_func_docstring(self):
        """
        TEST DB FUNCTIONS DOCSTRNGS
        """
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) > 1,
                            "{:s} method needs a docstring".format(func[0]))

class Test_DbStorage(unittest.TestCase):
    """
    TEST DB STORAGE
    """
    @unittest.skipIf(models.storage_t != "db", "Not testing filestorage")
    def test_all_method(self):
        """
        TESTS TEH ALL METHOD OF DBSTORAGE
        """
        self.assertIs(type(models.storage.all()), dict)
