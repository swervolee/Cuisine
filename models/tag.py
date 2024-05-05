#!/usr/bin/python3
"""TAG CLASS"""
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Tag(BaseModel, Base):
    """DEFINES A CLASS TAG
    -----------------------
    NAME - NAME OF THE TAG
    """
    if models.storage_type == "db":
        __tablename__ = 'tags'
        name = Column(String(128), nullable=False)
    else:
        name = ""
