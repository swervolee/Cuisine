#!/usr/bin/python3
"""A CLASS RECIPES"""
from models.base_model import BaseModel, Base
from models.comment import Comment
from models.tag import Tag
import models
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Table, String, Integer, ForeignKey, Boolean
from os import getenv


if models.storage_type == "db":
    tag_recipe = Table('tag_recipe', Base.metadata,
                       Column('recipe_id', String(60),
                              ForeignKey('recipes.id', onupdate="CASCADE",
                                         ondelete="CASCADE"),
                              primary_key=True),
                       Column('tag_id', String(60),
                              ForeignKey('tags.id', onupdate="CASCADE",
                                         ondelete="CASCADE"),
                              primary_key=True))


class Recipe(BaseModel, Base):
    """
    DEFINES THE RECIPE CLASS
    """

    if models.storage_type == "db":
        __tablename__ = "recipes"
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        title = Column(String(60), nullable=False)
        introduction = Column(String(60), nullable=False)
        ingredients = Column(String(60), nullable=False)
        instructions = Column(String(60), nullable=False)
        private = Column(Boolean, default=False)
        servings = Column(Integer, default=0)
        _tags = relationship("Tag", secondary="tag_recipe",
                             backref="recipe_tags",
                             viewonly=False)
        comments = relationship("Comment",
                                backref="recipe",
                                cascade="all, delete-orphan")
    else:
        user_id = ""
        title = ""
        introduction = ""
        ingredients = ""
        instructions = ""
        private = False
        servings = 0
        _tags = []  # Define _tags attribute to store Tag objects

    @property
    def tag(self):
        """
        RETURNS A LIST OF TAGS ASSOCIATED WITH THE RECIPE
        """
        return self._tags

    @tag.setter
    def tag(self, value):
        """
        ASSOCIATES A RECIPE WITH A TAG
        """
        if value.__class__.__name__ == "Tag":
            if models.storage_type != "db":
                if value.id not in self._tags:
                    self._tags.append(value.id)
            else:
                if value not in self._tags:
                    self._tags.append(value)

    def untag(self, value):
        """
        UNTAG A RECIPE
        """
        if models.storage_type == "db":
            if value in self._tags:
                self._tags.remove(value)
        else:
            if value.id in self._tags:
                self._tags.remove(value.id)

    if models.storage_type != "db":
        @property
        def comments(self):
            """
            RETURNS A LIST OF COMMENTS ASSOCIATED WITH THE RECIPE
            """
            result = []
            for item in models.storage.all("Comment").values():
                if item.recipe_id == self.id:
                    result.append(item)
            return result

        @property
        def favorited_by(self):
            """
            A LIST OF USERS WHO HAVE FAVORITED THIS RECIPE
            """
            users = models.storage.all("User").values()
            result = []

            for person in users:
                favs = person.favorites
                if self.id in favs:
                    result.append(person.id)
            return result
