#!/usr/bin/python3
"""A COMMENT CLASS"""
from models.base_model import BaseModel, Base
import models
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Comment(BaseModel):
    """
    DEFINES A COMMENT CLASS
    """
    if models.storage_type == "db":
        __tablename__ = "comments"
        text = Column(String(1024), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        recipe_id = Column(String(60), ForeignKey("recipes.id"), nullable=False)
    else:
        text = ""
        user_id = ""
        recipe_id = ""
