#!/usr/bin/python3
"""A CLASS RECIPES"""
from models.base_model import BaseModel, Base
from models.comment import Comment
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
        tags = relationship("Tag", secondary="tag_recipe",
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
        _comments = []  # Define _comments attribute to store Comment objects

    if models.storage_type != "db":
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
            if isinstance(value, Tag) and value not in self.tags:
                self._tags.append(value)

        def untag(self, value):
            """
            UNTAG A RECIPE
            """
            if value in self.tags:
                self._tags.remove(value)

        @property
        def comments(self):
            """
            RETURNS A LIST OF COMMENTS ASSOCIATED WITH THE RECIPE
            """
            return self._comments

        @comments.setter
        def comments(self, value):
            """
            ASSOCIATES A RECIPE WITH A COMMENT
            """
            if isinstance(value, Comment) and value not in self._comments:
                self._comments.append(value.id)
