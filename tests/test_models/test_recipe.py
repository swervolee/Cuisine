#!/usr/bin/python3
"""Test Recipe for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
import uuid
from unittest import mock
Recipe = models.recipe.Recipe
module_doc = models.recipe.__doc__


class TestRecipeDocs(unittest.TestCase):
    """Tests to check the documentation and style of Recipe class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.recipe_funcs = inspect.getmembers(Recipe, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/recipe.py conforms to PEP8."""
        for path in ['models/recipe.py',
                     'tests/test_models/test_recipe.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "recipe.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "recipe.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Recipe class docstring"""
        self.assertIsNot(Recipe.__doc__, None,
                         "Recipe class needs a docstring")
        self.assertTrue(len(Recipe.__doc__) >= 1,
                        "Recipe class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Recipe methods"""
        for func in self.recipe_funcs:
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


class TestRecipe(unittest.TestCase):
    """Test the Recipe class"""

    def setUp(self):
        """
        SET UP TEST
        """
        self.recipe = Recipe()

    def test_instantiation(self):
        """Test that object is correctly created"""
        self.assertIsInstance(self.recipe, Recipe)

    def test_attributes(self):
        """Test the presence of attributes"""
        self.assertTrue(hasattr(self.recipe, 'title'))
        self.assertTrue(hasattr(self.recipe, 'introduction'))
        self.assertTrue(hasattr(self.recipe, 'ingredients'))
        self.assertTrue(hasattr(self.recipe, 'instructions'))
        self.assertTrue(hasattr(self.recipe, 'tags'))
        self.assertTrue(hasattr(self.recipe, 'servings'))
        self.assertTrue(hasattr(self.recipe, 'private'))
        self.assertTrue(hasattr(self.recipe, 'user_id'))

        self.assertIs(type(self.recipe.title), str)
        self.assertIs(type(self.recipe.introduction), str)
        self.assertIs(type(self.recipe.ingredients), str)
        self.assertIs(type(self.recipe.instructions), str)
        self.assertIs(type(self.recipe.tags), list)
        self.assertIs(type(self.recipe.servings), int)
        self.assertIs(type(self.recipe.private), bool)
        self.assertIs(type(self.recipe.user_id), str)

    def test_tags_property(self):
        """Test the tags property"""
        self.assertIs(type(self.recipe.tags), list)

    def test_comments_property(self):
        """Test the comments property"""
        self.assertIsInstance(self.recipe.comments, list)
