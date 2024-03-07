#!/usr/bin/python3
"""Test User for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import models
import time
import unittest
import uuid
from unittest import mock
from models.recipe import Recipe
User = models.user.User
module_doc = models.user.__doc__


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.user_funcs = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/user.py conforms to PEP8."""
        for path in ['models/user.py',
                     'tests/test_models/test_user.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "user.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "user.py needs a docstring")

    def test_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestUser(unittest.TestCase):
    """Test the User class"""
    @classmethod
    def setUpClass(cls):
        """
        DOES A CLASS SET UP
        """
        new_user = User(email="test_email",
                        password="test_password")
        new_recipe = Recipe(user_id=new_user.id,
                            title="empty",
                            introduction="empty",
                            ingredients="empty",
                            instructions="empty")

        cls.new_user = new_user
        cls.new_recipe = new_recipe

    def test_instantiation(self):
        """Test that object is correctly created"""
        user = User()
        self.assertIs(type(user), User)

    def test_attributes(self):
        """Test the presence of attributes"""
        user = User()
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'bio'))
        self.assertTrue(hasattr(user, '_favorites'))

    def test_favorites_property(self):
        """Test the favorites property"""
        user = User()
        self.assertIsInstance(user.favorites, list)

        self.new_user.favorites = self.new_recipe
        self.new_user.save()
        self.new_recipe.save()

        if models.storage_type == "db":
            self.assertIs(self.new_user.favorites[-1], self.new_recipe)
            self.assertIs(self.new_recipe.favorited_by[-1], self.new_user)

        else:
            self.assertIs(self.new_user.favorites[-1], self.new_recipe.id)
            self.assertTrue(
                self.new_recipe.favorited_by[-1] == self.new_user.id,
                """filestorage favorites not working""")

        self.new_user.delete()
        self.new_recipe.delete()

    def test_comments_property(self):
        """Test the comments property"""
        pass
