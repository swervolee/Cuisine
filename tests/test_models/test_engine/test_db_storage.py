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
DBStorage = db_storage.DBStorage

classes = {"BaseModel": BaseModel,
           "User": User,
           "Recipe": Recipe,
           "Tag": Tag,
           "Comment": Comment
           }

class TestDBStorge_docs(uinttest.TestCase):
    """
    TEST DBSTORAGE DOCS
    """
    def setUpClass(cls):
        """
        TEST SETUP
        """
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)
        
