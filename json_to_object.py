#!/usr/bin/python3
"""
This module tries to synchronize to database
the filestorage objects
"""
import json
from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models.comment import Comment

data = None
try:
    with open("file.json", "r") as f:
        data = json.load(f)

    for i in data:
        new = eval(data[i]["__class__"])(**data[i])
        if new.__class__.__name__ == "Recipe":
            new.user_id = "98503c43-481b-4b76-92ca-cef42f4bf16f"
            new.save()
except Exception:
    print("Error")