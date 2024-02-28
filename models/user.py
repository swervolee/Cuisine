#!/usr/bin/python3
"""
A MODEL FOR USERS
"""
from models.base_model import BaseModel
from models import storage


class User(BaseModel):
    """
    USERS MODEL
    -------------
    FIRST_NAME - USERS FIRST NAME
    LAST_NAME - USERS LAST NAME
    EMAIL - EMAIL OF THE USER
    PASSWORD - USERS PASSWORD.THE PASSWORD WILL BE HASHED
    BIO - SMALL INFO ABOUT THE USER.(OPTIONAL)
    FAVORITES - USERS FAVOURITE RECIPES ID
    COMMENTS - IDS OF COMMENTS THAT HAVE BEEN CREATED BY THE USER
    """

    first_name = ""
    last_name = ""
    email = ""
    password = ""
    bio = ""
    favorites = []

    @property
    def favorites(self):
        """FAVOURITE RECIPES ID"""
        return self.favorites

    @favorites.setter
    def favorites(self, value):
        """ADDS TO FAVOURITES LIST"""
        if isinstance(value, str):
            self.favorites.append(value)

    def unfavorite(self, value):
        """DELETE A RECIPE FROM FAVOURITES"""
        if value in self.favorites:
            self.favorites.remove(value)

    @property
    def recipes(self):
        """RETURNS RECIPES CREATED BY THE USER"""
        result = []
        for item in storage.all(Recipe):
            if item.user_id == self.id:
                result.append(item.id)
        return result



    @property
    def comments(self):
        """COMMENTS CREATED BY THE USER"""
        result = []
        for item in storage.all(Recipe):
            if item.user_id == self.id:
                result.append(item.id)
