#!/usr/bin/python3
"""USER CLASS"""
import models
from models.base_model import BaseModel
from models.comment import Comment


class User(BaseModel):
    """
    CONSTRUCTS THE CLASS BASEMODEL
    """
    first_name = ""
    last_name = ""
    email = ""
    password = ""
    bio = ""
    _favorites = []

    @property
    def favorites(self):
        """RETURNS FAVOURITED RECIIPES ID LIST"""
        return self._favorites

    @favorites.setter
    def favorites(self, value):
        """ADDS TO THE FAVOURITES LIST"""
        if isinstance(value, str):
            self._favorites.append(value)

    def unfavorite(self, value):
        """REMOVE AN ID FROM FAVOURITES"""
        if value in self._favorites:
            self._favorites.remove(value)

    @property
    def recipes(self):
        """RETURNS A LIST OF IDS CREATED BY THE USER"""
        result = []
        for item in models.storage.all(Recipe).values():
            if item.user_id == self.id:
                result.append(item.id)
        return result

    @property
    def comments(self):
        """RETURNS A LIST OF COMMENTS BY THE USER"""
        result = []
        for item in models.storage.all(Comment).values():
            if item.user_id == self.id:
                result.append(item.id)
        return result
