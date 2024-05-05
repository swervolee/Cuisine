#!/usr/bin/python3
"""
DATABASE TESTS
"""

from datetime import datetime
import inspect
from models.engine import db_storage
from models import storage
import os
import models
import json
import unittest
from models.base_model import BaseModel
from models.recipe import Recipe
from models.user import User
from models.tag import Tag
from models.comment import Comment
import pep8
import MySQLdb

DBStorage = db_storage.DBStorage

classes = {"user": User,
           "recipe": Recipe,
           "tag": Tag,
           "comment": Comment
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


strg = models.storage_type != "db"
msg = "Not testing FileStorge"


class Test_DbStorage(unittest.TestCase):
    """
    TEST DB STORAGE
    """
    @classmethod
    def setUpClass(cls):
        """
        DOES A CLASS SETUP
        """
        cls.clist = ["users", "recipes", "tags", "comments"]
        db = MySQLdb.connect(host="localhost",
                             user="cuisine_dev",
                             password="cuisine_dev_pwd",
                             db="cuisine_dev_db")
        cls.cur = db.cursor()

    @unittest.skipIf(strg, msg)
    def test_all_method(self):
        """
        TESTS TEH ALL METHOD OF DBSTORAGE
        """
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(strg, msg)
    def test_all_method_without_class(self):
        """
        TEST ALL METHOD WITHOUT ARGUMENTS
        """
        def count_items():
            count = 0
            for item in self.clist:
                self.cur.execute(f"SELECT * FROM {item}")
                count += len(self.cur.fetchall())
            return count

        self.assertTrue(count_items() == len(models.storage.all()),
                        "Models.storage.all should return all classes")

    @unittest.skipIf(strg, msg)
    def test_all_method_with_a_class(self):
        """
       TEST ALL METHOD WITH ARGUMENTS
        """
        for item in classes.keys():
            self.cur.execute(f"SELECT * FROM {item}s")
            self.assertTrue(len(models.storage.
                                all(classes[item])
                                ) == len(self.cur.fetchall()))

    @unittest.skipIf(strg, msg)
    def test_new_method(self):
        """
        TESTS THE NEW METHOD OF FILESTORAGE
        """
        before = len(models.storage.all("User"))
        arguments = {"email": "test@email",
                     "password": "test_password"}
        new = User(**arguments)
        models.storage.new(new)
        self.assertTrue(new in models.storage.all().values(),
                        "Object not stored")

    @unittest.skipIf(strg, msg)
    def test_save_method(self):
        """
        TEST DB SAVE METHOD
        """
        arguments = {"email": "test@email",
                     "password": "test@password"}

        new = User(**arguments)
        models.storage.new(new)
        models.storage.save()

        db = MySQLdb.connect(host="localhost",
                             user="cuisine_dev",
                             password="cuisine_dev_pwd",
                             db="cuisine_dev_db")

        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE id=%s",
                       (new.id,))

        all_user = cursor.fetchone()

        self.assertTrue(all_user, "Save method not working")

    @unittest.skipIf(strg, msg)
    def test_get_db(self):
        """
        TEST THE GET METHOD OF DBSTORAGE
        """
        new = Tag(name="breakfast")
        new.save()

        get_instance = models.storage.get(Tag, new.id)
        self. assertEqual(get_instance, new)

    @unittest.skipIf(strg, msg)
    def test_count(self):
        """
        TEST THE COUNT METHOD OF DB STORGE
        """
        for item in classes.keys():
            self.cur.execute(f"SELECT * FROM {item}s")
            self.assertEqual(models.storage.count(classes[item]),
                             len(self.cur.fetchall()),
                             "Count method not working right")
