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
