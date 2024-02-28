#!/usr/bin/python3
"""A CLASS RECIPES"""
from models.base_model import BaseModel
from models.comment import Comment


class Recipe(BaseModel):
    """A CLASS RECIPE"""
    title = ""
    introduction = ""
    ingredients = []
    instructions = []
    tags = []
    servings = 0
    private = False
    user_id = ""

    @property
    def tags(self):
        """RETURNS ID OF ASSOCIATED TAGS"""
        return self.tags;

    @tags.setter
    def tags(self, value):
        """ASSOCIATES A RECIPE WITH A TAG"""
        if value and isintance(value, str) and value not in self.tags:
            tags.append(value)

    def untag(self, value):
        """UNTAGS A RECIPE"""
        if value in self.tags:
            self.tags.remove(value)

    @property
    def comments(self):
        """RETURNS IDS OF COMMENTS ASSOCIATED WITH THE RECIPE"""
        result = []
        for item in storage.all(Comment):
            if item.recipe == self.id:
                result.append(item.id)
        return result
