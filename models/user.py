#!/usr/bin/python3
"""USER CLASS"""
import models
from models.base_model import BaseModel, Base
from models.comment import Comment
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

# SQLAlchemy setup
if models.storage_type == "db":
    favorites_table = Table('favorites', Base.metadata,
                            Column('user_id', String(128),
                                   ForeignKey('users.id')),
                            Column('recipe_id', String(128), ForeignKey(
                                'recipes.id')))


class User(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS BASEMODEL
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
        favorites = relationship("Recipe",
                                 secondary=favorites_table,
                                 backref="favorited_by")
    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""
        bio = ""
        _favorites = []

    def favorite(self, recipe_id):
        """Adds a recipe to favorites."""
        if models.storage_type == "db":
            if recipe_id not in [recipe.id for recipe in self.favorites]:
                self.favorites.append(models.storage.get(Recipe, recipe_id))
        else:
            if recipe_id not in self._favorites:
                self._favorites.append(recipe_id)

    def unfavorite(self, recipe_id):
        """Removes a recipe from favorites."""
        if models.storage_type == "db":
            for recipe in self.favorites:
                if recipe.id == recipe_id:
                    self.favorites.remove(recipe)
                    break
        else:
            if recipe_id in self._favorites:
                self._favorites.remove(recipe_id)

    if models.storage_type != 'db':
        @property
        def favorites(self):
            """Returns favorited recipes."""
            if models.storage_type == "db":
                return [recipe.id for recipe in self.favorites]
            else:
                return self._favorites

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
