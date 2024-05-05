#!/usr/bin/python3
"""
THIS IS A MODULE TO CREATE DUMMY RECIPE DATA
"""
import random
from os import getenv
from models.recipe import Recipe
import models
import sys

def generate_recipe(mode=None):
    recipe = {
        'user_id': '98503c43-481b-4b76-92ca-cef42f4bf16f',
        'title': 'Recipe ' + str(random.randint(1, 100)),
        'description': 'Description for recipe ' + str(random.randint(1, 100)),
        'introduction': 'Introduction for recipe' + str(random.randint(1, 100)),
        'ingredients': "\n".join([f'Ingredient {i}' for i in range(random.randint(3, 10))]),
        'instructions': "\n".join([f'Instruction {i}' for i in range(random.randint(3, 10))])
    }
    return recipe

try:
    mode = sys.argv[1]

    if  mode == "create":
        for i in range(100):
            new = Recipe(**generate_recipe())
            new.save()
    elif mode == "destroy":
        all_recipes = models.storage.all("Recipe").values()
        for i in all_recipes:
            i.delete()
        models.storage.save()
except Exception:
    pass