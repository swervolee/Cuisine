#!/usr/bin/python3
"""A CLASS RECIPES"""
from models.base_model import BaseModel
from models.comment import Comment
import models


class Recipe(BaseModel):
    """
    DEFINES THE RECIPE CLASS
    """
    title = ""
    introduction = ""
    ingredients = []
    instructions = []
    _tags = []
    servings = 0
    private = False
    user_id = ""

    @property
    def tags(self):
        """
        RETURNS A LIST OF TAGS ASSOCIATED WITH THE RECIPE
        """
        return self._tags

    @tags.setter
    def tags(self, value):
        """
        ASSOCIATES A RECIPE WITH A TAG
        """
        if value and isinstance(value, str) and value not in self._tags:
            self._tags.append(value)

    def untag(self, value):
        """
        UNTAG A RECIPE
        """
        if value in self._tags:
            self._tags.remove(value)

    @property
    def comments(self):
        """
        RETURNS A LIST OF COMMENT IDS ASSOCIATED WITH A CLASS
        """
        result = []
        for item in models.storage.all(Comment).values():
            if item.recipe_id == self.id:
                result.append(item.id)
        return result
