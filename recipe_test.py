#!/usr/bin/python3
from models.recipe import Recipe
import models

data = {"title": "small_chicken",
        "introduction": "a me thing",
        "ingredients": "chicken drumsticks",
        }

new = Recipe(**data)

print(new)


print(new.user_id)


