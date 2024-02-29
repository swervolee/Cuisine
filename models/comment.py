#!/usr/bin/python3
"""A COMMENT CLASS"""
from models.base_model import BaseModel


class Comment(BaseModel):
    """
    DEFINES A COMMENT CLASS
    """
    text = ""
    user_id = ""
    recipe_id = ""
