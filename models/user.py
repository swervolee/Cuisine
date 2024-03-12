#!/usr/bin/python3
"""USER CLASS"""
import models
from models.base_model import BaseModel, Base
from models.comment import Comment
from models.recipe import Recipe
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

# SQLAlchemy setup
if models.storage_type == "db":
    favorites_table = Table('favourites', Base.metadata,
                            Column('user_id', String(128),
                                   ForeignKey('users.id')),
                            Column('recipe_id', String(128), ForeignKey(
                                'recipes.id')))


class User(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS USER
    """
    if models.storage_type == "db":

        __tablename__ = "users"

        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        bio = Column(String(1024), nullable=True)
        recipes = relationship("Recipe",
                               backref="user",
                               cascade="all, delete-orphan")
        comments = relationship("Comment",
                                backref="user",
                                cascade="all, delete-orphan")
        _favorites = relationship("Recipe",
                                  secondary=favorites_table,
                                  backref="favorited_by")
    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""
        bio = ""
        _favorites = []
        _comments = []

    @property
    def favorites(self):
        """
        RETURN S A LIST OF FAVORITED ITEMS
        """
        return self._favorites

    @favorites.setter
    def favorites(self, value):
        """
        RETURNS A LIST OF FAVOURITED RECIPES
        """
        if models.storage_type == "db":
            if value not in self._favorites:
                self.favorites.append(value)
        else:
            if value.id not in self._favorites:
                self._favorites.append(value.id)

    def unfavorite(self, value):
        """Removes a recipe from favorites."""
        if models.storage_type == "db" and value in self._favorites:
            self._favorites.remove(value)
        else:
            if value.id in self._favorites:
                self._favorites.remove(value)

    if models.storage_type != "db":
        @property
        def recipes(self):
            """Returns a list of recipe IDs created by the user."""
            result = []
            for item in models.storage.all(Recipe).values():
                if item.user_id == self.id:
                    result.append(item.id)
            return result

        @property
        def comments(self):
            """Returns a list of comments by the user."""
            result = []
            for item in models.storage.all(Comment).values():
                if item.user_id == self.id:
                    result.append(item.id)
            return result
