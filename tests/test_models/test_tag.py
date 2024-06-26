#!/usr/bin/python3
"""Test Tag for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
import uuid
from unittest import mock
Tag = models.tag.Tag
module_doc = models.tag.__doc__


class TestTagDocs(unittest.TestCase):
    """Tests to check the documentation and style of Tag class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.tag_funcs = inspect.getmembers(Tag, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/tag.py conforms to PEP8."""
        for path in ['models/tag.py',
                     'tests/test_models/test_tag.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "tag.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "tag.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Tag class docstring"""
        self.assertIsNot(Tag.__doc__, None,
                         "Tag class needs a docstring")
        self.assertTrue(len(Tag.__doc__) >= 1,
                        "Tag class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Tag methods"""
        for func in self.tag_funcs:
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


class TestTag(unittest.TestCase):
    """Test the Tag class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        tag = Tag()
        self.assertIs(type(tag), Tag)
