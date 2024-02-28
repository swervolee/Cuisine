#!/usr/bin/python3
"""A COMMENT CLASS"""
from models.base_model import BaseModel



class Comment(BaseModel):
    """CREATES AND SETS A COMMENT MODEL"""
    text = ""
    user_id = ""
    recipe_id = ""
