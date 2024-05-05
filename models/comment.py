#!/usr/bin/python3
"""A COMMENT CLASS"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Comment(BaseModel, Base):
    """
    DEFINES A COMMENT CLASS
    """
    if models.storage_type == "db":
        __tablename__ = "comments"
        text = Column(String(1024), nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'), nullable=False)
        recipe_id = Column(String(60),
                           ForeignKey("recipes.id"), nullable=False)
    else:
        text = ""
        user_id = ""
        recipe_id = ""

    if models.storage_type != "db":
        @property
        def user(self):
            """
            FETCHES THE COMMENT WRITER
            """
            if self.user_id != "":
                user = models.storage.get("User", self.user_id)
                return user

        @property
        def recipe(self):
            """
            FETCHES THE RECIPE COMMENTED
            """
            if self.recipe_id:
                recipe = models.storage.get("Recipe", self.recipe_id)
                return recipe
