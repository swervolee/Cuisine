#!/usr/bin/python3
"""Test Recipe for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
import uuid
import os
from models.tag import Tag
from models.user import User
from models.comment import Comment
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

    @classmethod
    def setUpClass(cls):
        """
        SET UP TEST
        """
        new_user = User(email="test_email", password="test_password")
        new_recipe = Recipe(user_id=new_user.id,
                            title="lunch",
                            introduction="empty",
                            ingredients="empty",
                            instructions="empty")
        new_tag = Tag(name="breakfast")
        new_comment = Comment(user_id=new_user.id,
                              recipe_id=new_recipe.id,
                              text="good cook")
        cls.new_user = new_user
        cls.recipe = new_recipe
        cls.new_recipe = new_recipe
        cls.new_comment = new_comment

    def test_instantiation(self):
        """Test that object is correctly created"""
        self.assertIsInstance(self.new_recipe, Recipe)

    @unittest.skipIf(os.getenv("CUISINE_TYPE_STORAGE") == "db", "FILESTORAGE")
    def test_attributes(self):
        """Test the presence of attributes"""
        self.assertTrue(hasattr(self.recipe, 'title'))
        self.assertTrue(hasattr(self.recipe, 'introduction'))
        self.assertTrue(hasattr(self.recipe, 'ingredients'))
        self.assertTrue(hasattr(self.recipe, 'instructions'))
        self.assertTrue(hasattr(self.recipe, '_tags'))
        self.assertTrue(hasattr(self.recipe, 'servings'))
        self.assertTrue(hasattr(self.recipe, 'private'))
        self.assertTrue(hasattr(self.recipe, 'user_id'))

        self.assertIs(type(self.recipe.title), str)
        self.assertIs(type(self.recipe.introduction), str)
        self.assertIs(type(self.recipe.ingredients), str)
        self.assertIs(type(self.recipe.instructions), str)
        self.assertIs(type(self.recipe._tags), list)
        self.assertIs(type(self.recipe.servings), int)
        self.assertIs(type(self.recipe.private), bool)
        self.assertIs(type(self.recipe.user_id), str)

    @unittest.skipIf(os.getenv("CUISINE_TYPE_STORAGE") == "db", "FILESTORAGE")
    def test_tags_property(self):
        """Test the tags property"""
        self.assertIs(type(self.recipe._tags), list)

    def test_tag_property(self):
        """
        TEST THE TAG PROPERTY FOR DB STORGE
        """
        new_user = User(email="test_email", password="test_password")
        new_recipe = Recipe(user_id=new_user.id,
                            title="lunch",
                            introduction="empty",
                            ingredients="empty",
                            instructions="empty")
        new_tag = Tag(name="lunch")
        new_recipe.tag = new_tag
        if models.storage_type != "db":
            self.assertTrue(new_recipe.tag[-1] == new_tag.id)
        else:
            self.assertTrue(new_recipe.tag[-1] == new_tag)

    def test_untag_method(self):
        """
        TESTS THE UNTAG METHOD OF RECIPE
        """
        new_user = User(email="test_email", password="test_password")
        new_recipe = Recipe(user_id=new_user.id,
                            title="lunch",
                            introduction="empty",
                            ingredients="empty",
                            instructions="empty")
        new_tag = Tag(name="lunch")
        new_recipe.tag = new_tag
        if models.storage_type != "db":
            self.assertTrue(new_recipe.tag[-1] == new_tag.id)
        else:
            self.assertTrue(new_recipe.tag[-1] == new_tag)

        new_recipe.untag(new_tag)

        if models.storage_type == "db":
            self.assertTrue(new_tag not in new_recipe.tag)
        else:
            self.assertTrue(new_tag.id not in new_recipe.tag)

    def test_comments_property(self):
        """Test the comments property"""
        self.assertIsInstance(self.recipe.comments, list)

    def test_comment_recipe_relationship(self):
        """
        TEST THE COMMENT RECIPE RELATIONSHIP
        """
        self.new_user.save()
        self.new_recipe.save()
        self.new_comment.save()
        self.assertTrue(self.new_recipe.comments != [],
                        "Comment was not created")

        self.new_user.delete()
        self.new_recipe.delete()
        self.new_comment.delete()
