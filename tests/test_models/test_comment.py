#!/usr/bin/python3
"""Test Comment for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
import uuid
from unittest import mock
Comment = models.comment.Comment
module_doc = models.comment.__doc__


class TestCommentDocs(unittest.TestCase):
    """Tests to check the documentation and style of Comment class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.comment_funcs = inspect.getmembers(Comment, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/comment.py conforms to PEP8."""
        for path in ['models/comment.py',
                     'tests/test_models/test_comment.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "comment.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "comment.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Comment class docstring"""
        self.assertIsNot(Comment.__doc__, None,
                         "Comment class needs a docstring")
        self.assertTrue(len(Comment.__doc__) >= 1,
                        "Comment class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Comment methods"""
        for func in self.comment_funcs:
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


class TestComment(unittest.TestCase):
    """Test the Comment class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        comment = Comment()
        self.assertIs(type(comment), Comment)
