#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
import os

os.environ["CUISINE_TYPE_STORAGE"] = "db"

storage_type = getenv('CUISINE_TYPE_STORAGE')

#if storage_type == "db":
from models.engine.db_storage import DBStorage
storage = DBStorage()
# else:
#    from models.engine.file_storage import FileStorage
#    storage = FileStorage()

storage.reload()
