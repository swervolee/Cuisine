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
    def test_instantiation(self):
        """Test that object is correctly created"""
        recipe = Recipe()
        self.assertIs(type(recipe), Recipe)

    def test_attributes(self):
        """Test the presence of attributes"""
        recipe = Recipe()
        self.assertTrue(hasattr(recipe, 'title'))
        self.assertTrue(hasattr(recipe, 'introduction'))
        self.assertTrue(hasattr(recipe, 'ingredients'))
        self.assertTrue(hasattr(recipe, 'instructions'))
        self.assertTrue(hasattr(recipe, 'tags'))
        self.assertTrue(hasattr(recipe, 'servings'))
        self.assertTrue(hasattr(recipe, 'private'))
        self.assertTrue(hasattr(recipe, 'user_id'))

    def test_tags_property(self):
        """Test the tags property"""
        recipe = Recipe()
        self.assertIsInstance(recipe.tags, list)

    def test_comments_property(self):
        """Test the comments property"""
        recipe = Recipe()
        self.assertIsInstance(recipe.comments, list)
